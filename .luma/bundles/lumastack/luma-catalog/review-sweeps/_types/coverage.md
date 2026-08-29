---
type: type_definition
defines: coverage
fields:
  indexed_at:
    field_presence: required
    field_type: text
    desc: "the 12-character commit this index was last reconciled against"
---

# Coverage

**The index of a sweep: every file in scope, and what has happened to it.** One
per sweep, beside the `sweep` that states what the sweep is for.

## Why it is not part of the sweep

**The two stand in opposite relations to the truth.** A sweep's goal and
reasoning should stay true as the work proceeds and get truer as it teaches
something. **This file is expected to go false** — every commit to the
repository ages it — and is brought back to current at every slice.

**So staleness means opposite things in the two.** A stale index is the
ordinary state between slices, and reconciliation exists because of it. A stale
sweep is a defect.

**A file expected to rot must not live inside one expected to hold**, or nobody
can tell which half has gone off.

## `indexed_at` lives here, not on the sweep

It is a fact about the index rather than about the sweep: the commit this table
was last reconciled against, advanced every time a slice reconciles. **The
sweep has no commit** and deliberately so — it is true of a moving target.

## No counts in the frontmatter

**Progress is derived from the rows and written in the body at the time of
writing.** A count in frontmatter is a number a consumer would trust, kept true
by nobody, and wrong from the first status change that forgets it.
