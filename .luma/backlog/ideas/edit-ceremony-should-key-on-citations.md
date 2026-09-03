---
type: luma/idea
title: What an edit to a decision costs should key on citations, not on stage
created: { by: agent:claude-opus-5, at: 2026-08-26T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: later
scope: organization
stage: draft
---

# Edit ceremony should key on citations, not on `stage`

`decision-guidelines` charges ceremony by status: `draft` lets the decision
move, `provisional` lets only the explanation move, `stable` needs agreement
first. **What that ceremony protects is citations** — the bundle says so
directly: *"an ADR number is a promise that the position never moved… cited in
commits, in conversation, and from other records, and every one of those
citations is wrong the moment the same number means something different."*

**Status and citation count usually correlate, and sometimes do not.** A
`provisional` record merged an hour ago in a single pull request has no
citations at all, and reversing it still costs a new number, an archival and a
`superseded_by`. The machinery runs at full price to protect nothing.

## The measurement is checkable, which recency is not

*It is only a day old* is unenforceable and slides a week at a time — that
argument is already settled in `decision-guidelines`, and this is not a
proposal to reopen it. **Counting inbound `ADR-NNNN` references is different**:
it is a fact about the repository, not a judgement about how long is long
enough, and a tool can produce the same answer twice.

An uncited record could then be revised in place regardless of status, and the
tool could say so rather than the author guessing.

## What it shares with the other half

[[a-reminder-needs-somewhere-to-live]] needs the same count for a different
reason — a citation appearing against a `draft` is what should trigger a
promotion request. **One implementation serves both**, and building it twice
would be the mistake. That is the strongest argument for doing either.

## What is unresolved

**Where the count comes from.** Commit messages, other records, policies, code
comments — and whether a mention inside `.luma/records/archived/` counts, given
nothing loads that directory by default.

**Whether it weakens the promise.** The ADR number's guarantee is worth
something *because* it is unconditional. *This number's position never moved,
unless nothing happened to be citing it at the time* is a weaker promise, and
somebody discovers the exception at the worst possible moment — when their
citation turns out to have been the second one, added after the check.

That objection may be fatal. It is the reason this is filed rather than
proposed.

## Notes

Raised while promoting two records in one afternoon, both of which turned out to
have stale claims and neither of which had a citation outside its own
repository. Belongs in `luma-catalog` if it goes anywhere — `decision-records`
is vendored here.
