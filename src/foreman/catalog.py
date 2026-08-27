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

  luma-foreman catalog list           every catalog this project draws from
  luma-foreman catalog show <name>    what a catalog publishes

  --to <project>   a project other than this repository

`<name>` is a short name from `list`, a path to a catalog checkout, or a git
URL. `list` is derived from what has been adopted and works offline; `show`
reaches the catalog and needs a network.

Exit codes: 0 fine, 2 could not run."""


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
    base = os.environ.get("XDG_CACHE_HOME") or (Path.home() / ".cache")
    return Path(base) / "luma" / "catalogs"


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




def _terminal_width() -> int:
    """Usable width, capped so a wide terminal does not sprawl.

    Prose stops being readable somewhere around 100 columns however much room
    there is, and `shutil` already answers 80 when it cannot tell.
    """
    return min(shutil.get_terminal_size((80, 24)).columns, 100)


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
    configured = config.catalog_source(project_root)
    if configured:
        out.setdefault(configured, [])
    return out


def show(source: str) -> int:
    catalog = find(source)
    if isinstance(catalog, str):
        return _err(catalog)

    names = catalog.names()
    if not names:
        return _err(f"catalog at {catalog.root} publishes no bundles")

    # The namespace is a header rather than a column. It is identical on every
    # row and 23 characters wide for this catalog — repeating it costs a quarter
    # of a laptop screen to say nothing that changes.
    if catalog.namespace:
        print(f"{catalog.namespace} — {len(names)} bundle(s)")
        print()

    rows = []
    for name in names:
        manifest = lkf.read(catalog.root / "bundles" / name / "BUNDLE.md") or {}
        rows.append((
            name,
            lkf.unquote(manifest.get("version", "?")),
            " ".join(str(manifest.get("description", "")).split()),
        ))

    width = max(len(n) for n, _, _ in rows)
    held = max(len(v) for _, v, _ in rows)
    lead = 2 + width + 2 + held + 2
    body = max(32, _terminal_width() - lead)

    # Blank lines only where descriptions wrap. Without them a wrapped list is
    # a wall; with them everywhere, a short list is twice as tall as it needs.
    wrapped = any(len(d) > body for _, _, d in rows)

    for i, (name, version, description) in enumerate(rows):
        if wrapped and i:
            print()
        head = f"  {name:<{width}}  {version:<{held}}  "
        if not description:
            print(head.rstrip())
            continue
        # Hanging indent, so the name column stays scannable and no line runs
        # off the screen. A description is a sentence, not a field.
        for i, line in enumerate(textwrap.wrap(description, body) or [""]):
            print((head if i == 0 else " " * lead) + line)

    if not catalog.namespace:
        print()
        print(
            "  This catalog declares no namespace, so a bundle here has no full\n"
            "  name. Adopt with an explicit one: luma-foreman get <namespace>/"
            f"{names[0]}"
        )
    return 0



def listing(project_root: Path) -> int:
    found = sources(project_root)
    if not found:
        print("no catalogs — nothing adopted, and no [catalog] source configured.")
        print()
        print("  luma-foreman get <bundle> --from <catalog>")
        return 0

    configured = config.catalog_source(project_root)
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
        return show(wanted)

    return _err(f"unknown: catalog {verb} (try luma-foreman catalog --help)")
