---
type: luma/idea
title: Foreman targets Claude Code, and should work for most agentic AI
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
stage: draft
---

# Foreman targets Claude Code, and should work for most agentic AI

**Every adapter foreman writes today is a Claude Code adapter.** `apply` writes
`.claude/skills/` and a managed block in `CLAUDE.md`, and nothing else. The
knowledge underneath is harness-neutral by construction — the entry point and
the rings are written once — **so the coupling is one layer thick and is the
layer nobody has widened.**

## What that layer would have to carry

- **A second harness at all.** `AGENTS.md` is the obvious next target, and until
  something other than Claude Code consumes what `apply` writes, *harness-
  neutral* is a claim rather than a demonstrated property.
- **More than skills.** Workflows reach an agent as skills; **scripts, assets
  and anything that is not a procedure have no projection at all.** See
  [[no-format-for-non-procedural-knowledge]], which is the format-side half of
  the same gap.

## Why it is not urgent

**Skill distribution is close to solved** — `SKILL.md` is an open standard and
many agents read it, so one output written to that standard covers most of the
surface without an adapter each.
The `hook-delivery` plan argues the exception: hooks have no standard, so they
are where per-harness work is genuinely owed.

**So the honest shape may be one standard output plus per-harness hooks**, which
is much less than *an adapter per agent* and worth confirming before anyone
builds the general case.

## Notes

Absorbed from `docs/scope.md` when that document was scattered on 2026-08-29,
where it was two bullets under *what is not built* with no argument attached.
