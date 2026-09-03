"""The PreToolUse hook.

Runs before every Bash/Read/Write tool call, so it does two things and exits.

  1. FILE TOOLS are re-checked against the filesystem, because a native
     `Edit(//tmp/**)` allow rule matches the path as a STRING and a symlink at
     /tmp/x pointing to ~/.zshrc satisfies it.

  2. BASH commands are gated by the per-project policy resolved at call time.

Failure policy: this fails CLOSED. The shell implementation fell through to "no
opinion" if jq was missing, so on an image without jq `sudo rm -rf /` went from
"ask" to unguarded, silently. A guard that disappears with a dependency is worse
than no guard, because you believe you have one.
"""

from __future__ import annotations

import json
import os
import re
import sys
import tomllib
from pathlib import Path

from . import match, store
from .model import ALLOW, ALWAYS, ASK, DENY, GATED, SAFE, TRUSTED

TEMP_ROOTS = ("/tmp", "/private/tmp")


def _emit(decision: str, reason: str) -> None:
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": decision,
                "permissionDecisionReason": reason,
            }
        },
        sys.stdout,
    )


def _deepest_existing(p: Path) -> Path:
    """The deepest ancestor of *p* that exists, following the shell's -e/-L logic.

    A write target usually does not exist yet, and a symlink can only live in
    the part of the path that already does. The is_symlink() test is
    load-bearing: exists() follows links, so a dangling link looks absent, the
    walk climbs past it, and the path reads as temp — while the write still
    lands at the link target. A file that does not exist yet is exactly the
    interesting case; ~/.zshenv does not either, and every shell sources it.
    """
    while not p.exists() and not p.is_symlink():
        if p.parent == p:
            return p
        p = p.parent
    return p


def _under_temp(path: str) -> bool:
    real = os.path.realpath(_deepest_existing(Path(path)))
    return any(real == r or real.startswith(r + os.sep) for r in TEMP_ROOTS)


def _file_tool_decision(path: str) -> tuple[str, str] | None:
    if not path:
        return None
    if not any(path == r or path.startswith(r + os.sep) for r in TEMP_ROOTS):
        # Not temp-looking: no opinion. The normal flow and the deny rules decide.
        return None
    if _under_temp(path):
        return None
    return ASK, "Temp-looking path resolves outside /tmp"


# --------------------------------------------------------------------------
# Bundle enforcement — a separate question, deliberately kept apart.
#
# This shares nothing with the permission policy below: a different input, a
# different owner, a different meaning. **Permissions are the operator's, and
# they are settable. This is the project's, and it is not.** Nothing in
# `agent-permissions` reads or writes `routing.toml`, there is no key for it and
# no flag, and that is what "cannot be turned off" means in practice.
#
# It is consulted *first* and its answer is final, because a rule a Bundle
# declares as blocking is not a preference that a preference can outrank.
#
# The only ways out are to stop adopting the Bundle or to fork it into your own
# namespace — both visible in `MANIFEST.md`, where editing the vendored copy
# instead is drift that `inspect` reports.


def _project_root(start: str) -> Path | None:
    """The nearest ancestor holding `.luma/`, or None."""
    here = Path(start or os.getcwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / ".luma").is_dir():
            return candidate
    return None


def _command_fires(shape: str, cmd: str) -> bool:
    """Does *cmd* invoke the command *shape* names?

    A shape is a literal invocation — `git commit`, `git push --force` — and
    matching is on word boundaries. `git commitmsg` is a different command and
    must not be caught by a rule about committing, which is the difference
    between a guardrail and a nuisance.
    """
    if not shape:
        return False
    pattern = r"(?<![\w-])" + r"\s+".join(re.escape(w) for w in shape.split()) + r"(?![\w-])"
    return re.search(pattern, cmd) is not None


def _refused_by_bundle(cmd: str, cwd: str) -> tuple[str, str] | None:
    """A rule this project adopted that refuses *cmd*, if there is one.

    Reads the compiled table rather than the Bundles themselves. This runs
    before **every** tool call, and walking `.luma/bundles/` to parse
    frontmatter each time would cost more than the whole gate does.
    """
    root = _project_root(cwd)
    if root is None:
        return None
    table = root / ".luma" / "bundles" / "routing.toml"
    try:
        with table.open("rb") as fh:
            data = tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError):
        return None

    for rule in data.get("rule", []):
        if rule.get("on_violation") != "block":
            continue
        for trigger in rule.get("matches", []):
            kind, _, shape = str(trigger).partition(":")
            if kind == "command" and _command_fires(shape, cmd):
                title = rule.get("title") or rule.get("document", "an adopted rule")
                where = rule.get("path", "")
                return DENY, (
                    f"Refused by {title} — a rule this project adopted, which "
                    f"blocks this. Read {where} for what to do instead. This "
                    f"cannot be overridden by permissions; it changes when the "
                    f"bundle does."
                )
    return None


def _bash_decision(cmd: str, mode: str, cwd: str) -> tuple[str, str] | None:
    # First, and final. See above: this is the project's rule, not the
    # operator's preference, so no permission value and no mode outranks it.
    refused = _refused_by_bundle(cmd, cwd)
    if refused:
        return refused

    pol = store.resolve_for(cwd or os.getcwd())

    # Pass 1 — "always" and "deny" run above the bypass short-circuit, so they
    # fire in every mode.
    for key in GATED:
        value = pol[key.name]
        if value == ALWAYS and match.matches(key.name, cmd):
            return ASK, f"Gated in every mode by policy ({key.name}=always)"
        if value == DENY and match.matches(key.name, cmd):
            return DENY, f"Refused by policy ({key.name}=deny)"

    # bypassPermissions is a per-session opt-out; trust="full" a per-project one.
    if mode == "bypassPermissions" or pol["trust"] == "full":
        return None

    # Pass 2 — gated during ordinary work, silent under bypass or full trust.
    for key in GATED:
        value = pol[key.name]
        if value in (ALLOW, ALWAYS, DENY) or not match.matches(key.name, cmd):
            continue
        if value == ASK:
            return ASK, f"Gated outside bypass mode ({key.name}=ask)"
        if value == TRUSTED and key.name == "ssh":
            if not match.ssh_trusted(cmd, pol["ssh_hosts"]):
                return ASK, "ssh host is not on ssh_hosts"
        elif value == SAFE:
            if match.fetch_unsafe(cmd):
                return ASK, f"{key.name} writes to disk, uploads, or pipes to a shell"
        else:
            return ASK, f"Unknown policy value for {key.name}: {value}"
    return None


def main(argv: list[str] | None = None) -> int:
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw.strip() else {}
        tool = event.get("tool_name") or ""
        tool_input = event.get("tool_input") or {}

        if tool in ("Read", "Write", "Edit", "MultiEdit", "NotebookEdit"):
            path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
            result = _file_tool_decision(str(path))
        elif tool == "Bash":
            result = _bash_decision(
                str(tool_input.get("command") or ""),
                str(event.get("permission_mode") or "default"),
                str(event.get("cwd") or ""),
            )
        else:
            result = None

        if result:
            _emit(*result)
        return 0
    except Exception as exc:  # noqa: BLE001 — deliberately broad; see module docstring
        # Fail closed. Something is wrong with the gate itself, which is exactly
        # when silence is most dangerous.
        _emit(ASK, f"Permission gate failed and is asking to be safe: {exc.__class__.__name__}")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
