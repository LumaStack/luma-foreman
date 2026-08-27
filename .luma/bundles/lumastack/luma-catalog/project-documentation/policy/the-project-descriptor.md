---
type: policy
title: The project descriptor
description: The file a repository publishes about itself for something outside it to read — where it lives, what belongs in it, and why the repository has to own it rather than whoever collects it.
matches:
  - path: ".luma/PROJECT.md"
---

# The project descriptor

`.luma/PROJECT.md` — one file, usually one good sentence, answering **when
should somebody open this repository?**

It exists because something outside the repository eventually has to choose
between it and forty others, and **nothing outside can keep a description
true.**

## Every repository can have one; most should

Unlike everything else in [[which-document]], this has no interesting condition.
**The condition is that anything outside the repository ever needs to find it.**

Write one when the repository is one of several — which is most of them, and is
true from the moment a second exists. A single-repository project genuinely does
not need one; its README is the whole answer.

## The repository owns it. That is the point.

Whoever collects these — an organization's index, a search tool, an agent
choosing where to work — **could write descriptions instead. They should not.**

A collected description is a copy, and a copy of something that changes is wrong
from the first commit that changes it, with nothing to announce the drift. The
project ships, the description stays, and six months later something is being
selected on the strength of a sentence that has not been true since spring.

**Written here, it changes in the same commit as the change that invalidated
it** — reviewed by the people who caused the change, while they still remember
why. That is not a stronger process; it is the *only* one that keeps a
description honest, because it is the only one where updating it is cheaper than
not.

So: **the repository authors, and everyone else combines.**

## Keep it to what only this repository knows

**Do not restate what a reader already has.** Where it is hosted, what language
it is in, whether it is archived, when it was last pushed — anybody holding the
repository has all of that, and copying it here creates a second answer that
will eventually disagree with the first.

The test: **could whoever is reading this get it from the repository itself in
ten seconds?** Then leave it out.

What only this repository knows is **why it exists, when somebody should open
it, and where its boundaries are.** That is the file.

## It is not a README

Different reader, different job.

| | README | descriptor |
| --- | --- | --- |
| read by | a person deciding whether to keep reading | something deciding whether this is relevant at all |
| length | four sections | one sentence, plus boundaries |
| when read | after arriving | **before arriving** |

**The descriptor is read first and by something that will not read further** if
the answer is no. That is why it is separate: a front door assumes somebody is
already at the door.

**Do not generate one from the other.** A README's opening line is a reasonable
*fallback* for whoever has no descriptor to read, and it is not a substitute —
it was written to hook a human, not to be selected on.

## Nobody outside writes into it uninvited

A descriptor is a claim the repository makes about itself, so **the repository's
own people make it.**

Somebody collecting descriptors may propose one — that is useful, and often the
only way a gap gets closed. It arrives as **a pull request against that
repository**, per repository, decided by its owners. Never a direct commit, and
never in bulk across an organization.

**And never in a repository that has not adopted `.luma/`.** Having something to
file is not a reason to introduce a directory structure into somebody's project;
where there is no `.luma/`, the honest answer is that there is nowhere to put
one yet.

## An absent descriptor is a real answer

**Do not invent one to fill a gap.**

An invented description is indistinguishable from an authored one, and something
selecting repositories on a guess is worse off than something that knows it does
not know. *Nobody has said what this is for* is findable, fixable, and honest;
a confident sentence nobody wrote is none of those.

Deriving is different from inventing, and the difference is provenance: a
fallback taken from a README or a hosting description, **recorded with its
source**, stays visibly second-best. A sentence an agent composed from reading
the code, stored as though the project said it, does not.
