# Verification template

Copy the blocks to `verification.md`, beside the response. **Copy the blocks, not
this file.** Written by the auditor, never by the respondent.

## Frontmatter

```yaml
---
type: verification
title: Verification of <audit>
verifies: 2026-12-23-e286f3bd9c11
verified: YYYY-MM-DD
verifier: human:<id> | agent:<model> | process:<tool>
# round: 2      matches the response round it checks
---
```

## Body

```markdown
# Verification of <audit>

## F-001 — closed | closed (accepted) | open | withdrawn

<What you checked, not what you were told.

 closed — the change you read, and why it resolves the finding.

 closed (accepted) — why the reasoning for carrying it holds. Accepting an
 acceptance is a real decision; if the reasoning does not hold, that is open.

 open — what is still wrong, and **specifically what would close it**. An open
 finding with no stated remedy is an argument rather than a record.

 withdrawn — the finding was wrong and you say so. An audit process whose
 findings are never wrong is one nobody trusts.>

## F-002 — …

## Outcome

<How many closed, how many open, and whether a second round follows. Write this
section even when everything closed — an audit with no verification is
indistinguishable from an abandoned one.>
```
