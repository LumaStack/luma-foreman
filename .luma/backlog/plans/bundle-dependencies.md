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

## What a split is for, now that rings exist

**The token argument is mostly gone and the reasoning has not caught up.** A
bundle used to cost its documents in every session. Under rings it costs **one
line** until something opens it. So *split it to keep the common case light* is
now a much weaker reason than it was when the bundles were first cut.

**Three reasons survive, and they are about people rather than bytes:**

| | the test |
| --- | --- |
| **condition** | does this apply to everyone, or only to people doing a particular thing? |
| **audience** | who opens it, and are they doing the same job? |
| **replaceability** | would somebody swap out this part alone and keep the rest? |

**One bundle, one condition, one audience.** That is the rule this estate has
been reaching for and has not written down.

**Options inside a bundle are the smell.** *Use it this way, or that way* is
usually two conditions wearing one manifest — and it forces every reader of the
common case to skim past the uncommon one to be sure it does not apply to them.

**A fourth reason is ours alone:** what is specific to this estate should not
leak into a bundle other people might take. That is not a split criterion so
much as a placement one, and `where-a-bundle-belongs` already owns it.

## Decision: `git-workflow` and `git-worktrees` stay separate

**Recommended, and not for the reason they were first split.**

**Everyone integrates changes. Only some people run concurrent agents in
worktrees.** That is one condition versus another, not one depth versus another
— and a bundle whose condition never fires costs a line under rings, which is
the cheapest possible way to be irrelevant.

**Collapsing them would force the common reader past worktree provisioning,
teardown and recovery** to reach a rule about merge commits. **The heavy half
would be paid by everyone in attention, which rings do not fix.**

**And they are separately replaceable.** An organization with its own worktree
conventions swaps one bundle and keeps the other. Merged, it would have to fork
the pair.

*The coupling that already exists is a citation, not a dependency:
`proving-work-landed` mentions `git worktree list` and sends the reader to
`git-worktrees` for what to do about it. **A bundle that names another for depth
is fine; one that needs another to function is the case this plan is about.***

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
