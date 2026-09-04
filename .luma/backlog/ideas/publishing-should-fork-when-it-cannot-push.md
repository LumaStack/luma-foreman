---
type: luma/idea
title: Publishing should fork when it cannot push
created: { by: agent:claude-opus-5, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# Publishing should fork when it cannot push

**`luma-foreman publish` works for people who can already write to the
catalog.** Everybody else gets a refusal telling them to fork and open the
request by hand. That was accepted deliberately for the MVP, and it is the half
of the design that does not yet do what the design claims.

## What happens today

The push to `origin` fails, and the refusal says so:

```
luma-foreman publish: could not push to lumastack/luma-catalog
  Opening a request needs write access to the catalog. Forking on
  your behalf is not built yet — fork it, then publish against
  your fork and open the request by hand.
```

Which is honest, and is also the point at which somebody publishing their first
bundle stops.

## Why it was left out rather than half-built

**`gh` already does it.** `gh pr create` forks transparently when push rights
are absent, and `gh repo fork` is explicit about it. The mechanism is not the
hard part.

**The hard part is that it fails in the case that matters.** A fork introduces
a second remote, a branch that lives somewhere other than where the request
points, a `--head <user>:<branch>` on the request, and a fork that may already
exist from last time and be stale. None of that is exercised by a test suite
with `gh` stubbed on PATH, and a forking path that is wrong is worse than one
that is absent — the absent one refuses in a sentence, and the wrong one opens
a request against the wrong tree.

## What it has to do

- **Detect it before pushing**, not by pushing and reading the failure. A
  refusal that arrives after a commit has been built reads as the tool breaking
  rather than as a permission it never had.
- **Reuse an existing fork rather than making a second one**, and refresh it
  from upstream first — a fork left over from a previous publication is behind,
  and a request opened from a stale base is a diff nobody can read.
- **Say which case it was.** The output already distinguishes routes elsewhere;
  publishing through a fork is a different route than publishing directly and
  the person should know which one they are in, because the follow-up differs.

## What it does not change

**The design already holds for strangers** — that is why forking is the only
gap rather than a redesign. One path, one gate, whoever you are: the request is
still a pull request, the catalog's pre-merge job still judges it, and a
maintainer still merges. Forking is how git carries a contributor who lacks
write access, and it was always meant to be the tool's job rather than the
person's.

*Related:* [[ADR-0014-publishing-is-a-custody-handover]] records the omission as
a standing consequence, and the plan at
`.luma/backlog/plans/bundle-publish.md` carries the reasoning it came from.
