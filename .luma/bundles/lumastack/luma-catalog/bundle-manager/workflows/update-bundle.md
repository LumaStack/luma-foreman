---
type: workflow
title: Update a bundle
description: Change a bundle's contents and version it correctly. Use when editing, extending, or fixing an existing bundle.
---

# Update a bundle

## 1. Make the change

Follow [[organizing-a-bundle]] for where things go. Two edits deserve a pause:

- **Moving a document between directories changes its Document ID** and breaks
  inbound links. Fix them in the same commit.
- **Renaming or removing a document** is breaking for anyone who linked to it.

## 2. Version it

Semantic versioning, and the version is a **promise about what upgrading costs**
rather than a signal of how significant the work felt.

| bump | when |
| --- | --- |
| **major** | an adopter doing nothing has to act |
| **minor** | new content, existing use unaffected |
| **patch** | corrections and clarifications |

Breaking, for a bundle, means: a document removed or renamed, a Type Definition
gaining a mandatory field, an existing field's obligation strengthened, or a
document gaining or losing a `matches` when it had one, or not.

Below `1.0.0` a breaking change **may** ship as a patch. Say so where you record
it, or it reads as a mistake later.

## 3. Remember nobody has it yet

Adopters hold **vendored copies**. Publishing changes nothing for them until
they re-adopt, which is the guarantee the model exists to provide — nothing
changes underneath a project.

The consequence: **you cannot fix an adopter's copy by publishing.** A serious
defect needs the version bumped *and* the adopters told.

## 4. Audit

Run [[audit-bundle]] before publishing. Most breakage arrives through
edits, not through creation.
