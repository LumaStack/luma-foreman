# Changelog — `sweep`

The history of the `sweep` Type Definition, newest first, keyed by the
type's own `version`. History from before it declared one is in this
repository's git history — no retroactive backfill.

## 0.0.2

- The four discipline and approval enums gain `values:` keys —
  `goal_discipline`, `scope_discipline` and `strategy_discipline` declare
  [strict, adaptive, exploratory], `approval` declares [required,
  recommended, optional, prohibited]. The vocabularies were already in
  each field's `desc` prose, where a validator cannot read them; the spec
  requires `values` when `field_type` is enum, and `luma-foreman lint`
  reported exactly that. No field is added, removed, or re-presenced —
  every document valid against 0.0.1 is valid against 0.0.2.
  Shipped 2026-09-20.

## 0.0.1

- Versioning begins: the type declares its own `version`, independent of
  the bundle's. Shipped 2026-09-19 with the catalog's migration to LKF
  v0.0.21, which moved every Type Definition to the folder shape — this
  definition now lives at `type_definitions/sweep/DEFINITION.md`, with
  this changelog beside it. The contract is otherwise unchanged.
