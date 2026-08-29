---
type: decision
title: refit is removed rather than renamed, and there is no composite status command
decided: 2026-08-26
lifecycle: draft
reopen_trigger: Somebody needs a single answer to "am I current" and the three existing commands are genuinely too many. The record that re-opens this has to say what such a command can honestly report with no network.
---

# ADR-0004: refit is removed rather than renamed, and there is no composite status command


**Returned to `draft` on 2026-08-26.** This was recorded as settled while the argument was still running, and several positions in it moved the same day. `provisional` means decided and in force; this was neither, and saying so was the error rather than the changes that followed.
## Summary

`refit` is deleted from the command set. It is not renamed to `reapply`, and it
is not replaced by a composite `status`. What it promised is already built,
split across three commands, and the split is load-bearing.

## Problem

`refit` was never implemented — it printed *not built yet* and exited 2. It
survived as a name because it paired with `outfit`: a foreman outfits a crew and
refits it later.

[[ADR-0003-cli-speaks-convention-not-metaphor]] renames `outfit` to `apply`,
which orphans it. The obvious substitution makes things worse: `apply` is
idempotent, so `reapply` names something `apply` already does, and the first
question anyone asks is what the difference is. There is no answer.

## Decision

**Remove `refit`.** No `reapply`. No composite `status`.

**The three commands that cover it stay separate:**

| | answers | needs network |
| --- | --- | --- |
| `bundle outdated` | has a newer version been published? | yes |
| `inspect --rule adoption` | is the copy still what was adopted, and was it applied? | no |
| `apply --check` | is what was written stale against the bundles? | no |

## Why

**Its knowledge moved to the catalog, and only the name stayed.** `refit` was
defined by *knowing the latest learnings* — and knowing things is what the
catalog took. What remained was mechanics, and the mechanics got built under
other names. This is not a capability being dropped; it is a name that outlived
the argument for it.

**The offline/online split is deliberate and a composite would cross it.**
`bundle outdated` exists as its own command rather than a flag on `inspect`
precisely because it needs a network, and `inspect` must survive a bare clone with no
configuration. A single command answering all three questions either requires a
network — breaking that guarantee — or degrades silently when it has none. The
project already names the second outcome as the worse one: *an inspection that
reads clean while silently skipping half its checks is worse than no
inspection.*

**Its own description never settled what it was.** The README calls it
*"confirm the latest learnings have actually been applied"* — read-only — and
also files it among the commands that *"change a repository."* A command that
was never built and was described two incompatible ways is not a specification.

**A stub advertises a promise.** `refit` has appeared in `--help` since before
the catalog existed. Removing it costs nothing, because nothing can depend on a
command that has only ever exited 2.

## Alternatives

**`reapply`.** Deferred, and hard to see re-opening: it would require `apply` to
stop being idempotent, which is
[[ADR-0001-apply-writes-adapters-not-copies]] reversed.

**A composite `status`.** Deferred, and the likeliest to return. Re-open when
running three commands is genuinely the friction rather than a theoretical one.
The record that re-opens it must answer the question this one refuses to dodge:
what does it report when there is no network? Naming a version column *unknown*
is honest; omitting it silently is the failure mode above.

**Keep `refit` unbuilt under its current name.** Deferred: costs nothing today
and keeps a name that no longer matches any sibling. Re-open never on these
grounds — the metaphor it belonged to is gone.

**Fold it into `inspect` as a fourth rule.** Deferred, and closer to right than
it looks: two of the three questions are already offline. Blocked only by the
version comparison, which cannot be. Re-open if the version check ever becomes
answerable from committed state alone.

## Tradeoffs

**Pros**
- Nothing in the usage string advertises a command that has never existed.
- The offline guarantee stays legible: which commands need a network is visible
  from the command list rather than from reading help text.

**Cons**
- Three commands to answer one plain question — *am I current?* — and no single
  place that says so.
- Someone will propose `status` again, and this record is the only thing that
  will tell them why it was not built the first time.

## Standing consequences

`UNBUILT` in the dispatcher holds `init` alone until that is built, after which
it goes away with the branch that reads it.
