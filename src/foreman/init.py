"""Stand `.luma/` up in a repository that has none.

**The whole job is a descriptor, a config, and refusing to guess.** Both files
have contents on the day they are written and both are committed; everything
else in `.luma/` arrives when something writes to it — `bundles/` on the first
`get`, `records/` on the first decision or audit.

Follows `luma/luma-layout`'s `initialize-luma`: create only what will have
contents, add no `.gitignore` entry, and commit before using. That workflow is
what an agent reads; this is the same thing as one command.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import adopt, project

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



def _shown(path: Path, target: Path) -> str:
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
    luma = target / ".luma"

    if luma.exists():
        # Not an error worth two exit codes: whether the right answer is
        # `migrate-into-luma` or just adding the one missing directory depends
        # on what is in there, and this command cannot tell.
        return _refuse(
            f"{luma} already exists — nothing to initialize",
            "Add what is missing, or see the `migrate-into-luma` workflow in "
            "luma/luma-layout for moving an existing structure into it.",
        )
    if not target.is_dir():
        return _err(f"not a directory: {target}")

    # A descriptor claiming to describe a repository, written somewhere that is
    # not one, is the kind of file nobody notices is wrong until it travels.
    root = project.repo_root(project.canonical(target))
    if root is None:
        return _refuse(
            f"{target} is not in a git repository",
            "`.luma/` is committed with the project, so there has to be a "
            "project. Run `git init` first.",
        )

    (luma / "config").mkdir(parents=True)
    (luma / "PROJECT.md").write_text(DESCRIPTOR.format(title=root.name))
    adopt.config_path(target).write_text(
        CONFIG_SET.format(source=catalog) if catalog else CONFIG_BLANK
    )

    print(f"initialized {_shown(luma, target)}")
    print()
    config = f"config/{adopt.CONFIG}"
    width = max(len("PROJECT.md"), len(config))
    print(f"  {'PROJECT.md':<{width}}  describe this repository — every TODO is yours")
    where = f"bundles come from {catalog}" if catalog else "where bundles come from, once you set it"
    print(f"  {config:<{width}}  {where}")
    print()
    print("  Nothing to gitignore — .luma/ is committed in full. Anything here")
    print("  that should not be is machine-local and belongs in ~/.config/luma/.")
    print()
    if catalog:
        print("  Then: luma-foreman get luma/<bundle>")
    else:
        print("  Then: luma-foreman get luma/<bundle> --from <catalog>")
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
