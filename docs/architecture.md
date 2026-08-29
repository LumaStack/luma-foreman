# Architecture

**The invariants, and where state lives.** Read before adding a capability —
each rule below is one a newcomer would break without noticing, and two of them
are the reason foreman is a separate tool at all.

## Foreman can always run on its own

**Other luma tools (including luma-leader) are optional.** When one exists, foreman may 
use it and may be better for it. When one does not, nothing foreman does stops working.

**That is a guarantee, not a ban.** Consulting an hq is allowed and may well be
worth doing; *requiring* it is not. Every capability gets the same question —
does this still work with no hq? — and some things honestly cannot exist without
one. *"How does this project compare to the other forty?"* is not answerable from
inside one repository, and pretending otherwise would be a lie.

**What the guarantee protects is that the jobs foreman already does keep
working.**

## Foreman enforces standards; it does not decide them

A rule compiled in here is a rule nobody agreed to. Standards are argued and
settled elsewhere and travel here as executable checks.

**Where a standard came from does not matter.** One may start in a single
project, be promoted to an organization, and come back to twenty others — or
start in a project and stay there for good, never worth sharing. Both arrive the
same way: vendored, committed, readable with no network required to run.

**What breaks the boundary is a check that cannot run without reaching outside
the repository.** Origin is not the test; runtime dependency is. A rule that has
to ask an organization something at the moment it runs has stopped being
executable here, and is worth failing loudly.

## Foreman does not accumulate knowledge across projects

That is luma-leader + hq's job. **The moment answering a question requires knowing about
your *organization*, the question belonged to hq.**

**Knowledge still travels both ways.** Plenty of it starts in one project and
outgrows it, and foreman should make promoting it upward easy. Foreman is where
knowledge can originate and always where it lands; an hq is what carries it
between projects.

## Foreman writes freely into what it owns, never into what the operator owns

Foreman's own directories are fair game. Changes to files the operator owns —
`~/.claude/settings.json` above all — are **printed for a person to apply**.

## Where state lives

| scope | holds | committed |
| --- | --- | --- |
| shipped | the standards, as executable rules | yes, in this repository |
| project | decisions about a project that its whole team shares | yes, in the target repository |
| workstation | who this operator is, what this machine trusts | no |
| workstation, per project | this operator's decisions about one repository | no |

**The last row is the awkward one and it earns its place.** Some per-project
decisions must not be committed: what an agent is permitted to do inside a
repository is the operator's call on their own machine, not a property of the
repository that every clone should inherit.

Paths follow XDG, nested `~/.config/<org>/<application>/` — see
[`where-configuration-lives`](../.luma/bundles/lumastack/luma-catalog/luma-config/policy/where-configuration-lives.md)
in the adopted `luma-config` bundle, which is where that rule is decided.

## Which commands run where

**`inspect` must survive a bare environment** — fresh clone, no configuration, no
organization access, exit codes, continuous integration. It is the one that has
to hold the line.

**`init` and `apply` are workstation operations.** They change a repository, they
expect an operator, and they may use workstation state to do it. Requiring them
to run in continuous integration was never the point and would buy nothing.

## How adoption stays a copy

**`get` fetches once and records what arrived.** The bundle lands in
`.luma/bundles/<org>/<name>/`, and `adopted.toml` records the version, where it
came from, the catalog commit, and a checksum of exactly what landed.

**Nothing is fetched later.** That is what keeps this a copy rather than an
install, and what lets a fresh clone with no network reproduce the project
exactly.

**A bundle with no version cannot be adopted at all**, because a project holding
one could say nothing honest about what it has.

## How apply reaches an agent

**`apply` writes thin adapters for each harness, never copies.** A workflow
becomes whatever that harness invokes — for Claude Code, a skill — saying which
document to read, which bundle it came from, and where that bundle is vendored.
It carries no copy, because a copy would drift.

**Nothing an agent reads carries the knowledge itself.** Three levels, each
pointing at the next:

| | holds |
| --- | --- |
| the harness adapter — for Claude Code, a managed block in `CLAUDE.md` | *read the entry point*, and an import of it. No knowledge of its own |
| `.luma/bundles/entrypoint.md` | one line per **bundle**, each pointing at that bundle's ring |
| a **ring** | one line per document in that bundle, each with what surfaces it |

**A ring is how an agent decides what to open — not what to know.** For one
bundle it gives the version and what the bundle is for, where to start reading,
where the bundle is vendored, and then every document it holds: the document's
id, its type, one line on what it says, and **the trigger that brings it into
play** — a path, a topic, a command.

**So an agent never reads a bundle whole.** It matches the work in front of it
against the triggers and opens one document. The ring is the only part it reads
speculatively, and it is deliberately small enough to.

**A ring also says what does not arrive through it.** A bundle's workflows reach
a harness as things it can invoke directly, so the ring names them and sends the
reader to invoke them by name rather than to read them here.

**The entry point and the rings are written once and are harness-neutral.** Only
the adapter is per-harness, and its whole job is to get the entry point read.

**Only the region between the `luma:begin` and `luma:end` markers is touched**, so
a hand-written file keeps the rest. Everything `apply` writes is generated and
disposable — commit it or gitignore it, but regenerate rather than edit.

## Agent permissions share none of this

**`agent-permissions` is unrelated to adoption.** It shares no machinery with
bundles and would function identically if they had never existed.

It is in the same binary because it is the same operator working on the same
repository — not because the two are one system. See
[Agent permissions](claude-agent-permissions.md).

## A regex that stops matching a command name fails open

`agent_permissions/match.py` carries `CLI_WRITE` and `CLI_INVOCATION`, which
recognise a `luma-foreman agent-permissions` invocation **in order to gate it**.
Rename or restructure that command and the patterns stop matching — silently,
and in the permissive direction. **The subsystem exists to prevent exactly
that.**

**Write the gating test before the change, so it fails first.** Anything that
reads a command's own name to decide whether to gate it is in this category, and
the failure never announces itself.

The same shape applies to the config file: a `policy.toml` left by an older name
is still read when `permissions.toml` is absent, because a permission file that
quietly stops being read fails open too.
