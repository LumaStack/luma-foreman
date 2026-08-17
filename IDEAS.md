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

## Claud code modes

I want to be able to edit how claude code hooks allow or disallow using a command that changes how the hooks code works.  Either by editing claude config or by having claude config run a command and i can change how the command works.

- Full trust mode
- Allow/disallow downloads
- Allow/disallow ssh
- Allow "trusted" ssh only
- Allow/disallow curl
- Allow harmless curl (non-executable files)
