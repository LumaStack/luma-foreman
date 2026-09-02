---
type: decision
title: Apply writes adapters
decided: 2026-08-23
lifecycle: draft
reopen_trigger: A harness appears that cannot follow a file path from a skill body, or measurement shows the extra read costs more than the duplication would.
---

# ADR-0001: Apply writes adapters

## Summary

`luma-foreman apply` writes a pointer to each adopted document and avoids duplicating
document contents.

## Problem

An adopted bundle sits in `.luma/bundles/`, where no agent looks unless
something points at it. Each adopted document has to be placed in front of the
harness, and harnesses differ in what they will accept — Claude Code reads
skills from `.claude/skills/` and context from `CLAUDE.md`, where another may
follow a plain path it is handed.

The straightforward way to do that is to copy each document's text into the
file its harness reads. Most generators work exactly like that — read a source,
write the output, and the output is what gets used.

Here that costs two things. The copy becomes a second version of the document
that nothing keeps in step, and it loads on every session whether the work
needs it or not. Neither cost is visible at the moment you choose it, and both
grow with every bundle adopted.

## Decision

**An adapter is a file `apply` generates so a harness can reach a document it
would otherwise never find.** It carries whatever that harness needs in order to
recognise the file, a path to the real document under `.luma/`, and nothing
else. Two kinds exist today: a skill per procedure, and the block in `CLAUDE.md`.
Both are generated, both are disposable, and neither is a source of truth.

**A general form is preferred wherever one works.** Something harness-specific
is reached for only where a harness requires it, or where it demonstrably beats
the general form. It is a cost to be justified, not the default — which is why
the ring is written once and each harness gets a pointer at it rather than a
rendering of its own.

**A generated `SKILL.md` carries harness frontmatter, a path to the real
document under `.luma/`, and the standing context that document assumes.** It
does not carry the document body.

**Below the body, an adapter carries the least that makes the harness behave
well** — and behaving well includes the agent actually following the pointer.
Claude Code decides what to invoke from a skill's description alone, so the
description is copied into the frontmatter, without which the skill is
unreachable. A generated skill also says why it points elsewhere and warns
against editing the vendored copy: neither is required to make it resolve, and
an adapter that gets obeyed is worth more than one that is merely small.

**What is never traded is the body.** Everything above it is a judgement about
the least that works, and reasonable people will put the line in slightly
different places. The body is not a judgement — it is the second source of truth
this record exists to prevent, and no gain in behaviour buys it.

**The same reasoning runs the other way.** Where a harness already carries
something, the adapter does not repeat it — workflows are left out of a ring
because the harness has loaded their names and descriptions already.

**What reaches `CLAUDE.md` is a pointer, not content** — an instruction to read
the project's entry point, and nothing about what any bundle holds. The entry
point carries a line per bundle, and each bundle's ring carries a line per
document, saying what exists and what brings it into play. Never a summary and
never an excerpt.

**A line is not a copy.** A generated file may carry a document's title,
description and `matches` — enough for a reader to tell what exists and what
brings it into play, without opening anything.

## Why

**A copy is a second source of truth, and this one is a copy of a copy.** The
vendored bundle is already a copy of the catalog's, checksummed so drift is
detectable. Pasting its content into `.claude/` produces a third artifact that
nothing checksums — so an edit there is invisible to the drift rule, which is
watching the wrong file.

**The cost lands on every session, and the author cannot see it.** Content
inlined into `CLAUDE.md` loads whether or not the work touches it. One bundle's
always-on document measured 1,262 words; a project with eight adopted bundles
pays for all eight while doing something none of them govern. The person who
declares a document always-on in a catalog has no view of what else an adopting
project adopted.

**The read is cheap and it is conditional.** An agent that matches a skill
description opens one file. An agent that does not, opens nothing.

## Alternatives

**Inline the content.** Guarantees the text is in context. Rejected on the three
grounds above; the deciding one is that *load this before the work it governs*
and *load this in every session* are different instructions, and inlining
conflates them.

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
- The entry point is a rounding error against a single always-on document, and
  it covers everything adopted.
- A consumer can always see what it is *not* loading, which is what stops
  *nothing applies here* being indistinguishable from *I did not look*.

**Cons**
- An agent must perform one extra read to act on a workflow, and an agent that
  ignores the pointer gets nothing.
- The entry point says a document exists and not what it says, so a rule can be
  skipped by a reader who decides the line does not apply to them.

## Assumptions

That a harness will follow a relative path given in a skill body. True of Claude
Code; untested elsewhere, and the first harness where it is false reopens this.

## Measured, 2026-08-23

Three bundles, eleven documents, four of them declared to load in every session:

| | words |
| --- | --- |
| those four, if inlined | **3,176** |
| the index that replaces them | **682** |

**21% of the cost, covering eleven documents rather than four.** The position
was taken before any of this was measured.

## References

- Implements [`policy/an-index-of-what-exists`](https://github.com/LumaStack/luma-catalog/blob/7b2a0f6f29f29155092a7e5a92023a09bd419cbd/catalog/bundles/bundle-manager/policy/an-index-of-what-exists.md) in `lumastack/luma-catalog/bundle-manager`
