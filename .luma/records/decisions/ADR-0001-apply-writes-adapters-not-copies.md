---
type: decision
title: Apply writes adapters, never copies of a document
decided: 2026-08-23
lifecycle_status: provisional
reopen_trigger: A harness appears that cannot follow a file path from a skill body, or measurement shows the extra read costs more than the duplication would.
---

# ADR-0001: Apply writes adapters, never copies of a document

## Summary

`luma-foreman apply` writes a pointer to each adopted document and never a copy
of its content.

## Problem

An adopted bundle sits in `.luma/bundles/` and no agent knows it is there.
Something has to put it in front of a harness, and a harness reads its own
formats — `SKILL.md` for Claude Code, `CLAUDE.md` at the project root.

The obvious implementation writes the document's content into those files, and
it is obvious because it is what a build step normally does.

## Decision

**A generated `SKILL.md` carries harness frontmatter, a path to the real
document under `.luma/`, and the standing context that document assumes.** It
does not carry the document body.

**The `CLAUDE.md` block is an index**: one line per document saying what it is,
with `preload: mandatory` documents hoisted into a *read these first* section.
Not a summary and not an excerpt — a line.

## Why

**A copy is a second source of truth, and this one is a copy of a copy.** The
vendored bundle is already a copy of the catalog's, checksummed so drift is
detectable. Pasting its content into `.claude/` produces a third artifact that
nothing checksums — so an edit there is invisible to the drift rule, which is
watching the wrong file.

**The cost lands on every session, and the author cannot see it.** Content
inlined into `CLAUDE.md` loads whether or not the work touches it. One bundle's
mandatory document measured 1,262 words; a project with eight adopted bundles
pays for all eight while doing something none of them govern. The person
declaring `preload: mandatory` in a catalog has no view of what else an adopting
project adopted.

**The read is cheap and it is conditional.** An agent that matches a skill
description opens one file. An agent that does not, opens nothing — which is the
behaviour the whole `preload` ladder is trying to describe.

## Alternatives

**Inline the content.** Guarantees the text is in context. Rejected on the three
grounds above; the deciding one is that `preload: mandatory` means *before work
this governs*, not *every session*, and inlining conflates them.

**Symlink `.claude/skills/<name>` at the bundle directory.** No copy, no
staleness. Rejected because a `SKILL.md` needs frontmatter the source document
does not have, and because symlinks in a committed tree behave differently
across platforms and archives.

**Generate nothing and document the paths in a README.** Free. Rejected because
it is the status quo, and the status quo is a person telling an agent where to
look every time.

## Tradeoffs

**Pros**
- One source of truth. The vendored copy is the only place the text exists.
- The index is a rounding error against a single preloaded document, and it
  covers everything adopted.
- A consumer can always see what it is *not* loading, which is what stops
  *nothing applies here* being indistinguishable from *I did not look*.

**Cons**
- An agent must perform one extra read to act on a workflow, and an agent that
  ignores the pointer gets nothing.
- The index says a document exists and not what it says, so a rule can be
  skipped by a reader who decides the line does not apply to them.

## Assumptions

That a harness will follow a relative path given in a skill body. True of Claude
Code; untested elsewhere, and the first harness where it is false reopens this.

## Measured, 2026-08-23

*Added the day two more bundles were adopted. The position is unchanged; this is
the evidence it was decided without.*

Three bundles, eleven documents, four of them `preload: mandatory`:

| | words |
| --- | --- |
| the mandatory set, if inlined | **3,176** |
| the index that replaces it | **682** |

**The index costs 21% of inlining and covers eleven documents rather than
four.** At this rate the fifteen bundles in the catalog would put roughly 16,000
words into every session — which is the ceiling this decision was guessing at,
now with a number against it.

## Follow-up

`preload` levels currently differ only in emphasis once written this way —
recorded in `.luma/backlog/ideas/preload-levels-collapse-into-emphasis.md`.

**Reporting this number at adopt time** is the cheap version of the same
insight, and is unbuilt — `luma-leader/docs/adoption-use-cases.md` names it as
the highest-value item nobody has built.

## References

Implements the *an index of what exists* policy in the `luma/bundle-manager`
bundle, which named the pattern after it had been rediscovered three times.
