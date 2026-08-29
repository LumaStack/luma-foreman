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

**A fix may land now only if a person is in the sweep and says so.** With
nobody human here, nothing lands during the slice — a third party works from
the record afterwards, and the gap is where the findings get checked as a set.

**Propose before applying, always.** A change the reader has not seen turns
their review into a diff review of yours. And a yes to one fix is not a yes to
the same fix in four other places.

Nothing worth keeping stays in the slice note.

## 7. Write the slice and update `coverage.md`

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

**`reviewed`** where the reader was satisfied; an agent may set this for
itself. **`approved`** where a person signed off, and **only a person may give
it**. Record what they say without argument — your own view lives in
`reviewed`.

## 8. Batch what the practice taught; do not stop for it

**A slice that keeps pausing to fix the practice is not running.** Where the
sweep exposes something wrong with sweeping — an order that fails, a
presentation that does not work, a rule that fires wrongly — **change the
behaviour immediately and batch the written fix for the end of the slice.**

**In the first sweep ever conducted, the first three files were spent on the
practice rather than on the files.** That is what a `draft` practice costs
once, and the cost is only acceptable once — a second slice that produces as
many changes to the bundle as findings about the code is a sweep that has
stopped sweeping.

## 9. Commit the slice

One commit for the slice note and the index. That is the sweep's record and it
lands whether or not anything was fixed.

**The fixes are on their own schedule** — batched by kind rather than by where
they were found, and landed however this project lands changes. See
[[what-a-slice-produces]].

**The one thing to watch is staleness.** If a large pile of unlanded fixes is
building up, land it before the next slice; otherwise you are reading your own
work in progress.
