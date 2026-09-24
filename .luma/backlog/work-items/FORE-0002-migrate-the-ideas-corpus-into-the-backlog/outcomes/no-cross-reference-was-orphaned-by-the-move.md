---
type: outcome
title: No cross-reference was orphaned by the move
desired_state: "No wikilink anywhere in the work items still points at an idea slug, so nothing that used to resolve now silently fails."
verify_by: "Scan every work item for wikilinks whose target is an idea slug. Zero. Anything left unresolved must be a prose example or a link into another repository, and must be named rather than counted."
work_item: '[[work-items/FORE-0002-migrate-the-ideas-corpus-into-the-backlog]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T22:32:27Z'}
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T22:32:43Z'}
verified:
  - as: proven
    at: "2026-09-24T22:33:01Z"
    by: agent:claude-opus-5/luma-backlog
evidence:
  - at: "2026-09-24T22:33:01Z"
    by: agent:claude-opus-5/luma-backlog
    what: 'Scanned every work item for wikilinks whose target is an idea slug: zero. 53 were repointed at work items and 2 at plans/migrate-estate-to-type-definitions. Nine targets remain unresolved and each was read rather than counted: wikilink twice and wikilinks once are prose examples of the syntax; refresh-index is a slug inside a frontmatter example; the-repository-index, create-internal-hq, an-index-of-what-exists, conditional-preload and rethinking-the-luma-prefixed-bundles point into other repositories and never resolved in this one.'
---

# No cross-reference was orphaned by the move

Why this matters, and anything needed to read the check correctly.
