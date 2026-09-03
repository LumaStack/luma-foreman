---
type: luma/idea
title: A bundle declares what it works with, and get prints it rather than fetching it
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# A bundle declares what it works with, and `get` prints it

## The idea, as raised

**A bundle should be able to say, during `get`, that it needs another bundle to
work.** Raised while sweeping `docs/architecture.md`, against the claim that
bundles depend on nothing.

## What is true today

**Bundles depend on nothing, by policy and by implementation.**
`bundle-manager`'s `organizing-a-bundle` states it as a rule — *a bundle may
reference another for depth, never for capability* — and nothing in foreman
resolves anything.

**But the escape hatch the policy names does not exist.** It says *composition
belongs to the catalog, not to bundles*, and points at the catalog's `requires`
field. `CATALOG.md` declares one — `git-secrets`, recommended — and **nothing in
`src/foreman/` reads it.**

So there is currently no way to express *you need both*, at either level. The
reason bundles may not depend is that the catalog handles it, and the catalog
does not.

## The pain this would relieve

**Vendored types drift and nothing detects it.** `luma-types` exists because
several bundles need the same type; each carries its own copy, and
`audit-bundle` checks byte-identity by hand. That is the concrete cost of having
no dependencies.

## Why not full resolution

Three things arrive with it, and none has been asked for:

- **A resolver.** `organizing-a-bundle` says outright that the fix for an
  accidental dependency is *to move content back rather than to build a
  resolver*.
- **Version conflicts.** Two bundles wanting different versions of a third is
  the problem no package manager has solved.
- **A `get` that can fail.** Today it is a copy that cannot fail for dependency
  reasons, and that is load-bearing for *a fresh clone with no network
  reproduces the project exactly*.

## The proposal

**Advisory, not resolved.** A bundle declares what it works with; `get` prints
it and fetches nothing:

```
lumastack/luma-catalog/decision-records: adopted 0.9.2
  works with  lumastack/luma-catalog/luma-types — not adopted here
```

**No graph, no conflicts, no new failure mode.** The author's knowledge travels
with the bundle instead of sitting in a catalog field nothing reads, and it does
not foreclose real resolution later.

## What it would take

- A field on `BUNDLE.md` — and a decision on whether it supersedes the catalog's
  unread `requires` or sits beside it.
- `get` printing what is declared and not adopted here.
- `organizing-a-bundle` revisited. **Its *acknowledge, do not depend* section is
  load-bearing in three workflows** — `create-bundle` uses it to argue when to
  split a bundle in two, and `migrate-bundle` and `where-a-bundle-belongs` both
  rest on *nothing to update, bundles depend on nothing*. Those arguments change,
  not just the sentence.

## Raised from

Sweep `the-whole-of-foreman`, slice 001, while reading `docs/architecture.md`.
The same claim was corrected in `docs/commands.md` in the same slice.
