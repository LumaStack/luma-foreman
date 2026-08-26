"""What a project took, and proof of what it looked like.

The model behind ``adopted.toml``. Three commands need it and they need it for
three different reasons — ``adopt`` writes it, ``outfit`` reads it to know what
there is to project, and ``inspect`` re-derives the checksum to find out whether
anybody edited the copy. Putting the format in one place is what keeps those
three from disagreeing about it.

**It is not a lockfile, though it resembles one.** Bundles are committed, so
nothing is ever restored from this file. It answers three questions only: has
anyone edited this copy, is a newer version available, and what was this taken
alongside.
"""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass
from pathlib import Path

# macOS writes these into any directory Finder has looked at. No bundle ever
# intends one, so hashing them would report drift that says nothing about the
# bundle — the one exclusion, named rather than generalised into a pattern list.
IGNORED = {".DS_Store"}

HEADER = """\
# Written by luma-foreman. Do not edit by hand.
#
# checksum covers every file in the vendored copy: sha256 over each file's own
# sha256, in sorted path order. Editing this value makes the drift check start
# passing silently, which is the one failure it exists to prevent.
"""


@dataclass(frozen=True)
class Adopted:
    """One bundle's line in ``adopted.toml``."""

    bundle: str
    version: str
    source: str
    commit: str
    checksum: str

    @property
    def namespace(self) -> str:
        return self.bundle.split("/", 1)[0]

    @property
    def name(self) -> str:
        return self.bundle.split("/", 1)[-1]


def luma_dir(project: Path) -> Path:
    return project / ".luma"


def bundles_dir(project: Path) -> Path:
    return luma_dir(project) / "bundles"


def manifest_path(project: Path) -> Path:
    return bundles_dir(project) / "adopted.toml"


def vendored(project: Path, bundle: str) -> Path:
    """Where a bundle lives once adopted: ``.luma/bundles/<org>/<name>/``.

    The namespace is in the path because it is what tells an adopted bundle from
    one this project wrote. A ``vendor/`` directory would put the same fact in
    two places, and two copies of one fact can disagree.
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
    """Every adopted bundle, keyed by ID. Empty when nothing has been adopted.

    An entry missing a field it should have is dropped rather than raised on:
    the file is machine-written, so a malformed one means something went wrong
    upstream of here, and the caller's job is to report that rather than to
    crash inside a read.
    """
    path = manifest_path(project)
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


def write(project: Path, entries: dict[str, Adopted]) -> None:
    """Rewrite the whole file from *entries*, sorted by bundle ID.

    Whole-file rather than in-place because the file has no hand-written
    content to preserve — it says so at the top — and rewriting is the only way
    a removed adoption actually leaves.
    """
    lines = [HEADER]
    for bundle in sorted(entries):
        e = entries[bundle]
        lines.append(
            f'["{bundle}"]\n'
            f'version  = "{e.version}"\n'
            f'source   = "{e.source}"\n'
            f'commit   = "{e.commit}"\n'
            f'checksum = "{e.checksum}"\n'
        )
    path = manifest_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
