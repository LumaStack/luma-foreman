---
type: luma/idea
title: Confusion earns a retro, not automatically a rule
created: { by: human:benlinton, at: 2026-09-06T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# Confusion earns a retro, not automatically a rule

**A model hits a problem, then finds the detail that dissolves it — and its
next instinct is to write that down somewhere.** Do that a few dozen times and
the system is full of answers to problems nobody had. The reflex needs a gate
in front of it.

## The failure this addresses

Models resolve confusion by adding text. Each addition looks locally
reasonable and costs almost nothing to write, so nothing stops it — and the
accumulation is rot: prose nobody asked for, answering questions nobody has,
which the next reader has to wade through and eventually distrust.

**Writing nothing has to be a first-class outcome**, not the thing that happens
when somebody forgets to write something.

## What went wrong — pick one

- **We invented the problem.** Recording its answer is bloat, because we are
  writing answers to problems we never had.
- **A one-off model mistake.** The next model will not hit it, and nothing
  needs to change.
- **The documentation was not clear enough**, and there is tuning to be done.
- **The documentation disagreed in two or more places**, and that disagreement
  caused the confusion — so there is something to fix rather than something to
  add.
- **Would adding text make this better, or just add noise?**

## How would we fix it — pick one

- **The knowledge was too hard to surface at the right place and time.**
- **Surfacing was fine and the model got lazy**, which it does — so the
  knowledge may need injecting more forcefully rather than being written again.
- **The knowledge disagrees with itself in two or more places** and needs
  reconciling.
- **A lack of clarification let an assumption fill a blank**, and the
  assumption was wrong.
- **Do we understand the fix well enough to make it better?** Or might we make
  it worse by confidently writing a rule that overreaches or does not last.

## What it would be

A policy for the judgement, and a procedure that walks it — kicking in when a
problem is raised and then withdrawn, and ending in an explicit decision about
whether anything durable gets written at all.

## Open

**Where it belongs.** This is a general practice for anyone maintaining
knowledge, not something specific to foreman — so it may be a catalog bundle
rather than a project idea. Captured here because that is where the
conversation happened.

**What triggers it.** *A problem was raised and then withdrawn* is the clear
case. Whether it should also fire on a rule being added at all is undecided,
and the broader trigger is the one that would catch more rot and annoy people
more.

## Related

**[[verification-beyond-inspect]] is the same rot from the other end.** It says
mechanical rot is checkable and the other kind is not — *"a policy nobody
follows, a document still accurate but no longer read"* — because those are
facts about behaviour rather than about the file. Reflexive
documentation-writing is one of the things that manufactures exactly that
undetectable kind, so this attacks at the moment of creation what that one
cannot find afterwards.

**[[feedback-and-learning]] wants evidence of what actually went wrong**, and
says the first real question is what the system is allowed to observe. A retro
that records how a session got confused produces that evidence as a by-product,
from inside the session, without observing anybody.
