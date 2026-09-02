---
type: decision
title: Loading posture is derived from matches
decided: 2026-09-02
lifecycle: draft
---

# ADR-0007: Loading posture is derived from matches

A document declares one field, `matches`; its loading posture —
guaranteed, offered, or standby — is derived from the matcher's shape and
never declared beside it.

## Problem

How knowledge reaches context needs an authored declaration, and the
prototype grew two: a matcher and a classification flag. Two fields that
can disagree are two fields that will, and they did.

## Decision

**One field.** `matches`, in LKF frontmatter, with the vocabulary `eager`,
`topic:`, `path:`, `command:`, `event:`, `tool:`. Model-evaluated in the
MVP; the structured forms are machine-evaluable later without re-authoring.

**The derivation:** `eager` → guaranteed (loads when its container
loads); conditions → offered (announced in its container's index, the
model decides); absent → standby (a request or a citation is the way in).
Postures are container-relative: `eager` on a document means required
reading when its bundle opens; `eager` on a bundle lifts its required
documents into every session's floor.

**The grammar** is the spec's: `eager` and `nothing` are scalar values of
the field, never members of the condition list, and conditions are a list
of single-key maps — the extensible form, growing qualifier keys in place
if one ever earns them, with none defined yet.

**The names:** `eager`, not `always`, which overclaimed scope; the field
stays `matches`, not `trigger`, which overclaims causation. `nothing`
stays as deliberate absence — and is never a lock: the postures say what
volunteers content, never what may be reached.

**Deferred:** the `expected` / `optional` split inside *offered*, until a
load log can observe a miss. Every delta went upstream as an LKF spec
proposal rather than a convention smuggled around it, and was ratified in
spec `v0.0.19` — `matches` is now a core field, optional everywhere.

## Why

The declaration shape is expensive to change later — every bundle carries
it — while the mechanism under it is cheap to change. Deriving the posture
makes disagreement between declaration and classification structurally
impossible, and container-relative pricing makes the session floor
computable: the chance the container loads, times the size.

## Alternatives

**A posture field beside the matcher** — the prototype's shape; rejected
as a second copy of one fact.

**`skip-register`-style negated flags and boolean values** — rejected
wherever they arose: a value that only ever takes one state is a marker
wearing a value costume.

## Re-open when

A load log exists and the `expected` / `optional` split can be acted on —
that adds a distinction, not a reversal. Full reasoning:
[bundle design MVP](../../backlog/plans/bundle-design-mvp.md).
