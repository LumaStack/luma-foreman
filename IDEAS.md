# Ideas

Wanted capabilities, captured so they survive. Nothing here is designed, ordered, or committed to — this is a holding pen, like `examples/`. Expect it to be replaced by `.backlog/` once the repository is ready for it.

## Stop personally identifiable information from leaking into git

Projects must not publish the maintainer's real name, personal email, home paths, or machine names. Secrets scanning is the obvious sibling and probably the same machinery with a different list.

Four surfaces, and the non-obvious ones are where the leaks actually happen:

- **Working tree content** — names, emails, `/Users/<name>` paths, hostnames.
- **Commit metadata** — author and committer identity on every commit. This is the surface that leaked in practice while the docs looked clean.
- **History content** — committed once and deleted later is still published.
- **Configuration** — whether `user.email` is set to a noreply address, and whether anything prevents the next bad commit.

Delivery mechanism is undecided. Candidates: install a hook into every project, write the rule into each project's `CLAUDE.md`, run as an inspection only, or some combination. Prevention and detection are both wanted; which one leads is open.

Open design question: the check needs to know which identities are private, but foreman must run with no organization context. That pushes the list into each project being checked — where it is itself published. Hashes rather than literals is one way out.

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

**Settled by a working prototype**, currently living in the maintainer's dotfiles as `permission-gate.sh` plus a `luma-policy` command:

- The policy has to live in a file the hook reads on every call, not in `settings.json`. Claude Code snapshots hook *configuration* at session start, so a settings-based design needs a session restart per change; a file the hook re-reads takes effect on the next tool call.
- Resolution is per key, most specific wins: project, then a global fallback, then built-in defaults. A project only names what it overrides.
- Projects are keyed by repository root, slugged the way Claude Code names `~/.claude/projects`, so every session in a repo shares one policy no matter which subdirectory it started in.
- This is **workstation state, per project** — never committed. What an agent may do in a repository is the operator's call, not something every clone inherits.
- The value vocabulary is Claude Code's own — `allow`, `ask`, `deny` — plus `always` for bypass-proof, and refinements like `trusted` for ssh and `safe` for fetches. Not `disallow`; nothing in this space uses that word.
- Textual command matching is not a security boundary and must not be described as one. It catches your own slips and an agent's carelessness. Sandboxing is the boundary; this rides on top for ergonomics.
- Whatever governs the agent has to be something the agent cannot edit, including the gate itself. The prototype protects the policy files and *not* the gate script, which is a live gap.

Open: relocating it here from the dotfiles, and what that means for installation on a workstation that has no chezmoi. Also open: whether foreman additionally writes *committed* per-project Claude Code settings — the shared floor a team gets from a clone — with this machine-local layer as overrides on top. Those are two different capabilities that happen to touch the same file format.