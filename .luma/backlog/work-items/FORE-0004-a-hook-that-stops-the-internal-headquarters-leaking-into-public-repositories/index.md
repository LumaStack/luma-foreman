---
type: work-item
key: FORE-0004
title: A hook that stops the internal headquarters leaking into public repositories
workflow_status: captured
rank: 010.0030.000
kind: idea
stage: draft
created: {by: 'human:luma-founder', at: '2026-08-21T00:00:00Z'}
description: 'A pre-commit hook should read the configured internal repository name and refuse a commit that names it in a public repository. Today the rule is enforced by whoever is typing remembering it, which failed on 2026-08-21 in a session where the rule had been stated minutes earlier. The obvious implementation breaks foreman''s boundary — the hook needs the internal repository''s name, which lives in the organization tool''s config, and a check that needs organization context to run has broken the boundary. Three ways out, none free: the organization tool owns the hook; foreman matches a project-local string, which writes the protected thing into the public repository; or foreman matches a digest it cannot reverse, which costs machinery.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:40:25Z'}
---

# A hook that stops the internal headquarters leaking into public repositories

Leaking the internal headquarters into a public repository should be stopped by a
hook. It should read the configured internal repository and prevent the commit.

## The problem it addresses

A public repository must never name an organization's internal one. Today that is
enforced by whoever is typing remembering the rule — which failed on 2026-08-21,
in a session where the rule had been stated minutes earlier and the risk was
flagged in the same message as the violation. Nothing caught it; a person did,
afterwards.

## Why not now

**The obvious implementation breaks a standing boundary.** The hook has to know
the internal repository's name in order to match against it, and that name lives
in `~/.config/luma/luma-leader/config.toml`. Foreman's own rule is a test: *if a check
ever needs organization context in order to run, the boundary has been broken.*

Three ways out, none free:

- **The organization tool owns the hook.** It may read that configuration. But
  only repositories where it is checked out get protected.
- **Foreman matches a project-local string.** Keeps the boundary — and writes the
  thing being protected into the public repository, which defeats it.
- **Foreman matches a digest it cannot reverse.** Keeps both the boundary and the
  secret; costs more machinery.

## Notes

**Pre-commit is the right boundary.** The failure cost nothing because nothing was
committed. One step later it is a pushed commit, and a merged pull request keeps
its diff whether or not the commit stays reachable — which is the incident this
stack already had once.

## Related work

- Born from the idea it replaces: [`hook-against-leaking-internal-hq`](../../ideas/hook-against-leaking-internal-hq.md)
