# luma-foreman

Runs the site. It walks into a project repository, sets it up to succeed, and comes back periodically to check the work still holds.

> **Status:** early. One capability is built and tested; the four jobs below are still mostly shape.

## The four jobs

- **Bootstrap.** Stand a new project up with the structure it should have had from the first commit.
- **Outfit.** Install the tooling every project is expected to carry — linting, tests, continuous integration, independent review, a backlog.
- **Inspect.** Check a project against the baseline and report where it falls short. Findings, exit codes, runnable in continuous integration.
- **Refit.** Return over time and confirm the latest learnings have actually been applied, not just published.

## What works today

**`luma-foreman policy`** — per-project control over what Claude Code is allowed to do, changed with a command instead of by editing a hook. Claude Code's own permission rules are global; this adds a per-project layer, so loosening a rule for one repository does not loosen it everywhere. See [docs/claude-permission-policy.md](docs/claude-permission-policy.md).

```bash
luma-foreman policy                 # what is allowed in this repository, and why
luma-foreman policy allow curl      # ...and change it, effective on the next tool call
```

Everything else prints "not built yet" and exits 2.

## Install

Requires `sh`, `jq`, and `awk`. No build step.

```bash
git clone https://github.com/LumaStack/luma-foreman.git
ln -s "$PWD/luma-foreman/bin/luma-foreman" ~/.local/bin/luma-foreman   # or add bin/ to PATH

luma-foreman policy install
```

`policy install` copies the permission gate into `~/.config/luma/foreman/` and then **prints** the two changes you need to make to `~/.claude/settings.json`. It does not edit that file: foreman writes freely into the directory it owns and never silently edits config you own. Re-run it after every upgrade — it is idempotent and says when there is nothing to do.

The only thing you have to change by hand is `~/.claude/settings.json`, and `policy install` shows you exactly what. Hook wiring needs a Claude Code restart to take effect; policy changes after that are live.

Run the tests with `sh tests/run`. They are hermetic — `HOME` and `LUMA_FOREMAN_HOME` are redirected into temp directories, so running them never touches your configuration.

It also carries **meta-skills**: skills whose job is to generate a project's own best-practice skills, so each repository ends up with tooling suited to it rather than a copied template.

The goal is projects that are homogeneous where homogeneity pays and optimal where it does not.

## The constraint that defines this repository

Three limits. They are easy to collapse into one another, and collapsing them is how this charter goes wrong — so they are named separately.

| | |
| --- | --- |
| **Dependency** | Foreman runs with no hq checkout, no network call, no organization secrets. |
| **Authority** | Foreman enforces standards; it does not decide them, and it does not accumulate knowledge across projects in order to. |
| **Existence** | hq is optional. Foreman has to be worth installing where no hq will ever exist. |

Dependency is the runtime limit and is elaborated below. Authority and Existence are about foreman's role, and are elaborated in [Relationship to luma-hq](#relationship-to-luma-hq).

Note what none of the three say: that foreman may hold no state. That is a different question, answered in [Where state lives](#where-state-lives).

**Foreman works one repository at a time, and needs nothing from the organization to do it.**

A check that needs to know what the organization learned last quarter in order to run is a broken check — the learning must be baked in as an executable rule before it ships here. That is why there is no [luma-hq](https://github.com/LumaStack/luma-hq) checkout and no call out to fetch standards.

Foreman knows hq can exist, and a rule may name the decision it came from. What it never does is *depend* on one. That is what makes foreman usable in a repository belonging to someone with no access to the rest of the organization, and in an organization that has no rest.

### What the constraint does not forbid

It forbids organization context as an **input**. It does not forbid foreman from keeping state as it works.

Foreman is boots on the ground: one operator, one workstation, many repositories, over and over. It has to record what this machine and this operator have decided, and those are local facts rather than organization knowledge. A foreman that cannot hold them only works for whoever's dotfiles it grew up in — which fails the same test the constraint exists to pass.

Two rules keep that honest:

- **Every capability has a correct default with no configuration present.** Configuration changes what foreman does for you. It never changes what the standard is.
- **Configuration carries local facts, never standards.** "This workstation may ssh to build01" is a local fact. "Projects must not leak personally identifiable information" is a standard, and standards ship as code.

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

## Relationship to luma-hq

Two of the three limits live here: **Existence** first, then **Authority**.

**hq is optional.** Many organizations will never have one, so foreman has to be worth installing on its own. What ships here is a complete and defensible standard, not a stub waiting for orders.

Where an hq does exist, the division is: luma-hq is where a standard is argued, decided, and justified, and where the organization's view across every project lives. luma-foreman is where a standard becomes executable and gets enforced, one repository at a time. Changes flow one way: hq settles, foreman ships.

Foreman does not do hq's job. It does not argue standards, and it does not accumulate knowledge across projects in order to decide something — the moment answering a question requires knowing about your *other* repositories, that question belonged to hq.

Bookkeeping is not that. Knowing which repositories this workstation has configured is local state; knowing what the organization owns is hq's.
