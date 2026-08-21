---
type: idea
title: A hook that stops the internal headquarters leaking into public repositories
created: { by: human:benlinton, at: 2026-08-21T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
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
in `~/.config/luma/luma-hq/config.toml`. Foreman's own rule is a test: *if a check
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
