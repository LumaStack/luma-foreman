---
type: luma/idea
title: bundle index can regenerate a vendored copy adopted from a registered catalog
created: { by: agent:claude-opus-5, at: 2026-09-06T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: next
scope: project
stage: draft
---

# `bundle index` can regenerate a vendored copy adopted from a registered catalog

**`vendored_here` asks whether a bundle is somebody else's copy by testing one
field, and since the registry landed that field is empty for the common case.**
The guard it powers stops `bundle index` regenerating an index a catalog
froze — so where it fails, the drift it exists to prevent is exactly what
happens.

`src/foreman/bundle_index.py:181`:

```python
entry = adoption.read(project).get(bundle_id)
if entry is not None and entry.source:
    return bundle_id
```

`src/foreman/get.py:222`, writing the receipt:

```python
source="" if registered_as else catalog.source,
```

**A bundle taken from a registered catalog records `catalog:` and leaves
`source:` empty**, by design — ADR-0012 made receipts name-indirect so a moved
catalog is one config line rather than every receipt going stale. So
`entry.source` is falsy, `vendored_here` returns `None`, and the copy is
treated as local.

## Why the tests do not catch it

`tests/bundle-index-test.sh` builds its local case as `org/local` — it
exercises the *shape* rule, that an entry with no custody sublines is a bundle
written here. It never builds a name-indirect receipt, so the one arrangement
that breaks this has no fixture.

## The fix, and the reason to look wider

`entry.source or entry.catalog`, which is what **every other local-versus-
vendored test in the codebase already uses** — `outdated.py` and `bundle show`
both check both fields. This one site is the odd one out, which is the tell:
the predicate is duplicated at four sites and only three were updated when the
registry landed.

**Worth extracting rather than patching in place.** A fourth copy of *is this
vendored* is what produced the bug, and the same reasoning that moved
`adoption.resolve` out of `bundle.py` applies — two consumers disagreeing about
one question is the failure that is hardest to see.

## Notes

Found while building `publish`, and recorded until now only in an appendix to
`.luma/backlog/plans/bundle-publish.md`, where nothing tends it.
