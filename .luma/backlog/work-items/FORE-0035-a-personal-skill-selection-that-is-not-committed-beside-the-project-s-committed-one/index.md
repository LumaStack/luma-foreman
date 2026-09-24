---
type: work-item
key: FORE-0035
title: A personal skill selection that is not committed, beside the project's committed one
workflow_status: captured
rank: 010.0340.000
kind: idea
stage: draft
created: {by: 'human:luma-founder', at: '2026-08-21T00:00:00'}
description: Point at the workflows you want loaded as skills and have foreman project them into the project — and be able to say that some of that selection belongs to the project and is committed, while some belongs to you and is not. A project's skill set and an individual's are not the same set, and only one of them should travel with a clone. Today there is nowhere for the second to live.
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:44Z'}
---

# A personal skill selection that is not committed, beside the project's committed one

Point at the workflows you want loaded as skills and have foreman project them
into the project — and be able to say that some of that selection belongs to the
project and is committed, while some belongs to you and is not.

## The problem it addresses

A project's skill set and an individual's are not the same set, and only one of
them should travel with a clone. Today there is nowhere for the second to live.

**`.luma/` cannot hold it.** The `luma-layout` bundle states the invariant
plainly — *"Everything in `.luma/` is committed, no exceptions"* — because if
uncommitted files could live there, two agents on two machines would read
different rules for the same repository. That is the right invariant and this
idea must not weaken it.

So a personal selection needs the machine-local tier, the way `agent-permissions`
policy already lives under `~/.config/luma/luma-foreman/` keyed by repository
root. What is undecided is how a machine-local selection and a committed one
compose at write time.

## Notes

Captured 2026-08-21, during the migration of `docs/IDEAS.md`.

**The writing-out half is a separate unbuilt thing and is not what this idea is
for.** *Selecting at write time which subset of adopted content gets written —
including by symlink* is unbuilt because **nothing yet decides the subset**.
This file is titled on the part that has no home: what the subset is decided
*from*.

**Mid-session swapping is blocked, and not by us.** Agent Skills' progressive
disclosure loads every skill's name and description at startup and the body on
description match, **with no hook for *conditions changed, drop these***.
Between sessions is achievable; during one is not, in any harness. **Selecting
at write time gets most of the value**, which is the reason to build that and
stop. Worth knowing before anyone promises "change them quickly".

*Both absorbed from `docs/scope.md` when that document was scattered on
2026-08-29; this entry had cited it for each.*

**The same shape appears twice.** The open question left by `agent-permissions`
— whether foreman writes *committed* per-project Claude Code settings as a shared
floor, with the machine-local layer as overrides on top — is this same pattern
applied to permissions instead of skills. A committed team floor plus a personal
uncommitted layer may want one answer serving both rather than two.

## Related work

- Born from the idea it replaces: [`personal-skill-selection-not-committed`](../../ideas/personal-skill-selection-not-committed.md)
