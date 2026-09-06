---
type: luma/idea
title: The loading posture vocabulary is user-facing now, and two of the words are unsettled
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5, agent:claude-opus-5]
horizon: later
scope: project
stage: draft
---

# The loading posture vocabulary is user-facing now, and two of the words are unsettled

**The display half of this shipped.** `bundle list` prints each bundle's
posture, which is the fact a reader tending context cost actually wants. What
remains is the naming, and it matters more than it did — these words now appear
on rows people read rather than only in a record.

## Renaming a posture is nearly free, and that is the point

**A posture is derived and only ever printed.** `matches: eager` and
`matches: nothing` are authored in bundles; `guaranteed`, `offered` and
`standby` are what the tool *calls* the result. Changing an authored value is a
format change that touches every bundle in the estate and needs a tolerance
either side of it. Changing a posture name changes one table and some prose.

So this should be decided on which words are clearest, not on what they cost.

## `eager` versus `guaranteed`, and whether they are two names at all

**ADR-0007 says the postures are `guaranteed`, `offered`, `standby`. The code
says `eager`, `offered`, `standby`.** They have disagreed since the record was
written, and nothing has been wrong as a result — which is itself the argument
that one of them is redundant.

**The real question is whether the authored value and the posture it produces
should share a word.** `matches: eager` producing a posture called `eager` is
one word to learn and an obvious mapping. ADR-0007's `guaranteed` describes the
*consequence* — it loads, guaranteed — where `eager` describes the *request*.
Both are defensible; the estate currently has both, which is the one option
that is not.

## `standby`, and what else it could be

*standby* does not explain itself on a row the way *on-demand* would. It is the
posture for a bundle with no matcher: nothing announces it, and a request or a
citation is the way in.

Neither word is obviously right. **`standby` suggests waiting to be activated**,
which overstates — nothing is watching for a moment to load it. **`on-demand`
suggests a mechanism**, which also overstates, since the demand is somebody
naming it. Worth weighing alongside *by request*, which is what the generated
project index already calls this section, and *unlisted*, which describes what
is actually true of it.

**`by request` has the strongest claim on precedent** — `apply` writes it into
every project's index today — and using two words for one state in two
generated outputs is the disagreement this whole entry is about.

## `offered` is now read less, which cuts both ways

`bundle list` shows a posture only when it is not `offered`, since the default
on every row was a word becoming wallpaper. So the word is seen rarely — which
lowers the stakes on getting it right, and raises them on the two that are now
the only ones anybody sees.

## Notes

The original entry paired this with surfacing the posture in `bundle list`,
which is done. Its filename still says so and no longer matches what it holds —
worth renaming when somebody picks this up.
