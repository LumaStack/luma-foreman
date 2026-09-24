---
type: work-item
key: FORE-0031
title: Distribution — foreman installs by clone and symlink
workflow_status: captured
rank: 010.0300.000
kind: idea
stage: draft
created: {by: 'human:luma-founder', at: '2026-08-17T00:00:00'}
description: Install is currently a clone plus a symlink, which is fine for one operator and not for an organization. There is no released artifact at all. Foreman has no git tags and its changelog holds only an `[Unreleased]` section, so the install path is not merely awkward — there is nothing to install but a working copy.
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:43Z'}
---

# Distribution — foreman installs by clone and symlink

Install is currently a clone plus a symlink, which is fine for one operator and
not for an organization.

## The problem it addresses

There is no released artifact at all. Foreman has no git tags and its changelog
holds only an `[Unreleased]` section, so the install path is not merely awkward —
there is nothing to install but a working copy.

## Notes

Migrated from `docs/IDEAS.md` on 2026-08-21, where it was an open question left
behind by the shipped `agent-permissions` work. `created.at` is a day-level
estimate from git history.

**A constraint the original entry did not name.** The README promises no build
step and nothing to install, and that promise is load-bearing elsewhere — it is
ADR-0002's reason semver dependency
resolution may not be affordable. **A pip or brew package is precisely a build
step and a thing to install.** Distribution and that promise are in tension and
nothing has chosen between them. Whoever picks this up should decide that first,
because it governs every option below it.

**The release half already has knowledge behind it.** The `luma/github-release`
bundle is published; what is missing is foreman using it.

**Related, and recorded elsewhere.** Whether foreman's own release process
should live in a bundle it has to adopt is
[[work-items/FORE-0012-which-bundles-this-project-should-carry-and-what-decides-it]]'s question, not this one.

## What the ecosystem already solved

Worth knowing before building any of this, because two of the four are
load-bearing against the options above.

- **Claude Code plugins are a real package manager.** Semver,
  plugin-to-plugin dependencies with ranges, git sources pinned to tags resolved
  to SHAs, frozen lockfile installs with `--ignore-scripts`, lifecycle scripts
  disabled, path traversal blocked — and a **`managed` install scope that is
  organization-controlled and read-only.** That last one is an obligation
  mechanism already designed, and worth reading before designing another.
- **But plugins cache to `~/.claude/plugins/cache/` and are not committed**, so
  a fresh clone with no network does not reproduce. **Vendoring into the
  repository does**, which is a real difference rather than a stylistic one, and
  it is the argument ADR-0002 rests on.

*Absorbed from `docs/scope.md` when that document was scattered on 2026-08-29.
Its claim that `SKILL.md` is "read by 40+ agents" was dropped as an unsourced
count.*

## Related work

- Born from the idea it replaces: [`distribution-beyond-clone-and-symlink`](../../ideas/distribution-beyond-clone-and-symlink.md)
