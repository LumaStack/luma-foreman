---
type: idea
title: A personal skill selection that is not committed, beside the project's committed one
created: { by: human:benlinton, at: 2026-08-21T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
lifecycle_status: draft
---

# A personal skill selection that is not committed, beside the project's committed one

Point at the workflows you want loaded as skills and have foreman project them
into the project — and be able to say that some of that selection belongs to the
project and is committed, while some belongs to you and is not.

## The problem it addresses

A project's skill set and an individual's are not the same set, and only one of
them should travel with a clone. Today there is nowhere for the second to live.

**`.luma/` cannot hold it.** The `luma/luma-layout` bundle states the invariant
plainly — *"Everything in `.luma/` is committed, no exceptions"* — because if
uncommitted files could live there, two agents on two machines would read
different rules for the same repository. That is the right invariant and this
idea must not weaken it.

So a personal selection needs the machine-local tier, the way `agent-permissions`
policy already lives under `~/.config/luma/luma-foreman/` keyed by repository
root. What is undecided is how a machine-local selection and a committed one
compose at projection time.

## Notes

Captured 2026-08-21, during the migration of `docs/IDEAS.md`.

**The projection half is already scoped and is not what this idea is for.**
`docs/scope.md` lists *"load and unload skills — possibly by symlink, possibly
another mechanism"*, and costs *"selecting at projection time which subset of
adopted content is written out — including by symlink"* as **buildable now**.
This file is titled on the part that has no home.

**Mid-session swapping is blocked, and not by us.** `docs/scope.md` records that
loading and unloading mid-session *"needs cooperation that does not exist"* —
Agent Skills loads every skill's name and description at startup and the body on
description match, with no hook for *conditions changed, drop these*. Between
sessions is achievable; during one is not, in any harness. Worth knowing before
anyone promises "change them quickly".

**The same shape appears twice.** The open question left by `agent-permissions`
— whether foreman writes *committed* per-project Claude Code settings as a shared
floor, with the machine-local layer as overrides on top — is this same pattern
applied to permissions instead of skills. A committed team floor plus a personal
uncommitted layer may want one answer serving both rather than two.
