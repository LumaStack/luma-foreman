# Where the sweep stands

Copy the block below. **Copy the block, not this file** — it is a message shape,
like [the presentation template](file-presentation.md).

**One output, two moments.** It is the same message either way; only what
triggers it differs.

| moment | trigger |
| --- | --- |
| **a slice ends** | **automatic and unprompted**, every time |
| **a slice starts** | **only after a detour** — and then only when the reader asks to get back on track, or you recommend it |

**Back-to-back slices get it once, at the close.** Saying it again immediately
is the same message twice with nothing between them to have changed it.

**After a detour it is owed**, because the reader has lost the thread and will
not think to ask for it back. See step 2 and step 11 of the `review-next`
workflow.

## The block

```markdown
`path/to/last-file.ext` — <how it closed, and by whom>

---

## Slice NNN closed          <or: Starting slice NNN>

### What just happened

<Three or four lines. At a close: what the slice did — not the slice note,
which is the record, but the reader remembering it before they choose what is
next. After a detour: what the detour was, in the same three or four lines.>

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

### What's next

- **`entry and shared` — 7 files.** Code, so the agent reads and you take a
  summary. Roughly a slice's worth.
- **Revisit the read-by arrangement first.** One turn, and it changes how every
  remaining slice runs.
- **Close the sweep.** Everything left is code and skipped rows; the close
  harvests the journal and archives the rest.

<Each option gets its cost in a clause. A reader choosing between three
unpriced options is guessing.>

### Should you /clear          <whatever this harness calls it>

<Weigh it. Do not assert it — the answer changes every time and a fixed one
reads as boilerplate the moment it is wrong.>

**Yes, and it is cheap.** The next slice is a different subsystem, so nothing
loaded here carries over — and what is loaded is eight repositories the next
cluster will never touch.

**→ Type `/clear`, then paste this:**   <the same command, named again>

```
Resume the review sweep in .luma/backlog/sweeps/the-whole-of-foreman/.
Read charter.md and coverage.md, then invoke review-next.
Ordering is led — ask me which cluster is next.
```
```

## Two sections, because they are two questions

**`What's next` is a report; `Should you /clear` asks for an answer.** Running
them together buries the only part with an action in it, which is where a reader
stops reading.

**In that order, because clearing depends on what is next.** Same cluster means
carry on; a different subsystem means clear. Asking first asks before the input
exists.

**Fill in the command this harness actually uses**, in the heading and again
above the fence. `/clear` in Claude Code; whatever the equivalent is wherever
this runs; and where a harness has none, drop to *start a fresh session* and
keep the paste block, which is the part that carries the value.

**The heading carries the literal command on purpose** — *should you clear* is a
question about housekeeping, and *should you `/clear`* is a thing to type.

## The paste block goes under a label, not after a paragraph

**The instruction sits on its own line, immediately above the fence**, with
nothing between them. A fence at the tail of a long message with its
instruction buried mid-paragraph is a fence nobody notices.

**A fenced block, never a blockquote.** A terminal renders a blockquote with a
prefix character on every line, and the prefix comes along when the reader
selects it. The fence is the copy-safe shape and terminals already render it as
one.

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

## Weigh it, do not assert it

**The answer is not always yes**, and a section that always says yes is one a
reader stops reading.

**Both choices are taxed and the recommendation is the smaller tax** — the same
rule `what-a-slice-produces` gives for fixing now versus routing, and it is not
restated here. **What is specific to clearing is which taxes:** clearing costs a
re-read of whatever the next slice needs and this session already holds;
carrying on costs the irrelevant context, paid again on every remaining turn.

**So it turns on one question — how much of what is loaded does the next slice
actually want?**

- **A different subsystem, or anything after a detour** — almost none of it.
  **Clearing is cheap, and it is the usual answer.**
- **The same cluster, continued** — most of it. **Clearing buys a re-read of
  files about to be discussed. Say so and carry on.**
- **Something exists only in this session** — **a defect, not a cost.** Name it,
  write it to the journal, then clear. Never a reason to hold context.

**Say which of the three it is and why, in a sentence or two** — and give the
options above regardless, because *carry on* is still a choice between them.
