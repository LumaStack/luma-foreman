---
type: work-item
key: FORE-0051
title: Permission tuning may need to be its own command
workflow_status: captured
rank: 010.0500.000
kind: idea
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-04T00:00:00'}
---

# Permission tuning may need to be its own command

**`agent-permissions` may not belong inside `luma-foreman`.** An organization
may well want to allow foreman and deny anyone changing what an agent is
permitted to do — and while both live behind one binary, that is one decision
rather than two.

*Not the same as [[work-items/FORE-0030-a-committed-per-project-permission-floor-under-the-machine-local-layer]]*, which asks where permission
settings live and whether a team shares a posture. This asks whether the two
capabilities can be permitted separately at all.

## Related work

- Born from the idea it replaces: [`permission-tuning-may-be-its-own-command`](../../ideas/permission-tuning-may-be-its-own-command.md)
