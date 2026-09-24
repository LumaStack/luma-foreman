---
type: outcome
title: Keys allocate under the project's configured prefix
description: "The reason the prefix is configurable at all. Partly demonstrated by the key migration, which moved WORK-0001 to FORE-0001 \u2014 but that proves migration, not allocation, and a new record is the case that matters for a project standing up."
desired_state: "A work item created here takes a key under the prefix this project configured, not the tool's default."
verify_by: "With work_item_key: FORE, create a work item and read its key. It begins FORE-, and the number continues the project's sequence rather than restarting."
work_item: '[[work-items/FORE-0001-test-backlog-in-a-new-project]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T14:16:27Z'}
---

# Keys allocate under the project's configured prefix

Why this matters, and anything needed to read the check correctly.
