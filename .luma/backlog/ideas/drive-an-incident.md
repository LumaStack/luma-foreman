---
type: luma/idea
title: Drive an incident, and store it as markdown
created: { by: human:benlinton, at: 2026-08-09T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: someday
scope: project
stage: draft
---

# Drive an incident, and store it as markdown

When something goes wrong, foreman runs the response rather than leaving it to
memory and chat: prompts for what is known, tracks what has been tried, and
captures the timeline as it happens rather than reconstructing it afterward. The
record is markdown, committed in the affected project.

Likely delivered as a skill foreman installs into a project, rather than
something foreman runs itself — the response happens inside the affected
repository, with whoever is already working there.

## The problem it addresses

A timeline reconstructed after the fact is the one nobody trusts. What was known
when, and what had already been tried, are exactly the details that do not
survive being remembered later.

## Notes

**Settled:** incident records conform to the Luma Knowledge Format. They are
knowledge like any other record, not a separate filing system.

**Open:** where the records live, and whether driving and recording are one
capability or two, since recording a timeline is useful even when nobody is
being walked through the response.

**Was open, and is not.** The original entry assumed that needing a record type
for an accumulating timeline would be "a format request". Checked during the
migration of `docs/IDEAS.md`: it is not. `SPEC.md` §10.1 declares types with an
ordinary `type_definition` document in a bundle's `_types/` directory, and §4
requires only a non-empty `type` — consumers "MUST NOT reject a Document for an
unrecognized `type`". An `incident` type can be defined wherever this work lands,
with no change to the format. The `backlog-ideas` bundle already does this with
`_types/idea.md`.
