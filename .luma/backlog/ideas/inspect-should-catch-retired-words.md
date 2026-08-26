---
type: luma/idea
title: inspect should catch retired words, and needs a severity that does not fail
created: { by: human:benlinton, at: 2026-08-26T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
---

# `inspect` should catch retired words

ADR-0003 retires three words — `jobs` for subcommands, `projection` for what
`apply` writes, `refit` for anything. **Nothing enforces that.**

**A retired word comes back by being reinvented, not by being remembered.**
Both `jobs` and `projection` are the natural English for what they described, so
an author reaches for one again and it reads as a fresh choice rather than a
revival. Absence from the codebase is the only current defence and it is a weak
one — it makes recurrence look original.

The retirement is written down now, which makes it citable. It does not make it
checked.

## What it would have caught

The sweep that retired `projection` **missed `.luma/backlog/ideas/` entirely**
— sixteen lines across six files, still naming commands that exit 1. The passes
covered `src/`, `docs/`, `README`, `CHANGELOG`, the records and the catalog, and
nobody thought of the backlog until a stray use in conversation prompted a
re-grep. A rule reading the whole repository does not forget a directory.

## The shape

A list of retired terms with what replaced each, and where the list lives is the
first question. Candidates: `.luma/config/luma-foreman.toml`, which is meant to
hold overrides rather than content; a `prose-conventions` bundle, which is
[[prose-conventions]] and would travel to every adopter; or the rule's own
source, which is wrong the moment a project retires a word of its own.

**The exemption is the part to get right.** A published `## Version` history
correctly says `outfit` — it records what was true when written, and rewriting
it would falsify the record. So would an ADR describing a decision in the terms
of its day. A rule that cannot express *everywhere except history* will be
turned off within a week.

## The severity it needs now exists

`inspect` has a **notice**: printed as loudly as a finding, counted separately,
never part of the exit code. Built 2026-08-26, taking the word
`luma-catalog-curator` already used. [[a-reminder-needs-somewhere-to-live]]
wanted the same tier and can use it too.

That was the blocker. What remains is the rule.

## A grep cannot tell a revival from a legitimate use

**And it must not try.** *Projection* has an ordinary mathematical sense.
*Jobs* means something real in a sentence about CI. A quotation of somebody
else's prose is not a revival, and neither is an example of what not to write.

**This is the reason it is a notice rather than a finding**, and the reason a
notice carries more context than a finding: the check is handing somebody a
judgement it cannot make, so it owes them what the judgement needs.

Each hit should carry:

- **the term**, and what replaced it
- **where it was retired and why** — a citation, so the reader can go and read
  the reasoning rather than take the tool's word
- **the hit in context**, with its location

A model reading `inspect --json` then has enough to decide *this is a revival,
fix it* against *this is fine, leave it*, and to say which. A bare list of
line numbers would make it guess, and guessing is what turns a notice into
noise somebody filters out.

**One exemption is mechanical rather than a judgement.** A published `##
Version` history correctly names a since-renamed thing — it records what was
true when written, and rewriting it falsifies the record. Same for a decision
record describing its own moment. A rule that cannot express *everywhere except
history* gets switched off within a week.

## The objection

**A tier nothing fails on is a tier people stop reading.** Two notices become
twenty and the section turns into scenery. That is the argument for keeping the
list very short — retired words only, not house style — and for `inspect --json`
carrying them so something else can decide to care.
