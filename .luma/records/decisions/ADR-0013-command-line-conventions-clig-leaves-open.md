---
type: decision
title: Command line conventions CLIG leaves open
decided: 2026-09-03
stage: draft
reopen_trigger: A fourth failure mode is worth distinguishing at the exit code, or a noun acquires a verb so obviously default that printing a menu instead reads as the tool being unhelpful rather than being careful.
---

# ADR-0013: Command line conventions CLIG leaves open

The [Command Line Interface Guidelines](https://clig.dev) decide this
project's command line, by way of the `local/command-line-interface` bundle.
CLIG deliberately leaves some choices open. This is the list of what this
project settles in those gaps, and nothing else belongs here.

**There are no departures.** Every entry below answers a question CLIG
declines to answer, not one it answers differently. That is worth stating
because the bundle requires a divergence to be recorded with its reasoning,
so an empty set is itself the claim: anything in this project's command line
that disagrees with CLIG is a defect rather than a choice.

## Problem

Some conventions were being re-derived per command, and re-derived
differently each time. They existed only in the shape of code and in commit
messages, which meant every new verb re-opened questions somebody had already
answered — what a bare noun does, whether an idempotent no-op is an error,
how much a refusal has to say.

The bundle that adopts CLIG says the way to make something outrank it is to
decide the thing deliberately and write it down, **not to do it twice**. Doing
it twice is exactly what had happened.

## Decision

**Three exit codes, and every command's help states its own.**

| | |
| --- | --- |
| `0` | fine, including an idempotent no-op |
| `1` | refused, or something is wrong |
| `2` | could not run |

CLIG requires zero for success and says to map non-zero codes to failure
modes worth distinguishing; which codes, and how many, is ours. The split
that earns the third code is *the tool declined* versus *the tool could not
try* — a refusal is an answer, and a reader who conflates the two cannot tell
a working tool from a broken one.

**A bare noun prints its menu and exits 0**, at every level:
`luma-foreman`, `luma-foreman bundle`, `luma-foreman catalog`,
`luma-foreman agent-permissions`. Not an error — somebody asking what is here
should not get a non-zero status.

CLIG says bare `myapp` shows full help, and for a git-like tool it names
`myapp help`, `myapp help subcommand` and `myapp subcommand --help`. It does
not say what bare `myapp subcommand` does. This extends the rule it does
state to the level it does not: a noun behaves like the program.

**An error message contains the command to run.** Not a description of what
to type, and not a syntax to work out — the literal line, ready to copy.
Where the right command depends on what the project holds, the code reads
that and prints the real thing:

```
luma-foreman get: bundle-manager is not a bundle ID — a bundle is addressed
<namespace>/<name>, and the namespace is the catalog's.
  From a catalog registered here:
    luma-foreman get lumastack/luma-catalog/bundle-manager
```

That last line is generated from the catalogs actually registered in this
project. The alternative — *"pass a fully qualified bundle ID"* — is true,
and leaves the reader to find out which catalogs exist and reassemble the
command themselves.

CLIG says to suggest corrections and to ask before acting on one. It does not
say the suggestion has to be executable, which is the part that turns a
refusal into an answer.

**Never overwrite the file that makes a thing what it is.** A `BUNDLE.md` is
what makes a directory a bundle, so replacing it discards the bundle rather
than the file. A command that would land on one adds what is missing and
leaves what is there — `init`'s contract — which also means a second run is
never an error.

**Say which case it was.** Where a command reaches the same end state by
different routes — created from nothing, written onto existing work, already
done — the output names the route. The routes fail differently later, so a
reader needs to know which one they are in.

## Why

**These are the choices CLIG declines to make, and a project that has not
made them answers them differently every time.** That is not a criticism of
the guide: which exit codes mean what is properly local, and a guide that
fixed it would be wrong somewhere.

**Recording them is what makes them binding.** The bundle's own rule is that
precedent is not a decision — what a program already does carries no
authority. Every convention here was established practice before it was
written down, which under that rule meant none of it bound anything. The
gap this closes is not knowledge, it is standing.

**What is deliberately absent is as much of the decision as what is here.**
Anything CLIG settles stays out, however much this project relies on it:
`noun verb` ordering, ordering menus by usage frequency, and `-h`/`--help`
being answered whatever else was typed are all followed here and none of
them is recorded, because following a guide needs no record. A list that
restated the guide would need maintaining against it, and would eventually
disagree with it silently.

## Alternatives

**Two exit codes.** Deferred: it is what CLIG's letter requires, and it is
what most tools do. Re-open if the refused/could-not-run split turns out
never to change what a caller does — the third code earns its place only
while somebody acts on the difference.

**A bare noun runs `list`.** Rejected as the shape a noun outgrows: `bundle`
had three reporting verbs when defaulting to `list` was a fair guess and now
has seven, four of which write. A default verb gets more arbitrary with every
verb added, and the arbitrariness is invisible until somebody is surprised
by it. The re-open trigger above is the case that would change this back.

**Recording these in the bundle instead.** Rejected: the bundle is written to
be promoted, and conventions specific to this project would make it
un-adoptable by anyone else. The bundle points at CLIG and states the
precedence rule; the local answers live here, which is the division it asks
for.

## Standing consequences

**A new noun inherits all of this** — bare invocation prints its menu, and
its help states its exit codes. It inherits CLIG's rules the same way, which
this record does not restate.

**A command that can no-op must exit 0 and say so.** *Nothing to do* is a
successful outcome, and reporting it as a failure makes every wrapper script
treat a settled state as a problem.

**A refusal that cannot name a concrete fix is a refusal that has not
finished being written.** Where project state would make the message
concrete, read it.

## References

The guidelines themselves are adopted by
`.luma/bundles/local/command-line-interface/`, whose policy carries the
precedence rule this record depends on: a decision in force outranks CLIG,
precedent outranks nothing.

Landed as: `#131` and `#132` (an error message contains the command to run),
`#134` and `#136` (never overwrite the identity file; say which case it was),
`#135` (the bare noun). The exit code trio predates all of them and is cited
by [[ADR-0012-catalogs-are-registered-sources]] without ever having been
decided.
