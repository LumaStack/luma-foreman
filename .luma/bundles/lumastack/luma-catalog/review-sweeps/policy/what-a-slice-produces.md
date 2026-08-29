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

**Only where a person is in the sweep and says so.** Then it is worth doing
immediately: the context is hot, they understood it, and deferring means
somebody re-derives it later at full price.

**The record is written either way.** The finding exists whether or not the fix
does, because a fix that lands leaves a diff and a diff does not say what was
wrong or why anybody looked.

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

**The one thing that legitimately waits is a conclusion the sweep has not
reached yet** — a suspicion about the shape of the whole system needing three
more slices before it can be stated. Write it as a suspicion, say what would
confirm it, and let a later slice settle it.

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

*How changes get integrated is not this bundle's to say — `git-workflow`, and
whatever this project already does, own that.*
