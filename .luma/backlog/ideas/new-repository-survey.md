---
type: idea
title: A survey of a new repository, capturing what drives how it gets used
created: { by: human:benlinton, at: 2026-08-17T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
lifecycle_status: draft
---

# A survey of a new repository, capturing what drives how it gets used

When setting up a new repo, capture infromation that will drive how it gets used
now and later. Ensure these are fluid and don't rot.

- greenfield vs brown field
- where are we in the design process
  - these ideas are locked in
  - this is all experimental and much of it may head in a different direction
- how established is this project
  - changes are expensive, change as little as possible
  - move fast and break things
- capture creates optimal change request output
  - for examplek: design (cheapest) < prototype < implementation < production (most expensive)
  - at what point does this change?
  - this might change by project
- how many users now, and how many intended
  - this tells us how much we can break for rapid development
- how critical is this system
- how sensitive are the users
- distribution of user expertise
- what is our intended test strategy
  - vs what is the reality
- what are the default user profiles
- what are your example names, addresses, etc so identifiable info doesn't leak in
- when is editing decisions not allowed (e.g. on the first day, it should be ok to edit a decision instead of taking on tech debt)

## Notes

Migrated from `docs/IDEAS.md` on 2026-08-21, verbatim including its typos.
`created.at` is a day-level estimate from git history.

**The project-level counterpart to an existing idea.** `luma-leader` holds
*A survey of how an organization is divided*
(`.luma/backlog/ideas/organization-division-survey.md`) — same shape, one level
up. This one is filed here because projects are what foreman runs inside.

**Two bullets already have homes**, and are kept in the list anyway because they
are questions this survey would ask:

- *how established is this project* is the subject of
  [[declared-maturity-and-behaviour]], filed in this repository. It covers
  declaring maturity and behaving differently in response, and notes that LKF's
  `lifecycle_status` already supplies the vocabulary.
- *what are your example names, addresses* is answered by the `luma/git-secrets`
  bundle's `configure-identity` workflow, step 5 — decide them at project start
  and record them in the project's policy.

**The other eleven have no home anywhere.** Cost-of-change by stage, user count
as a breakage budget, criticality, user sensitivity, expertise distribution,
intended versus actual test strategy, and when editing a decision stops being
acceptable are all uncaptured.

**"Ensure these are fluid and don't rot" is the hard part.** LKF's `stale_after`
is at least a mechanism to point at.
