---
type: document
title: Sweeps and audits
description: Why these are different practices rather than two rigours of the same one — what each is complete against, which one puts somebody on the hook, and the two kinds of independence they need for opposite reasons.
---

# Sweeps and audits

**They look alike from a distance and the resemblance is getting closer**,
which is why this is written down rather than left to be re-derived every time
somebody asks.

**An audit answers a question. A sweep covers a territory.**

An audit can examine three files and be finished, if those three answered what
it was aimed at. A sweep is not finished until every row in its index is
accounted for. **Coverage is what a sweep sells; a verdict is what an audit
sells.**

## The differences that survive

| | **audit** | **sweep** |
| --- | --- | --- |
| **complete when** | the question is answered | every file is accounted for |
| **obligation created** | somebody accountable **must respond** to each finding | none — findings join the backlog like any other observation |
| **the second party is** | accountable for the thing being examined | a collaborator trying to understand the same thing |
| **pinned to** | one commit | nothing — it spans weeks and the code moves |
| **lifecycle** | `records/` — append-only, settles | `backlog/` — churns, then evaporates |
| **usually** | demanded | chosen |

## Obligation is the one to remember

**An audit puts somebody on the hook.** A respondent accountable for the thing
takes a position on every finding — agreed, partially, disagreed, accepted —
and the auditor then closes it. **That exchange is the record**, and producing
it is what an audit is for.

**A sweep puts nobody on the hook.** Its findings become ideas, or backlog
items, or nothing at all. There is no respondent because there is no
accountability axis — only two parties reading the same code, trying to
understand it.

That is also why the two lifecycles differ. An exchange somebody owes an answer
to has to be append-only and has to settle. A pile of observations nobody owes
anything on can churn and then evaporate, because everything worth keeping left
at the slice that produced it.

## Coverage is what the machinery is for

**Everything structural in a sweep exists to make one claim true**: nothing was
missed. The index, the order chosen on purpose, the estimate, the exclusions
written down, *read with nothing found* being a recordable result — none of it
is about finding defects, and all of it is about being able to say afterwards
that the whole territory was looked at.

**An audit needs none of that**, because it never has to prove it looked
everywhere. It only has to say what it *did not* look at, which is one
paragraph rather than a ledger.

**So a sweep cannot be pinned to a commit and an audit must be.** A claim about
one instant is what makes a finding reproducible; a claim about complete
coverage takes weeks, and the code moves underneath it the whole time.

## Both need independence, for opposite reasons

The mechanism is identical — separate sessions — and the purpose is not, which
is worth holding onto because it decides what a violation costs.

| | independence protects against | so the failure is |
| --- | --- | --- |
| **audit** | **self-grading** — answering your own finding | a record whose only valuable property is gone |
| **sweep** | **anchoring** — being shown a view before forming one | a review with two names on it and one judgement in it |

**A sweep needing independence is recent.** It was written as a person reading
with an agent, where independence looked impossible and undesirable; once
either seat could be an agent, the pairing turn turned out to depend on exactly
the same session boundary an audit does. Same tool, different job.

## Which to reach for

| | |
| --- | --- |
| somebody is waiting on an answer | **audit** |
| someone has to formally respond — accountability, handover, compliance | **audit** |
| something broke and nobody knows how widespread it is | **audit**, targeted |
| you want to be able to say all of it has been looked at | **sweep** |
| you want to know your own system | **sweep** |
| nobody knows where to look and there are weeks available | **sweep** |

**They feed each other.** A sweep that turns up something genuinely needing an
accountable answer raises an audit. An audit concluding *this whole subsystem
is untrustworthy* is a good reason to start a sweep.

## The wrinkle, stated rather than hidden

**The shapes have converged.** A sweep with no person in it — recording
findings, handing them to a third party who fixes them — is structurally close
to auditor, respondent, verifier. Anyone comparing the two on structure alone
will struggle to tell them apart.

**What still separates them is that the fixer is not a respondent.** Nobody is
accountable, nobody must take a position, and nothing settles. The findings are
work waiting to be done rather than claims waiting to be answered.

**If sweeps start needing formal responses, that is the signal they have become
audits**, and the answer is to use that practice rather than to grow a response
mechanism here. Watch for it — it would arrive as a reasonable-sounding request
for the fixer to record why they disagreed.

*Audits are `audit-records`'. It is named rather than linked, because it is a
separate bundle and may not be adopted here.*
