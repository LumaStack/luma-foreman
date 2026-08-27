---
type: luma/idea
title: Declared maturity, and behaviour that respects it
created: { by: human:benlinton, at: 2026-08-19T00:00:00Z }
contributors: [human:benlinton]
horizon: someday
scope: project
lifecycle_status: draft
---

# Declared maturity, and behaviour that respects it

A repo or LKF document can declare it's maturity. Repos can declare in
README.md, CLAUDE.md, or maybe one or two other places. We need to provide a
list of maturities. Maybe we already have them and can use what's already
provided by LKF.

And then a when a repo has a declared maturity we can behave in different ways.
When something is brand new we should stop saying things like, this is already
established so we have to follow this or that rule. And when it's very stable
and established we have to treat most things like they are law.

We should prefer maturity at the document level, but when repos are brand new we
should accept it at the repo level as well so it's flexible.

## Notes

Migrated from `luma-leader/IDEAS.md` on 2026-08-21. `created.at` is a day-level
estimate.

**Added at migration — the document-level half already exists.** The knowledge
format defines `lifecycle_status` as a core field, `draft | provisional | stable
| archived`, defaulting to `provisional` when absent. That answers *"we need to
provide a list of maturities"*, and the entry's own guess that it might already
be there was right.

**A repo-level field belongs to the `project` type, not to the format.**
`.luma/project.md` is defined by the `project-documentation` bundle, which
is where a repository-wide maturity declaration would sit — alongside
`disclosure_level`, which is the same shape of claim.

**Kept out of the knowledge format deliberately.** A contract should be dumb
about how things get used: it defines shapes, not what a consumer does with
them. A format that encoded *treat a draft repository's rules as suggestions*
would couple the specification to one consumer's behaviour, and would be false
the moment another consumer ignored it. So the format supplies the field and
this repository supplies the behaviour.

**The behaviour is the unbuilt part, and the point.** Nothing currently reads
maturity to modulate how firmly it asserts anything — which is what produces
*this is already established* about a repository three days old.
