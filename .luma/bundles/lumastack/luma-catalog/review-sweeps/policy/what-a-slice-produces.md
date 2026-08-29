---
type: policy
title: What a slice produces
description: A slice produces a record and never a rewrite — what gets recorded, why a proposed fix is a suggestion rather than a directive, and when a fix may land during the sweep at all.
matches:
  - topic: acting on what a review turned up
---

# What a slice produces

**A slice produces a record, not a change.** What is wrong, where, why it
matters — and optionally what you would do about it.

**The record is the durable thing and the fix is not.** A finding outlives
every attempt at it: the fix can be wrong, superseded, or better made by
somebody with context the reader never had, and none of that damages the
finding. A sweep that rewrites as it reads has spent its output on the
replaceable half.

There is a second reason, smaller and felt sooner: **fixing pulls you out of
reading.** Twenty minutes into a patch you are no longer holding the cluster,
and the slice is what you came for.

## Where each reaction goes

| the reaction | what you record | owned by |
| --- | --- | --- |
| **this is wrong, and I can see the fix** | the finding, **and the fix as a proposal** | the sweep's routing, below |
| **this is wrong and I do not understand it yet** | the finding, without one | `backlog-ideas`, or `audit-records` |
| **this is fine, but I had to work out why** | a decision record | `decision-records` |
| **this is fine** | the row is marked `reviewed`, or `approved` if a person signed off | the sweep index |

*Those bundles are named rather than linked — they are separate and may not be
adopted here. Where one is absent the destination is whatever this project
already uses, and the routing rule is unchanged.*

**Row four is the most common and the easiest to skip.** *Reviewed and clean is
a result*: it is what lets somebody later tell *examined and fine* from *never
looked at*. A sweep that records only problems has an index of complaints with
unexplained gaps between them. Mark it off — it costs a cell.

## A proposed fix is a suggestion, not a directive

**This is the pairing turn again, pointed one seat further down.** A proposal
written as an instruction short-circuits the judgement of whoever applies it,
which is the same failure as opening a slice with verdicts — and it is easier
to commit here, because a diff looks like a decision that has already been
made.

**The reader saw this file for twenty minutes.** Whoever fixes it may own the
subsystem, may know why the pattern is deliberate, may have work in flight that
the proposal collides with, or may simply have a better fix. **None of that is
visible from inside the slice.**

So write *here is what I would do, and why* — never *do this*. And **record the
reasoning rather than only the diff**: somebody who rejects your fix may still
accept your finding, and that is a good outcome the proposal has to survive.

**Not fixing it is a legitimate outcome** and stays available. A finding whose
answer is *we know, and we are living with it* has done its job.

### And it is stale from the moment it is written

**A proposal is true of one commit.** Between the slice and the fix the file
moves, adjacent fixes land, and other findings change what this one means. By
the time anybody acts on it, the diff may not apply, may apply and be wrong, or
may be fixing something that is already gone.

**So whoever fixes re-derives rather than applies.** Check the finding still
holds before touching anything — and where it does not, that is a result worth
recording, not a proposal to force through.

**This is the real reason the reasoning beats the diff.** A stale diff is worth
nothing. Stale reasoning is still evaluable: somebody reads *why* and decides
in a minute whether it still applies.

**The gap is longest exactly where the proposal carries most authority** — a
sweep with no person in it, whose findings are fixed by a third party days
later, with nobody in between who ever saw the file. Treating those proposals
as law is how a sweep ships confident changes that no longer match the code.

## When a fix may land during the sweep

**Only where a person is in the sweep and says so.** It is theirs to decide,
and **the recommendation is yours to make** — they cannot see what the fix
would cost and you can.

### Both choices are taxed, and you are choosing which tax to pay

**Doing it now taxes the session.** Context that does not belong to this file
enters it and stays — a renderer's shape is now in the room while the reader is
trying to hold a document. **A slice that keeps paying this tax stops being
about anything.**

**Doing it later taxes the finding**, in two ways that are both silent:

- **The code moves.** By the time somebody returns, the thing observed may not
  exist in that shape, and the note describes a version nobody can find. **A
  finding is a claim about a moment.**
- **The context is gone.** Whoever picks it up has a different session, a
  different read of the file, and only what was written down. **Framing rots
  faster than facts** — *what was wrong* survives in a note; *why it mattered
  here* usually does not, and a successor can re-derive the first and not the
  second.

### Which tax is smaller

| the fix needs | recommend | because |
| --- | --- | --- |
| **only context already loaded**, and lands in about one turn | **now** | the session tax is one turn; deferring pays a full reload plus the risk of rot |
| **more than two turns**, or files nobody has opened | **route it** | that load happens either way, so paying it here buys nothing and pollutes the slice for free |

**Two turns is where the saving generally disappears**, and it is a heuristic
rather than a line. One turn is the fix; two is the fix and the check that it
worked. Past that you are usually loading new context — and new context loaded
mid-slice is the *while I'm here* failure below wearing an efficiency argument.

***Generally*, because the count is a proxy.** What actually decides it is
whether the fix needs context nobody has loaded, and turns are only the
cheapest way to estimate that in advance. **A three-turn fix inside a file
already open is still cheap**; a one-turn fix in a subsystem nobody has read is
not. Where the proxy and the thing it stands for disagree, **the context
wins.**

**Say which it is and why, in one sentence, then let them choose.**

### Two questions, and only the first one is yours

1. **Which tax is smaller here?** Yours to compute, and the recommendation.
2. **Does the reader care enough to override it?** Theirs, and not yours to
   argue.

**Token economy** is the one you can compute. You know what the fix would load
and what deferring would reload, and that is the recommendation.

**Cohesion is the other, and it is theirs.** A slice holds together because it
is about one thing, and so does a reader's attention. Somebody deep in a
document may not want to be pulled sideways into a renderer — or may badly want
to be, because the annoyance is what they will otherwise remember instead of
the file. **Both are legitimate, they change by the hour, and nothing in the
sweep can see which one is true today.**

**The strongest reason to overrule the economy is the reader's own clarity.**
*I understand this now and I will not understand it as well in a fortnight* is
a judgement only they can make, and it is a direct read on the rot tax above.
**When they say it, pay the session tax and fix it** — they are telling you the
other tax is larger, and they are the only one who can know.

**And that is a rational trade, not an indulgence.** Tokens are renewable: a
session can be re-run, a file re-read, a context rebuilt, and the price is only
time and money. **A reader's understanding right now is not.** It exists in one
head at one moment, and if it does not get written down it is not recoverable
at any price — a successor can re-derive what was wrong and cannot re-derive
why it mattered.

**So spending tokens to keep knowledge that would otherwise be forgotten is the
economy working, not failing.** The recommendation prices the context. **It
cannot price the thing being bought**, and an agent that argues the number is
arguing the only half it can see.

So they will override sometimes and they should. **A reader choosing to
context-switch against the economy is not making a mistake**, and one refusing
to switch when the fix was free is not either. Make the call on the numbers,
hand it over, and do not argue the preference.

**Never just ask.** *Fix it now, or route it?* with no recommendation hands the
reader an accounting problem they have no numbers for, and the usual answer to
a question like that is whichever takes less thought.

### One case overrides the economy

**A fix that edits the file under review.** It has to be shown and re-confirmed
— [[review-next]] step 7a — and until it is, **the reader is holding a verdict
on a state of the file they have not read.** Route it unless they ask
otherwise, however cheap it looks.

**The record is written either way, and it is not part of the choice.** The
finding exists whether or not the fix does, because a fix that lands leaves a
diff and a diff does not say what was wrong or why anybody looked. **Routing
means deferring the fix, never deferring the record.**

**Propose before applying, every time.** A change nobody has seen turns their
review into a diff review of yours. And **a yes to one fix is not a yes to the
pattern** — if the same thing appears four more times, that is one proposal
covering five sites, not four unremarked edits.

**Watch for `while I'm here`.** It is how a two-file slice becomes a
nineteen-file diff nobody can review. The test is whether the change is one you
understood *in this slice* — not whether it is small, and not whether it is
obviously correct.

**Anything larger is recorded, not attempted.** *This whole layer wants
restructuring* is a real observation and it is not slice work; taking it on
stalls the sweep on file four for a week.

## When no person is in the sweep, nothing lands during it

**The sweep records. A third party fixes afterwards, from the record.**

**Separate from both sweep parties**, on the same reasoning that separates the
reader from whoever orients — see [[who-does-the-reading]]. A party that argued
a finding into existence will implement it rather than re-examine it.

**The gap between recording and fixing is the point, not the overhead.** It is
where somebody can look at the findings as a set — before any code has moved —
and drop the ones that are wrong, merge the four that are the same finding, and
notice the one that changes what the others mean. **None of that is possible
once the fixes are already in.**

*How the fixing party works is not this bundle's to say.* What belongs here is
the separation, and the record being good enough to act on without the sweep
being in the room.

## What the slice half-finished

**A slice that creates work and does not record it is worse than one that
changed nothing**, because the loose end is invisible and the index looks
complete.

Two shapes, and both are common:

- **Content that moved.** A document split into four; a section lifted into its
  own file. The new files are new rows, `pending`, and **the slice says which
  approval created them** so the next slice knows where to look first.
- **A change that was started and not finished.** A rename applied in three of
  five places, a fix that needs one more decision. It goes wherever the project
  tracks work, now, with what remains.

**Neither blocks the row that produced it.** Approving a file makes no claim
about what it spawned — see [[how-a-sweep-is-stored]]. Recording is
bookkeeping, not a dependency, and conflating them is how a project that moves
things becomes one where nothing can be approved.

## A finding may be about more than the file

**The file is where you found it, not necessarily what it is about.** A claim
repeated in six places is a finding about all six; one that contradicts another
repository is a finding about the boundary between them.

**Route it at its real scope, and say where it was found.** *Filed from slice
004, seen in `docs/commands.md`, asserted in five documents across another
bundle* is actionable. *`docs/commands.md:41` is wrong* is a fix that leaves
five copies standing.

**Do not chase it inside the slice.** Following a finding out of the sweep's
scope is how a slice becomes an afternoon, and the sweep is the thing with
momentum worth protecting. Record where it reaches and move on.

## Nothing worth keeping stays in the sweep

**Everything routes out.** A sweep is backlog: it gets archived and eventually
deleted, and anything parked in a slice note as *we should really…* dies with
it. A slice that ends with six observations in a note has produced nothing.

**Route during the slice.** A pile of *to be filed later* is filed by nobody —
the reasoning that made each one worth capturing is gone within a day, and what
gets written a fortnight later is a shorter, worse version of it.

**Where a sweep keeps a `journal.md`, a not-yet-conclusion goes there** —
dated, with the slice it came from. **It is not a queue**: anything actionable
still goes to its real destination at the slice that produced it, and an entry
that sits there while being actionable was routed wrongly.

**The one thing that legitimately waits is a conclusion the sweep has not
reached yet** — a suspicion about the shape of the whole system needing three
more slices before it can be stated. Write it as a suspicion, say what would
confirm it, and let a later slice settle it.

## When a slice removes a document, it owes a ledger

**A slice that deletes a file has produced something no other slice does: an
absence.** Everything else a slice produces can be checked against the file it
came from. **A removed file cannot be re-read**, so what the slice concluded
about it is the only remaining record of what it held.

**Two obligations follow, and neither is optional.**

### The removal and every destination land in one commit

**So the diff is the whole story** — every deletion and every insertion side by
side, in one `git show`. Split across commits, a reader watches content vanish
in one place and appear in another with nothing tying them together, and has to
reconstruct the mapping by hand from two diffs that do not mention each other.

**It also fails safely.** A half-landed scatter leaves live references pointing
at a file that is already gone. One commit either lands or does not.

**This does not make a slice a pull request boundary** — the section below
still holds. **The unit here is one removal**, which is usually smaller than a
slice and occasionally spans two.

### A verdict for every part of what was removed

A table in the slice record: each range of the removed document, and what
became of it.

| lines | what it held | verdict | where it went |
| --- | --- | --- | --- |

**The verdict column is the one that matters**, and it has to separate four
outcomes:

| verdict | means |
| --- | --- |
| **moved** | carried to a destination, substantially as it was |
| **rewritten** | the substance survived; the words did not |
| **dropped as duplicate** | already recorded elsewhere — and *where* is the destination |
| **dropped as wrong** | false, stale or unsourced. **No destination, deliberately** |

**A diff cannot make that last distinction.** Content discarded on purpose and
content lost by accident look identical in a deletion — both are red lines with
nothing corresponding anywhere. **The ledger is the only thing that separates
them**, and it is what lets somebody trust a removal they did not perform.

**Name what each *dropped as wrong* row was checked against.** *Dropped as
wrong* on its own asks the reader to take your word for it. *Contradicted by
`apply.py:19`* lets them go and look. This is `cross-check` doing the work it
already does, written down where it can be audited.

**Write it while removing, not afterwards.** The reason for dropping a claim is
available for as long as you are holding the claim and not much longer, and a
ledger reconstructed a week later is a guess wearing a table's clothes.

**It is proportional to what was removed, not to the sweep.** Deleting a stub
nobody cited needs a line. Dismantling a document eleven files point at needs
every range accounted for, because eleven readers will arrive expecting it.

## Landing whatever does get fixed

**A slice is not a pull request boundary.** Most slices produce no change at
all, so one pull request per slice means a stream of empty and one-line pull
requests with the ones that matter lost among them.

**The two sizes are governed by different things.** A slice is sized by what
you can comprehend together; a pull request by what reviews well. Forcing them
to be the same object guarantees one of them is wrong.

**Batch by kind, across slices.** *Here are the six places that swallow the
exception* is one idea, reviewable as one idea — better than six pull requests
of one line each, where nobody ever sees the pattern. It is also how the sweep
learns: slice 009 routinely reveals that 003 and 005 had the same problem.

**The one constraint is staleness, not size.** Do not carry a large pile of
unlanded fixes into the next slice — reading with a big uncommitted diff
underneath you means reviewing your own work in progress, and the sweep starts
chasing itself.

**The exception is a removal**, which lands whole or not at all — see above.
That is a constraint on one commit's contents rather than on how commits are
grouped, so it sits alongside batching rather than against it.

*How changes get integrated is not this bundle's to say — `git-workflow`, and
whatever this project already does, own that.*
