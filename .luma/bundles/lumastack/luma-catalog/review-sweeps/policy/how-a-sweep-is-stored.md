---
type: policy
title: How a sweep is stored
description: Where a review sweep lives, why it is backlog rather than a record, and the two units — the file that must be covered and the cluster actually reviewed in one go.
matches:
  - topic: running or resuming a review sweep
  - path: ".luma/backlog/sweeps/**"
---

# How a sweep is stored

A **sweep** is one party reading a codebase from one end to the other, with a
second beside it. **Usually a person with an agent, and not necessarily** — see
[[who-does-the-reading]]. It runs for as long as it takes — hours, days,
sometimes more — and survives every session boundary in between.

```
.luma/backlog/sweeps/the-cli-surface/
  sweep.md                    scope, exclusions, the order chosen, the index
  slices/
    001-entrypoint-and-args.md
    002-the-permission-gate.md
```

## It is backlog, not a record

**The tier is decided by lifecycle, and a sweep in progress is an intention.**
It churns — the index is edited at every slice, files are added when the tree
moves under it, rows go from pending to reviewed or approved. `records/` is
append-only and never edited, so a sweep filed there would break the tier on
its first day.

**A sweep evaporates; an audit settles.** That is the lifecycle half of a
larger distinction — what each is complete against, which one puts somebody on
the hook, and why both need independence for opposite reasons. It is in
[[sweeps-and-audits]] rather than here, because most work inside a sweep never
has to ask it.

**Do not file a sweep as an audit to make it look more rigorous.** It produces
a commit pin that is false by the third file, and a record nobody owes an
answer to, filed where things that settle are kept.

*Audits are `audit-records`'. Where a sweep turns up something that genuinely
wants an accountable answer, that is a finding to raise there — not a reason to
restructure the sweep.*

## The slices are the source; the index is a cache

`sweep.md` carries a table of every in-scope file and its status. **That table
is an index and can be rebuilt** — the truth is in the slices, each of which
says which files it covered.

This matters the first time the table and the notes disagree, which they will.
A slice note is written once and never revised; a table cell is edited every
time anything happens. **When they conflict, the notes win**, and the table is
regenerated from them rather than argued with.

*Storing derived status is a thing records must never do, for a reason that
does not reach here: it forces somebody to edit a document they did not write.
A sweep has one writer. The prohibition is about authorship, not about
derivation.*

## Two units, and confusing them is the common failure

**The unit of coverage is the file.** Every file in scope appears in the index,
so *read with nothing found* stays distinguishable from *never looked at*. A
sweep that cannot tell those apart has produced confidence it did not earn.

**The unit of a slice is a cluster** — a module, an execution path, a directory
that means something. You review six files together because they only make
sense together.

Reviewing files in isolation because the index is a list of files is the
mistake this distinction exists to prevent. **A file read without its
collaborators is read as a stranger**: you can see that a function is called
and not whether the caller holds the lock it assumes. The index is a coverage
ledger, not a running order.

**One slice, one note, several files marked off.**

**The bound is comprehension, not a file count.** A slice that covers one file
is right when the file is dense enough to spend an evening on. A slice that
covers thirty short documents is also right, because thirty pages of prose is
an amount of material a reader can genuinely hold at once.

The test is whether you could still say what each file did afterwards. **A
slice that fails that is a skim with a note attached**, at any size — and a
slice of three files can fail it just as easily as one of thirty.

## Slices partition the sweep

**A file belongs to one slice.** All the slices together are the scope, and
each file is read once — which is what makes the coverage arithmetic mean
anything.

**Re-covering is an exception the sweep records, not a mode it runs in.** Code
moves under a sweep that takes weeks, and occasionally a file changes enough to
want reading again. That is a decision somebody makes and the index notes, with
the earlier slice named — never a row that quietly resets.

**The difference is what you can see.** A ledger that churns silently looks the
same at 60% whether nothing drifted or half of it did. One that records
re-coverings shows drift accumulating while there is still time to cut the
scope.

## Two ways a row finishes, and they are not the same claim

| status | means | who may set it |
| --- | --- | --- |
| `reviewed` | read, and the reader is satisfied | **any party**, agent included |
| `approved` | **signed off** | **a human only** |

**Every row also records the actor** — `reviewed` by `agent:opus-5` and
`reviewed` by `human:warden` are different facts, and the status alone cannot
tell them apart.

**Status and actor are not redundant.** The status says how strong the claim
is; the actor says who made it. A person may legitimately mark a row `reviewed`
rather than `approved` — *I have read this, it is fine for now, I am not
signing off* — which is a real state an actor column alone cannot express.

**`approved` is strictly stronger.** A row may go `reviewed` then `approved`,
or straight to `approved` when a person read it themselves. Nothing requires
the first before the second.

**Both are needed because a sweep does not always have a human in it.**
[[who-does-the-reading]] permits two agents, and a status only a person can set
would leave such a sweep unable to finish a single row. **An agent must be able
to say *I read this and it is fine*** — what it must not do is say *and that
settles it*.

**Neither party may withhold a status the other is entitled to set.** An agent
records `approved` when the person gives it, whatever the agent thinks and
however the file got that way — rewritten rather than examined, given without a
full slice, given against the agent's advice. **The bundle exists to protect
the reader's judgement and must never be turned against it.**

**Challenge belongs before the status, never after it.** Ask what they made of
it, name a goal they may have drifted from, say where you read it differently.
Then record what they decide. [[the-pairing-turn]] draws that line.

**The close reports both.** *Fifty-three approved, twelve reviewed and never
signed off* is a true sentence about a sweep that ran out of the person's
attention, and one status cannot say it.

## Rows are independent

**Approving a file makes no claim about anything it links to.** A document
approved today may point at four that are still `pending`, and that is an
ordinary state rather than an inconsistency.

**The alternative is unbounded.** If a row could only be approved once
everything it referenced was, then a project where things move — content split
out, a document broken in two — becomes one where nothing can ever be approved,
because every approval drags in more. **Coverage is per file, and the index is
what holds it together.**

**What a split does owe is a note**: the new rows exist, they are pending, and
the slice that created them says so. That is bookkeeping, not a dependency.

## A slice is not an agent session

**The word is qualified for a reason.** A slice is a unit of *reading* — one
cluster, one note, one coherent piece of reasoning. An agent session is a unit
of *conversation*, and it ends for reasons that have nothing to do with the
review: a context limit, a crash, going to bed.

**They do not line up, in either direction.** One slice may span three agent
sessions when the cluster is hard or the day keeps interrupting it. Three
slices may fit inside one long agent session when the material is light — which
is the ordinary case for prose.

**So never close a slice because a conversation ended, and never hold one open
because a conversation is still going.** It closes when the cluster has been
read, argued about, and routed. That is what the note records, and it is the
only thing that marks files off the index.

*What to write when the conversation itself ends is `session-manager`'s, not
this bundle's. A sweep needs little of it: the index and the notes are
committed, so a half-finished slice costs a paragraph to resume rather than a
handover.*

## Naming

**The sweep directory is a slug for what is being read** — `the-cli-surface`,
`everything`, `docs-and-prose`. No date, and no commit: a sweep spans many of
both, and pinning either in the name would be a claim it cannot keep.

**Slices are numbered and slugged** — `001-entrypoint-and-args.md`. The number
is the identity and the order they happened in; the slug is for finding one
again. Numbering from `001` rather than by date, because *what did we do first*
is the question anybody asks of a sweep and the date does not answer it.

## More than one sweep at a time

**Two sweeps sharing neither owner nor territory are ordinary**, and want no
apology. Somebody reading the prose while somebody else reads the CLI is two
sweeps, correctly — nothing is contended, and merging them would buy a single
index nobody can act on alone.

**What fails is two sweeps competing for one person's attention.** Neither
finishes, because attention is the only scarce resource involved and it does
not divide. That is the mistake the rule is about, and it is a mistake about
the reader rather than about the number.

**Overlap in either dimension collapses them into one.** Same reader, or the
same files, and what you have is one sweep with two indexes disagreeing about
its coverage.

## Archive when closed; delete later and deliberately

A closed sweep moves to `.luma/backlog/sweeps/archived/<slug>/`, keeping the
`slices/` beside it. **What the sweep produced has already left** — a merged
pull request, an idea, a decision, a finding — so what remains is working
notes, and their value decays.

Deleting them is fine eventually and is nobody's emergency. Archiving needs no
permission; deleting somebody else's sweep needs theirs.
