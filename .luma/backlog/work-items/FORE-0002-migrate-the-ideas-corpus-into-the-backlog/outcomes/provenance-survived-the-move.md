---
type: outcome
title: Provenance survived the move
desired_state: "Each migrated record carries the created actor and timestamp from the idea it came from, not the date of the migration — except where the source had none to carry."
verify_by: "Read created on every migrated record. Only records whose source idea had no frontmatter show the migration date."
work_item: '[[work-items/FORE-0002-migrate-the-ideas-corpus-into-the-backlog]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T22:32:27Z'}
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T22:32:43Z'}
verified:
  - as: proven
    at: "2026-09-24T22:33:00Z"
    by: agent:claude-opus-5/luma-backlog
evidence:
  - at: "2026-09-24T22:33:00Z"
    by: agent:claude-opus-5/luma-backlog
    what: Read created on all 61 migrated records. Two carry the migration date and both are the records whose source had no frontmatter and therefore no created to preserve — data-files and pretty-command-line-output. The other 59 carry the original actor and timestamp, back to 2026-08-09.
---

# Provenance survived the move

Why this matters, and anything needed to read the check correctly.
