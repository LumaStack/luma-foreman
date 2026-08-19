# Ideas

Wanted capabilities, captured so they survive. Nothing here is designed, ordered, or committed to — this is a holding pen, like `docs/examples/`. Expect it to be replaced by `.luma/backlog/` once the repository is ready for it.

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

**Settled: the vocabulary.** Every file in a bundle is either a document or an
asset. A document carries YAML frontmatter with a `type`; an asset does not. No
overlap, no third category, no exception clause.

| term | meaning |
| --- | --- |
| file | anything on disk — used loosely, defines nothing |
| **document** | a file with frontmatter and a `type` |
| **asset** | a file without |
| attachment | an asset a document links to — derived, names the two checks |

Only `document` and `asset` are normative. `attachment` is derived vocabulary,
worth defining so tools do not invent conflicting meanings for it, and it earns
its place by naming the two checks: a document linking to something that is not
there is a **missing attachment** (broken, fails on apply), and an asset nothing
links to is **nobody's attachment** (cruft). Different severities, different
remedies.

Three candidates were rejected, and two of the reasons generalise. `payload`
inverts the relationship it names — an HTTP payload is the point and the
envelope is overhead, whereas here the document is primary. `sidecar` belongs to
Kubernetes and means a companion *process*. `attachment` as the *category* name
comes from paper correspondence and legal filing, where an attachment belongs to
one letter or one filing — so as a category it smuggles in the document-level
ownership this design rejects, while as a relationship it is exactly right.

`file` was the last one considered and the closest call. It is the plainest
possible word and free to learn, but a document *is* a file, so narrowing it to
mean the others needs a defusing sentence in the spec and then charges a small
ambiguity tax forever — "the bundle has twelve files" becomes a question, and a
`files` subcommand that omits documents is surprising. `asset` costs one
glossary entry and nothing after.

**Required: documents must be able to link to assets.** Material that cannot be
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
declares where its material goes; nothing runs to put it there. Same MVP
scoping as the dependency decision, and reversible later if something genuinely
needs it.

**To be unmistakable, because this has already been misread once: bundles carry
executables freely.** A workflow that ships `scripts/check.sh` is ordinary and
often required — that is what projects into a harness skill, and a workflow
whose scripts could not travel with it would project into a skill that does not
work.

The constraint is on **adoption**, not on contents. `foreman adopt` copies files
and runs nothing. A script in a bundle executes when a person or an agent
deliberately invokes it, having seen what it is — which is an ordinary script,
not a supply chain. What would make it one is code executing as a side effect of
fetching, before anyone has looked.

### Format decisions for LKF — shipped

These landed in `luma-knowledge-format` on `develop`, unreleased, destined for
the next tag. Foreman can rely on them once that release is cut.

- **`Concept` → `Document`.** `document` is the root type every type implicitly
  extends; `concept` is now an ordinary built-in type for knowledge-base
  entries. No file has to change — "Concept" was the spec's word for the object,
  never a value anyone wrote.
- **Assets and attachments.** Every file in a Bundle is a Document or an Asset.
  An Attachment is an Asset a Document links to.
- **Asset links.** `[[…]]` links a Document, `[…](…)` links anything else. A
  link must point inside the Bundle; whether the target exists is separate, and
  an unresolved link stays legal.
- **`bundle` built-in type and `bundle.md`.** A Bundle describes itself at its
  root with `type: bundle`, `version` mandatory (`semver`), `published`
  recommended. `description` is inherited from the core fields as `optional` —
  inheritance is add-only, so a type cannot restate a field to strengthen it.
- **`semver` field type.** Full semver, no `v` prefix.
- **Built-in types ship as files** in LKF's own `_types/`, making that repo a
  Bundle.
- **Redefining a built-in is `SHOULD NOT`,** not `MUST NOT`.

Still open in LKF, tracked in its own `docs/ROADMAP.md` under *Next steps*: the
`extends: source` errata, whether a Type Definition carries a `version`, and
whether `concept` should ever carry fields of its own.

The earlier decisions below stand as the reasoning behind those changes.

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

**A bundle holds assets.** The spec
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

**Specify assets.** Naming them is the easy half; six things need answering
before the concept is specified rather than gestured at.

1. *What it is.* A file in a bundle that is not a document — no frontmatter, no
   `type`, not subject to Type Definition validation. "Not a document" is the
   whole definition and should be stated plainly.
2. *Where it lives.* Anywhere in the bundle. A reserved `_assets/` would fight
   the natural `scripts/`, `templates/`, `examples/` layout a workflow bundle
   wants.
3. *Placement is deliberately unspecified.* An asset may sit beside the
   document that uses it, in a `scripts/` directory, in a shared folder —
   wherever the author finds natural. Nothing mechanical needs to know: not
   resolving a reference, not detecting dead assets, not vendoring, not
   applying. Ownership is a convention for humans, so specifying it buys
   nothing and forecloses cases that genuinely differ — one document with three
   scripts wants colocation, ten documents sharing one template obviously do
   not. If a convention proves dominant, promote it later to a `recommended`,
   which breaks no existing bundle.

   The one real constraint is **self-containment**: an asset must be *inside*
   the bundle, and a link must resolve to something that is actually there. A path leading outside the directory breaks the property the
   whole distribution model rests on — that you can tar it, ship it, and have
   it still work.

4. *Containment, reference and ownership are three questions, and only the
   first two have answers.* The **bundle** contains assets — it is the
   directory and the unit of distribution, so they travel with it. **Documents
   reference** them, and any document may link any asset; several may link the
   same one, or none may. **Nothing owns** an asset in a lifecycle sense: delete
   a document and the assets it linked do not vanish, they merely stop being
   anybody's attachment. That is precisely why dead-asset detection is worth
   having — with no owner, unreferenced files accumulate
   in silence and only a check will say so. Per-document folders
   (`foo.md` + `foo.assets/`) were the alternative: tidier, and a rule nobody
   follows.
5. *ID.* §3 strips `.md` from a document's ID. An asset's ID keeps its
   extension, or `setup` is ambiguous between `setup.md` and `setup.sh`.
6. *Referencing.* LKF's own roadmap already carries the candidate rule, and it
   is better than the wikilink scheme first proposed here: `[[…]]` links
   documents, `[…](…)` links everything else. No new syntax, no change to the ID
   rules, no extension-ambiguity to resolve, and the distinction is visible at a
   glance. Foreman parsing two link forms is trivial and is not the format's
   problem.
7. *Consumer obligations.* Tolerate a missing target, consistent with §3 on
   unresolved links; preserve assets when rewriting a bundle; never reject a
   bundle for carrying them.

An earlier draft of this entry argued for wikilinking assets. That was wrong
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

This is also where the asset rules land: LKF tolerates a dangling link, foreman
must fail on one. A bundle referencing a script that is not there stays
perfectly conformant and then breaks the moment it is applied. That gives
foreman two checks with different severities — a **missing attachment** is
broken and fails on apply; an asset that is **nobody's attachment** is merely
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

### The vocabulary: reach and obligation

Two axes, and conflating them is what made this hard to write about. Earlier
drafts had three; the third dissolved, for a reason worth keeping.

**Reach** is which catalog a bundle came from — universal, organization, or
project. It is **never declared**. A bundle in the universal catalog has
universal reach because that is where it is, so promotion is a directory move
with nothing to edit and no way for a bundle to misstate how far it travels.

**Obligation** is how strongly the publishing catalog expects a project to adopt
it. Declared per bundle in that catalog's `catalog.md`, never in the bundle —
the same bundle is mandatory at one organization and merely available
everywhere else, so it cannot be a property of the bundle itself.

- **mandatory** — must be adopted. With a `by` date it is a warning and a
  countdown until then and a failure after; with no date, a failure immediately.
- **recommended** — reported as a gap, never fails. A project may decline, and
  ideally records why.
- **optional** — a curated shortlist. Never reported as missing. This is what
  separates "worth knowing about" from the rest of the catalog, which is
  available regardless.
- **deprecated** — reported if still adopted. The retirement path a catalog
  needs and earlier drafts had no room for.

**Settled: this is the Luma Knowledge Format's own field ladder, reused
deliberately.** §5 already defines `mandatory` / `recommended` / `optional` /
`deprecated` for fields. This is the same question — how strongly is this
expected — asked about a bundle instead of a field, so a parallel vocabulary
would be two words for one idea.

**The distinction that has to survive:** *obligation governs whether you must
adopt; it does not govern how hard conformance is checked once you have.* A
recommended bundle a project chose to adopt is checked exactly as strictly as a
mandated one — drift is drift. What `recommended` buys is the freedom not to
adopt it at all, and nothing else.

That split is what keeps an earlier position intact. This entry previously said
nothing in the catalog is advisory, on the grounds that a graded severity is the
setting everyone quietly turns down to `warn` until failures stop happening. That
danger is real, and it lives entirely in the second question. Grading the first
one costs nothing, because a project that declined a recommendation is not
failing — it simply has not adopted it.

**Optional is a rung, not a mistake.** An earlier draft rejected the word for
implying weaker enforcement. It does imply that, and now that is correct: the
enforcement being weakened is on *adoption*, not on conformance.

**Location carries the metadata, when it can.** Two of three proposed fields
dissolved into where the thing already sits: which catalog a bundle came from,
and who to ask for an exemption — whichever catalog declared the obligation.

The third did not, and the failure sharpened the rule. Which level a bundle can
be adopted at was briefly a directory, `project/` and `organization/`. But a
bundle can apply at both, and **a path can only ever say one** — so bundles are
flat and declare `consumers`. A bundle's path is its identity for adoption, so
whatever is encoded there cannot change without breaking every pin and adopt
command referring to it. **The path carries only what is single-valued and
permanent**; everything else is a field. Settled in `luma-hq/DECISIONS.md`.

A project's own bundles have no obligation, and that gap is meaningful. A
project cannot mandate anything to itself — whatever it wrote, it can unwrite —
so obligation names precisely what arrives from somewhere the project does not
control.

**Mandatory bundles are what stop "adopt nothing" from being compliant.**
Without them a project that opts into nothing passes every check trivially, and
Inspect measures enthusiasm rather than conformance. They are the floor that
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

### A catalog's content belongs in one subtree

**Proposed, not settled.** A catalog repository holds two different things: the
catalog itself — `catalog.md`, `_types/`, `bundles/` — and the project that
maintains it, which is documentation, a changelog, contribution guidance, and
continuous integration. Those should not share a root namespace.

Today they do not collide, because a fresh catalog has only the two content
directories. The collision arrives with the third thing. Once `docs/` exists, a
reader has to know by convention which top-level entries are content, and adding
a third content directory later — a `workstation/` seat, say — puts it beside
`docs/` with nothing structural telling them apart.

```
luma-catalog/
  catalog/
    catalog.md
    project/
    organization/
  docs/
  README.md
```

Nesting makes the boundary mechanical rather than conventional: everything under
`catalog/` is the catalog, everything outside maintains it. It is the move the
format repository already made for its own bundle, and the reasoning transfers —
the specification, the changelog and the project documentation maintain that
bundle rather than being part of it.

Two things this buys beyond tidiness. A sparse checkout can name exactly the
content, which only works if there is one subtree to name. And it gives any
program that consumes catalogs a single unambiguous answer to "where does the
content start" — otherwise every such program needs its own rule about which
root directories count, and they will disagree.

**A catalog is not a bundle, and the layout should not imply it is.** A bundle
carries a mandatory version; a catalog carries none. A bundle is copied
wholesale; a catalog is read and picked from. A bundle contains documents and
assets; a catalog contains bundles. Calling the subtree a bundle would owe an
answer to whether an outer version bumps when an inner one does — a question
with no good answer and no reason to have been asked. Same layout pattern,
different kind of thing.

**The cost curve is one-directional.** With no bundles and no consumers this is
a two-path move. After bundles exist it invalidates every pinned path and every
adopt command anyone has written down.

**Closed: the scope directories are gone.** `project/` and `organization/` were
briefly going to become `for-projects/` and `for-organizations/`, on the grounds
that a directory name almost always describes its contents and these held
bundles rather than projects. That naming question died with the directories
themselves — a bundle can apply at both levels, so the fact was never
single-valued and never belonged in a path. Bundles are flat and declare
`consumers`. Settled in `luma-hq/DECISIONS.md`.

Worth keeping from the naming detour, since the question recurs for any scope
directory: `by-` is wrong in directory names — it means *grouped by* or
*authored by*, so `by-project/` promises one subdirectory per project. And
singular scope directories do have real precedent, `/etc/systemd/system/` and
`.../user/` holding units rather than systems or users, but that convention
works because it was learned once from ubiquitous documentation, which a new
format does not have.

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

## Permission modes

I want to be able to setup a mode in the config or via the command line or both.

It will make it so when I say I want to be in "foobar" mode it auto applies all my permissions to the way I set them.  The simpliest way is the setting sits as a mapping in the config.  The nice to have would be taking a snapshot of my current settings, name it, and then the current settings get added to config as a new mapping set.