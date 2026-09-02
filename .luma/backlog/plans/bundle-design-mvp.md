---
type: document
title: Bundle design MVP
description: The design for loading bundles and context — one declaration on a document, loading postures derived from it, an index in every container, what apply compiles for a harness now, and the eventual state the same declarations grow into.
lifecycle: draft
created: { by: agent:claude-fable-5, at: 2026-09-01T00:00:00Z }
---

# Bundle design MVP

**Carved from the [bundle design exploration](bundle-design-exploration.md),
which stays the reasoning record.** That document argues; this one decides.
Nothing is carried by citation and nothing is inherited from the prototype —
the generated rings directory, the routing table, and the classification
flags that exist in code today are measured against this design, not the
reverse. Where
something below matches what the prototype built, that is the prototype having
guessed right, and where it does not, the prototype loses.

## The thesis

**Settle the declaration; keep the mechanism replaceable.** The exploration's
strongest finding is that the shape of a declaration is expensive to change
later while the machinery under it is not — every adopted bundle carries the
declaration, only one tool carries the mechanism. So the MVP ships one field an
author writes, derives everything else from it, and implements it with the two
mechanisms that already exist in every harness worth supporting: a file the
harness always loads, and a model reading an index. Hooks, logs, and overrides
upgrade the mechanism later without re-authoring a single bundle.

**And promise only what a mechanism keeps.** The MVP makes exactly one
machine-kept guarantee: content routed into the harness's always-loaded chain
is resident at session start. Every conditional load is a model's judgement
over an announcement, and this design says so rather than wrapping model
judgement in a word like *guaranteed* that nothing enforces.

## The declaration

**One field, `matches`, in a document's LKF frontmatter.** It is the author's
claim about when the document applies — written by someone who has never seen
the adopting project, so it claims *when*, never what any project will do
about it.

```yaml
matches: eager        # load when my container loads
matches:              # load when the work matches — any one of them
  - topic: merging
  - command: git merge
# absent              # load only when asked for
```

The vocabulary is `eager`, `topic:`, `path:`, `command:`, `event:`,
`tool:`. In the MVP a model evaluates all of it. The forms are structured
anyway, because `path:`, `command:`, `event:` and `tool:` are exactly what a
machine can evaluate later, and settling the shape now is what makes that
upgrade free. `topic:` is the one that will stay model-evaluated forever,
and that is fine — judging whether work is *about* something is what a model
is for.

**The grammar is the spec's, and it extends by construction.** `eager` and
`nothing` are scalar values of the field, never members of the condition
list — as a list member either could sit beside a condition it silently
renders dead under OR semantics, and a form whose invalid state cannot be
written needs no rule forbidding it. Conditions are a list of single-key
maps — `- command: git commit` — which is already the extensible form: a
condition that ever earns qualifier keys grows them in place, with none
defined until a forcing case. Indexes render conditions in one fixed
compact form, derived one-to-one from the frontmatter — a rendering
concern rather than a second syntax, with the frontmatter authoritative
as everywhere.

**The field is LKF's, core as of spec `v0.0.19`.** `matches` is a core
field on the root — optional everywhere, so any document may say what
surfaces it — with values `eager`, `nothing`, or the condition list, and
absence meaning `nothing`. This design's proposals were taken upstream
and ratified rather than smuggled around the spec: the scope-honest
rename to `eager`, the field's promotion to core, `nothing` kept as the
deliberate form of absence — it says an author decided, where a bare
absence says nothing at all — and the `workflow` type renamed
`procedure`, for the reasons recorded with the procedure mock-up below.

**And `nothing` is never a lock.** The postures say what *volunteers*
content, never what may be reached: a request or a citation loads anything
that landed, `matches: nothing` included, and in the MVP there is no
unreachable state at all. *Blocked, ever* is a different axis by
construction, not merely by choice — a frontmatter field is a declaration
the model can read, and what a model can read is advice, not a wall. A
true block needs something standing between the model and the content, set
by a governing body or an adopter rather than by an author who has no
standing to forbid anything in projects never seen. That is `expose`, and
it stays deferred with the rest of governance.

**The loading posture — which class a document falls into: guaranteed,
offered, or standby — is derived from the matcher's shape, never declared
beside it.** Two fields that can disagree are two fields that will, and the
prototype proved it by growing both. The derivation:

| the matcher | derived posture | which means |
| --- | --- | --- |
| `eager` | **guaranteed** | loads when its container loads; absence is a defect |
| conditions | **offered** | announced in its container's index; the model decides |
| absent | **standby** | nothing volunteers it; a request or a citation is the way in |

These are the exploration's postures, kept as the vocabulary the design
grows into. The `expected` / `optional` split inside *offered* is deferred —
not rejected — because nothing in the MVP can observe a miss, so nothing can
act on the difference. The day a load log exists, the split earns a field.

**`guaranteed` always takes an object.** In the table it promises a body:
loads when its container loads. Machinery can later promise an
*announcement* instead — an offered document's index line re-asserted so
no compaction or clear takes the model's map away, while the body stays
the model's call. Different promises, different machinery, and the word
never appears without saying which is meant — a guarantee with a vague
object reads as more than anything keeps.

**Every posture is container-relative, and the containers chain.** A
document's declaration means *once the thing holding me is in play*. A
document's container is its bundle; a bundle's container is the project; the
project's index is held by the harness, which always loads it. So `eager` on
a document in an ordinary bundle means *required reading the moment this
bundle is opened* and costs nothing until then — while `eager` on the bundle
itself lifts its required documents into every session's floor. One rule,
priced honestly at every level: the chance the container loads, times the
size.

**Two words were rejected for this field, on the same ground.** The value was
`always`, which overclaims scope — on a document it never meant every
session, only every opening of its bundle, and `eager` says *load at the
earliest opportunity, wherever I sit* without naming a container. And the
field itself stays `matches` rather than `trigger`, which overclaims
causation — nothing fires in the MVP, a model judges a relevance claim, and
even eventually only the structured forms under a hook truly trigger while
`topic:` never does. Both words would have started lying the way *guaranteed*
does when nothing keeps it.

## The mock-up — a document's frontmatter

```yaml
---
type: policy
title: Never commit credentials
description: What counts as a credential, which files never belong in a
  repository, and why rotation comes before cleanup.
matches:
  - command: git commit
  - command: git push
  - event: before-commit
lifecycle: stable
created: {by: human:asmith, at: 2026-08-12T09:00:00Z}
modified: {by: agent:claude-fable-5, at: 2026-09-01T16:00:00Z}
---
```

An eager policy differs by one value; a standby reference by one absence:

```yaml
matches: eager          # required reading the moment this bundle is opened
```

```yaml
type: document
title: Scrubbing history
description: What removing something from git history actually takes, and
  what it can never undo.
# no matches — by request, reached by name or by citation
```

**The `description` is the announcement.** Every index line is generated
from this field, so its length is the announcement's length — one sentence
here is one line in the bundle's index, paid in every session that opens
the bundle. This is where the exploration's *an announcement has no natural
size* problem gets its handle: one field, one rendered line, one place to
audit.

**A bundle declares `eager` on its own document.** LKF already defines a
`bundle` type for a bundle's metadata, so `matches: eager` on that
document is what lifts the bundle's required reading into the session
floor — the spec's own shape, no new file.

A procedure's frontmatter is the same shape, and what it omits is the point:

```yaml
---
type: procedure
title: Audit sensitive data
description: Check whether a repository has already published credentials
  or private identity, and decide what each finding is worth. Use before
  making a repository public, or on any repository nobody has checked.
lifecycle: stable
created: {by: human:asmith, at: 2026-08-12T09:00:00Z}
modified: {by: agent:claude-fable-5, at: 2026-09-01T16:00:00Z}
---
```

**No invocable-name field — the name derives from the filename.**
`procedure/audit-sensitive-data.md` installs as `audit-sensitive-data`. A
name field beside a filename is two names that can disagree, and
per-project collisions are the binding's to resolve at apply, not the
author's to predict.

**No `matches` — a procedure's surfacing is harness registration.** Its
description becomes the skill description, registered at startup and paid
in every session's floor, which makes it the most expensive description in
the system: written to be matched against work — what it does, then *use
when* — never to sell. The field stays legal on procedures and unread until
hooks arrive with something to evaluate it.

**And the type is `procedure` — not `workflow`, not `skill`.** The test
that settled it: sometimes this renders as a skill, sometimes as a
command, sometimes — someday — as a workflow, so the source must be named
for the invariant across its renderings, and the invariant is written
steps an agent carries out: a procedure. `workflow` was the prototype's
name, and it both misnames the thing — everywhere else in software a
workflow is an orchestrated multi-step process, which this is not — and
spends the word that future orchestration will want; it stays reserved for
a thing that composes procedures, if that thing ever comes. `skill` came
closest: these are skills in the concept sense, and the package precedent —
npm, cargo, apt: one word, many metadata schemes, disambiguated by
namespace — makes *an LKF skill* defensible. But naming the source after
one of its renderings is the overclaim again — `always` overclaimed scope,
`trigger` causation, `router` agency — it invites the SKILL.md-contract
misreading, and the word wobbles the day a harness renders these as
commands. *Skill* appears only at the harness boundary, where it is true;
*invoke* and *invocable* are the verbs everywhere; and `policy` beside
`procedure` gives the acting types a pair every institution already knows.

Everything else in the frontmatter — lifecycle, provenance events, tags —
is LKF's own business, orthogonal to loading, and deliberately untouched
here.

**Standby is not the weakest tier.** A long reference, a changelog, an
upgrade note — large, specific, and reached by name from a citation or a
request. Its floor cost is zero however much sits behind it, which no other
posture can say.

## Every container has an index

**One rule carries the whole loading structure.** Every container has an
index. A container is entered by reading its index. An index names each
member, what it is for, and what brings it into play. The project is a
container of bundles; a bundle is a container of documents; a catalog, an
organization, or a sectioned document can each join the system later by
getting an index, not by getting a new concept — which is how this grows
without gutting anything.

**The word is `index`, and the precedent is `index.html`.** Every directory
of the web has one, you enter through it, and it links inward to the next
level — thirty years of doing exactly this job, needing no explanation for
any human or model. The names it replaces, and why: **ring** said
containers-nest-and-load-in-a-chain, but the rule above says that now, and
the concentric model that coined the word is retired with the prototype;
**map** collides with Python's builtin in a Python codebase; **router**
claims the file acts when it is data a model judges — the same overclaim
stripped from `always` and declined in `trigger`; **entrypoint** names the
entering but not the contents, and collides with Dockerfiles. What
*entrypoint* and *map* each reached for, `index` covers.

**A bundle's index travels inside the bundle.** `INDEX.md`, reserved, at the
bundle root — generated when the bundle is edited or published, checked by
`audit-bundle`, never touched by `apply`. When a
project adopts the bundle, the index lands with it, frozen at that version
and covered by the same checksum as everything else. It cannot be stale
within a project, because it does not describe the project; it describes one
version of one bundle, and it is exactly as current as the copy it arrived
in. The prototype generated its per-bundle maps into a per-project shadow
directory, and every defect it grew — staleness between applies, orphan
sweeping, generated files where hand-edits reach, descriptions drifting from
frontmatter — came from that placement. Moved inside the bundle, all four
stop existing rather than needing management.

**Local bundles regenerate instead of freezing.** A bundle written in this
project has no publish moment, so its index is refreshed by the same
generator whenever the bundle is edited, and `audit-bundle` reports a
listing that disagrees with the frontmatter. The vendored and the local
case differ only in when generation runs — the file is the same file.

**A bundle needs no catalog to exist.** Creating, editing, and indexing a
bundle are foreman acts on a directory in a project, complete in
themselves. A catalog is how bundles are organized and distributed once
they are worth sharing — a consumer of finished bundles, never a
precondition for one. Every moment this design touches — create, edit,
regenerate, adopt, load — works with no catalog anywhere; publishing is the
one act that involves a catalog, and it is optional. This is also the
deeper reason the generator lives in foreman rather than in catalog tooling
or CI: the tool has to stand where bundles are born, and they are born in
projects.

**One generator owns the rendering, and it lives in foreman.** A single
command — generate for a bundle path, `--check` to verify without writing —
invoked at every moment generation happens: `create-bundle` and
`update-bundle` after an edit, `publish-to-the-catalog` before shipping,
and `audit-bundle` in check mode, which is regenerate-and-compare with the
same code and so cannot disagree with the generator. Foreman is already
standing at all of those moments — local bundles live in projects,
publishing runs from an operator's machine — so this costs no new tool and
no catalog-side dependency. The division of labor: the spec defines what an
index is, foreman renders it; a second generator elsewhere is the forcing
case for moving the code upstream, not before. And the adopter line holds —
index generation is an authoring act, `apply` a project rendering act, so
`apply` still never writes into a bundle, vendored or local.

**The authored half lives in the bundle's own document.** The exploration's
split answer to what an index is — facts derived, judgement authored, each
half where it cannot go wrong — lands here without a new field. The strong
judgement, *read this before acting here*, is already `matches: eager`
and renders as the Required gate. Everything judgement-shaped beyond it —
how the parts relate, what belongs together, what this bundle deliberately
does not cover — is prose in the body of the bundle's `type: bundle`
document, and the generator renders that body between the purpose line and
the derived sections. This retires the prototype's `entrypoint` key: what
it pointed at is an `eager` declaration, and what it could not say is body
prose. The body is paid in every session that opens the bundle, so the
announcement-size discipline applies to it, and `audit-bundle` flags a
bloated one.

**Listing order is deterministic, and meaning does not ride on it.** Within
each derived section the generator lists by path, so the same state always
renders the same index. Where reading order genuinely carries meaning, the
bundle body says so in prose — *read X before Y* — which a model follows as
well as any field. An ordering field waits for the first bundle that proves
prose insufficient; it would arrive as one optional field and a
regeneration, breaking nothing already authored.

## The index is markdown, because it is a rendering

**The frontmatter an index renders is authoritative, always.** The ground
truth is the documents' LKF frontmatter and the bundle's own metadata; the
index is generated from that truth, and any tool that needs the data —
`apply` compiling the project index, `audit-bundle` verifying, the
eventual hook building its binding table — reads the frontmatter. A tool
MAY read an index mechanically instead — one file instead of many, and in
an unmodified copy the rendering cannot disagree with its source — but
where the two disagree the frontmatter wins, and the disagreement is a
reportable defect of that copy, exactly as spec `v0.0.19` states. The
index is *written for* two readers, models and humans, and for them
markdown wins outright: it carries
the judgement no data format can (*read this first — everything else assumes
it*), models are trained on it, and it matches the estate of reserved
ALL-CAPS markdown. A data format would spend tokens on syntax to serve a
tool audience that does not exist. One source of truth with a rendered view
is also what makes drift impossible by construction rather than detected
after the fact.

**One discipline keeps it honest:** the `matches:` lines in an index are
rendered in a single fixed compact form, derived one-to-one from the
frontmatter — a display convention, never a second declaration syntax, and
never a place where a fact appears that the frontmatter does not state.

## The mock-up — a bundle's `INDEX.md`

```markdown
<!-- Generated when this bundle is published. Regenerate, never edit. -->

# lumastack/luma-catalog/git-secrets 0.5.1

Keeping credentials and private identity out of a repository — names,
personal addresses, home paths, machine names, tokens and key files.
Prevention first, then audit.

## Required — do NOT act on this bundle before reading these

- `policy/never-commit-private-identity` (policy) — real names, personal
  emails, home paths and machine names must not appear in commits or
  tracked content; what to use instead, and why deletion does not undo it.
  - matches: eager

## Offered — open when the work matches

- `policy/never-commit-credentials` (policy) — what counts as a credential,
  which files never belong in a repository, and why rotation comes before
  cleanup.
  - matches: command:git commit, command:git push, event:before-commit

## By request — reached by name or by citation

- `reference/scrubbing-history` (document) — what removing something from
  git history actually takes, and what it can never undo.

Procedures in `procedure/` are installed in your harness — invoke them by
name rather than reading them here.
```

**The derived postures render as the visible groupings**, so the
derivation table above is what a reader actually sees. In it: identity and
version; the purpose line, written to be matched against work; each
document's id, type, one-liner, and compactly rendered matches. Not in it: document
bodies; the catalog sell-copy, which answers *is this worth adopting* for a
different reader at a different moment; the changelog; checksums and
provenance, which are the manifest's; and per-project skill-name
resolutions, which are binding output and cannot live in a file frozen
upstream of any project.

**Emphasis is spent only where no mechanism exists.** The Required heading
is the MVP's one enforcement surface for `eager` documents — pure
instruction, nothing checking — so it gets the strongest phrasing there is:
a gate on the next action, *do not act before reading*, which models follow
more reliably than an adjective like ALWAYS describing a general habit. It
is also the only place an index shouts. Everywhere a mechanism keeps the
promise — the project index's imports above all — the prose stays calm,
because emphasis works by contrast and a document that shouts everywhere
teaches its reader to ignore shouting.

**Procedures are accounted for in one line and never listed.** Their names
and descriptions already sit in the session floor through harness
registration, so listing them here would charge the same tokens twice in the
same context — and a reader who found files the index never mentioned would
be looking at what smells like a stray. One class-level sentence covers
them without naming one, so nothing doubles and nothing drifts.

## The mock-up — the project index

```markdown
<!-- Generated by `luma-foreman apply`. Regenerate, never edit. -->

# What this project knows

Every container has an index. This is the project's: one entry per bundle,
what each is for, and what brings it into play. A bundle's own index sits
at `<bundle-id>/INDEX.md` beside this file — open it when the bundle's
line matches the work, and not before. Procedures are installed in your
harness as skills and are not listed here.

## Required — imported here, already in your context

- `myorg/conventions` 0.3.0 — how code, commits and reviews are done in
  this organization.

@myorg/conventions/policy/how-we-work.md

## Offered — open a bundle's index when its line matches the work

- `lumastack/luma-catalog/git-secrets` 0.7.2 — keeping credentials and
  private identity out of a repository — names, addresses, home paths,
  tokens and key files. Prevention first, then audit.
- `lumastack/luma-catalog/git-worktrees` 0.6.2 — isolated worktrees for
  concurrent agents in one repository — provisioning them, and tearing
  them down without wreckage.
  - matches: command:git worktree
- `lumastack/luma-catalog/decision-records` 0.10.0 — decisions recorded
  with their reasoning, deferred alternatives, and re-open triggers.

## By request — adopted, and never volunteered

- `lumastack/luma-catalog/versioning-reference` 0.2.0 — the long tables:
  what every version part promises, case by case.
```

**The same shape one level out, and two floor economies.** No per-entry
path lines — every bundle's index is at `<bundle-id>/INDEX.md`, so the
convention is stated once in the preamble rather than spent once per
bundle. And the Required section is where the floor is assembled: the
adapter imports this file, this file imports the eager bundles' required
documents, so the complete session floor is auditable by reading one file.

**What an entry asserts.** The derived postures render at this level too —
an eager bundle under Required, a bundle never volunteered under By
request. A bundle-level conditional matcher renders the same way where one
exists; for most bundles the purpose line is the whole announcement. A
local bundle is indistinguishable from a vendored one here, because
provenance and integrity are the manifest's facts, not loading facts.
The preamble carries the protocol and nothing else — adoption policy such
as *this is a copy, change it upstream* belongs in an eager policy
document that rides the Required section like any other floor content,
versioned and owned, rather than in generator boilerplate.

## What apply compiles

`apply` reads every adopted bundle and writes, for Claude Code — never
reaching inside a vendored bundle, only pointing at it:

**The adapter** — a managed block in `CLAUDE.md` that says *read the project
index now*, imports it, and carries nothing else. Per-harness by nature; its
whole job is to get the project index read.

**The project index** — `.luma/bundles/INDEX.md`, always resident, the same
shape as a bundle's index one level up: one entry per bundle — name,
version, purpose line — with the path to a bundle's own index stated once
as a convention rather than once per entry. O(bundles) by construction,
regenerated on every apply from the manifest's membership and the bundles'
own metadata, so it cannot disagree with what the project carries. This retires `entrypoint.md`, name and file
both.

**Guaranteed floor content** — a bundle declaring `eager` gets its required
documents imported into the always-loaded chain, so the harness itself keeps
the promise. The body is paid in every session, the index entry says so, and
that visible price is the brake on overusing it.

**A skill per procedure** — already the settled shape: the harness registers
every skill's name and description at startup, which is eager announcement
as a harness limit, accepted.

**Two request skills, fixed cost however many bundles** — one that re-reads
the project index when it has fallen out of context, one that opens a named
bundle's index. These are the request helpers: recovery for anything
offered, the only way in for standby, and the repair path when a compaction
has eaten what was loaded.

Everything `apply` writes is generated, nothing edited, regenerated rather
than repaired. Pointers, never copies — the only content that travels into
the floor is the `eager` imports, and the harness loads those from the
vendored files themselves.

## The format policy — under evaluation

**Format follows expected behavior, and the policy is on trial.** A format
is not a container but an instruction: it tells whoever touches the file
how to behave. Every file this design creates is placed by two behavioral
questions — never by precedent or taste, in either direction: not markdown
because that is what the estate does, not a data format because data
sounds serious. This is recorded as something being tried, not something
proven — it holds until a file resists its cell.

**What must the writer conform to, and what must the reader do?** A tool
conforms through its emitter and serves any format equally; an agent
conforms only as hard as the format and its validator force it — which is
where strictness genuinely buys hallucination resistance; a human cannot
be forced at all and needs forgiveness and comments instead. On the other
side, a reader either obeys the file literally as data or weighs it as
judgement — and format is how the file says which: a strict format says
*obey* (a model reading JSON copies values; a model reading prose
paraphrases), a prose format says *think*. Readability discriminates
nothing — humans read every format here fine.

**The reading moments each format serves:**

- **Loaded into model context** — a recurring token tax, and the content
  is prose. Markdown wins: syntax costs almost nothing and judgement sits
  beside facts.
- **Judged in review** — a human decides whether a diff is right, so the
  diff must *be* the semantic change: one fact per line, no syntax spill
  (JSON's commas and brackets bleed one edit across neighbouring lines),
  and room for a rationale beside a fact when one is ever needed —
  comments hold *why*, which JSON structurally cannot.
- **Parsed at runtime, never judged** — strictness and speed win,
  elegance is irrelevant, and the file is regenerable, so its format can
  never trap anyone.
- **Edited by hand** — forgiving syntax, comments, and editor support
  earn their keep.

| file | the writer must | the reader must | format |
| --- | --- | --- | --- |
| knowledge documents | conform to LKF, validator-enforced (agents and humans write here) | interpret with judgement | markdown + frontmatter |
| indexes, skills | conform via the generator | judge relevance, follow pointers | markdown |
| manifest; the binding record, if it comes | conform via command emitters, strict validator behind them | trust the facts; humans judge the diffs in review | the line grammar |
| hook table and injection log, when they come | conform via the compiler | obey literally, no interpretation | JSON |
| permissions and configuration | nothing — humans are forgiven, the reader validates | obey strictly (the reader is the tool) | TOML |

**Three arguments carry it.** Models never author records — commands write
the manifest, generators write indexes, compilers write tables — so
enforcement effort concentrates where models actually write: strict
validation of LKF frontmatter in the generator's check and in
`audit-bundle`. Format strictness anywhere else defends a door only the
tool enters. Second, the no-dependencies promise flattens the schema
advantage of the standard formats — JSON Schema validators and format
linters are dependencies, so validation here is hand-written whichever
syntax is chosen, and strictness is a property of the validator, not the
format. Third, migration cost is smallest exactly where the bets are
taken: a tool-owned format migrates by reading old and emitting new in one
release, while the expensive format bet — files humans and models
author — is already placed upstream in the LKF spec, where it belongs.

**Each format keeps the one cell it wins.** JSON is designated now for
disposable machine artifacts — strict, standard-library round-trip, and
unable to trap anyone, because a regenerable file's format is never a
commitment. TOML keeps operator-edited configuration, where `tomllib`
reads, foreman never writes, and editors help humans. Markdown carries
everything models read. No format is the default; every new file is placed
by the matrix, out loud.

**What would break the trial, and when to look.** A committed record that
fights its cell — needing nesting the line grammar cannot express, or a
strictness the hand-rolled validator keeps failing to deliver. Validation
missing defects a schema ecosystem would have caught. An agent repeatedly
mis-authoring a tool-owned file, which would break the
models-never-author-records premise the policy leans on. JSON creeping
from artifacts into committed records, or prose creeping into compiled
tables. A decisive reading misjudged — a file classed as runtime-only that
people turn out to review, or a reviewed file whose diffs nobody actually
judges. Re-review when the first compiled artifact ships, and at every new
file's placement — each one is a data point for or against.

## The project's record — `MANIFEST.md`

**A receipt, kept by commands.** `.luma/bundles/MANIFEST.md` records every
bundle this project carries and the custody facts about each: the version
taken, where a copy came from, the commit it left at, the checksum of what
landed. `get` writes an entry, removal deletes it, and a claiming command
blesses a directory that arrived by hand — tools change this file, people
run the tools. Membership is what makes a stray reportable at all: a walk
can only say what is on disk, never what belongs. This replaces the
prototype's `adopted.toml`, whose name could never honestly hold a bundle
written here — which was never adopted — where a manifest is exactly a
receipt of what is aboard.

**The format is the policy's command-written cell: the line grammar.** One
bullet per bundle, `key: value` sublines, nothing nested. The general
argument is the format policy's above; what the manifest adds is its own
fit: edits are line-oriented so a command touches one entry, a bare line
naming a bundle is already valid grammar so the authored future stays
open, and the file matches the reserved ALL-CAPS estate. The rejected
candidates fall out of the policy's constraints — TOML has no
standard-library writer even for a regenerated receipt, JSON closes the
authored door, YAML does not exist in the standard library at all.

```markdown
<!-- Written by `luma-foreman`. Change it with commands, not by hand. -->

# Bundles

- `lumastack/luma-catalog/git-secrets` 0.7.2
  - source: https://github.com/LumaStack/luma-catalog
  - commit: 8ec0cce285bb27f0b6c58bacb62d37bd62a702ee
  - sha256: 2eb6115374ff3202da0fccc0452e044f6011dde17948bef76df2ab56243ac72d
- `lumastack/luma-catalog/token-manager` 0.10.2
  - source: https://github.com/LumaStack/luma-catalog
  - commit: 8ec0cce285bb27f0b6c58bacb62d37bd62a702ee
  - sha256: 9f41c2ae7d305b118e6a0cc472fd9be2513a86d7f0e4b9c1a2d385f6704e8ba3
  - register: nothing
- `myorg/conventions` 0.3.0
```

**The kinds are distinguished by shape, not by a flag.** Custody lines mark
a vendored copy; a bare entry is a bundle written here. No `local: true`,
because a flag restating what the lines already show is a second copy of
one fact.

**The manifest records *did we get this* and *should this be wired* —
never *is it wired*.** The first two are unrecoverable: custody, which
nothing can reconstruct once the moment passes, and intent, which is a
decision. The third is observable at any time, because `apply` generates
deterministically from the manifest and the bundles — *wired* means *the
generated artifacts match a regeneration* — so recording it would be a
claim about observable state: true the moment written, a lie the moment
anything changed without it. With intent recorded and actuality derived,
`inspect` compares the two and reports both directions of mismatch:
believed wired but is not, healed by regenerating; wired but believed not,
which `apply` removes. Corruption always has a source of truth to heal
toward, and nothing anywhere describes generated state.

**Intent is the `register:` field, and its values are what to wire into.**
Absent — the overwhelming default — means *wire everywhere `apply`
reaches*, and costs zero lines. `register: nothing` means *deliberately
landed and not wired*, the one divergence the file records; `apply` honors
it in the MVP by skipping the bundle everywhere. A list of harnesses is
the possible future, arriving only if per-harness wiring is ever forced —
richer intent, same field, same directive mood. The value space follows
`matches: nothing`: an explicit `nothing` is a decision, absence is the
default, and the estate teaches the pattern once. Two shapes were
rejected: `register: no`, a flag disguised as a value; and
`skip-register: true`, a value carrying no information that dead-ends the
moment intent grows richer. The field never carries event data — what
commit applied it, when, and by whom is the committed manifest's own git
history, already incorruptible and already free. This also answers the
exploration Entry 4's *Enablement*: present and switched off is
`register: nothing`.

**Manifest and index divide cleanly.** The index says what is in play; the
manifest says what is here and where it came from — loading facts and
custody facts, both at `.luma/bundles/`, no overlap. The one deliberate
double appearance is version, as two different facts: the manifest records
the version taken, the index renders the version the bundle says it is,
and disagreement between them is a signal `inspect` reports, not drift.

**Authored is the open future, not the design.** A mature manifest might
accept partial entries — a line naming a bundle, the tool resolving the
rest — and a bare line is already valid grammar, so that future is a
behavior change, not a format change. It arrives, if ever, when somebody
actually wants to claim bundles by hand; nothing is built for it now
beyond not closing the door.

## The trade a bundle-level index takes, stated plainly

**A project index that announces per bundle buys a small floor and pays in
reachability.** When a document's own line would have matched the work but
its bundle's one entry did not, the document is silently unreachable — and
the bundle boundary not deciding relevance is settled, so this will happen.
The MVP takes the trade with eyes open: the floor stays O(bundles), every
load costs one extra hop through a bundle's index, and the pressure valve —
a document promoting its own line into the project index when its bundle's
entry would bury it — is deferred until a real miss is observed, because it
reopens the floor question the moment it exists and an author guessing about
promotion is the exploration's own warning.

## No hooks in the MVP

**Hooks buy exactly one thing: machine-kept conditional loading.** The MVP
has no conditional guarantees to keep — `eager` is kept by the import, and
everything conditional is offered, where the model deciding is the design and
not a degradation. So a hook would enforce a promise nobody has made yet, at
the price of per-call evaluation, dedup, an injection log, and an installed
component that can silently not be installed.

**What forces them back is a measured miss.** The first observed case of a
model failing to open what an index plainly matched, where the miss cost
something — that is evidence the offered tier needs a machine under part of
it, and the structured matchers are already shaped for a hook to read. Until
then, hook machinery is built against a failure rate nobody has seen.

## What a session costs

The floor, all of it visible and measurable: the managed block, the project
index, the bodies of any eager-bundle imports, and every procedure skill's
name and description. A bundle's index is paid only in sessions that open
that bundle; a document only in sessions that load it. A floor audit is a
read of generated files, no harness required.

## Diagnosing a miss

Three destinations, walked by name, in order: did it **land** (the vendored
directory and its index exist), was it **registered** (the project index
entry or skill exists), did it **load** (the model opened it). Manual in the
MVP. The first two are mechanical checks a tool can already answer; the
third is the one only the eventual log can see.

## The eventual state

The same declarations, honored by more machinery, in roughly this order, each
piece waiting for its forcing event.

**A hook makes conditional matchers machine-kept.** `apply` additionally
compiles a binding table from the documents' frontmatter; an installed hook
evaluates `path:`, `command:`, `tool:` and `event:` per call and injects the
document when one fires — with dedup so a condition firing forty times injects once,
and a log of every injection. `topic:` stays with the model. On a harness
without the hook, `apply` says plainly that these matchers are being served
as offered — the degradation is reported, never silent.

**The Required gate graduates from instruction to injection.** In the MVP,
*do not act before reading* is prose a model obeys; the declaration behind
it is already data. A hook can see a bundle being opened — reading its
`INDEX.md` is a tool call — and inject that bundle's `eager` documents in
the same turn, making the container-relative guarantee machine-kept, with
the same dedup and log as every other injection. If ordering has earned a
field by then, the injector honours it mechanically, and prose ordering
remains the form everything degrades to. Nothing authored changes at
graduation — the test the MVP's prose choice was made against.

**The log makes loading tunable.** With injections and requests recorded, a
trend exists: whether the right documents load more often than they used to.
That is when `expected` splits from `optional` — an absence somebody can
finally see — and when an adopter can demote what never fires and promote
what keeps being requested, from evidence instead of feel.

**Residency machinery makes announcements guaranteed.** The floor already
survives every reset — the harness re-sends the always-loaded chain each
turn — but everything conversation-borne is losable: a bundle index
opened mid-session, an eager body read at the gate, a requested document,
all silently summarized away by a compaction. The log is what closes
this: a hook that records what it injected and observes what the model
opened knows the intended-resident set, and re-asserts it after a reset —
announcements first, the cheap half whose loss takes the model's map with
it and with it the ability to request what it no longer knows exists.
This is the exploration's problem 9 given its mechanism, and it is the
second job hooks arrive to do.

**Promotion answers the missed-bundle failure.** A document whose line
belongs in the project index even when its bundle's entry would not surface
it gets a way to say so, and the floor grows only by what is promoted.
Forced back by the first miss that cost something; priced by the floor audit
that exists by then.

**An `entrypoint` nicety may return as sugar, never as a second truth.** A
single pointer an author writes instead of learning `eager` — resolved at
generation into the same declarations it abbreviates, so it can add
convenience, or even enforcement, without adding a second way to state one
fact. Forced back by real authors finding `eager` plus body prose too
fiddly; rejected again the moment it would mean something the existing
declarations cannot.

**Overrides arrive as input to resolution.** A project file naming what this
adopter decided differently — a matcher narrowed to `src/`, a document
silenced, a name rebound — read by `apply` on every run and resolved into
what it generates, never patched into output. Forced back by the first
adopter who is not the author.

**What earns a record is a decision, never an artifact.** Healing corrupted
wiring needs no record of the wiring: `inspect` detects by
regenerate-and-compare, `apply` heals by regenerating from checksummed and
committed inputs, and git holds every prior wire for rollback — a snapshot
of generated state would be a third copy of derivable truth, corruptible by
the same hand-edit it guards against, teaching the system to heal toward
the corruption. What regeneration cannot recover is a history-dependent
decision: which colliding procedure kept the bare name, which of several
providers was taken — facts the stability requirement makes load-bearing,
because a name an agent learned yesterday must still resolve today even
after membership changes. Those arrive, when collisions become real, as a
binding record: a sister file beside the manifest and the overrides,
recording resolutions — and it is an *input* to `apply`, so healing remains
one command regenerating from recorded inputs, and nothing anywhere claims
to describe generated state.

**Governance and `expose` stay out** until a governing body exists, and then
arrive as the exploration frames them: a boundary designed in one place, that
adopter override cannot reach past. `expose` is also where *never loadable*
will live — a block is enforced between the model and the content, which no
field a model can read could ever be. The same goes for `provides` / `needs`,
the cross-catalog vocabulary, and section-level loading — each has a real
problem behind it and no instance of that problem yet.

## What this drops from the prototype

Measured against the design above: the per-project `rings/` directory and
its orphan-sweeping, and the word *ring* itself — the artifact survives as
the bundle's index, moved inside the bundle where it freezes with the
version; `entrypoint.md`, renamed to the project index so one word serves
every level; `adopted.toml`, replaced by the manifest — receipt semantics
kept, name and format corrected; the routing table as a separate artifact;
the derived always-on
/ advertised / on-demand class names — the postures above replace them,
derived the same way but meaning what an absence is; and any posture field
declared beside `matches`. The adapter block, the always-resident project
index, the procedure skills, and the two fixed-cost request skills all
survive — those the prototype guessed right.
