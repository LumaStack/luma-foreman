"""What a check reports.

Two kinds of outcome matter, and conflating them is how an inspection lies. A
check that ran and found nothing is a pass. A check that could not run — because
what it needed was absent — is NOT a pass, and must never be rendered as one.
That distinction is the whole reason `Skipped` exists alongside `Finding`.
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
    skipped: list[Skipped] = field(default_factory=list)
    ran: list[str] = field(default_factory=list)

    def extend(self, other: "Result") -> None:
        self.findings.extend(other.findings)
        self.skipped.extend(other.skipped)
        self.ran.extend(other.ran)

    def sorted_findings(self) -> list[Finding]:
        return sorted(self.findings, key=lambda f: (f.rank, f.rule, f.summary))
