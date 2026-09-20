---
type: luma/idea
type_version: "0.1.0"
title: Retire the migration tolerances once the estate has re-adopted
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5]
horizon: next
scope: project
stage: draft
archived: 2026-09-20
---

# Retire the migration tolerances once the estate has re-adopted

> **Done, and pruned.** The gate was satisfied 2026-09-20 — the estate-wide
> query (zero `_types/` directories, zero typed documents missing
> `type_version`, all eight repositories) came back empty — and the three
> tolerances were removed the same day: `always` now resolves like any unknown
> keyword and inspect reports it as a finding; the implicit `adopted.toml`
> read is gone, with `bundle migrate-manifest` kept as the one explicit
> migration path; `applied()` answers from the project index alone. The
> analysis below is the record of why they existed.

**Three tolerances were left in foreman so old-format bundles keep working
while the rest of the estate migrates. Once every estate repository has
re-adopted on the new catalog, remove them.**

They are:

- the `always` keyword in `lkf.matches` and in inspect's KEYWORDS — superseded
  by `eager`;
- the legacy `adopted.toml` read — superseded by `MANIFEST.md`, which any write
  already retires in place;
- `applied()`'s entrypoint fallback — superseded by the project index.

The deferral was recorded in commit `f596cd6` (PR #116): the tolerances stay
because other estate repositories (luma-clarify, luma-backlog, …) still hold
old-format bundles and share this binary. This file exists so the cleanup stops
living only in commit archaeology.

**Gate:** every estate repository migrated and re-adopted. Believed, not
confirmed, that an un-migrated repo's `apply` under new foreman yields zero
skills until it re-adopts — worth confirming during the migration itself.

**The gate became checkable with LKF `v0.0.21`.** Documents now carry
`type_version`, and the estate stamped them during the
`migrate-estate-to-type-definitions` wave (a temporary plan, pruned with the
wave it drove) — so "every repository migrated"
is a query over frontmatter rather than a belief: grep the estate for typed
documents with no `type_version`, and for any `_types/` directory still on
disk. When both come back empty, the tolerances above have nothing left to
tolerate.
