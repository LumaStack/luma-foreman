"""Stand `.luma/` up in a repository that has none.

**The whole job is a descriptor, a config, and refusing to guess.** Both files
have contents on the day they are written and both are committed; everything
else in `.luma/` arrives when something writes to it — `bundles/` on the first
`get`, `records/` on the first decision or audit.

Follows `luma-layout`'s `initialize-luma`: create only what will have
contents, add no `.gitignore` entry, and commit before using. That workflow is
what an agent reads; this is the same thing as one command.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import config, project
from . import catalog as catalogs

USAGE = """Stand `.luma/` up in a repository that does not have one.

  luma-foreman init                      initialize this repository
  luma-foreman init --catalog <source>   ...and record where bundles come from
  luma-foreman init --to <dir>           a directory other than this one

Creates `.luma/PROJECT.md` and `.luma/config/luma-foreman.toml`, and nothing
else. `bundles/` appears on the first `luma-foreman get` and `records/` on the
first decision or audit. An empty directory is a question a reader has to
answer, and git will not commit one anyway, so none is created ahead of having
contents.

Adds no `.gitignore` entry — `.luma/` is committed in full, and a project whose
`.luma/` differs between two machines is two projects.

Exit codes: 0 created, 1 refused, 2 could not run."""

DESCRIPTOR = """\
---
type: luma/project
title: {title}
disclosure_level: internal
description: >-
  TODO — one sentence, for somebody outside this repository. What is this, and
  when would a person or an agent open it rather than something else?
owns:
  - TODO — what decisions belong here and nowhere else
must_not_own:
  - TODO — what belongs to another repository, named
---

# {title}

TODO — what this repository is. The frontmatter above is read by tools; this
body is read by people and by agents arriving cold.

## Status

TODO — what works, what does not, and what somebody should not rely on yet.
"""


# A config carries what this project OVERRIDES, and as little else as possible.
# Every value written here is one an upgrade cannot move: defaults live in the
# tool and travel with it, so the smallest file is the one that ages best.
#
# The exception is a value with no default, or one nobody should discover by
# being surprised. `[catalog] source` is both, so it is written out even when
# it is only a comment.
#
# No commented-out defaults either. One is a behavioural override a keystroke
# away — somebody uncomments it to be explicit and freezes a value that should
# have followed the upgrade. Where settings get documented, this header should
# point at that rather than list them; there is nothing to point at yet.

CONFIG_HEADER = """\
# How luma-foreman behaves in this project. Committed, and shared by everyone.
#
# Kept minimal by design. What you leave out follows the tool and improves with
# it; what you set here is frozen, and every frozen value is one more thing to
# reconcile at upgrade.
"""

CONFIG_BLANK = CONFIG_HEADER + """
[catalog]
# Where `luma-foreman get` takes bundles from when no --from is given.
# No default — nothing can guess which catalog is yours.
# source = "https://github.com/LumaStack/luma-catalog"
"""

CONFIG_SET = CONFIG_HEADER + """
[catalog]
# Where `luma-foreman get` takes bundles from when no --from is given.
source = "{source}"
"""



# Where a project keeps records before it has a `.luma/`. The same list
# `record-decision` searches, which is what makes finding one here meaningful
# rather than a guess: these are the places a migration would be moving from.
ELSEWHERE = (
    "DECISIONS.md",
    "docs/DECISIONS.md",
    "docs/decisions",
    ".records",
)


def _records_elsewhere(target: Path) -> list[str]:
    return [p for p in ELSEWHERE if (target / p).exists()]


def _shown(path: Path) -> str:
    """A path as the operator would type it, absolute only when it has to be."""
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def _err(message: str) -> int:
    print(f"luma-foreman init: {message}", file=sys.stderr)
    return 2


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman init: {summary}", file=sys.stderr)
    print(f"  {remedy}", file=sys.stderr)
    return 1


def run(target: Path, catalog: str | None) -> int:
    if not target.is_dir():
        return _err(f"not a directory: {target}")

    # A descriptor claiming to describe a repository, written somewhere that is
    # not one, is the kind of file nobody notices is wrong until it travels.
    root = project.repo_root(project.canonical(target))
    if root is None:
        return _refuse(
            f"{_shown(target)} is not in a git repository",
            "`.luma/` is committed with the project, so there has to be a "
            "project. Run `git init` first.",
        )

    luma = target / ".luma"
    descriptor = luma / "PROJECT.md"
    config_file = config.config_path(target)

    # Idempotent, and never destructive. A file that is already there is left
    # exactly as it is — running this twice is how somebody adds what a newer
    # version writes, and refusing would make them do by hand what the refusal
    # had just finished diagnosing.
    plan = [
        (descriptor, DESCRIPTOR.format(title=root.name),
         "created — every TODO in it is yours to answer"),
        (config_file, CONFIG_SET.format(source=catalog) if catalog else CONFIG_BLANK,
         f"created — bundles come from {catalog}" if catalog else "created"),
    ]
    wrote: list[Path] = []
    kept: list[Path] = []
    done: list[tuple[Path, str]] = []

    for path, contents, note in plan:
        if path.exists():
            kept.append(path)
            done.append((path, "already there, left alone"))
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents)
        wrote.append(path)
        done.append((path, note))

    print("luma-foreman init:")
    width = max(len(_shown(p)) for p, _ in done)
    for path, note in done:
        print(f"  {_shown(path):<{width}}  {note}")

    print()
    if not wrote:
        print("Nothing to do.")
        return 0

    if catalog and config_file in kept:
        print("--catalog was not applied: the config already exists, and this")
        print("never overwrites one. Set [catalog] source in it by hand.")
        print()

    if descriptor in wrote:
        print("  Nothing to gitignore — .luma/ is committed in full. Anything here")
        print("  that should not be is machine-local and belongs in ~/.config/luma/.")
        print()

    # Two steps, because the first question is always what is on offer and the
    # answer is a command nobody guesses. Named concretely where the config
    # knows the catalog, so neither line has a placeholder to work out.
    source = catalog or config.catalog_source(target)
    print("Next steps:")
    if source:
        name = catalogs.short_name(source)
        steps = [
            (f"luma-foreman catalog show {name}", "what it publishes"),
            ("luma-foreman get luma/<bundle>", "take one"),
        ]
    else:
        steps = [
            ("luma-foreman catalog show <catalog>", "what a catalog publishes"),
            ("luma-foreman get luma/<bundle> --from <catalog>", "take one"),
        ]
    step_width = max(len(s) for s, _ in steps)
    for step, why in steps:
        print(f"  {step:<{step_width}}  {why}")

    # Only said when it is true. A standing pointer to a migration workflow is
    # noise in the common case, and the case it is for is one this can check.
    found = _records_elsewhere(target)
    if found:
        print()
        print(f"This project already keeps records in {', '.join(found)}.")
        print("The `migrate-into-luma` workflow in luma-layout moves an")
        print("existing project in, rather than leaving two places to look.")
    return 0


def main(argv: list[str]) -> int:
    target: Path | None = None
    catalog: str | None = None
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
        elif arg == "--catalog":
            if not rest:
                return _err("--catalog needs a path or a URL")
            catalog = rest.pop(0)
        else:
            return _err(f"unknown option: {arg}")

    return run(target or Path.cwd(), catalog)
