---
type: slice
title: The documents split out of the README
created: 2026-08-29
covers:
  - docs/getting-started.md
  - docs/commands.md
  - docs/architecture.md
  - docs/inspect.md
contributors:
  - human:benlinton
  - agent:claude-opus-5
---

# 001: split from README

## What this is

The four documents created when `README.md` was thinned to the
`project-documentation` readme policy — install, the command reference, the
inspect rules, and foreman's invariants. Written by the agent, read here by
their author for the first time.

**Presented one at a time, agent's read first, then opened for the reader.** The
sweep declares `human-agent` and this cluster is `read by: both`.

## What we made of it

**Three of the four contained false claims, and all four were a day old.** The
sweep is aimed at churn damage; what this slice found was not drift. **The
documents were wrong when they were written**, and splitting them out of the
README is what made that visible — the same errors had been sitting in the
README unread.

| file | what was wrong |
| --- | --- |
| `getting-started.md` | the optional permission gate led, before the loop foreman exists for. An unstated `$PWD` assumption in the install line, silently wrong for anyone who `cd`s into the clone |
| `commands.md` | *"every command takes `--to`"* — false. *"exit codes are consistent"* — false, that was one command's set. *"four verbs, two nouns"* — a count, which `writing-style` forbids. `--check` described as Ansible's dry run when it is a formatter's staleness gate |
| `architecture.md` | *"bundles depend on nothing"*, *"a directory copy"*, the edited-copy sentence. **`CLAUDE.md` described as indexing what is adopted** — it does not; it points at an entry point that points at rings |
| `inspect.md` | nothing wrong. The only file whose cross-check was clean on the first pass |

**`inspect.md` was collapsed into `commands.md` rather than approved.** A
command's detail belongs in the command reference until it outgrows a section:
fifty lines is a section, and `claude-agent-permissions.md` at 274 is a
document.

**The `cross-check` habit found everything mechanical.** Every false claim came
from running the thing the document described — `--help`, the rules on disk,
`install.py` — rather than from reading carefully. The claims that survived
careful reading were the ones nobody had checked.

## Against the goal

**On track, and the goal was aimed slightly wrong.** *Does every file still say
what its author meant after the churn* assumes drift. These files had no history
to drift from; they were false on creation.

**Worth carrying into later slices**: for anything created during the estate's
recent churn, the question is not *did this rot* but *was this ever true*.

## Where it went

| what | where it went |
| --- | --- |
| bundles should be able to depend on bundles | idea — `.luma/backlog/ideas/bundles-declare-what-they-work-with.md` |
| never derive an actor from the OS user | idea — `.luma/backlog/ideas/never-derive-an-actor-from-the-os-user.md` |
| a real workstation account in two published catalog files | fixed — `review-sweeps` `0.9.1` |
| every false claim above | fixed in place, by the author, during the slice |
| `inspect.md` | deleted; content absorbed into `commands.md` |

**Everything the practice taught went into the bundle**: `review-sweeps` went
`0.6.1` → `0.9.1` across four releases during this one slice.

## Still open

**`docs/getting-started.md:9`** — the `$PWD` assumption was raised and not
addressed. Approved with it standing.

**`bundles depend on nothing` is load-bearing in three `bundle-manager`
workflows.** `create-bundle` uses it to argue when to split a bundle in two;
`migrate-bundle` and `where-a-bundle-belongs` rest on *nothing to update*. The
idea records it; the arguments have not been revisited.

**`index` may be retired vocabulary and nothing enforces it.** The `vocabulary`
rule ran clean because the term is not configured. If *entry point* and *routing*
have replaced it, that is a decision record and a vocabulary entry away from
being caught automatically.

## Where the practice fought us

**The agent refused a status the reader had given.** The largest failure of the
slice, and the bundle existed to prevent exactly it. Fixed in `0.7.0` — the
reader owns the row, and `reviewed` split from `approved` so an agent-agent
sweep can still finish one.

**Presentation was invented three times before it settled.** File-at-a-once,
then wrong order, then wrong depth. Fixed in `0.8.0` with a policy and a
template — and the first three files of this slice were spent on it rather than
on the files.

**The agent could not open files and assumed it could.** `EDITOR` is a terminal
editor here; a non-interactive call has no terminal to give it. Fixed in `0.9.0`:
emit `path:line` in full and let the reader's terminal resolve it.

**The reader edited files mid-presentation, twice, and both agent edits silently
missed.** Fixed in `0.9.0` — re-read before editing, because the copy you
presented is already history.

**`git add -A` swept an unrelated untracked file into a pull request twice**, in
the same repository, caught both times by the catalog's own versioning check
rather than by the agent.
