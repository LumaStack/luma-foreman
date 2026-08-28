---
type: type_definition
defines: sweep
fields:
  goal:
    field_presence: required
    field_type: text
    desc: "what the sweep is for — what you want to be true afterwards, stated so it can be checked against"
  scope:
    field_presence: required
    field_type: text
    desc: "what is being read — and, in the body, what deliberately is not"
  ordering:
    field_presence: required
    field_type: text
    desc: "the order units are taken in: narrative, risk-weighted, dependency, directory, or led"
  indexed_at:
    field_presence: required
    field_type: text
    desc: "the 12-character commit the index was last reconciled against"
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

## `indexed_at` is what keeps the index honest

The tree moves under a sweep — by the sweep's own fixes, if nothing else — so
every slice reconciles the index from this commit to `HEAD` and then advances
it. Without it, reconciliation is a guess about what has already been accounted
for.

## No coverage field

**Coverage is derived from the slices, never stored.** Each slice says what it
covered; the index in the body is a cache of that, and the number in a closing
summary is computed at closing time.

The table in the body is edited constantly and will eventually be wrong. That
is tolerable precisely because it can be rebuilt — **when the index and the
slices disagree, the slices win.**
