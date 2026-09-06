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

## Putting it in `type:` itself

The candidate spellings, and what decides between them:

| | |
| --- | --- |
| `type: idea@1.0` | **the strongest.** `@` is a YAML reserved indicator only at the *start* of a plain scalar, so this is safe. And *name at version* reads instantly from npm, Go modules and pip |
| `type: idea:1.0` | legal — a colon not followed by a space stays in the scalar — but colon is the structural separator, so a line carries two of them and `type: idea: 1.0` is a parse error |
| `type: idea (1.0)` | two tokens where readers expect one, whitespace-significant, parens to strip. The most work for a parser that is a deliberate minimal subset |
| `type: idea#1.0` | **rule out.** `#` opens a comment when preceded by whitespace, so `type: idea #1.0` silently becomes `idea` and the version vanishes with no error |

Namespaced types already carry a `/` — `luma/idea@1.0` — and none of these
collide with it.

## The bootstrap problem, which probably decides more than the syntax

**Putting a version inside `type:` is the one change the estate's own technique
cannot absorb.** `change-a-shared-type` says *"Add the new form; keep the old
one. Both valid"* — that works for any field a reader can fall back on, and not
for the field every reader dispatches on. `luma/idea@1.0` is an unknown type to
every tool shipping today.

In foreman alone that is `bundle_index.py:105` (`== "procedure"`) and
`apply.py:175` (`d.type == kind`), across 236 documents in 12 type values, and
foreman is one of several tools that read this.

**Which suggests the order matters more than the spelling.** Teach readers to
split on the separator and compare the name before anything writes a version.
That change is small, ships harmlessly, and is field-tolerance applied to the
*value* rather than to the field — after which versioned and unversioned forms
coexist exactly as the procedure intends.

**The alternative is a sibling field** — `type_version: 1.0` — which old
readers ignore for free, since unknown frontmatter keys are already ignored. It
rolls out with no sequencing at all. What it buys in safety it pays for in
drift: a sibling can go stale against the type it describes, and an in-band
version cannot be separated from what it versions.

## Half of this already exists, which narrows it

**Type definitions already carry a version, and bundles already record which
one they took.** `_types/idea.md` declares `version: "0.1.0"`, and every
vendored copy carries:

```yaml
vendored_from:
  resource: https://github.com/LumaStack/luma-catalog
  version: "0.1.0"          # the type's own version, not the bundle's
  at: 2026-08-23
```

`luma-types` `0.3.0` moved to exactly this deliberately, after the failure it
exists to prevent had already happened: *"a vendored `luma/catalog` recorded
`0.1.0` while the bundle read `0.2.0`"*.

**So this is not inventing versioning — it is extending it one hop.** Types are
versioned, and bundles say which version they hold. **Documents say nothing**,
and that is the entire remaining gap. A `type_version` on a document would cite
the number the type definition already declares, so there is nothing new to
mint and nothing to keep in step by hand.

It also makes the folder idea land cleanly: migrations sit beside a schema that
already has versions to key them on.

## `type_version` and `lkf_version` are not alternatives

They answer different questions, and picking one is really deciding which
failure is being prevented:

| | |
| --- | --- |
| `type_version` | this document was written against `luma/idea` at `0.1.0`. Catches a field that moved, an enum that gained a value, a key that was renamed |
| `lkf_version` | this document was written against the *format* — frontmatter grammar, `matches` syntax, what a Document is. Catches a change beneath every type at once |

They move at different rates, which is the argument for not conflating them —
the format is at `v0.0.x` and individual types are at `0.1.0`, `0.2.0`, `0.3.0`
independently. **They also differ in granularity**: a type version is per
vendored copy, and a format version is estate-wide, so a bundle could honestly
carry the second and only a document can carry the first.

Both may eventually be wanted. Only one is needed to make a document
migratable, and it is `type_version`.

## Open

**What carries the version.** In-band on `type:`, a sibling field, or one line
per bundle declaring what it was built against — one line per bundle rather
than one per document, at the cost of granularity.

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
