# Architecture

**The invariants, and where state lives.** Read before adding a capability —
each rule below is one a newcomer would break without noticing, and two of them
are the reason foreman is a separate tool at all.

## Foreman can always run on its own

**luma-leader is optional.** When one exists, foreman may use it and may be
better for it. When one does not, nothing foreman does stops working.

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

**If a check ever needs organization context in order to run, the boundary has
been broken** — that is the test, and it is worth failing loudly rather than
quietly special-casing.

## Foreman does not accumulate knowledge across projects

That is an hq's job. **The moment answering a question requires knowing about
your *other* repositories, the question belonged to hq.**

Bookkeeping is not that. Knowing which repositories this workstation has
configured is local state; knowing what the organization owns is not.

**Knowledge still travels both ways.** Plenty of it starts in one project and
outgrows it, and foreman should make promoting it upward easy. Foreman is where
knowledge can originate and always where it lands; an hq is what carries it
between projects.

## It writes freely into what it owns, never into what the operator owns

Its own directories are fair game. Changes to files the operator owns —
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

Paths follow XDG — see [Standards](standards.md).

## Which commands run where

**`inspect` must survive a bare environment** — fresh clone, no configuration, no
organization access, exit codes, continuous integration. It is the one that has
to hold the line.

**`init` and `apply` are workstation operations.** They change a repository, they
expect an operator, and they may use workstation state to do it. Requiring them
to run in continuous integration was never the point and would buy nothing.

## How adoption stays a copy

**`get` is a directory copy with a receipt.** The bundle lands in
`.luma/bundles/<org>/<name>/`, and `adopted.toml` records the version, where it
came from, the catalog commit, and a checksum of exactly what landed.

**Nothing resolves and nothing is fetched later.** Bundles depend on nothing,
which is what keeps this a copy rather than an install — and what lets a fresh
clone with no network reproduce the project exactly.

An edited copy is never silently overwritten, and a bundle with no version
cannot be adopted at all.

## How apply reaches an agent

**`apply` writes thin adapters, never copies.** Each workflow becomes a skill
pointing at the real document under `.luma/`, naming the standing context that
document assumes.

A managed block in `CLAUDE.md` indexes everything adopted: a document declaring
`matches: always` is imported so its body arrives, and everything else
contributes one line saying what it is and what surfaces it.

**Only the region between the `luma:begin` and `luma:end` markers is touched**, so
a hand-written file keeps the rest. Everything `apply` writes is generated and
disposable — commit it or gitignore it, but regenerate rather than edit.

## Agent permissions share none of this

**`agent-permissions` is unrelated to adoption.** It shares no machinery with
bundles and would function identically if they had never existed.

It is in the same binary because it is the same operator working on the same
repository — not because the two are one system. See
[Agent permissions](claude-agent-permissions.md).
