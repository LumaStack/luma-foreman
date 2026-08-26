---
type: decision
title: Adoption copies a directory and never resolves anything
decided: 2026-08-23
lifecycle_status: provisional
reopen_trigger: Bundle dependencies are adopted as a design, at which point something has to decide what a bundle's declared needs mean at adopt time.
---

# ADR-0002: Adoption copies a directory and never resolves anything

## Summary

`luma-foreman get` copies one bundle directory and writes a receipt. It
resolves no graph, fetches nothing later, and installs nothing.

## Problem

Taking a bundle from a catalog looks like package installation, and the tools
that look like this all grew resolvers: a dependency graph, version ranges, a
lockfile, a cache, and a restore step. Building the small version of that now
would be the normal thing to do.

## Decision

**Adoption is `cp -r` plus a record.** The bundle lands in
`.luma/bundles/<org>/<name>/` and `adopted.toml` gains four values: version,
source, the catalog commit, and a checksum of exactly what landed.

**The copy is committed** with the rest of the project. Nothing is ever restored
from `adopted.toml` — it is not a lockfile, though it resembles one.

**Two refusals rather than an overwrite.** A vendored copy that was edited
locally is never silently replaced. A bundle declaring no version cannot be
adopted at all.

## Why

**Bundles depend on nothing, so there is no graph.** That is a property of the
bundle model rather than a simplification of it — self-containment is what makes
promotion between catalogs a directory copy, and a resolver would be machinery
for a relationship the format does not have.

**Resolution is more dangerous for content than for code.** Two versions of a
library conflict and something crashes. Two versions of a policy conflict and
**nothing happens** — both are readable, both are plausible, and nobody finds
out which one an agent followed.

**Committing beats caching, and the difference is reproducibility.** Claude Code
plugins cache to a home directory and are not committed, so a fresh clone with
no network does not reproduce. The knowledge a project runs on should survive
being handed to somebody on a plane.

**The checksum is what makes adoption mean anything.** Without it this is a copy
with a comment attached, and a locally edited bundle is indistinguishable from
an untouched one. With it, the three failure states are all detectable — edited,
missing, and never written anywhere an agent reads.

**Refusing to overwrite an edit is not politeness.** The edit is somebody's work
and the next `adopt` is where it would silently disappear, along with any chance
of it reaching upstream.

## Alternatives

**A resolver with version ranges.** Rejected: nothing declares a dependency, and
the README's promise of no build step and nothing to install probably cannot
survive semver range resolution.

**Fetch at use time rather than vendoring.** Rejected: it makes a project's
behaviour depend on a network and on a catalog nobody controls, and a bundle
that changes underneath a project changes it silently.

**Record the version only, no checksum.** Rejected: it detects an out-of-date
copy and not an edited one, and the edited one is the failure that produces
wrong behaviour rather than merely old behaviour.

## Tradeoffs

**Pros**
- Reproducible offline, and reviewable in a diff like everything else.
- No solver, no lockfile, no cache to invalidate.
- Every failure state has a name and a check.

**Cons**
- The repository grows by the size of everything adopted.
- Upgrading is per bundle and manual; nothing tells a project a newer version
  exists, because that needs the catalog and `inspect` runs offline.
- A bundle that genuinely needs another one has no way to say so, and the
  adopter finds out by reading.

## Assumptions

That bundles stay dependency-free. `luma-leader/docs/bundle-dependencies.md`
drafts the reversal, and adopting that draft is the re-open condition.

## References

The layout and `adopted.toml` shape come from the `luma/luma-layout` bundle,
which specifies both. `docs/scope.md` carries the wider argument about declaring
and detecting dependencies rather than solving them.
