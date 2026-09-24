---
type: work-item
key: FORE-0029
title: Consumer records resolve no contract, so validation never sees them
workflow_status: captured
rank: 010.0280.000
kind: idea
stage: draft
created: {by: 'agent:claude-fable-5', at: '2026-09-20T00:00:00'}
description: 'The shape of it, in this repository: Resolution walks upward from a document, looking for `type_definitions/<name>/DEFINITION.md` under each ancestor — the spec''s rule, generalized the way LKF''s roadmap leans (Where `type_definitions/` resolves: the directory root a Document is found under). The vendored contract sits on a sibling branch, so the walk never sees it; the type resolves to nothing, and an undefined type is never reported (the permissive-conformance law). The same shape holds for luma-backlog''s ~100 work items against `local/backlog`''s own contracts, and for every violation and decision record in the estate.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:42Z'}
---

# Consumer records resolve no contract, so validation never sees them

**Every record in every consuming repository is invisible to `luma-foreman
lint`.** Found the day the linter shipped, by its first ripple: the sweep
contract moved to `0.0.2`, this repository's sweep charter still cited
`0.0.1`, and lint said nothing — not because the check is wrong, but because
the record resolves no contract at all.

The shape of it, in this repository:

```
.luma/
  backlog/sweeps/the-whole-of-foreman/charter.md     type: sweep
  bundles/lumastack/luma-catalog/review-sweeps/
    type_definitions/sweep/DEFINITION.md             the contract
```

Resolution walks **upward** from a document, looking for
`type_definitions/<name>/DEFINITION.md` under each ancestor — the spec's rule,
generalized the way LKF's roadmap leans (*Where `type_definitions/` resolves*:
the directory root a Document is found under). The vendored contract sits on a
**sibling branch**, so the walk never sees it; the type resolves to nothing,
and an undefined type is never reported (the permissive-conformance law). The
same shape holds for luma-backlog's ~100 work items against
`local/backlog`'s own contracts, and for every violation and decision record
in the estate. Validation works today only where documents and contracts share
a root: catalogs, bundles, and clarify-style notebooks.

## The decision this waits on

This is the parked `.luma/type_definitions/` question with a consequence
attached. Three answers, mutually exclusive:

1. **Keep the project-root store, and fill it.** Contracts a project's records
   use are placed (or projected by `apply`, mechanically) at
   `.luma/type_definitions/` — then the upward walk from anything under
   `.luma/` finds them, and currency starts firing for consumer records. This
   is precisely the job `luma-layout`'s policy already assigns the directory,
   including its disambiguation rule for when two adopted bundles disagree.
   An `apply`-projected copy would want the generated-content marker.
2. **Teach resolution to look inside adopted bundles.** No new directory, but
   it reopens what `luma-layout` already answered: two adopted bundles may
   legitimately hold different versions of one type, and a record outside
   both gives resolution no way to pick. Any tiebreak invented here is a
   private rule a second consumer would guess differently — the exact failure
   namespacing exists to prevent.
3. **Accept the gap.** Validation covers only shared-root cases; consumer
   records go unvalidated. Free, and it quietly caps what `type_version`
   bought — migration-by-query works estate-wide, but currency-by-lint stops
   at bundle boundaries.

The lean recorded when the store was kept "for a while" (2026-09-20): option 1
is what the directory exists for, and `apply` projecting contracts mechanically
would keep it out of hand-maintenance. Whatever is decided should be fed back
to LKF's roadmap item, which is tracking the same question from the
specification's side.

## What unblocks

Consumer-side `type_version` currency — the check the migration bought,
firing where most of the estate's typed documents actually live — and honest
`lint` coverage for the records registers (violations, decisions, work items)
whose contracts are all vendored today.

## Related work

- Born from the idea it replaces: [`consumer-records-resolve-no-contract`](../../ideas/consumer-records-resolve-no-contract.md)
