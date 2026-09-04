"""`remove` — dropping a bundle this project holds.

**The inverse of `get`, and shaped like it.** Both take one bundle ID, both act
on this project alone, both finish the moment they return. That symmetry is
true — unlike `publish`, which is gated by somebody else's decision and cannot
be shaped this way.

**It is a command rather than a note telling somebody to use `rm`** because the
directory is only half of it: the manifest entry has to go, and `apply` has to
run afterwards so the generated skills and the project index stop naming a
bundle that left. Deleting the directory by hand leaves a receipt for something
that is not there.

**The guard keys on recoverability, not on where the bundle came from.** The
question worth asking before destroying anything is *does something else hold
this* — and the answer differs by state rather than by kind:

    vendored, clean    `get` restores it byte-identical; the checksum proves it
    local, committed   git restores it
    local, dirty       nothing holds it
    vendored, edited   nothing holds the edits

So the rule is one sentence covering both kinds: **refuse when removing would
lose work nothing else holds.** That generalises the refusal `get` already
makes over an edited copy rather than inventing a second, differently-shaped
guard beside it.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from . import adoption, project

USAGE = """Remove a bundle from this project, and drop its entry from the manifest.

  luma-foreman remove <bundle>          remove one — e.g. lumastack/luma-catalog/git-secrets
  luma-foreman remove <bundle> --force  remove it even though nothing else holds it

A bare bundle name works where only one namespace holds it; where two do, the
refusal names them and asks for the fully qualified <namespace>/<name>.

This refuses when removing would lose work nothing else has a copy of — a
bundle written here that is not committed, or a vendored copy somebody edited.
Anything else is recoverable, and the output says how.

  --to <project>     the project to remove from (default: this repository)

Run `luma-foreman apply` afterwards, so the generated skills and the project
index stop naming what left.

Exit codes: 0 removed, 1 refused, 2 could not run."""

# Written by `apply` from the manifest and the bundles on disk, so they heal by
# regeneration rather than by editing. Naming a bundle here is not a reference
# anybody has to repoint — reporting them as such would bury the hand-written
# ones that do need attention.
GENERATED = (
    ".luma/bundles/INDEX.md",
    ".luma/bundles/MANIFEST.md",
    ".luma/bundles/routing.toml",
    "CLAUDE.md",
    ".claude/skills/",
)


def _err(message: str) -> int:
    print(f"luma-foreman remove: {message}", file=sys.stderr)
    return 2


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman remove: {summary}", file=sys.stderr)
    for line in remedy.splitlines():
        print(f"  {line}", file=sys.stderr)
    return 1


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


def committed(project_root: Path, home: Path) -> bool:
    """Does git hold everything in *home* exactly as it is on disk?

    One question, asked of the whole directory at once: `status --porcelain`
    over a path reports modifications, staged changes and untracked files
    alike, and any of the three means deleting the directory loses something
    git cannot give back. Empty output is the only answer that means safe.

    A directory outside a repository, or a git that will not run, is not
    committed — the honest answer when nothing can be verified is *no*.
    """
    if _git(project_root, "rev-parse", "--git-dir") is None:
        return False
    status = _git(project_root, "status", "--porcelain", "--", str(home))
    return status == ""


def references(project_root: Path, bundle_id: str, home: Path) -> list[str]:
    """Files that name *bundle_id*, excluding the bundle itself and generated ones.

    Removing a bundle silently turns anything that cited it into a dangling
    reference. `inspect` reports a dangling *wikilink* afterwards, but a bundle
    is just as often cited as a bare path in prose, which nothing catches — so
    a warning before is worth more than a finding that never comes.
    """
    listed = _git(project_root, "grep", "-l", "--fixed-strings", bundle_id)
    if listed is None:
        return []
    try:
        rel_home = home.relative_to(project_root).as_posix()
    except ValueError:
        rel_home = None
    out = []
    for path in listed.splitlines():
        if rel_home and (path == rel_home or path.startswith(rel_home + "/")):
            continue
        if any(path == g or path.startswith(g) for g in GENERATED):
            continue
        out.append(path)
    return sorted(out)


def run(project_root: Path, requested: str, force: bool) -> int:
    entries = adoption.read(project_root)
    found = adoption.resolve(entries, requested)
    if isinstance(found, str):
        return _err(found)
    entry = found
    bundle_id = entry.bundle
    home = adoption.vendored(project_root, bundle_id)
    vendored = bool(entry.source or entry.catalog) and bool(entry.checksum)
    state = adoption.state(project_root, entry)

    # Nothing on disk. The entry is the only thing left, and dropping it is
    # repair rather than removal — so it never refuses, whatever the guard
    # would have said about content that is not there.
    if state == "missing":
        del entries[bundle_id]
        adoption.write(project_root, entries)
        print(f"{bundle_id}: entry dropped — nothing was on disk")
        print()
        print("  Then: luma-foreman apply")
        return 0

    # Asked before anything is deleted. Afterwards `status` reports the removal
    # itself as a change, so the same call would answer "not committed" for a
    # bundle git holds perfectly well — and the recovery line would be wrong in
    # exactly the case somebody needs it.
    was_committed = committed(project_root, home)

    if not force:
        if vendored and state == "edited":
            return _refuse(
                f"{bundle_id} has been edited here",
                "Nothing else holds those edits — the catalog has the "
                "unedited\n"
                "bundle, and this copy is no longer it.\n"
                "If the edits are disposable:\n"
                f"  luma-foreman remove {bundle_id} --force",
            )
        if not vendored and not was_committed:
            return _refuse(
                f"{bundle_id} has uncommitted work",
                "Nothing else holds it — not git, and no catalog.\n"
                "Commit it first, or:\n"
                f"  luma-foreman remove {bundle_id} --force",
            )

    citing = references(project_root, bundle_id, home)

    shutil.rmtree(home)
    del entries[bundle_id]
    adoption.write(project_root, entries)

    print(f"removed  {bundle_id}")
    # Say which case it was: the routes recover differently, so a reader needs
    # to know which one they are in — and the line that says how is worth more
    # than the one that says it happened.
    if vendored and state == "ok":
        print("  the catalog has it — recover with:")
        print(f"    luma-foreman get {bundle_id}")
    elif was_committed:
        rel = home.relative_to(project_root).as_posix()
        print("  it was committed — recover with:")
        print(f"    git checkout HEAD -- {rel}")
    else:
        print("  forced — nothing else held it, so this is not recoverable")

    if citing:
        print()
        print(f"  {len(citing)} file(s) still name it:")
        for path in citing:
            print(f"    {path}")
        print("  Those are dangling now. Repoint or remove them.")

    print()
    print("  Then: luma-foreman apply")
    return 1 if citing else 0


def main(argv: list[str]) -> int:
    target: Path | None = None
    force = False
    requested: list[str] = []

    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--force":
            force = True
        elif arg == "--to":
            if not rest:
                return _err("--to needs a project directory")
            target = Path(rest.pop(0))
        elif arg.startswith("-"):
            return _err(f"unknown option: {arg}")
        else:
            requested.append(arg)

    if target and not target.is_dir():
        return _err(f"not a directory: {target}")
    project_root, _ = project.resolve(target or Path.cwd())

    if len(requested) != 1:
        return _err("usage: luma-foreman remove <bundle>")

    return run(project_root, requested[0], force)
