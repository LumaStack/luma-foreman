---
type: work-item
key: FORE-0003
title: Deprecate backlog-ideas, and learn how deprecation goes
workflow_status: captured
rank: 010.0020.000
kind: change
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-24T17:37:23Z'}
description: 'Three parts. First, salvage: take whatever in backlog-ideas is worth keeping and move it into the backlog bundle, which is where ideas land once FORE-0002 moves the corpus. Second, deprecate the bundle itself in luma-catalog. Third, and the reason this is worth doing carefully — it is the estate''s first deprecation, and the only adopter is the maintainer. Treat it as a rehearsal for a deprecation with real consumers, and work out the procedure while there is nobody to hurt. delete-bundle already exists and is the candidate, but running it for real is how its gaps get found. Two are visible before starting: it says to set obligation: deprecated in the catalog''s requires, which is what makes an adopter hear anything at all, and foreman reads no obligation key and has no deprecation report — the catalog speaks the word and the adopter-side tool is deaf to it. And it says nothing about salvage, which is the first part here. Whatever is learned should end up improving delete-bundle rather than living only in this record.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T17:37:34Z'}
---

# Deprecate backlog-ideas, and learn how deprecation goes

## The problem

## What is being delivered

## Out of scope

## Constraints
