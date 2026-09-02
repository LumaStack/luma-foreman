---
type: document
title: Bundle MVP implementation
description: The ratified bundle design sequenced into landable changes — what each step delivers, what gates it, and what proves it done. The design decides what; this decides in what order.
lifecycle: draft
created: { by: agent:claude-fable-5, at: 2026-09-02T00:00:00Z }
---

# Bundle MVP implementation

**Sequences the [bundle design MVP](bundle-design-mvp.md); decides nothing
the design already decided.** The what and the why live there and in
ADR-0006 through ADR-0010; the declaration surface is LKF spec `v0.0.19`,
already released. This document owns only order, scope per step, and the
check that proves a step done.

**The order exists to avoid throwaway code, and a broken stretch is
accepted.** Two orders were possible. Rewriting `apply` before the
catalog migrates means the new `apply` meets this repository's still
old-format vendored copies, and the only way through is a two-format
compatibility layer — built, tested, and deleted within days, serving
zero external adopters. Migrating the catalog first costs nothing here,
because adoption is a copy: this repository runs on its vendored bundles
and the old `apply`'s committed artifacts, and a newer catalog upstream
affects it exactly as much as a newer library affects a pinned lockfile —
not at all, until step 5 chooses to update. So the catalog migrates
first, `apply` is rewritten against a world where every published bundle
is new-format, and the compatibility layer is never written. Between
steps 2 and 5 the published catalog is ahead of the installed tool, and a
mid-stretch `get` would land a bundle the old `apply` cannot render.
Acceptable: the implementation may pass through broken states, and the
only promise is that step 5 ends with everything working and verified.

## Step 1 — the index generator

**Delivers:** `luma-foreman bundle index <path>` and `--check`. Reads the
bundle's documents' frontmatter (spec-form `matches`: scalar `eager` /
`nothing`, conditions as single-key maps) and `BUNDLE.md`, renders
`INDEX.md` per the design's mock-up — purpose, Required gate, Offered
with compact-rendered matches, By request, the one-line procedure
accounting. `--check` is regenerate-and-compare.

**Gates:** nothing — the spec is released.
**Done when:** generating for a local bundle matches the mock-up's shape;
`--check` passes on a fresh generation, fails on any hand-edit; the
strict parser rejects unknown matches shapes with a report, not a crash.

## Step 2 — catalog migration

**Delivers:** every bundle in luma-catalog on spec `v0.0.19`:
`type: workflow` → `type: procedure`, `workflow/` directories renamed,
`always` → `eager` where declared, `entrypoint` fields replaced by
`matches: eager` on the start-here document, `INDEX.md` generated into
each bundle. Versions bump per the versioning bundle's rules — directory
renames break inbound links, so these are not patch bumps. Published per
the catalog's own process.

**Gates:** step 1 (the generator makes the indexes).
**Done when:** `audit-bundle` is clean on every migrated bundle;
`--check` passes on each published `INDEX.md`; the catalog's own CI, if
any, is green.

## Step 3 — the manifest module

**Delivers:** the line-grammar parser and emitter for
`.luma/bundles/MANIFEST.md`; `get` writes it; a one-time migration
reading `adopted.toml` and emitting the manifest; `register:` parsed and
carried (honored by `apply` in step 4). Strict: unknown keys reported,
malformed lines errors.

**Gates:** nothing — independent of steps 1–2; may run in parallel.
**Done when:** `get` on a test bundle writes a manifest entry matching
the design's mock; the migration converts this repository's
`adopted.toml` losslessly; round-trip (parse → emit) is byte-stable.

## Step 4 — the `apply` rewrite

**Delivers:** the adapter block importing `.luma/bundles/INDEX.md`; the
project index generated from manifest membership plus bundle metadata,
with Required imports for `eager` bundles, per the design's mock-up; a
skill per procedure; the two fixed-cost request skills repointed at
indexes; `register: nothing` honored by skipping. Deleted outright: the
per-project `rings/` generation and its orphan sweep, `routing.toml`,
`entrypoint.md` generation, and the derived class names. Also updated in
the same change: `docs/architecture.md`, which still describes the
entrypoint-and-rings chain — a sentence only true in the past is a
defect.

**Gates:** steps 2 and 3 — `apply` reads only new-format bundles and the
manifest.
**Done when:** `apply` on a fixture project produces the mock-ups'
artifacts; running it twice is idempotent; nothing writes inside any
bundle directory; `agent-permissions` is untouched (its gating tests
still pass).

## Step 5 — re-adopt and verify

**Delivers:** this repository on its own new machinery. Re-`get` every
adopted bundle at its migrated version; run the `adopted.toml` migration;
run `apply`; delete the stale generated artifacts the old `apply` left.

**Gates:** steps 2–4.
**Done when:** `inspect` is clean — membership, integrity, and the
wired-versus-intended comparison all agree; the diagnosing-a-miss walk
(landed, registered, loaded) answers correctly for one bundle followed by
hand; a `token-audit` before/after records the session floor the design
promised against the floor the prototype paid, which is the design's
first real measurement.

## Out of scope, deliberately

Everything the design's eventual state defers: hooks and the binding
table, the injection log, announcement residency, overrides, the binding
record, document promotion into the project index, governance. Each has
its forcing event recorded in the design; none is implementation debt.

## Standing constraints

- Every step lands as a PR with its reasoning in the body; nothing goes
  straight to `main`.
- `apply` never writes inside a bundle; index generation never runs
  against a vendored copy in an adopting project.
- Foreman stays stdlib-only — the strict parsers this plan adds are
  hand-rolled, and their strictness is the validator's, not a format's.
- The format policy stays under evaluation; steps 3 and 4 are its first
  two data points and should be read as such when they land.
