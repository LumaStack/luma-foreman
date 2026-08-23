"""Taking a bundle from a catalog and making it this project's own.

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

import os
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path

from . import adoption, lkf, project

USAGE = """Take a bundle from a catalog into this project, and record what you took.

  luma-foreman adopt <bundle>            adopt one — e.g. luma/decision-records
  luma-foreman adopt --list              what the catalog offers
  luma-foreman adopt <bundle> --force    overwrite a copy that exists or was edited

  --from <catalog>   a path to a catalog checkout, or a git URL. Defaults to
                     [catalog] source in .luma/config/foreman.toml
  --to <project>     the project to adopt into (default: this repository)

The bundle lands in .luma/bundles/<org>/<name>/ and is committed with the rest
of the project. Nothing is resolved and nothing is fetched later — bundles
depend on nothing, which is what keeps this a copy rather than an install.

Exit codes: 0 adopted, 1 refused, 2 could not run."""

URL = re.compile(r"^(https?://|git@|ssh://|git://)")


def _err(message: str) -> int:
    print(f"luma-foreman adopt: {message}", file=sys.stderr)
    return 2


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


# --------------------------------------------------------------------------
# finding a catalog


@dataclass(frozen=True)
class Catalog:
    """A catalog checkout on this machine, and where it came from."""

    root: Path
    source: str
    commit: str
    dirty: bool
    namespace: str | None

    def bundle(self, name: str) -> Path | None:
        manifest = self.root / "bundles" / name / "bundle.md"
        return manifest.parent if manifest.is_file() else None

    def names(self) -> list[str]:
        directory = self.root / "bundles"
        if not directory.is_dir():
            return []
        return sorted(
            p.name for p in directory.iterdir() if (p / "bundle.md").is_file()
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


def _configured(project_root: Path) -> str | None:
    """``[catalog] source`` from the project's committed foreman config."""
    path = project_root / ".luma" / "config" / "foreman.toml"
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    source = data.get("catalog", {}).get("source")
    return str(source) if source else None


def _root(start: Path) -> Path | None:
    """A catalog's content directory — where ``catalog.md`` sits.

    Checked one level down as well, because a catalog repository conventionally
    keeps its content under ``catalog/`` and pointing ``--from`` at the
    repository is what anybody would do.
    """
    for candidate in (start, start / "catalog"):
        if (candidate / "catalog.md").is_file():
            return candidate
    return None


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
            f"not a catalog: {checkout} — nothing named catalog.md here or in "
            f"catalog/"
        )

    commit = _git(root, "rev-parse", "HEAD") or ""
    status = _git(root, "status", "--porcelain")
    manifest = lkf.read(root / "catalog.md") or {}
    namespace = manifest.get("namespace")
    return Catalog(
        root=root,
        source=origin,
        commit=commit,
        dirty=bool(status),
        namespace=lkf.unquote(namespace) if namespace else None,
    )


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


def _resolve_id(catalog: Catalog, requested: str) -> tuple[str, str] | str:
    """Full bundle ID and bundle name, or a message saying what is wrong.

    A bundle is addressed ``<namespace>/<name>``, and **the namespace is the
    catalog's rather than the bundle's** — the same bundle promoted into
    another organization's catalog is that organization's to name.
    """
    if "/" in requested:
        namespace, name = requested.split("/", 1)
        if catalog.namespace and namespace != catalog.namespace:
            return (
                f"this catalog publishes {catalog.namespace}/, not {namespace}/ "
                f"— did you mean {catalog.namespace}/{name}?"
            )
        return f"{namespace}/{name}", name
    if catalog.namespace:
        return f"{catalog.namespace}/{requested}", requested
    return (
        f"name the namespace: {requested} is ambiguous, and this catalog "
        f"declares none of its own. Try <namespace>/{requested}."
    )


def run(
    requested: str,
    source: str,
    project_root: Path,
    force: bool,
) -> int:
    catalog = find(source)
    if isinstance(catalog, str):
        return _err(catalog)

    resolved = _resolve_id(catalog, requested)
    if isinstance(resolved, str):
        return _err(resolved)
    bundle_id, name = resolved

    src = catalog.bundle(name)
    if src is None:
        offered = ", ".join(catalog.names()) or "nothing"
        return _err(f"no bundle named {name} in this catalog (it offers: {offered})")

    manifest = lkf.read(src / "bundle.md") or {}
    version = lkf.unquote(manifest.get("version", ""))
    if not version:
        return _err(
            f"{bundle_id} declares no version — a bundle that cannot be pinned "
            f"cannot honestly be reported as adopted"
        )

    dst = adoption.vendored(project_root, bundle_id)
    entries = adoption.read(project_root)
    existing = entries.get(bundle_id)

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
    count = _copy(src, dst)
    entries[bundle_id] = adoption.Adopted(
        bundle=bundle_id,
        version=version,
        source=catalog.source,
        commit=catalog.commit,
        checksum=adoption.checksum(dst),
    )
    adoption.write(project_root, entries)

    verb = f"upgraded {upgrade} -> {version}" if upgrade else f"adopted {version}"
    print(f"{bundle_id}: {verb}")
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
    print("  Then: luma-foreman outfit")
    return 0


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman adopt: {summary}", file=sys.stderr)
    print(f"  {remedy}", file=sys.stderr)
    return 1


def listing(source: str) -> int:
    catalog = find(source)
    if isinstance(catalog, str):
        return _err(catalog)

    names = catalog.names()
    if not names:
        return _err(f"catalog at {catalog.root} publishes no bundles")

    prefix = f"{catalog.namespace}/" if catalog.namespace else ""
    width = max(len(n) for n in names) + len(prefix)
    for name in names:
        manifest = lkf.read(catalog.root / "bundles" / name / "bundle.md") or {}
        version = lkf.unquote(manifest.get("version", "?"))
        description = manifest.get("description", "")
        print(f"  {prefix + name:<{width}}  {version:<8}  {description}")

    if not catalog.namespace:
        print()
        print(
            "  This catalog declares no namespace, so a bundle here has no full\n"
            "  name. Adopt with an explicit one: luma-foreman adopt <namespace>/"
            f"{names[0]}"
        )
    return 0


def main(argv: list[str]) -> int:
    source: str | None = None
    target: Path | None = None
    force = False
    as_list = False
    requested: list[str] = []

    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--list":
            as_list = True
        elif arg == "--force":
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

    if source is None:
        source = _configured(project_root)
    if source is None:
        return _err(
            "no catalog — pass --from <path-or-url>, or set [catalog] source "
            "in .luma/config/foreman.toml"
        )

    if as_list:
        return listing(source)
    if len(requested) != 1:
        return _err("name exactly one bundle (or --list to see what there is)")
    return run(requested[0], source, project_root, force)
