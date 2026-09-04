"""Adopted bundles that are no longer what was adopted.

**Adoption without this check is just a copy.** The record in `MANIFEST.md`
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

    # A namespaced entry always carries a checksum and says where it came from.
    # That invariant is what makes every vendored copy verifiable, and it holds
    # precisely because a bundle keeps its `local/` ID for as long as a
    # publication request is outstanding — before the merge it has not been
    # published, and the request may yet be declined.
    #
    # An entry that breaks it is not a bundle in a bad state; it is a receipt
    # nothing can check, and `state()` skips the comparison when the checksum is
    # empty — so the drift check passes for it silently, forever. That is the
    # one failure the checksum exists to prevent.
    #
    # **The commit is deliberately not required.** A catalog that is not a git
    # checkout has none to record, which `get` already reports as `(not a git
    # checkout)` rather than treating as an error. Demanding it here would make
    # a sanctioned adoption report as broken.
    unverifiable = [
        f"{bundle_id} {entry.version}".rstrip()
        for bundle_id, entry in sorted(recorded.items())
        if entry.namespace != adoption.LOCAL
        and not (entry.checksum and (entry.catalog or entry.source))
    ]
    if unverifiable:
        bad(
            "high",
            f"{len(unverifiable)} entry(s) claim a catalog namespace without "
            f"custody and a checksum",
            unverifiable,
            "A bundle under a catalog's namespace is a vendored copy, and one "
            "nothing can verify is a receipt nobody can check — the drift check "
            "passes for it silently. Re-take it with `luma-foreman get "
            "<bundle>`. A bundle written here and not yet published belongs "
            "under local/, whether or not a catalog has been asked to take it.",
        )

    if missing:
        bad(
            "high",
            f"{len(missing)} adopted bundle(s) are recorded but not here",
            missing,
            "Re-adopt them, or drop the entry from .luma/bundles/MANIFEST.md. "
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
            "Housekeeping in .luma/bundles/MANIFEST.md.",
        )

    return result
