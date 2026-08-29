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

**Correction to the entry above** — the scope is *within the catalog*, not code
review generally. Sweeps as how the estate formalises its own reviews, rather
than a claim about the practice at large. Narrower, and considerably more
plausible: the estate already runs on bundles, coverage and routed findings, so
a sweep aimed at a change rather than a repository is a smaller step than it
looked a paragraph ago.

*Appended rather than edited. A view that has moved on gets a new entry.*

**`.luma/PROJECT.md` wants a rework and it was deliberately not taken.**

**The prose should be thin and earn its place** — help a human or an agent, and
be written so it does not rot. What is there is longer than its job needs and
duplicates `docs/architecture.md`, which now carries the invariants and the
boundaries.

**The frontmatter needs work and may need to require more.** In particular:
**`owns` and `must_not_own` are prose that is treated like data.** List syntax,
free-text values — so they *look* structured and nothing can validate them,
match against them, or enforce them. The field's stated job is routing, and
routing needs matching.

The type's own example uses names: `owns: [storefront, checkout,
payment-integration]`. This repository has three sentences. **A clause cannot be
matched against a question** — *which repository owns adoption?* is answerable
from names and not from prose. Length also hid the gap: `owns` omits adoption
entirely, and four names checked against seven commands would have shown that
where three sentences did not.

**It reaches past this repository.** `luma/project` is defined in
`lumastack/luma-catalog/luma-types` and vendored, so tightening those fields is a
change there and affects every project carrying a descriptor.

**Undecided, which is why this is here and not an idea**: whether `owns` should
be a closed vocabulary, a list of short names, or something derived rather than
asserted; what else the frontmatter should require; and whether the prose
survives at all.

*Filed as an idea first and withdrawn — the shape is a direction rather than a
task, and routing it prematurely is the failure this file exists to prevent. The
close will promote it if it still warrants one.*

**`docs/scope.md` was deleted, and the deletion needed a ledger.** The reader
asked to be able to check afterwards that the right things survived and the
outdated things did not — *"some of what's in scope is outdated, and I want to
verify the correct stuff made it where it belongs."*

**A diff alone does not answer that.** `git show` proves what moved; it cannot
show what was dropped *on purpose* versus dropped by accident, and those look
identical in a deletion. The slice record carries a per-line-range table with a
verdict column for exactly that, and three rows say **dropped as false** or
**dropped as unsourced** rather than naming a destination.

**Worth promoting to the bundle if it holds.** `what-a-slice-produces` says a
slice produces a record; it does not say a slice that removes a file owes a
ledger of where the file went. **The obligation appears when the artifact stops
existing** — nobody can re-derive the mapping from a file that is gone.

**The transitional cluster half-collapsed.** `split from README` was declared
transitional and expected to fold into `what it says it is` once read. All four
of its rows are now closed, so it should fold at the next reconciliation — and
`what it says it is` is closed too. **Two clusters are done and the charter
still lists both**, which is the first thing reconciliation should tidy.
