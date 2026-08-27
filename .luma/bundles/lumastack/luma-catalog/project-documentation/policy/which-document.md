---
type: policy
title: Which document to write
description: The documents most projects can have, what each is called, and the condition that earns it. Write one when its condition is met, not before.
matches:
  - topic: deciding whether a document is worth writing
---

# Which document to write

**Every document is a liability until somebody reads it.** It has to be kept
true, and a stale document is worse than a missing one — missing is honest,
stale is confidently wrong.

So the question is never *what should we have*. It is **what condition have we
hit**.

## The matrix

| document | where | write it when |
| --- | --- | --- |
| **README.md** | root | always. Every repository, from the first commit |
| **.luma/PROJECT.md** | `.luma/` | anything outside the repository has to choose between it and others — true from the moment a second exists. See [[the-project-descriptor]] |
| **LICENSE** | root | anyone outside the team might use it. Absent, the default is *nobody may* |
| **CONTRIBUTING.md** | root | somebody outside the core has offered to help, or you want them to |
| **SECURITY.md** | root | a stranger finding a vulnerability would not know who to tell |
| **CODE_OF_CONDUCT.md** | root | the project has a public space where people interact |
| **docs/getting-started.md** | `docs/` | setup is more than clone-and-run, and the README section is outgrowing itself |
| **docs/architecture.md** | `docs/` | the shape is not obvious from the directory tree, or an invariant exists that a newcomer would break |
| **docs/explanation.md** | `docs/` | people keep asking *why is it like this*, and the answer is not a decision record |
| **docs/glossary.md** | `docs/` | a term means something specific here, and somebody has already been confused by it |
| **docs/troubleshooting.md** | `docs/` | the same question has been answered twice |
| **docs/<task>.md** | `docs/` | a task has more than a few steps and is done more than once |

**The right-hand column is the whole point.** Each condition is observable — a
question asked twice, a person confused once, a stranger with nowhere to report.
Writing a document before its condition fires produces something nobody needed
and everybody now has to maintain.

## The kinds, and why mixing them fails

The [Diátaxis](https://diataxis.fr) framework is worth reading once. Its claim,
compressed: documentation serves four distinct needs, and a document trying to
serve two serves neither.

| kind | the reader wants | example |
| --- | --- | --- |
| **tutorial** | to learn by doing | getting started |
| **how-to** | to accomplish a specific task | deploying, adding a migration |
| **reference** | to look something up | configuration options |
| **explanation** | to understand why | architecture, design rationale |

The common failure is a *how-to* that keeps stopping to explain, so somebody
following it has to skim past reasoning to find the next command — and somebody
reading to understand has to skip the commands. **Split them and both work.**

## What is not on this list

**`CHANGELOG.md`** is owned by the release bundle. **Decision, audit and log
records** are owned by their record bundles and live in `.luma/records/`.
**`AGENTS.md` and `CLAUDE.md`** are generated from `.luma/`, never authored.

Named so an omission reads as a boundary rather than a gap.

## Deleting counts as maintenance

A document whose condition has passed should go. The setup guide for a system
you no longer run, the troubleshooting entry for a bug that was fixed — both are
now traps, because a reader has no way to know they are obsolete.

**Delete it and say so in the commit.** The history keeps it. Leaving it in
place with a note saying it is out of date is the worst option: still found,
still read, and now with a disclaimer nobody trusts.
