"""Identifying the project a session is working in.

This is the logic the shell implementation had to duplicate between the gate and
the CLI, with a comment in each telling the reader to keep them in sync by hand.
It exists once now. That was one of the reasons to leave shell.
"""

from __future__ import annotations

import os
from pathlib import Path


def repo_root(start: Path) -> Path | None:
    """Nearest ancestor of *start* containing ``.git``, or None.

    ``.git`` may be a file rather than a directory — that is how worktrees and
    submodules record their location — so this tests for existence, not for a
    directory. A worktree therefore resolves to itself and gets its own policy,
    which is deliberate: a worktree is a separate working context.
    """
    for d in (start, *start.parents):
        if (d / ".git").exists():
            return d
    return None


def canonical(path: str | os.PathLike[str]) -> Path:
    """Resolve symlinks so two spellings of one directory agree.

    Load-bearing on macOS, where /tmp is a symlink to /private/tmp: the hook
    receives whichever form the session started with, while the CLI computes
    its own from the resolved form. If these disagree the hook reads a policy
    file the CLI never writes, and nothing appears to be wrong.
    """
    try:
        return Path(path).resolve()
    except OSError:
        return Path(path)


def slug(path: Path) -> str:
    """Name a directory the way Claude Code names ~/.claude/projects entries.

    The absolute path with every "/" and "." replaced by "-". Matching Claude
    Code's own scheme means a project's policy file and its transcript
    directory carry the same name, which makes them findable together.
    """
    return str(path).replace("/", "-").replace(".", "-")


def resolve(cwd: str | os.PathLike[str]) -> tuple[Path, str]:
    """The project directory for *cwd*, and its slug.

    The repository root when there is one, so that every session in a repo
    shares a policy no matter which subdirectory it started in; otherwise the
    directory itself.
    """
    real = canonical(cwd)
    return (root := repo_root(real) or real), slug(root)
