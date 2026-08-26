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
`show`. The old names survive as deprecated aliases.

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
| *nothing* | `bundle list`, `bundle show <name>`, `catalog list` |

**`adopt` and `outfit` remain as working aliases** that print a deprecation
notice. `bootstrap` gets none — it was never built, so nothing can depend on it.

**`install` is not the verb for taking a bundle.**

**Nouns are for reading an inventory; verbs stay flat.** `bundle` and `catalog`
group the two listing commands and nothing else. `get`, `apply`, `inspect` and
`outdated` remain top-level, because a noun group earns its place by
partitioning the command set rather than by being frequent — and bundles are the
product, not a subsystem. Prefixing every verb with `bundle` would add a word
everywhere and distinguish nothing.

**Each noun lists instances of itself.** `bundle list` lists bundles this
project holds; `catalog list` lists catalogs it draws from. `show` drills into
one of either. Nothing is named for a thing it does not return.

**Only `catalog show` needs a network.** The other three read committed state —
`adopted.toml` and `.luma/config/foreman.toml` — so they work in a bare clone.
The offline guarantee that `inspect` carries extends to every read command
except the one that reaches the far side.

## Why

**Discoverability is paid by every new user forever; the metaphor was paid once,
by the author.** That asymmetry decides it on its own.

**`install` is precluded by [[ADR-0002-adoption-copies-and-never-resolves]].** It
promises a resolver, a lockfile, an uninstall, and transitive fetching. Adoption
refuses all four by design, and the README already names the conflict — *"which
is what keeps this a copy rather than an install."* The nearest real analogue in
any ecosystem is `go get`, which is called `get`.

**`apply` names the contract that `outfit` left implicit.** Projection is
idempotent, re-runnable, and produces derived output that is safe to delete —
which is [[ADR-0001-projection-writes-adapters-not-copies]]. `apply` is the
terraform and kubectl reading of exactly that: make derived state match declared
state. It also survives being run repeatedly, which matters because `--check`
runs in continuous integration.

**Aliases rather than a clean break, because the catalog documents foreman and
ships on its own version.** `luma/luma-tools workflows/adopt-knowledge` prints
`luma-foreman adopt` and `luma-foreman outfit`. A project can adopt an older
`luma-tools` into a newer foreman at any time, so a stale command name in bundle
prose is a permanent condition rather than a transitional one. An agent reading
that prose must not hit a hard error.

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

**`setup` for projection.** Deferred: it collides with `init`, and it names a
one-time act. Projection runs after every `get` and in CI. Re-open never on
these grounds; the objection is structural.

**`mount`, `bind`, `link`, `attach`, `connect`.** Deferred as a family. Each
implies a live relationship maintained over time, and the projection is
generated files — edit `.luma/` and the output is silently stale until re-run.
Re-open if projection ever becomes live rather than generated.

**`reapply` for the projection re-run.** Deferred permanently in
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
- Two aliases to carry, and no decided date for dropping them.
- The rename is not complete until `luma-catalog` ships updated bundle prose,
  which is a second repository on its own release cadence.
- `get` feeds the package-manager mental model that
  [[ADR-0002-adoption-copies-and-never-resolves]] exists to fight. The
  documentation carries that correction now, not the verb.

## Standing consequences

**The generated header is source, not content.** `Regenerate with luma-foreman
outfit` is emitted by the projection code, so it changes in `outfit.py` and then
by regeneration — never by editing `.claude/skills/`.

**Renaming a command is now a two-repository change.** Any bundle that documents
foreman has to be updated, versioned and published in `luma-catalog`, then
re-adopted. Follow `publish-to-the-catalog`.

**Deprecated aliases need a removal condition before they accumulate.** None is
set here deliberately — the condition depends on how long stale bundle prose
stays in circulation, which nothing has measured yet.

**Catalogs need a short name, and do not have one.** `catalog show` takes an
argument, and today a catalog is identified by a URL or a path. Derive a short
name from the last path segment and accept the full source string too. This is
the first real pressure toward registering catalogs rather than deriving them,
and it should be recorded as such when it arrives rather than solved by
accident.

**Only `catalog show` may reach the network.** `bundle list`, `bundle show` and
`catalog list` read committed state, and the guarantee is the one `inspect`
carries: a check that cannot run is reported as skipped, never as a pass. A
version-available column on `bundle list` would quietly break it — that
comparison belongs to `outdated`.

## References

The vocabulary change from *jobs* to *commands* shipped ahead of the rest, in
`Subcommands are commands, not jobs`. `docs/scope.md` carries the argument that
the original command set was defined by knowledge the catalog has since taken.
