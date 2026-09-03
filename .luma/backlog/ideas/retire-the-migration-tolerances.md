---
type: luma/idea
title: Retire the migration tolerances once the estate has re-adopted
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5]
horizon: next
scope: project
stage: draft
---

# Retire the migration tolerances once the estate has re-adopted

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
