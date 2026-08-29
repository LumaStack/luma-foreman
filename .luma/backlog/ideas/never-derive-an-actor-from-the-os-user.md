---
type: luma/idea
title: Never derive an actor from the OS user, and let a project say its usernames are secret
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle: draft
---

# Never derive an actor from the OS user

## The idea, as raised

**An actor written as `human:<os-user>` is wrong twice, and one of the two is a
disclosure.** Raised during sweep `the-whole-of-foreman`, after an agent wrote a
workstation account name into a sweep record and into two published catalog
files.

## This has happened before

**`luma-backlog`'s journal, 2026-08-10:**

> *Found by dogfooding: verify attributed agent work to `human:<os-user>`,
> because `LUMA_BACKLOG_ACTOR` was unset and detection falls back to the OS
> user. Provenance is the whole point of the actor field, so a default that is
> wrong in the common case is worse than no default.*

**Diagnosed in one tool, then reproduced by hand in another nineteen days
later.** Nothing carried the lesson between them, which is the argument for
making it a rule rather than a note.

## Two faults, and they are separate

| | |
| --- | --- |
| **provenance** | the logged-in account is not necessarily who acted. Wrong in any organization, whatever its policy |
| **disclosure** | in some organizations a workstation username is secret. **In others it is public and unremarkable** — which is why this half has to be a setting, not a compiled-in rule |

## What should happen instead

**Derive an actor from the git or forge identity**, never from the OS. `git
config user.name` and the forge login are statements about who a person is;
`$USER` is a statement about which account is logged in.

**Where neither is available, write `human:unknown`.** The format says so
already: *a tool that cannot tell who invoked it should write the honest value
rather than guessing a plausible one.* An OS-user fallback is precisely the
plausible guess it warns against.

## Why `inspect --rule identity` cannot catch it today

**By design, and its own docstring names the gap:**

> *Everything here is detectable by SHAPE, so it needs no configuration and runs
> in a bare clone… an optional identity list would make this check better, but
> requiring one would make it unrunnable in continuous integration.*

**`human:<os-account>` is not shape-detectable.** Nothing distinguishes it from
a legitimate handle without knowing which one the machine is logged in as — and in
continuous integration the OS account is the runner, so comparing against it is
worthless exactly where the rule is built to run.

**The docstring already proposes the answer**: an optional identity list, used
when present and skipped when absent. That keeps the bare-clone guarantee and
catches this on the workstation where it is written, which is where it can still
be fixed cheaply.

## What it would take

- **Stop the fallback.** Wherever an actor is derived, prefer git identity, then
  forge login, then `human:unknown`. Never `$USER`.
- **An optional identity list** in `.luma/config/luma-foreman.toml` — names and
  handles this project considers private. Absent, the check skips and says so.
- **A decision** on whether the list is committed. It is a list of things that
  must not appear in the repository, which is an awkward thing to put in the
  repository.

That last point is the real design question and it is not obvious.

## Raised from

Sweep `the-whole-of-foreman`, slice 001. The leak reached
`.luma/backlog/sweeps/`, two files in the published `review-sweeps` bundle, and
four commits of git history.
