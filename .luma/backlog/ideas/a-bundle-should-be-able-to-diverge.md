---
type: luma/idea
title: A bundle should be able to diverge from its catalog
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# A bundle should be able to diverge from its catalog

**Take a bundle, change how it works, and keep it** — under your own catalog, or
under no catalog at all. Today there is no way to do that on purpose.

## The state exists already, as a defect

`inspect --rule adoption` reports three states, and the first one is this idea
described as a failure:

> **edited** — somebody changed the vendored copy. Their change dies at the next
> `get`, and upstream never hears about it.

**So there are two sanctioned states: identical to upstream, or broken.** A
project that deliberately wants a different version of a bundle has nowhere to
stand — it either carries a permanent finding or abandons the change.

**Diverging is the sanctioned form of `edited`.** The check stops reporting it
because the receipt says the divergence was chosen.

## Recording upstream is the whole feature, and it is nearly free

**`adopted.toml` already holds what a return needs** — `source`, `commit`,
`version`, `checksum`:

```toml
["lumastack/luma-catalog/audit-records"]
version  = "0.7.2"
source   = "https://github.com/LumaStack/luma-catalog.git"
commit   = "8ec0cce285bb27f0b6c58bacb62d37bd62a702ee"
```

**Diverging keeps `source` and `commit` and changes what they mean**: from *this
is what we hold* to *this is where we left*. The checksum stops measuring
conformance to upstream and starts measuring nothing, or measures the fork.

**Returning is then `get --force` against the recorded source** — which is why
this is cheap to build and why it should be built even if nobody ever merges
anything back. **A direction you cannot abandon is not a direction, it is a
commitment**, and the record is what makes it the first thing.

## Two destinations, and the namespace work already handled one

**Into your own catalog.** This mostly works already: a catalog's namespace
derives from where it lives, so a fork published from a different repository
*gets its own namespace without anybody arranging it* and sits beside the
original in a project rather than colliding with it. `publish-to-the-catalog`
is the existing path.

**Into no catalog.** A bundle that is simply yours, local, unpublished. Nothing
supports this today and it is the more common case — most divergence is one
project wanting one rule different, not a project starting a catalog.

## What has to change

- **`get` must refuse to overwrite a diverged bundle**, or require an explicit
  re-take. Today `--force` overwrites a copy that was edited here, which is
  correct for accidental edits and wrong for deliberate ones.
- **`bundle outdated` has to say something honest.** A diverged bundle is not
  behind; it is elsewhere. *Upstream has moved* is useful; *you are out of date*
  is not.
- **The adoption check needs the fourth state.** `edited` becomes a finding only
  when nobody declared the divergence.

## Merging back is deferred, deliberately

**Not designed here, and possibly never built.** The record is worth having on
its own — returning to source is the cheap half and does not need a merge.

**If real demand appears**, `source` and `commit` are exactly what a three-way
merge would need, so building the record now costs nothing and leaves the door
open. *That is the whole argument for doing the near-free half early: it is the
half the expensive half would have required anyway.*

## What it does not solve

**A fork that never diverges is worse than no fork.** It stops taking upstream
improvements and gains nothing for it — and nothing here would detect that, since
a fork looks identical to a fork that changed everything.

**A fork that diverges far cannot really return**, record or no record. The
receipt makes the *source* recoverable, not the work of reconciling with it.

*Related:* `no-way-to-un-adopt` — the neighbouring gap. Both are ways of stopping
tracking upstream, and they differ only in whether the content stays.
