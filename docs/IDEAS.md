# Ideas

Wanted capabilities, captured so they survive. Nothing here is designed, ordered, or committed to — this is a holding pen, like `docs/examples/`. Expect it to be replaced by `.backlog/` once the repository is ready for it.

## Stop personally identifiable information from leaking into git

Projects must not publish the maintainer's real name, personal email, home paths, or machine names. Secrets scanning is the obvious sibling and probably the same machinery with a different list.

Four surfaces, and the non-obvious ones are where the leaks actually happen:

- **Working tree content** — names, emails, `/Users/<name>` paths, hostnames.
- **Commit metadata** — author and committer identity on every commit. This is the surface that leaked in practice while the docs looked clean.
- **History content** — committed once and deleted later is still published.
- **Configuration** — whether `user.email` is set to a noreply address, and whether anything prevents the next bad commit.

Delivery mechanism is undecided. Candidates: install a hook into every project, write the rule into each project's `CLAUDE.md`, run as an inspection only, or some combination. Prevention and detection are both wanted; which one leads is open.

The check needs to know which identities are private, and that list must not end up published in the project being checked.

**Partly built.** `luma-foreman inspect` now covers the shape-detectable half, and that turned out to be most of it. A machine-derived identity like `alice@laptop.local` is recognisable without knowing who alice is; so is a malformed address, and so is a home path in tracked content. None of it needs an identity list, so it runs in a bare clone — which is what the "must survive continuous integration" constraint demanded. Validated against a real repository: it reproduced, in a second and with no configuration, what a long manual investigation had found by hand.

Still wanted: the identity *list* for the narrower "this specific address is private" case, secret scanning as the obvious sibling, and history-content scanning (committed once and deleted later is still published).

**Half of this is settled by the state model in the README.** Who the operator is counts as workstation state — a local fact, not organization knowledge — so the identity list lives in workstation config and never enters a repository at all. That covers prevention: bootstrap, outfit, and anything running at a workstation before a commit exists.

Still open: Inspect has to survive a bare environment with no configuration, and a check that silently passes because its list is absent is worse than no check. Hashes rather than literals, committed to the project, is one way out. Another is for Inspect to report honestly that it ran without an identity list rather than reporting clean.

## Drive an incident, and store it as markdown

When something goes wrong, foreman runs the response rather than leaving it to memory and chat: prompts for what is known, tracks what has been tried, and captures the timeline as it happens rather than reconstructing it afterward. The record is markdown, committed in the affected project.

Likely delivered as a skill foreman installs into a project, rather than something foreman runs itself — the response happens inside the affected repository, with whoever is already working there.

**Settled:** incident records conform to the Luma Knowledge Format. They are knowledge like any other record, not a separate filing system.

Open: whether the format already has a record type that fits, or whether an incident needs a new one — a timeline that accumulates during an event is a different shape from a record written once. If it needs one, that is a format request, not a reason to contort around the gap. Also open: where the records live, and whether driving and recording are one capability or two, since recording a timeline is useful even when nobody is being walked through the response.

## Other capabilities named but not yet captured properly

- Bootstrap a new project with the structure it should have had from the first commit.
- Install the standard tooling — linting, tests, continuous integration, independent review, a backlog.
- Meta-skills: skills that generate a project's own best-practice skills, rather than copying a template.
- Return periodically to confirm the latest learnings were actually applied.
- Git worktee workflows

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

## Define how to resolve common terms or requests

What does it mean when i say:
- I want a situation report
  you should respond with: "Let me drop the options and show you the actual situation."
- I need help coming up to speed
- Where did we leave off
- What do you know to be true
- Checkpoint

## Claude Code modes

Change what Claude Code's hooks allow or disallow with a command, per project, without editing the hook or restarting the session.

- Full trust mode
- Allow/disallow downloads
- Allow/disallow ssh
- Allow "trusted" ssh only
- Allow/disallow curl
- Allow harmless curl (non-executable files)

**Built.** Shipped as `luma-foreman policy` — see [docs/claude-permission-policy.md](docs/claude-permission-policy.md). What it settled, kept here because the reasoning is worth more than the code:

- The policy has to live in a file the hook reads on every call, not in `settings.json`. Claude Code snapshots hook *configuration* at session start, so a settings-based design needs a session restart per change; a file the hook re-reads takes effect on the next tool call.
- Resolution is per key, most specific wins: project, then a global fallback, then built-in defaults. A project only names what it overrides.
- Projects are keyed by repository root, slugged the way Claude Code names `~/.claude/projects`, so every session in a repo shares one policy no matter which subdirectory it started in.
- This is **workstation state, per project** — never committed. What an agent may do in a repository is the operator's call, not something every clone inherits.
- The value vocabulary is Claude Code's own — `allow`, `ask`, `deny` — plus `always` for bypass-proof, and refinements like `trusted` for ssh and `safe` for fetches. Not `disallow`; nothing in this space uses that word.
- Textual command matching is not a security boundary and must not be described as one. It catches your own slips and an agent's carelessness. Sandboxing is the boundary; this rides on top for ergonomics.
- Whatever governs the agent has to be something the agent cannot edit, including the gate itself. Solved with deny rules covering both the policy and the installed gate. The prototype protected the rulebook and not the lock. They deliberately live in *different* directories — configuration in `~/.config`, program files in `~/.local/share` — so that clearing your config cannot delete the gate, which would fail it open.
- A tool that has to touch someone else's config writes freely into the directory it owns and never silently edits the directory the user owns. `policy install` copies the gate and *prints* the `settings.json` changes, following `pre-commit install`.

Open: whether foreman additionally writes *committed* per-project Claude Code settings — the shared floor a team gets from a clone — with this machine-local layer as overrides on top. Those are two different capabilities that happen to touch the same file format. Also open: distribution. Install is currently a clone plus a symlink, which is fine for one operator and not for an organization.

## Workflows

A workflow is a [bundle](#bundles) type. The distribution, versioning and
selection questions are answered there; this entry is about what a workflow
contains.

I want all skill logic to live under workflows/ and then add thin adapaters to make it work with various agent harnesses so they can trigger the skills.  A workflow can be a single skill file or a folder of files, scripts, templates, examples, and more.

## Bundles

**Settled: a bundle is an LKF Knowledge Bundle.** Not a similar thing, the same
thing. LKF already defines a Bundle as "a self-contained, hierarchical
collection of knowledge documents — the unit of distribution", and foreman had
independently arrived at a self-contained, typed unit of distribution. Two names
for one idea was the only thing separating them.

This is stronger than a convenience. Foreman's thesis is that a standard is
knowledge in executable form; if that holds, a script, a template and a document
are the same substance at different degrees of executability, and one unit of
distribution is what follows rather than a tidy coincidence. It also collapses
three threads: hq curates bundles and foreman applies them — same artifacts,
different verbs — and incident records, already settled as LKF, become a bundle
type rather than a separate filing system.

Foreman therefore defines no format of its own. A bundle *type* is an LKF Type
Definition (§10.1) living in the bundle's reserved `_types/` directory,
declaring its fields and their obligations — `version`, `published`, and
whatever else a type needs. The manifest question is answered by a spec that
already exists.

**Settled: material is payload, not first-class (Model A).** The base object is
a typed markdown file. Scripts, templates and binaries ride along as material
the bundle carries; they carry no type and are not knowledge in their own right.

**Settled: they are just files.** A bundle contains **files**. A file with YAML
frontmatter and a `type` is a **document**. A file that a document links to is
an **attachment** — a relationship, not a category.

Two terms rather than three, and neither is invented. Naming the non-document
files something — `asset`, `payload`, `sidecar` — was the instinct throughout,
and every candidate had a flaw: `payload` inverts the relationship it names (an
HTTP payload is the point, the envelope is overhead; here the document is
primary), `sidecar` belongs to Kubernetes and means a companion *process*, and
`asset` was fine but unnecessary. `attachment` as the *category* was wrong for a
subtler reason worth keeping: it comes from paper correspondence and legal
filing, where an attachment belongs to one letter or one filing, so as a
category it smuggles in the document-level ownership this design rejects. As a
relationship it is exactly right.

The reason no word is needed is that the rules partition into *all files* and
*documents specifically* — the complement almost never has to be named. It also
matches the format's own first principle, that the files themselves are the
whole system; a second word for a file works against that.

Naming the relationship still pays. It gives the two checks their names: a
document linking to something that is not there is a **missing attachment**
(broken, fails on apply), and a file nothing links to is **nobody's attachment**
(cruft). Only `file` and `document` need to be normative; `attachment` is
derived vocabulary, worth defining so tools do not invent conflicting meanings.

**Required: documents must be able to link to files.** Material that cannot be
pointed at is dead weight; a workflow whose document cannot say "run
`scripts/setup.sh`" has not described a workflow.

The alternative was making every file a first-class member, and it fails on
contact: a shell script cannot carry YAML frontmatter and a PNG certainly
cannot, so every non-markdown member would need a sidecar or a manifest. That
trades away the format's best property — files that describe themselves — for
uniformity nobody asked for. Assets can be promoted to first-class later if
something genuinely needs a script to be versioned and linkable on its own;
going the other way, once every file needs a sidecar, is much harder.

**Settled: bundles do not depend on other bundles, in the MVP.** This is the
fork between a catalog and a package manager. Allowing dependencies buys version
resolution, conflicts, diamonds and a solver — a year of work that has eaten
better-funded projects. Every bundle is self-contained; if two need the same
material, it is copied, or the project adopts both. Boring, and boring is
correct here. Note that the word "bundle" was chosen partly because "package"
imports the opposite expectation.

**Wanted: what goes into a bundle should be unconstrained.** Files, scripts,
templates, examples, documentation, context — whatever a type needs, in whatever
shape it needs it.

Two kinds of flexibility hide in that sentence and they cost very differently.

*What a bundle contains* is free. Distribution is copying a directory,
versioning is a checksum over it, and verifying that what was applied still
matches what was adopted is the same checksum. None of that gets harder as the
contents get richer, so there is no reason to constrain them.

*What applying a bundle can do* is where to stay narrow. If a bundle ships an
install script, then adopting one means executing code that arrived from up to
three levels away, and the promotion chain — project to organization to luma to
every organization — becomes a supply chain. Foreman spends its other half
deciding what an agent is allowed to run; handing a catalog arbitrary execution
would undo that from the other side.

Proposed, not settled: contents unconstrained, placement declarative. A bundle
declares where its material goes; it does not bring a program that puts it
there. Same MVP scoping as the dependency decision, and reversible later if
something genuinely needs it.

### Format decisions for LKF

LKF is ours to change, so these are decisions rather than requests. Foreman
should not work around any of them locally.

**Rename the base object from Concept to Document.** A `lab_result` is not a
concept. Neither is a `task`, nor an incident timeline, nor a bundle's manifest.
The spec has to stretch to cover them — "a tangible asset, an abstract idea, or
anything in between" — which is the sound of an abstraction named after its
first instance. Meanwhile the spec's own prose already says the right word when
speaking plainly: a bundle is "a collection of knowledge **documents**".
`concept` then becomes what it always was — one type, for genuinely conceptual
entries like `wiki/concepts/diffusion-models` — extending the base through the
`extends` mechanism §10.3 already provides. LKF is `v0.0.3` and declares the
`0.0.z` tier unstable, so this is exactly the window such a change exists for.

**A bundle holds non-document files.** The spec
currently defines a bundle as markdown documents and rules on nothing else.
Model A needs it to say yes.

**A bundle describes itself.** Two separate things, easy to conflate:

- `_types/bundle.md` — the Type Definition, declaring what a bundle document
  carries. One per format.
- a document at the bundle root with `type: bundle` — the instance, carrying
  *this* bundle's values. One per bundle.

Its fields:

| field | obligation | why |
| --- | --- | --- |
| `type: bundle` | mandatory | it is the only hard requirement LKF has |
| `version` | mandatory | the entire adopt-and-pin model is version-shaped — "do not change under me", "a newer one exists", "you are two behind", "this mandate is unmet" mean nothing without it. A bundle foreman cannot pin is one it cannot honestly say anything about |
| `published` | recommended | wanted for adoption deadlines, but a bundle works without a date |
| `description` | recommended | |

`version` is mandatory on the asymmetry rather than on principle: going
mandatory → recommended later breaks no existing bundle, while recommended →
mandatory invalidates every bundle that skipped it. Require now, relax if it
proves wrong. It also costs nothing to declare, since in LKF `mandatory` is
published intent rather than a gate — foreman is what enforces it.

**Specify non-document files.** Naming them is the easy half; six things need answering
before the concept is specified rather than gestured at.

1. *What it is.* A file in a bundle that is not a document — no frontmatter, no
   `type`, not subject to Type Definition validation. "Not a document" is the
   whole definition and should be stated plainly.
2. *Where it lives.* Anywhere in the bundle. A reserved `_files/` would fight
   the natural `scripts/`, `templates/`, `examples/` layout a workflow bundle
   wants.
3. *Placement is deliberately unspecified.* A file may sit beside the
   document that uses it, in a `scripts/` directory, in a shared folder —
   wherever the author finds natural. Nothing mechanical needs to know: not
   resolving a reference, not detecting dead files, not vendoring, not
   applying. Ownership is a convention for humans, so specifying it buys
   nothing and forecloses cases that genuinely differ — one document with three
   scripts wants colocation, ten documents sharing one template obviously do
   not. If a convention proves dominant, promote it later to a `recommended`,
   which breaks no existing bundle.

   The one real constraint is **self-containment**: a linked file must be
   *inside* the bundle, and a link must resolve to something that is actually there. A path leading outside the directory breaks the property the
   whole distribution model rests on — that you can tar it, ship it, and have
   it still work.

4. *Containment, reference and ownership are three questions, and only the
   first two have answers.* The **bundle** contains files — it is the
   directory and the unit of distribution, so they travel with it. **Documents
   reference** them, and any document may link any file; several may link the
   same one, or none may. **Nothing owns** a file in a lifecycle sense: delete a
   document and the files it linked do not vanish, they merely stop being
   anybody's attachment. That is precisely why dead-file detection is worth
   having — with no owner, unreferenced files accumulate
   in silence and only a check will say so. Per-document folders
   (`foo.md` + `foo.assets/`) were the alternative: tidier, and a rule nobody
   follows.
5. *ID.* §3 strips `.md` from a document's ID. A non-document file's ID keeps its
   extension, or `setup` is ambiguous between `setup.md` and `setup.sh`.
6. *Referencing.* LKF's own roadmap already carries the candidate rule, and it
   is better than the wikilink scheme first proposed here: `[[…]]` links
   documents, `[…](…)` links everything else. No new syntax, no change to the ID
   rules, no extension-ambiguity to resolve, and the distinction is visible at a
   glance. Foreman parsing two link forms is trivial and is not the format's
   problem.
7. *Consumer obligations.* Tolerate a missing target, consistent with §3 on
   unresolved links; preserve non-document files when rewriting a bundle; never reject a
   bundle for carrying them.

An earlier draft of this entry argued for wikilinking non-document files. That was wrong
twice over: it mistook the spec's document-to-document definition of Link for a
design constraint, and it charged foreman's convenience — one uniform traversal
— to the format's spec surface.

### The seam: LKF never rejects, foreman must

LKF is emphatic that consumers "MUST NOT reject a Concept for: missing
recommended or optional fields, an unrecognized `type`, unknown extra keys, or
unresolved links", and that a Type Definition publishes *intent* — validation is
"never a conformance gate, and it never rejects by default".

Foreman's whole job is to reject. So **conformant LKF will never mean valid
foreman bundle**: a bundle missing its `version` is perfectly legal LKF and
useless here. That enforcement lives in foreman, explicitly, and someone will
eventually assume the format is doing work it openly refuses to do.

This is also where the file rules land: LKF tolerates a dangling link, foreman
must fail on one. A bundle referencing a script that is not there stays
perfectly conformant and then breaks the moment it is applied. That gives
foreman two checks with different severities — a **missing attachment** is
broken and fails on apply; a file that is **nobody's attachment** is merely
cruft.

One place the seam cuts the right way: §3 requires consumers to tolerate links
whose target does not resolve. That is exactly the property that lets bundles
reference each other without a resolver — so "no dependencies in the MVP" means
no *resolution*, not no references.

The rest of this section was originally captured as "strategy selection". A
strategy is now one type of bundle; the reasoning below applies to all of them.


I want to have a catalog of strategies to apply to each project.  And for each project I can choose from the catalog (either via copy or maybe symlink, this mechanism needs to get fleshed out) to apply them to my given project by using a command found in luma-foreman.   The `luma-hq` project will help us define the strategies we can select from for our org.  `luma-hq` will use its breadth of organization knowledge to develop the strategies and then it will promote them to luma-foreman where they become available for selection.  But strategies do not HAVE to come from luma-hq, they can start bluegrass style where a strategy is either unique to a project, or it is trialed in a project and then eventually gets circulated up and through hq.  It is a two way street, it is just that hq will have the context of all projects and foreman will have the context of a single project.   

There will be three buckets of stategies:
- Universal strategies, provided by luma organization for all other organizations to select from (not just for the luma organization)
- Organization strategies, provided by your organization — specific to your organization, these will go under your own git repo and your own version of luma-hq will help you establish them
- Project strategies, provided by a given project and not shared enough to get promoted to organization or universal strategies

Then each project will somehow select from these buckets what strategies get applied.  And we need to select in a way where as strategies change the project doesn't get it's strategy changed from underneath it.  For example if a universal strategy XYZ goes from v1.0.0 to v2.0.0 then the project should not automatically adopt v2.0.0 but it should be made aware that new stratgies are available.

And either this project luma-foreman and/or luma-hq should be able to force new strategies down for critical stuff where projects are not allowed to adopt on their own schedule.  It's mandated and immediate.  

A nice to have is when new strategies are published they should also publish some kind of date that lets projects know what kind of timeline they have to reasonably adopt them before they "fall out of compliance".

The same mechanism serves [Workflows](#workflows). A strategy is context and a workflow is skill content, but both are material published in a catalog, selected per project, and versioned — so they should share one distribution model rather than growing two.

### How a bundle arrives: mandated or adopted

Two independent axes, and conflating them is what makes this hard to write about.

**Scope** is where a bundle lives: universal, organization, or project — the
three buckets above.

**Arrival** is how it reached a project:

- **mandated** — handed down; the project cannot decline it and cannot drop it
- **adopted** — the project decided it applies; it may later drop it

|  | universal | organization | project |
| --- | --- | --- | --- |
| **mandated** | everyone, no opt-out | this organization, no opt-out | — |
| **adopted** | picked off the shelf | picked off the shelf | written here |

Nothing in the catalog is advisory. Both kinds bind identically once in place,
and Inspect does not care how a bundle arrived — a project that adopted
something and then drifted from it fails exactly as hard as one ignoring a
mandate. The difference shows up only at the edges: what a project is allowed to
stop doing, and who it has to argue with to stop.

"Optional" is the wrong word for the second kind and was the first word tried.
It implies weaker enforcement, and there is none.

The empty cell is the interesting one. A project cannot meaningfully mandate
something to itself — whatever it wrote, it can unwrite. Project scope is always
adopted, which means *mandated* names precisely the tier that arrives from
somewhere the project does not control. That is what earns it a separate word.

**Mandates are what stop "adopt nothing" from being compliant.** Without them a
project that opts into nothing passes every check trivially, and Inspect
measures enthusiasm rather than conformance. The mandated tier is the floor that
makes a green result mean something on a project that never opted into anything.

### Bundles are a distribution problem, and it is already solved elsewhere

Nothing above is a new problem. A catalog, per-project selection, pinned versions, "do not change under me", "tell me what is available", "this one is mandatory", "here is your deadline" — that is package management, and every part of it is solved somewhere worth stealing from rather than inventing against.

| wanted | prior art |
| --- | --- |
| the catalog | a registry |
| what this project selected | a manifest — `package.json`, `Gemfile` |
| do not change under me | a lockfile, plus a vendored copy |
| tell me what is new | `npm outdated`, `bundle outdated` |
| mandatory and immediate | a security advisory — `npm audit`, Dependabot |
| adoption deadline | a deprecation window, a remediation SLA |
| promotion upward | contributing a fork back upstream |

It also lands on the four jobs without stretching. **Outfit** applies what a project selected. **Inspect** verifies that what is applied still matches what was selected. **Refit** is the outdated-and-overdue report, which is already what its charter line describes: return over time and confirm the latest learnings were actually applied, not just published.

**Settled: vendor into the project, do not reference.** The open copy-or-symlink question is answered by the charter rather than by taste. Inspect must run in a fresh clone with no configuration and no organization access. If a project's strategies live by reference in an organization repository, a continuous integration run cannot verify compliance at all — it can only report the check as skipped, and the project's whole posture becomes unverifiable in the place it most needs verifying. Vendoring also buys the no-surprise property outright: a vendored copy cannot change underneath a project, because changing it is a commit.

Open, in the order they block:

**Is a strategy content, or content plus a check?** This decides everything downstream. If a strategy is only context and skill files, "applied" means the files match the vendored copy — a checksum, and Inspect stays trivial. If a strategy can also assert something about a project ("this repository uses conventional commits"), then strategies carry executable rules, the catalog becomes a plugin system, and Inspect needs the rule configuration format currently being deferred. Start content-only and let the first strategy that genuinely needs a check force the question.

**Vendoring publishes an organization's strategies into every project that uses them.** A private strategy vendored into a repository that is later opened up is now public. That is the same class of leak the identity work was about, and it will happen the first time someone open-sources a project. Either organization strategies are public-safe by construction, or they carry a confidential marker and `outfit` refuses to vendor them into a repository with a public remote.

**A mandate needs an escape hatch, or people route around the tool.** A mandatory strategy that breaks a project leaves someone choosing between fixing it immediately and deleting foreman, and they will delete foreman. The usual answer is a declared exception with an owner and an expiry, which Inspect reports as a finding rather than silently honouring — visible, time-boxed, and itself out of compliance.

Also open: how two strategies that both want to write the same file compose, and whether a strategy identity survives promotion from project to organization to universal without becoming a second copy with a different name.

**Watch the Authority limit.** "hq will have the context of all projects" is right, and it is exactly what the charter forbids foreman from having. Keep the promotion pipeline one-directional in terms of knowledge: foreman makes one project's strategy usage legible and exportable; hq is what looks across many projects and notices a pattern worth promoting. Foreman must never need to know what any other project selected.

## Permission modes

I want to be able to setup a mode in the config or via the command line or both.

It will make it so when I say I want to be in "foobar" mode it auto applies all my permissions to the way I set them.  The simpliest way is the setting sits as a mapping in the config.  The nice to have would be taking a snapshot of my current settings, name it, and then the current settings get added to config as a new mapping set.