"""Where this project's knowledge comes from.

**A catalog is not a registered thing.** There is no `catalog add`, no list of
remotes, and nothing to configure beyond one optional default. A catalog is an
argument — a path or a URL — and that is deliberate: adoption is a copy with a
receipt, not a subscription, so there is no relationship to keep.

**So the set is derived rather than stored.** It is the distinct `source`
values in `adopted.toml`, plus `[catalog] source` if the project sets one.
That is already how `outdated` decides where to look, and it means the
org-private-plus-universal case works with nothing registered.

`list` therefore reads committed state and works offline. `show` is the only
command here that reaches a catalog.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import adopt, adoption, project

USAGE = """Where this project's knowledge comes from.

  luma-foreman catalog list           every catalog this project draws from
  luma-foreman catalog show <name>    what a catalog publishes

  --to <project>   a project other than this repository

`<name>` is a short name from `list`, a path to a catalog checkout, or a git
URL. `list` is derived from what has been adopted and works offline; `show`
reaches the catalog and needs a network.

Exit codes: 0 fine, 2 could not run."""


def _err(message: str) -> int:
    print(f"luma-foreman catalog: {message}", file=sys.stderr)
    return 2


def short_name(source: str) -> str:
    """A typeable handle for a catalog that has only ever had a URL.

    Last path segment, `.git` removed. Not an identifier and not stored —
    `show` accepts the full source too, so a collision costs a longer argument
    rather than an unreachable catalog.
    """
    return source.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git") or source


def sources(project_root: Path) -> dict[str, list[str]]:
    """Every catalog this project draws from, to the bundles taken from it."""
    out: dict[str, list[str]] = {}
    for bundle_id, entry in sorted(adoption.read(project_root).items()):
        out.setdefault(entry.source, []).append(bundle_id)
    configured = adopt._configured(project_root)
    if configured:
        out.setdefault(configured, [])
    return out


def listing(project_root: Path) -> int:
    found = sources(project_root)
    if not found:
        print("no catalogs — nothing adopted, and no [catalog] source configured.")
        print()
        print("  luma-foreman get <bundle> --from <catalog>")
        return 0

    configured = adopt._configured(project_root)
    width = max(len(short_name(s)) for s in found)
    for source, bundles in sorted(found.items(), key=lambda kv: short_name(kv[0])):
        count = f"{len(bundles)} bundle(s)" if bundles else "nothing taken yet"
        default = "  (configured default)" if source == configured else ""
        print(f"  {short_name(source):<{width}}  {count:<16}  {source}{default}")

    print()
    print(f"{len(found)} catalog(s), derived from what has been adopted.")
    print()
    print("  luma-foreman catalog show <name>    what one publishes")
    return 0


def main(argv: list[str]) -> int:
    target: Path | None = None
    args: list[str] = []
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--to":
            if not rest:
                return _err("--to needs a directory")
            target = Path(rest.pop(0))
        else:
            args.append(arg)

    if target and not target.is_dir():
        return _err(f"not a directory: {target}")
    project_root, _ = project.resolve(target or Path.cwd())

    verb = args[0] if args else "list"
    operands = args[1:]

    if verb == "list":
        if operands:
            return _err(f"list takes no arguments (got: {operands[0]})")
        return listing(project_root)

    if verb == "show":
        if len(operands) != 1:
            return _err("usage: luma-foreman catalog show <name>")
        wanted = operands[0]
        # A short name only resolves against catalogs this project already
        # draws from; anything else is passed through as a path or URL, so a
        # catalog nobody has adopted from is still reachable.
        for source in sources(project_root):
            if short_name(source) == wanted:
                wanted = source
                break
        return adopt.listing(wanted)

    return _err(f"unknown: catalog {verb} (try luma-foreman catalog --help)")
