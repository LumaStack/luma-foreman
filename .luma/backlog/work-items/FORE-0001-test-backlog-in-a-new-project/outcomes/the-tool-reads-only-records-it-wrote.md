---
type: outcome
title: The tool reads only records it wrote
description: "This is where it broke. BACK-0108 was found on first use against a second project: isRecordPath was a denylist, so another tool's ideas/, plans/ and records/decisions/ were read as this corpus \u2014 three parse warnings on every command, and decision list showing 13 records it never wrote and offering to edit them. Fixed by making it an allowlist; nothing here says it must stay fixed, and this repository is the one that found it."
desired_state: "Another luma tool's records in this repository are not read as this tool's corpus, and produce no warnings."
verify_by: "With another tool's content present under .luma/ \u2014 ideas, plans, or decisions this tool did not write \u2014 every command runs clean and no listing offers them."
work_item: '[[work-items/FORE-0001-test-backlog-in-a-new-project]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T14:16:27Z'}
---

# The tool reads only records it wrote

Why this matters, and anything needed to read the check correctly.
