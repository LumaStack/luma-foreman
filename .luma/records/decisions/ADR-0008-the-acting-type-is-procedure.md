---
type: decision
title: The acting type is procedure
decided: 2026-09-02
lifecycle: draft
---

# ADR-0008: The acting type is procedure

The LKF type for invocable, executable knowledge is `procedure` — not
`workflow`, not `skill`. Proposed upstream as a spec rename.

## Problem

The type was named `workflow`, which misnames the thing — everywhere else
in software a workflow is an orchestrated multi-step process, and this is
a single set of steps an agent carries out — and spends the word future
orchestration will want. The obvious replacement, `skill`, is what these
things are in the concept sense, but the concept word is entangled with
one harness's artifact and its SKILL.md contract.

## Decision

**`procedure`**, named by the invariance test: sometimes this renders as
a skill, sometimes as a command, someday under a real workflow — it is
always a procedure. The source is named for the invariant across its
renderings, never for one of them.

**`workflow` is reserved** for a future thing that composes procedures,
if it ever comes. **`skill` is used only at the harness boundary**, where
it is true: a procedure installs as a skill in Claude Code. **`invoke`**
and **`invocable`** are the verbs everywhere.

**No invocable-name field** — the name derives from the filename, and
per-project collisions are the binding's to resolve at apply. **No
`matches` needed** — a procedure's surfacing is harness registration, its
description becoming the skill description.

## Why

`policy` beside `procedure` gives the acting types a pair every
institution already knows. And the word never wobbles when a second
harness arrives — *our procedures install as commands there* is the
design working.

## Alternatives

**Keep `workflow`** — rejected: misnames and spends the orchestration word.

**`skill`** — came closest. The package precedent (npm, cargo, apt: one
word, many metadata schemes, disambiguated by namespace) makes *an LKF
skill* defensible, and users will often say "skill" regardless. Rejected
because naming the source after one rendering is the overclaim pattern
(`always` scope, `trigger` causation, `router` agency), and it invites
the SKILL.md-contract misreading.

**`ability`, `protocol`, `invocation`, compounds like `portable-skill`** —
each fails a test: names the effect not the artifact, collides with MCP,
names the act not the thing, or truncates back to the word being avoided.

## Re-open when

The LKF spec rejects the rename, or the ecosystem settles "skill" as the
fully generic cross-vendor concept while harness diversity never
materializes. Full reasoning:
[bundle design MVP](../../backlog/plans/bundle-design-mvp.md).
