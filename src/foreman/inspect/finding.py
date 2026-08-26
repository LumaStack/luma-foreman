"""What a check reports.

Three kinds of outcome, and conflating any two is how an inspection lies.

A check that ran and found nothing is a pass. A check that could not run —
because what it needed was absent — is NOT a pass, and must never be rendered
as one; that is why `Skipped` exists. And a thing worth a reader's attention
that is not a defect is neither, which is why `Notice` does.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Ordered worst first, so sorting is just this tuple's index.
SEVERITIES = ("high", "medium", "low")

# The four places a leak lives. Named because the non-obvious ones are where
# leaks actually happen: everyone greps the working tree, nobody checks the
# commit metadata, and history outlives deletion.
SURFACES = ("working-tree", "commit-metadata", "history", "config")


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    surface: str
    summary: str
    evidence: tuple[str, ...] = ()
    remedy: str = ""

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"unknown severity: {self.severity}")
        if self.surface not in SURFACES:
            raise ValueError(f"unknown surface: {self.surface}")

    @property
    def rank(self) -> int:
        return SEVERITIES.index(self.severity)

    def as_dict(self) -> dict[str, object]:
        return {
            "rule": self.rule,
            "severity": self.severity,
            "surface": self.surface,
            "summary": self.summary,
            "evidence": list(self.evidence),
            "remedy": self.remedy,
        }


@dataclass(frozen=True)
class Notice:
    """Something worth a reader's judgement, which must not fail a build.

    **A finding says what is wrong. A notice says what to look at.** The
    difference is who decides: a finding has already decided, and a notice
    cannot — because the check that raised it does not have what it would take.

    So a notice carries *more* context than a finding, not less. Somebody is
    being asked to make a call, and `remedy` is where the basis for it goes:
    what was expected, what decided that, and where to read why.

    **It counts for nothing in the exit code.** A heuristic wired to a merge
    gate is a heuristic somebody switches off, and every reason to raise a
    notice rather than a finding is a reason it will sometimes be wrong.
    """

    rule: str
    summary: str
    evidence: tuple[str, ...] = ()
    remedy: str = ""

    def as_dict(self) -> dict[str, object]:
        return {
            "rule": self.rule,
            "summary": self.summary,
            "evidence": list(self.evidence),
            "remedy": self.remedy,
        }


@dataclass(frozen=True)
class Skipped:
    """A check that could not run, and why.

    Rendered as loudly as a finding. An inspection that reports "clean" while
    silently skipping half its checks is worse than no inspection, because it
    manufactures confidence that was never earned.
    """

    rule: str
    reason: str
    remedy: str = ""

    def as_dict(self) -> dict[str, object]:
        return {"rule": self.rule, "reason": self.reason, "remedy": self.remedy}


@dataclass
class Result:
    findings: list[Finding] = field(default_factory=list)
    notices: list[Notice] = field(default_factory=list)
    skipped: list[Skipped] = field(default_factory=list)
    ran: list[str] = field(default_factory=list)

    def extend(self, other: "Result") -> None:
        self.findings.extend(other.findings)
        self.notices.extend(other.notices)
        self.skipped.extend(other.skipped)
        self.ran.extend(other.ran)

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: (f.rank, f.rule, f.summary))
