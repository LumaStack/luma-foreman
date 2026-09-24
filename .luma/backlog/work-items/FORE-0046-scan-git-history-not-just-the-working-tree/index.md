---
type: work-item
key: FORE-0046
title: Scan git history, not just the working tree
workflow_status: captured
rank: 010.0450.000
kind: idea
stage: draft
created: {by: 'human:luma-founder', at: '2026-08-09T00:00:00'}
description: A secret committed and deleted a month later is still published, and that is where most real leaks live. Nothing here scans it. A clean working tree implies an answer the check cannot give. The `git-secrets` bundle says so plainly rather than letting the silence be read as nothing found, which is the right stance and not a substitute for the capability.
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:47Z'}
---

# Scan git history, not just the working tree

A secret committed and deleted a month later is still published, and that is
where most real leaks live. Nothing here scans it.

## The problem it addresses

A clean working tree implies an answer the check cannot give. The `git-secrets`
bundle says so plainly rather than letting the silence be read as *nothing
found*, which is the right stance and not a substitute for the capability.

## Notes

Raised during the migration of `docs/IDEAS.md`, not part of the original entry:

- `inspect`'s `identity` rule already reads history for **author identities**
  (`git log --all`), so the gap is specifically file *content* — that scan is a
  `git grep` against the working tree.
- Walking every blob in every commit is a deliberate command rather than
  something that runs on each `inspect`.
- `gitleaks` and `trufflehog` do this already and are mature. Wrapping one may
  be the honest answer rather than building a scanner.

## Related work

- Born from the idea it replaces: [`scan-history-not-just-the-working-tree`](../../ideas/scan-history-not-just-the-working-tree.md)
