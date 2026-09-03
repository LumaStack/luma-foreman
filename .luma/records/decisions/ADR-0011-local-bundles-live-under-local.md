---
type: decision
title: Local bundles live under local/
decided: 2026-09-02
lifecycle: draft
---

# ADR-0011: Local bundles live under local/

A bundle written in this project, not yet published anywhere, lives at
`.luma/bundles/local/<bundle-name>/`. `local` is a reserved namespace no
catalog may derive or declare. Publication moves the bundle to its real
namespace, and the move is the moment identity is acquired.

## Problem

A vendored bundle's namespace derives from its catalog's address, so its
full ID says where it came from just by being read. A bundle written
locally has no catalog to derive from, and the question — what namespace
does it take? — was recorded open. Deriving from the project's own repo
address was the standing lean, and it has two defects: it fails in a
repository with no remote, which foreman's standalone guarantee protects,
and it gives an unpublished bundle an ID that reads as published.

## Decision

**`local/<bundle-name>`, flat.** No configuration, no derivation, works in
a bare repository.

**`local` is reserved.** No catalog may publish under it — the same
anti-squatting shape as derived namespaces, made absolute — so collision
with a published bundle is impossible rather than unlikely.

**Publication is the rename.** Promoting a bundle moves it from `local/`
to `<namespace>/<bundle-name>` under its catalog's derived namespace;
[[migrate-bundle]] owns the mechanics — the move, repointing inbound
wikilinks, the audit — plus the manifest and index updates. A dedicated
command can follow if the procedure proves fiddly.

**Recommended, with teeth later.** Nothing refuses a local bundle placed
elsewhere — the estate is permissive by default — but `inspect` may
eventually notice a bundle that is neither under `local/` nor recorded
with custody, which is the stray-detection shape this design already uses.

## Why

The name states the one true fact about an unpublished bundle: it has no
published identity. Nothing outside the project can cite `local/x`,
because the name announces it is unpublished — cross-project references to
unpublished bundles become impossible by construction. And the path now
distinguishes local from vendored by shape, the way the manifest's bare
entries already do, instead of by a lookup.

## Alternatives

**Derive from the project's repo address** — rejected: fails with no
remote, and pretends to a published identity before one exists. Every
scheme renames at publication anyway (a repo-derived ID still changes to
the catalog's namespace), so hiding the rename bought nothing.

**A bare single-segment name as the local marker** — rejected: it is a
convention only a reader who knows it can see, where `local/` is a word.

## Re-open when

A project needs more than one tier of unpublished bundle — staged for one
catalog versus another, say — and a flat `local/` cannot express it.
