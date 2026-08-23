---
type: luma/idea
title: Distribution — foreman installs by clone and symlink
created: { by: human:benlinton, at: 2026-08-17T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
lifecycle_status: draft
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

**A constraint the original entry did not name.** `docs/scope.md` records that
*"the README promises no build step and nothing to install"*, and leans on that
promise elsewhere — it is cited as a reason semver dependency resolution may not
be affordable. A pip or brew package is precisely a build step and a thing to
install. Distribution and that promise are in tension and nothing has chosen
between them. Whoever picks this up should decide that first, because it governs
every option below it.

**The release half already has knowledge behind it.** The `luma/github-release`
bundle is published; what is missing is foreman using it.

**Related, and recorded elsewhere.** `docs/next-steps.md` asks whether foreman's
own release process should live in a bundle it has to adopt — "elegant or an
ever-present headache for maintainers". Adjacent question, already captured
there, not duplicated here.
