---
type: luma/idea
title: The curator's word-count column reads a keyword the catalog retired
created: { by: agent:claude-opus-5, at: 2026-09-06T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: next
scope: project
stage: draft
---

# The curator's word-count column reads a keyword the catalog retired

**Belongs to `luma-catalog-curator`, parked here until it can be moved.** That
repository has no backlog directory, so nothing there knows about this.

**`luma-catalog-curator report` prints the number its README says the tool
exists to produce, and that number is now zero for every bundle.** The column
sums the documents a bundle loads unconditionally, keyed on the trigger keyword
`always` — which the catalog migrated off in favour of `eager`. Nothing in
`luma-catalog` declares the old spelling any more, so every row reads `0`.

The README calls that column *"the number this tool exists to produce"* —
what a bundle costs an adopter in every session, the asymmetry a
publisher-side tool exists to expose because an adopter cannot see it before
adopting.

## Why it is worse than a wrong number

**It prints "Zero is the expected reading" underneath.** So the output
explains away its own failure, and a reader with no reason to doubt it is told
the silence is correct.

That is the failure mode the curator's own commit history argues against — a
check that stops finding things cannot be told from one that passes. Here the
tool goes further and reassures.

## The fix

Read `eager`, and keep `always` beside it for bundles published before the
rename — the same tolerance `foreman` carries for the identical reason, and
recorded there as something to retire only once the estate has re-adopted. See
[[retire-the-migration-tolerances]].

## Also, while in that repository

**Its own adopted bundles are stale** — vendored under the old `luma/`
namespace, with `workflows/` rather than `procedure/` and an `adopted.toml`
rather than a `MANIFEST.md`. So the curator repository is not currently reading
the boundary policy that describes it. A re-adopt would fix both, and is
probably one sitting's work with this.

## Notes

Found while building `publish`, and recorded until now only in an appendix to
`.luma/backlog/plans/bundle-publish.md`.
