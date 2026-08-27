---
type: luma/idea
title: The lifecycle ladder is written one way, and a record sometimes has to come back down
created: { by: human:benlinton, at: 2026-08-26T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: organization
lifecycle_status: draft
---

# A record sometimes has to come back down

`decision-guidelines` describes `lifecycle_status` as a mutability ladder and
every transition in it climbs: `draft` becomes `provisional` becomes `stable`,
and `archived` is the exit. **Nothing describes going the other way.**

So a reader who discovers that a `provisional` record was never actually settled
has two apparent options, and both are wrong. Edit it anyway, which the ladder
forbids — only `draft` permits changing the decision. Or supersede it, which
archives a record that was not a decision in the first place and leaves a
successor claiming to replace something that never held.

**The honest answer is neither: return it to `draft`.** The status was the
error, not the position, and correcting a status to match reality is what
`provisional` permits — *the explanation, freely and in place*. What was
explained wrongly is how settled the thing was.

## Where it happened

`luma-foreman` recorded five decisions in one day and promoted four of them
while the argument was still running. Two positions in ADR-0003 moved the same
afternoon, and one — that only two commands may reach the network — turned out
to be wrong on its own terms once `catalog list` was written. All four went back
to `draft`.

Nothing in the bundle said that was allowed, and the alternative on offer was
superseding four records that had never been in force.

## What it needs to say

**Demotion is the owner's act, like promotion.** [[a-reminder-needs-somewhere-to-live]]
argues promotion must not happen by side effect; the same holds in reverse, and
for a sharper reason — a record that quietly loses its status is a record whose
citations silently stop meaning what they said.

**And it has to leave a mark.** A dated note in the record, because somebody
cited it while it was `provisional` and needs to find out why it is not any
more. Promotion can be silent; demotion cannot.

## What is unresolved

**Whether `stable` may be demoted at all.** `provisional` to `draft` is
correcting a status nobody had leaned on for long. `stable` to anything is
different: `stable` is the status that says *cite this*, and taking it back
retroactively makes every citation wrong. That may be the case where
supersession genuinely is the only honest route.

**Whether a demoted record keeps its number.** It should — the number is the
handle, and nothing about the position moved. But that is worth saying, because
the instinct on discovering a record was wrong is to start a new one.
