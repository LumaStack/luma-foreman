---
type: workflow
title: Conduct an audit
description: Examine something, record what is wrong and why, and leave a record somebody else can act on. Use when auditing a codebase, a process, or any artifact that has a commit.
---

# Conduct an audit

## 1. Ask three questions before looking at anything

**An audit answers a question somebody has.** Guessing at it produces a document
nobody needed, and the guess does not show up in the result. Write the answers
into `audit.md` — they are the scope section, arrived at rather than
reconstructed.

### Targeted, or open-ended?

**Ask this first, before asking what is wrong.** Otherwise anyone with a
complaint ready gets a targeted audit without having chosen one — and the choice
matters more than the complaint does.

**Neither is the neutral option.** They are biased in opposite directions, and
picking one is picking which bias you would rather have.

| | **Targeted** | **Open-ended** |
| --- | --- | --- |
| **starts from** | problems you name | nothing |
| **biased toward** | what you already suspect | what is easy to notice |
| **finds** | instances, and how widespread they are | whatever is most prominent |
| **misses** | anything not shaped like the worry — **including its cause** | anything subtle, or with no obvious surface |
| **use when** | somebody is waiting on a specific answer | nobody knows where to look |

**Tunnel vision is the cost of targeting, and it has a specific shape: a problem
is usually a symptom, and an audit aimed at a symptom never looks at the cause.**
*The same mistake keeps happening* is almost always one.

**A targeted audit's finding count means little.** An auditor told to look for
something finds things shaped like it, because looking harder produces more.
**A long list is evidence of effort, not of severity** — read the severities.

**Open-ended is not unbiased either.** With nothing stated, an auditor reports
what it can see and argue: the countable, the greppable, the already familiar.
**An auditor who has just worked on the subject cannot run an open-ended audit
of it** — its own recent context is the anchor whether or not anyone named one.
Say so in `audit.md`, or use a session that has not seen the work. **This is the
same boundary independence turns on** ([[audit-layout]]): anchoring and
self-grading are one problem wearing two hats, and what carries between them is
the session.

### What problems do you want to target?

*Skip this if the audit is open-ended. An open-ended audit with a list of
problems attached is a targeted audit that has not admitted it.*

> *For example: something broke and you do not know how widely; the same mistake
> keeps recurring; you inherited this and do not trust it; a rule exists that
> nobody follows; you are about to publish and want to know what is
> embarrassing. Your own answer beats any of these.*

**Naming nothing is sometimes the better answer, and not only when you have no
complaints.** If you already know what is wrong, an audit that confirms it buys
little — where an open-ended one might find why it keeps happening. **Withhold a
suspicion deliberately and it becomes a test of the audit** rather than an
instruction to it.

**A targeted audit owes an answer to what it was aimed at, either way.**
*Asked to look for X. Found: two instances, F-002 and F-004* — or *Found: none,
in tracked content only.* **A negative is a result**, and often the point: it is
what lets somebody stop worrying, and an audit reporting only what it found
cannot say it.

### What is the scope of your search?

**Ask, do not infer.** The problems usually imply a scope, and implying is how
an audit ends up covering whatever was convenient.

- a single backlog item
- one feature, or one subsystem
- a directory tree
- one repository
- several repositories
- the whole estate

**Then ask what to leave out.** They usually know something that would cost a
day and answer nothing: vendored code, a subtree somebody else owns, generated
files, an area audited last month.

### When there is nobody to ask

**An audit may run unattended — in continuous integration, on a schedule, inside
a swarm.** It is open-ended, and `audit.md` says so: *"No interview conducted;
scope chosen by the auditor."* A reader can then tell an audit nobody anchored
from one where nobody was asked.

## 2. Pin the commit before you look at anything

```sh
git rev-parse --short=12 HEAD
```

**An audit is a claim about a specific state.** Pin it first, because a codebase
that moves under you produces findings that cannot be reproduced — and a finding
nobody can reproduce is one nobody has to answer.

```sh
DATE=$(date +%F)
SHA=$(git rev-parse --short=12 HEAD)
DIR=".luma/records/audits/${DATE}-${SHA}"
mkdir -p "$DIR/findings"
```

If several audits of the same commit will run on the same day, add a scope
suffix now rather than discovering the collision later:
`${DATE}-${SHA}-security`.

## 3. Write the scope down, including what you are not looking at

**Before examining anything.** Step 1 settled most of this; writing it down now
is what stops it being reconstructed later. **Scope recorded afterwards is scope
fitted to what you happened to find.**

**The half people skip is what was excluded.** *"Reviewed the HTTP layer; did not
examine authentication or the data model"* lets a reader tell *examined and
clean* from *never looked*. Without it, a clean audit is indistinguishable from
a shallow one.

**Exclusions come from two places and both belong here** — what you were told to
leave out, and what you decided to. Say which is which where it matters: an area
the owner ruled out reads differently from one you ran out of time for.

## 4. Examine

Where a tool does part of the job, run it and keep the output as evidence rather
than as findings. `luma-foreman inspect` and its equivalents belong here.

**Tool output is not yet an audit.** Eleven instances of one pattern is one
finding with eleven locations. The judgement — does this matter, by whose rule,
what does it cost — is the part you are here to add.

## 5. Write one file per finding

```
findings/F-001-<short-slug>.md
```

Numbered from `F-001`, stable within this audit, and the handle every response
and verification will use.

**Required when more than one auditor is running** — a swarm writing into a
single file is one merge conflict per agent. Recommended even alone; see
[[audit-layout]].

Each finding carries condition, criteria, cause, effect and recommendation, with
severity rated on consequence rather than effort. [[writing-findings]] covers
what makes each of those actionable, and [the finding template](../templates/finding.md)
has the shape.

## 6. Write `audit.md`

Scope, commit, what was excluded, who audited, and a summary of the findings by
severity. Not a restatement of them — a reader should be able to decide from this
file alone whether they need to read the rest.

**Plus what step 1 settled:** whether this was targeted or open-ended, what it
was aimed at, and — for a targeted audit — **the answer to that aim, including
when the answer is *nothing found***.

[The audit template](../templates/audit.md).

## 7. Stop before writing the response

**You are not the party that answers this.** An auditor who writes the response
is grading their own work, and the record loses the only property that made it
worth keeping.

**Hand off to a separate session, and prefer a different model.** The boundary is
the session rather than the identity — a fresh session of the same model is a
legitimate respondent, and a different model answering is better still. **This
session continuing into the response is the weakest arrangement**: permitted, but
it has to be disclosed in `response.md` so a reader can weigh it. The ladder is in
[[audit-layout]].

**It is the easiest failure to commit by accident**, because the session that
just finished the audit is the one still open, and carrying on looks like
momentum rather than a lost property.

## 8. Commit it

One commit, the whole audit directory. It is a record: append-only, dated, and
never edited afterwards. What happens next is written by somebody else in their
own file.
