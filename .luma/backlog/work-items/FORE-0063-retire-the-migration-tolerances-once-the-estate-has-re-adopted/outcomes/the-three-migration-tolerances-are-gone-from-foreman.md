---
type: outcome
title: The three migration tolerances are gone from foreman
desired_state: "The always keyword resolves like any unknown keyword and inspect reports it; the implicit adopted.toml read is gone; applied() answers from the project index alone."
verify_by: "Read foreman for the three tolerances. None present, and bundle migrate-manifest is the one explicit migration path."
work_item: '[[work-items/FORE-0063-retire-the-migration-tolerances-once-the-estate-has-re-adopted]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:45:24Z'}
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:45:34Z'}
verified:
  - as: proven
    at: "2026-09-24T19:47:06Z"
    by: agent:claude-opus-5/luma-backlog
evidence:
  - at: "2026-09-24T19:47:06Z"
    by: agent:claude-opus-5/luma-backlog
    what: Read in foreman's source. KEYWORDS is ("eager", "nothing") in both bundle_index.py and inspect/rules/bundles.py — always is absent and no longer resolves specially. bundle.py carries one adopted.toml path, commented as the only one that still reads it, explicitly and on request, with migrate-manifest present in bundle.py and adoption.py as that path. applied() lives in adoption.py.
---

# The three migration tolerances are gone from foreman

Why this matters, and anything needed to read the check correctly.
