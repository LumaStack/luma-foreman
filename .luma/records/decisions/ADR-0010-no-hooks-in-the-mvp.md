---
type: decision
title: No hooks in the MVP
decided: 2026-09-02
stage: draft
---

# ADR-0010: No hooks in the MVP

Loading is model-mediated in the MVP. The one machine-kept guarantee is
the harness's always-loaded chain; no hook is installed for knowledge
delivery.

## Problem

Hooks can evaluate matchers per tool call and inject content — a real
guarantee where the MVP has a model's judgement. Building them first
would be the normal thing to do, and it would mean per-call evaluation,
dedup, an injection log, and an installed component that can silently not
be installed — all built against a failure rate nobody has observed.

## Decision

**Hooks buy exactly one thing — machine-kept conditional loading — and
the MVP makes no conditional promises to keep.** `eager` is kept by
imports into the always-loaded chain; everything conditional is offered,
where the model deciding is the design, not a degradation. The structured
matcher vocabulary is already shaped for a hook to read, so the upgrade
re-authors nothing.

**The graduation paths are recorded, not improvised:** a hook that
evaluates `path:`, `command:`, `tool:` and `event:` with dedup and a log;
the Required gate graduating from instruction to injection when a bundle's
index is opened; announcements re-asserted after a context reset, so the
model's map survives what the conversation cannot; degradation reported
on harnesses without the hook, never silent.

## Why

Promise only what a mechanism keeps. A `guaranteed` that nothing enforces
reads as kept to its author, its adopter, and every audit — which is
worse than an honest *offered*. And enforcement machinery built before
any measured miss is machinery sized against a guess.

## Alternatives

**Hooks now** — rejected as above. **Skills as knowledge carriers** —
rejected: skills are workflow-shaped registrations, and policy knowledge
would pollute the skill namespace while still being model-mediated.
**Inlining required documents into generated files** — rejected: `apply`
writes pointers, never copies.

## Re-open when

The first measured case of a model failing to open what an index plainly
matched, where the miss cost something. That is the forcing event this
record exists to name. Full reasoning:
[bundle design MVP](../../backlog/plans/bundle-design-mvp.md).
