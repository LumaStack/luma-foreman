"""Words this project retired, still in use.

**A retired word comes back by being reinvented, not by being remembered.** The
words worth retiring are usually the natural English for what they described, so
absence from a repository is a weak defence — an author reaches for one again and
it reads as a fresh choice rather than a revival. That happened here within
minutes of a sweep that removed one.

**Every hit is a notice, never a finding, because a grep cannot tell a revival
from a legitimate use.** *Projection* has an ordinary mathematical sense. *Jobs*
means something real in a sentence about continuous integration. A quotation of
somebody else's prose is not a revival, and neither is an example of what not to
write. The check is handing over a judgement it cannot make, so it owes the
reader what the judgement needs: the term, what replaced it, where that was
decided, and the line as written.

**Nothing is retired by default.** The list is a project's own, declared in its
config, and a project that declares none skips this entirely — a tool shipping
opinions about English would be wrong everywhere at once.
"""

from __future__ import annotations

import re
import subprocess
import tomllib
from pathlib import Path

from ..finding import Notice, Result, Skipped

RULE = "vocabulary"

# Two places a retired word is correct rather than stale, and both are records
# of a moment rather than statements about now.
#
# A published `## Version` entry says what was true when it was written; editing
# it to use today's words falsifies the changelog. And the record that retires a
# word has to name the word — it is the one document that cannot avoid it.
VERSION_HEADING = re.compile(r"^##+\s+Version\s*$", re.M)

# A changelog is a version history for a whole repository rather than one
# bundle. Same argument, no heading to key on: an entry describes the release it
# shipped in and is wrong the moment it is modernised.
HISTORY = {"CHANGELOG.md"}

CONFIG = ".luma/config/luma-foreman.toml"


def _git(repo: Path, *args: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=120
    )
    if out.returncode not in (0, 1):
        raise RuntimeError(out.stderr.strip() or "git failed")
    return [line for line in out.stdout.splitlines() if line]


def _retired(repo: Path) -> list[dict]:
    """`[[retired]]` from the project's config, or nothing."""
    path = repo / ".luma" / "config" / "luma-foreman.toml"
    if not path.is_file():
        return []
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return []
    entries = data.get("retired")
    if not isinstance(entries, list):
        return []
    return [e for e in entries if isinstance(e, dict) and e.get("term")]


def _searchable(text: str) -> str:
    """*text* with its `## Version` history blanked out.

    Blanked rather than removed, so a line number still points at the line it
    did before.
    """
    match = VERSION_HEADING.search(text)
    if match is None:
        return text
    head, tail = text[: match.start()], text[match.start():]
    return head + re.sub(r"[^\n]", " ", tail)


def check(repo: Path) -> Result:
    retired = _retired(repo)
    if not retired:
        return Result(
            skipped=[
                Skipped(
                    RULE,
                    "nothing is retired — no [[retired]] in the project config",
                    "A retired word is a project's own decision. Declare one in "
                    ".luma/config/luma-foreman.toml with what replaced it and "
                    "where that was decided.",
                )
            ]
        )

    if not (repo / ".git").exists():
        return Result(skipped=[Skipped(RULE, "not a git repository", "run inside a repository")])
    try:
        tracked = _git(repo, "ls-files")
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return Result(skipped=[Skipped(RULE, f"could not list tracked files: {exc}", "")])

    result = Result(ran=[RULE])

    for entry in retired:
        term = str(entry["term"])
        replacement = str(entry.get("use", "") or "")
        decided = entry.get("decided") or []
        decided = [decided] if isinstance(decided, str) else [str(d) for d in decided]
        allowed = [str(x) for x in (entry.get("except") or [])]
        pattern = re.compile(rf"(?<![\w-]){re.escape(term)}(?![\w-])", re.I)

        hits: list[str] = []
        for rel in tracked:
            # A vendored bundle is somebody else's prose. This project's
            # retirement does not bind them, and there is nothing to fix here.
            if rel.startswith(".luma/bundles/"):
                continue
            # The config naming the term matches itself, always.
            if rel == CONFIG or Path(rel).name in HISTORY:
                continue
            # The record that retired a word is the one document that cannot
            # avoid naming it, and a project may exempt others it has read.
            if any(Path(rel).name.startswith(d) for d in decided):
                continue
            if any(rel == a or rel.startswith(a.rstrip("/") + "/") for a in allowed):
                continue
            path = repo / rel
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for number, line in enumerate(_searchable(text).splitlines(), 1):
                if pattern.search(line):
                    hits.append(f"{rel}:{number}: {line.strip()[:100]}")

        if not hits:
            continue

        remedy = f"`{term}` was retired"
        if decided:
            remedy += f" by {', '.join(decided)}"
        remedy += ". "
        remedy += f"Use {replacement}. " if replacement else ""
        remedy += (
            "Each line above may be a revival or an ordinary use of the word — "
            "read it and decide. A quotation, an example of what not to write, "
            "and a different sense of the same word are all correct as they "
            "stand."
        )
        result.notices.append(
            Notice(
                rule=RULE,
                summary=f"{len(hits)} use(s) of `{term}`, which this project retired",
                evidence=tuple(hits[:10]),
                remedy=remedy,
            )
        )

    return result
