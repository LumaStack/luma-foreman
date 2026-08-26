"""Stand `.luma/` up in a repository that has none.

**The whole job is a directory, a descriptor, and refusing to guess.** There is
no template to choose and nothing to configure, because everything else in
`.luma/` arrives when something writes to it — `bundles/` on the first `get`,
`config/` when a setting is actually set.

Follows `luma/luma-layout`'s `initialize-luma`, which is the specification for
this: create only what will have contents, add no `.gitignore` entry, and
commit before using. That workflow is what an agent reads; this is the same
thing as one command.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import project

USAGE = """Stand `.luma/` up in a repository that does not have one.

  luma-foreman init                 initialize this repository
  luma-foreman init --to <dir>      a directory other than this one

Creates `.luma/PROJECT.md` and `.luma/records/`, and nothing else. `bundles/`
appears on the first `luma-foreman get`; `config/` when a setting needs one. An
empty directory is a question a reader has to answer, so none is created ahead
of having contents.

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


def _err(message: str) -> int:
    print(f"luma-foreman init: {message}", file=sys.stderr)
    return 2


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman init: {summary}", file=sys.stderr)
    print(f"  {remedy}", file=sys.stderr)
    return 1


def run(target: Path) -> int:
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

    (luma / "records").mkdir(parents=True)
    descriptor = luma / "PROJECT.md"
    descriptor.write_text(DESCRIPTOR.format(title=root.name))

    print(f"initialized {luma.relative_to(target) if target in luma.parents else luma}")
    print()
    print("  PROJECT.md   describe this repository — every TODO is yours to answer")
    print("  records/     empty, for whatever writes a decision or an audit first")
    print()
    # Git tracks files rather than directories, so `records/` cannot be
    # committed while it is empty. Saying so beats letting somebody discover it
    # when the directory is missing from a fresh clone.
    print("Git does not track an empty directory, so `records/` joins the")
    print("repository with whatever is written into it first.")
    print()
    print("  Nothing to gitignore — .luma/ is committed in full. Anything here")
    print("  that should not be is machine-local and belongs in ~/.config/luma/.")
    print()
    print("  Then: luma-foreman get luma/<bundle> --from <catalog>")
    return 0


def main(argv: list[str]) -> int:
    target: Path | None = None
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
            return _err(f"unknown option: {arg}")

    return run(target or Path.cwd())
