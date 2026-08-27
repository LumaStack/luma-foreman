---
type: document
title: Where history belongs
description: History stays in loaded context only where it earns its place; otherwise it belongs in git, in records, in backlog journals, in logs, or wherever else a team already keeps it. Neither list is comprehensive.
---

# Where history belongs

**Preferences, not rules.** This is where things usually belong and why. Real
work keeps producing cases nobody anticipated, so depart from any of it when
there is a reason — and the reason does not have to appear below.

**The short version: history stays in loaded context only where it earns its
place.** Everywhere else it moves somewhere holding it is the job, and the
document, policy or workflow says what is true now.

## Where history belongs

**In git, in records, in backlog journals, in logs, and in whatever else a team
already uses for it.**

**That is not a comprehensive list and should not be read as one.** What these
have in common is that holding the reasoning is their job — so any destination
with that property qualifies, including ones nobody here has thought of.

- **git history** — the commit message. The `merge-commits` policy in the
  `lumastack/luma-catalog/git-workflow` bundle rests its case against squashing on the commit
  message being where rationale lives, so this is a home that already claims the
  job.
- **pull requests and review threads** — often the more natural place for an
  argument that involved several people.
- **records** — a decision record keeps deferred alternatives and re-open
  triggers; an audit record keeps a finding and the answer to it.
- **backlog journals** — how an intention changed, kept beside the intention
  rather than in whatever describes the current plan.
- **logs** — `log.md` is reserved for this by the `lumastack/luma-catalog/luma-layout` bundle:
  append-only, newest first, never rewritten.
- **wherever a team already keeps this** — an issue tracker, a design archive, a
  wiki. A destination that exists and is used beats a better one that is not.

**None of this is discarding history.** It is worth keeping — detective work when
something breaks, and learning what a process gets wrong so it can get better,
both need the false starts and the arguments that lost. **That job is done better
when the material is in one place** than when it is sprinkled through content
everybody loads.

**One distinction inside the list is worth keeping straight.** Git history and
pull requests sit outside the working tree, so they cost a reader nothing until
somebody goes looking. Records and journals are committed and loadable, so they
cost what any content costs. The difference is that in them the reasoning is not
noise: the same paragraph is clutter in a policy and content in a decision record,
and nothing about the paragraph changed.

## Earning a place in loaded context

**This is not only about documents.** A policy, a workflow, a guide — anything an
agent loads is context somebody pays for, and the question is the same for all of
it.

**History earns its place by being useful to a reader now.** Some ways it does,
and certainly not all of them:

- **it prevents re-litigation** — a compressed *this was considered and not taken,
  because* saves the next person a week. The paragraph, not the argument as it
  happened.
- **it justifies why something is the way it is** — some rules only make sense
  once you know what went wrong, and stripping the story leaves something nobody
  can apply or trust.
- **the reader is learning rather than looking something up** — explanation and
  tutorial material often teaches through the wrong turn.
- **the history is the subject** — a postmortem, a migration guide, an account of
  how something came to be shaped this way.
- **the type exists for it** — see below.

**Where it is genuinely unclear, leaving it out is the cheaper mistake.** Adding a
paragraph back later costs a paragraph. Removing one that has been read for a year
costs everyone who read it.

## What usually goes where

Illustrative, not exhaustive.

| | usually |
| --- | --- |
| what was decided, and what is in force | the content |
| what was rejected, and why it stays rejected | the content |
| the back-and-forth before deciding | history |
| scratchpad notes and working thoughts | history, or nowhere |
| what an earlier draft said | history |
| that somebody was wrong, and corrected it | history |
| how long it took, and how many attempts | history |

**The pattern underneath, loosely:** *the shape of the answer* tends to belong in
what gets loaded; *the shape of the work* tends to belong in history. A lean, not
a boundary — plenty of things sit on it.

**None of this argues for terseness.** Length spent on what is true now earns its
place. A long explanation of a live constraint is fine; a short paragraph about a
dead one is not.

## Why the cost is higher than it looks

**Loaded content is read by agents, in full, repeatedly, against a finite budget.**
A paragraph a person skims in a second is paid for on every read, forever — and an
agent cannot skim. It reads what it is given.

**The second effect is worse than the cost.** Content describing a position nobody
holds any more invites a reader to reason about it as though somebody did. A
person recognises *we used to think X* as background. An agent may take it as a
live constraint, and nothing in the text marks which sentences are still in force.

That gives *every document is a liability until somebody reads it* — from
[[which-document]] — a second and sharper reason.

## Some types show their work by design

**Where a record type exists whose job is showing the work, the question does not
arise.** Decision records keep the argument that was not taken so a decision can be
revisited rather than re-litigated; audit records keep a finding and the answer to
it, because the exchange is the point.

**That is the easy case, and it is easy because the file decides rather than the
author.** Everywhere else somebody has to think about it, which is why the rest of
this is preference rather than rule.

## In practice

**When reasoning changes course mid-edit**, the usual move is that the correction
goes into history and the content simply reads correctly afterwards. A note
explaining the change is usually worth deleting.

**When reviewing**, a sentence that only makes sense to somebody who knows what it
used to say is the one worth a second look. Sometimes it has earned its place.
Often it is a leftover.

**A rejected alternative is design. "I previously thought X" is a diary.** That
distinction carries more weight than any rule here.
