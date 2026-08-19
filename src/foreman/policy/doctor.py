"""Checking that the gate actually works, not merely that it is wired up.

`install` answers "is it connected". That is not the question that matters: a
gate can be installed, wired, and silently returning nothing, and `install` will
call it perfect while it protects you from nothing. Verifying that by hand is
what turned up the deny-blocks-its-own-undo lockout.

The behaviour checks run the INSTALLED gate — the file Claude Code executes —
against a TEMPORARY policy directory, so this never reads or writes the policy
actually in use.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from . import install as _install
from . import model, store


class Report:
    def __init__(self) -> None:
        self.checks: list[dict[str, str]] = []
        self.current = ""

    def section(self, name: str) -> None:
        self.current = name

    def _add(self, status: str, text: str) -> None:
        self.checks.append({"status": status, "check": text, "section": self.current})

    def ok(self, text: str) -> None:
        self._add("ok", text)

    def bad(self, text: str) -> None:
        self._add("fail", text)

    def warn(self, text: str) -> None:
        self._add("warn", text)

    @property
    def failures(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "fail")

    @property
    def passes(self) -> int:
        return sum(1 for c in self.checks if c["status"] == "ok")


def _decide(gate: Path, home: Path, cmd: str, cwd: str, mode: str = "default") -> str:
    event = json.dumps(
        {"tool_name": "Bash", "permission_mode": mode, "cwd": cwd, "tool_input": {"command": cmd}}
    )
    env = {**os.environ, "LUMA_FOREMAN_HOME": str(home)}
    try:
        out = subprocess.run(
            [str(gate)], input=event, capture_output=True, text=True, env=env, timeout=20
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return "error"
    if not out.strip():
        return "none"
    try:
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return "malformed"


def run(as_json: bool = False) -> int:
    home = store.home()
    gate = _install.gate_path()
    report = Report()

    report.section("installation")
    # -- installation --------------------------------------------------------
    if os.access(gate, os.X_OK):
        report.ok(f"gate installed at {gate}")
    else:
        report.bad(f"no executable gate at {gate} — run: luma-foreman policy install")

    if gate.exists():
        state = _install.status()
        if state == "already current":
            report.ok("installed gate matches this version")
        else:
            report.bad("installed gate is out of date — run: luma-foreman policy install")

    stale = Path.home() / ".claude" / "permission-gate.sh"
    if stale.exists():
        report.warn(f"a stale gate remains at {stale} — delete it")
    for old in _install.legacy_install():
        report.warn(
            f"a directory from an earlier layout remains at {old} — run "
            "`luma-foreman policy install`, apply the settings.json changes it prints, "
            "then delete it"
        )

    report.section("claude code wiring")
    # -- wiring --------------------------------------------------------------
    wiring = _install.wiring()
    if wiring["exists"]:
        report.ok(f"settings found at {wiring['settings']}")
        if wiring["hook_ok"]:
            report.ok("PreToolUse hook points at the installed gate")
        else:
            report.bad("no PreToolUse hook points at the gate — run: luma-foreman policy install")
        if wiring["deny_ok"]:
            report.ok("deny rule protects the policy directory")
        else:
            report.bad("no deny rule protects the policy directory; an agent can rewrite its own rules")
    else:
        report.bad(f"no settings file at {wiring['settings']}")

    # -- behaviour -----------------------------------------------------------
    report.section("behaviour  (temporary policy directory; your real policy is untouched)")
    if os.access(gate, os.X_OK):
        with tempfile.TemporaryDirectory(prefix="luma-doctor.") as tmp:
            root = Path(tmp)
            (root / "repo" / ".git").mkdir(parents=True)
            (root / "repo" / "sub").mkdir(parents=True)
            (root / "home" / "projects").mkdir(parents=True)
            proj = (root / "repo").resolve()
            fake = root / "home"
            pfile = fake / "projects" / f"{str(proj).replace('/', '-').replace('.', '-')}.toml"

            def d(cmd: str, cwd: Path = proj, mode: str = "default") -> str:
                return _decide(gate, fake, cmd, str(cwd), mode)

            if all(d(c) == "ask" for c in ("sudo ls", "ssh host", "curl https://example.com")):
                report.ok("gates ssh, curl and sudo by default")
            else:
                report.bad("default gating is not firing — the gate may be returning nothing")

            if all(d(c) == "none" for c in ("git status", "ls -la")):
                report.ok("read-only commands pass without an opinion")
            else:
                report.bad("ordinary commands are being gated")

            if d("rm -rf /tmp/x", mode="bypassPermissions") == "ask":
                report.ok("always-tier still fires under bypassPermissions")
            else:
                report.bad("bypassPermissions silences the always tier — recursive rm is unguarded")

            if d(f"echo x > {gate}", mode="bypassPermissions") == "ask":
                report.ok("the gate refuses writes to itself")
            else:
                report.bad("the gate does not protect itself")

            pfile.write_text('curl = "deny"\n')
            if d("curl https://example.com") == "deny":
                report.ok("deny blocks outright, and policy applies with no restart")
            else:
                report.bad("a deny rule did not take effect")
            if d("luma-foreman policy reset curl") == "ask":
                report.ok("a deny rule does not block its own undo")
            else:
                report.bad("a deny rule blocks the command that would lift it")

            pfile.unlink()
            if d("curl https://example.com") == "ask":
                report.ok("removing a policy reverts to the default, with no restart")
            else:
                report.bad("policy removal did not take effect")

            pfile.write_text('sudo = "allow"\n')
            if d("sudo ls", cwd=proj / "sub") == "none":
                report.ok("one policy per repository, from any subdirectory")
            else:
                report.bad("subdirectories do not resolve to the repository policy")

    # -- this machine's policy ------------------------------------------------
    pol = store.resolve_for(Path.cwd(), home)
    if pol["trust"] == "full":
        report.warn('trust = "full" here: every ask-tier gate is silenced in this project')
    if pol["policy_write"] != model.ALWAYS:
        report.warn('policy_write is below "always": an agent can change its own rules')

    if as_json:
        json.dump(
            {
                "checks": report.checks,
                "pass": report.passes,
                "fail": report.failures,
                "project": str(pol.project_dir),
                "values": pol.values,
            },
            sys.stdout,
            indent=2,
        )
        print()
        return 1 if report.failures else 0

    section = None
    for check in report.checks:
        if check["section"] != section:
            section = check["section"]
            print(section)
        mark = {"ok": "  ok  ", "fail": "  FAIL", "warn": "  warn"}[check["status"]]
        print(f"{mark}  {check['check']}")
    print(f"\nyour policy here\n  project {pol.project_dir}")
    for key in model.KEYS:
        if pol.sources[key.name] != "default":
            print(f"  {key.name:<14} {pol[key.name]:<10} ({pol.sources[key.name]})")
    print(f"\npass={report.passes} fail={report.failures}")
    return 1 if report.failures else 0
