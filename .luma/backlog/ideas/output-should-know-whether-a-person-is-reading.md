---
type: luma/idea
title: Output should know whether a person is reading it
created: { by: human:benlinton, at: 2026-09-06T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# Output should know whether a person is reading it

**Every command prints the same bytes to a terminal, a pipe, a log and a
screen reader.** CLIG asks for the opposite — decorate for a human, simplify
for a program — and foreman does it nowhere.

## What is at stake, now that there is decoration to strip

`bundle list` draws box glyphs and status marks. They are the right thing in
front of a person and the wrong thing everywhere else:

**A screen reader announces every one of them.** `├─` is read as *box drawings
light vertical and right*, or dropped, before every row. The status marks
(`● ◐ ⊘ ○`) at least carry meaning; the tree glyphs are decoration, and a
reader who cannot see them pays for them anyway.

**A pipe gets furniture it cannot use.** `grep` is unaffected — it matches
whole lines — but `awk` and `cut` see `├─` where a caller expected a name.

**A log file keeps the drawing forever**, which is what CI output becomes.

## What it would be

**Detect a non-terminal on stdout and drop to plain.** No box glyphs, no
alignment padding computed from terminal width. The status marks are the open
question: they are information rather than ornament, so a word may be the
right plain rendering rather than nothing.

**A flag that forces either way**, because detection is wrong sometimes and a
person piping to `less` still wants the decoration.

**`NO_COLOR` if colour ever lands.** It has not — there is no ANSI anywhere in
foreman today — and the moment it does, this is where honouring that
convention belongs.

## What it is not

**Not `--json`.** That already exists where machine consumption is real
(`inspect`, `bundle outdated`) and is the right answer for a caller that wants
fields. This is about the human-readable stream being honest about who is
reading it, not about growing a second machine format.

## Why it is worth doing rather than not decorating

The alternative is keeping every output plain forever on the chance somebody
pipes it. That trades a certain cost — worse reading for the people who
actually run these commands — against a rare one, and it is the wrong way
round. **One mechanism fixes the screen reader, the pipe and the log at once**,
which is why it is worth building rather than avoiding decoration.

## Notes

Raised while adding tree glyphs to `bundle list`. The glyphs went in anyway:
this is the mitigation for them, and it touches every command that prints
rather than that one.
