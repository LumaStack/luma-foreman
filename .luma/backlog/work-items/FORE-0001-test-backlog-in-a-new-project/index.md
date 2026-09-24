---
type: work-item
key: FORE-0001
title: Test backlog in a new project
workflow_status: closed
rank: 070.0010.000
kind: change
stage: draft
created: {by: 'human:luma-founder', at: '2026-09-20T21:13:25Z'}
former_keys: ["WORK-0001"]
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T18:28:03Z'}
description: 'Get luma-backlog running in a second project — the first one that is not the repository it grew up in: a configured key prefix, another tool''s records sharing .luma/, and agents that have to be told when to run anything. Opened as a placeholder with no outcomes, because what standing it up would run into was not knowable in advance; the outcomes were written afterwards from what turned up. It runs. Fixing the defects it surfaced belongs to luma-backlog.'
closed: {on: 2026-09-24, as: completed, by: 'agent:claude-opus-5/luma-backlog', reason: 'The backlog runs in a second project, which was the whole intention. The defects it surfaced — the actor resolved from the OS account, and a disproven outcome rendering as passing — belong to luma-backlog and are not closed by this.'}
---

# Test backlog in a new project

## The problem

**This record was a placeholder, and it is honest about that.** It was opened to
hold one intention — get the backlog running in a second project — with no
outcomes, because nobody knew yet what standing it up would run into. The
outcomes below were written afterwards, from what actually turned up. They are a
retrospective account rather than criteria agreed in advance, and reading them as
a contract this work was measured against gets the record backwards.

**What made it worth doing: the tool grew up in one repository, and nothing had
shown it works in a repository it did not grow up in.** Everything about luma-backlog's own corpus is
the case its author had in front of him: the default key prefix, records only
this tool wrote, and an author who already knew which command to reach for. None
of those hold for a second project, and each is a way the tool could be quietly
unusable without a single test failing.

This repository is the first one to stand it up. It carries a configured key
prefix rather than the default, it shares `.luma/` with another tool's ideas,
plans, sweeps and decisions, and its agents have to be told when to run anything
at all. That makes it the place where *usable elsewhere* either holds or does
not.

**The window matters.** BACK-0037 says migration stays a one-repository problem
only until a second project starts — so this is also the last moment where
finding a shape problem costs one corpus instead of several.

## What is being delivered

**A working backlog in a second project — which is delivered; it runs.** The
evidence sits in the outcomes, each checked by hand here and recorded with what
the check rests on, so a reader who does not trust a result can repeat it. They
were written to capture what standing it up taught, not to gate it.

What that produced: the allowlist holds, and another tool's material under
`.luma/` neither parses as this corpus nor warns. Keys allocate under the
configured prefix and continue the project's sequence. The bundle is adopted and
its procedures are reachable as skills, demonstrated by reaching this work
through them. And the create-and-read check failed on its last clause, which is
the finding this work item exists to have produced.

## Out of scope

**Fixing what it finds.** The defects belong to luma-backlog, not here — the
actor resolved from the OS account, and a disproven outcome rendering as passing.
This work item records them; it does not repair them.

**The two work items that came out of this and are not it.** FORE-0002 moves the
ideas corpus into the backlog. FORE-0003 retires the bundle behind it. Both were
found here and neither is this.

**Promoting the decisions.** Thirteen ADRs sitting at `draft` is a real problem
and a separate one; it is a ruling rather than a migration.

## Constraints

**The checking has to happen here.** A test in luma-backlog's own repository
cannot answer whether the tool works in a repository it did not grow up in —
that is the one question this exists to ask, and the only place it can be asked
is somewhere else.

**Reading the output is part of it.** One outcome was closed by the maintainer
reading every command's output by hand before init ran, because whether output is
*right to a reader* is what a test cannot answer.

## Related work

**[BACK-0070 · Make the backlog usable in another project](https://github.com/LumaStack/luma-backlog/tree/main/.luma/backlog/work-items/BACK-0070-make-the-backlog-usable-in-another-project)**
— in `luma-backlog`. That record states everything that has to be true before a
second project can adopt the tool and keep receiving updates. This one is that
second project, so it is where those conditions either hold or do not. Findings
here are evidence against BACK-0070 rather than a separate concern.

A cross-repository link is a URL because it has to be. Wikilinks resolve within
one corpus, so `[[work-items/BACK-0070-…]]` written here would find nothing and
say nothing about it.
