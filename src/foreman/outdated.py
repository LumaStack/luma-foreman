"""Which adopted bundles have moved on without you.

**Publication notifies nobody.** A bundle becomes available by being committed
to a catalog's `main`; nothing tells the projects that already took it. An
adopter finds out by asking, and until now the only way to ask was to re-run
`get` on every bundle and read what it said.

**This is a separate command rather than a flag on `inspect`, and the reason is the
network.** `inspect` works in a bare clone with no configuration and reports a
check it could not run as skipped rather than passed — that guarantee is worth
more than the convenience of folding this into it. Answering *is there a newer
version* requires reaching the catalog, so it is its own command, and somebody
running it has chosen to be online.

The name is what every package manager already calls this — `npm outdated`,
`bundle outdated`, `brew outdated`. There is no reason to make anybody learn a
second word for it.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

from . import adoption, catalog as catalogs, lkf, project

USAGE = """Report which adopted bundles have a newer version published.

  luma-foreman outdated              check every adopted bundle
  luma-foreman outdated --json       machine-readable
  luma-foreman outdated --to <dir>   a project other than this repository

Reaches the catalog each bundle was adopted from, so it needs a network. This
is the one command here that does — `inspect` deliberately does not, which is why
this is not part of it.

Exit codes: 0 everything current, 1 something is behind, 2 could not run."""


@dataclass(frozen=True)
class Status:
    bundle: str
    held: str
    available: str | None
    source: str
    note: str = ""

    @property
    def behind(self) -> bool:
        return self.available is not None and self.available != self.held


def _newest(source: str, name: str, cache: dict) -> tuple[str | None, str]:
    """The version a catalog currently publishes for *name*, and why not."""
    if source not in cache:
        cache[source] = catalogs.find(source)
    catalog = cache[source]
    if isinstance(catalog, str):
        return None, catalog
    home = catalog.bundle(name)
    if home is None:
        # Retired upstream, renamed, or moved to another catalog. The project
        # still holds a working copy — this is news rather than breakage.
        return None, "no longer published here"
    version = lkf.unquote((lkf.read(home / "BUNDLE.md") or {}).get("version", ""))
    return (version, "") if version else (None, "published without a version")


def survey(project_root: Path) -> list[Status]:
    entries = adoption.read(project_root)
    out: list[Status] = []
    # One catalog is usually the source for many bundles, and `find` clones or
    # fetches. Resolving each source once rather than once per bundle is the
    # difference between one network round trip and fifteen.
    cache: dict = {}
    for bundle_id, entry in sorted(entries.items()):
        available, note = _newest(entry.source, entry.name, cache)
        out.append(
            Status(
                bundle=bundle_id,
                held=entry.version,
                available=available,
                source=entry.source,
                note=note,
            )
        )
    return out


def main(argv: list[str]) -> int:
    as_json = False
    target: Path | None = None
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--json":
            as_json = True
        elif arg == "--to":
            if not rest:
                print("luma-foreman outdated: --to needs a directory", file=sys.stderr)
                return 2
            target = Path(rest.pop(0))
        else:
            print(f"luma-foreman outdated: unknown option: {arg}", file=sys.stderr)
            return 2

    if target and not target.is_dir():
        print(f"luma-foreman outdated: not a directory: {target}", file=sys.stderr)
        return 2
    project_root, _ = project.resolve(target or Path.cwd())

    if not adoption.read(project_root):
        print(
            "nothing adopted — .luma/bundles/MANIFEST.md holds no entries.",
            file=sys.stderr,
        )
        return 2

    rows = survey(project_root)
    behind = [r for r in rows if r.behind]
    unknown = [r for r in rows if r.available is None]

    if as_json:
        import json

        print(json.dumps(
            [{"bundle": r.bundle, "held": r.held, "available": r.available,
              "source": r.source, "behind": r.behind, "note": r.note} for r in rows],
            indent=2,
        ))
        return 1 if behind else 0

    by_id = {r.bundle: r for r in rows}
    groups = adoption.by_namespace(list(by_id))
    width = max(len(n) for _, names in groups for n in names)
    held = max(len(r.held) for r in rows)

    for i, (namespace, names) in enumerate(groups):
        if i:
            print()
        print(namespace)
        for name in names:
            row = by_id[f"{namespace}/{name}" if namespace else name]
            head = f"  {name:<{width}}  {row.held:<{held}}"
            if row.behind:
                print(f"{head}  ->  {row.available}")
            elif row.available is None:
                print(f"{head}      ? {row.note}")
            else:
                print(f"{head}      current")

    print()
    if behind:
        print(f"{len(behind)} of {len(rows)} adopted bundle(s) are behind.")
        print()
        print("  luma-foreman get <bundle>     take the newer version")
        print("  luma-foreman apply            then rewrite what agents read")
        print()
        print(
            "**Read what changed before taking it.** For prose a two-character\n"
            "edit can reverse a rule, so the tier is a signal rather than a\n"
            "guarantee — the bundle's `## Version` section is what says why."
        )
    else:
        print(f"all {len(rows)} adopted bundle(s) are current.")

    if unknown:
        print()
        print(
            f"{len(unknown)} could not be answered. A bundle its catalog no longer\n"
            "publishes still works — you hold a copy — but nothing will tell you\n"
            "about it again."
        )
    return 1 if behind else 0
