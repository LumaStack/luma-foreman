---
type: outcome
title: init leaves a project able to create and read records
description: "The existing outcome covers only the moment BEFORE init \u2014 that the tool refuses correctly without a configuration file. Nothing asserted that it works afterwards, which is the actual point of standing it up."
desired_state: "After init, a work item can be created, listed, shown and journalled, and each returns what it should."
verify_by: "In this repository: create a work item, then list, show and journal it. Each command returns the record rather than an error, and the record on disk carries the fields it should."
work_item: '[[work-items/FORE-0001-test-backlog-in-a-new-project]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T14:16:27Z'}
---

# init leaves a project able to create and read records

Why this matters, and anything needed to read the check correctly.
