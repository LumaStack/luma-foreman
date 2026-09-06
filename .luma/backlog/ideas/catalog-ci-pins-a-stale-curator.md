---
type: luma/idea
title: The catalog's gate pins a curator that keeps falling behind
created: { by: agent:claude-opus-5, at: 2026-09-06T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: next
scope: project
stage: draft
---

# The catalog's gate pins a curator that keeps falling behind

**Belongs to `luma-catalog`, parked here until it can be moved.**

**`luma-catalog`'s pre-merge job pins `luma-catalog-curator` and `luma-foreman`
by SHA, and the curator pin is several merges behind.** Pinning is right — a
gate that floats changes what it enforces without anybody deciding to. Falling
behind silently is not.

**A weekly job existed to notice, went red on twenty consecutive merges, and
was deleted rather than repaired.** The workflow's own comment now records that
nothing notices when a pin moves. So the mechanism that would have caught this
was removed *because* it kept correctly reporting the problem.

## Why it matters more than a stale dependency usually would

**This gate is what publication rests on.** Merging to `main` is publication —
there is no tag, no release and no registry — and this job is the only thing
between a bundle and being available to everyone. A gate running an old checker
enforces an old set of rules, and nothing in the output says which.

It also cuts against the curator's own stated purpose. A catalog is meant never
to be in a corrupt state; a pin nobody watches means the checker's fixes do not
reach the one catalog that wired it as a gate.

## What would fix it, and what would not

**Not a floating pin.** That trades a silent staleness for a silent change in
what is enforced, which is worse for the same reason.

**A job that reports rather than fails is what was tried**, and it was deleted
for being noisy. So the question is not *how do we notice* — that was solved
and then thrown away — but **what makes a notice actionable enough that nobody
deletes it**. Bumping on a schedule, or opening a pull request that updates the
pin rather than a run that goes red, are both worth weighing.

## Notes

Found while building `publish`, and recorded until now only in an appendix to
`.luma/backlog/plans/bundle-publish.md`.
