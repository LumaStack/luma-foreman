---
type: journal
title: Journal — the whole of luma-foreman
created: 2026-08-29
---

# Journal

**Scratch, newest last, append-only.** Add entries; never revise them — a view
that has moved on gets a new entry saying so.

**Nothing here is meant to survive the sweep.** The close harvests every entry
into a backlog item, a learning, or a deliberate drop.

## 2026-08-29 — opened during slice 002

**Backdated from slices 001 and 002**, which ran before this file existed. These
were being carried in conversation with nowhere to put them, which is the gap
the journal was added to close.

---

**`index` may be retired vocabulary and nothing enforces it.** The word was
replaced by *entry point* and *routing* somewhere, and `docs/architecture.md`
was using it wrongly until slice 001. The `vocabulary` rule ran clean because
the term is not configured. Check against `.luma/records/decisions/` when that
cluster comes up — if it was decided, the rule should know; if it was never
decided, that is why nothing caught it.

**Two documents now describe how `apply` reaches an agent.** `docs/commands.md`
and `docs/architecture.md`, since the README split. Not a finding yet — one is
behaviour and one is shape. **Watch whether a third appears**, or whether they
start disagreeing.

**`docs/commands.md` is the last hand-maintained thing tracking a moving CLI.**
Nothing fails when an eighth command lands. Slice 001 found two false claims in
it after one day. The `cross-check` habit is the only thing standing between it
and rot, and a habit is not a check.

**`docs/architecture.md`'s `apply` section is now a third of the file**, against
three sentences for `get`. May be correct — `apply` is the least obvious thing
foreman does — or may be where the writing went because it was interesting.
Revisit after the `src/` clusters, when there is something to compare it to.

**The invariants in `docs/architecture.md` are unenforced.** *Does this still
work with no hq* is a test somebody has to remember to apply; `inspect` has five
rules and none of them is this. Probably unenforceable, but worth deciding
deliberately rather than by omission.

**`.luma/PROJECT.md` went three days untouched** while the README was rewritten,
four documents were split out of it, a bundle's vocabulary was renamed twice and
the format's section numbering changed. **A descriptor that does not move while
its subject does is where drift accumulates unseen** — and it had drifted, at
`:5`. Worth checking whether anything else in `.luma/` has the same quiet
profile.

## 2026-08-29 — during slice 002

**Sweeps might become how code reviews are formalised.** Raised while adding
strictness to the bundle, and explicitly *not a bridge to cross yet*.

Worth noting what the sweep already has that a code review wants: coverage that
can be proven rather than claimed, a reader whose independent judgement is
protected, statuses that record who signed off, and a record that says what was
*not* looked at. What it lacks is a diff — a sweep is aimed at a repository, and
a review is aimed at a change.

**Not actionable.** Harvest as an idea against `review-sweeps` at the close, or
drop it if it still looks premature then.
