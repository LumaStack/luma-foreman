---
type: decision
title: The manifest records custody and intent
decided: 2026-09-02
lifecycle: draft
---

# ADR-0009: The manifest records custody and intent

The project's record of its bundles is `MANIFEST.md` — a receipt kept by
commands, recording *did we get this* and *should this be wired*, and
never *is it wired*.

## Problem

`adopted.toml` conflated a name with a state — a bundle written locally
was never adopted — and nothing distinguished what a file must record
from what a comparison can answer. Every past attempt to design an
applied-state record produced a file that could lie: true the moment
written, false the moment anything changed without it.

## Decision

**A receipt of unrecoverable facts.** Per vendored bundle: version taken,
source, commit, checksum. A bundle written here is a bare entry — the
kinds are distinguished by shape, not a flag.

**Intent, divergence-only.** `register: nothing` marks a bundle
deliberately landed and not wired; absence means wire everywhere. The
value space is *what to register into* — a harness list is the possible
future — never a boolean, and never event data: who applied what, when,
is the committed manifest's git history.

**Nothing records derived state.** Wiring is verified by
regenerate-and-compare, healed by regeneration from checksummed inputs,
rolled back by git. `inspect` compares recorded intent against derived
actuality and reports both mismatch directions.

**The line grammar, per the format policy** (held under evaluation in
the design): one bullet per bundle, `key: value` sublines. A bare line
naming a bundle is already valid, so an authored future — partial entries
a tool resolves — is a behavior change, not a format change.

## Why

Records that describe generated state teach the system to heal toward
corruption; records of decisions and custody cannot be contradicted by
anything on disk. What earns a record is a decision, never an artifact —
the future binding record (stable name assignments, provider choices)
follows the same rule as another input to `apply`.

## Alternatives

**An authored manifest now** — deferred; the only adopters are the
authors. **An applied-state record or wiring snapshot** — rejected as
lie-shaped. **Separate manifest and registry files** — rejected: a second
file earns existence only when writer or lifecycle differ, and neither
does. **TOML** — no standard-library writer exists, even for a
regenerated receipt.

## Re-open when

Somebody wants to claim bundles by hand (authored partial entries), or
per-harness wiring is forced (`register:` grows a list). Full reasoning:
[bundle design MVP](../../backlog/plans/bundle-design-mvp.md).
