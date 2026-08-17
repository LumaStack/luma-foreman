"""Credentials published through git.

Two properties matter more than coverage.

**Findings never contain the secret.** They are printed to terminals, pasted
into issues, and captured in continuous integration logs — all places a leaked
credential travels further than it did in the repository. Evidence is a
location and a kind, with the value redacted to a short prefix.

**False positives are the failure that matters.** A scanner that cries wolf gets
switched off, and a switched-off scanner protects nothing. So this ships only
patterns with a distinctive prefix and a fixed shape — the ones a provider
designed to be recognisable. Entropy heuristics and `password = "..."` matching
find more and are wrong far more often; they are deliberately absent.

What this is not: a replacement for a dedicated scanner. It does not scan
history, and it says so rather than implying a clean bill of health.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from ..finding import Finding, Result, Skipped

RULE = "secrets"

# Provider-issued credentials with a distinctive prefix and a fixed shape.
# Anything needing entropy scoring or surrounding context to judge does not
# belong here.
#
# Each entry carries TWO patterns, and the reason is not cosmetic. `git grep -E`
# speaks POSIX ERE: `\b` matches nothing at all — silently, so the scanner just
# finds less — and `(?:...)` is a fatal error. The searching is done in ERE for
# speed across a whole tree; the confirming and redacting is done in Python,
# where word boundaries actually work.
PATTERNS: tuple[tuple[str, str, re.Pattern[str]], ...] = (
    ("AWS access key id",
     r"AKIA[0-9A-Z]{16}", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub personal access token",
     r"gh[pousr]_[A-Za-z0-9]{36}", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b")),
    ("GitHub fine-grained token",
     r"github_pat_[A-Za-z0-9_]{22,}", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}")),
    ("Slack token",
     r"xox[baprs]-[A-Za-z0-9-]{10,}", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Slack webhook",
     r"https://hooks\.slack\.com/services/T[A-Za-z0-9/+]{20,}",
     re.compile(r"https://hooks\.slack\.com/services/T[A-Za-z0-9/+]{20,}")),
    ("Stripe live key",
     r"[sr]k_live_[A-Za-z0-9]{24,}", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{24,}")),
    ("Anthropic API key",
     r"sk-ant-[A-Za-z0-9_-]{20,}", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}")),
    ("OpenAI API key",
     r"sk-[A-Za-z0-9]{48}", re.compile(r"\bsk-[A-Za-z0-9]{48}\b")),
    ("Google API key",
     r"AIza[0-9A-Za-z_-]{35}", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("npm access token",
     r"npm_[A-Za-z0-9]{36}", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("PyPI upload token",
     r"pypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{50,}",
     re.compile(r"\bpypi-AgEIcHlwaS5vcmc[A-Za-z0-9_-]{50,}")),
    ("private key block",
     r"-----BEGIN ([A-Z ]+ )?PRIVATE KEY-----",
     re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
)

# Files whose very presence in a repository is the finding — no content match
# needed. Cheaper and more reliable than scanning them.
SECRET_FILES = re.compile(
    r"(?:^|/)(?:"
    r"\.env(?:\.[A-Za-z0-9_-]+)?"
    r"|id_(?:rsa|dsa|ecdsa|ed25519)"
    r"|.*\.(?:pem|pfx|p12|jks|keystore|ppk)"
    r"|\.npmrc|\.pypirc|\.netrc"
    r")$"
)

# Names that exist to be committed. `.env.example` is the documented way to ship
# a template, and flagging it teaches people to ignore the scanner.
TEMPLATE_SUFFIX = re.compile(
    r"\.(?:example|sample|template|dist|tpl)$|(?:^|/)(?:example|sample|template)\.", re.I
)


def _git(repo: Path, *args: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=120
    )
    if out.returncode not in (0, 1):  # 1 == grep found nothing
        raise RuntimeError(out.stderr.strip() or "git failed")
    return [line for line in out.stdout.splitlines() if line]


def _redact(value: str) -> str:
    """Enough to recognise it, not enough to use it."""
    keep = 4 if len(value) > 12 else 2
    return f"{value[:keep]}{'…' * 3} ({len(value)} chars)"


def check(repo: Path) -> Result:
    if not (repo / ".git").exists():
        return Result(skipped=[Skipped(RULE, "not a git repository", "run inside a repository")])

    result = Result(ran=[RULE])

    try:
        tracked = _git(repo, "ls-files")
    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        return Result(skipped=[Skipped(RULE, f"could not list tracked files: {exc}", "")])

    # --- files that should never be committed at all -------------------------
    risky = [
        f for f in tracked if SECRET_FILES.search(f) and not TEMPLATE_SUFFIX.search(f)
    ]
    if risky:
        result.findings.append(
            Finding(
                rule=RULE,
                severity="high",
                surface="working-tree",
                summary=f"{len(risky)} file(s) that normally hold credentials are tracked",
                evidence=tuple(sorted(risky)[:10]),
                remedy="Remove from the index, add to .gitignore, and rotate anything they "
                "held — deleting the file does not unpublish what was already pushed.",
            )
        )

    # --- credentials inside tracked content ----------------------------------
    hits: dict[str, list[str]] = {}
    for name, ere, pattern in PATTERNS:
        try:
            # -e is required, not stylistic: the private-key pattern begins with
            # "-----" and git would otherwise parse it as options.
            lines = _git(repo, "grep", "-nIE", "-e", ere, "--", ".")
        except (OSError, RuntimeError, subprocess.SubprocessError):
            continue
        for line in lines:
            location, _, text = line.partition(":")
            lineno, _, body = text.partition(":")
            if TEMPLATE_SUFFIX.search(location):
                continue
            if match := pattern.search(body):
                hits.setdefault(name, []).append(f"{location}:{lineno}  {_redact(match.group(0))}")

    if hits:
        total = sum(len(v) for v in hits.values())
        evidence: list[str] = []
        for name in sorted(hits):
            evidence.append(f"{name}:")
            evidence.extend(f"  {where}" for where in sorted(hits[name])[:5])
        result.findings.append(
            Finding(
                rule=RULE,
                severity="high",
                surface="working-tree",
                summary=f"{total} credential(s) of {len(hits)} kind(s) in tracked content",
                evidence=tuple(evidence),
                remedy="Rotate them first — they are published and rewriting history does not "
                "recall them. Then remove and add the paths to .gitignore.",
            )
        )

    # --- what this did NOT look at -------------------------------------------
    # A credential committed and deleted later is still published, and that is
    # where most real leaks live. Saying nothing here would let a clean report
    # imply a guarantee this rule cannot make.
    result.skipped.append(
        Skipped(
            RULE,
            "history was not scanned — only the current tracked content",
            "A secret removed in a later commit is still published. For history, use a "
            "dedicated scanner such as gitleaks or trufflehog.",
        )
    )
    return result
