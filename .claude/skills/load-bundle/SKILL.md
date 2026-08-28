---
name: load-bundle
description: Open one adopted bundle and see what it holds — its rules, what fires each one, and anything that applies throughout it. Use when a bundle's line looks relevant, or when asked to load a bundle by name.
---

<!-- luma-foreman:generated navigation. Regenerate with `luma-foreman apply`; edits are lost. -->

# Open a bundle

**Every adopted bundle and the exact path to its ring:**

- `lumastack/luma-catalog/audit-records` — Audits as records — findings written by one party, answered by another, closed by the first. The whole exchange lives in git.
  `.luma/bundles/rings/lumastack/luma-catalog/audit-records.md`
- `lumastack/luma-catalog/backlog-ideas` — Ideas as individual files rather than one growing IDEAS.md — what earns a file, how capture stays fast, and how the list gets tended rather than accumulating.
  `.luma/bundles/rings/lumastack/luma-catalog/backlog-ideas.md`
- `lumastack/luma-catalog/bundle-manager` — Creating, updating, auditing, repairing, migrating and retiring bundles — the layout they use and which catalog they belong in.
  `.luma/bundles/rings/lumastack/luma-catalog/bundle-manager.md`
- `lumastack/luma-catalog/decision-records` — Decisions recorded with their reasoning, deferred alternatives, and re-open triggers. Spent decisions are archived rather than deleted.
  `.luma/bundles/rings/lumastack/luma-catalog/decision-records.md`
- `lumastack/luma-catalog/git-secrets` — Keeping credentials and private identity out of a repository — names, personal addresses, home paths, machine names, tokens and key files. Prevention first, then audit.
  `.luma/bundles/rings/lumastack/luma-catalog/git-secrets.md`
- `lumastack/luma-catalog/git-workflow` — How changes get integrated — merge commits rather than squash or rebase, and the repository settings that make it true.
  `.luma/bundles/rings/lumastack/luma-catalog/git-workflow.md`
- `lumastack/luma-catalog/git-worktrees` — Isolated worktrees for concurrent agents in one repository — where they live, what has to be provisioned, and how to tear them down without leaving wreckage.
  `.luma/bundles/rings/lumastack/luma-catalog/git-worktrees.md`
- `lumastack/luma-catalog/github-release` — Cutting and publishing GitHub releases — choosing the version, the changelog, release titles and contents, and the gh workflow.
  `.luma/bundles/rings/lumastack/luma-catalog/github-release.md`
- `lumastack/luma-catalog/luma-config` — Where luma configuration lives, what is committed and what belongs to the machine, and the order in which layers win.
  `.luma/bundles/rings/lumastack/luma-catalog/luma-config.md`
- `lumastack/luma-catalog/luma-layout` — The .luma directory every luma tool writes into — the four tiers, what belongs in each, and the committed-only invariant that makes it trustworthy.
  `.luma/bundles/rings/lumastack/luma-catalog/luma-layout.md`
- `lumastack/luma-catalog/luma-maintainers` — Working on the luma tools themselves — the repositories and the boundary each defends, publishing to the universal catalog, and changing a type without making every tool upgrade at once.
  `.luma/bundles/rings/lumastack/luma-catalog/luma-maintainers.md`
- `lumastack/luma-catalog/luma-tools` — Using the luma tools — which one does what, getting them onto a machine, standing a project up, and the get-then-apply loop that puts knowledge in front of an agent.
  `.luma/bundles/rings/lumastack/luma-catalog/luma-tools.md`
- `lumastack/luma-catalog/luma-types` — The type definitions more than one luma tool has to agree on — namespaced, vendored, and deliberately not built into the knowledge format.
  `.luma/bundles/rings/lumastack/luma-catalog/luma-types.md`
- `lumastack/luma-catalog/project-documentation` — The prose a repository publishes — where it lives, what a README is for, and which documents are worth having at all.
  `.luma/bundles/rings/lumastack/luma-catalog/project-documentation.md`
- `lumastack/luma-catalog/session-manager` — Ending an agent session without losing what it learned — checkpoint while working, hand off to a successor, or close for good, each writing for a different reader.
  `.luma/bundles/rings/lumastack/luma-catalog/session-manager.md`
- `lumastack/luma-catalog/token-manager` — Where an agent session's tokens actually go — a paced tutorial on the mechanism and the fixes that follow from it, and an audit that measures a real setup instead of guessing at it.
  `.luma/bundles/rings/lumastack/luma-catalog/token-manager.md`
- `lumastack/luma-catalog/versioning` — What a version number promises, when to bump which part, and the rules that get decided wrongly — for anything versioned, not only releases.
  `.luma/bundles/rings/lumastack/luma-catalog/versioning.md`

Read the path beside the one you want. Nothing needs assembling — a bundle ID
carries its namespace, and guessing at one is how this fails.

If the name you were given is not above, `.luma/bundles/entrypoint.md` is the current list; this copy
is generated and can be behind it.

**What you get.** Anything the bundle says applies throughout it, to read now;
then every rule it holds, with what fires each. **Bodies are not included** —
open the ones that match the work, and not the rest.

**If the path does not exist**, the bundle is not adopted here. That is an
answer, not an error.
