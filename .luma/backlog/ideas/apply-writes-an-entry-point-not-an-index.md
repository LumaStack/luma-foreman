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

**The adapter block carries four things and no knowledge**, since everything it
could state is already stated somewhere a reader can be sent:

- where the entry point is, and that it should be read
- that the block is generated, which command owns it, and that a hand edit is
  discarded on the next run
- how to reach always-on content immediately, rather than on a trigger
- that `/list-bundles` and `/load-bundle` exist

Anything beyond those four is content, and content is what this change moves out.

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

## The shape — one rule, applied at every level

The naive version is an index of everything, which is what exists today. The
replacement is recursive: **each level carries what is always-on here, advertises
what is reachable from here with enough detail to choose, and defers the rest.**

The project's routing does that over bundles. A bundle's own routing does the
same over its documents. Sections within a document would be the same rule again
— the level `loading-mechanisms.md` calls unexplored, reachable only because the
rule generalises.

**Nothing new is declared. The three classes are already computed from
`matches`:**

| `matches` | class | what a router carries |
| --- | --- | --- |
| `always` | **always-on** | the body, present here |
| a list of triggers | **advertised** | the name and its triggers; the body arrives when one matches |
| `nothing`, or absent | **on-demand** | reachable, and nothing is spent until something asks |

**Workflows appear at no level.** `.claude/skills/` already carries them.

**Depth is the design, not a defect.** A document may sit several hops in — the
project names a bundle, the bundle's routing names some of its documents, one of
those links to another. That is what makes standing cost per-bundle rather than
per-document, and it is what the scale pressure demands.

**The trade: cost stops being knowable in advance.** `CLAUDE.md` can be measured
today and a session cost quoted. Under this, cost depends on the path walked — a
large knowable number exchanged for a small path-dependent one. Measurement moves
from *measure the artifact* to *measure a session*, which is a different
discipline and probably a different tool.

The CSS case is the test: nothing about a CSS bundle in context while nobody
touches CSS, but enough present to reach for it when somebody does.

## Most of the runtime half already exists, and is asleep

`apply` already generates `.luma/bundles/routing.toml` — `apply.py:440`. In this
repository it is 9,231 bytes holding 29 rules, one per document that declares a
trigger, with `bundle`, `document`, `title`, `path`, `on_violation` and
`matches`.

**It has one consumer and it does nothing.** `agent_permissions/gate.py:128`
reads only the rows that block; all 29 rows are `on_violation = "allow"`. So
nothing reads this file in practice.

**All 29 rules are policies. No workflow in the catalog declares a trigger at
all**, which is independent support for leaving them to `.claude/skills/`.

**The trigger split, measured.** A rule may declare several, so these are trigger
mentions across the 29:

| trigger | mentions | evaluated by |
| --- | --- | --- |
| `topic:` | 20 | **the model only** |
| `command:` | 10 | a hook, deterministically |
| `event:` | 7 | a hook, deterministically |
| `path:` | 7 | a hook, deterministically |

**By rule, which is what the design turns on: 9 are deliverable by hook alone; 20
declare at least one `topic:`.** The nine are `never-commit-credentials`,
`never-commit-private-identity`, `merge-commits`, `changelog`, `release-notes`,
`luma-directory-layout`, `readme`, `the-project-descriptor` and
`session-continuity`.

So roughly a third of the surface can be enforced and the rest cannot. `topic:`
is a model judgement by construction — the design must say which rules are
guaranteed and which are advisory, or a table that mixes them reads as though all
29 are policed.

**What the table is missing:** no `description` field, and no bundle-level rows
at all. The project level needs bundle descriptions; a bundle's own level needs
document descriptions. That is the concrete delta.

## Four ways a level below can load, and none is sufficient alone

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
- **No migration is needed, which was recorded wrongly here.** This entry claimed
  `CLAUDE.md` has no markers and the first run would have to recognise an
  unmarked form. It has them — `<!-- luma:begin … -->` and `<!-- luma:end -->`,
  `apply.py:59`. **The marker mechanism already exists and works**; what changes
  is only what goes between them. Worth noticing that this repository's
  `CLAUDE.md` is *entirely* managed block, so there is currently no hand-written
  content for the shared writer to preserve — which the design must not assume,
  since an adopting project will have some.

**Rejected: `init` installing a default bundle so the empty case never occurs.**
It needs a network and a catalog at `init` time, there is no way to un-adopt what
it installs — [[no-way-to-un-adopt]] — and naming a specific bundle compiles a
catalog into the engine, which fails the estate's own test that an engine
contains no knowledge of luma specifically. *What a new consumer begins with* is
`starters` in `luma/catalog`, keyed on what the repository declares itself to be.
An empty state that is rare is worse than one that is correct.

## What is named where, and what is merely reachable — settled

`loading-mechanisms.md` holds that *existence is cheap and content is expensive,
so every policy and workflow is named whatever its class*, reasoning that **a
rule nobody can see governs nothing.** Read as *everything gets a line at the top
level*, that is flat and per-document — which is what the same document's scale
pressure kills. The tension is inside the settled position rather than between it
and this one, and it resolves by separating loading from integrity.

**Loading — a document is not hoisted merely because nothing else would deliver
it.** Reached through a bundle, through a trigger, or through a link from a
document that is itself reachable, it is properly reached however many hops that
takes. Burying a document behind layers is the intended outcome, not a
compromise.

**Integrity — a document with no inbound path at all is a defect, and `inspect`
reports it.** A reachability check over a graph foreman already holds:

- **roots** — documents declaring `matches: always`, and every adopted bundle,
  since `/list-bundles` and `/load-bundle` make each one reachable on request
- **edges** — a bundle to the documents its routing names, a trigger to its
  document, a document to whatever it links to

Unreachable means no trigger, not named by its bundle's routing, and no inbound
link from anything reachable. It belongs in `inspect/rules/bundles.py`, which
already holds the nearest relative — *a `path:` glob matching nothing in this
project*, reported because it parses, publishes and never fires. **A warning, not
an error**, on the reasoning `vocabulary.py` already gives for its own rule: a
tool cannot tell an orphan from something reached by a path it cannot model, so
the reader decides whether an indirect path is acceptable.

**Two consequences.**

- **A broken wikilink changes severity.** `audit-bundle` treats one as a tidiness
  defect. Once links are a delivery mechanism, a broken link is a document that
  silently stopped being reachable.
- **A trigger edge is only real if something walks it.** The nine hook-deliverable
  policies are deferred on the grounds that a hook will deliver them. Where no
  gate is installed, nothing does — and the reachability check still passes,
  because the edge exists in the graph whether or not anything traverses it.
  **Whether a gate is wired up is machine-local state, so a repository cannot
  answer it**, which is why this is not simply a stricter check. Two candidate
  answers, neither taken: report it as a machine-scoped notice rather than a
  repository finding, or have the adapter name hook-deliverable documents when it
  can see no gate, so the saving is claimed only where the mechanism justifying
  it exists.
- **The check will pass on a hole it cannot see.** A `topic:` document is
  reachable in the graph through its bundle, but that first edge is a model
  judgement made from a bundle description. `capturing-ideas` declares
  `topic:capturing an idea worth keeping` inside `backlog-ideas`; an idea
  surfaces during unrelated work, nothing opens that bundle, the graph is intact,
  and the document never arrives. Not an argument for hoisting it — an argument
  that **bundle descriptions are load-bearing infrastructure**, and possibly a
  second, softer rule: a bundle whose documents declare topics its own
  description does not hint at.

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

**Answers [[preload-levels-collapse-into-emphasis]]**, which found the declared
levels collapse into emphasis once written into a harness, and left two readings
open: the ladder is over-specified, or the harness is the limitation. **It was
the mechanism.** A flat index has one delivery moment, so everything below
always-on renders identically; a router at every level has as many delivery
moments as it has levels, and the distinction lands. That entry's argument
against inlining bodies is untouched and still holds.

**Meets [[bundle-routines]] where a bundle's own routing lives.** That entry asks
what a bundle exposes — named routines rather than one `entry_point`. This one
asks what loads whichever of those a situation calls for. They should be designed
together: *a bundle's routing* here and *a folder of entry points* there are
plausibly the same artifact under two names.

**None of this reached `luma-leader` by any mechanism.** The `.luma/` tier
question above belongs there and is recorded here because there is nowhere else
to put it.
