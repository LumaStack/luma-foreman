---
type: workflow
title: Review the next unit
description: One slice — reconcile the index, orient without judging, let the reader read first, then act on what they say. Use to continue an open sweep, including after a break.
---

# Review the next unit

**This is the whole loop.** Resuming a sweep is running it again; there is no
separate resume procedure, because step 1 is the reconciliation a resume would
have done.

## 1. Reconcile `coverage.md` against the tree

The code moved since the index was built — by your own fixes, if nothing else.

```sh
git diff --name-status <indexed_at>..HEAD
```

- **Added** files in scope get rows, marked pending, **placed by the sweep's
  clustering strategy**. Where none of its clusters fits, add one to `charter.md`
  rather than inventing a name here.
- **Deleted** files are struck through rather than removed, so the index still
  explains itself.
- **Renamed** files keep their status. A move is not a reason to re-read
  something.
- **Substantially rewritten** files are the one case needing a decision, and it
  is not yours to make alone — see below.

Update `indexed_at` in `coverage.md` to the current commit.

**If the slices and `coverage.md` disagree, the slices win** — they are the
source and the index is a cache. Rebuild the row rather than trusting it.

### Re-covering is asked for, never applied

**Slices partition the sweep**, so in the ordinary case a file is read once.
**Never silently return a row to `pending`.**

Say what changed and ask — *`src/gate.py` was covered in slice 004 and has been
substantially rewritten since; do you want it re-covered, or does the earlier
read still stand?* Both answers are common, and the reader who read it is the
one who can tell.

**When a file is re-covered the row records it** — the earlier slice, the new
one, and why. That is what makes drift visible as something accumulating rather
than as a ledger quietly resetting itself.

**If rows keep going back to pending, the sweep is losing to the codebase.**
Say so rather than absorbing it: either the scope is too large for the rate of
change, or too much is being fixed mid-sweep.

## 2. Pick the next cluster

Follow the recorded order. **If the recorded order is not working, change it
deliberately** — a dated line in `charter.md` saying what changed and why. Not
one convenient slice at a time.

**Three to eight files.** Fewer means a file read without its collaborators;
more means a skim.

## 3. Orient — one file at a time

> **Gate. Do not present a file until the previous one is closed.**
>
> A file is closed when the reader has given a sign-off, said the reading is
> done, or skipped it with a reason — **and you have written that into
> `coverage.md`.** Nothing else closes a file.
>
> **If the previous file is not closed, go to step 7 and close it.** Presenting
> the next one is the violation; noticing here is the last chance to catch it.
>
> *First file of the slice: nothing is open, proceed.*

**[[presenting-a-file]] gives the shape**: the data block, a summary of what
the file is, what you make of it, then open it for them. One file, not the
cluster.

**Whether your read comes before or after theirs is the sweep's declared
arrangement**, not yours to pick per file. Under the turn order it comes after
— facts only until they have spoken. Where the reader has declared otherwise
for this area, it comes with the file.

### Under the turn order: facts only, no verdicts

**Read the cluster, then say what it is.** What these files do, how they
connect, what calls in and what they call out, what changed here recently and
how often.

**No judgement**, and this is the load-bearing constraint of the whole practice
— see [[the-pairing-turn]]. *This is called from three places, one holding no
lock* is orientation. *This is over-engineered* is a verdict, and saying it now
means the reader spends the slice reviewing your opinion instead of their code.

**A live hazard is the exception** and is said immediately.

## 4. Hand over, and let them speak first

Say what you would like from them — *read these four, tell me what you make of
the retry logic* — and then stop.

**Wait.** If they ask you to go first, decline once with the reason and offer
the read afterwards; if they ask again, do it and note it in the slice.

## 5. Respond

Now the judgement. Where you agree, where you do not and why, and what they did
not raise.

**Disagree where you disagree**, including when they have just called something
fine. An agent that only ratifies has added nothing to a slice they could have
run alone.

**Say what this cluster makes you doubt about an earlier one.** A sweep learns
as it goes and the ninth slice routinely falsifies the third; that is not a
failure, it is the compounding the order was chosen for.

## 6. Record, and route everything out

**Record before fixing, and record whether or not anything gets fixed.** What
is wrong, where, why it matters — and where you can see the answer, the fix as
a *proposal*. See [[what-a-slice-produces]].

**Write the reasoning, not just the diff.** A proposal is stale from the moment
it is written; the reasoning survives being stale and the diff does not.

**A fix may land now only if a person is in the sweep and says so — and you
recommend before they choose.** Now if it needs only context already loaded and
lands in about a turn; routed if it needs more than two turns or files nobody
has opened, since that load happens either way. **One sentence saying which and
why**, then it is theirs. See [[what-a-slice-produces]]. With nobody human
here, nothing lands during the slice — a third party works from the record
afterwards, and the gap is where the findings get checked as a set.

**Propose before applying, always.** A change the reader has not seen turns
their review into a diff review of yours. And a yes to one fix is not a yes to
the same fix in four other places.

Nothing worth keeping stays in the slice note.

## 7. Close the file

**Steps 3 to 7 are one file, and one file is open at a time.** Work through
this in order. Do not start step 3 again until this file is closed.

### 7a. If anything was edited, show what and how to check it

Skip only if nothing changed at all.

**Say what changed** — a table, a list, or a sentence, whichever is fastest to
read. The reader is about to sign something; they should not have to
reconstruct what.

**Give a diff command, and run it yourself before offering it.** It must work
pasted straight in, unmodified, from the directory the reader is standing in.
**A command they have to repair is worse than none** — they find out it was
wrong only after deciding to trust it.

- Wrong repository, wrong branch, a path that does not exist from here: run it
  and you will know.
- Reflowed prose: use `--word-diff`. A line diff of rewrapped markdown shows
  every paragraph that moved and buries the words that changed.

**Then stop and let them respond to it.** A file edited during its own review
has not been reviewed in the state it is now in.

### 7b. Ask for the confirmation this sweep's `approval` calls for

**One sentence.** They have been reading; do not hand them a menu.

| `approval` | ask for |
| --- | --- |
| `required` · `recommended` | **sign-off.** Say what withholding it means: `reviewed_by` filled, `approved_by` empty, which is an ordinary close and not a failure |
| `optional` · `prohibited` | **that the reading is done** — reviewed, or skipped with a reason |

### 7c. Wait. These are not confirmations

**An instruction to act is not a verdict on the row.** Acting on one and
inferring the row is how a file gets marked by the agent while the reader
believes they never said so.

| they say | it means | the row is |
| --- | --- | --- |
| *proceed*, *next*, *go on*, *ok* | carry on working | **still open** |
| *drop it*, *fix that*, *change it* | do the work | **still open** |
| *merge it*, *commit that*, *ship it* | land the change | **still open** |
| *yes*, *agreed*, *good point* | they agree with a claim | **still open** |
| silence, or a move to another subject | nothing | **still open** |

**Three things close a row, and nothing else does:**

1. **A sign-off** — approved, signed off, looks good
2. **The reading is done** — reviewed, covered, I have read it, move on from it
3. **A skip, with a reason**

**Ask even when the answer looks obvious.** It costs one line, and a reader who
has just told you to delete a file may still want the row to say `findings`
rather than nothing. **Only they know.**

**Where the wording is ambiguous, it is not a confirmation.** Ask which of the
three it was. Guessing right nine times does not make the tenth safe.

### 7d. Say what closed it, then write it down

**Before opening the next file, state in one line who closed this one and with
what.** *"`src/args.py` — reviewed by `human:fsmith`, `findings`, not signed
off."*

**This is the check that makes the rest hard to skip.** A row closed by
inference produces a sentence with nobody in it, and that sentence is
unwritable before it is noticed. Then update `coverage.md` and return to step
3.

### 7e. Returning to a file re-opens it

A reader may come back to anything at any time, and a later file routinely
changes what an earlier one meant — that compounding is why the order was
chosen.

**A re-opened row is open. It needs 7a to 7d again.** It is not still closed
from before: whatever brought them back may change what they want it to say.

### If you have already broken this

**Say so, name the row, and ask for the confirmation you skipped.** Do not
quietly correct `coverage.md` — the reader is the only one who can say what the
row should have held, and a silently fixed row is the same defect twice.

## 8. Write the slice and update `coverage.md`

[The slice template](../templates/slice.md). It is a working note, not a report
— what was covered, what was concluded, what left the sweep and where it went.

**Correcting the goal is a legitimate outcome of a slice, not a failure of
one.** A goal is written before anything has been read, so the first slices are
the first evidence it was aimed correctly. Where it was not, change it in
`charter.md` with what the slice found and why — and say how many of this
slice's files would have been out of scope under the old one, because that is
the measure of how wrong it was.

**Say whether the slice served the goal.** One clause. It is how drift becomes
visible early: three slices running that turn up nothing related to the goal
mean either the goal was wrong or the sweep has wandered, and both are worth
raising rather than absorbing.

**Re-take the rate while you are here.** A range across every slice so far,
with how many there have been — see [[start-a-sweep]]. It costs a count of rows
and it is the only thing that tells the reader whether the sweep is going to
finish.

Mark every file in the cluster, including the ones where nothing was found —
**read with nothing found is a result**, and an index that records only
problems has unexplained gaps in place of evidence.

**Fill the three columns from what they actually said.** `reviewed_by` — who
read it, an agent included. `approved_by` — who signed off, **a person only**.
`outcome` — `clean` or `findings`, what the reading concluded.

**Record it without argument.** Your own view lives in `reviewed_by` and
`outcome`, where it has no veto over anybody.

## 9. Batch what the practice taught; do not stop for it

**A slice that keeps pausing to fix the practice is not running.** Where the
sweep exposes something wrong with sweeping — an order that fails, a
presentation that does not work, a rule that fires wrongly — **change the
behaviour immediately and batch the written fix for the end of the slice.**

**In the first sweep ever conducted, the first three files were spent on the
practice rather than on the files.** That is what a `draft` practice costs
once, and the cost is only acceptable once — a second slice that produces as
many changes to the bundle as findings about the code is a sweep that has
stopped sweeping.

## 10. Commit the slice

One commit for the slice note and the index. That is the sweep's record and it
lands whether or not anything was fixed.

**The fixes are on their own schedule** — batched by kind rather than by where
they were found, and landed however this project lands changes. See
[[what-a-slice-produces]].

**The one thing to watch is staleness.** If a large pile of unlanded fixes is
building up, land it before the next slice; otherwise you are reading your own
work in progress.

**If this slice removed a document, that is the exception.** The removal and
every destination its content went to land in **one commit**, and the slice
note carries a ledger giving every range of the removed file a verdict — moved,
rewritten, dropped as duplicate, or **dropped as wrong with what it was checked
against**. A deletion is the one thing a later reader cannot go and verify for
themselves. [[what-a-slice-produces]] has the rule and the template has the
table.

## 11. Close out the slice

**Four parts, in order, every time** — what this slice did, where the sweep
stands, what is worth their attention, and how to proceed. **[The slice-close
template](../templates/slice-close.md) carries the shape**; what follows is why
the last two are there at all.

### The row close and the slice close are two events

**Step 7d's line comes first, alone, with a rule under it** — the row closed,
and by whom. Then the slice close.

**They are not one announcement.** A file ended; the slice ended *because* it
was the last one. Run together — *Slice 004 closed — `gate.md`, skipped* — and a
reader cannot tell whether the slice was skipped, the file was, or both.

### Everything that wants the reader gets a heading

**A paragraph with no heading reads as commentary and gets skimmed past.** That
is the opposite of what it is for — it holds the consequences, the ones a reader
may want to act on and nobody is blocked on.

**Put the decisions under it, including the ones you deliberately did not
take.** *Eleven rows sit under the reason you just gave and are still pending;
not marked, your call* belongs somewhere a reader stops.

### How to proceed is priced options, not prose

**Bullets, each with what it costs in a clause** — *seven files, roughly a
slice's worth*; *one turn, and it changes how every remaining slice runs*.
**A reader choosing between three unpriced options is guessing**, and the agent
is the one who can price them.

**Then the clear decision in a sentence, and the paste block.**

### Why a slice boundary is where a session gets cleared

**It is the cheapest moment there will ever be to drop the context**, and for a
structural reason: **by the time a slice closes, everything worth keeping has
already been written to disk.** The slice note, the index, the journal, the
routed findings, the commit. That is not luck — it is what steps 6 to 10 are
for.

**So it is a check rather than a judgement:** *is anything left that exists
only in this session?*

- **No.** Clearing costs nothing — **recommend it.** What the context mostly
  holds is files still sitting on disk, and re-reading the two that matter next
  is cheaper than carrying all of them through every remaining turn.
- **Yes.** **That is a defect, not a reason to keep the context.** Write it down
  and then clear. An observation surviving only in a session is one restart from
  gone, and [[how-a-sweep-is-stored]] gives the journal for exactly this.

**Recommend; do not decide.** The same shape as fix-now-or-route — you can see
what the context costs and you cannot see whether they are mid-thought about
something they have not said yet.

**Never clear inside a slice.** [[the-pairing-turn]]'s order depends on both
parties holding the same file. Halfway through, clearing makes the agent
re-derive a read the reader has already answered, and their answers no longer
attach to anything.

**The one case for carrying on: the next slice is the same cluster.**
Orientation carries over, and clearing buys a re-read of files about to be
discussed anyway. **Say so rather than recommending a clear out of habit.**

*In Claude Code this is `/clear`; the reasoning is the same wherever the
session lives.*

### The paste block is a pointer, never a handoff note

**Give the reader something to paste into the next session**, in a fenced block,
three or four lines. They are going to select it with a mouse.

**It carries what a fresh agent cannot read for itself and nothing else** — the
sweep's path, which files to read, which workflow to invoke, where to resume.

**If it needs to carry findings or context, something was not written down.**
Same test as the clear decision above it, failing the same way: **an observation
that survives only in a paste was never routed.**
