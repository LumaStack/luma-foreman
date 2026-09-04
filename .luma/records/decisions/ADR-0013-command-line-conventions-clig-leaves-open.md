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
CLIG deliberately leaves some choices open and this project departs from it
in one place. This is that list, and nothing else belongs here.

## Problem

Seven conventions were being re-derived per command, and re-derived
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

**`--help` is handled before verb dispatch.** What a bare noun resolves to
can never reach it. This is what keeps the previous decision cheap to revisit:
it is one word in each module, and the explicit route is structurally
untouched by it.

**Menus list reads before writes.** This is the one **departure** from CLIG,
which says to order by usage frequency. Frequency is unmeasured here and
would be guessed; kind is observable from the code, and the ordering it
produces puts the commands that cannot damage anything where a reader lands
first.

**A refusal names the fix as something to copy.** Not a syntax to
reconstruct — where the fix depends on project state, the message reads that
state and prints the real command:

```
luma-foreman get: bundle-manager is not a bundle ID — a bundle is addressed
<namespace>/<name>, and the namespace is the catalog's.
  From a catalog registered here:
    luma-foreman get lumastack/luma-catalog/bundle-manager
```

CLIG says to suggest corrections and to ask before acting on them. Reading
project state to make the suggestion concrete goes further, and it is the
half that turns a refusal into an answer.

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
the guide: exit code meanings and menu ordering are properly local, and a
guide that fixed them would be wrong somewhere.

**Recording them is what makes them binding.** The bundle's own rule is that
precedent is not a decision — what a program already does carries no
authority. Every convention here was established practice before it was
written down, which under that rule meant none of it bound anything. The
gap this closes is not knowledge, it is standing.

**The departure is the load-bearing entry.** The bundle requires that a
divergence from CLIG be written down with its reasoning, because a convention
broken on purpose and one broken by accident are identical in the code. Menu
ordering by kind is the only place this project currently diverges, and
without this record a later reader would have no way to tell which it was.

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

**Ordering menus by frequency, as CLIG says.** Deferred rather than
rejected — it is the better rule the moment frequency is *measured*. Nothing
here measures it, and a guessed frequency ordering is a worse version of the
same guess with none of the honesty.

**Recording these in the bundle instead.** Rejected: the bundle is written to
be promoted, and conventions specific to this project would make it
un-adoptable by anyone else. The bundle points at CLIG and states the
precedence rule; the local answers live here, which is the division it asks
for.

## Standing consequences

**A new noun inherits all of this** — bare invocation prints its menu,
`--help` is parsed before its verbs, its menu lists reads first, and its help
states its exit codes.

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

Landed as: `#131` and `#132` (refusals name a copyable command), `#134` and
`#136` (never overwrite the identity file; say which case it was), `#135`
(the bare noun, `--help` before dispatch, reads before writes). The exit code
trio predates all of them and is cited by
[[ADR-0012-catalogs-are-registered-sources]] without ever having been
decided.
