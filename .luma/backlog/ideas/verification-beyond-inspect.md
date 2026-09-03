---
type: luma/idea
title: Verification beyond inspect — compliance, mandates, and rot
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
stage: draft
---

# Verification beyond inspect — compliance, mandates, and rot

**`inspect` checks a project's structure. None of it checks whether the project
is actually being run the way it says.** Five rules — identity, secrets, bundle
structure, adoption drift, vocabulary — and every one of them reads the tree.

## What is not built

- **Keeping projects in compliance**, rather than reporting a snapshot of it.
- **Mandates handed down from an organization**, probably through the catalog.
  Claude Code's `managed` install scope is an obligation mechanism already
  designed and worth reading first — see
  [[distribution-beyond-clone-and-symlink]].
- **Rot, sought and destroyed.**
- **Observation and auditing** of the system as a whole.

## Rot is two problems and only one is buildable

**Mechanical rot is checkable now**: a dead link, a checksum mismatch, a bundle
five versions behind. Every one has a referent a rule can read.

**The other kind has no referent.** A policy nobody follows, a document still
accurate but no longer read, a re-open condition that quietly fired. **These are
not detectable by reading the file** — they are facts about behaviour around the
file, and a rule that guessed at them would fail in the permissive direction,
which is the worse one.

So the split is the design: build the mechanical half as `inspect` rules, and
treat the rest as something a person or an agent finds by reading. **A review
sweep is one answer to the second half**, which is worth noticing given one is
running.

## The frontmatter is the missing mechanism

**Nothing in a bundle's frontmatter lets tooling enforce anything.**
`.luma/PROJECT.md`'s `owns` and `must_not_own` are the live example — list
syntax and free-text values, so they *look* structured and nothing can validate,
match against, or enforce them. **Prose treated like data.**

Any of the above needs fields a tool can evaluate, so this is upstream of the
rest of the entry rather than beside it.

## Notes

Absorbed from `docs/scope.md` when that document was scattered on 2026-08-29,
where *verification* was four bullets with no argument. The frontmatter half was
found separately while reading `.luma/PROJECT.md` in the same sweep.
