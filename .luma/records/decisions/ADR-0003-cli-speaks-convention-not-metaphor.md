---
type: decision
title: The CLI speaks command-line convention, not the foreman metaphor
decided: 2026-08-26
lifecycle_status: provisional
reopen_trigger: Bundles declare dependencies and foreman resolves them — the re-open condition of ADR-0002. At that point `install` stops being a lie and the verb is worth revisiting.
---

# ADR-0003: The CLI speaks command-line convention, not the foreman metaphor

## Summary

Commands are named the way other command-line tools name them. The word for a
subcommand is **command**. The verbs are `get`, `apply`, `init` — not `adopt`,
`outfit`, `bootstrap`. Reading an inventory happens under a noun — `bundle` for
what this project has, `catalog` for where it came from — each with `list` and
`show`. Every rename is a clean break — the old names stop working.

## Problem

The tool is named for a role, and the metaphor extended into the command set: a
foreman has *jobs*, *outfits* a crew, and *refits* it later. Every one of those
reads well in the README and none of them is guessable at a prompt. Nobody's
first attempt is `adopt` — they type `install`, `add`, or `get`.

The metaphor also stopped carrying meaning without help. `outfit` never appeared
in the documentation without a gloss beside it: *"wire up"* in the command list,
*"projects them at agents"* in the pitch, *"Project adopted bundles into…"* in
its own help text. A verb that always travels with a translation is not doing
the work.

`jobs` had a sharper problem: the word is taken. In a shell it means a
background process; in continuous integration it means a unit of a pipeline.
Neither is what `luma-foreman inspect` is.

## Decision

**A subcommand is a command.** Usage, headers and error messages say so.

| was | is |
| --- | --- |
| `bootstrap` | `init` |
| `outfit` | `apply` |
| `adopt` | `get` |
| `adopt --list` | `catalog show <name>` |
| `outdated` | `bundle outdated` |
| *nothing* | `bundle list`, `bundle show <name>`, `catalog list` |

**Every rename is a clean break.** No aliases, no deprecation period. The old
names stop working the day the new ones land.

**`install` is not the verb for taking a bundle.**

**Nouns are for reading; verbs stay flat.** `get`, `apply` and `inspect` remain
top-level because they act on the project. `bundle` and `catalog` hold the
commands that only report — `list`, `show`, and `outdated`.

**Each noun lists instances of itself.** `bundle list` lists bundles this
project holds; `catalog list` lists catalogs it draws from. `show` drills into
one of either. Nothing is named for a thing it does not return.

**Two of the five need a network: `bundle outdated` and `catalog show`.** Both
ask about the far side. The other three read committed state — `adopted.toml`
and `.luma/config/foreman.toml` — so they work in a bare clone, which extends
the guarantee `inspect` carries to every read command that can honour it.

## Why

**Discoverability is paid by every new user forever; the metaphor was paid once,
by the author.** That asymmetry decides it on its own.

**`install` is precluded by [[ADR-0002-adoption-copies-and-never-resolves]].** It
promises a resolver, a lockfile, an uninstall, and transitive fetching. Adoption
refuses all four by design, and the README already names the conflict — *"which
is what keeps this a copy rather than an install."* The nearest real analogue in
any ecosystem is `go get`, which is called `get`.

**`apply` names the contract that `outfit` left implicit.** Applying is
idempotent, re-runnable, and produces derived output that is safe to delete —
which is [[ADR-0001-apply-writes-adapters-not-copies]]. `apply` is the
terraform and kubectl reading of exactly that: make derived state match declared
state. It also survives being run repeatedly, which matters because `--check`
runs in continuous integration.

**A clean break rather than aliases, because an alias would let the catalog stay
wrong.** `luma/luma-tools workflows/adopt-knowledge` prints `luma-foreman adopt`
and `luma-foreman outfit`, and the only real fix is to update that bundle and
republish it. An alias makes the stale prose keep working, which removes the
pressure to ever correct it — and leaves two names for one command with no
condition under which either dies. A hard error naming the new command teaches
the rename once; an alias defers it indefinitely.

**`bundle outdated` because it reports rather than acts.** It answers a question
about bundles and changes nothing, which is what the nouns are for. Leaving it
top-level would have made it the only bare word in the set that is a state
rather than an action.

**`catalog show` rather than `get --list`.** Browsing what a catalog offers was
never an adoption operation; it was filed under the adoption verb because that
was the command that already knew how to reach a catalog. Under `get` the
misfiling becomes visible — `get --list` reads as a query and is not one.

**A flag may change how much or how, never what comes back.** `adopt --list`
returns catalog contents from an adoption command; `catalog <name> --bundles`
and `catalog list --remote` would return bundles from a command that lists
catalogs. All three are the same mistake, and it is the one this record exists
to correct. When the answer is a different kind of thing, it is a different
command.

**`bundle list` closes the gap that started this.** Nothing listed what a
project had adopted. `outdated` came closest but required a network and framed
the answer as a version comparison; `apply --explain` counted bundles without
naming them; `inspect --rule adoption` only spoke on failure. The inventory
lived in `adopted.toml` with no command over it, and the command whose name
sounded right — `adopt --list` — returned the catalog's contents instead.

**The set of catalogs is derived, not registered.** A catalog is an argument and
a config default, not a tracked entity, so `catalog list` has nothing to read
but the distinct `source` values in `adopted.toml` plus the configured default —
which is already how `outdated` decides where to look. That is enough to answer
*where does my knowledge come from*, including the org-private-plus-universal
case, before anything builds catalog registration.

## Alternatives

Each is deferred rather than rejected; the trigger is what would make it right.

**`install` / `bundle install`.** Re-open with this record's trigger — if
bundles ever declare dependencies and foreman resolves them, the word stops
overpromising.

**`fetch`.** Deferred: for a git-adjacent audience `fetch` means *download
without applying*, and this operation applies — it lands the copy and the copy
gets committed. Re-open if a two-step retrieve-then-land flow ever exists, which
would give `fetch` something true to name.

**`setup` for what `apply` does.** Deferred: it collides with `init`, and it
names a one-time act. `apply` runs after every `get` and in CI. Re-open never on
these grounds; the objection is structural.

**`mount`, `bind`, `link`, `attach`, `connect`.** Deferred as a family. Each
implies a live relationship maintained over time, and what `apply` writes is
generated files — edit `.luma/` and the output is silently stale until re-run.
Re-open if the output ever becomes live rather than generated.

**`reapply` for re-running `apply`.** Deferred permanently in
[[ADR-0004-refit-is-removed-not-renamed]]: `apply` is idempotent, so `reapply`
names something `apply` already does.

**Noun-first grouping for the verbs too — `bundle get`, `bundle outdated`.**
Deferred, and the closest call here. It is more internally consistent than what
was chosen, at the cost of demoting the most-run command to two words. Re-open
when bundle operations exceed roughly four and form something with its own
shape; at that point `get` should survive as a top-level alias the way `git
pull` does.

**`catalog bundles` for the drill-down.** Deferred: unambiguous, and it reads as
*all bundles across all catalogs* rather than one catalog's contents. Re-open if
the merged cross-catalog view turns out to be what people actually want, at
which point it sits alongside `catalog show` rather than replacing it.

**`catalog <name> --bundles` and `catalog list --remote`.** Deferred and
unlikely: both select the subject matter with a flag, and neither can say which
catalog without an argument that makes it `catalog show` in longer form.

**`catalog remote <name>` instead of `catalog show <name>`.** Deferred: it has
no verb in it, so it reads as a subtype and implies a `catalog local` beside it.
It would also assert that catalogs are remote, and `--from` accepts a local
checkout — which is the normal case when developing a catalog.

## Tradeoffs

**Pros**
- Every verb is a first guess. None needs a gloss.
- `init` and `apply` are a recognised pair, and `apply --check` reads correctly
  in a CI gate.
- The two levels of the CLI now agree: `agent-permissions` already answered an
  unknown verb with *unknown command*.

**Cons**
- A window where `luma-catalog` still documents the old names and an agent
  following that prose hits an error. Closing it means shipping the catalog
  update promptly rather than eventually.
- Anyone with the old names in a script or in muscle memory gets a failure
  rather than a warning.
- `get` feeds the package-manager mental model that
  [[ADR-0002-adoption-copies-and-never-resolves]] exists to fight. The
  documentation carries that correction now, not the verb.

## Standing consequences

**The generated header is source, not content.** `Regenerate with luma-foreman
outfit` is emitted by the code behind `apply`, so it changes in `outfit.py` and then
by regeneration — never by editing `.claude/skills/`.

**Renaming a command is now a two-repository change.** Any bundle that documents
foreman has to be updated, versioned and published in `luma-catalog`, then
re-adopted. Follow `publish-to-the-catalog`.

**The unknown-command message has to carry the rename.** With no aliases it is
the only thing standing between someone typing `adopt` and a bare failure, so it
names the replacement: `unknown command: adopt (renamed to: get)`.

**The catalog update is not optional follow-up work.** It is what closes the
window this decision opens, and it should ship immediately after the rename
rather than whenever convenient.

**Catalogs need a short name, and do not have one.** `catalog show` takes an
argument, and today a catalog is identified by a URL or a path. Derive a short
name from the last path segment and accept the full source string too. This is
the first real pressure toward registering catalogs rather than deriving them,
and it should be recorded as such when it arrives rather than solved by
accident.

**Two commands may reach the network and no others: `bundle outdated` and
`catalog show`.** Both answer a question about the far side, and neither has an
offline answer worth giving. `bundle list`, `bundle show` and `catalog list`
read committed state, so the guarantee `inspect` carries extends to them: a
check that cannot run is reported as skipped, never as a pass.

**A version-available column on `bundle list` would quietly break that**, which
is the tempting change to refuse. It reads as a small convenience and it moves
the command across the line — the comparison belongs to `bundle outdated`,
which is named for needing a network.

## References

The vocabulary change from *jobs* to *commands* shipped ahead of the rest, in
`Subcommands are commands, not jobs`. `docs/scope.md` carries the argument that
the original command set was defined by knowledge the catalog has since taken.
