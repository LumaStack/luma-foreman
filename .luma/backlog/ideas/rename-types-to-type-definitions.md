---
type: luma/idea
title: Rename _types/ to type_definitions/
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5]
horizon: next
scope: project
stage: draft
---

# Rename `_types/` to `type_definitions/`

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
