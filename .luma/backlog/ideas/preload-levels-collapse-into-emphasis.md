---
type: luma/idea
title: Projected through an index, preload levels differ only in emphasis
created: { by: agent:claude-opus-5, at: 2026-08-23T00:00:00Z }
contributors: [agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
---

# Projected through an index, `preload` levels differ only in emphasis

**A finding from building `apply`, not a proposal.** The first thing to read
`preload` found that the three levels it can distinguish do not survive being
written into a harness.

## What `apply` does with the field today

| declared | what reaches an agent |
| --- | --- |
| `mandatory` | a line in a hoisted **read these first** section |
| `recommended` | a line in the bundle's list |
| `optional` | a line in the bundle's list |

**`mandatory` buys bold text and a better position.** `recommended` and
`optional` are currently indistinguishable in the output. That is not a bug in
the implementation — it is what the mechanism can express.

## Why inlining was rejected, which is the substance of it

The obvious stronger reading is that `mandatory` should mean *the content is in
context*, so `apply` should paste the document into `CLAUDE.md` rather than
linking it. Three things argue against it, and the first is the one that
matters:

**`CLAUDE.md` loads every session, and `mandatory` does not mean every
session.** It means *before work* — before work this document governs. Inlining
conflates the two, and the conflation is expensive in the direction nobody
notices: a project that adopts eight bundles pays for all eight mandatory
documents while doing something none of them touch. **The index is the more
faithful reading of the field, not the weaker one.**

**Measured, once.** The one `preload: mandatory` document in the estate —
`record-decision` — is 1,262 words. One bundle. That is affordable and it does
not stay affordable, and the ceiling arrives without warning because no author
sees the total.

**And the copy would drift.** Inlined content is a second copy of a vendored
copy, and nothing would check it against the source.

## What the finding actually is

**Either the ladder is doing less than it claims, or a harness with no
conditional-loading hook cannot express it.** Both readings are live and they
lead in different directions:

- *The ladder is over-specified.* `mandatory` versus the rest is the only
  distinction anything can act on, and `recommended` versus `optional` is
  advice to a human author dressed as a machine-readable field.
- *The harness is the limitation.* `SKILL.md` progressive disclosure loads a
  name and description at startup and a body on match, and there is no *this
  situation now applies, load these* hook in any harness. The field is right and
  nothing can honour it yet.

**Do not resolve this from the armchair.** The evidence that would settle it is
a project with enough adopted bundles that the mandatory set is genuinely
expensive — at which point either the levels start earning their keep, or the
answer is conditional loading and `preload` was never the mechanism.

## Related

[[routers]] — conditional loading, which is where the second reading leads.
[[bundle-routines]] — a named routine is a per-call loading path, which would
make this question moot by letting the caller choose rather than the author.
`conditional-preload` in `luma-leader` — the same field from the format's side.
