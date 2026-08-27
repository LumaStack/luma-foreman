---
type: luma/idea
title: A prose conventions bundle — spelling, terminology, house style
created: { by: human:benlinton, at: 2026-08-21T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: organization
lifecycle_status: draft
---

# A prose conventions bundle

Spelling, terminology, house style. **It would apply to every bundle, including
the ones already written.**

## There is concrete evidence this is wanted

The catalog carried **67 `-ize` spellings against 6 `-ise` ones**, and nothing
anywhere declared which was correct. **The convention existed only as weight of
usage**, which is exactly how the six got in — nobody was wrong, because there
was nothing to be wrong about.

That is the shape of the problem: a convention everybody follows and nobody
states drifts silently, and the drift is invisible until somebody counts.

## Absolutes are a claim, not a register

**Say what a thing does. Assert what it will always do only where boxing in the
future is the point.** *Always*, *never* and *no others* read as authority and
are often just emphasis — and an absolute stated in passing is one somebody has
to supersede later rather than update.

ADR-0003 is the worked example, three times in one afternoon. It said *"two
commands may reach the network and no others"* — a taxonomy of the day written
as a rule, so correcting it looked like it needed a superseding record. That
became *"`catalog` always reaches the catalog"*, the same mistake with new
content. Then *"a description, not a boundary"*, which is a rule about not
making rules. It now just says which commands reach out and which do not.

**Some absolutes earn it and must survive the sweep.** *Adoption never resolves
anything* is the decision itself. *A flag may change how much or how, never what
comes back* is a rule with three worked failures behind it. *A notice never
fails a run* is a designed guarantee. The test is not the word — it is whether
the sentence is deliberately constraining what may happen next, and whether
somebody could say why.

The five decision records hold about thirty-four of these and they have not been
sorted. That is a pass with judgement in it rather than a find-and-replace.

## Notes

Migrated from `docs/next-steps.md` on 2026-08-23, where it was listed twice
under *Wanted, not built* — once bare and once with the spelling count. The
duplicate is itself a small argument for the bundle.
