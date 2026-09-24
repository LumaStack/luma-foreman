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

**The bundle has lost its reason to be adopted.** `backlog-ideas` describes ideas
as individual files with their own lifecycle, tended in their own sessions. Once
the corpus moves into the backlog there is nothing here it governs, and an
adopted bundle nothing follows is knowledge in front of an agent that no longer
matches the project.

**Some of it is still worth keeping.** The bundle reasons about what earns a file,
how capture stays fast, and how a list gets tended rather than accumulating. That
thinking should survive in the backlog bundle rather than going out with the
directory.

**Nothing in the estate has ever been deprecated.** This is the first one, and the
only adopter is the maintainer — which makes it the cheapest possible rehearsal
for a deprecation that does have consumers, and the last chance to find out what
the procedure gets wrong while nobody can be hurt by the answer.

**Two gaps are already visible.** `delete-bundle` says to set
`obligation: deprecated` because *"that is what makes a project still holding it
hear anything at all"* — and foreman reads no `obligation` key and has no
deprecation report. The catalog speaks the word; the adopter-side tool is deaf to
it, so the procedure's one notification mechanism does not exist. And the
procedure says nothing about salvage, which is the first thing this needs.

## What is being delivered

**The parts worth keeping, moved into the backlog bundle**, before anything is
removed.

**The bundle deprecated in `lumastack/luma-catalog`**, with a successor named
rather than a bare notice, then removed after a window.

**An improved `delete-bundle`.** Whatever the rehearsal teaches has to end up in
the procedure, or the next deprecation rediscovers it. That is the deliverable
that outlives this bundle.

## Out of scope

**Moving the ideas.** FORE-0002 does that, and this cannot start until it has.

**Building `obligation` support in foreman.** The gap is a finding this work
produces; closing it is its own work.

**Un-adopting the bundle here.** There is no command for it, which is the subject
of its own record.

## Constraints

**Behave as though there were real consumers.** A deprecation done quickly
because only one person is affected teaches nothing, and teaching is the point.

**Adopted copies survive by design.** A vendored bundle is the project's own file
and no publisher can reach into it. That is the design working, not a leak.

**Do not empty the bundle and leave the manifest**, and **do not reuse the name**
— a future bundle at the same path is a different thing wearing an identity some
project already pinned.

## Related work

- [[work-items/FORE-0002-migrate-the-ideas-corpus-into-the-backlog]] — empties the
  corpus, which is what makes this sensible. Must land first.
- [[work-items/FORE-0010-there-is-no-way-to-un-adopt-a-bundle]] — the wall this
  runs into on the adopter side. Removing a bundle means hand-editing a file whose
  own header forbids it.
- [[work-items/FORE-0012-which-bundles-this-project-should-carry-and-what-decides-it]]
  — audits which bundles earn their place and counts `backlog-ideas` among the
  producers. This changes that answer.
- `.luma/bundles/lumastack/luma-catalog/bundle-manager/procedure/delete-bundle.md`
  — the candidate procedure, and the thing this work is meant to improve.
