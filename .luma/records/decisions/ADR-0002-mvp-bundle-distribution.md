---
type: decision
title: MVP bundle distribution
decided: 2026-08-23
stage: draft
---

# ADR-0002: MVP bundle distribution

`luma-foreman get` copies one bundle directory and writes a receipt. It
resolves no graph, fetches nothing later, and typically installs nothing.

## Problem

Taking a bundle from a catalog looks like package installation, and the tools
that look like this all grew resolvers: a dependency graph, version ranges, a
lockfile, a cache, and a restore step. Building the small version of that now
would be the normal thing to do.

## Decision

**`get` is `cp -r` plus a record.** The bundle lands in
`.luma/bundles/<org>/<name>/` and the manifest gains: version, source,
the source's commit, and a checksum of exactly what landed.

**The copy is committed** with the rest of the project.

**Refuse rather than overwrite.** A vendored copy that was edited
locally is never silently replaced; it should fail loudly.

## Why

**Resolution is more dangerous for content than for code.** Two versions of a
library conflict and something crashes. Two versions of a policy conflict and
**nothing happens** — both are readable, both are plausible, and nobody finds
out which one an agent followed.

**Committing beats caching, and the difference is reproducibility.** Claude Code
plugins cache to a home directory and are not committed, so a fresh clone with
no network does not reproduce. The knowledge a project runs on should survive
being handed to somebody on a plane.

**The checksum is what builds trust.** Without it this is a copy
with a comment attached, and a locally edited bundle is indistinguishable from
an untouched one. With it, the three failure states are all detectable — edited,
missing, and never written anywhere an agent reads.

**Refusing to overwrite an edit is not politeness.** The edit is somebody's work
and the next `get` is where it would silently disappear, along with any chance
of it reaching upstream.

## Alternatives

**Fetch at use time rather than vendoring.** Rejected: it makes a project's
behaviour depend on a network and on a catalog nobody controls, and a bundle
that changes underneath a project changes it silently.

**Record the version only, no checksum.** Rejected: it detects an out-of-date
copy and not an edited one, and the edited one is the failure that produces
wrong behaviour rather than merely old behaviour.

## Why resolution is more dangerous for content than for code

Two versions of a library conflict and something crashes. Two versions of a
policy conflict and nothing happens. The failure is silent, and a resolver
that quietly reconciles them makes it more silent still.

**Declaring and detecting, rather than solving**, keeps real dependencies
without a solver and keeps a conflict visible instead of reconciled. That is
the shape any reversal should take before it takes any other.
