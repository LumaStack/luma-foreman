# luma-foreman

> Every repository set up right, and kept that way.

It walks into a project repository, sets it up to succeed, and comes back periodically to check the work still holds.

> **Status:** early. Adoption, projection and inspection work end to end; `bootstrap` and `refit` are still shape.

## The foreman jobs

- **Bootstrap.** Stand a new project up with the structure it should have had as soon as possible.
- **Adopt.** Adopt a bundle of knowledge from a catalog and make it available in this repository.
- **Outfit.** Wire up what was adopted so agents use it correctly, so nobody has to say where to look.
- **Inspect.** Check a project against the baseline and report where it falls short.
- **Refit.** Return over time and confirm the latest learnings have actually been applied, not just published.

## Knowledge in, agent out

The loop foreman exists for. A catalog publishes bundles, a project adopts the ones it wants, and the projection puts them where an agent will meet them without being told to look.

```bash
luma-foreman adopt --list --from https://github.com/LumaStack/luma-catalog
luma-foreman adopt luma/decision-records --from https://github.com/LumaStack/luma-catalog
luma-foreman outfit
```

**`adopt` is a directory copy with a receipt.** The bundle lands in `.luma/bundles/<org>/<name>/` and `adopted.toml` records the version, where it came from, the catalog commit, and a checksum of exactly what landed. Nothing resolves and nothing is fetched later — bundles depend on nothing, which is what keeps this a copy rather than an install. The copy is committed, so a fresh clone with no network reproduces the project exactly.

An edited copy is never silently overwritten, and a bundle with no version cannot be adopted at all.

**`outfit` writes thin adapters, never copies.** Each workflow becomes a Claude Code skill that points at the real document under `.luma/` and names the standing context that document assumes. A managed block in `CLAUDE.md` indexes everything adopted, with `preload: mandatory` documents hoisted into a *read these first* section — load the index, never the content.

Everything it writes is generated and disposable: commit it or gitignore it, but regenerate rather than edit. Only the region between the `luma:begin` and `luma:end` markers in `CLAUDE.md` is touched, so a hand-written file keeps the rest.

## What works today

**`luma-foreman agent-permissions`** — per-project control over what Claude Code is allowed to do, changed with a command instead of by editing a hook. Claude Code's own permission rules are global; this adds a per-project layer, so loosening a rule for one repository does not loosen it everywhere. See [docs/claude-agent-permissions.md](docs/claude-agent-permissions.md).

```bash
luma-foreman agent-permissions                 # what is allowed in this repository, and why
luma-foreman agent-permissions allow curl      # ...and change it, effective on the next tool call
luma-foreman agent-permissions doctor          # ...and confirm it is actually working, not just wired up
```

**`luma-foreman inspect`** — checks a repository against the baseline and reports where it falls short. Findings, exit codes, runnable in continuous integration. Four rules so far:

- **identity** — personal information published through git: machine-derived author identities, malformed addresses, home directory paths in tracked content.
- **secrets** — provider-issued credentials in tracked content, and files that normally hold them. Findings never contain the secret itself, because findings end up in continuous integration logs.
- **bundles** — bundles broken in ways nothing else notices: a dangling link, an unquoted wikilink in frontmatter, a template carrying live frontmatter. All three are conformant, so the bundle publishes cleanly and the defect travels.
- **adoption** — an adopted bundle that is no longer what was adopted: edited in place, missing from disk, or adopted and projected nowhere. The last one reads green from every angle while the project quietly carries rules no agent has seen.

```bash
luma-foreman inspect                # 0 nothing found, 1 findings, 2 could not run
luma-foreman inspect --json         # for continuous integration
luma-foreman inspect --rule adoption
```

Every check works in a bare clone with no configuration, and a check that *cannot* run is reported as skipped rather than passed — an inspection that reads clean while silently skipping half its checks is worse than no inspection.

`bootstrap` and `refit` print "not built yet" and exit 2.

## Install

Requires Python 3.11+ and git. No build step, no dependencies to install.

```bash
git clone https://github.com/LumaStack/luma-foreman.git
ln -s "$PWD/luma-foreman/bin/luma-foreman" ~/.local/bin/luma-foreman   # or add bin/ to PATH

luma-foreman agent-permissions install
```

`agent-permissions install` installs the permission gate into `~/.local/share/luma/luma-foreman/` and then **prints** the two changes you need to make to `~/.claude/settings.json`. It does not edit that file: foreman writes freely into the directory it owns and never silently edits config you own. Re-run it after every upgrade — it is idempotent and says when there is nothing to do.

The only thing you have to change by hand is `~/.claude/settings.json`, and `agent-permissions install` shows you exactly what. Hook wiring needs a Claude Code restart to take effect; policy changes after that are live.

Run the tests with `sh tests/run`. They are hermetic — `HOME` and `LUMA_FOREMAN_HOME` are redirected into temp directories, so running them never touches your configuration.

It also carries **meta-skills**: skills whose job is to generate a project's own best-practice skills, so each repository ends up with tooling suited to it rather than a copied template.

The goal is projects that are homogeneous where homogeneity pays and optimal where it does not.

## The constraints that define this repository

**luma-foreman can always run on its own.**

luma-leader is optional. When one exists, foreman may use it and may be better for
it. When one does not, nothing foreman does stops working.

That is a guarantee, not a ban. Consulting hq is allowed and may well be worth
doing; requiring it is not. Every capability gets the same question — does this
still work with no hq? — and some things honestly cannot exist without one.
"How does this project compare to the other forty?" is not answerable from one
repository, and pretending otherwise would be a lie. What the guarantee protects
is that the jobs foreman already does keep working.

**Foreman enforces standards; it does not decide them.**

**Foreman does not accumulate knowledge across projects** — that is hq's job,
and the moment answering a question requires knowing about your *other*
repositories, the question belonged to hq.

But knowledge can travel both ways. Plenty of it starts in one project and
outgrows it, and foreman should make promoting it upward easy — to an hq if
there is one, which is what can circulate it back down to everyone else.
Foreman is where knowledge can originate and always where it lands; hq is what
carries it between projects.

## Where state lives

| scope | holds | committed |
| --- | --- | --- |
| shipped | the standards, as executable rules | yes, in this repository |
| project | decisions about a project that its whole team shares | yes, in the target repository |
| workstation | who this operator is, what this machine trusts | no |
| workstation, per project | this operator's decisions about one repository | no |

The last row is the awkward one, and it earns its place: some per-project decisions must not be committed. What an agent is permitted to do inside a repository is the operator's call on their own machine, not a property of the repository that every clone should inherit.

## Which jobs run where

**Inspect** is the job that must survive a bare environment — fresh clone, no configuration, no organization access, exit codes, continuous integration. It is the one that has to hold the line.

**Bootstrap**, **Outfit** and **Refit** are workstation operations. They change a repository, they expect an operator, and they may use workstation state to do it. Requiring them to run in continuous integration was never the point and would buy nothing.

## Relationship to luma-leader

Two of the three limits live here: **Existence** first, then **Authority**.

**hq is optional.** Many organizations will never have one, so foreman has to be worth installing on its own. What ships here is a complete and defensible standard, not a stub waiting for orders.

Where an hq does exist, the division is: luma-leader is where a standard is argued, decided, and justified, and where the organization's view across every project lives. luma-foreman is where a standard becomes executable and gets enforced, one repository at a time. Changes flow one way: hq settles, foreman ships.

Foreman does not do hq's job. It does not argue standards, and it does not accumulate knowledge across projects in order to decide something — the moment answering a question requires knowing about your *other* repositories, that question belonged to hq.

Bookkeeping is not that. Knowing which repositories this workstation has configured is local state; knowing what the organization owns is hq's.
