# Bundle manifest template

Copy the block below into `<bundle>/BUNDLE.md` and fill it in. **Copy the block,
not this file** — this file deliberately has no frontmatter of its own, because
a template carrying `type: bundle` would be a second manifest inside this
bundle, and every tool reading it would believe that.

```yaml
---
type: bundle
version: 0.1.0
published: YYYY-MM-DD
consumers: [project]
entry_point: workflows/CHANGE-ME
description: One line — what this holds and who it is for.
---
```

- **`version`** — `0.1.0` for anything used in one place or none. `1.0.0`
  claims the shape has stopped moving.
- **`consumers`** — `project`, `organization`, or both. Both when the same
  content is wanted at either level by different adopters.
- **`entry_point`** — the full Document ID, e.g. `workflows/create-bundle`.
- **`description`** — what a consumer reads when deciding whether to adopt.

## Body

```markdown
# Bundle Name

Why this exists, in a paragraph. What goes wrong without it.

## What is here

- [[the-entry-point]] — the workflow. Start here.
- [[a-policy]] — what this obliges.

## When these apply

Which documents bind, and when each one comes up. **Nothing here says when a
document loads** — that is computed from what it obliges and when it applies.

Keep an eye on any policy declaring `matches: always`: it loads into every
session of every adopter, forever. That is the one expensive outcome, and it now
has to be asked for — a policy that says nothing is available on request, so
nobody buys the cost by forgetting a field.

## Version

Why this number.
```

The *What is here* section links each document with one line on why to open it.
It is not an inventory — the directory already lists the files.
