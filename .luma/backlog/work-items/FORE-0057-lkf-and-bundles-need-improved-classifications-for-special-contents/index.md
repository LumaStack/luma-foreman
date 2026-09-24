---
type: work-item
key: FORE-0057
title: LKF and bundles need improved classifications for special contents
workflow_status: captured
rank: 010.0560.000
kind: idea
stage: draft
created: {by: 'human:luma-foundry', at: '2026-09-10T06:38:27'}
description: '`organizing-a-bundle` is categorical: frontmatter with a `type` makes it a document; no frontmatter makes it an asset; there is no third category. The list spans both sides of that line: The format removed the `concept` type in `0.0.10` — it added no fields and no consumer treated it differently from a plain `document`, which is the format''s own test for a type that has not earned its name. The directory convention survived, and `organizing-a-bundle` predicted it would.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:50Z'}
---

# LKF and bundles need improved classifications for special contents

**LKF and bundles need some improved classifications, or guidelines, for special
contents.**

---

## The list

*As proposed. Kept as written — spelling and formatting corrected, wording
untouched. Commentary is below, and deliberately not mixed in here.*

**Keepers**

- **policy** — reference that, if not followed, results in a violation
- **procedures** — generic skills, possibly will also include commands and
  workflows later on
- **templates**
- **scripts**
- **type_definitions** — maybe rename to `type_schemas`; contracts for how
  frontmatter is formatted, includes type-related migrations

**Needs evaluation, lean keeping**

- **assets** — static resources like images, videos, diagrams, etc.
- **references** — unclear if this is useful, possibly documents that are
  referenced but never surfaced
- **meta** — stuff about this bundle, maybe stuff about logs or journaling or
  config or changelog, not sure yet
- **config** — how to set up the config for this bundle, includes defaults

**Needs evaluation, lean discarding**

- **concepts** — was documents that weren't policy or procedure

**New additions**

- **sources** or **pointers** or **resources** — these will be things that we
  don't want to carry and instead we should point to, so we don't need to deal
  with the licensing. Reading documents is allowed, holding them is not.
- **migrations** — how to migrate the bundle and any scripts required for
  upgrading bundle versions, one version at a time so you can safely chain
  migrations together
- **change log** — every bundle should have a change log
- **licences** — bundles should be able to carry their own licences, and
  licences they inherited

**New additions, for consideration**

- **help**
- **guides**
- **tutorials**
- **getting started**
- **about this bundle**

---

## Commentary

*Agent commentary and prior art found while capturing. None of this modifies the
list above.*

### This is two lists, and they have different owners

`organizing-a-bundle` is categorical: **frontmatter with a `type` makes it a
document; no frontmatter makes it an asset; there is no third category.** The
list spans both sides of that line:

| | |
| --- | --- |
| **types** — the format's business | `policy`, `procedure`, `type_definition` |
| **asset directories** — the bundle layout's business | `templates/`, `scripts/`, `assets/` |

**Every "needs evaluation" item is unresolved partly because nobody has said
which axis it is on**, and that answer decides who owns it — LKF or
bundle-manager. Settling the axis first is probably the first real step.

### `concepts` is further along than it looks

The format **removed the `concept` type in `0.0.10`** — it added no fields and no
consumer treated it differently from a plain `document`, which is the format's
own test for a type that has not earned its name. The *directory* convention
survived, and `organizing-a-bundle` predicted it would.

So discarding is finishing a job rather than starting one — **unless** the five
explanatory categories are the real answer. `help`, `guides`, `getting started`
and `about this bundle` are all *prose that teaches rather than binds*, which is
exactly what `concepts/` was for. If that is right, `concepts` failed by being
**one undifferentiated bucket**, and the replacement is more granular rather
than absent — which makes it "split it" rather than "drop it", with a different
blast radius.

### Tutorials already exist

`luma/tutorial_step` and `luma/tutorial_quiz` are real types in the
`lumastack/luma-catalog/luma-types` bundle, vendored by `token-manager`, which
runs a twenty-step paced tutorial. There is also a `tutorial-workflow-maker`
bundle.

**The shape already settled on:** the tutorial lives at
`procedure/token-tutorial/` with `steps/` beneath it — a document that owns a
directory, per `organizing-a-bundle`. So **a tutorial is currently a procedure
carrying typed steps**, not a top-level category, and re-opening it means
disagreeing with a working implementation rather than filling a gap.

### `about this bundle` collides with `BUNDLE.md`

ALL CAPS names the file that speaks for its container, so `BUNDLE.md` already
*is* about this bundle — it carries the description, the contents list, the
loading rationale and the changelog. This item has to say what `BUNDLE.md` does
not cover, or it is a proposal to break `BUNDLE.md` up. The **meta** item raises
the same question from the other side.

### `change log` already exists, in a place

It is `BUNDLE.md`'s `## Version` section, and every bundle in the catalog has
one. The catalog also deliberately took changelogs *out* of `INDEX.md`. So the
live question is narrower than *every bundle should have one*: should it move
out of the manifest into its own file, and what does that fix?

### `sources` may want to be a type rather than a directory

If the point is that we do not hold the material, then what sits in the bundle
is a **pointer** — frontmatter naming the URL, the licence, and where the cache
goes. As a type that makes machine-checkable what `what-a-bundle-may-carry`
currently states only in prose: a tool could verify that a bundle carries
nothing it should not, and could warm every cache in one pass.

### `help` is ambiguous in a way the others are not

The `command-line-interface` bundle already owns help *text* — the template a
command's `--help` follows. Help *inside* a bundle is a different thing, and the
two will be confused unless the word is pinned down.

### The loading consequence

Explanatory material is the standard *do not load this by default* case, and the
three tiers — `policy` standing, `procedure` invoked, `concepts` when relevant —
exist to keep it out of every consumer's context. **Five new prose categories
multiply the places a bundle can accumulate text nobody reads.** Worth deciding
whether each earns a directory, or whether it is one tier with a `kind` field.

### Two items also have files of their own

Kept in the list above **and** split out, because each is independently
buildable and independently valuable:

- [[work-items/FORE-0056-bundles-should-carry-their-own-licences-and-licences-they-inherited]]
- [[work-items/FORE-0058-a-bundle-should-carry-migrations-one-version-at-a-time-so-they-chain]]

### Related, already filed

- [[work-items/FORE-0016-nobody-has-a-format-for-knowledge-that-is-not-a-procedure]] — *nobody has a format for
  knowledge that is not a procedure.* This idea is an attempt at the answer;
  that one is the gap it answers.
- [[work-items/FORE-0062-rename-types-to-type-definitions]] — live at `horizon: next`, and **in
  tension with `type_schemas`**: it argues the directory should be named for the
  type it holds, and rejects `lkf_types`/`format_types`. If the type is renamed,
  its conclusion becomes `type_schemas/`. Nobody acting on that idea would
  currently see this.
- [[work-items/FORE-0064-frontmatter-needs-a-version-and-a-type-definition-needs-migrations]] — a *different*
  migration from the one in the list: a document's frontmatter across type
  versions, rather than a bundle across its own versions.

## Related work

- Born from the idea it replaces: [`classify-bundle-contents`](../../ideas/classify-bundle-contents.md)
