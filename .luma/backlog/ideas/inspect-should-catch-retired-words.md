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

## It needs a severity that does not fail

**A retired word is not broken code**, and every `inspect` severity is a finding
that exits 1. Failing continuous integration over a word teaches people that a
red run means nothing, which costs more than the word does.

`luma-catalog-curator` already has the tier and calls it a **notice**: *"A
notice is for a second reader, and never fails a run."* It earned that on
2026-08-26, catching a real meaning shift inside a change that read as a pure
rename.

**This is the same missing tier [[a-reminder-needs-somewhere-to-live]] needs**,
for the same reason — a draft that has gone into use is not broken either.
Whichever gets built first should build the tier, and adopting the word the
sibling tool already uses beats inventing a second one.

## The objection

**A tier nothing fails on is a tier people stop reading.** Two notices become
twenty and the section turns into scenery. That is the argument for keeping the
list very short — retired words only, not house style — and for `inspect --json`
carrying them so something else can decide to care.
