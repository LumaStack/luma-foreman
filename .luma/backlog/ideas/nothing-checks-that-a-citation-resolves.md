---
type: luma/idea
title: Nothing checks that a citation resolves
created: { by: agent:claude-opus-5, at: 2026-08-29T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: next
scope: project
stage: draft
---

# Nothing checks that a citation resolves

A document in this repository can cite a bundle, a policy, another record or an
idea, and **nothing verifies that the thing it names exists.** A citation that
resolves to nothing throws no error, changes no behaviour, and leaves the
document looking exactly as authoritative as one that is correct.

## Where it bit

`ADR-0001` cited **`luma/bundle-manager`** — a namespace this repository has
never had. It survived the 2026-08-26 rename that moved everything to
`lumastack/luma-catalog/`, went through six estate-wide sweeps untouched, and
was found by a person reading the file in a review, not by anything running.

**It is the same silent-by-construction shape as the XDG path defect**: a wrong
path nobody writes to works perfectly, because nothing notices the right one is
empty.

## What it would check

Tracked prose outside `.luma/bundles/`, since a vendored copy is audited
upstream:

- **`[[wikilinks]]`** — resolves to a tracked file somewhere it could plausibly
  live. `ADR-0004` links `[[ADR-0001-apply-writes-adapters-not-copies]]`; an
  idea links `[[report-what-an-adoption-costs]]`.
- **bundle ids** — `lumastack/luma-catalog/bundle-manager` is a directory under
  `.luma/bundles/` or an entry in `adopted.toml`.
- **bundle-relative document ids** — `policy/an-index-of-what-exists` exists
  inside the bundle named alongside it.

**Both halves are already structured**, so this is a path existence test rather
than a parse. `adopted.toml` and the vendored tree are keyed on exactly these
ids.

## Pinning and checking solve different halves

**An external citation should be pinned, and then it cannot rot at all.**
`ADR-0001` now links `policy/an-index-of-what-exists` at the catalog commit it
was read at. The bundle can be renamed, restructured or retired and the link
still resolves to the text the decision was taken against. **A pinned reference
needs no checker, because its target is immutable.**

**An internal link cannot be pinned, which is what leaves work for a rule.**
`[[ADR-0001-apply-writes-adapters-not-copies]]` points at a live file in this
repository that is expected to move and change; pinning it to a commit would
defeat the purpose. Bundle ids and bundle-relative document ids are the same —
they name what this project carries *now*.

**So the rule's job is narrower than it first looked**: verify the links that
point at living things here, and verify that a citation reaching outside this
repository is pinned rather than dangling.

*This section previously argued that pinning was the wrong fix, on the grounds
that `adopted.toml` already records a commit. That was wrong. `adopted.toml`
records what the project carries today and changes on every `get`; a reference
records what was read when a decision was taken. Two different facts.*

## What has to be decided

**Finding or notice.** A dangling wikilink is unambiguous and should probably
fail. A bundle id that does not resolve may be a deliberate reference to
something not adopted here, which is a judgement and belongs as a notice.

**Whether it reaches across repositories.** `ADR-0001` cited
`luma-leader/docs/adoption-use-cases.md` at one point — unverifiable from
inside this repository, and no rule should pretend otherwise. **Out of reach is
a category, not a failure.**

**Whether records get stricter treatment.** A record is cited as authority long
after it stops being edited, so a dangling link costs more there than in an
idea that is still being argued.
