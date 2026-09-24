---
type: outcome
title: init leaves a project able to create and read records
description: "The existing outcome covers only the moment BEFORE init — that the tool refuses correctly without a configuration file. Nothing asserted that it works afterwards, which is the actual point of standing it up."
desired_state: "After init, a work item can be created, listed, shown and journalled, and each returns what it should."
verify_by: "In this repository: create a work item, then list, show and journal it. Each command returns the record rather than an error, and the record on disk carries the fields it should."
work_item: '[[work-items/FORE-0001-test-backlog-in-a-new-project]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T14:16:27Z'}
verified:
  - as: disproven
    at: "2026-09-24T17:35:43Z"
    by: agent:claude-opus-5/luma-backlog
evidence:
  - at: "2026-09-24T17:35:43Z"
    by: agent:claude-opus-5/luma-backlog
    what: 'First three clauses hold: create, list, show and journal each returned the record rather than an error, on FORE-0002 and FORE-0001 both. The last clause fails — the record on disk did not carry the fields it should. ''work-item new'' wrote created.by: human:<os-user>, deriving the actor from the OS account because LUMA_BACKLOG_ACTOR was unset, and ''set'' then wrote the same into modified.by. The convention is human:luma-founder. Both were hand-corrected afterwards, which is the point: an unconfigured machine writes a workstation account name into a committed record and nothing objects. The only mechanism is an environment variable, which cannot be committed, so the failure recurs on every fresh machine. Predicted in this repository by the idea never-derive-an-actor-from-the-os-user, which records the same fault in luma-backlog''s own journal on 2026-08-10.'
---

# init leaves a project able to create and read records

Why this matters, and anything needed to read the check correctly.
