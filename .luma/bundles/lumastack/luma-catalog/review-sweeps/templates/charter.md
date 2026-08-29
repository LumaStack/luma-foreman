# Charter template

**This file is why the sweep exists and how it is being run.** The index of
what has been covered lives beside it in `coverage.md` — see [the coverage
template](coverage.md). This one is written once and rarely edited; that one
changes at every slice.

Copy the blocks to `.luma/backlog/sweeps/<slug>/charter.md`. **Copy the blocks,
not this file** — this file has no frontmatter of its own on purpose, so
nothing reads it as a real sweep.

## Frontmatter

```yaml
---
type: sweep
title: <what is being read, in a few words>
created: YYYY-MM-DD
lifecycle_status: provisional
goal: <what you want to be true afterwards, stated so it can be checked>
scope: <one line — and say what is excluded in the body>
goal_discipline: strict | adaptive | exploratory       # default adaptive
scope_discipline: strict | adaptive | exploratory      # default adaptive
strategy_discipline: strict | adaptive | exploratory   # default adaptive
ordering: narrative | risk-weighted | dependency | directory | led
approval: required | recommended | optional | prohibited   # default recommended
pairing: human-agent | agent-agent
contributors:
  - human:fsmith      # or a second agent — the reader need not be a person
  - agent:opus-5
---
```

## Body

```markdown
# <what is being read>

## Goal

<What this sweep is for. Not "read everything" — that is the method. What do you
want to be true afterwards, and how would you know?>

**On track means:** <the observable version. Every slice gets checked against
this; three in a row that do not touch it means the goal was wrong or the sweep
has wandered.>

## Scope

<What is in. Paths, or a description precise enough to enumerate from. The goal
above should have narrowed this.>

**Not included:** <the half people skip. Without it, finished coverage means
nothing. Say which exclusions you were given and which you chose.>

## Clusters

<Named here, because they are authored. Group by what must be read together — a
subsystem, an execution path, a set of documents answering one question — which
is routinely not what shares a directory.>

| cluster | what it is |
| --- | --- |
| | |

<A file that fits none of these means this list is incomplete. Add a cluster
here rather than improvising one in coverage.md — the index applies this
strategy and does not invent it, which is what keeps it derivable.>

## Discipline

<A ladder of what you know. strict — you know what you are doing, so do not
touch it. adaptive — you know the shape, so refine and tune it. exploratory — you
do not know the shape yet, so go and find what it should be.

Absent, every axis is adaptive. The common mature configuration is strict goals,
strict scope, adaptive strategy: do not wander, but do improve how you read. A
first sweep of a new practice is exploratory on all three, and costs what
discovery costs.>

## Order

**<the order>** — <one sentence of why. This is what the slice consults when
the convenient next unit is not the correct one.>

<A dated line here for every change of order. Silent drift is what this section
exists to make visible.>

## Size

<A band, said to be a guess, estimated from the material rather than the file
count — prose and dense logic differ by more than an order of magnitude. Split
it where the scope is several kinds of thing.>

<Replaced by measurement, re-taken at every slice. A range with the number of
slices behind it, never a point estimate. Every slice counts — an odd one widens
the range, which is the signal.>

**Expected drift:** <how much of the scope changed in a window the length of the
estimate, and which parts — churn concentrates, so name the hot areas rather
than giving one percentage. Say whether that churn is finishing or ongoing;
only the owner knows. Compare against it at close.>

## Learnings

<What running this sweep taught — about the material, and about sweeping.
Written as it happens, not reconstructed at the close. This is the section a
second sweep reads first.>

## Closing summary

<Written at close, not before. Coverage as counts; what it produced and where
each thing went; what it changed about how you see the system; and why it
stopped, if it stopped early.>
```
