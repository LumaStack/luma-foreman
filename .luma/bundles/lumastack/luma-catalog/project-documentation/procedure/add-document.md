---
type: procedure
title: Add a document
description: Decide whether a document is needed, which one it is, and where it goes. Use when writing anything new, or when a document is outgrowing the file it is in.
---

# Add a document

## 1. Check the condition has actually fired

Every document in [[which-document]] carries the condition that earns it — a
question asked twice, somebody confused once, a stranger with nowhere to report.

**If no condition has fired, do not write it.** A document written in
anticipation is one nobody needed and everybody now maintains, and it will be
stale before it is read.

The exception is `README.md`, which every repository has from the first commit.

## 2. Check it is not somebody else's

Four things look like documentation and are owned elsewhere:

- **`CHANGELOG.md`** — the release bundle
- **decision records** — `decision-records`, in `.luma/records/decisions/`
- **audit and log records** — their own bundles, also under `.luma/records/`
- **`AGENTS.md`, `CLAUDE.md`** — generated, never authored

**The test between a document and a record:** if you would want to update it to
keep it accurate, it is documentation. If updating it would falsify history, it
is a record.

## 3. Pick one kind, not two

Tutorial, how-to, reference, or explanation — see [[which-document]]. A document
serving two of these serves neither, and the usual failure is a how-to that
keeps stopping to explain.

If the thing you are writing wants to be two, that is two documents.

## 4. Put it where it goes

`docs/`, unless something mechanically requires the root — see
[[documentation-layout]]. Four files earn the root and the rest is preference.

Do not create directories under `docs/` in advance. Flat until it hurts.

## 5. Write it

For a README, [the template](../templates/readme.md) and [[readme]].

For anything else, the shape follows the kind you picked in step 3. Start with
what a reader needs first rather than with what you know best — those are
rarely the same, and the second produces documents that make sense only to
whoever wrote them.

## 6. Link it from somewhere

**A document nothing links to will not be found.** The README is the front door;
if the new document matters to someone arriving, it belongs in the README's
links section. If it matters only to someone already deep in the project, link
it from wherever they will be.

An unlinked document in `docs/` is indistinguishable from an abandoned one.

## 7. Say what it replaced

If this document takes over from a README section that had outgrown itself, or
from another document, **delete the old text in the same commit**.

Two documents covering one subject drift, and a reader who finds the stale one
has no way to know. The history keeps whatever you removed.
