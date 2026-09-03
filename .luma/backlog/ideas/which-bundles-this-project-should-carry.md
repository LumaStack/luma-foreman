---
type: luma/idea
title: Which bundles this project should carry, and what decides it
created: { by: human:benlinton, at: 2026-08-27T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
stage: draft
---

# Which bundles this project should carry, and what decides it

**Seventeen of the catalog's nineteen bundles are adopted here, and that is
deliberate.** The open experiment is to keep adopting until it either stops
being convenient or does not. This asks whether it has, and finds that two do
not earn their place.

## Read by evidence, 2026-08-27

**Producing artifacts in this repository.** `decision-records` (5 ADRs),
`backlog-ideas` (27 ideas), `git-secrets`, `git-workflow`, `git-worktrees`,
`github-release`, `versioning`, `project-documentation`, `session-manager`. These
describe practice the repository actually follows.

**Reference for an implementer, which is a different relationship.**
`luma-types`, `luma-layout`, `luma-config`, `luma-tools`. Foreman does not
*follow* these, it *implements* them — `init` writes `type: luma/project`,
`inspect` enforces the layout. Still worth having in front of an agent, but not
for the reason `consumers` models, and worth noticing that the tool and the
bundle encode the same knowledge. The live question sitting under this: **will
anything ship natively in foreman, or is everything fetched?** It decides
whether logging, for one, is a bundle.

**`luma-maintainers` belongs here** — foreman is in the estate — **and is
mis-tagged upstream** as `consumers: [organization]` while its own body says
estate repositories adopt it. A `luma-catalog` fix, not a foreman one.

**Weak.**

- **`bundle-manager`** — one of its six documents is relevant here
  (`organizing-a-bundle`, which `inspect` enforces). The other five are workflows
  for creating, updating, deleting, migrating and repairing bundles, which is
  catalog-side work that does not happen in this repository.
- **`token-manager`** — two workflows, both for measuring or teaching somebody
  else's setup. Token management is something foreman should eventually
  *build*, which makes this a design input rather than a practice the repository
  keeps. It has produced nothing.

**Marginal: `audit-records`.** `.luma/records/` holds only `decisions/` — no
audit has been conducted here. `inspect` produces findings and one is plausible
soon, so keep and revisit rather than drop.

## The cost argument is real and temporary

At seventeen bundles: `CLAUDE.md` is 21,646 characters loaded every session, and
40 skills load their names and descriptions at startup.

**But most of that disappears under
[[apply-writes-an-entry-point-not-an-index]]**, which makes standing cost
per-bundle rather than per-document. Afterwards, carrying a bundle nobody opens
costs roughly one line.

**So the case for dropping these two rests on relevance, not on cost**, and it
should be argued that way or not at all. If the only reason is the token bill,
wait for the redesign and the reason evaporates. What survives is that five
workflows for authoring bundles and two for auditing somebody's token setup are
not things this repository does.

## What this exposes, which is the more useful half

**Both drop candidates are correctly `consumers: [project, organization]`.** They
would function here. They are simply not worth carrying — and **`consumers`
cannot express that, in any spelling.**

Three distinct questions wear one field today:

| | question | mechanism |
| --- | --- | --- |
| **floor** | would this even function in a repository like mine? | `consumers` |
| **fence** | is this mine to take, or somebody's internals? | none — `luma-maintainers` abused `consumers` for it |
| **selection** | of what fits and is mine, what do I want in front of me? | **none, and it is the adopter's judgement** |

`the-estate` already records the third: *"What is missing is the adopter's own
selection — a bundle-level answer to which of these do I want in front of me,
which nothing in the format provides."* This is that gap met from the consuming
side rather than the publishing side.

**Do not invent a mechanism for selection here.** It is a judgement exercised per
repository, and the useful step is recording the judgement, not automating it.

## Practical

Dropping a bundle is not a clean operation — [[no-way-to-un-adopt]]. Today it
means deleting the directory, hand-editing `adopted.toml` whose header says not
to, then running `apply`, which does correctly remove the orphaned skills.

## The question underneath: does foreman consume the catalog it serves?

**Foreman already records its own decisions through a bundle it took from the
catalog.** If its release process, its versioning rules and its prose
conventions go the same way, **foreman becomes a consumer of the catalog it was
built to serve.**

**Elegant, or a permanent headache for whoever maintains both ends?** Nobody
knows, and the way to find out is the experiment above — keep adopting until it
either stops being convenient or does not.

**It is the same question as *ship natively or fetch everything*, from the other
side.** One asks what foreman takes, the other what it carries; both are settled
by the same answer, and neither is settled yet. [[distribution-beyond-clone-and-symlink]]
depends on it, because a release process that lives in a bundle is a release
process foreman has to adopt before it can cut a release.

## Notes

**Absorbed from `docs/scope.md`** when that document was scattered on
2026-08-29. It had held the standards question and this entry had only cited it.

**Sequencing.** This is independent of the loading redesign and can happen before
or after it. If after, re-read the weak two on relevance alone, since the cost
half of the argument will be gone.

**A repository still cannot say what kind of consumer it is**, so none of the
floor question is enforceable yet from either side. Recorded in `luma-leader`.
