---
type: luma/idea
title: What happens to routing.toml
created: { by: agent:claude-opus-5, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
stage: draft
---

# What happens to routing.toml

**The design drops it. The permission gate needs it. Neither has moved, and
the file is sitting in the gap.**

`.luma/bundles/routing.toml` is a compiled table `apply` regenerates every
run: one row per Document that declares a trigger, carrying its bundle, its
path, its `matches`, and its `on_violation`. The MVP design lists it among
the artifacts the rewrite deletes. Step 4 of the implementation plan repeats
that, and in the same step requires `agent-permissions` to be untouched —
which it cannot be, because the gate reads this table.

## Why it is still here

**The gate enforces `on_violation = "block"` from it, before every tool
call.** Delete the table and `gate.py` finds nothing to read, which means an
adopted rule that says *block* silently permits instead. Failing open is the
specific failure `agent-permissions` exists to prevent, so the file stays
until its consumer has somewhere else to look.

**Compiled rather than derived, for one reason only.** The gate runs on a
millisecond budget against every tool call; walking `.luma/bundles/` and
parsing frontmatter per call would cost more than the whole gate does. That
is a performance constraint, not a claim that a project-level compiled
artifact is a good shape.

## What is actually at stake, measured

Today the mechanism is **dormant**, which is what makes this a *later* rather
than a *next*:

| | |
| --- | --- |
| rows in this project's table | 37 |
| rows with `on_violation = "block"` | 0 |
| adopted bundles declaring `on_violation` at all | 0 |

`apply` defaults every document to `allow`. So deleting the file today breaks
nothing observable — and that is exactly the trap. The day a bundle carrying
a block rule is adopted, the failure arrives with no error, no notice, and
nothing in the output that says a rule stopped being enforced.

**`on_violation` is a live field, not prototype residue.** The catalog's own
changelogs record `compliance` being removed *in its favour*, so this is a
mechanism nobody has used yet rather than one that has been retired.

## The ways out

**Wait for hook delivery.** What `apply.py`'s own comment intends: the table
is re-homed when the hook arrives, and the gate reads whatever that provides.
Costs nothing now, and leaves a project-level compiled artifact the design
says should not exist for however long that takes.

**Delete the table and the gate's block path together.** Defensible on the
design's own terms — blocking is deferred to `expose` and governance, and the
design says outright that a true block needs something standing between the
model and the content, which a frontmatter field a model can read is not. So
the gate implementing `block` is prototype residue too. This removes a
capability, and step 4's *agent-permissions is untouched* was written to stop
exactly that happening by accident.

**Re-home it now, without waiting.** The gate needs some compiled artifact
for the latency reason; nothing says it has to be this file in this place.
Most work, and it front-runs a hook design nobody has written.

## What would decide it

The first bundle that declares `on_violation: block` — at which point the
dormant mechanism is live and *wait* stops being free. Or hook delivery
landing, which resolves it without anybody choosing. Until one of those, the
cost of leaving it is one generated file and a plan that now says why.

## Related

- [[bundle-routines]] and the routing questions around it
- The design's drops-list, in `.luma/backlog/plans/bundle-design-mvp.md`
- Step 4 of `.luma/backlog/plans/bundle-mvp-implementation.md`, which is where
  the contradiction is recorded
