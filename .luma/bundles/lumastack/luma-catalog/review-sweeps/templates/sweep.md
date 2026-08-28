# Sweep template

Copy the blocks to `.luma/backlog/sweeps/<slug>/sweep.md`. **Copy the blocks,
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
ordering: narrative | risk-weighted | dependency | directory | led
indexed_at: <12-character commit the index was last reconciled against>
contributors:
  - human:<id>        # or agent:<model> — the reader need not be a person
  - agent:<model>
---
```

## Body

```markdown
# Sweep: <what is being read>

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

## Order

**<the order>** — <one sentence of why. This is what the slice consults when
the convenient next unit is not the correct one.>

<A dated line here for every change of order. Silent drift is what this section
exists to make visible.>

## Size

<A band, said to be a guess, estimated from the material rather than the file
count — prose and dense logic differ by more than an order of magnitude. Split
it where the scope is several kinds of thing.>

<Replace this with a measured rate after the second slice, and say what the
rate was. That number is worth more than any care taken over this one.>

**Expected drift:** <how much of the scope changed in a window the length of the
estimate, and which parts — churn concentrates, so name the hot areas rather
than giving one percentage. Say whether that churn is finishing or ongoing;
only the owner knows. Compare against it at close.>

## Index

<Every file in scope. Grouped into the clusters expected to be reviewed
together. A file missing from here can never be shown to have been read.>

| cluster | file | status | slice |
| --- | --- | --- | --- |
| entrypoint | `src/cli.py` | reviewed | 001 |
| entrypoint | `src/args.py` | reviewed | 001 |
| gate | `src/gate.py` | pending | |
| — | `src/generated_api.py` | skipped — generated | |

`pending` · `reviewed` · `skipped` **with a reason, always**

<Strike a deleted file through rather than removing the row, so the index still
explains itself.>

## Closing summary

<Written at close, not before. Coverage as counts; what it produced and where
each thing went; what it changed about how you see the system; and why it
stopped, if it stopped early.>
```
