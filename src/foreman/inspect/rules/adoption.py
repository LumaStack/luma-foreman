"""Adopted bundles that are no longer what was adopted.

**Adoption without this check is just a copy.** The record in `adopted.toml`
claims a project holds a particular bundle at a particular version, byte for
byte; nothing enforces that claim, and every way it can go wrong is quiet.

Three states, and the third is the one nothing else would ever surface:

| | |
| --- | --- |
| **edited** | somebody changed the vendored copy. Their change dies at the next `get`, and upstream never hears about it |
| **missing** | the record says a bundle is here and it is not. Every link into it is broken |
| **unapplied** | the bundle is present, unedited, and **no agent has ever seen it** — taken, and routed nowhere |

*Unapplied* looks correct from every angle: the directory is there, the
checksum matches, the report is green. The project is carrying rules nobody
reads.

**What this rule cannot answer is whether a newer version exists.** That needs
the catalog, and `inspect` runs in a bare clone with no network. A check that
silently degraded when offline would be worse than one that never claimed to.
"""

from __future__ import annotations

from pathlib import Path

from ... import adoption
from ..finding import Finding, Result, Skipped

RULE = "adoption"


def check(repo: Path) -> Result:
    recorded = adoption.read(repo)
    present = set(adoption.discover(repo))

    if not recorded and not present:
        return Result(
            skipped=[
                Skipped(
                    RULE,
                    "nothing adopted — .luma/bundles/ is absent or empty",
                    "luma-foreman catalog show <catalog>",
                )
            ]
        )

    result = Result(ran=[RULE])

    def bad(sev: str, summary: str, evidence: list[str], remedy: str) -> None:
        result.findings.append(
            Finding(
                rule=RULE,
                severity=sev,
                surface="working-tree",
                summary=summary,
                evidence=tuple(sorted(evidence)[:10]),
                remedy=remedy,
            )
        )

    edited: list[str] = []
    missing: list[str] = []
    for bundle_id, entry in sorted(recorded.items()):
        match adoption.state(repo, entry):
            case "missing":
                missing.append(f"{bundle_id} {entry.version}")
            case "edited":
                edited.append(f"{bundle_id} {entry.version}")

    if missing:
        bad(
            "high",
            f"{len(missing)} adopted bundle(s) are recorded but not here",
            missing,
            "Re-adopt them, or drop the entry from .luma/bundles/adopted.toml. "
            "Anything linking into a bundle that is not there is already broken.",
        )

    if edited:
        bad(
            "high",
            f"{len(edited)} adopted bundle(s) have been edited in place",
            edited,
            "An adopted bundle is a copy — the next `get` overwrites it and the "
            "change is gone, and upstream never learns anybody wanted it. Move "
            "the change into your own namespace, or propose it to the catalog "
            "the bundle came from.",
        )

    # Being present and unedited says nothing about whether anything reads it.
    # This is the state that reports green while a project quietly carries rules
    # no agent has ever been shown.
    unapplied = [b for b in present if not adoption.applied(repo, b)]
    if unapplied:
        bad(
            "medium",
            f"{len(unapplied)} bundle(s) are adopted but reach no agent",
            sorted(unapplied),
            "Run `luma-foreman apply`. A bundle nothing projects is present, "
            "checksummed, reported clean, and never loaded — which looks "
            "identical to working.",
        )

    orphaned = sorted(set(recorded) - present)
    if orphaned and not missing:
        bad(
            "low",
            f"{len(orphaned)} record(s) name a bundle that is not on disk",
            orphaned,
            "Housekeeping in .luma/bundles/adopted.toml.",
        )

    return result
