---
type: luma/idea
title: Report what an adoption costs before it loads
created: { by: agent:claude-opus-5, at: 2026-08-29T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: next
scope: project
stage: draft
---

# Report what an adoption costs before it loads

`get` adds a bundle and says nothing about what carrying it will cost. The
person adopting finds out later, or never — the cost lands on every session
afterwards and is invisible at the moment it is chosen.

**The number is computable before anything loads.** `matches` is declarative, so
a bundle's always-on documents can be counted the moment it is fetched. Nothing
has to run, and nothing has to be inferred.

## Where the number comes from

[[ADR-0001-apply-writes-adapters-not-copies]] measured it once, by hand: three
bundles, eleven documents, four of them always-on. **3,176 words if inlined
against 682 as an entry point.** That measurement is the whole reason the
decision is more than a rule that sounds good — and it exists because somebody
counted, once, and never again.

**A count nobody automated is a count that happened once.** The catalog has gone
from fifteen bundles to twenty-two since, and nothing recomputed anything.

## Why nobody has built it

`luma-leader/docs/adoption-use-cases.md:305` calls it *"the single highest-value
unbuilt item in this document"*, and gives the reason no prior art exists: **no
package manager reports this, because none has a budget to spend.** Disk is
free and context is not, so the analogy that usually helps here actively
misleads.

## What has to be decided

**What unit.** Words are what was measured and are harness-neutral. Tokens are
what actually gets charged and are model-specific. Reporting the wrong one
confidently is worse than reporting neither.

**Whether it counts what comes with it.** `bundle-dependencies` already
specifies the shape — *"Adopting A also brings B and C; four documents load up
front"* — so the transitive set is the honest number and the direct one is
misleading.

**Where it fires.** At `get`, which is when the choice is made and when it can
still be declined. Possibly also at `apply`, which is when the cost becomes
real. Both means the same fact is reported twice and they will disagree.

**Whether it is ever a refusal.** Almost certainly not — a budget nobody set
cannot be exceeded. Information, not a gate, until somebody asks for a gate.
