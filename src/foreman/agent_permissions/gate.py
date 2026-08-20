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
import sys
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


def _bash_decision(cmd: str, mode: str, cwd: str) -> tuple[str, str] | None:
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
