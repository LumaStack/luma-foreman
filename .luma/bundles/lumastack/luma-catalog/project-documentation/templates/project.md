# Project descriptor template

Copy the block to `.luma/PROJECT.md`. **Copy the block, not this file.**

**One sentence is a complete descriptor.** Everything past the frontmatter is
optional and most repositories should leave it out.

## The minimum, and usually the whole thing

```yaml
---
type: luma/project
title: acme-web
description: The customer-facing storefront — anything a buyer sees, checkout, or the payment integration.
---
```

**`description` answers one question: when should somebody open this
repository?** Not what it is built with, not what it does internally.

| | |
| --- | --- |
| ✗ | *"Next.js application with a Postgres backend."* |
| ✓ | *"The customer-facing storefront — anything a buyer sees, checkout, or the payment integration."* |

**The test: could somebody choose between this repository and four others using
only this sentence?** If two would read the same, it is not specific enough.

## With boundaries, where somebody has decided them

```yaml
---
type: luma/project
title: acme-web
description: The customer-facing storefront — anything a buyer sees, checkout, or the payment integration.
owns: [storefront, checkout, payment-integration]
must_not_own: [inventory levels, pricing rules]
modified: { by: human:fsmith, at: 2026-08-20T09:00:00Z }
---
```

**Only what was actually decided.** Invented boundaries are read as settled, and
a wrong claim looks exactly like a right one. Leave both out rather than
guessing — absent means nobody has said, which is findable.

**`must_not_own` is the more valuable half.** Everything owns something; an
explicit *this is not ours* is a boundary somebody argued about, and it is what
stops a project absorbing a neighbour's job over two years.

## Body, only if the sentence did not cover it

```markdown
## Why it exists

<One paragraph. The problem it solves, and what would be true if it did
not exist. Not how it works.>
```

**A heading with a restatement under it is worse than no heading** — it teaches
the next reader that this file is padding, and then nobody maintains it.

## What never goes in it

The URL, the language, the visibility, the default branch, when it was last
pushed, how to build or run it.

**Whoever is reading this is holding the repository**, so every one of those is
knowable in seconds — and a copy of a moving fact is a second answer that will
eventually disagree with the first. A repository that names its own location is
wrong the moment it is forked, mirrored, or transferred.
