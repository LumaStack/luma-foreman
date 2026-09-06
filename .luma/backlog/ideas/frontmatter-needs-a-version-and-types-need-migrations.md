---
type: luma/idea
title: Frontmatter needs a version, and a type definition needs migrations
created: { by: human:benlinton, at: 2026-09-06T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# Frontmatter needs a version, and a type definition needs migrations

**Nothing in a document's frontmatter says which version of its type it was
written against**, so as type definitions change there is no way to know what a
given file needs doing to it. A reader can tell a valid document from an
invalid one and cannot tell an old one from a wrong one.

**And a type definition may want to be a directory rather than a file** —
carrying its schema alongside the migrations that move a document from each
earlier version to the current one.

## Why it bites

Every change to a type today is absorbed by readers being tolerant: accepting
the old spelling beside the new one, indefinitely, because nothing can identify
which documents still need converting. The tolerances accumulate, and the only
way to remove one is to believe that every document everywhere has been
rewritten — which nothing can check.

A version on the document turns that from a belief into a query.

## The shape

```
_types/idea/
  schema.md               what an idea is, at the current version
  migrations/
    0.1.0-to-0.2.0.md     what changed, and what to do to a document
```

Whether migrations are prose an agent follows or something executable is open,
and the answer probably differs by tool.

## Open

**What carries the version.** A field on every document is the obvious answer
and the most invasive — it touches every file the estate has. Whether a bundle
declaring the type versions it was built against would do instead is worth
weighing, since that is one line per bundle rather than one per document.

**Which version is recorded** — the type's, or the format's. They move at
different rates and conflating them is how a version stops meaning anything.

**Where this belongs.** The type system is `luma-knowledge-format`'s and
`lumastack/luma-catalog/luma-types`', not foreman's. Captured here because that
is where it came up, and it is cheap to move.

## Related

**`change-a-shared-type` already names this gap, and works around it.** Step 2
says outright:

> **Tools are field-tolerant rather than version-aware, and have no choice** — a
> document never records which type version it was written against, so version
> dispatch is impossible. *Read the new field, or if absent the old one* is the
> entire technique.

So the procedure's whole technique is a workaround for the missing version, and
it is honest about being one. That is the strongest argument that this is worth
doing — and also the argument against rushing it, since the workaround is
already written down and functioning.

**[[rename-types-to-type-definitions]] touches the same directory**, moving
`_types/` to `type_definitions/`. If a type definition also becomes a folder,
these two are one change to that directory rather than two, and doing them
apart means editing every bundle twice.

**[[retire-the-migration-tolerances]] would benefit, less directly than it
first appears.** Its tolerances are three specific accommodations in foreman's
code, not document type versions — but its gate is *every estate repository
migrated and re-adopted*, recorded as "believed, not confirmed". A version is
what would make that gate checkable instead of believed.
