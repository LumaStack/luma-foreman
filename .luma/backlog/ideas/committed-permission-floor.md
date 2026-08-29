---
type: luma/idea
title: A committed per-project permission floor, under the machine-local layer
created: { by: human:benlinton, at: 2026-08-17T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
lifecycle: draft
---

# A committed per-project permission floor, under the machine-local layer

Whether foreman additionally writes *committed* per-project Claude Code settings
— the shared floor a team gets from a clone — with the machine-local layer as
overrides on top. Those are two different capabilities that happen to touch the
same file format.

## The problem it addresses

A clone currently arrives with no permission posture at all. Everything
`agent-permissions` knows is machine-local, so each operator configures a
repository from scratch and nothing records what the project itself expects.

## Notes

Migrated from `docs/IDEAS.md` on 2026-08-21, where it was an open question left
behind by the shipped `agent-permissions` work. `created.at` is a day-level
estimate from git history.

**The current design refuses this deliberately.** `docs/claude-agent-permissions.md`
states *"Nothing is stored inside the project, so none of it can be committed by
accident"*, and the reasoning behind it — what an agent may do in a repository is
the operator's call, not something every clone inherits — is a position this idea
has to argue against rather than around.

**The harness already has the two tiers.** Claude Code reads `.claude/settings.json`
as the shared committed file and `.claude/settings.local.json` as the personal,
gitignored one that takes precedence. So this is not designing a layered system;
it is deciding whether foreman authors the committed tier of one that exists.

**The same shape appears in [[personal-skill-selection-not-committed]]** — a
committed project layer beside a personal uncommitted one, there for skills and
here for permissions. One answer about how the two compose may serve both. They
are filed separately because the risk profiles differ and this one has a shipped
tool with a stated position.
