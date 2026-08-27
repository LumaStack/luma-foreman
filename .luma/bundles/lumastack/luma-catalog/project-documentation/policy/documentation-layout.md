---
type: policy
title: Where documentation lives
description: Prose goes in docs/. What stays at the repository root and why, and which documents this bundle deliberately does not own.
matches:
  - path: "docs/**"
  - topic: deciding where a document belongs
---

# Where documentation lives

**Prose goes in `docs/`.** Everything else at the root is there because
something looks for it there.

```
README.md          the front door
LICENSE            legal, and tooling reads it
CONTRIBUTING.md    forges surface it when someone opens a pull request
SECURITY.md        forges surface it as the reporting channel
docs/              everything else
.luma/             luma's own directory — not documentation, see below
```

## Why `docs/` rather than the root

A repository root is contested space: source, tests, manifests, continuous
integration config, tool dotfiles. Every prose file added there competes with
them for a reader's attention, and a root with fourteen markdown files buries
the four that matter.

**The exceptions earn their place mechanically, not aesthetically.** `README.md`
is rendered by every forge on the landing page. `LICENSE` is parsed by licence
detectors and package tooling. `CONTRIBUTING.md` and `SECURITY.md` are surfaced
by forges at the moment they are relevant — opening a pull request, reporting a
vulnerability.

Move one of those into `docs/` and it stops working. Leave anything else at the
root and it is a preference, not a requirement.

*Forges also accept these in a `.github/` directory or equivalent. That works,
and it trades discoverability for a tidier root — a contributor browsing the
tree finds `CONTRIBUTING.md` at the root without knowing to look in a hidden
directory.*

## `docs/` is flat until it hurts

Do not build a directory tree in advance. A `docs/` with six files needs no
structure, and a hierarchy imposed early is one everybody navigates around.

When it does grow, split by **what the reader is trying to do** rather than by
subject — the [Diátaxis](https://diataxis.fr) split of tutorial, how-to,
reference and explanation is the strongest available answer and worth reading
once before inventing your own.

## What this bundle does not own

Documentation is not the only prose in a repository, and several kinds belong to
somebody else. **Naming them here is deliberate**: a reader should be able to
tell that an omission is a boundary rather than a gap.

| | owned by | why not here |
| --- | --- | --- |
| `CHANGELOG.md` | the release bundle | its format follows from how versions are cut, not from how prose is written |
| decision records | the decision-records bundle | a record of what happened, with its own contract and lifecycle |
| audit and log records | their own record bundles | append-only, dated, machine-written |
| everything in `.luma/` | the luma-layout bundle | that directory is how the project is run, not what it publishes |
| `AGENTS.md`, `CLAUDE.md` | nothing — they are generated | written from `.luma/`, disposable, never edited by hand |

**These bundles are named, not depended on.** Nothing here breaks if the release
bundle is not adopted; you simply have no policy about your changelog. A bundle
may point at another to mark a boundary — it may never require one to be
present.

## Records are not documentation

The distinction is worth stating because it decides where a file goes.

**Documentation describes what is true now** and is edited when that changes. A
record says **what happened at a moment** and is never edited afterwards.

An architecture document is documentation: it describes the current shape, and
when the shape changes, so does the document. A decision record is a record: it
captures a position taken on a date, and if the position changes you write a new
record rather than editing the old one.

If you find yourself wanting to update a file to keep it accurate, it is
documentation. If updating it would be falsifying history, it is a record and
belongs in `.luma/records/`.
