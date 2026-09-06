---
type: luma/idea
title: Permission tuning may need to be its own command
created: { by: human:benlinton, at: 2026-09-04T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: someday
scope: project
stage: draft
---

# Permission tuning may need to be its own command

**`agent-permissions` may not belong inside `luma-foreman`.** An organization
may well want to allow foreman and deny anyone changing what an agent is
permitted to do — and while both live behind one binary, that is one decision
rather than two.

*Not the same as [[committed-permission-floor]]*, which asks where permission
settings live and whether a team shares a posture. This asks whether the two
capabilities can be permitted separately at all.
