---
type: policy
title: Where a bundle belongs
description: Which catalog a bundle goes in — universal, an organization's private one, or the project it was written in — and how it moves between them.
matches:
  - topic: deciding which catalog a bundle belongs in
---

# Where a bundle belongs

Three homes, and the honest default is the nearest one.

| home | for | who sees it |
| --- | --- | --- |
| **the project** | written here, useful here, nowhere else yet | this repository |
| **an organization's catalog** | several of your projects want it | your organization |
| **the universal catalog** | useful to an organization sharing nothing with yours | everyone |

## Start where it was written

A bundle is born in the project that needed it. That is not a formality — a
bundle written for a general audience before anyone has used it once is designed
against an imagined consumer, and it shows.

**Promote when a second consumer actually appears**, not when you anticipate
one. A bundle serving one project is a project bundle no matter how general it
looks.

## Promote one step at a time

```
project  ──▶  organization's catalog  ──▶  universal catalog
```

**Do not skip the middle.** An organization's catalog is where vouching happens
— somebody with context said this is good enough for other people's projects. A
bundle going straight from one repository to the universal catalog has been
vouched for by nobody.

## The test for the universal catalog

**Would this help an organization that shares nothing with yours?**

Not *is it general* — almost anything can be phrased generally. Whether it
survives contact with a company that has different tooling, different scale, and
none of your history.

Anything naming your customers, your systems, your people, or your internal
services belongs in your own catalog, permanently. Generalising it usually means
deleting the part that made it useful.

## What promotion actually is

A directory copy and a namespace rewrite. Nothing else — no dependency to
update, no manifest to edit, because bundles depend on nothing.

```
acme-web/deploy   ──▶   acme/deploy   ──▶   luma/deploy
```

**It is deliberately two steps.** Promoting copies the bundle *out*. The
originating project then separately adopts the promoted copy and drops its
local one. Promotion that silently rewrote the source project would break the
guarantee the whole model rests on — that nothing changes underneath a project
without it asking.

## Nothing is forked

An organization's catalog is its own repository that names an upstream. It is
never a copy of the universal catalog that drifts.

If adopting something appears to require forking a catalog, that is a defect
worth reporting rather than a workflow to follow.

## Reach is where you found it

A bundle declares nothing about its own origin. It is universal because it sits
in the universal catalog — so promotion is a directory move with nothing to
edit, and a bundle cannot misstate how far it travels.

What *does* travel with it is the **namespace**: `luma/deploy` still says where
it came from after it has been vendored into a project alongside bundles from
elsewhere.
