# Slice template

Copy the blocks to `.luma/backlog/sweeps/<slug>/slices/<NNN>-<slug>.md`. **Copy
the blocks, not this file.**

## Frontmatter

```yaml
---
type: slice
title: <the cluster, in a few words>
created: YYYY-MM-DD
covers:
  - src/cli.py
  - src/args.py
contributors:
  - human:<id>        # or agent:<model> — the reader need not be a person
  - agent:<model>
---
```

**List every file read, including the ones where nothing was found.** Coverage
is derived from `covers`; a file left out of it cannot be shown to have been
examined.

## Body

```markdown
# <NNN>: <the cluster>

## What this is

<The orientation, compressed to what is worth keeping. What these files do and
how they connect — the part a later slice will want.>

## What we made of it

<Their read first, then yours. Where you disagreed, and why — a slice where
the agent agreed with everything is worth a second look.>

<If the agent read first — because they asked, or because the file warranted
it — say so here. A disclosed weakness can be discounted.>

## Against the goal

<One clause: did this slice serve what the sweep is for? Three in a row that
did not is a signal, not a mood.>

## What this makes me doubt about earlier

<Optional, and often the most valuable section. A sweep learns as it goes and
the ninth slice routinely falsifies the third.>

## Where it went

<Every outcome, routed out of the sweep during this slice. Nothing worth
keeping stays in this note — it is archived with the sweep and eventually
deleted.>

| what is wrong | where it went | fix proposed? |
| --- | --- | --- |
| retry loop swallows the timeout | idea — `.luma/backlog/ideas/retry-swallows-timeout.md` | yes — reasoning recorded, landed as PR #214 |
| this whole layer wants restructuring | idea — `.luma/backlog/ideas/flatten-the-transport-layer.md` | no — too large to see from here |
| why the cache is keyed on the raw path | decision — ADR-0012 | n/a — nothing wrong |
| the four config readers disagree | finding — audit 2026-09-02-a1b2c3d4e5f6 | yes, as a suggestion only |

<A proposed fix is a suggestion, never a directive — record why, not just the
diff. Whoever applies it re-derives first, because it is stale from the moment
it is written.>

## Still open

<Only a conclusion the sweep genuinely has not reached yet — a suspicion needing
more slices before it can be stated. Say what would confirm it.>

<Not a to-do list. Anything actionable was routed above.>
```
