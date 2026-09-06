"""luma-foreman — the entrypoint.

Each command lives under its own module so that `luma-foreman <command>` is the
only thing anyone has to remember.
"""

from __future__ import annotations

import sys

from . import __version__
from .inspect import registry, report
from .agent_permissions import commands

# Sectioned rather than one list, because the commands are not one kind of
# thing: most act on this repository's knowledge, one governs what an agent may
# do, and two are what somebody runs before they have either. A flat menu made
# a reader work that out for themselves every time.
#
# **Ordered by how often they are reached**, which is what CLIG asks for and
# what the old alphabetical-ish order was not. `get` and `apply` are the loop;
# `init` is run once and sits with the other thing a newcomer needs.
#
# The tagline is the README's, word for word. Two copies of a positioning line
# that drift apart is worse than one in the wrong place.
USAGE = """Predictable intelligence and reliable governance — for every project.

USAGE
  luma-foreman <command> <subcommand> [args]

CORE COMMANDS
  get                 Fetch a bundle for this repository
  apply               Adopt bundles into agent harnesses
  inspect             Check health
  bundle              Manage bundles
  catalog             Manage catalogs — where bundles come from
  publish             Publish to a catalog
  remove              Drop a bundle

RESTRICT
  agent-permissions   Restrict agents in this repository

GETTING STARTED
  init                Set this repository up, safely
  help                Show this

FLAGS
  --help              Show help for command
  --version           Show version

EXAMPLES
  $ luma-foreman init
  $ luma-foreman catalog add https://github.com/LumaStack/luma-catalog
  $ luma-foreman get lumastack/luma-catalog/git-workflow
  $ luma-foreman apply
  $ luma-foreman bundle list

LEARN MORE
  Use `luma-foreman <command> --help` for a command's own options.
  Find more at https://github.com/LumaStack/luma-foreman"""

POLICY_USAGE = """Restrict what an agent may do in this repository.

USAGE
  luma-foreman agent-permissions <command> [args]

READING
  show                The effective permissions here — also `list`, or no command
  keys [<key>]        What you can set, and what each key gates

SETTING
  allow <key>         Shorthand for: set <key> allow
  ask <key>           Shorthand for: set <key> ask
  deny <key>          Shorthand for: set <key> deny
  set <key> <value>   The general form — reaches safe, trusted, always
  reset [<key>]       Drop one override, or every override in this scope — also `unset`

THE GATE
  install             Install or update the gate, and report what
                      settings.json still needs
  doctor              Check it is working, not just wired up

THE CONFIG FILE
  projects            Every project that has a config
  path                Print the config file path
  edit                Open it in $EDITOR

FLAGS
  -g, --global        Target the global fallback instead of this project
  --json              Machine-readable output for show, keys and doctor
  --help              Show this

EXAMPLES
  $ luma-foreman agent-permissions
  $ luma-foreman agent-permissions deny network
  $ luma-foreman agent-permissions install
  $ luma-foreman agent-permissions doctor

NOTES
  Changes take effect on the NEXT tool call — no session restart, because the
  hook re-reads these files each time it runs.
  Reads always show the merged result; -g/--global affects writes only.

EXIT CODES
  0 fine   1 refused, or something is wrong"""

# Renamed commands are a hard error, not an alias — ADR-0003. This is the only
# thing between somebody typing the old name and a bare failure, so it has to
# say where the command went. `refit` is here too: removed by ADR-0004 with no
# replacement, and saying so beats letting it read as a typo.
RENAMED = {
    "adopt": "get",
    "outfit": "apply",
    "bootstrap": "init",
    "outdated": "bundle outdated",
    "refit": None,
}


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

    # A bare noun shows what the noun can do — see the note in `bundle`. The
    # third noun, changed with the other two: fixing two of three would move
    # the inconsistency rather than end it.
    verb = args[0] if args else "help"
    rest = args[1:]

    if verb == "help":
        print(POLICY_USAGE)
        return 0
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


# Not "against the baseline". That noun appeared in exactly two sentences in the
# whole repository — this one and its copy in the docs — and named nothing: no
# concept, no file, no config. It read as more specific than it was and sent a
# reader looking for something that does not exist. What the five rules actually
# do is compare what a repository declares against what is there.
INSPECT_USAGE = """Check what this repository declares against what is actually here.

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
    command = argv[0] if argv else "help"

    if command in ("help", "-h", "--help"):
        print(USAGE)
        return 0
    # Both spellings, because both get typed: `--version` is what a flag-shaped
    # habit reaches for and `version` is what a command-shaped one does. The
    # same reasoning already gives `agent-permissions` show/list and
    # reset/unset.
    if command in ("version", "-V", "--version"):
        print(f"luma-foreman {__version__}")
        return 0
    if command == "agent-permissions":
        return _policy(argv[1:])
    if command == "inspect":
        return _inspect(argv[1:])
    if command == "get":
        from . import get

        return get.main(argv[1:])
    if command == "remove":
        from . import remove

        return remove.main(argv[1:])
    if command == "publish":
        from . import publish

        return publish.main(argv[1:])
    if command == "apply":
        from . import apply

        return apply.main(argv[1:])
    if command == "bundle":
        from . import bundle

        return bundle.main(argv[1:])
    if command == "catalog":
        from . import catalog

        return catalog.main(argv[1:])
    if command == "init":
        from . import init

        return init.main(argv[1:])
    if command in RENAMED:
        moved = RENAMED[command]
        note = f"renamed to: {moved}" if moved else "removed, with no replacement"
        print(f"luma-foreman: unknown command: {command} ({note})", file=sys.stderr)
        return 1
    print(f"luma-foreman: unknown command: {command}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
