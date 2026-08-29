---
type: slice
title: ADR-0001, and the scope change that made this a prose sweep
created: 2026-08-29
covers:
  - .luma/records/decisions/ADR-0001-apply-writes-adapters-not-copies.md
contributors:
  - human:benlinton
  - agent:claude-opus-5
---

# 005: decisions

## What this is

**One record of five, and that is the whole slice.** `ADR-0001` was presented,
read closely by the reader over many turns, rewritten substantially, and signed
off. `ADR-0002` through `ADR-0005` are untouched.

**It also carried the scope change.** All remaining code left the sweep at this
slice — the reader excluded `src/`, `tests/` and `bin/` to finish the prose and
read the code in a sweep of its own. That landed separately as PR #101.

**And it survived a mid-slice clear.** The session was cleared with the file
open; the cross-check was in the journal, so the next session resumed without
re-deriving it. That is the journal doing the job it was added for.

## What we made of it

**Every finding came from running something, and none from careful reading** —
the same result slice 001 reported, on a document nobody had checked in six
days:

| claim | what checking it showed |
| --- | --- |
| `:33-35` the `CLAUDE.md` block is an index, `preload: mandatory` hoisted | the block is four lines and an import; the hoisting was never built and was later reversed |
| `:119` implements a policy in `luma/bundle-manager` | a namespace this repository has never had |
| `:29` a generated `SKILL.md` is frontmatter, path and standing context | exact, verified against a real one |
| `:113` `luma-leader` names cost reporting as the highest-value unbuilt item | exact, at `:305` |

**The record was false in ways nothing could report.** `preload` sits on the
vocabulary rule's exception list, correctly — a record may use a retired word to
say what was decided at the time. But the passage was present tense, describing
a mechanism that no longer existed, and no rule distinguishes those.

**The reader's own reading did the work the agent's could not.** The scope of
the rewrite — dropping `Follow-up` entirely, pulling every mention of a retired
field, cutting the record's commentary on itself — came from the reader
questioning premises the agent had accepted, including several the agent had
written that hour.

## Against the goal

**Served it.** *Nothing here should state something false* — the record stated
three false things and now states none, and the two verified claims are recorded
as verified so nobody re-derives them.

**And it produced the goal's sharpest case yet.** `:33-35` was true when
written, false when read, and invisible to every mechanical check. The fix was
not a correction but a separation: state what was decided, and say separately
where it currently lives. **A record that mixes decision and mechanism goes
false every time the mechanism moves.**

## Where it went

| finding | destination |
| --- | --- |
| the whole rewrite | the record itself, PR #102 |
| cost reporting at `get` time | `.luma/backlog/ideas/report-what-an-adoption-costs.md` |
| nothing checks a citation resolves | `.luma/backlog/ideas/nothing-checks-that-a-citation-resolves.md` |
| `apply.py` uses *adapter* two ways, ships the losing one 43 times | journal — code, out of scope since this slice |
| `apply.py:13` says "Two outputs" above three rows | journal — same |
| `luma-foreman.toml:46` exempts `ADR-0001` for a word it no longer contains | journal — a pending row owns it |
| `charter.md:180` uses `projection`, retired | journal — this sweep's own file |
| `american-spelling.md` is followed 1:70 and its parent standard was deleted | journal — `docs/examples/` is skipped |

## Still open

**Four records unread** — `ADR-0002` through `ADR-0005`. The rules extracted
here apply to all of them: no self-referential prose, no `Follow-up`, references
pinned, no locators for things that move.

**`ADR-0002` through `ADR-0005` still carry the demotion paragraph** dropped
from `ADR-0001` at the reader's instruction. Not swept — a yes to one was
explicitly not a yes to four.

**The rate is the thing to look at before continuing.** One record cost a
session. Four remain.
