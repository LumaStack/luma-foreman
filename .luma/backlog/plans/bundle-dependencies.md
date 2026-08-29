---
type: document
title: Splitting bundles, and letting one declare it needs another
description: Why review-sweeps needs git-workflow, what a bundle split is actually for now that rings exist, and the order to build declared dependencies in — with what is already designed and what is still open.
lifecycle: draft
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
modified: { by: agent:claude-opus-5, at: 2026-08-29T00:00:00Z }
---

# Splitting bundles, and letting one declare it needs another

**This is a plan, not a design.** The design exists —
`luma-leader/docs/bundle-dependencies.md` — flat resolution, one version, no
nesting, and long. **Nothing here restates it.** What is here is why the
question became live, what to decide before building, and the order to build in.

## Why now

**`review-sweeps` 0.28.0 put git commands in a sweep workflow.** They belonged
in `git-workflow`, which is now their source of truth — and the moment that
moved, `review-sweeps` became a bundle whose workflow **does not work** unless
the reader also has `git-workflow`.

**Today it cites prose and hopes.** `luma-directory-layout` names the limit
plainly: *"a bundle citing this policy is citing prose — there is no resolver,
and adopting this bundle is not required to act on the sentence."* It says that
is tolerable **exactly while every bundle agrees on the default**, and that the
first project to disagree is the trigger.

**A cited bundle nobody adopted is that disagreement**, arriving from the other
direction.

**And ADR-0002 predicted it.** Its `reopen_trigger` reads: *"Bundle dependencies
are adopted as a design, at which point something has to decide what a bundle's
declared needs mean at `get` time."* **That has now happened.** The ADR is not
wrong yet — adoption still copies and resolves nothing — but its re-open
condition has fired and it should be revisited rather than left looking settled.

## What a split is for, now that rings exist — measured, not assumed

**The token argument does not survive measurement.** Merging `git-worktrees`
into `git-workflow` would save one entrypoint line and cost one ring line, and
the workflows become skills either way, so what loads at startup is identical.
**Net zero.**

| | merged | separate |
| --- | --- | --- |
| entrypoint lines | 1 | 2 |
| `git-workflow` ring lines | 3 | 2 |
| skills at startup | 5 | 5 |

**And *it forces readers to skim past the uncommon half* is also wrong.**
`matches` gates at the document, not the bundle: a reader who never works in a
worktree never opens that document whether it sits in one bundle or two. **The
attention argument was answered before it was made.**

*Both were asserted here before being checked. They are left in the record
rather than deleted, because a plan that shows only its surviving reasons
teaches nobody which ones to distrust.*

### What actually survives

**Independent versioning, and it is the one with evidence.** `git-worktrees` has
moved through `0.6.x` while `git-workflow` sat at `0.5.2`. **Merged, every
worktree fix bumps the bundle carrying the merge-commit policy**, and every
adopter re-adopts for a change they do not care about. In an estate that moved
nine bundle versions in a day, that is a recurring cost rather than a
hypothetical one.

**Replaceability, which is real and rare.** An organization with its own
worktree conventions swaps one bundle. Merged, it forks the pair to keep the
half it wanted.

**And placement, which is not a split rule at all** — what is specific to this
estate should not leak into a bundle other people might take.
`where-a-bundle-belongs` owns that.

### So the rule is narrower than it looked

**Split when the two parts will version independently, or when somebody would
plausibly replace one and keep the other.** Not for tokens, and not for
attention — **rings and `matches` already handle both.**

**Many workflows are not the smell.** `git-worktrees` has four — create, remove,
recover, repair — and `review-sweeps` has three. They are moments in one job,
and a reader doing that job reaches most of them.

**The audience question survives as a hint, not a rule.** A bundle whose halves
are read by different people usually *also* versions independently and *is*
separately replaceable — **the audience is the tell, and versioning is the
reason.**

*Some of this would matter less if [[routers]] existed — conditional loading
would gate by situation rather than by how the manifests were cut. **The fork
rule is partly a workaround for a mechanism that does not exist yet**, and it
should weaken if that one ships.*

## A dependency is never conditional on the reader

**This is the constraint that stops the audience rule turning into a
combinatorial mess**, and it needs writing down before anything is built.

**A bundle declares what it needs to do its own job.** Not what its reader might
also want, and not what would be useful if they happen to work a particular way.

**`review-sweeps` needs `git-workflow`** because its workflow cites
`proving-work-landed` and **every sweep lands a record.** Unconditional.

**It does not need `git-worktrees`**, even for a reader who runs sweeps in
worktrees — **the sweep does not require worktrees to function.** That reader
wants `git-worktrees` for reasons of their own, which is a different sentence.

**So the test is: does the bundle stop working without it?**

| | |
| --- | --- |
| **stops working** | a dependency. Declare it |
| **works, and would be better** | a **recommendation** — and it belongs to the adopter's selection, not to this bundle |

**If it varies by reader, it is not a dependency.** That is the whole answer to
*what happens when my dependencies fork by audience*: **they do not.** A forked
dependency is a recommendation that has been mislabelled, and labelling it
correctly removes the fork.

**`which-bundles-this-project-should-carry` already owns the other half** — *of
what fits and is mine, what do I want in front of me* — and names it as the
adopter's judgement with no mechanism. **That is the right place for it and it
should stay unmechanised**; a bundle recommending bundles is how a dependency
graph grows conditions.

### The chain stays flat because citation is not dependency

`review-sweeps` → **needs** → `git-workflow` → **cites for depth** →
`git-worktrees`.

**The second arrow is not a dependency and must never become one.**
`proving-work-landed` mentions `git worktree list` and sends the reader to
`git-worktrees` for what to do about it — **a reader with no worktrees reads that
line and moves on.** Nothing is missing for them.

**Flat, and one level, is not a simplification here — it is the property that
keeps this tractable**, and it is what the design in `luma-leader` already
chose.

### If a bundle needs *either* A *or* B

**It does not.** A bundle that would accept either of two others needs something
neither provides — an interface, a shape, a guarantee — and **has no way to say
so.**

**Declare nothing and cite both.** An *or* dependency is where resolvers grow
the machinery this estate has twice decided not to build.

## What to decide before building

**1. What the field is called and what it means.** `depends_on`, `requires`,
`needs` — and whether it means *fetch this too* or *warn if it is absent*.
**Start at the weakest thing that helps**: `get` prints what else is needed and
adopts nothing. That is `bundles-declare-what-they-work-with`'s proposal and it
reverses no decision.

**2. Whether `get` ever fetches transitively.** The design says a dependency is
transitive adoption. **ADR-0002 says adoption copies and resolves nothing.**
These conflict, and the conflict is the actual decision — not the field name.

**3. What a missing dependency does to `inspect`.** A finding, a notice, or
nothing. **Probably a notice**: the project may have the knowledge by another
route, and `inspect` cannot tell.

**4. Whether the catalog's `requires` is the same mechanism.** `CATALOG.md`
already declares one — `git-secrets`, recommended — and **nothing in
`src/foreman/` reads it.** Two fields for one idea is the defect this estate
keeps finding; decide whether the bundle-level field replaces it, feeds it, or
sits beside it with a stated difference.

## Order to build in

1. **Revisit ADR-0002** — its trigger has fired. Either it holds and this stays
   declaration-only, or it is superseded and something resolves. **Nothing else
   here can be decided while that is open.**
2. **Add the field to `bundle-manager`'s `organizing-a-bundle`**, declaration
   only, with `review-sweeps` → `git-workflow` as the first and only user.
3. **Make `get` print it.** No fetching. One line: *this bundle expects
   `lumastack/luma-catalog/git-workflow`; you do not have it.*
4. **Make `inspect` notice it**, so the gap is visible after adoption rather
   than only during it.
5. **Then, and only then**, ask whether transitive fetching is worth it. By that
   point there will be evidence about how often the printed line is ignored.

## What is already written, and where

| | |
| --- | --- |
| the design | `luma-leader/docs/bundle-dependencies.md` — flat, one version, no nesting, resolution at a catalog snapshot |
| the decision it reverses | `.luma/records/decisions/ADR-0002-adoption-copies-and-never-resolves.md` |
| the weakest first step | `.luma/backlog/ideas/bundles-declare-what-they-work-with.md` |
| the types half of the same question | `luma-leader/.luma/backlog/ideas/bundle-declares-the-types-it-uses.md` |
| why prose citation is tolerable, and until when | `luma-layout`'s `luma-directory-layout`, *The limit, and it is not solved here* |

## Open, and not resolved here

**Whether the splitting rule belongs in `bundle-manager`.** It is a rule about
what a bundle is, which is that bundle's subject — but it was derived here from
a live case, and writing it before a second case would be guessing.

**Whether `review-sweeps` should have been split at all**, rather than
`git-workflow` growing a policy. It went the way it did because how git works is
not a sweep's business; the same argument will recur every time a bundle needs
something general.
