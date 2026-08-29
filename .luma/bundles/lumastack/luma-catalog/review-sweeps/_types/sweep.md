---
type: type_definition
defines: sweep
fields:
  goal:
    field_presence: required
    field_type: text
    desc: "what the sweep is for — what you want to be true afterwards, stated so it can be checked against"
  strictness:
    field_presence: required
    field_type: enum
    desc: "strict — the goal, scope and strategy are fixed for this sweep. evolving — expect them to move as the sweep learns"
  scope:
    field_presence: required
    field_type: text
    desc: "what is being read — and, in the body, what deliberately is not"
  ordering:
    field_presence: required
    field_type: text
    desc: "the order units are taken in: narrative, risk-weighted, dependency, directory, or led"
  pairing:
    field_presence: required
    field_type: text
    desc: "who is in this sweep — human-agent, or agent-agent. Declared before the first slice"
  contributors:
    field_presence: recommended
    field_type: list of actor
    desc: "everyone reading in this sweep, human and agent alike"
  archived:
    field_presence: optional
    field_type: date
    desc: "when the sweep was closed and moved to archived/"
---

# Sweep

One long read of a codebase, by a reader with a second party beside them. The
Document carries the scope, the order, and the index of what has been covered.

**It is not a record**, and the fields say so: `indexed_at` moves, the index is
edited at every slice, and there is no commit pinning what the sweep is true of
— because a sweep is true of a moving target by construction. What it does
carry is enough to resume it and enough to check its coverage.

*Only what the format does not already have is declared here.* `created`,
`lifecycle_status` and `title` are core fields and are used as they come.

## `goal` is what the sweep is checked against

**Not what it covers — what it is for.** *Read the whole project* is the
method; the goal is what you want to be true afterwards, and it is the only
thing that makes *on track* and *off track* mean anything during a run that
takes weeks.

**Checkable beats precise.** Not a metric — something that could be observed.
*I can answer questions about any part without opening the file* is a goal. *I
want to understand it* is the same wish with the test removed.

**It decides what is worth stopping on.** Two readers with different goals flag
different things in the same file; with nothing written down the agent chooses
for them, silently.

**It is what a drifting sweep is compared against.** Three slices running that
turn up nothing related to the goal mean the goal was wrong or the sweep has
wandered — and neither shows without this field.

## `strictness` decides whether the plan may move

**Not whether the sweep may notice things — whether it may change its own
terms.** Both kinds record everything they find; they differ in what they do
about the ones that would rewrite the sweep.

| | **`strict`** | **`evolving`** |
| --- | --- | --- |
| the goal, scope and strategy | **fixed for this sweep** | **expected to move** |
| something that would change them | recorded, and left for a later sweep | acted on, and the sweep says what changed and why |
| drifting from the goal | **a defect** — the sweep has wandered | ordinary, and a reason to re-aim |
| what it costs | things you noticed wait | **velocity** — every change is time not spent reading |

**A strict sweep is not a blind one.** It routes findings exactly as any sweep
does; what it declines is redirecting itself. *That is a real observation and
this is not the sweep for it* is a legitimate thing to write in a journal.

**Choose `evolving` when the practice or the material is genuinely new**, and
expect to pay for it. The first sweep ever run was `evolving` and produced
thirteen releases of this bundle while covering six files — **correct for a
first sweep, and ruinous for a tenth.**

**Most sweeps should be `strict`.** Once neither the practice nor the material
is new, `evolving` is a licence to be distracted by whatever is more
interesting than the next file.

**It is declared, not drifted into.** A sweep that quietly starts rewriting its
own goal was `evolving` all along and nobody said so — which means nobody
budgeted for it, and the estimate is now wrong for a reason the record does not
show.

## `scope` must say what was left out

The half people skip, and the one that decides whether finished coverage means
anything. *"Everything under src/ and docs/; not the vendored tree, not the
generated clients"* is a scope. *"The repository"* is not — a reader cannot
then tell an empty row from an excluded one.

**Say which exclusions were given to you and which you chose.** An area the
owner ruled out reads differently from one you ran out of appetite for.

## `ordering` is not decorative

It is what makes the sequence checkable afterwards, and what a slice consults
when the convenient next unit is not the correct one. Record the reason in the
body — the field carries the name, the prose carries why.

**Changing it mid-sweep is legitimate and gets a dated line in the body.**
Silently drifting from it is what the field exists to make visible.

**`led` is a value, not a blank.** A sweep whose person picks the next cluster
each slice is running a declared order and says so; the defect the field
catches is a sweep claiming `narrative` while being led in practice.

## The index is not here

**A sweep states what it is for; `coverage` records what has been covered.**
The two have opposite lifecycles — this file is written once and rarely
touched, while the index is edited at every slice — and keeping them together
buries every change of reasoning under a hundred rows of bookkeeping.

`indexed_at` goes with the index, because it is a fact about the index.

## No coverage field

**Coverage is derived from the slices, never stored.** Each slice says what it
covered; the index in the body is a cache of that, and the number in a closing
summary is computed at closing time.

The table in the body is edited constantly and will eventually be wrong. That
is tolerable precisely because it can be rebuilt — **when the index and the
slices disagree, the slices win.**
