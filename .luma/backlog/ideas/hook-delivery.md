---
type: luma/idea
title: Building hook delivery
description: How the fired transport gets built — which hook carries what, the once-per-session rule that keeps it from costing more than it saves, and the three questions to settle before any of it.
stage: draft
created: { by: human:benlinton, at: 2026-08-28T00:00:00Z }
modified: { by: agent:claude-opus-5, at: 2026-08-28T00:00:00Z }
---

# Building hook delivery

**For review before anything is built.** This is step 4b of
[knowledge-delivery](knowledge-delivery.md) — the *fired* transport, the one
`how-knowledge-arrives` calls guaranteed.

## What planning it changed

**Automatic delivery is per-document, not per-ring.** 4b was written as *fire the
bundle ring automatically*. It should not. A trigger names one document and
knows exactly which — delivering its whole ring instead would hand over a map
nobody asked for and charge for the rest of the bundle.

So the two halves separate cleanly, and the split is worth stating as a rule:

| | what arrives | chosen by |
| --- | --- | --- |
| **automatic** | one document | its own trigger |
| **deliberate** | a ring | a person or an agent asking |

Rings stay a browsing surface. `/load-bundle` and `/list-bundles` already cover
them and need no hook.

## Which hook carries what

| event | carries | confidence |
| --- | --- | --- |
| `PreToolUse` | `path:`, `command:`, `event:` — 24 of 44 trigger mentions | **high** — the gate already reads `routing.toml` here |
| `UserPromptSubmit` | `topic:` — 20 mentions | **low, see below** |
| `SessionStart` | `1-project` | **questionable, see below** |

## The once-per-session rule, which is not optional

**A trigger fires as often as the thing it watches happens.** `path:.luma/**`
matches every edit under `.luma/`, and this session made dozens. Injecting the
same policy body each time would spend more context than the whole design saves.

**So delivery is once per document per session**, and that needs state keyed on
the `session_id` every hook receives. Nothing in foreman keeps per-session state
today, so this is new machinery rather than a flag.

**It is also the first thing to build.** Without it, the first `path:` rule to
fire in a busy session is a regression, and a delivery mechanism that has to be
switched off is worse than none.

*Open: does a re-fire ever deserve a second delivery — a rule broken twice, an
hour apart? A one-line reminder rather than the body is a middle option, and
`on_violation` may be the field that decides, not `matches`.*

## `topic:` is deliverable, and weakly

**Correcting an overclaim from earlier today.** `UserPromptSubmit` accepts
`additionalContext` and sees the prompt, so a topic *can* be delivered. I called
that two-thirds of the surface moving from advisory to guaranteed. It is not.

**A `topic:` value is a sentence** — *"capturing an idea worth keeping"* — and
matching a prompt against it needs judgement. The hook types that can bring
judgement, `prompt` and `agent`, are **only available on tool events**:
`PreToolUse`, `PostToolUse`, `PermissionRequest`. `UserPromptSubmit` gets a
`command` hook, which is a shell process doing lexical matching.

So `topic:` becomes **mechanically triggerable by keyword**, not reliably
matched. Better than nothing and much worse than the other three.

*Open: is lexical matching on a hand-written sentence worth having at all?
Options are keywords declared beside the topic, an LLM call the hook makes
itself, or leaving `topic:` to the model and saying so plainly. **Do not build
this until it is answered** — a matcher that fires on a third of the right
prompts trains people to ignore it.*

## `SessionStart` may not be worth building

`1-project` already arrives through the `CLAUDE.md` adapter, which works. Moving
it to `SessionStart` swaps one Claude Code mechanism for another — **it is not
more harness-neutral**, it is a different harness-specific route, and it costs a
process at every session start.

**The one real argument for it:** `CLAUDE.md` belongs to whoever wrote it, and
the managed block is a guest there. A hook owns its own channel entirely.

*Open: is that worth a hook? My reading is no, not yet, and this stays on the
list only because it was on it.*

## Order

1. **Session state and the once-per-session rule.** Nothing ships before it.
2. **`PreToolUse` delivery** — highest confidence, mechanical triggers, and the
   gate is already there reading the same table. This is the real deliverable.
3. **Measure.** A session's delivered bytes, against the 5,783 standing cost.
   Routing was always the mechanism and token management the objective; this is
   the first thing that can be measured against a baseline rather than argued.
4. **`topic:`** — only after its open question is answered.
5. **`SessionStart`** — only if the argument above gets stronger.

## What this does not touch

**`on_violation` stays where it is.** Blocking is the gate's job at `PreToolUse`
and is already built; this adds delivery alongside it. Two fields, two jobs, one
event — and a rule that both blocks and teaches should do both in one place.

## Why hooks are the only place an adapter is owed

**`SKILL.md` is an open standard and many agents read it, so skill distribution
is solved and not worth competing on** — one output written to the standard,
rather than an adapter per harness.

**Hooks have no standard**, which is what makes them the exception. Every
harness that fires them fires them its own way, so a per-harness adapter is the
only shape available. **That is the argument for this plan existing separately
from knowledge delivery at all**, and it is worth stating because the obvious
symmetry — *skills get adapters, so hooks get adapters* — has the reasoning
backwards.

## And this may not be foreman's job

**Both *set up tooling so projects stay in compliance* and *load and unload
hooks* imply foreman writing configuration it invented**, which puts it back to
knowing things — the boundary
[architecture](../../../docs/architecture.md) draws. **They may instead be
bundles carrying config that adoption copies**, in which case foreman builds the
copying and nothing else. Worth settling before building the second half of
this plan rather than after.

*Both absorbed from `docs/scope.md` when that document was scattered on
2026-08-29.*
