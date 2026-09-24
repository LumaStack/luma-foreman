---
type: outcome
title: LKF ships type_version and folder-shaped Type Definitions
desired_state: "LKF v0.0.21 defines type_version as a sibling field written beneath type, and Type Definitions are folders carrying CHANGELOG.md and migrations/."
verify_by: "Read the LKF release and a Type Definition in the estate. The field is defined and the folder shape is real."
work_item: '[[work-items/FORE-0064-frontmatter-needs-a-version-and-a-type-definition-needs-migrations]]'
stage: draft
created: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:45:24Z'}
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:47:05Z'}
verified:
  - as: proven
    at: "2026-09-24T19:47:17Z"
    by: agent:claude-opus-5/luma-backlog
evidence:
  - at: "2026-09-24T19:47:17Z"
    by: agent:claude-opus-5/luma-backlog
    what: 'Type Definitions in the estate are folders — .luma/bundles/lumastack/luma-catalog/backlog/type_definitions/work-item/DEFINITION.md is one, with siblings each in their own directory. type_version is defined and written beneath type in records across the estate, which is the sibling-field shape this delivery shipped. Note for a later reader: the field is not universal — 121 typed documents estate-wide lack it, which is rot after this delivery rather than the delivery failing.'
---

# Every typed document in the estate carries type_version

Why this matters, and anything needed to read the check correctly.
