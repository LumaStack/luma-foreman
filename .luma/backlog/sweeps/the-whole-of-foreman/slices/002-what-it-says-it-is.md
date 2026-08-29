---
type: slice
title: What this project says it is
created: 2026-08-29
covers:
  - CLAUDE.md
  - .luma/PROJECT.md
  - docs/scope.md
contributors:
  - human:benlinton
  - agent:claude-opus-5
---

# 002: what it says it is

## What this is

The three documents a newcomer reads to learn what foreman is, after
`README.md`. Two survived. **One was deleted.**

## What we made of it

| file | outcome | |
| --- | --- | --- |
| `CLAUDE.md` | clean | approved |
| `.luma/PROJECT.md` | findings | **read closely and deliberately not signed off** |
| `docs/scope.md` | findings | **scattered into eleven files and deleted** |

### `.luma/PROJECT.md` — read, not approved

**`:5` was the sweep's first confirmed churn-damage finding.** *"Eventually
adoption"* was true when written and false since — `get`, `apply`, `bundle` and
`catalog` all ship and this sweep had used every one of them that day. `owns`
has the same gap from the same cause.

**And the frontmatter is prose treated like data.** `owns` and `must_not_own`
have list syntax and free-text values, so they look structured and nothing can
validate, match against, or enforce them. Recorded in the journal rather than
routed, because the shape is a direction and not yet a task.

**The row is `reviewed_by: human:benlinton` with `approved_by` empty**, which is
the state that drove `review-sweeps` 0.18.0. Under `approval: recommended` that
is a known compromise, not a shortfall.

### `docs/scope.md` — the first file the sweep removed rather than fixed

**It was the repository's first document, created 2026-08-19, and it had
outgrown its duties.** Five jobs in one file: a status table, a roadmap, the
arguments behind the roadmap, an architectural hazard, and prior art. No name
fit it, which is what made the question *should it be renamed* the wrong
question.

**`:18` was false in the way `architecture.md:102` had already been false** —
*"an index of everything adopted in a managed block in `CLAUDE.md`"*, against
`apply.py:19`, which says the block *"points at the entrypoint and carries
nothing else."* The reader had struck that claim out of `architecture.md` in
slice 001. It survived here because the two were read in different slices.

**Seven of its thirteen pieces were already recorded elsewhere**, each cited
back to `scope.md` only because `scope.md` came first. The citations were what
kept it alive.

## The ledger

**Every line range, and what happened to it.** `git show` for this slice is the
diff; this table says what to look for in it.

| lines | what it held | verdict | where it went |
| --- | --- | --- | --- |
| 12–21 | status table of the six commands | **dropped** | superseded by `docs/commands.md` |
| 18 | *an index in `CLAUDE.md`* | **dropped as false** | contradicted by `apply.py:19`. Carried nowhere |
| 19 | `inspect`'s rules, four of five | **dropped as stale** | `vocabulary.py` was missing from the list |
| 23–26 | *`agent-permissions` is unrelated* | **dropped** | already near-verbatim at `architecture.md:128` |
| 32–33 | share more than skills; resolve dependencies | rewritten | `independent-of-the-harness`, ADR-0002 |
| 35 | be independent of Claude Code | rewritten | **new** `independent-of-the-harness` |
| 39–44 | select at write time, load/unload skills | **dropped** | already at `personal-skill-selection:37` |
| 45 | frontmatter that enforces governance | rewritten | **new** `verification-beyond-inspect` |
| 49–52 | routing bullets | **dropped** | already at `routers:94` |
| 54–65 | routing is the mechanism, tokens the objective | **moved** | `apply-writes-an-entry-point-not-an-index` |
| 69–73 | verification — compliance, mandates, rot, audit | rewritten | **new** `verification-beyond-inspect` |
| 77–78 | feedback — alerts, learn and improve | rewritten | **new** `feedback-and-learning` |
| 84–88 | mid-session swapping needs cooperation | **dropped** | already at `personal-skill-selection:44` |
| 92–99 | do luma's own standards live outside luma tooling | **moved** | `which-bundles-this-project-should-carry` |
| 100–101 | ship natively, or fetch everything | **dropped** | already at `which-bundles:30` |
| 105–108 | routing: prose or data | **dropped** | already at `routers:94`, reframed better there |
| 109–114 | two policies conflict and nothing happens | **moved** | ADR-0002, which had cited this as its source |
| 115–117 | the no-build-step promise | **dropped** | already at `distribution:28` |
| 121–123 | rot is mechanical and not | **moved** | **new** `verification-beyond-inspect` |
| 124 | learn and improve | **moved** | **new** `feedback-and-learning` |
| 125–127 | tooling and hooks may not be foreman's | **moved** | `plans/hook-delivery` |
| 129–142 | a regex that fails open | **moved verbatim** | `docs/architecture.md` |
| 148–150 | `SKILL.md` is a standard; adapters are for hooks | rewritten | `plans/hook-delivery` |
| 148 | *"read by 40+ agents"* | **dropped as unsourced** | a count with no source. Carried nowhere |
| 151–156 | Claude Code plugins are a real package manager | **moved** | `distribution-beyond-clone-and-symlink` |
| 157–160 | nobody has a format for non-procedural knowledge | **moved** | **new** `no-format-for-non-procedural-knowledge` |
| 161–163 | plugins cache uncommitted; no offline reproduce | **moved** | `distribution`, and it is ADR-0002's evidence |

**Three claims were dropped as wrong rather than moved** — `:18`, `:19` and the
`40+` count. **Nothing false was carried forward**, which is the thing this
table exists to let somebody check.

## Where it went

| what | where |
| --- | --- |
| four new ideas | `independent-of-the-harness`, `no-format-for-non-procedural-knowledge`, `verification-beyond-inspect`, `feedback-and-learning` |
| four ideas absorbed what they had been citing | `routers`, `distribution-…`, `personal-skill-selection-…`, `which-bundles-…`, `apply-writes-an-entry-point-…` |
| an invariant | `docs/architecture.md` |
| an argument a record had deferred | ADR-0002 |
| two adapters' worth of reasoning | `plans/hook-delivery` |
| `.luma/PROJECT.md`'s rework | journal, deliberately not routed |

**`no-format-for-non-procedural-knowledge` belongs in `luma-knowledge-format`,
not here.** Filed in foreman's backlog because that is where it was found, with
the note that it should move — the same handling `routers` already uses.

## Against the goal

**Both halves of the goal fired in one slice.** `.luma/PROJECT.md:5` is churn
damage; `docs/scope.md:18` was false on creation. The corrected goal caught
both, and the original would have caught only the first.

**And `cross-check` held as the primary method for the third slice running.**
Every mechanical finding came from running something — `apply.py`, the rules on
disk, `init.py`, `match.py`, `store.py`. Careful reading found only claims with
no referent, which in `scope.md` was most of the file.

## Where the practice fought us

**A document can be superseded rather than wrong, and coverage had no way to
say so.** `docs/scope.md` was read, produced findings, and then ceased to
exist. The row carries `outcome: findings` and a struck-through path, which
works — but the sweep found it by improvising, not by following anything.

**Two link conventions were invented mid-scatter and caught before they
shipped** — a wikilink to an ADR and a path-form wikilink, neither of which this
repository uses. **A scatter is exactly where a new convention rides along
unnoticed**, because attention is on the content being moved.
