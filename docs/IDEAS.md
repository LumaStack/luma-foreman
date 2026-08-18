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

I want all skill logic to live under workflows/ and then add thin adapaters to make it work with various agent harnesses so they can trigger the skills.  A workflow can be a single skill file or a folder of files, scripts, templates, examples, and more.

## Strategy selection

I want to have a catalog of strategies to apply to each project.  And for each project I can choose from the catalog (either via copy or maybe symlink, this mechanism needs to get fleshed out) to apply them to my given project by using a command found in luma-foreman.   The `luma-hq` project will help us define the strategies we can select from for our org.  `luma-hq` will use its breadth of organization knowledge to develop the strategies and then it will promote them to luma-foreman where they become available for selection.  But strategies do not HAVE to come from luma-hq, they can start bluegrass style where a strategy is either unique to a project, or it is trialed in a project and then eventually gets circulated up and through hq.  It is a two way street, it is just that hq will have the context of all projects and foreman will have the context of a single project.   

There will be three buckets of stategies:
- Universal strategies, provided by luma organization for all other organizations to select from (not just for the luma organization)
- Organization strategies, provided by your organization — specific to your organization, these will go under your own git repo and your own version of luma-hq will help you establish them
- Project strategies, provided by a given project and not shared enough to get promoted to organization or universal strategies

Then each project will somehow select from these buckets what strategies get applied.  And we need to select in a way where as strategies change the project doesn't get it's strategy changed from underneath it.  For example if a universal strategy XYZ goes from v1.0.0 to v2.0.0 then the project should not automatically adopt v2.0.0 but it should be made aware that new stratgies are available.

And either this project luma-foreman and/or luma-hq should be able to force new strategies down for critical stuff where projects are not allowed to adopt on their own schedule.  It's mandated and immediate.  

A nice to have is when new strategies are published they should also publish some kind of date that lets projects know what kind of timeline they have to reasonably adopt them before they "fall out of compliance".

The same mechanism serves [Workflows](#workflows). A strategy is context and a workflow is skill content, but both are material published in a catalog, selected per project, and versioned — so they should share one distribution model rather than growing two.

### Strategies are dependencies

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