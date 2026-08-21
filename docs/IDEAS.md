# Ideas

Wanted capabilities, captured so they survive. Nothing here is designed, ordered, or committed to — this is a holding pen, like `docs/examples/`. Expect it to be replaced by `.luma/backlog/` once the repository is ready for it.

## Migrated — 2026-08-21

Moved to one file per idea, following `luma/backlog-ideas`. **All 19 reviewable
ideas decided**, from the 18 agreed at the start plus one split. Every entry
below carries a marker saying where it went or why it was dropped.

Fifteen files were written or amended across four repositories. Every one has
been verified to exist and to carry `type`, `title`, `created`, `scope` and
`horizon`.

**Migrated**

| # | Title | Landed | Modifications | Metadata |
|---|---|---|---|---|
| 2 | History | `luma-foreman` · scan-history-not-just-the-working-tree.md | retitled · notes added | someday · project |
| 3 | Drive an incident, and store it as markdown | `luma-foreman` · drive-an-incident.md | notes added | someday · project |
| 5 | Install the standard tooling | `luma-catalog` · bundles-for-linting-tests-ci-and-review.md | retitled · notes added | later · project |
| 6 | Meta-skills | `luma-catalog` · meta-skills-that-generate-project-practice.md | retitled · notes added | someday · project |
| 7 | Return periodically to confirm learnings applied | `luma-leader` · tools-that-run-on-a-schedule.md | absorbed into tools-that-run-on-a-schedule.md | *target's* |
| 9 | New repo survey | `luma-foreman` · new-repository-survey.md | retitled · notes added | later · project |
| 10 | Define how to resolve common terms or requests | `luma-catalog` · declared-vocabulary-for-requests.md | retitled · notes added | later · project |
| 11 | Committed per-project Claude Code settings | `luma-foreman` · committed-permission-floor.md | retitled · notes added | later · project |
| 12 | Distribution | `luma-foreman` · distribution-beyond-clone-and-symlink.md | retitled · notes added | later · project |
| 14 | Bundle migrations | `luma-catalog` · bundle-migrations.md | notes added | later · project |
| 15 | Routers | `luma-foreman` · routers.md | retitled · notes added | someday · project |
| 16 | Browsing a catalog is an engine's job | `luma-foreman` · browsing-a-catalog-is-an-engines-job.md | notes added | someday · project |
| 17a | Manifest files may want to be YAML | `luma-knowledge-format` · bundle-manifest-as-yaml.md | split 1 of 2 · retitled | later · project |
| 17b | Manifest files may want to be YAML | `luma-catalog` · catalog-manifest-as-yaml.md | split 2 of 2 · retitled | later · project |
| 18 | Permission modes | `luma-foreman` · named-permission-profiles.md | retitled · notes added | later · project |
| — | A personal skill selection that is not committed | `luma-foreman` · personal-skill-selection-not-committed.md | new capture | later · project |

**Pruned**

| # | Title | Why |
|---|---|---|
| 1 | An identity list for the case shape cannot reach | `inspect`'s `identity` rule already lists well-formed author addresses once a repository has more than three. The residual gap is that threshold, and the honest-reporting half is a guard on a feature that does not exist |
| 4 | Bootstrap a new project | `bootstrap` is a stub command in the README, its scope recorded in `docs/scope.md` and its ordering in `docs/next-steps.md`. The structural knowledge moved to the `luma-layout` bundle |
| 8 | Git worktee workflows | Already happened — the `luma/git-worktrees` bundle, published 2026-08-18: a policy and four workflows |
| 13 | The package-management prior art | Not an idea. Every mechanism in its table is a settled decision in `luma-leader/docs/DECISIONS.md`, and the one row that is not recorded is one that decision rejects |

`luma-foreman` 9 · `luma-catalog` 5 · `luma-knowledge-format` 1 ·
`luma-leader` 1 absorbed · pruned 4

**Eight entries were retitled**, in every case because the original named a
mechanism that turned out to be already scoped, and the gap underneath it was the
part worth keeping. Three of the four prunes were *already happened* rather than
*not wanted*.

## Keep sensitive data out of git

**Built and shipped.** The policy and the workflows are the `luma/git-secrets`
bundle in the catalog; the checks are `inspect`'s `identity` and `secrets`
rules. What was here — the four surfaces, prevention versus detection, what to
use instead — lives there now, and is deleted rather than duplicated.

Two things it still cannot do, which are the reason this entry survives at all.

**An identity list, for the narrow case shape cannot reach.** `alice@laptop.local`
is recognisable without knowing who alice is, and so is a malformed address or a
home path — which turned out to be most of it, and is why the check needs no
configuration and runs in a bare clone. What it cannot know is that a
well-formed address at a real domain is personal rather than professional.

Half of that is settled: who the operator is counts as workstation state, so the
list lives in workstation configuration and never enters a repository. The open
half is harder — a check that silently passes because its list is absent is
worse than no check. Hashes committed to the project is one way out; the other
is for the check to report honestly that it ran without a list rather than
reporting clean.

> *Pruned, not migrated. `inspect`'s `identity` rule already lists well-formed
> author addresses as evidence once a repository has more than three of them, so
> the gap is narrower than this entry claims — it is the threshold, not the
> absence of a list. The honest-reporting half is a guard on a feature that does
> not exist and is not independently buildable.*

**History.** A secret committed and deleted a month later is still published,
and that is where most real leaks live. Nothing here scans it, and the bundle
says so rather than letting a clean working tree imply an answer it cannot give.

> *Migrated to `.luma/backlog/ideas/scan-history-not-just-the-working-tree.md`.*


## Drive an incident, and store it as markdown

When something goes wrong, foreman runs the response rather than leaving it to memory and chat: prompts for what is known, tracks what has been tried, and captures the timeline as it happens rather than reconstructing it afterward. The record is markdown, committed in the affected project.

Likely delivered as a skill foreman installs into a project, rather than something foreman runs itself — the response happens inside the affected repository, with whoever is already working there.

**Settled:** incident records conform to the Luma Knowledge Format. They are knowledge like any other record, not a separate filing system.

Open: whether the format already has a record type that fits, or whether an incident needs a new one — a timeline that accumulates during an event is a different shape from a record written once. If it needs one, that is a format request, not a reason to contort around the gap. Also open: where the records live, and whether driving and recording are one capability or two, since recording a timeline is useful even when nobody is being walked through the response.

> *Migrated to `.luma/backlog/ideas/drive-an-incident.md`.*

## Other capabilities named but not yet captured properly

- Bootstrap a new project with the structure it should have had from the first commit.
  > *Pruned, not migrated. `bootstrap` is a stub command in the README; its scope is
  > recorded in `docs/scope.md` and its ordering in `docs/next-steps.md`, and the
  > structural knowledge moved to the `luma-layout` bundle.*
- Install the standard tooling — linting, tests, continuous integration, independent review, a backlog.
  > *Migrated to `luma-catalog`, `.luma/backlog/ideas/bundles-for-linting-tests-ci-and-review.md`,
  > retitled — the mechanism is scoped here, but four of the five named bundles do not exist.*
- Meta-skills: skills that generate a project's own best-practice skills, rather than copying a template.
  > *Migrated to `luma-catalog`, `.luma/backlog/ideas/meta-skills-that-generate-project-practice.md`.*
- Return periodically to confirm the latest learnings were actually applied.
  > *Pruned as scheduling. The one new part — `refit` as a recurring consumer — was
  > absorbed into `luma-leader`, `.luma/backlog/ideas/tools-that-run-on-a-schedule.md`.*
- Git worktee workflows
  > *Pruned — already happened. Shipped as the `luma/git-worktrees` bundle
  > (published 2026-08-18): a policy and four workflows.*

## New repo survey

When setting up a new repo, capture infromation that will drive how it gets used now and later.  Ensure these are fluid and don't rot.

- greenfield vs brown field
- where are we in the design process
  - these ideas are locked in
  - this is all experimental and much of it may head in a different direction
- how established is this project
  - changes are expensive, change as little as possible
  - move fast and break things
- capture creates optimal change request output
  - for examplek: design (cheapest) < prototype < implementation < production (most expensive)
  - at what point does this change?
  - this might change by project
- how many users now, and how many intended
  - this tells us how much we can break for rapid development
- how critical is this system
- how sensitive are the users
- distribution of user expertise
- what is our intended test strategy
  - vs what is the reality
- what are the default user profiles
- what are your example names, addresses, etc so identifiable info doesn't leak in
- when is editing decisions not allowed (e.g. on the first day, it should be ok to edit a decision instead of taking on tech debt)

> *Migrated to `.luma/backlog/ideas/new-repository-survey.md`.*

## Define how to resolve common terms or requests

What does it mean when i say:
- I want a situation report
  you should respond with: "Let me drop the options and show you the actual situation."
- I need help coming up to speed
- Where did we leave off
- What do you know to be true
- Checkpoint

> *Migrated to `luma-catalog`, `.luma/backlog/ideas/declared-vocabulary-for-requests.md`,
> retitled — three of the five phrases already resolve to `session-manager` workflows, so
> the want is a binding layer rather than five capabilities.*

## Claude Code modes

Change what Claude Code's hooks allow or disallow with a command, per project, without editing the hook or restarting the session.

- Full trust mode
- Allow/disallow downloads
- Allow/disallow ssh
- Allow "trusted" ssh only
- Allow/disallow curl
- Allow harmless curl (non-executable files)

**Built.** Shipped as `luma-foreman agent-permissions` — see [docs/claude-agent-permissions.md](docs/claude-agent-permissions.md). What it settled, kept here because the reasoning is worth more than the code:

- The policy has to live in a file the hook reads on every call, not in `settings.json`. Claude Code snapshots hook *configuration* at session start, so a settings-based design needs a session restart per change; a file the hook re-reads takes effect on the next tool call.
- Resolution is per key, most specific wins: project, then a global fallback, then built-in defaults. A project only names what it overrides.
- Projects are keyed by repository root, slugged the way Claude Code names `~/.claude/projects`, so every session in a repo shares one policy no matter which subdirectory it started in.
- This is **workstation state, per project** — never committed. What an agent may do in a repository is the operator's call, not something every clone inherits.
- The value vocabulary is Claude Code's own — `allow`, `ask`, `deny` — plus `always` for bypass-proof, and refinements like `trusted` for ssh and `safe` for fetches. Not `disallow`; nothing in this space uses that word.
- Textual command matching is not a security boundary and must not be described as one. It catches your own slips and an agent's carelessness. Sandboxing is the boundary; this rides on top for ergonomics.
- Whatever governs the agent has to be something the agent cannot edit, including the gate itself. Solved with deny rules covering both the policy and the installed gate. The prototype protected the rulebook and not the lock. They deliberately live in *different* directories — configuration in `~/.config`, program files in `~/.local/share` — so that clearing your config cannot delete the gate, which would fail it open.
- A tool that has to touch someone else's config writes freely into the directory it owns and never silently edits the directory the user owns. `policy install` copies the gate and *prints* the `settings.json` changes, following `pre-commit install`.

Open: whether foreman additionally writes *committed* per-project Claude Code settings — the shared floor a team gets from a clone — with this machine-local layer as overrides on top. Those are two different capabilities that happen to touch the same file format. Also open: distribution. Install is currently a clone plus a symlink, which is fine for one operator and not for an organization.

> *Both opens migrated — `.luma/backlog/ideas/committed-permission-floor.md` and
> `.luma/backlog/ideas/distribution-beyond-clone-and-symlink.md`. The rest of this
> heading is settled reasoning about shipped work, recorded in
> [docs/claude-agent-permissions.md](claude-agent-permissions.md).*

## Bundles

**Settled, and recorded elsewhere.** The bundle model is no longer an idea: the
decisions live in `luma-leader/docs/DECISIONS.md`, the conventions in the catalog's
`bundle-manager` bundle, and the structural checks in `inspect`'s `bundles`
rule. What used to be here — the vocabulary, the seam against the format, the
distribution model, the catalog layout, workflows as a bundle type — is deleted
rather than kept, because two copies of settled reasoning drift and nobody can
tell which is current.

Where to look now:

| question | where it lives |
| --- | --- |
| what a bundle is, and why it is a Knowledge Bundle | `luma-leader/docs/DECISIONS.md` |
| documents, assets, attachments | the format's `SPEC.md` §2, §8 |
| `consumers`, `entry_point`, `preload` | the format's `SPEC.md` §5.2, §11.1 |
| obligation, starters, tags, catalog inheritance | `luma-leader/docs/DECISIONS.md` |
| where a bundle goes, and how it is promoted | `luma/bundle-manager` |
| how a bundle is laid out | `luma/bundle-manager` |
| what makes one structurally wrong | `foreman inspect --rule bundles` |

**One thing worth keeping, because nothing else records it.** None of this was a
new problem. A catalog, per-project selection, pinned versions, *do not change
under me*, *tell me what is available*, *this one is mandatory*, *here is your
deadline* — that is package management, and each part was solved somewhere worth
stealing from rather than inventing against:

| wanted | prior art |
| --- | --- |
| the catalog | a registry |
| what this project selected | a manifest — `package.json`, `Gemfile` |
| do not change under me | a lockfile, plus a vendored copy |
| tell me what is new | `npm outdated`, `bundle outdated` |
| mandatory and immediate | a security advisory — `npm audit`, Dependabot |
| adoption deadline | a deprecation window, a remediation SLA |
| promotion upward | contributing a fork back upstream |

The one place the borrowing stops is **resolution**. Bundles have no
dependencies, so there is no solver, no version negotiation, and no lockfile
beyond the vendored copy itself — which is why the thing is a catalog and not a
registry.

> *Pruned, not migrated. This heading holds no unfiled want. Its own justification —
> "nothing else records it" — was true when written and is not now: every mechanism
> in the prior-art table is a settled decision in `luma-leader/docs/DECISIONS.md` (the
> registry naming at §"The catalog is a catalog, not a registry", manifest and
> vendoring, the vendored directory as lockfile, upstream and mandate drift, the
> obligation ladder's `by:` deadline, and promotion as copy-then-adopt). The one row
> that is not recorded — promotion as contributing a fork upstream — is not recorded
> because the decision rejects it: "no subtree, no submodule, no git surgery". The
> attributions to npm, Gemfile and Dependabot were deliberately not carried across;
> the sentence that matters, "the catalog is the registry-shaped thing, minus
> resolution", is already in that decision.*


### Bundle migrations

**Wanted, not designed.** A way to say *here is how to get from version X to
version Y*, so an adopter several versions behind can be walked forward rather
than left to work it out from a changelog.

```
<bundle>/migrations/0.2.0/migration.md      what to do to arrive at 0.2.0
<bundle>/migrations/0.3.0/migration.md
```

Mostly prose an agent follows, with scripts alongside where a step is
mechanical. A directory per migration rather than a file, for the same reason a
workflow carrying assets gets one.

#### The reframe that makes it tractable

**A migration is about the adopter's content, not the bundle's.**

Re-vendoring already replaces the bundle wholesale — the new version arrives by
copying, and nothing needs migrating inside it. What breaks is **everything
outside the bundle that depended on the old shape**: the project's own documents
linking to a renamed one, its configuration naming a moved path, records written
against a Type Definition whose fields changed.

That is the whole job, and stating it that way keeps the scope from swallowing
the upgrade process entirely.

#### Where it goes: `bundle-manager`, not the format

It earns a type by the §10.4 test — a consumer **consults** it, reading every
migration and computing which to run in what order, where a `workflow` is
*chosen* rather than derived.

It fails the further test for being built in. The format's machinery does not
depend on it, and ubiquity is unmeasurable because **zero migrations exist** —
predicting would be exactly what the ubiquity test now warns against. There is a
cleaner line too: `bundle` is in the format because a Bundle is the unit of
distribution it defines, while *upgrading between versions* is the adoption
lifecycle, which the format deliberately does not cover.

If most bundles turn out to carry migrations, that count is the argument for
promoting it later.

#### Design, as far as it is settled

- **`extends: workflow`.** A migration *is* a procedure an agent runs. It adds
  version metadata and is selected by comparison rather than by choice, and
  inheriting says both at once.
- **Name the directory for the version it migrates *to*.** `0.2.0/` reads as
  *to get here, do this*, and chaining becomes a version sort. An arbitrary
  identifier needs a second field to establish order.
- **Reversibility is a field.** Some migrations are one-way in practice —
  splitting a `decision_log` into individual records is the known case, since
  each record then accumulates its own history that collapsing would discard. A
  migration that does not say so is one somebody tries to undo.
- **A migration that needs a person says so.** An agent that attempts an
  unautomatable step is worse than one that stops and explains.
- **Migrations never run on adoption.** A migration carrying a script is fine —
  that is code invoked deliberately. `foreman adopt` running one automatically
  is code executing as a side effect of fetching, which is the supply chain the
  bundle model refuses. Deliberate invocation only, always.

#### What foreman would do

Read `adopted.toml` for the version in place, read the bundle's `migrations/`,
select every migration whose target is above the current version and at or below
the desired one, and run them in ascending order.

No solver, no constraints, no graph — a sort. Worth saying because it looks like
dependency resolution and is not.

#### Open, and worth settling before building

**Distinguishing "no migration needed" from "migration missing."** A bundle
going `0.1.0` → `0.2.0` → `0.4.0` with nothing for `0.3.0` might have needed
nothing, or might have a hole. Nothing tells them apart, and an adopter crossing
the gap silently skips whatever was required. Possibly every version needs an
entry, with most saying *nothing to do*.

**Partial failure.** The same shape as a half-created worktree: leave nothing or
leave everything. A migration that stops halfway produces an adopter confidently
running against a state neither version describes.

**Accumulation.** Migrations pile up forever and nothing prunes them. Dropping
those below the last major is the obvious rule and would strand anybody further
behind than that.

**Local drift.** An adopter who edited their vendored copy — already a finding —
has content a migration's assumptions do not hold for. Refusing to migrate a
drifted bundle is probably right, and it makes drift block an upgrade, which
some adopter will resent at exactly the wrong moment.

> *Migrated to `luma-catalog`, `.luma/backlog/ideas/bundle-migrations.md`.*

### Routers

**Loose, and worth pursuing.** A `router` is a Document whose content is
*decision logic* — not knowledge, but the rules for reaching knowledge. Where to
go next, when to load what, which bundle answers a given question, whose
catalog to consult for more.

#### What is actually missing

**`preload` is unconditional.** A Document is `mandatory`, `recommended` or
`optional` always, decided once by its author. There is no way to say
*mandatory when auditing*, *irrelevant unless this is a release*, or *load the
release policy only if somebody is cutting one*.

That is the gap in one sentence, and everything else a router might do is
adjacent to it:

- **Progressive disclosure with conditions.** `preload` and links between them
  give eager and lazy loading. Neither gives *conditional*.
- **Which bundle answers this.** A project with eleven adopted bundles has no
  index from question to bundle. An agent either loads everything or guesses.
- **When to reach outside.** Into another corpus, another catalog, another
  organization's published knowledge. The catalog `upstream` chain does a
  narrow version of this for bundles and nothing does it for knowledge.

#### It would earn a type easily

By §10.4's test, this is the strongest dispatch case yet seen: a consumer does
not merely read a router, it **evaluates** one — reads conditions, tests them,
and decides what to load as a result. Nothing else in a Bundle is executed that
way.

Whether it should be *built in* is open and unmeasurable, since none exist. But
unlike bundle migrations, this one has a genuine claim on the format rather than
on the tooling: `preload` is already a core field, so conditional loading is
territory the format has entered rather than declined.

#### The central design question

**Is a router prose an agent follows, or data a tool evaluates?**

*Prose* is a workflow with a different name, and it inherits every good property
of one: no syntax to design, no expressiveness ceiling, and an agent can reason
about a condition nobody anticipated. Its cost is that nothing mechanical can
use it — no tool can pre-compute a context budget or verify a router is total.

*Data* is a condition language, and **that is where policy systems die.** The
catalog's tag rules already say so: any-of matching, no booleans, and a
composite condition becomes a named tag somebody has to claim. A router that
grows operators one reasonable step at a time ends up a small programming
language nobody can predict.

The middle worth exploring: **data for the conditions the tag vocabulary can
already express, prose for everything else.** A router row keys on the same tags
a project already declares, and anything beyond that is a paragraph rather than
a new operator.

#### Open, and worth settling before building

**Whose router is it?** A bundle routing within itself, a catalog routing to
bundles, and a project routing over what it has adopted are three different
scopes. They plausibly chain — which is itself routing, and a chain that can
loop.

**Does it reintroduce dependencies?** A router that says *for this, use bundle
X* is a bundle reference. That must stay a mention rather than a requirement,
or it becomes resolution wearing a new name. A router pointing at a bundle
nobody adopted should degrade to silence, not to an error.

**What does it overlap?** `preload`, `entry_point`, `tags` and a catalog's
`requires` each do a slice of this today. A router should absorb or defer to
each explicitly rather than quietly duplicating them — two mechanisms answering
one question is how they drift into disagreeing.

**Can it be verified?** A router with a gap routes somebody nowhere, silently.
Whether totality is checkable depends entirely on the prose-or-data answer
above, which is another reason that question comes first.

> *Migrated to `.luma/backlog/ideas/routers.md`. Filed here rather than in the
> knowledge format, against this entry's own argument; the disagreement is recorded
> in the file.*

**Guide or mandate?** The obligation ladder already exists and could apply — a
route can be a suggestion or a rule. Worth reusing rather than inventing a
second vocabulary for the same idea.

### Browsing a catalog is an engine's job, not a catalog's

A web interface for browsing bundles is wanted eventually. It must not live
inside a catalog.

An organization with a private catalog wants the same view of its own bundles.
A browser that lives inside the universal catalog is welded to that catalog's
content, so every organization wanting it has to fork — which is the thing the
architecture spends its effort avoiding. **A browser has to point at *a*
catalog, not be a feature of *the* catalog**, for the same reason foreman is
separate from an hq: it has to run against content it does not contain.

Whether that is its own repository or a foreman capability is open. Foreman is
already what talks to catalogs at apply time, and `list what is available here`
is close to `outfit` and `refit` in what it has to read, so a subcommand may
earn it before a second program does.

A secondary reason to keep it out regardless: an application gives the one
repository that is meant to be pure content a dependency tree, a lockfile, a
build, and a vulnerability feed. Every organization fetches content from that
repository. Dependency alerts on a catalog are a category error.

If the browser is a static site, the answer is the same with different
mechanics — the generator is an engine and lives elsewhere; the output is a
build artifact and is not committed to the content branch.

> *Migrated to `.luma/backlog/ideas/browsing-a-catalog-is-an-engines-job.md`.*

### Manifest files may want to be YAML, not markdown

**Unsettled, and worth revisiting deliberately rather than by drift.** Neither
`bundle.md` nor `catalog.md` is obviously right, and `catalog.md` is the weaker
of the two.

The doubt is about files that are almost entirely frontmatter. A markdown
document with a manifest at the top is the format's best property when the body
carries something; it is a YAML file wearing a costume when the body does not.
After the general prose moved into `_types/catalog.md` where it belonged,
`catalog.md` is a short instance note over a manifest — close to the point where
the extension stops being honest.

**They may deserve different answers, and forcing symmetry is part of what makes
this feel wrong.** A bundle is knowledge-adjacent, and its body has a real job:
what this bundle does, when to reach for it, what it assumes. A catalog is pure
configuration — an index with obligations, read by one tool, correct or not
according to cross-field rules. Nothing says both belong in the same file
format.

What YAML would buy: a JSON Schema, which brings editor validation and
completion that frontmatter never gets; no ambiguity about whether the body is
normative; and one obvious parse. What markdown buys: one parser across every
document foreman reads, a `type` that makes the file discoverable by the same
tooling that reads bundles, and the self-describing property the whole format
rests on.

**The timing matters more than the answer.** `bundle.md` is a reserved file in
the specification and `bundle` is a built-in type, so moving it is a breaking
change — but the format is in the `0.0.z` tier it declares unstable, which is
exactly the window such a change exists for. That window closes at `1.0`, and
this is a cheap edit now and an expensive migration later. Same one-directional
cost curve as nesting the catalog content.

**What would settle it:** whether real bundles turn out to have bodies worth
reading. If they do, `bundle.md` earns itself and only `catalog.yaml` moves. If
they do not, both are manifests and the markdown wrapper is costing a schema for
nothing.

> *Split at migration into two ideas, because only one has a deadline —
> `luma-knowledge-format`, `.luma/backlog/ideas/bundle-manifest-as-yaml.md` (a
> breaking spec change, window closes at `1.0`) and `luma-catalog`,
> `.luma/backlog/ideas/catalog-manifest-as-yaml.md` (defined nowhere in the
> specification, decidable unilaterally).*

## Permission modes

I want to be able to setup a mode in the config or via the command line or both.

It will make it so when I say I want to be in "foobar" mode it auto applies all my permissions to the way I set them.  The simpliest way is the setting sits as a mapping in the config.  The nice to have would be taking a snapshot of my current settings, name it, and then the current settings get added to config as a new mapping set.

> *Migrated to `.luma/backlog/ideas/named-permission-profiles.md`, retitled —
> `mode` already means two other things in this tool.*