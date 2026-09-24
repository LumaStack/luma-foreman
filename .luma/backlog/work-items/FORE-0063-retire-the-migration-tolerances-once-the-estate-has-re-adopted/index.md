---
type: work-item
key: FORE-0063
title: Retire the migration tolerances once the estate has re-adopted
workflow_status: closed
rank: 070.0030.000
kind: idea
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-03T00:00:00'}
description: 'They are: The deferral was recorded in commit `f596cd6` (PR #116): the tolerances stay because other estate repositories (luma-clarify, luma-backlog, …) still hold old-format bundles and share this binary. This file exists so the cleanup stops living only in commit archaeology.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:47:17Z'}
closed: {on: 2026-09-24, as: completed, by: 'agent:claude-opus-5/luma-backlog', reason: 'Delivered before this record existed; the idea recorded it as answered and pruned, and the outcome was written and checked during the migration into the backlog.'}
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
[[plans/migrate-estate-to-type-definitions]] wave — so "every repository migrated"
is a query over frontmatter rather than a belief: grep the estate for typed
documents with no `type_version`, and for any `_types/` directory still on
disk. When both come back empty, the tolerances above have nothing left to
tolerate.

## Related work

- Born from the idea it replaces: [`retire-the-migration-tolerances`](../../ideas/retire-the-migration-tolerances.md)
