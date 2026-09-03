---
type: policy
title: What a README is for
description: A README answers what this is, why it exists, and where to go next — in that order. What belongs in one, what does not, and why the limit matters.
matches: eager
---

# What a README is for

**A README is a front door, not a manual.** Most people who open one are
deciding whether to keep reading at all, and they decide in seconds.

That single job sets everything below. A README that tries to also be a
tutorial, an API reference and a contribution guide fails at all four, because
the reader who needed one of them has to find it inside the other three.

## The default shape

A strong suggestion rather than a rule — a project with a good reason to differ
should differ, and most projects do not have one.

**1. A hook, then what it is.** One or two sentences that let a reader decide
whether to continue. Lead with what it does for someone, not with what it is
built from.

**2. Why it exists.** The problem it solves, or what was wrong with the
alternatives. This is the section most often skipped and the one that most often
decides adoption — anyone can see *what* from the code, and nobody can
reconstruct *why*.

**3. An example, if one helps.** Optional, and genuinely optional: some projects
are clearer without one. When included, make it the smallest thing that actually
works, and make sure it runs.

**4. Links to everything else.** Where to start, how to contribute, where the
documentation lives. Short lines with a reason to click, not an inventory.

Anything beyond those four earns its place individually.

## What belongs

- **Status, if it affects adoption.** Unstable, unmaintained, experimental,
  pre-release. Say it near the top — a reader who finds out later, from a broken
  build, has been misled by omission.
- **Installation**, when it is a line or two. Longer than that and it is a
  document.
- **Licence**, as a line and a link.

## What does not

Each of these has a better home, and moving it makes the README work again:

| in a README | belongs |
| --- | --- |
| exhaustive option and API reference | `docs/`, generated where possible |
| version history | `CHANGELOG.md` |
| how to set up a development environment | `CONTRIBUTING.md` |
| architecture and internal design | `docs/` |
| a tutorial series | `docs/`, one document per task |
| roadmap and future plans | wherever intent is tracked — and it goes stale fastest of all |
| badges past the two or three that mean something | nowhere |

**The test: would a reader deciding whether to use this need it in the first
thirty seconds?** If not, link to it.

## Why the limit is the point

A long README is not a thorough one. Every section added pushes the four that
matter further down, and the reader who was deciding whether to continue has
already stopped.

There is a second cost, slower and worse: **a README nobody can hold in their
head is a README nobody updates.** It drifts, and a drifted front door is worse
than a thin one, because a thin README is honest about what it does not cover
while a stale one is confidently wrong.

## Write for someone who has never heard of it

The hardest thing about a README is that you cannot read it as its audience.
Assume no context: not the problem domain, not the tooling, not the team's
vocabulary, not why anyone would want this.

That is why the hook comes first. It is the only part guaranteed to be read.
