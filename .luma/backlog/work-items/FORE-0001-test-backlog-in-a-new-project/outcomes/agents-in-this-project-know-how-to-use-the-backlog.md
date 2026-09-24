---
type: outcome
title: Agents in this project know how to use the backlog
description: "The commands work without the bundle and that path is supported, but standing up the tool without it leaves the commands working and nobody knowing when to run them. open-questions 25 in luma-backlog is the argument."
desired_state: "The backlog bundle is adopted here and its procedures are reachable as skills in an agent's harness."
verify_by: "luma-foreman apply has run, .luma/bundles/ carries the backlog bundle, and the procedures appear as skills. An agent asked to capture or refine something reaches the procedure rather than inventing a shape."
work_item: '[[work-items/FORE-0001-test-backlog-in-a-new-project]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T14:16:27Z'}
verified:
  - as: proven
    at: "2026-09-24T17:21:31Z"
    by: agent:claude-opus-5/luma-backlog
evidence:
  - at: "2026-09-24T17:21:31Z"
    by: agent:claude-opus-5/luma-backlog
    what: 'All four checks in verify_by read. (1) apply has run: CLAUDE.md carries the luma:begin generated marker, and .claude/skills/ holds generated adapters each stamped ''luma-foreman:generated from lumastack/luma-catalog/backlog''. (2) .luma/bundles/lumastack/luma-catalog/backlog/ is present with its BUNDLE.md, INDEX.md, policy/, procedure/, templates/ and type_definitions/. (3) Seven procedures appear as skills: backlog-capture, -journal, -refine, -rundown, -show, -transition, -verify. (4) Demonstrated live rather than asserted: this verification was reached by invoking the backlog-verify skill, which routed to the vendored procedure and its required policy reading, and this entry follows that procedure''s evidence rules. The adapter carries no copy of the procedure, so the route cannot drift.'
---

# Agents in this project know how to use the backlog

Why this matters, and anything needed to read the check correctly.
