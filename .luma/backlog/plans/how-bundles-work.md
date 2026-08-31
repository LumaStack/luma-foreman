---
type: document
title: How bundles work
description: The end-to-end design for bundles — what one is, how it arrives, what records it, and how it reaches an agent. Written forward, entry by entry, rather than derived from what exists.
lifecycle: draft
created: { by: human:benlinton, at: 2026-08-30T00:00:00Z }
modified: { by: agent:claude-opus-5, at: 2026-08-30T00:00:00Z }
---

# How bundles work

**Written forward.** What exists today is a prototype that grew four artifacts
answering overlapping questions — a manifest, a routing table, a project ring
and a per-bundle ring — and the way out is not to reconcile them. This document
designs the thing that should exist and lets the prototype be measured against
it, never the reverse.

**Built entry by entry.** Each section is settled before the next one starts. An
entry states what it is, what problems it has to solve, and only then what
fields or files that implies — in that order, because deriving fields from a
mock-up is how a design acquires columns nobody can justify later.

**Earlier plans are raw material, not sources.** *How bundles compose* worked
through capabilities, `needs` and `provides`; *knowledge delivery* and *hook
delivery* worked through transports. Whatever survives from them gets restated
in an entry here and argued on its own. Nothing is carried forward by citation.

## Settled before this document opened

- **A bundle is a distribution unit, not a relevance unit.** It is versioned,
  published, copied and recorded. What an agent reads is decided per document,
  never per bundle.

---

# Entry 1 — `.luma/bundles/manifest.toml`

**Every bundle this project has, vendored or written here.** It is the project's
statement of what it carries, which is a different thing from what happens to be
on disk.

## Mock-up

```toml
# Every bundle this project has.
#
# Authored — `luma-foreman get` adds rows and fills in where a copy came from.
# A row with source/commit/checksum is a copy of something upstream: change it
# there and take it again, never here. A row without them was written in this
# repository, and its own BUNDLE.md is the truth.

["lumastack/luma-catalog/git-secrets"]
version  = "0.5.1"
source   = "https://github.com/LumaStack/luma-catalog"
commit   = "8ec0cce285bb27f0b6c58bacb62d37bd62a702ee"
checksum = "sha256:2eb6115374ff3202da0fccc0452e044f6011dde17948bef76df2ab56243ac72d"

["lumastack/luma-catalog/review-sweeps"]
version  = "0.28.0"
source   = "https://github.com/LumaStack/luma-catalog"
commit   = "0ea2719dcbb01b129fd563aa3003b5d83e379c46"
checksum = "sha256:31c0764829539698d6522a31afa06291fc349c0ead1be6591b53e6842fed26b0"

# Taken from a catalog checkout on disk rather than a remote. Still a copy.
["acme/house-rules/incident-response"]
version  = "1.2.0"
source   = "../catalogs/house-rules"
commit   = "4f1c9ab0d2e8a77315b0c6d9e4f2a1b8c3d5e6f7"
checksum = "sha256:9c1e..."

# Written here. Membership is the whole of the row — version lives in its own
# BUNDLE.md, and there is no upstream to point at or verify against.
["lumastack/luma-foreman/adoption-internals"]
```

## What the mock-up is asserting

**The row's existence is the fact.** A directory with a `BUNDLE.md` is
indistinguishable from one that wandered in; only a manifest can say which
belong. That is the capability a directory walk structurally cannot provide —
whatever a walk finds is by definition what is there, so it can never report a
stray.

**The two kinds are distinguished by shape, not by a flag.** Presence of
`source`/`commit`/`checksum` marks a copy. No `local = true`, because a flag
that restates what the other columns already show is a second copy of one fact.

**A local row carries no version.** You are the author, the `BUNDLE.md` is the
truth, and duplicating it into a table produces two numbers that will eventually
disagree.

**The file is authored, not generated.** `get` edits it the way
`npm install --save` edits `package.json`. It carries no *do not edit* banner.

## Open — what it has to solve

Not yet settled. The fields above are a starting shape, not a proposal; each one
survives only if a problem below needs it.

1. **Membership.** What is part of this project — so a stray directory and a
   missing one are both reportable.
2. **Provenance.** Where a copy came from, and at what point in that source's
   history.
3. **Integrity.** Whether a copy has been changed here since it landed.
4. **Currency.** Whether something newer exists upstream.
5. **Divergence.** Whether an edit to a copy is *intentional*, so the integrity
   check stops reporting it. See
   [a bundle should be able to diverge](../ideas/a-bundle-should-be-able-to-diverge.md).
6. **Reproducibility.** Whether a copy could be re-fetched exactly — and whether
   that is a promise worth making, given nothing restores from this file.
7. **Identity for local bundles.** What namespace a project-authored bundle
   takes when it has no catalog behind it.
8. **Level.** Bundles declare `consumers: [project, organization]`. Whether
   adoption at a level records anything here.
9. **Enablement.** Whether a bundle can be present and switched off.
10. **Precedence.** Whether this file decides anything when two bundles collide.

## Open — placement

`.luma/bundles/manifest.toml` assumes the directory stays `bundles/`. If the
knowledge tree is renamed the file moves with it and the name still holds.
