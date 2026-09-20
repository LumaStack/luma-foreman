---
type: luma/idea
type_version: "0.1.0"
title: Rename _types/ to type_definitions/
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5]
horizon: next
scope: project
stage: draft
archived: 2026-09-20
---

# Rename `_types/` to `type_definitions/`

> **Done, and pruned.** LKF `v0.0.21` shipped the rename (and went further:
> every Type Definition is a folder), and the blast-radius list below was
> executed in full by 2026-09-20 — foreman's code (#158), the bundle-manager
> prose and template plus every type-carrying bundle (luma-catalog#168), and
> the re-adopt across the estate (#159, luma-backlog#147, luma-leader#72,
> luma-catalog-curator#25). The estate-wide query returns zero `_types/`
> anywhere. The argument below is the record of why the name changed.

**The bundle directory for Type Definitions should be named after what it
holds, like its siblings.** The files in it are documents declaring
`type: type_definition`, and the concept is already called a Type Definition
everywhere the prose speaks — the directory is the only place the name hides.

The underscore was collision avoidance from when types might have lived at
project roots. They now live only inside bundles, where the author controls
every sibling, so the fear is obsolete. The prefix's other reading —
machinery, not reading material — was never load-bearing: `templates/` gets
the identical tooling exemption with no prefix.

**Rejected:** `lkf_types` and `format_types`. Everything in a bundle is the
format, so the qualifier distinguishes nothing — and the format's name,
embedded in a directory vendored into every adopted project, is the most
expensive place to put a brand while the spec is at v0.0.x. Plural over
singular, matching `concepts/` and `templates/`.

## Blast radius

`_types/` is reserved by the format, so this is an LKF spec change first,
then:

- foreman: `SKIP` in `apply.py`, `EXEMPT_DIRS` and the `_types/` doc-id
  check in `inspect/rules/bundles.py`;
- the bundle-manager bundle's prose (`organizing-a-bundle.md`,
  `audit-bundle.md`) and the `type-definition.md` template;
- every bundle in luma-catalog that carries a `_types/`;
- a re-adopt across the estate.

Sequences naturally with the estate migration behind
[[retire-the-migration-tolerances]] — one re-adopt wave can carry both.

**The spec change shipped: LKF `v0.0.21` renamed the directory and made every
Type Definition a folder.** The estate-wide execution plan is
[[migrate-estate-to-type-definitions]], executed in full — kept in `plans/`
for now as a reference, past its own prune-when-done rule, at the
maintainer's request.
