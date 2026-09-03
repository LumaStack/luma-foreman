"""Where this project's knowledge comes from.

**A catalog is registered once, the way an apt source is.** `catalog add`
fetches it, learns the namespace it serves, and records name and URL in
`.luma/config/luma-foreman.toml` — committed, so a teammate's `get` resolves
the same way this one does. Verifying at add time is the point: a wrong
sources entry fails when written, not when somebody runs `get` next week.

**The registry owns name-to-URL; nothing else restates it.** A receipt
records the catalog *name*, so a moved catalog is one config line. A catalog
nobody registered still works — it is an argument to `--from`, and its
receipt keeps the raw URL, like a hand-installed .deb.

**The set `list` reports is the registry plus what receipts remember** — the
distinct sources in `MANIFEST.md` still count, so a project that registered
nothing keeps its answer. `list` reads committed state and works offline;
`add` and `show` reach a catalog.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path

from . import adoption, config, lkf, project

USAGE = """Where this project's knowledge comes from.

  luma-foreman catalog list            every catalog this project draws from
  luma-foreman catalog show <name>     what a catalog publishes
  luma-foreman catalog add <source>    register one, so `get` needs no --from

  --to <project>   a project other than this repository

`<name>` is a registered name, a short name from `list`, a path to a catalog
checkout, or a git URL. `add` fetches the catalog to learn the namespace it
serves, then records it in .luma/config/luma-foreman.toml — committed, so the
whole team resolves the same way. `list` reads the registry and the receipts
and works offline; `add` and `show` reach the catalog and need a network.

Exit codes: 0 fine, 1 refused, 2 could not run."""


# --------------------------------------------------------------------------
# finding a catalog

URL = re.compile(r"^(https?://|git@|ssh://|git://)")



def _git(cwd: Path, *args: str) -> str | None:
    """Run git in *cwd* and return stripped stdout, or None if it could not."""
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), *args],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None



@dataclass(frozen=True)
class Catalog:
    """A catalog checkout on this machine, and where it came from."""

    root: Path
    source: str
    commit: str
    dirty: bool
    namespace: str | None

    def bundle(self, name: str) -> Path | None:
        manifest = self.root / "bundles" / name / "BUNDLE.md"
        return manifest.parent if manifest.is_file() else None

    def names(self) -> list[str]:
        directory = self.root / "bundles"
        if not directory.is_dir():
            return []
        return sorted(
            p.name for p in directory.iterdir() if (p / "BUNDLE.md").is_file()
        )


def _cache_dir() -> Path:
    """Catalog checkouts, under ``~/.cache/<org>/<application>/``.

    The application segment is ``luma-foreman`` in full and never shortened —
    the shape ``luma-config`` gives, and the same one ``store.py`` uses for
    config and data. It read ``~/.cache/luma/catalogs`` until 2026-08-29, which
    put ``catalogs`` where the application name belongs, so nothing under
    ``~/.cache/luma/`` mapped to a repository any more.

    No migration is owed and none is offered: this is cache by that bundle's
    own test, so the stale directory loses nothing and ``_clone`` refetches.
    """
    base = os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache")
    return Path(base) / "luma" / "luma-foreman" / "catalogs"


def _clone(url: str) -> Path | None:
    """Fetch a catalog into the cache, or refresh it if it is already there.

    **The cache is genuinely cache** — deleting it loses no decision anybody
    made, because everything adopted from it is already committed in the
    project. That is the test luma-config gives for telling the two apart, and
    it is why this is not under ``~/.config``.
    """
    target = _cache_dir() / re.sub(r"[^A-Za-z0-9._-]", "-", url)
    if (target / ".git").exists():
        _git(target, "fetch", "--quiet", "--depth", "1", "origin", "HEAD")
        _git(target, "checkout", "--quiet", "FETCH_HEAD")
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        out = subprocess.run(
            ["git", "clone", "--quiet", "--depth", "1", url, str(target)],
            capture_output=True, text=True, timeout=300,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return target if out.returncode == 0 else None


def _root(start: Path) -> Path | None:
    """A catalog's content directory — where ``CATALOG.md`` sits.

    Checked one level down as well, because a catalog repository conventionally
    keeps its content under ``catalog/`` and pointing ``--from`` at the
    repository is what anybody would do.
    """
    for candidate in (start, start / "catalog"):
        if (candidate / "CATALOG.md").is_file():
            return candidate
    return None



def derive_namespace(source: str) -> str | None:
    """A catalog's namespace from where it lives, or None if nowhere says.

    **The last two path segments, `.git` stripped, lowercased.**
    `https://github.com/LumaStack/luma-catalog.git` becomes
    `lumastack/luma-catalog`. No hosting is assumed: any URL with a path
    derives, a LAN git server included, and a local checkout resolves through
    its origin so `--from ../luma-catalog` gives the same answer as the URL it
    was cloned from.

    **A fork gets its own namespace without anybody thinking about it**, which
    is the point — it lives somewhere else, so it is named something else. Only
    a catalog declaring one explicitly can be impersonated by a fork, and that
    catalog chose to be nameable.

    Returns None for a plain directory with no remote. Nothing can guess a name
    for that, so it has to declare one.
    """
    text = source.strip().rstrip("/")
    if not text:
        return None

    if "://" in text:                       # scheme://host/path...
        path = text.split("://", 1)[1].split("/")[1:]
    elif ":" in text and not text[1:3] == ":\\":   # scp-style git@host:org/repo
        path = text.split(":", 1)[1].split("/")
    else:
        return None                         # a bare local path says nothing

    segments = [s for s in path if s]
    if not segments:
        return None
    segments[-1] = segments[-1].removesuffix(".git")
    return "/".join(segments[-2:]).lower() or None



def find(source: str) -> Catalog | str:
    """Resolve *source* to a Catalog, or return a message saying why not."""
    if URL.match(source):
        checkout = _clone(source)
        if checkout is None:
            return f"could not fetch catalog: {source}"
        origin = source
    else:
        checkout = Path(source).expanduser()
        if not checkout.is_dir():
            return f"no such catalog: {source}"
        origin = _git(checkout, "remote", "get-url", "origin") or str(
            checkout.resolve()
        )

    root = _root(checkout)
    if root is None:
        return (
            f"not a catalog: {checkout} — nothing named CATALOG.md here or in "
            f"catalog/"
        )

    commit = _git(root, "rev-parse", "HEAD") or ""
    status = _git(root, "status", "--porcelain")
    manifest = lkf.read(root / "CATALOG.md") or {}
    declared = manifest.get("namespace")
    # Declared always wins; derived is the default so that the common case
    # needs no configuration and a fork cannot inherit somebody else's name.
    namespace = lkf.unquote(declared) if declared else derive_namespace(origin)
    return Catalog(
        root=root,
        source=origin,
        commit=commit,
        dirty=bool(status),
        namespace=namespace or None,
    )




def _count(n: int, noun: str) -> str:
    """`1 bundle`, `19 bundles`. A `(s)` makes the reader do the work."""
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def _terminal_width() -> int:
    """Usable width, capped so a wide terminal does not sprawl.

    Prose stops being readable somewhere around 100 columns however much room
    there is, and `shutil` already answers 80 when it cannot tell.
    """
    return min(shutil.get_terminal_size((80, 24)).columns, 100)


def _err(message: str) -> int:
    print(f"luma-foreman catalog: {message}", file=sys.stderr)
    return 2


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman catalog: {summary}", file=sys.stderr)
    print(f"  {remedy}", file=sys.stderr)
    return 1


def short_name(source: str) -> str:
    """A typeable handle for a catalog that has only ever had a URL.

    Last path segment, `.git` removed. Not an identifier and not stored —
    `show` accepts the full source too, so a collision costs a longer argument
    rather than an unreachable catalog.
    """
    return source.rstrip("/").rsplit("/", 1)[-1].removesuffix(".git") or source


def sources(project_root: Path) -> dict[str, list[str]]:
    """Every catalog this project draws from, to the bundles taken from it.

    The registered catalogs, plus what the receipts remember: a name-indirect
    receipt resolves through the registry, and one whose catalog is no longer
    registered is shown under the bare name — a listing that silently dropped
    it would read as the bundle coming from nowhere.

    **Grouped by origin, not by spelling.** `.git`, a trailing slash, a
    scheme, an scp-style address — git accepts them all for one repository,
    and a listing keyed on the raw string showed one catalog as two, each
    claiming half the bundles. The display form is the shortest spelling on
    record, which in practice is the one without the suffix.
    """
    grouped: dict[str, tuple[str, list[str]]] = {}

    def add(source: str, bundle_id: str | None) -> None:
        key = adoption.origin(source)
        display, bundles = grouped.setdefault(key, (source, []))
        if bundle_id is not None:
            bundles.append(bundle_id)
        if len(source) < len(display):
            grouped[key] = (source, bundles)

    registered = config.registry(project_root)
    for bundle_id, entry in sorted(adoption.read(project_root).items()):
        source = registered.get(entry.catalog, entry.catalog) if entry.catalog \
            else entry.source
        if source:
            add(source, bundle_id)
    for source in registered.values():
        add(source, None)
    configured = config.catalog_source(project_root)
    if configured:
        add(configured, None)
    return {display: bundles for display, bundles in grouped.values()}


def show(source: str, project_root: Path) -> int:
    catalog = find(source)
    if isinstance(catalog, str):
        return _err(catalog)

    names = catalog.names()
    if not names:
        return _err(f"catalog at {catalog.root} publishes no bundles")

    # The namespace is a header rather than a column. It is identical on every
    # row and 23 characters wide for this catalog — repeating it costs a quarter
    # of a laptop screen to say nothing that changes.
    # Three states, because the tool has two steps. A bundle can be here and
    # still reach no agent — which is what `inspect` reports as `unapplied`,
    # and the state somebody browsing a catalog has no other way to notice.
    held_here = adoption.read(project_root)
    rows = []
    for name in names:
        manifest = lkf.read(catalog.root / "bundles" / name / "BUNDLE.md") or {}
        bundle_id = f"{catalog.namespace}/{name}" if catalog.namespace else name
        if bundle_id not in held_here:
            mark = "○"
        elif adoption.applied(project_root, bundle_id):
            mark = "●"
        else:
            mark = "◐"
        rows.append((
            mark,
            name,
            lkf.unquote(manifest.get("version", "?")),
            " ".join(str(manifest.get("description", "")).split()),
        ))

    taken = sum(1 for m, _, _, _ in rows if m != "○")
    if catalog.namespace:
        print(f"{catalog.namespace} — {len(names)} bundles, {taken} taken")
    print("● taken and applied   ◐ taken, not applied yet   ○ not taken")
    print()

    # The name is a heading rather than a column. As a column it reserved its
    # own width on every line of every description — twenty-six characters of
    # nothing, on the lines that needed the room most.
    # Name and version are the heading; the description sits under it. As
    # columns they reserved their own width on every line of every
    # description — thirty characters of nothing, on the lines needing it most.
    lead = 4
    body = max(32, _terminal_width() - lead)

    for i, (mark, name, version, description) in enumerate(rows):
        if i:
            print()
        # The mark is the first character on the line, so the three states are
        # a column the eye can run down rather than something to look for.
        print(f"{mark} {name}  {version}")
        for line in textwrap.wrap(description, body, break_on_hyphens=False):
            print(" " * lead + line)

    if not catalog.namespace:
        print()
        print(
            "  This catalog declares no namespace, so a bundle here has no full\n"
            "  name. Adopt with an explicit one: luma-foreman get <namespace>/"
            f"{names[0]}"
        )
    return 0



def add(source: str, project_root: Path) -> int:
    """Register a catalog by the namespace it serves, verified by fetching it.

    The name is never an argument — it is what the catalog answers when
    asked, the same declared-beats-derived rule `get` uses. Registering what
    was verified is what makes the entry trustworthy: a URL that stops
    serving its namespace fails here, at write time, instead of in a
    teammate's `get` next week.
    """
    if not config.config_path(project_root).is_file():
        return _refuse(
            f"no .luma/config/{config.CONFIG} to register into",
            "The registry is committed project config. Run `luma-foreman "
            "init` first.",
        )

    catalog = find(source)
    if isinstance(catalog, str):
        return _err(catalog)
    name = catalog.namespace
    if not name:
        return _err(
            f"this catalog declares no namespace and none derives from "
            f"{catalog.source} — a registry entry needs a name. Add "
            f"`namespace:` to its CATALOG.md."
        )
    if name == "local" or name.startswith("local/"):
        # ADR-0011: local/ marks a bundle with no published identity yet. A
        # catalog claiming it could shadow every unpublished bundle at once.
        return _refuse(
            f"{name} is reserved for bundles written in a project",
            "No catalog may claim the local/ namespace — see ADR-0011.",
        )

    held = config.registry(project_root).get(name)
    if held:
        if adoption.same_origin(held, catalog.source):
            print(f"{name} is already registered — nothing to do")
            return 0
        return _refuse(
            f"{name} is already registered from a different source",
            f"holds:  {held}\n"
            f"  asked:  {catalog.source}\n"
            "  Same name, different origin — the second entry would shadow "
            "the first. If the catalog moved, edit the entry in "
            f".luma/config/{config.CONFIG}.",
        )

    config.register_catalog(project_root, name, catalog.source)
    print(f"{name}: registered")
    print(f"  source  {catalog.source}")
    print(f"  in      .luma/config/{config.CONFIG}")
    print()
    print("  Commit the config — the registry is how a teammate's `get` "
          "resolves too.")
    print(f"  Then: luma-foreman get {name}/<bundle>")
    return 0


def listing(project_root: Path) -> int:
    found = sources(project_root)
    if not found:
        print("no catalogs — nothing registered, and nothing adopted.")
        print()
        print("  luma-foreman catalog add <url>              register one")
        print("  luma-foreman get <bundle> --from <catalog>  or take without registering")
        return 0

    configured = config.catalog_source(project_root)
    registered = config.registry(project_root)
    by_origin = {adoption.origin(url): name for name, url in registered.items()}

    # How many a catalog publishes is the part worth knowing — `3 taken` says
    # nothing you did not already know, and `3 of 19 taken` says there is more
    # here. It costs a fetch per catalog, which is what `catalog` is for.
    rows = []
    for source, bundles in sorted(found.items(), key=lambda kv: short_name(kv[0])):
        catalog = find(source)
        if isinstance(catalog, str):
            # Unreachable is reported, not fatal. An outage is not a property
            # of this repository, and a blank where a number belongs reads as
            # zero — which is the one thing that must not happen.
            taken = f"{_count(len(bundles), 'bundle')} taken, ? published"
            rows.append((short_name(source), taken, source, catalog))
            continue
        published = len(catalog.names())
        rows.append((
            short_name(source),
            f"{len(bundles)} of {_count(published, 'bundle')} taken",
            source,
            None,
        ))

    # Same shape as `catalog show`: the name is a heading, everything about it
    # is indented under it. Three kinds of thing on one line — a name, a count
    # and a URL — was three columns competing for the same width.
    for i, (name, count, source, why) in enumerate(rows):
        if i:
            print()
        registered_as = by_origin.get(adoption.origin(source))
        default = ("   (configured default)"
                   if configured and adoption.same_origin(source, configured)
                   else "")
        # A registered catalog is headed by its registered name — the same
        # string a bundle ID starts with, which is what `get` resolves by.
        print(f"  {registered_as or name}"
              + ("   (registered)" if registered_as else default))
        # `find` puts the source in its message, and the line below carries it.
        print(f"    {count}" + (f" — {why.replace(source, '').strip(': ')}" if why else ""))
        print(f"    {source}")

    print()
    if registered:
        print(f"{_count(len(found), 'catalog')} — registered in "
              f".luma/config/{config.CONFIG}, or remembered by receipts.")
    else:
        print(f"{_count(len(found), 'catalog')}, derived from what this project has adopted.")
    unreachable = [n for n, _, _, why in rows if why]
    if unreachable:
        print(f"{len(unreachable)} could not be reached, so what they publish is unknown.")
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
        # A registered name resolves first, then a short name against
        # catalogs this project already draws from; anything else is passed
        # through as a path or URL, so a catalog nobody has adopted from is
        # still reachable.
        registered = config.registry(project_root)
        if wanted in registered:
            wanted = registered[wanted]
        else:
            for source in sources(project_root):
                if short_name(source) == wanted:
                    wanted = source
                    break
        return show(wanted, project_root)

    if verb == "add":
        if len(operands) != 1:
            return _err("usage: luma-foreman catalog add <path-or-url>")
        return add(operands[0], project_root)

    return _err(f"unknown: catalog {verb} (try luma-foreman catalog --help)")
