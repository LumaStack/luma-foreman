---
type: outcome
title: Verify correct output of all commands before running init on the project
desired_state: "Every command's output was read in a project that had not yet run init, and each was correct — the refusal to operate without a configuration file included."
verify_by: "A person runs each command in a repository with no backlog and reads what comes back. Not a test: the question is whether the output is right to a reader, which is the thing a test cannot answer."
work_item: '[[work-items/FORE-0001-test-backlog-in-a-new-project]]'
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-20T21:16:26Z'}
verified:
  - as: proven
    at: "2026-09-24T14:14:04Z"
    by: human:luma-founder
evidence:
  - at: "2026-09-24T14:14:04Z"
    by: human:luma-founder
    what: Done by hand by the maintainer in this repository before init was run, and reported on 2026-09-24. Backfilled into the record afterwards by an agent at the maintainer's instruction; the checking was his, the writing-down was not.
---

# Verify correct output of all commands before running init on the project

Why this matters, and anything needed to read the check correctly.
