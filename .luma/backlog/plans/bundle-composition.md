---
type: document
title: How bundles compose
description: Three layers where there is currently one — distribution, composition, delivery — with capabilities as the composition currency, additive providers instead of conditional dependencies, and what foreman does about it.
lifecycle: draft
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
modified: { by: agent:claude-opus-5, at: 2026-08-29T00:00:00Z }
---

# How bundles compose

**A design, written forward.** It replaces an earlier plan on this file that
worked backwards from what exists; that reasoning is in the history and is not
carried here.

## The problem: one boundary is doing three jobs

**"Bundle" currently means all of these at once**, which is why deciding where to
cut one is so hard — every cut is three decisions taken together and only one of
them is usually being thought about.

| job | decides |
| --- | --- |
| **distribution** | what is fetched, versioned, checksummed, replaced |
| **composition** | what builds on what |
| **delivery** | what reaches an agent, and when |

**Package managers conflate the first two and get away with it**, because code
has a call graph and a compiler that fails loudly. **Knowledge has neither.**

**And the third has no analogue in software distribution at all.** A library
never has to arrive *at the right moment*. Knowledge does, and that is the
requirement most of this design exists to serve.

## The design: separate them

| layer | unit | declares | evaluated |
| --- | --- | --- | --- |
| **distribution** | bundle | version, origin, checksum | at fetch |
| **composition** | document | `needs: [capability]` | when that document is delivered |
| **delivery** | document | `matches: [condition]` | continuously |

**`provides: [capability]` is declared per document.** A bundle's capabilities
are the union of its documents' — **derived, never written twice.**

### What each separation buys

**Splitting or merging a bundle becomes purely a distribution decision.**
Versioning cadence, ownership, replaceability. **It has no effect on composition
or delivery**, so it stops being a design question and becomes an operational
one.

*Measured on 2026-08-29, and it is why this holds*: merging two adjacent bundles
moved one line from an entrypoint to a ring and left the startup cost identical.
**Packaging is not where the cost is**, so packaging should not be where the
thinking goes.

**Needs are per-document and lazy.** A need fires only when its document is
delivered. **An unsatisfied need is therefore not a project-wide error** — it is
*this document assumes X, and nothing here provides it*, said at the moment it
matters and to somebody who can act on it.

**Delivery is already solved and should absorb every condition.** `matches`
decides what arrives. Nothing else in the system should grow a condition, ever.

## Capabilities, not bundle names

```yaml
# git-workflow/policy/proving-work-landed.md
provides: [integration-policy]

# review-sweeps/workflows/review-next.md
needs: [integration-policy]
```

**A named dependency defeats replacement.** If `review-sweeps` needs
`lumastack/luma-catalog/git-workflow` by name, swapping in your own git bundle
breaks it and you fork the sweep too. **Anything providing `integration-policy`
satisfies it** — ours, yours, a fork, a competitor's.

**No version resolution, ever.** You have a provider or you do not. No ranges,
no graph, no solver — the machinery that drags in a package manager never
arrives.

**And *needs A or B* was never a real case.** It only looked like one because
dependencies named bundles. **Two providers of one capability is the normal
state, not a conflict.**

## Providers are additive, which is what removes conditionality

**More providers means more coverage.** This is the piece that makes conditional
dependencies unnecessary rather than merely discouraged.

```yaml
# git-workflow/policy/proving-work-landed.md
provides: [integration-policy]
matches:
  - topic: checking whether work has landed

# git-worktrees/policy/landing-work-from-a-worktree.md
provides: [integration-policy]
matches:
  - topic: checking whether work has landed
  - path: .git/worktrees/**
```

**Neither depends on the other.** A reader with only `git-workflow` gets the
single-checkout check, **which is complete and correct for them.** A reader with
both gets the worktree coverage composed on top, delivered by its own `matches`.

| you have | delivered | |
| --- | --- | --- |
| `git-workflow` | the single-checkout check | complete for you |
| both | both documents | coverage composes |
| neither | nothing | `needs` unsatisfied — a real finding |

**Nobody fetches something they will not use, and nothing is declared
conditionally.**

## A bundle may ship its own fallback, which anything better replaces

**A bundle that needs a capability may also provide a minimal version of it**, so
it works alone and gets better when composed.

```yaml
# review-sweeps/policy/landing-a-slice-record.md
provides: [integration-policy]
fallback: true
matches:
  - topic: checking whether work has landed
```

**Enough to function, and deliberately thin** — for a sweep, *the record is
committed and pushed, and you have shown that it is.* No branch model, no forge,
no worktrees. **Adopt `git-workflow` and the real one takes over.**

### Two rules make this unambiguous

**A fallback yields to any non-fallback provider.** Where a real provider
exists, the fallback is not delivered at all — **not stacked, not appended.**
That is the one place providers are exclusive rather than additive, and it is
what makes *replaceable* mean something.

**A fallback satisfies only needs inside its own bundle.** `review-sweeps`'
fallback answers `review-sweeps`' need and nothing else's. **This removes the
ambiguity of two bundles each shipping a fallback** — they never compete,
because they were never candidates for the same need.

### What it changes

**A bundle is never broken out of the box.** Adopt one thing, it works. Adopt
more, it improves. **Nobody is required to assemble a working set** before
getting value.

**And it makes declaring a need safe.** The cite-when-unsure asymmetry above
exists because an over-declared need cries wolf — **a bundle that ships a
fallback cannot cry wolf**, because the need is satisfied from the moment it is
adopted. **Where you can write a thin fallback, declare the need.**

*A fallback is a real document with a real `matches`, not a stub. If it cannot
be written honestly and briefly, that is a sign the capability is too coarse or
does not belong to this bundle at all.*

## A conditional need is a document that has not been split

**Conditions have a home already.** Three cases, and only one is a need:

| | |
| --- | --- |
| **the document does not work without it** | `needs` — unconditional |
| **it works, and a reader in situation X would want more** | **a citation**, not a need |
| **half of it assumes X** | **split the document**; each half's need is unconditional |

**`needs` stays a flat list of strings, and that is load-bearing.** The moment it
takes objects with conditions it is a condition language, and **two condition
languages in one system is one too many.**

### When you cannot tell, cite

**The costs are not symmetric.**

- **A citation that should have been a need**: a reader follows a pointer and
  finds nothing, once. Visible, cheap, self-correcting.
- **A need that should have been a citation**: the checker reports a gap that is
  not one, forever. **Invisible damage — it teaches people to distrust the
  check**, and the next real finding is waved through.

**Cite when unsure. Promote to a need when something actually breaks without
it.**

## What foreman does, and does not

**`get`** — prints unsatisfied needs. **Fetches nothing.**

**`inspect`** — reports an unsatisfied need. A finding rather than a notice: it
is mechanically checkable and it is a real gap. **A need covered by its own
bundle's fallback is satisfied and reported as nothing** — but `inspect` may say
so once, quietly, since *working on the fallback* is worth knowing when a better
provider exists in a catalog.

**Nothing else.** No resolution, no transitive fetching, no lockfile.

```
NOTICE  review-sweeps needs `integration-policy`
        no adopted bundle provides it
        providers in lumastack/luma-catalog: git-workflow, git-worktrees
```

**When a need is satisfied it says nothing.** One provider is enough.

## Invariants

**No transitive fetching, ever.** Declaring is not acquiring. The moment `get`
pulls a second thing there is a resolver, and everything that follows.

**Every declaration is mechanically checkable.** `provides`, `needs`, `matches`.
**Nothing prose-only**, because prose-only is what rots without reporting.

**Derived is never declared twice.** A bundle's capabilities come from its
documents. One record.

**A fallback is never a second copy of a real provider.** It is thinner on
purpose. If it drifts toward being a copy, the bundle is holding knowledge that
belongs elsewhere.

## The honest gap

**A reader who uses worktrees and does not have `git-worktrees` is told
nothing.** `matches: path: .git/worktrees/**` cannot fire from a bundle they do
not have. **You cannot be told about knowledge you do not possess.**

**Leave it.** It is the ordinary condition of not having something, and browsing
a catalog is where that is discovered.

**The real fix, if it ever bites: the project declares its own situation** —
`uses: [worktrees]` — and capability checks become project-aware. **Conditions
about the reader belong to the project, never to a bundle.** Not built, because
it is a second declaration surface and the gap has not cost anything yet.

## Open

**Does a capability name a subject or a guarantee?** `integration-policy` versus
`can-answer-whether-work-landed`. **Subjects are easier to name, vaguer, and
few. Guarantees are precise and multiply.** Start with subjects; let a real
mismatch force the change.

**How coarse is a capability?** The working rule: **the size of a bundle, not the
size of a document.** Needing a fine-grained one is a signal the bundle is cut
wrong.

**Who governs the vocabulary?** It is a shared namespace and that is the real
cost of this design — the part that rots if nobody owns it.

## Build order

1. **`provides`, `needs` and `fallback` in the format**, as optional fields on a
   Document. Declaration only, nothing reads them.
2. **`review-sweeps` and `git-workflow` declare the first pair**, since the
   citation already exists and would become the first real case.
3. **`inspect` reports unsatisfied needs.** This is the whole payoff — the point
   at which a gap becomes visible without anybody remembering to look.
4. **`get` prints them at adoption**, so the gap is visible earlier than the
   next `inspect`.
5. **Stop.** Revisit only if something the design forbids turns out to be
   needed.
