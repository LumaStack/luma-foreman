---
type: work-item
key: FORE-0002
title: Migrate the ideas corpus into the backlog
workflow_status: closed
rank: 070.0050.000
kind: change
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-24T17:33:58Z'}
description: 'The ideas in .luma/backlog/ideas/ sit outside the backlog corpus — isRecordPath excludes that directory, so no backlog command sees them. Move them in. The backlog''s kind: idea is the destination shape, but some are plainly defects rather than ideas, so each needs classifying rather than copying; a few are already archived as done and should not move at all. No existing procedure or skill does this properly — migrate-ideas covers splitting a single IDEAS.md into files, which this repository did long ago, and tend-ideas maintains the separate corpus rather than emptying it. Do not bend either into shape. Open and deliberately unsettled: whether every idea becomes a work item, or only the ones ready to be judged. If all of them move, backlog-ideas has no reason to stay adopted and this runs into no-way-to-un-adopt; if only some graduate, the corpus stays and this becomes recurring tending rather than a one-off.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T22:33:09Z'}
closed: {on: 2026-09-24, as: completed, by: 'agent:claude-opus-5/luma-backlog', reason: 'The corpus is in the backlog: every idea has a work item, provenance survived, no cross-reference was orphaned, each record points back at its origin, and the plan exists so another project need not rediscover it. The idea files stay until somebody has used the back-links to review; removing them is a separate decision.'}
---

# Migrate the ideas corpus into the backlog

## The problem

**The ideas sat outside the corpus, and no backlog command could see them.**
`isRecordPath` is an allowlist and `.luma/backlog/ideas/` is not in it — correctly,
because the ideas belonged to a different tool's format. The consequence was two
systems holding the same kind of thing, where only one of them could be listed,
ranked, transitioned or closed.

**They were not raw thoughts.** The median body ran to dozens of lines and
several past a hundred, with problems stated, alternatives weighed and re-open
triggers recorded. That is a backlog written in the wrong place, not a scratchpad.

**And no procedure covered moving them.** `migrate-ideas` splits a single
`IDEAS.md` into files, which this repository did long ago. `tend-ideas` maintains
the separate corpus rather than emptying it. Bending either into shape was
explicitly ruled out.

## What is being delivered

**Every idea as a work item**, ordered by `horizon` and then by creation date
within each band, created in that order so rank fell out rather than needing a
pass of its own.

Each keeps its title and body verbatim and its original `created` actor and
timestamp. Each is `kind: idea`, because nobody has judged them yet. Each gained
a `description`, derived from the idea's own opening paragraphs, since a listing
shows nothing else.

**The cross-references repointed**, in a second pass once every key existed.
**A back-link on every record** to the idea it came from, so the result can be
reviewed by following links rather than by trusting a report.

**And the reusable half** — a plan another project can follow, carrying the
ordering rule, the field mapping, and the refusals and silent failures this run
found the hard way.

## Out of scope

**Deleting the idea files.** They stay until somebody has used the back-links to
check the migration. Removing them is a separate decision made after that.

**Retiring the bundle.** That is FORE-0003, and it only becomes sensible because
this emptied the corpus.

**Classifying the work.** Everything arrives as `kind: idea`. Several read as
defects and one of those judgements is cheap to make later; making it during a
mechanical move would smuggle a second decision into the first.

**Fixing what the migration found.** The actor resolved from the OS account, and
`type_version` absent from every record this created. Both are recorded, neither
is repaired here.

## Constraints

**The two passes cannot be combined.** The second record links to the thirtieth,
which has no key until it exists, so links can only be fixed after every record
is created. The bodies are knowingly wrong in between.

**`created` has to be written by hand.** `work-item new` takes both actor and
timestamp from the environment and has no flag for either, so left alone a corpus
loses its provenance in a single run.

**Verification means running the check, not reading the claim.** One archived
idea's closing note asserted an estate-wide invariant that had since rotted, and
believing it would have recorded something false.


## Related work

- The reusable procedure this produced: [`plans/migrate-ideas-into-the-backlog`](../../plans/migrate-ideas-into-the-backlog.md)
  — written so another project with the same problem can repeat it without
  rediscovering the refusals and silent failures this run found.
- [[work-items/FORE-0003-deprecate-backlog-ideas-and-learn-how-deprecation-goes]]
  — retires the bundle this corpus belonged to, which only makes sense once the
  corpus is empty.
