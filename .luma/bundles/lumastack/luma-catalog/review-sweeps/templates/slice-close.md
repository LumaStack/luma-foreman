# Closing a slice

Copy the block below when a slice ends. **Copy the block, not this file** — it
is a message shape, like [the presentation template](file-presentation.md).

**Four parts, in order:** what the slice did, where the sweep stands, what is
worth the reader's attention, and how to proceed. The reasoning — why a slice
boundary is the cheapest moment to clear, and when not to — is in step 11 of the
`review-next` workflow.

## The block

```markdown
`path/to/last-file.ext` — <how it closed, and by whom>

---

## Slice NNN closed

### What this slice did

<Three or four lines. Not the slice note, which is the record — this is the
reader remembering what just happened before they choose what is next.>

- `args.py` closed — reviewed by human:fsmith, findings, not signed off
- `flags.py` closed — approved
- two findings routed to the backlog, one fixed in place
- the practice gained a rule about removals

### Where the sweep stands

| | |
| --- | --- |
| closed | `cli.py`, `args.py`, `flags.py`, `parse.py` |
| skipped | `generated/` — reader's exclusion; `vendor/` — not ours |
| open | `docs/gate.md` |
| untouched | the transport layer, the test suites, the migration scripts |

<Names in the first three rows. Groups in the last — a reader wants to know
which files are done and roughly what is left, and ninety filenames under
`untouched` is the index printed twice.>

<Then one line saying what the table makes obvious: "two clusters closed and
none of `src/` reached".>

### For your consideration

<Anything the reader may want to act on that is not blocking. Observations,
consequences, and decisions that are theirs. **Give it a heading** — without
one it reads as commentary and gets skimmed past, which is the opposite of
what it is for.>

- **Eleven rows sit under the reason you just gave** and are still pending. If
  the subsystem is out of scope, that reason covers them too — and leaving them
  pending claims the sweep intends to reach them. **Not marked; your call.**
- **The read-by arrangement was written when code was half the sweep.** It is
  now nearly all of it, so *the reader's view is downstream of the agent's* is
  a larger concession than when it was agreed.

### How to proceed

- **Next slice — `entry and shared`, 7 files.** Code, so the agent reads and
  you take a summary. Roughly a slice's worth.
- **Revisit the read-by arrangement first.** One turn, and it changes how every
  remaining slice runs.
- **Close the sweep.** Everything left is code and skipped rows; the close
  harvests the journal and archives the rest.

<Each option gets its cost in a clause. A reader choosing between three
unpriced options is guessing.>

**Clearing is free here** — nothing exists only in this session. Type `/clear`,
then paste:

```
Resume the review sweep in .luma/backlog/sweeps/the-whole-of-foreman/.
Read charter.md and coverage.md, then invoke review-next.
Next cluster: entry and shared.
```
```

## The row close and the slice close are two events

**The first line is step 7d's**, not part of this block: the row closed, and by
whom. **The slice closing is a consequence of it** — the last file in the
cluster ran out.

**Keep them apart, with a rule between.** Run together in one heading —
*Slice 004 closed — `gate.md`, skipped* — and a reader cannot tell whether the
slice was skipped, the file was, or both. **One file ended; the slice ended
because of it.**

## The paste block is a pointer, never a handoff note

**It carries what a fresh agent cannot read for itself and nothing else** — the
sweep's path, which files to read, which workflow to invoke, and where to
resume.

**If it needs to carry findings or context, something was not written down.**
That is the same test as the clear decision one line above it, and it fails the
same way: an observation that only survives in a paste is an observation that
was never routed.

**Three or four lines, in a fenced block.** The reader is going to select it
with a mouse.

## The three shapes the clear paragraph takes

**Clearing is free.** Nothing exists only in the session and the next slice is
elsewhere. The usual case, and the reason a slice boundary exists.

**Write something down first.** Something is still only in the session — that
is a defect rather than a reason to hold the context. Name it, write it to the
journal, then clear.

**Carry on instead.** The next slice is the same cluster, so orientation
carries over and clearing buys a re-read of files about to be discussed. **Say
which of the three it is, and why, in a line** — then give the options above
regardless, because *carry on* is still a choice between them.
