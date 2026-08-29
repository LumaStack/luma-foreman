---
type: slice
title: The standards document, and the paths it was wrong about
created: 2026-08-29
covers:
  - docs/standards.md
contributors:
  - human:benlinton
  - agent:claude-opus-5
---

# 003: standards

## What this is

**One file, and the cluster's other document deferred.** `docs/standards.md`
turned out to be superseded by an adopted bundle, and checking that produced
three code defects. That is a slice's worth on its own;
`docs/claude-agent-permissions.md` moves to 004.

## What we made of it

**It was a subset of `luma-config/policy/where-configuration-lives.md`**, which
this project has adopted. Same arguments, tighter, with the XDG specification
and the direnv changelog cited as `sources`. **Every section had a destination
already written and better.**

**`:3` said it was a stop-gap** *"until we have a proper standards system +
ecosystem."* That system exists, this repository adopted it, and the file went
on describing itself as the thing standing in for it.

### The reversal note turned out not to be at risk

`:58-63` recorded that an earlier version argued for flat paths, and named the
two grounds that did not survive. It looked like the one thing a deletion would
lose. **`CHANGELOG.md:92-93` already carries it, in more detail** — so no
decision record was needed and nothing was preserved on the way out.

**Worth stating because the opposite was assumed for most of the slice.** The
check that settled it was a grep, not a judgement.

### Checking it against the code found three defects

**The table in the bundle was the cause of all three.** It gave
`~/.config/<application>/` with no organization segment, and put the nesting
rule in a subsection below it. **A table is what a reader takes as canonical**,
so three real paths were written without the segment:

| | |
| --- | --- |
| `catalog.py:89` | `~/.cache/luma/catalogs` — `catalogs` in the application slot |
| `session-manager`, 6 documents | `~/.local/state/luma/sessions` — **upstream, out of scope** |
| `permission-gate-test.sh`, 4 places | `~/.config/luma/foreman` — truncated |

**None was reported by anything.** A path nobody has written to before is
created on demand, and nothing notices the old one is empty.

### And one of them is a test that does not test what it says

`permission-gate-test.sh:265-267` asserts an agent cannot rewrite the gate.
**The gate lives under `data_home()`; the test writes under `config_home()`**,
which nothing installs into. It passes because `match.py:53` matches
`config/luma/` at the organization level, so any path under there is caught.

**The protection looks intact and the test does not demonstrate it.** Filed as
[[the-gate-test-does-not-test-the-gate]].

## The ledger

**`docs/standards.md`, 100 lines, every range.** The removal and every
destination are in one commit with this note.

| lines | what it held | verdict | where it went |
| --- | --- | --- | --- |
| 3 | *"a temporary stop gap until we have a proper standards system"* | **dropped as wrong** | that system exists and is adopted here. Carried nowhere |
| 5-8 | what XDG decides | **dropped as duplicate** | `luma-config` policy, *Machine-local paths follow XDG* |
| 9-12 | the four-directory list | **dropped as wrong** | no organization segment, and no `~/.cache` row. Superseded by the five-row table, corrected in `luma-config` 0.8.0 |
| 14-57 | nest under the organization, and the deny-rule argument | **dropped as duplicate** | `luma-config` policy, *Why nest under the organization* |
| 58-63 | the reversal note | **dropped as duplicate** | `CHANGELOG.md:92-93`, which holds more |
| 65-67 | `luma-shared` as its own repository | **dropped as duplicate** | `luma-config` policy, same section |
| 69-82 | config vs data vs state, and direnv | **dropped as duplicate** | `luma-config` policy, *Choosing between config, data and state* — with the changelog cited as a source |
| 83-85 | the foreman example — *"`policy edit` opens it in your editor"* | **dropped as wrong** | no such command; `--help` gives `agent-permissions edit`, and `policy.toml` became `permissions.toml`. Carried nowhere |
| 87-93 | the split is not cosmetic | **dropped as duplicate** | `luma-config` policy, sharper — it names the disarmed gate |
| 95-100 | migrating a path is user-visible | **dropped as duplicate** | `luma-config` policy, *Moving a path is a user-visible event* |

**Nothing was moved and nothing was rewritten.** Every surviving range already
existed in an adopted bundle, which is what made this a deletion rather than a
scatter — **the rarest of the four verdicts is the one that did not appear.**

**Three rows say `dropped as wrong` and name no destination**, each with what it
was checked against: the adopted bundle for `:3`, the corrected table for
`:9-12`, `--help` for `:83-85`.

## Where it went

| what | where |
| --- | --- |
| the organization segment missing from the canonical table | fixed — `luma-config` 0.8.0, and `<tool>`/`<application>` unified across the bundle |
| `~/.cache/luma/catalogs` | fixed in place — `catalog.py:89`. No migration owed; it is cache by that bundle's own test |
| the gate test | idea — `.luma/backlog/ideas/the-gate-test-does-not-test-the-gate.md` |
| `session-manager`'s `~/.local/state/luma/sessions` | journal — upstream, and vendored bundles are out of scope |
| `CHANGELOG.md:96` naming `policy doctor` and `policy install` | journal — a finding about a row this slice did not cover |
| `docs/architecture.md:65` and `CHANGELOG.md:100` pointing at the deleted file | repointed in this commit |

## Against the goal

**Both halves fired again, and the second one came from a bundle rather than
from this repository.** `:3` and `:83-85` were churn damage. The four-row list
was false on creation — and it was false *upstream too*, which is why three
repositories wrote the same wrong path.

**The most useful finding did not come from reading the file.** It came from
running the rule the file described against every path the code builds, which
is `cross-check` doing what slice 001 concluded it does.

## What this makes me doubt about earlier

**A document being superseded is not visible from inside it.** `standards.md`
read as reasonable prose; nothing in it announced that an adopted bundle had
taken the subject. **The check is mechanical — does an adopted bundle cover
this? — and no slice before this one ran it.** Slices 001 and 002 read four
documents that a bundle may well also cover, and that was never asked.

## Still open

**`docs/claude-agent-permissions.md`**, 274 lines, deferred to slice 004 — and
it is the document most likely to describe the gate whose test is broken.
