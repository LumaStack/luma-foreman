"""luma-foreman — the entrypoint.

Each job lives under its own module so that `luma-foreman <job>` is the only
thing anyone has to remember.
"""

from __future__ import annotations

import sys

from .inspect import registry, report
from .agent_permissions import commands

USAGE = """usage: luma-foreman <job> [args]

Jobs:
  agent-permissions   what an agent is allowed to do in this repository
  adopt               take a bundle from a catalog into this project
  outfit              project what this project adopted into what a harness reads
  inspect             check a project against the baseline and report shortfalls
  bootstrap           stand a new project up with the structure it should have had
  refit               confirm the latest learnings were actually applied

Run `luma-foreman <job> --help` for a job's own options."""

POLICY_USAGE = """Read and write the per-project agent permissions that the permission gate
consults on every Bash tool call. Changes take effect on the NEXT tool call — no
session restart, because the hook re-reads these files each time it runs.

  luma-foreman agent-permissions                    the effective permissions here
  luma-foreman agent-permissions list               the same thing, spelled the way git/npm/gh spell it
  luma-foreman agent-permissions keys [<key>]       what you can set, and what each key gates

  luma-foreman agent-permissions allow <key>        shorthand for: set <key> allow
  luma-foreman agent-permissions ask <key>          shorthand for: set <key> ask
  luma-foreman agent-permissions deny <key>         shorthand for: set <key> deny
  luma-foreman agent-permissions set <key> <value>  the general form — reaches safe, trusted, always
  luma-foreman agent-permissions reset [<key>]      drop one override, or every override in this scope

  luma-foreman agent-permissions projects           every project that has a config
  luma-foreman agent-permissions path               print the config file path
  luma-foreman agent-permissions edit               open it in $EDITOR
  luma-foreman agent-permissions install            install or update the gate, and report
                                                    what settings.json still needs
  luma-foreman agent-permissions doctor             check it is actually working, not just wired up

Add -g/--global to any write to target the global fallback instead of this
project. Reads always show the merged result. Add --json to `policy`, `keys`
and `doctor` for machine-readable output."""

UNBUILT = ("bootstrap", "refit")


def _policy(argv: list[str]) -> int:
    scope_global = False
    as_json = False
    args: list[str] = []
    for arg in argv:
        if arg in ("-g", "--global"):
            scope_global = True
        elif arg == "--json":
            as_json = True
        elif arg in ("-h", "--help"):
            print(POLICY_USAGE)
            return 0
        else:
            args.append(arg)

    verb = args[0] if args else "show"
    rest = args[1:]

    if verb in ("show", "list"):
        return commands.show(scope_global, as_json)
    if verb == "keys":
        if len(rest) > 1:
            return commands._err("usage: luma-foreman agent-permissions keys [<key>]")
        return commands.keys(rest[0] if rest else None, as_json)
    if verb in ("allow", "ask", "deny"):
        if len(rest) != 1:
            return commands._err(f"usage: luma-foreman agent-permissions {verb} [-g] <key>")
        return commands.shorthand(verb, rest[0], scope_global)
    if verb == "set":
        if len(rest) != 2:
            return commands._err("usage: luma-foreman agent-permissions set [-g] <key> <value>")
        return commands.set_value(rest[0], rest[1], scope_global)
    if verb in ("reset", "unset"):
        if len(rest) > 1:
            return commands._err("usage: luma-foreman agent-permissions reset [-g] [<key>]")
        return commands.reset(rest[0] if rest else None, scope_global)
    if verb == "projects":
        return commands.projects()
    if verb == "path":
        return commands.path(scope_global)
    if verb == "edit":
        return commands.edit(scope_global)
    if verb == "install":
        return commands.install_cmd()
    if verb == "doctor":
        return commands.doctor(as_json)
    if verb == "help":
        print(POLICY_USAGE)
        return 0
    return commands._err(f"unknown command: {verb} (try luma-foreman agent-permissions --help)")


INSPECT_USAGE = """Check a project against the baseline and report where it falls short.

  luma-foreman inspect [<path>]      inspect a repository (default: the current one)
  luma-foreman inspect --json        machine-readable findings, for continuous integration
  luma-foreman inspect --rule <name> run one rule only

Exit codes: 0 nothing found, 1 findings, 2 could not run.

Every check here works in a bare clone with no configuration. A check that
cannot run is reported as skipped, never as a pass."""


def _inspect(argv: list[str]) -> int:
    from pathlib import Path

    as_json = False
    rule: str | None = None
    target = Path.cwd()
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg == "--json":
            as_json = True
        elif arg == "--rule":
            if not rest:
                print("luma-foreman inspect: --rule needs a name", file=sys.stderr)
                return 2
            rule = rest.pop(0)
        elif arg in ("-h", "--help"):
            print(INSPECT_USAGE)
            return 0
        else:
            target = Path(arg)

    if not target.is_dir():
        print(f"luma-foreman inspect: not a directory: {target}", file=sys.stderr)
        return 2
    if rule and rule not in registry.RULES:
        known = ", ".join(registry.RULES)
        print(f"luma-foreman inspect: unknown rule: {rule} (known: {known})", file=sys.stderr)
        return 2
    return report.render(registry.run(target, rule), as_json)


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    job = argv[0] if argv else "help"

    if job in ("help", "-h", "--help"):
        print(USAGE)
        return 0
    if job == "agent-permissions":
        return _policy(argv[1:])
    if job == "inspect":
        return _inspect(argv[1:])
    if job == "adopt":
        from . import adopt

        return adopt.main(argv[1:])
    if job == "outfit":
        from . import outfit

        return outfit.main(argv[1:])
    if job in UNBUILT:
        print(
            f"luma-foreman: {job} is not built yet — see .luma/backlog/ideas/",
            file=sys.stderr,
        )
        return 2
    print(f"luma-foreman: unknown job: {job}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
