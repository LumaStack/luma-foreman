---
type: luma/project
title: luma-foreman
disclosure_level: public
description: The command-line tool that runs inside a project repository — agent permissions, inspect rules, and eventually adoption. Open it for anything foreman does to a repository, not for what a standard says.
owns:
  - the Claude Code permission gate and its per-project rules
  - inspect rules and their findings
  - projections from .luma/ into whatever a tool expects
must_not_own:
  - what a standard says, or the reasoning behind it
  - the knowledge format
  - any organization's decisions or private context
---

## Why it exists

A standard that lives only in prose is a standard nobody keeps. This is where
one becomes executable — a check that runs in continuous integration, a gate
that fires on a tool call, a structure written into a repository that did not
have it.

**It runs where the work is.** Everything else in this stack is read; this is
the part that acts, inside repositories that may know nothing about any of it.

## Boundaries

**It never reads an organization's headquarters at runtime.** Standards are
argued and settled there and travel here as executable checks. **If a check ever
needs organization context in order to run, the boundary has been broken** —
that is the test, and it is worth failing loudly rather than quietly special-
casing.

**It does not decide what good looks like.** The catalog holds the standards and
an organization holds its own; this enforces them. A rule compiled in here is a
rule nobody agreed to.

**It writes freely into what it owns and never silently into what the operator
owns.** Its own directories are fair game; `settings.json` changes are printed
for a person to apply.

## Status

Early, and every command works — `init`, `get`, `apply`, `inspect`, `bundle`,
`catalog` and `agent-permissions`. Python 3.11+, standard library only. The
catalog now holds the knowledge the original command set was built on, which is
what `owns` below is meant to state.
