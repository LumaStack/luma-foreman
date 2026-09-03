"""`get` — adopting a bundle from a catalog into this project.

**Finding the catalog is `catalog`'s job, not this one's.** This copies a
bundle out of one and writes the receipt; resolving a source to a `Catalog`,
deriving its namespace and listing what it publishes all live next to the
commands that report on catalogs.

**Adoption is a directory copy, and keeping it one is the design.** Bundles
depend on nothing, so there is no graph to resolve, no version to solve for and
no order to install in. What separates this from ``cp -r`` is the record it
leaves: which bundle, which version, which commit of the catalog, and a checksum
of exactly what landed.

**The copy is committed, and that is the difference from a package cache.** A
fresh clone with no network reproduces the project exactly, because the
knowledge is in the repository rather than in a directory somewhere under a home
directory that a teammate does not have.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from . import adoption, catalog as catalogs, config, lkf, project

USAGE = """Adopt a bundle from a catalog into this project, and record what you took.

  luma-foreman get <bundle>            adopt one — e.g. lumastack/luma-catalog/decision-records
  luma-foreman get <bundle> --force    overwrite a copy that was edited here

To see what a catalog publishes: luma-foreman catalog show <name>

  --from <catalog>   a path to a catalog checkout, or a git URL. Without it
                     the bundle ID resolves through the registered catalogs
                     in .luma/config/luma-foreman.toml (the ID starts with
                     the catalog's name), then the source recorded for an
                     already-adopted bundle, then [catalog] source. Register
                     with: luma-foreman catalog add <url>

A bundle is addressed <namespace>/<name>, and the namespace is the catalog's.
It derives from where the catalog lives — github.com/LumaStack/luma-catalog
becomes lumastack/luma-catalog — unless CATALOG.md declares one, which wins.
A fork therefore gets its own namespace without anybody arranging it.
  --to <project>     the project to adopt into (default: this repository)

The bundle lands in .luma/bundles/<namespace>/<bundle-name>/ and is committed with the rest
of the project. Nothing is resolved and nothing is fetched later — bundles
depend on nothing, which is what keeps this a copy rather than an install.

Exit codes: 0 adopted, 1 refused, 2 could not run."""

def _err(message: str) -> int:
    print(f"luma-foreman get: {message}", file=sys.stderr)
    return 2


# --------------------------------------------------------------------------
# finding a catalog


# --------------------------------------------------------------------------
# adopting


def _copy(src: Path, dst: Path) -> int:
    """Replace *dst* with *src*, and report how many files landed.

    Replace rather than merge: a file the new version dropped has to disappear,
    or the copy is neither the old bundle nor the new one and its checksum
    matches nothing.
    """
    if dst.exists():
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        src, dst, ignore=shutil.ignore_patterns(*adoption.IGNORED, ".git")
    )
    return len(adoption.files(dst))


def _resolve_id(catalog: catalogs.Catalog, requested: str) -> tuple[str, str] | str:
    """Full bundle ID and bundle name, or a message saying what is wrong.

    A bundle is addressed ``<namespace>/<name>``, and **the namespace is the
    catalog's rather than the bundle's** — the same bundle promoted into
    another organization's catalog is that organization's to name.
    """
    # Matched against the catalog's own namespace rather than split on the
    # first slash, because a namespace may be any number of segments —
    # `lumastack/luma-catalog/widgets` is one bundle, not a nested one.
    if catalog.namespace:
        prefix = f"{catalog.namespace}/"
        if requested.startswith(prefix):
            name = requested[len(prefix):]
            return f"{catalog.namespace}/{name}", name
        if "/" in requested:
            name = requested.rsplit("/", 1)[-1]
            return (
                f"this catalog publishes {catalog.namespace}/, not "
                f"{requested.rsplit('/', 1)[0]}/ — did you mean "
                f"{catalog.namespace}/{name}?"
            )
        return f"{catalog.namespace}/{requested}", requested

    # No namespace declared and none derivable — a plain directory with no
    # remote. The caller may still name it: pointing at a local catalog and
    # saying what to call its bundles is the whole reason this path exists.
    if "/" in requested:
        return requested, requested.rsplit("/", 1)[-1]
    return (
        f"name the namespace: {requested} is ambiguous. This catalog declares "
        f"none, and none can be derived from a path with no remote. Try "
        f"<namespace>/{requested}, or add `namespace:` to its CATALOG.md."
    )


def _same_lineage(
    existing: adoption.Adopted,
    catalog: catalogs.Catalog,
    registered: dict[str, str],
) -> bool:
    """Does the receipt's origin match the catalog being fetched from?

    A name-indirect receipt resolves through the registry first — that is the
    indirection working: the registry says where the name lives *now*. A name
    the registry no longer holds falls back to comparing names, because a
    catalog's name is its namespace and derivation gives a fork a different
    one — the same property the URL comparison leans on.
    """
    if existing.catalog:
        held = registered.get(existing.catalog)
        if held:
            return adoption.same_origin(held, catalog.source)
        return existing.catalog == catalog.namespace
    return adoption.same_origin(existing.source, catalog.source)


def run(
    requested: str,
    source: str,
    project_root: Path,
    force: bool,
) -> int:
    catalog = catalogs.find(source)
    if isinstance(catalog, str):
        return _err(catalog)

    # Registered catalogs go name-indirect on the receipt: the registry owns
    # name-to-URL, and a receipt restating the URL would go stale with it.
    # Matched by origin rather than by how the catalog was named at the
    # prompt, so --from pointing at a registered catalog's checkout still
    # records the name.
    registered = config.registry(project_root)
    registered_as = next(
        (name for name, url in registered.items()
         if adoption.same_origin(url, catalog.source)),
        "",
    )

    resolved = _resolve_id(catalog, requested)
    if isinstance(resolved, str):
        return _err(resolved)
    bundle_id, name = resolved

    src = catalog.bundle(name)
    if src is None:
        offered = ", ".join(catalog.names()) or "nothing"
        return _err(f"no bundle named {name} in this catalog (it offers: {offered})")

    manifest = lkf.read(src / "BUNDLE.md") or {}
    version = lkf.unquote(manifest.get("version", ""))
    if not version:
        return _err(
            f"{bundle_id} declares no version — a bundle that cannot be pinned "
            f"cannot honestly be reported as adopted"
        )

    dst = adoption.vendored(project_root, bundle_id)
    entries = adoption.read(project_root)
    existing = entries.get(bundle_id)

    # A different catalog under the same ID is a change of lineage, not an
    # upgrade, and it is the one case where doing nothing is the wrong answer.
    # Two catalogs can only share an ID by both declaring the same namespace —
    # derivation makes that impossible — so this catches the deliberate case
    # and the misconfigured one, both of which somebody should decide about.
    if (existing and (existing.source or existing.catalog)
            and not _same_lineage(existing, catalog, registered)
            and not force):
        return _refuse(
            f"{bundle_id} here came from a different catalog",
            f"holds:  {existing.catalog or existing.source}\n"
            f"  asked:  {catalog.source}\n"
            "  Same name, different origin — an upgrade would silently swap "
            "what this bundle is. --force to switch lineage; MANIFEST.md "
            "records the new source.",
        )

    if dst.exists() and not force:
        here = adoption.checksum(dst)
        if existing and existing.checksum and here != existing.checksum:
            return _refuse(
                f"{bundle_id} has been edited here — adopting would discard "
                f"those edits",
                "Editing an adopted bundle is drift. If it needs to be "
                "different, that is a different bundle in your own namespace. "
                "Use --force if the edits are disposable.",
            )
        if existing and existing.version == version:
            print(f"{bundle_id} is already at {version} — nothing to do")
            return 0

    upgrade = existing.version if existing else None
    switched = bool(existing and (existing.source or existing.catalog)
                    and not _same_lineage(existing, catalog, registered))
    count = _copy(src, dst)
    entries[bundle_id] = adoption.Adopted(
        bundle=bundle_id,
        version=version,
        source="" if registered_as else catalog.source,
        commit=catalog.commit,
        checksum=adoption.checksum(dst),
        catalog=registered_as,
    )
    adoption.write(project_root, entries)

    # `--force` at the same version re-copies, it does not upgrade. Saying
    # "upgraded 0.3.1 -> 0.3.1" reports something that did not happen, and
    # output nobody can trust is worse than output nobody reads.
    if switched:
        # Reporting a lineage change as a version event would describe the one
        # thing that did not happen. The version may not have moved at all.
        verb = f"switched to {version} from another catalog"
    elif upgrade == version:
        verb = f"took {version} again"
    elif upgrade:
        verb = f"upgraded {upgrade} -> {version}"
    else:
        verb = f"adopted {version}"
    print(f"{bundle_id}: {verb}")
    if registered_as:
        print(f"  from     {registered_as} — {catalog.source}")
    else:
        print(f"  from     {catalog.source}")
    print(f"  commit   {catalog.commit or '(not a git checkout)'}")
    rel = dst.relative_to(project_root).as_posix()
    print(f"  into     {rel}/  ({count} files)")
    print(f"  checksum {entries[bundle_id].checksum}")

    if catalog.dirty:
        print()
        print(
            "  warning: the catalog checkout has uncommitted changes, so the "
            "commit\n           recorded above does not identify what was "
            "copied."
        )
    print()
    print("  Commit the copy — an adopted bundle lives in the repository.")
    print("  Then: luma-foreman apply")
    return 0


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman get: {summary}", file=sys.stderr)
    print(f"  {remedy}", file=sys.stderr)
    return 1


def main(argv: list[str]) -> int:
    source: str | None = None
    target: Path | None = None
    force = False
    requested: list[str] = []

    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--list":
            # Browsing a catalog was never an adoption operation; it lived here
            # because this was the command that could already reach one.
            return _err(
                "--list is gone — browsing a catalog is `luma-foreman catalog "
                "show <name>`"
            )
        if arg == "--force":
            force = True
        elif arg == "--from":
            if not rest:
                return _err("--from needs a catalog path or URL")
            source = rest.pop(0)
        elif arg == "--to":
            if not rest:
                return _err("--to needs a project directory")
            target = Path(rest.pop(0))
        elif arg.startswith("-"):
            return _err(f"unknown option: {arg}")
        else:
            requested.append(arg)

    project_root, _ = project.resolve(target or Path.cwd())
    if target and not target.is_dir():
        return _err(f"not a directory: {target}")

    if len(requested) != 1:
        return _err(
            "name exactly one bundle (`luma-foreman catalog show <name>` lists them)"
        )
    wanted = requested[0]

    if source is None:
        # A bundle ID starts with the name of the catalog that publishes it,
        # so the registry resolves it with nothing restated. Longest name
        # first, because a name may be any number of segments. The registry
        # outranks the receipt deliberately: a moved catalog makes the
        # registry current truth and the receipt history.
        registered = config.registry(project_root)
        for name in sorted(registered, key=len, reverse=True):
            if wanted.startswith(name + "/"):
                source = registered[name]
                break
    if source is None:
        # A bundle adopted before the registry existed records its raw
        # source, and re-taking it is the common case — demanding --from for
        # a fact the receipt already holds made an operator repeat the
        # tool's own record back to it, eighteen times in one migration.
        entries = adoption.read(project_root)
        entry = entries.get(wanted)
        if entry is None:
            named = [e for e in entries.values() if e.name == wanted]
            if len(named) == 1:
                entry = named[0]
        if entry and entry.source:
            source = entry.source
        elif entry and entry.catalog:
            # Name-indirect, and the name resolved to nothing above — the
            # registry entry this receipt leans on is gone.
            return _err(
                f"{entry.bundle} came from {entry.catalog}, which is not "
                f"registered here — luma-foreman catalog add <url> to "
                f"restore it, or pass --from"
            )
    if source is None:
        source = config.catalog_source(project_root)
    if source is None:
        return _err(
            "no catalog — luma-foreman catalog add <url> to register one, "
            "or pass --from <path-or-url>"
        )

    return run(wanted, source, project_root, force)
