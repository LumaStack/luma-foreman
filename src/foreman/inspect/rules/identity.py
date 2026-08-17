"""Personal information published through git.

The rule that started this repository, because it bit its own maintainer:
a personal address, two former employers' addresses, and a handful of machine
hostnames were sitting in public history while the documentation looked clean.

Everything here is detectable by SHAPE, so it needs no configuration and runs in
a bare clone. `alice@laptop.local` is identifiable as machine-derived without
knowing who alice is. That matters: an optional identity list would make this
check better, but requiring one would make it unrunnable in continuous
integration, which is the one place it most needs to run.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from ..finding import Finding, Result, Skipped

RULE = "identity"

# Git invents `user@hostname` when no user.email is configured. These are the
# shapes that produces, and they leak machine and internal network names.
MACHINE_SUFFIX = re.compile(r"@[^@]*\.(local|localdomain|lan|home|internal|localhost)$", re.I)
# A home directory in tracked content. The username is the payload.
#
# The leading character must not be a dot: a real username does not start with
# one, and without that guard this matches constructed paths like
# "$TMP/home/.config/..." and reports ".config" as a person. Found by running
# this rule against its own repository.
HOME_PATH = re.compile(r"/(?:Users|home)/([A-Za-z0-9_-][A-Za-z0-9._-]*)/")
# Addresses git accepted that are not addresses at all — a typo'd user.email
# produces a valid-looking identity that no pattern-based cleanup will match.
MALFORMED = re.compile(r"^[^@]+$")

NOREPLY = re.compile(r"@users\.noreply\.github\.com$|^noreply@|@noreply\.", re.I)
BOT = re.compile(r"\[bot\]|^(?:actions|dependabot|github-actions)@", re.I)


def _git(repo: Path, *args: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        timeout=120,
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "git failed")
    return [line for line in out.stdout.splitlines() if line]


def check(repo: Path) -> Result:
    result = Result(ran=[RULE])

    if not (repo / ".git").exists():
        return Result(skipped=[Skipped(RULE, "not a git repository", "run inside a repository")])

    try:
        identities = _git(repo, "log", "--all", "--format=%ae%n%ce")
        taggers = [
            t.strip("<>")
            for t in _git(repo, "for-each-ref", "refs/tags", "--format=%(taggeremail)")
            if t.strip("<>")
        ]
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return Result(
            skipped=[Skipped(RULE, f"could not read git history: {exc}", "check the repository is intact")]
        )

    # Taggers are counted with authors deliberately. Annotated tags carry their
    # own identity, and a cleanup that rewrites commits and forgets tags leaves
    # the address in place while looking finished.
    everyone = identities + taggers
    if not everyone:
        return Result(skipped=[Skipped(RULE, "repository has no commits", "")])

    counts: dict[str, int] = {}
    for email in everyone:
        counts[email] = counts.get(email, 0) + 1

    machine = {e: n for e, n in counts.items() if MACHINE_SUFFIX.search(e)}
    malformed = {e: n for e, n in counts.items() if MALFORMED.match(e)}

    if machine:
        result.findings.append(
            Finding(
                rule=RULE,
                severity="high",
                surface="commit-metadata",
                summary=f"{len(machine)} machine-derived author identities publish hostnames",
                evidence=tuple(f"{e} ({n} occurrences)" for e, n in sorted(machine.items(), key=lambda kv: -kv[1])),
                remedy="Set user.email explicitly, and `git config --global user.useConfigOnly true` "
                "so git refuses to invent one.",
            )
        )

    if malformed:
        result.findings.append(
            Finding(
                rule=RULE,
                severity="medium",
                surface="commit-metadata",
                summary=f"{len(malformed)} author identities are not valid email addresses",
                evidence=tuple(f"{e} ({n} occurrences)" for e, n in sorted(malformed.items(), key=lambda kv: -kv[1])),
                remedy="A typo'd user.email still commits. These match no pattern-based cleanup "
                "and must be listed literally to be fixed.",
            )
        )

    # Home paths in tracked content. Scanned through git so ignored files and
    # the working directory's own state cannot affect the answer.
    try:
        hits = _git(repo, "grep", "-nIE", r"/(Users|home)/[A-Za-z0-9_-][A-Za-z0-9._-]*/", "--", ".")
    except (OSError, RuntimeError, subprocess.SubprocessError):
        hits = []
    users: dict[str, str] = {}
    for line in hits:
        if match := HOME_PATH.search(line):
            name = match.group(1)
            if name not in ("runner", "root", "user", "name", "your-name", "<name>"):
                users.setdefault(name, line[:120])
    if users:
        result.findings.append(
            Finding(
                rule=RULE,
                severity="medium",
                surface="working-tree",
                summary=f"home directory paths for {len(users)} user(s) appear in tracked files",
                evidence=tuple(f"{name}: {where}" for name, where in sorted(users.items())),
                remedy="Replace with ~ or a placeholder. A home path names the machine's user.",
            )
        )

    real = {e for e in counts if not NOREPLY.search(e) and not BOT.search(e)}
    if len(real) > 3:
        result.findings.append(
            Finding(
                rule=RULE,
                severity="low",
                surface="history",
                summary=f"{len(real)} distinct non-bot author identities in history",
                evidence=tuple(
                    f"{e} ({counts[e]})" for e in sorted(real, key=lambda e: -counts[e])[:8]
                ),
                remedy="Expected in a repository with many contributors. In a personal one it "
                "usually means identity drifted across machines and jobs.",
            )
        )

    return result
