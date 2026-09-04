---
type: policy
title: Command line interface guidelines
description: Read our command line interface guidelines before designing or changing CLIs.
matches: eager
---

# Command line interface guidelines

## Step one: read [clig.dev](https://clig.dev)

**Before adding or changing a command, a verb, a flag, or a message a user
sees — read the [Command Line Interface Guidelines](https://clig.dev) (CLIG).**
It is one page, and adopting this bundle is the act of saying that a project
designs against it.

**What to look for**, so the read is targeted rather than a skim: the
stdout / stderr / exit-code contract; writing for a human on a terminal
versus a program on a pipe, and everything that follows from detecting which
(`--json`, `--plain`, `NO_COLOR`, suppressed animation); the standard flag
names; when to confirm before a destructive action; the configuration
precedence order; and the rule that secrets never travel through a flag or
an environment variable. Those are the parts that decide whether code is
right or wrong, rather than merely nice.

## Step two: what outranks it

**A decision that is in force.** Where this project has
recorded a decision about the command line and that decision is in force —
`provisional` or `stable` on the ladder this estate uses, not `draft` —
it was made with context no external guide has, and it is the answer.
A `draft` is a proposal, so it outranks nothing - but may be worth
mentioning to the user.

If a decision in force and CLIG disagree in a way that looks like an
oversight rather than a choice, that is a reason to re-open the decision. It
is never a licence to quietly ignore it.

**What the program already does is not an argument.** Precedent is not a
decision. A convention can be established and still be wrong, and adopting
this bundle is a commitment to improving a command line rather than to
preserving whichever shape it drifted into. Where there is no decision in
force, follow CLIG — including where that means changing something that
already works.

The cost of changing it is real, but it is a *sequencing* problem rather than
a reason: a change users can see is a breaking change, and CLIG's own
future-proofing rules say how to make one. Follow those. Do not use them as
grounds to keep the old shape.

**Follow the user's directives.**  If a user gives a directive to break
from these guidelines, inform them of the break so they are made aware
and also follow the directive for the remainder of the session.

## Step three: record what you decided

**Where this project departs from CLIG, write down why.** A convention
broken on purpose and a convention broken by accident look identical in the
code, and the next person — or the next agent — cannot tell them apart
without a record. The record is what makes the divergence defensible instead
of merely present.

**Record the choices the guide leaves open, too.** Which exit codes mean
what, what a bare invocation does, how a refusal is phrased, whether verbs
sort by frequency or by kind — CLIG deliberately does not settle these,
and a project that has not settled them will answer them differently every
time somebody adds a command.

**Until it is recorded and in force, it does not bind.** That is the whole
weight of this step: the way to make something outrank CLIG is to decide
it deliberately and write it down, not to do it twice.

## Disclaimer

**CLIG is not summarised here on purpose.** clig.dev is licensed
[CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/), so a
distillation of it is a derivative work carrying a second licence into
whatever repository holds it — for prose that already exists, in one place,
maintained by the people who wrote it. Read the source.