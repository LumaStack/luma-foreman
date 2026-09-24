# Journal — Test backlog in a new project

> The work item's memory. Newest entry first; everything below the top block is
> historical. Append, never curate. Shape: `spec.md` §5.5.

---

## ▶ 2026-09-24

The allowlist fix from BACK-0108 holds here: 61 ideas, 5 plans and a sweep under .luma/backlog/ produce no parse warnings on any command.
decision list does return this repo's 14 ADRs, but .luma/records/decisions/ is inside the allowlist by design — the ADRs sit at the location the tool and the record-decision procedure both own, so this is not the BACK-0108 leak returning.
ADR-0011 carried lifecycle: draft where the rest carry stage: draft, so it listed with a blank status. Last record in the whole estate still using the retired field; fixed. lifecycle stays live in BUNDLE.md manifests, which is a different field.
Outcome 'the tool reads only records it wrote' is removed, not abandoned. Its verify_by required that decisions this tool did not write be absent from listings, but .luma/records/decisions/ is inside the allowlist by design — the outcome demanded the opposite of the intended behaviour, so it was never a requirement to drop. Deleted as a same-day draft; abandon would have left it counting as unmet and forced --force on close, recording a failure that did not happen.
work-item new derived the actor from the OS account — created.by: human:<os-user> — because LUMA_BACKLOG_ACTOR was unset. Hand-corrected. The only mechanism is an env var, which cannot be committed, so a fresh machine repeats it. This is what disproved the create-and-read outcome.
A disproven outcome renders as passing. The verdict is correct on disk (as: disproven) but list --tree marks it passing and show counts it toward 3 of 4 proven. showing-records already concedes the gap — an outcome is unverified or passing with nothing between — so the display model has no room for a verdict the record can hold.
