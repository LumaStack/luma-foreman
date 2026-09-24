---
type: work-item
key: FORE-0002
title: Migrate the ideas corpus into the backlog
workflow_status: captured
rank: 010.0010.000
kind: change
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-24T17:33:58Z'}
description: 'The ideas in .luma/backlog/ideas/ sit outside the backlog corpus — isRecordPath excludes that directory, so no backlog command sees them. Move them in. The backlog''s kind: idea is the destination shape, but some are plainly defects rather than ideas, so each needs classifying rather than copying; a few are already archived as done and should not move at all. No existing procedure or skill does this properly — migrate-ideas covers splitting a single IDEAS.md into files, which this repository did long ago, and tend-ideas maintains the separate corpus rather than emptying it. Do not bend either into shape. Open and deliberately unsettled: whether every idea becomes a work item, or only the ones ready to be judged. If all of them move, backlog-ideas has no reason to stay adopted and this runs into no-way-to-un-adopt; if only some graduate, the corpus stays and this becomes recurring tending rather than a one-off.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T17:34:54Z'}
---

# Migrate the ideas corpus into the backlog

## The problem

## What is being delivered

## Out of scope

## Constraints

## Related work

- The reusable procedure this produced: [`plans/migrate-ideas-into-the-backlog`](../../plans/migrate-ideas-into-the-backlog.md)
  — written so another project with the same problem can repeat it without
  rediscovering the refusals and silent failures this run found.
- [[work-items/FORE-0003-deprecate-backlog-ideas-and-learn-how-deprecation-goes]]
  — retires the bundle this corpus belonged to, which only makes sense once the
  corpus is empty.
