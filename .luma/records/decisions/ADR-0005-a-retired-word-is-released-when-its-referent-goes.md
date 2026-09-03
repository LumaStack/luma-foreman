---
type: decision
title: A retired word is released when its referent goes, not when time passes
decided: 2026-08-26
stage: draft
reopen_trigger: Evidence that reinvention does decay — a word retired here, absent for a long stretch, and then plausibly unreinventable by somebody arriving cold. Nothing has run long enough to say.
---

# ADR-0005: A retired word is released when its referent goes, not when time passes

## Summary

A `[[retired]]` entry is removed when **the thing the word named no longer
exists**. Not after a number of releases, not after a number of sessions, and
not because the count has been zero for a while.

## Problem

`inspect --rule vocabulary` reports uses of a retired word, and the natural
instinct once the count reaches zero is to delete the entry — the migration is
finished, so the check has done its job. Some measure of *finished* is needed,
and the obvious candidates are all durations: a few releases, a few sessions,
long enough.

The instinct is right that an entry should not live forever unexamined. The
measure is what is wrong.

## Decision

**An entry may be released when nothing in the product still needs a name for
what the word named.** That is the test, and it is answerable by looking rather
than by counting.

Applied to what is retired here today:

| word | named | releasable |
| --- | --- | --- |
| `refit` | a command that was removed rather than renamed | **released 2026-08-26** |
| `outfit` | the command now called `apply` — still there | **no** |
| `projection` | what `apply` writes — still there | **no** |

`refit` is the worked example: its count reached zero, nothing in the product
needs a name for what it named, and the entry is gone. The other two never
reach that state while `apply` exists.

**A second condition, rarely reached:** the decision that retired the word is
archived with nothing superseding it. A retirement nothing decides is not in
force, and the entry should go with it.

## Why

**A retired word comes back by being reinvented, not by being remembered.** The
words worth retiring are the natural English for what they described, so the
pull toward them is a property of the language rather than of anybody's memory.
That pull does not weaken.

**Which is why a duration measures nothing.** After twenty clean sessions a
human who was present has learned the new word. A fresh agent has not — session
twenty-one is identical to session two for whoever arrives cold, and most of the
prose here is written by somebody arriving cold. *Sessions* is a better unit
than *releases*, because authoring is when words get chosen and a release with
no authoring tests nothing. It is still the wrong axis.

**The evidence is one afternoon.** `projection` was retired, swept out of the
code, the docs, the records and the catalog — and reintroduced in conversation
minutes later, by the same author, while the removal was still in flight. Zero
decay under the most favourable conditions available.

**What protects a project is a clean corpus, and the rule is what keeps it
clean.** Removing the rule because the corpus is clean removes the thing
maintaining the condition that was providing the protection. That is circular in
the direction that fails quietly: nothing breaks on the day the entry goes, and
the word returns whenever somebody next reaches for it.

**And a clean entry costs nothing.** It greps tracked files for one term and
prints nothing when absent. The expense of this rule is entirely in its notices,
which is the state a finished migration has already left.

**A word for a thing that does not exist cannot be reinvented**, which is what
makes the referent test the honest one rather than a refusal to ever release
anything. Nobody reaches for `refit`, because there is nothing to name.

## Alternatives

**After N releases.** Deferred: a release is a publishing event, and words are
chosen while authoring. A quiet release proves nothing. Re-open if releases ever
become the unit in which prose is written.

**After N sessions.** Deferred, and the better of the two — authoring is what
carries the risk. Rejected on the axis rather than the unit: a fresh session has
no memory of the clean ones before it. Re-open with this record's trigger.

**Never release an entry.** Deferred: it is nearly right and fails on
`refit`-shaped words, where the entry can only ever produce a false positive
about a word nobody can revive. Re-open if the referent test turns out to be
hard to answer in practice.

**Release when the notice count has been zero for a while.** Deferred: this is
the duration argument wearing the check's clothing, and it inverts the
mechanism — a rule that has been silent is a rule that has been *working*.

## Tradeoffs

**Pros**
- Answerable by looking at the product rather than at a calendar.
- Releases the entries that genuinely cannot fire again, so the list does not
  only grow.
- A clean entry is silent and nearly free, so keeping one costs no attention.

**Cons**
- The list grows for as long as the product keeps its concepts, and most
  concepts outlive the words retired for them. In some years it will hold
  entries nobody remembers arguing about.
- *Does this thing still exist* is a judgement, and a generous reading of
  "gone" would release an entry early. The `decided` citation is what a reader
  checks it against.

## Standing consequences

**An entry cites the decision that retired the word**, and that citation is what
makes the referent test answerable later — it is where somebody reads what the
word named. An entry without one cannot be released honestly, because nothing
says what it was for.

**A retired-word entry naming a decision that no longer exists is a defect**, and
a checkable one. Not built; worth a rule if the list ever grows past a handful.
