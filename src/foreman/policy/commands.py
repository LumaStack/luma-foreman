"""The `luma-foreman policy` subcommands."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from . import install as _install
from . import model, store
from .doctor import run as doctor_run

CMD = "luma-foreman policy"


def _err(message: str) -> int:
    print(f"{CMD}: {message}", file=sys.stderr)
    return 1


def _resolved(scope_global: bool):
    home = store.home()
    pol = store.resolve_for(Path.cwd(), home)
    target = pol.global_file if scope_global else pol.project_file
    return home, pol, target


def show(scope_global: bool, as_json: bool) -> int:
    _, pol, _ = _resolved(scope_global)
    if as_json:
        json.dump(
            {
                "project": str(pol.project_dir),
                "slug": pol.slug,
                "project_file": str(pol.project_file),
                "global_file": str(pol.global_file),
                "values": pol.values,
                "sources": pol.sources,
            },
            sys.stdout,
            indent=2,
        )
        print()
        return 0

    print(f"project  {pol.project_dir}")
    print(f"slug     {pol.slug}")
    for label, path in (("project", pol.project_file), ("global ", pol.global_file)):
        print(f"{label}  {path}" + ("" if path.exists() else "  (none)"))
    print()
    print(f"{'KEY':<14} {'VALUE':<10} SOURCE")
    for key in model.KEYS:
        value = pol[key.name] or "(unset)"
        print(f"{key.name:<14} {value:<10} {pol.sources[key.name]}")
    print(f"\nRun `{CMD} keys` for what each key gates.")
    return 0


def keys(name: str | None, as_json: bool) -> int:
    if as_json:
        json.dump(
            [
                {"key": k.name, "accepts": list(k.values), "default": k.default, "gates": k.gates}
                for k in model.KEYS
            ],
            sys.stdout,
            indent=2,
        )
        print()
        return 0

    if name:
        key = model.BY_NAME.get(name)
        if not key:
            return _err(f"unknown key: {name} (try {CMD} keys)")
        _, pol, _ = _resolved(False)
        accepts = " | ".join(key.values) if key.values else "<hostnames>"
        print(f"{key.name}\n")
        print(f"  accepts   {accepts}")
        print(f"  default   {key.default or '(unset)'}")
        print(f"  current   {pol[key.name] or '(unset)'} (from {pol.sources[key.name]})\n")
        print("\n".join(f"  {line}" for line in _wrap(key.gates)))
        if note := model.note_for(key):
            print()
            print("\n".join(f"  {line}" for line in note.splitlines()))
        return 0

    print(f"{'KEY':<14} {'ACCEPTS':<38} DEFAULT")
    for key in model.KEYS:
        accepts = " | ".join(key.values) if key.values else "<hostnames>"
        print(f"{key.name:<14} {accepts:<38} {key.default or '(unset)'}")
    print("\nValue meanings:\n")
    print(_VALUE_MEANINGS)
    print(f"\nRun `{CMD} keys <key>` for what one key gates and where it bites.")
    return 0


_VALUE_MEANINGS = """  allow    no opinion — the normal Claude Code permission flow decides
  ask      prompt, but bypassPermissions and trust = "full" silence it
  always   prompt in every mode, bypass included
  deny     the hook refuses outright, every mode
  trusted  (ssh) allow a host on ssh_hosts, otherwise prompt
  safe     (curl/wget) allow a plain fetch; prompt when the command writes to
           disk, uploads a body, or pipes into an interpreter"""


def _wrap(text: str, width: int = 76) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        if line and len(line) + 1 + len(word) > width:
            lines.append(line)
            line = word
        else:
            line = f"{line} {word}".strip()
    if line:
        lines.append(line)
    return lines


def set_value(name: str, value: str, scope_global: bool) -> int:
    key = model.BY_NAME.get(name)
    if not key:
        return _err(f"unknown key: {name} (try {CMD} keys)")
    if key.free_form:
        if any(c not in " ,-._@:/" and not c.isalnum() for c in value):
            return _err(f"invalid value for {name}: {value} (try {CMD} keys {name})")
    elif value not in key.values:
        return _err(f"invalid value for {name}: {value} (try {CMD} keys {name})")

    _, pol, target = _resolved(scope_global)
    store.write_key(target, name, value, None if scope_global else pol.project_dir)
    print(f'{name} = "{value}"  ->  {target}')
    print("Takes effect on the next tool call; no session restart needed.")
    return 0


def shorthand(verb: str, name: str, scope_global: bool) -> int:
    key = model.BY_NAME.get(name)
    if not key:
        return _err(f"unknown key: {name} (try {CMD} keys)")
    if key.free_form:
        return _err(f"{name} takes a value, not a verb — try: {CMD} set {name} <value>")
    return set_value(name, verb, scope_global)


def reset(name: str | None, scope_global: bool) -> int:
    _, pol, target = _resolved(scope_global)
    if not target.exists():
        return _err(f"no config to reset: {target}")
    if name is None:
        target.unlink()
        print(f"removed {target}")
        fallback = "the built-in defaults" if scope_global else "global, then the built-in defaults"
        print(f"Every key in this scope now falls back to {fallback}.")
        return 0
    if name not in model.BY_NAME:
        return _err(f"unknown key: {name} (try {CMD} keys)")
    store.drop_key(target, name)
    after = store.resolve_for(Path.cwd(), store.home())
    print(f"reset {name} in {target}")
    print(f"{name} is now {after[name] or '(unset)'} (from {after.sources[name]}).")
    return 0


def projects() -> int:
    directory = store.home() / "projects"
    files = sorted(directory.glob("*.toml")) if directory.is_dir() else []
    if not files:
        print(f"no project configs under {directory}")
        return 0
    for path in files:
        print(path.stem)
        for key, value in store._read(path).items():
            print(f"    {key}={value}")
    return 0


def path(scope_global: bool) -> int:
    _, _, target = _resolved(scope_global)
    print(target)
    return 0


def edit(scope_global: bool) -> int:
    _, _, target = _resolved(scope_global)
    target.parent.mkdir(parents=True, exist_ok=True)
    return subprocess.call([os.environ.get("EDITOR", "vi"), str(target)])


def install_cmd() -> int:
    verb = _install.install()
    gate = _install.gate_path()
    print(f"gate {verb}: {gate}\n")

    state = _install.wiring()
    print(f"Claude Code settings: {state['settings']}")
    if not state["exists"]:
        print("  (does not exist yet — create it with the JSON below)")
    print(f"  {'OK  ' if state['hook_ok'] else 'TODO'} PreToolUse hook wired to the gate")
    if state["stale_hook"]:
        print("       ...a PreToolUse hook points at a permission-gate.sh somewhere")
        print("       ELSE. Repoint it at the path above, or you are running an old gate.")
    print(f"  {'OK  ' if state['deny_ok'] else 'TODO'} deny rule protecting the policy directory")

    if old := _install.legacy_install():
        print("\n  note  directories from an earlier layout remain:")
        for path in old:
            print(f"          {path}")
        print("        Directories nest under the organization now —")
        print("        ~/.config/luma/luma-foreman/ rather than ~/.config/luma-foreman/,")
        print("        so one rule covers every luma tool. Any policy in the old")
        print("        location is NOT read any more —")
        print("        copy it across if you had settings there. Delete the old")
        print("        directories once the hook above points at the new path AND Claude")
        print("        Code has restarted; not before, or the running session is")
        print("        unguarded.")

    if state["hook_ok"] and state["deny_ok"]:
        print(f"\nNothing left to do. Run `{CMD}` to see the effective policy.")
        return 0

    print(f"\nAdd these to {state['settings']} by hand — this file is yours, so nothing")
    print("here edits it. Merge into the existing arrays rather than replacing them:\n")
    print(_install.snippet())
    print("\nThe deny rule is not optional. It is what stops a session editing the policy —")
    print("and the gate itself. Two rules, because configuration and program files\n")
    print("live in different places — deleting your config must not delete the gate.\n")
    print("Hook changes need a Claude Code restart; Claude Code snapshots hook")
    print("configuration at session start. Policy changes after that are live.")
    return 0


def doctor(as_json: bool) -> int:
    return doctor_run(as_json)
