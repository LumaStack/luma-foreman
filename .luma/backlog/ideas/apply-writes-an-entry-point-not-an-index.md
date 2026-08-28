---
type: luma/idea
title: apply writes an entry point, not an index into CLAUDE.md
created: { by: human:benlinton, at: 2026-08-27T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
---

# `apply` writes an entry point, not an index into `CLAUDE.md`

**`apply` should stop writing content into `CLAUDE.md` and start generating a
harness-neutral entry point that `CLAUDE.md` merely points at.** `CLAUDE.md`
keeps a small generated block — the adapter — and nothing else.

**Wanted before adopting more bundles**, because every bundle added under the
current shape makes the thing that has to be replaced larger.

## Why, and it is not tokens

Three reasons, none of which is context cost:

- **More than one harness can load the luma system.** One artifact that every
  adapter points at, rather than a rendering per harness.
- **`CLAUDE.md` stops churning.** Today every `get` rewrites it, so it conflicts
  on every parallel branch.
- **Routing moves somewhere a hook can police it.** Enforcement needs data at a
  known path, not prose in a harness file.

**Moving the index out of `CLAUDE.md` saves nothing on its own.** An `@path`
import is inlined at session start, so the bytes arrive either way. Every token
saved comes from *what stops being written*, not from where it is written.
Worth stating because the file move looks like the saving and is not.

## What it costs today

Measured in this repository at 17 adopted bundles, 2026-08-27:

| | |
| --- | --- |
| `CLAUDE.md` | 21,646 characters, about 5,300 tokens, every session |
| of which workflow lines | 8,451 characters — **byte-identical** to descriptions Claude Code already loads from skill frontmatter |
| skills generated | 40 |
| documents indexed | 69, across 17 bundles |

**The duplicate is roughly 2,100 tokens a session, paid twice to one harness.**
Dropping it saves only the duplication — those 40 skills still load their names
and descriptions at startup.

## The shape

| ring | content | present |
| --- | --- | --- |
| **0** | the adapter block in `CLAUDE.md` — rules, and how to reach the rest | always; written once, rewritten in place |
| **1** | always-on policy bodies; bundle names and descriptions | always |
| **2** | a bundle's documents, their descriptions and triggers | when that bundle is reached for |

**Workflows appear in none of them.** `.claude/skills/` already carries them.

The CSS case is the test: nothing about a CSS bundle should be in context while
nobody touches CSS, but enough must be present to reach for it when somebody
does — and reaching for it loads that bundle's own routing, which loads what the
rules say.

## Most of the runtime half already exists, and is asleep

`apply` already generates `.luma/bundles/routing.toml` — `apply.py:440`. In this
repository it is 9,231 bytes holding 29 rules, one per document that declares a
trigger, with `bundle`, `document`, `title`, `path`, `on_violation` and
`matches`.

**It has one consumer and it does nothing.** `agent_permissions/gate.py:128`
reads only the rows that block; all 29 rows are `on_violation = "allow"`. So
nothing reads this file in practice.

**The trigger split, measured:**

| trigger | count | evaluated by |
| --- | --- | --- |
| `path:` | 6 | a hook, deterministically |
| `command:` | 6 | a hook, deterministically |
| `event:` | 2 | a hook, deterministically |
| `topic:` | 15 | **the model only** |

About half the routing surface is enforceable and half is not, and the half that
is not is most of the policy triggers. `topic:` is a model judgement by
construction — the design must say which rules are guaranteed and which are
advisory, or a table that mixes them reads as though all 29 are policed.

**What the table is missing** for the rings above: no `description` field, and no
bundle-level rows at all. Ring 1 needs bundle descriptions; ring 2 needs document
descriptions. That is the concrete delta.

## Four ways ring 2 can load, and none of them is sufficient alone

- **Prose the model follows.** Free, and degrades silently.
- **A hook injects it.** Deterministic, but hooks fire on tool calls — nothing
  fires on *let us work on CSS*.
- **A skill per bundle** — description is the bundle description, body is that
  bundle's routing. Native progressive disclosure, using a mechanism already paid
  for. Costs one description per bundle at startup, and trades against today's
  skill-per-workflow, which is what gives direct invocation by name.
- **Explicit `/load-bundle` and `/list-bundles`.** One skill each regardless of
  bundle count. **The only mechanism that cannot degrade**, because it does not
  depend on anything noticing — the floor the other three sit on, not a fallback.
  `/list-bundles` is also the natural home for what is adopted *and* what is
  merely available, which nothing addresses today.

Explicit loading must not be the only route. Automatic and deliberate are
complementary, and the cost does not scale twice.

## `init` and `apply` share one writer

Both call one idempotent function that finds or creates a marked block in
`CLAUDE.md` and rewrites it. `init` then has a working adapter from the first
commit rather than from the first `get`.

**Two things this needs:**

- **`apply` must stop treating an empty project as an error.** `apply.py:578`
  prints `nothing adopted` and returns 2. Under this design a repository with no
  bundles is a legitimate state whose correct output is the adapter block plus a
  stub entry point saying so. Making the empty case correct also makes `apply`
  safe to run from four places, which is what a generated artifact needs.
- **The first run has to migrate.** Today's `CLAUDE.md` has no markers, so the
  block must recognise and replace the current unmarked form rather than
  appending a second index beside it.

**Rejected: `init` installing a default bundle so the empty case never occurs.**
It needs a network and a catalog at `init` time, there is no way to un-adopt what
it installs — [[no-way-to-un-adopt]] — and naming a specific bundle compiles a
catalog into the engine, which fails the estate's own test that an engine
contains no knowledge of luma specifically. *What a new consumer begins with* is
`starters` in `luma/catalog`, keyed on what the repository declares itself to be.
An empty state that is rare is worse than one that is correct.

## Open

**What is a derived artifact's home?** `luma-leader`'s `DECISIONS.md` says
generated adapters stay outside `.luma/`, but its premise is stale — it reads
*generated from `policy/`*, and a later decision in the same file removed
`policy/`. It also fuses a platform fact with a principle: *live where the tool
looks* is not a choice for `CLAUDE.md`, while *nothing generated is ever the
source* is durable and says nothing about location. The rule that survives is
**a generated artifact lives where its reader looks** — a harness's location if a
harness reads it, `.luma/` if luma's own tooling does. That explains
`routing.toml` living inside `.luma/` today.

**Derived is not cache.** Derived is provenance; committed is storage; they are
independent. The test for committing is **does anything have to read it without
the tool that made it** — a bare clone, a runtime gate that fails open if it is
missing, another harness. Yes means committed. No means a cache, and a cache
cannot live under `.luma/` at all, because everything there is committed without
exception. The deferred `cache/` tier argues for a home inside `.luma/` and
justifies it with a `.gitignore` line, which is a contradiction rather than a
hard call. **The real gap is that committed-derived material has no tier** —
`routing.toml` sits in `bundles/` and is not a bundle. *Belongs to
`luma-leader`.*

**What to call the new tier and its files — not a blocker, and no name here is
sacred.** `routing` is currently spoken for by the permission gate and
`index.md` is reserved at a bundle root rather than a project root, but that is
a constraint to know about rather than one to design around. **The collision
resolves in either direction**: `routing.toml` holds a permission table, which is
the narrower job, so it may be the file that should move. Every copy of it lives
in a repository we own and is days old, which is the cheapest this rename will
ever be.

**Per-tool subsections in the adapter block: no, not yet.** One writer today, and
structure is cheap to add later.

**A conflict to settle before building.** `loading-mechanisms.md` settled that
*existence is cheap and content is expensive, so every policy and workflow is
named whatever its class* — everything gets a ring 1 line. The ring design above
defers document names to ring 2. Those disagree about the same bytes. A possible
reconciliation, since that position was reasoned from *a rule nobody can see
governs nothing*: policies named at ring 1 always, workflows omitted entirely,
background never named.

## Notes

**No document in this repository declares `matches: always` today** — every
occurrence is prose discussing the value. The always-on tier is empty, so the
hoisting path is currently untestable against the catalog. Declarations are
expected soon, which is an argument for building that path now, while it is
trivial to verify.

**Not a variation of [[routers]]**, which is the concept — conditional loading,
prose or data, whose router — at `horizon: someday`. This is the implementation
it would land in, with measurements, and it answers part of that entry's central
question: the evaluator decides the form, and `routing.toml` is already the data
half.

**Extends [[preload-levels-collapse-into-emphasis]]**, which found that the three
levels collapse when written into a harness and argued against inlining bodies
into `CLAUDE.md`. That argument holds and this does not contradict it — the index
stays an index; it moves and sheds what is duplicated.

**Meets [[bundle-routines]] at ring 2.** That entry asks what a bundle exposes —
named routines rather than one `entry_point`. This one asks what loads whichever
of those a situation calls for. They should be designed together: *a bundle's own
routing* here and *a folder of entry points* there are plausibly the same
artifact under two names.

**None of this reached `luma-leader` by any mechanism.** The `.luma/` tier
question above belongs there and is recorded here because there is nowhere else
to put it.
