---
type: luma/idea
title: Bundles should carry their own licences, and licences they inherited
created: { by: human:luma-foundry, at: 2026-09-10T06:38:27Z }
contributors: [human:luma-foundry, agent:claude-opus-5]
scope: project
stage: draft
---

# Bundles should carry their own licences, and licences they inherited

**Bundles should be able to carry their own licences, and licences they
inherited.**

Split from [[classify-bundle-contents]], where it is one item in a larger list.

## The problem it addresses

**Adoption is redistribution.** `foreman get` copies a bundle's directory into
another repository, so anything vendored under somebody else's licence lands
there too — with its attribution duty — in a repository whose licence nobody
checked and whose owner was never asked. Today the only thing that can say so is
prose in `BUNDLE.md`, which nothing reads and nothing checks.

**And a bundle currently inherits its licence from whatever repository it
happens to sit in.** That is right for a catalog where everything is one licence
and wrong the moment a bundle travels: the adopting repository's `LICENSE` says
nothing true about a vendored directory that came from somewhere else.

## Notes

**Downstream of `what-a-bundle-may-carry`**, added to
`lumastack/luma-catalog/bundle-manager` at `0.16.0`. That policy makes *carry
only what you wrote, point at everything else* the default, partly because
nothing can currently express the alternative safely. **A licence declaration is
what would make the other routes usable** rather than merely permitted.

**The pairing matters more than either half.** *This bundle is Apache-2.0* and
*this directory inside it is CC BY 4.0, attributed to X, modified* are different
claims, and an adopter needs both. A single licence field that cannot express
the second is close to useless — the second is the one that creates an
obligation the adopter did not choose.

**What it could enable**, roughly in order of value:

- a check that refuses to publish a bundle carrying material whose licence it
  never declared
- an adopter warned at `foreman get` that this bundle brings obligations with it
- a generated attribution file, instead of a hand-kept `NOTICE`
- a catalog able to answer *what am I distributing, and under what terms*

**Open:** whether the inherited-licence declaration belongs on the bundle
manifest, on each vendored document, or on a `sources`-style pointer. The third
is attractive, because a pointer already has to name a URL and a licence is the
other thing worth knowing about a URL.
