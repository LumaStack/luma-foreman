---
type: luma/idea
title: adopt or install as shorthand for get plus apply
created: { by: human:benlinton, at: 2026-08-26T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
lifecycle_status: draft
---

# `adopt` or `install` as shorthand for `get` plus `apply`

Taking a bundle is two commands, and it is two commands **on purpose**: `get`
copies a directory and writes a receipt, `apply` writes what agents read, and
the gap between them is the `unapplied` finding — a bundle present,
checksummed, reported clean, and seen by nobody.

**Nearly every real use runs both.** `bundle outdated` prints them as a pair,
`get` ends by telling you to run `apply`, and the catalog's `adopt-knowledge`
workflow shows them together. A single command for the common path is the
obvious convenience.

Two names are candidates and **neither is settled**.

## `adopt`

**It is already the name of the operation.** `adopted.toml`, `inspect --rule
adoption`, ADR-0002's title. A command called `adopt` that performs adoption
completely is the one reading that needs no explanation.

**And the reason it was wrong for `get` is the reason it fits here.** ADR-0003
rejects it as a name for `get` because it *sounds like taking something in,
which reasonably includes wiring it up* — and `get` wires nothing up. That
overpromise is an accurate description of two commands.

**Against:** the word was just retired from the command surface, and bringing it
back means `luma-foreman adopt` goes from an error naming its replacement to a
working command that does something broader than what it used to. Anybody who
learned the rename learned it wrong.

## `install`

**It is what the rest of the world calls exactly this.** `npm install` fetches
a package *and* puts it where the runtime will find it. That is `get` plus
`apply`, precisely — arguably a closer fit than `adopt`, which describes taking
ownership rather than making something usable.

**Against:** ADR-0002 rules it out for adoption because it promises a resolver,
a lockfile, an uninstall and transitive fetching, and a compound command
inherits every one of those expectations. The bundle model has none of them.

**And it summons `uninstall`.** Nobody expects `unadopt`; everybody expects
`uninstall`. Removing a bundle — delete the copy, drop the receipt, re-apply —
is a real operation nothing has built, and picking `install` creates the
pressure to build it before anybody decided it should exist.

## What decides it

**Whether the compound is *finishing adoption* or *making a thing usable*.**
Those are the same action and different framings, and the name should follow
whichever the project believes. `adopt` says the unit of work is a bundle
becoming this project's own. `install` says the unit of work is knowledge
becoming available to an agent.

**Whether reversing a rename costs more than the better word is worth.** `adopt`
was an error message hours ago. `install` never was.

## What has to be decided either way

**What it does when the second half fails.** `get` succeeded and `apply` did not
is a real state, and the compound has to leave the project somewhere describable
rather than half-done under one exit code.

**Whether it hides the thing the split exists to teach.** The two-command shape
is how anybody learns that adoption does not reach an agent by itself. A
shorthand that always works makes `unapplied` a finding nobody understands when
they finally hit it from some other route.

**Whether it takes `--to`, `--force`, `--from` and `--check`**, or refuses
options and stays the trivial path. A compound accepting every flag of both
halves is two commands with extra steps.

## Notes

Raised 2026-08-26, immediately after settling that `get` keeps its name. Not
urgent: two commands work, and the pair is printed everywhere it matters.
