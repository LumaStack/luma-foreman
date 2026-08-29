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

**Scope as data and scope as prose is an anti-pattern, and this sweep proved it
on itself.** The `sweep` type requires `scope:` as a field — a rule — and the
charter template asks for scope prose beneath it. This charter's prose
*enumerated the included paths*, which is the rule copied by hand.

**It disagreed within two slices.** `.gitignore` is tracked, is not `.claude/`
and is not a vendored bundle, so the rule always included it; the list never
named it, so it never got a row. Reconciliation at slice 003 found the file with
nowhere to go.

**The fix is not to drop one of them — they hold different facts.** The field
states the rule. The prose states **what the rule excluded and who decided**,
given or chosen, which no field can carry. **What the prose must never do is
enumerate what is in**, because that is derivable and `coverage.md` already
derives it.

**For the bundle**: `_types/sweep.md` says `scope` must say what was left out.
It does not say the body must not restate what was left *in*, and the template
invites exactly that. Both want the rule. Batched rather than taken — step 8.

*The same shape as `.luma/PROJECT.md`'s `owns`, found in slice 002, running the
other way: there, prose was treated as data; here, data was restated as prose.
**One fact, two records, and the copy is always the half that rots.***

**One wrong table produced three wrong paths in three repositories.**
`luma-config`'s XDG table gave `~/.config/<application>/` and put the
organization segment in a subsection below it. **A table is what a reader takes
as canonical**, so `catalog.py` wrote `~/.cache/luma/catalogs`,
`session-manager` wrote `~/.local/state/luma/sessions`, and this repository's
gate tests wrote `~/.config/luma/foreman`.

**None was reported by anything**, and the reason is worth keeping: a path
nobody has written to before is created on demand, so the wrong path works
perfectly. Nothing notices the right one is empty. **A path defect is silent by
construction** — unlike a wrong command name, which fails the moment somebody
runs it.

**`session-manager` is upstream and out of scope.** Six documents, a
`luma-catalog` fix, recorded here rather than taken because vendored bundles are
excluded and fixing one in place is drift by definition.

**`CHANGELOG.md:96` says `policy doctor` and `policy install`.** Both retired;
the command is `agent-permissions`. Found while checking whether the changelog
held the reversal note — it does, at `:92-93`, and more fully than
`docs/standards.md` did. **`CHANGELOG.md` is a pending row in cluster *plans,
config, changelog* and this is waiting for it.**

**A changelog is the one document where a stale name may be correct**, because
it records what was true when written. `:96` is not that case — it is migration
instructions telling somebody to run a command that no longer exists.

**The check no earlier slice ran: does an adopted bundle already cover this
document?** `docs/standards.md` read as reasonable prose and nothing in it
announced that `luma-config` had taken the subject. **Being superseded is not
visible from inside a file.** Slices 001 and 002 read four documents without
asking, and at least `docs/architecture.md` overlaps `luma-layout`. Worth a pass
before slice 004 rather than after the sweep.

**Four rows were closed by the agent inferring a verdict, and the reader
delegated rather than re-confirming.** Recorded because the rows now look
identical to properly confirmed ones and are not.

| row | what actually closed it |
| --- | --- |
| `docs/scope.md` | *"delete this file"* — an instruction, not a verdict |
| `docs/standards.md` | *"merge 131 and drop standards.md"* — the same |
| `docs/getting-started.md` | nothing quotable; slice 001 records *"approved with it standing"* |
| `docs/inspect.md` | removed rather than closed; the collapse may have been the agent's call |

**All four were kept as they stand**, on *"do whatever you think is right, I'll
trust it"*. **That is a delegation and not a confirmation**, and the difference
matters at the close: four rows rest on the reader's general trust rather than
on four specific answers. `review-sweeps` 0.20.0 stops this happening again.

**`CLAUDE.md` was the fifth and the reader took it back** — *"CLAUDE is
approved, it needs work but good enough for MVP."* A sign-off with a finding
attached, which is why the row reads `approved_by: human:benlinton` with
`outcome: findings` rather than `clean`.

**What the work is was not specified**, and that is recorded rather than
guessed. The one thing known about it: **the file is entirely generated.** Zero
lines outside the `luma:begin`/`luma:end` block, untouched during the slice that
read it — so *needs work* cannot mean the file and must mean what `apply` writes
into it, which is `apply.py` and the entrypoint. **Both are pending rows.**

**And it probably should not have a row at all.** The charter excludes
`.claude/` on reasoning that covers this file exactly — *reviewing generated
output tells you about the generator, which is in scope as `apply.py`* — and
**`luma-layout` groups them explicitly**: *"`.claude/`, `AGENTS.md`, `CLAUDE.md`
and whatever replaces them ... are generated from what is in `.luma/`, and are
disposable."* The scope rule excludes one member of a set the adopted bundle
names as one thing.

**Not corrected, now less than ever.** The row carries a sign-off; flipping a
signed-off row to `skipped` on the agent's reasoning is the defect the entry
above is about. It belongs in the close, or in the next sweep's charter, where
the exclusion can be written once and correctly.
