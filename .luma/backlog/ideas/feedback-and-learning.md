---
type: luma/idea
title: Telling people when it did not work, and learning from that
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: someday
scope: project
lifecycle_status: draft
---

# Telling people when it did not work, and learning from that

**Two unbuilt things, and the second depends on the first.**

**Alert people when things do not work.** `inspect` reports to whoever ran it.
Nothing reaches somebody who did not run it, so a project that drifts stays
drifted until a person happens to look.

**Ways the system can learn and improve.** The least specified thing recorded
anywhere about foreman, and the most interesting.

## Why the order is fixed

**Learning needs a record of outcomes, and alerting is what produces one.** A
system that never notices a failure has nothing to learn from; one that reports
every failure to a person has a log of what actually went wrong, which is the
input the second half needs. Building them in the other order gives a learner
with no evidence.

## What makes it hard to specify

**Learn *what*, from *whom*, and applied *where*?** A rule that fires constantly
and is always overridden is evidence the rule is wrong; a bundle nobody opens is
evidence it should not be adopted. **Both are observations about behaviour, and
foreman currently observes none.** Deciding what it is allowed to observe is
probably the first real question, and it is a privacy question before it is a
design one.

## Notes

Absorbed from `docs/scope.md` when that document was scattered on 2026-08-29,
where it was two bullets under *feedback*. Kept together because the dependency
between them is the only structure either has.
