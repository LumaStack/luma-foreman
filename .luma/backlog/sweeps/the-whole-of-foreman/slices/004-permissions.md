---
type: slice
title: The permissions document, skipped
created: 2026-08-29
covers:
  - docs/claude-agent-permissions.md
contributors:
  - human:benlinton
  - agent:claude-opus-5
---

# 004: permissions

## What this is

**One file, presented and skipped.** `docs/claude-agent-permissions.md` — the
permission gate end to end: install, the two enforcement layers, precedence, the
four values, per-project policy, what the layer is not, keeping the agent out of
its own rulebook, and how to verify.

**Skipped by the reader**, on a reason that is about the subsystem rather than
the document: **agent permissions are half-baked, and settling that is outside
MVP.**

**That reason reaches further than this row.** It is not *this file is fine* — it
is *this whole area is not ready to be held to a standard yet*, and the sweep's
goal is whether documents state the truth about things that exist. **A document
describing a subsystem still being decided cannot be checked against a settled
answer**, because there is not one.

## What we made of it

**The reader did not read it.** The agent's orientation and cross-check were
given and stand as the only read; **no verdict was formed about the content** and
none is recorded.

### The cross-check came back clean, and it is the only one that has

**274 lines, one commit, created 2026-08-20, never revised** — and more churn
around it than any file the sweep has read.

| checked | result |
| --- | --- |
| every command invocation | **all current.** No `policy` spelling anywhere, unlike `docs/standards.md` and `CHANGELOG.md:96` |
| every path | **correct and unabbreviated** — `~/.local/share/luma/luma-foreman/`, `~/.config/luma/luma-foreman/permissions.toml` |
| `:243`'s `sh tests/run` | runs, all suites pass |
| every check `:255-262` claims `doctor` performs | present in `doctor.py` |

**`:177` gets the config/data split right**, explicitly — *"They are in
**different** directories on purpose"*, gate in `~/.local/share`, policy in
`~/.config`. **This is the document `permission-gate-test.sh` contradicts.** The
prose was correct the whole time and the test was not.

**The least-maintained file in the sweep had nothing wrong with it.** That is
one observation, not a pattern, and it sits against the goal rather than with
it.

## Against the goal

**It did not serve the first goal and could not have.** A file with no false
statements produces no findings, and the sweep learned that only by checking.
**Reading with nothing found is a result** — but the reader did not read, so
even that is the agent's result alone.

**It served the second goal heavily.** Five releases of `review-sweeps` came out
of this slice — 0.19.0 through 0.23.0 — every one from a case that occurred
here: a removal owing a ledger, a file closing on a verdict rather than
momentum, fix-now-or-route, no counts in the charter, and the slice-close
routine. **That is the lopsidedness the charter now names as a risk**, visible
in a single slice.

## Where it went

| what | where |
| --- | --- |
| the correction to `the-gate-test-does-not-test-the-gate` — `doctor` *does* probe the real path | the idea, updated in slice 003's commit |
| `doctor`'s heading shape, and the renderer split under it | journal — routed at the reader's choice |
| templates carry no frontmatter and never say where their output goes | `luma-leader`, as `bundle-template-maker` |
| the idea backlog, 31 rows | skipped, given |

## Still open

**Nothing from this file.** Its findings are none, and its row is closed.

**Eleven rows sit under the same reason and are still `pending`.** Eight modules
in `src/foreman/agent_permissions/`, `libexec/permission-gate.py`, and the two
suites that exercise them. **If the subsystem is out of MVP, the reason given
here applies to all of them** — and leaving them pending claims the sweep
intends to reach them.

**Not assumed and not marked.** The reader gave a reason for one row; extending
it to eleven is exactly the inference `review-sweeps` 0.20.0 exists to stop.

**It also changes what a finding there would be worth.**
[[the-gate-test-does-not-test-the-gate]] is a real defect in a subsystem nobody
has settled, which makes it worth keeping and not worth prioritising. Recorded
so the close does not read it as urgent.

**The sweep's shape changed underneath it.** With the ideas skipped, what remains
is `src/`, `tests/`, `bin/`, `libexec/` and four prose files — **almost entirely
the half read by agent with the reader taking a summary**, which the charter
already flags as where the reader's independent view is weakest. Worth deciding
before slice 005 whether that arrangement still holds now that it is nearly the
whole remainder rather than half of it.
