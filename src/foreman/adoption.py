"""What a project took, and proof of what it looked like.

The model behind ``MANIFEST.md`` — a receipt kept by commands. Three commands
need it and they need it for three different reasons — ``get`` writes it,
``apply`` reads it to know what there is to project, and ``inspect``
re-derives the checksum to find out whether anybody edited the copy. Putting
the format in one place is what keeps those three from disagreeing about it.

**It is not a lockfile, though it resembles one.** Bundles are committed, so
nothing is ever restored from this file. It records the unrecoverable facts —
custody, and intent (`register`) — and never derived state: whether a bundle
is *wired* is answered by comparison, not by a record that could lie.

**The legacy spelling, ``adopted.toml``, is still read** where no manifest
exists, and any write completes the migration by replacing it. A receipt that
quietly stopped being read would fail open.
"""

from __future__ import annotations

import hashlib
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

# macOS writes these into any directory Finder has looked at. No bundle ever
# intends one, so hashing them would report drift that says nothing about the
# bundle — the one exclusion, named rather than generalised into a pattern list.
IGNORED = {".DS_Store"}

HEADER = """\
<!-- Written by `luma-foreman`. Change it with commands, not by hand.
     sha256 covers every file in the vendored copy: sha256 over each file's
     own sha256, in sorted path order. Editing this value makes the drift
     check start passing silently, the one failure it exists to prevent. -->

# Bundles
"""

# One bullet per bundle, `key: value` sublines, nothing nested. The kinds are
# distinguished by shape: custody sublines mark a vendored copy, a bare entry
# is a bundle written here, and `register:` appears only when intent diverges
# from the default (wire everywhere).
ENTRY = re.compile(r"^- `([^`]+)`(?:\s+(\S+))?\s*$")
SUBLINE = re.compile(r"^  - ([a-z][a-z0-9_-]*):\s*(.*?)\s*$")


@dataclass(frozen=True)
class Adopted:
    """One bundle's entry in the manifest."""

    bundle: str
    version: str
    source: str
    commit: str
    checksum: str
    # Intent, divergence-only: "" means wire everywhere (the default);
    # "nothing" means deliberately landed and not wired. Values are what to
    # register into, never a boolean and never event data.
    register: str = ""

    # Split from the right: a namespace may have any number of segments, and
    # the bundle name is always the last one. `lumastack/luma-catalog/widgets`
    # is namespace `lumastack/luma-catalog`, name `widgets`.
    @property
    def namespace(self) -> str:
        return self.bundle.rsplit("/", 1)[0]

    @property
    def name(self) -> str:
        return self.bundle.rsplit("/", 1)[-1]


def luma_dir(project: Path) -> Path:
    return project / ".luma"


def bundles_dir(project: Path) -> Path:
    return luma_dir(project) / "bundles"


def manifest_path(project: Path) -> Path:
    return bundles_dir(project) / "MANIFEST.md"


def legacy_path(project: Path) -> Path:
    return bundles_dir(project) / "adopted.toml"


def vendored(project: Path, bundle: str) -> Path:
    """Where a bundle lives once adopted: ``.luma/bundles/<namespace>/<bundle-name>/``.

    The namespace is the catalog identifier, derived from the catalog's
    address — ``lumastack/luma-catalog`` — with any number of segments, the
    bundle name always the last. Two catalogs from one organization therefore
    vendor side by side, and a bundle's full ID says where it came from just
    by being read. It is in the path because a ``vendor/`` directory would put
    the same fact in two places, and two copies of one fact can disagree.
    """
    return bundles_dir(project) / bundle


def files(root: Path) -> list[Path]:
    """Every file in a bundle, sorted, in the order the checksum walks them."""
    return sorted(
        p for p in root.rglob("*") if p.is_file() and p.name not in IGNORED
    )


def checksum(root: Path) -> str:
    """``sha256:<hex>`` over a bundle's contents and their paths.

    Hashing each file's digest rather than concatenating the bytes means a byte
    moved across a file boundary cannot go unnoticed, and it bounds memory
    regardless of what a bundle carries. Paths are included because a renamed
    file is a changed bundle.
    """
    outer = hashlib.sha256()
    for path in files(root):
        rel = path.relative_to(root).as_posix()
        inner = hashlib.sha256(path.read_bytes()).hexdigest()
        outer.update(rel.encode("utf-8") + b"\0" + inner.encode("ascii") + b"\n")
    return f"sha256:{outer.hexdigest()}"


def discover(project: Path) -> dict[str, Path]:
    """Every bundle on disk, by ID, whether adopted or written here.

    One implementation because three callers ask and must agree: `apply` writes
    what it finds, `inspect` compares what it finds against the receipt, and a
    disagreement between them reports a bundle as both present and missing.

    **Any depth.** A namespace may be any number of segments, so a fixed
    `*/*/BUNDLE.md` finds nothing under `lumastack/luma-catalog/x` and reports
    an empty project rather than an error.

    **A bundle inside a bundle is not a concept the format has.** The outer one
    owns its whole tree; anything below is its content, not a second bundle.
    """
    root = bundles_dir(project)
    if not root.is_dir():
        return {}
    homes = {m.parent for m in root.rglob("BUNDLE.md")}
    return {
        home.relative_to(root).as_posix(): home
        for home in sorted(homes)
        if not any(other != home and other in home.parents for other in homes)
    }


def by_namespace(bundle_ids: list[str]) -> list[tuple[str, list[str]]]:
    """Bundle IDs grouped under their namespace, both sorted.

    Printed flat, every row repeats a namespace that is usually identical and
    is 23 characters wide for the universal catalog — a quarter of a laptop
    screen saying nothing that changes between rows. Grouped, the namespace is
    said once and stays visible when a project draws on more than one.
    """
    groups: dict[str, list[str]] = {}
    for bundle_id in bundle_ids:
        namespace, _, name = bundle_id.rpartition("/")
        groups.setdefault(namespace, []).append(name)
    return [(ns, sorted(names)) for ns, names in sorted(groups.items())]


def applied(project: Path, bundle_id: str) -> bool:
    """Has this bundle ever been written into what an agent reads?

    Deliberately weak. Whether what was written is *current* is what
    `luma-foreman apply --check` answers, and a second implementation of that
    comparison would be a second thing to keep true. This answers the cruder
    and more damaging question: has anybody ever seen this bundle.

    Two files, and both have to be right. The adapter in ``CLAUDE.md`` is what
    a harness loads; the project index is what names the bundle. Either one
    missing means nothing reaches an agent, and checking only the index would
    report green for a project whose harness was never wired to read it.
    """
    from . import apply  # imported here: apply reads this module at import time

    claude = project / "CLAUDE.md"
    index = project / apply.INDEX
    if not index.is_file():
        # The predecessor artifact, read until the next apply sweeps it — a
        # project mid-migration still reaches its agent through it, and
        # reporting every bundle unreachable would be the check lying.
        index = project / apply.LEGACY_ENTRYPOINT
    if not claude.is_file() or not index.is_file():
        return False
    try:
        adapter = claude.read_text(encoding="utf-8")
        named = index.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    return apply.BEGIN in adapter and bundle_id in named


def same_origin(a: str, b: str) -> bool:
    """Do two recorded sources name the same catalog?

    **Compared after normalising, because the raw strings disagree over things
    that are not disagreements.** One repository recorded this catalog as
    `.../luma-catalog` and another as `.../luma-catalog.git`; git accepts both,
    GitHub serves both, and a literal comparison called them different lineages
    and refused every upgrade.

    **The refusal it guards is the right one** — a bundle quietly acquiring a
    different origin is a change nobody would see — which is exactly why it must
    not fire on a suffix. The workaround is `--force`, and `--force` performs the
    real lineage switch too: teaching somebody to reach for it while the check is
    being pedantic is how they reach for it on the day it is right.

    What is normalised is only what cannot distinguish two repositories: a
    trailing slash, a trailing `.git`, the scheme, an embedded user, and the
    case of the host. **The path keeps its case** — hosts are case-insensitive
    and paths are not, everywhere except the one forge everybody tests on.
    """
    return _origin(a) == _origin(b)


def origin(source: str) -> str:
    """The normalised identity of a recorded source — what `same_origin`
    compares, public so a listing can group by it rather than by spelling."""
    return _origin(source)


def _origin(source: str) -> str:
    s = source.strip().rstrip("/")
    if s.endswith(".git"):
        s = s[:-4]
    # scp-style, which has no scheme: git@host:org/repo
    scp = re.match(r"^[^/@]+@([^:/]+):(.+)$", s)
    if scp:
        return f"{scp.group(1).lower()}/{scp.group(2)}"
    url = re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://(?:[^@/]+@)?([^/]+)(/.*)?$", s)
    if url:
        return f"{url.group(1).lower()}{url.group(2) or ''}"
    # scp-style without a user: github.com:LumaStack/luma-catalog. The host
    # must contain a dot, or a relative path with a colon in it would be read
    # as a remote.
    bare = re.match(r"^([A-Za-z0-9][A-Za-z0-9.-]*\.[A-Za-z0-9.-]+):([^/].*)$", s)
    if bare:
        return f"{bare.group(1).lower()}/{bare.group(2)}"
    # A filesystem path. Left alone beyond the two suffixes above, because its
    # case is load-bearing and it has no host to fold.
    return s


def state(project: Path, entry: Adopted) -> str:
    """``ok``, ``edited`` or ``missing`` — what this copy is right now.

    One implementation because two commands ask: `inspect --rule adoption`
    turns it into findings, and `bundle list` prints it in a column. They
    disagreeing about what *edited* means is the failure this prevents.

    Answered from committed state alone, so it holds in a bare clone. Whether a
    *newer* version exists is a different question and needs the network —
    that is `bundle outdated`.
    """
    home = vendored(project, entry.bundle)
    if not home.is_dir():
        return "missing"
    if entry.checksum and checksum(home) != entry.checksum:
        return "edited"
    return "ok"


def read(project: Path) -> dict[str, Adopted]:
    """Every bundle the manifest records, keyed by ID.

    Prefers ``MANIFEST.md``; falls back to the legacy ``adopted.toml`` where
    no manifest exists yet. An entry missing a field it should have is kept
    with the field empty rather than raised on: the file is machine-written,
    so a malformed one means something went wrong upstream of here, and the
    caller's job is to report that rather than to crash inside a read.
    """
    path = manifest_path(project)
    if path.is_file():
        try:
            return parse(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            return {}
    return _read_legacy(project)


def parse(text: str) -> dict[str, Adopted]:
    """The manifest's line grammar. Unknown sublines are ignored, not errors."""
    out: dict[str, Adopted] = {}
    current: dict[str, str] | None = None

    def flush() -> None:
        if current is not None:
            checksum = current.pop("sha256", "")
            out[current["bundle"]] = Adopted(
                bundle=current["bundle"],
                version=current.get("version", ""),
                source=current.get("source", ""),
                commit=current.get("commit", ""),
                checksum=f"sha256:{checksum}" if checksum else "",
                register=current.get("register", ""),
            )

    for line in text.splitlines():
        entry = ENTRY.match(line)
        if entry:
            flush()
            current = {"bundle": entry.group(1), "version": entry.group(2) or ""}
            continue
        sub = SUBLINE.match(line)
        if sub and current is not None:
            current[sub.group(1)] = sub.group(2)
    flush()
    return out


def emit(entries: dict[str, Adopted]) -> str:
    """The manifest's canonical rendering, sorted by bundle ID."""
    lines = [HEADER]
    for bundle in sorted(entries):
        e = entries[bundle]
        lines.append(f"- `{bundle}` {e.version}".rstrip())
        if e.source:
            lines.append(f"  - source: {e.source}")
        if e.commit:
            lines.append(f"  - commit: {e.commit}")
        if e.checksum:
            lines.append(f"  - sha256: {e.checksum.removeprefix('sha256:')}")
        if e.register:
            lines.append(f"  - register: {e.register}")
    return "\n".join(lines) + "\n"


def write(project: Path, entries: dict[str, Adopted]) -> None:
    """Rewrite the whole manifest from *entries*, and retire the legacy file.

    Whole-file rather than in-place because the file has no hand-written
    content to preserve — it says so at the top — and rewriting is the only way
    a removed adoption actually leaves. Any write completes the migration: two
    records of one fact could disagree, so the legacy file goes the moment the
    manifest exists.
    """
    path = manifest_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(emit(entries), encoding="utf-8")
    legacy_path(project).unlink(missing_ok=True)


def _read_legacy(project: Path) -> dict[str, Adopted]:
    path = legacy_path(project)
    if not path.is_file():
        return {}
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return {}

    out: dict[str, Adopted] = {}
    for bundle, entry in data.items():
        if not isinstance(entry, dict):
            continue
        out[bundle] = Adopted(
            bundle=bundle,
            version=str(entry.get("version", "")),
            source=str(entry.get("source", "")),
            commit=str(entry.get("commit", "")),
            checksum=str(entry.get("checksum", "")),
        )
    return out
