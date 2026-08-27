# Response template

Copy the blocks to `response.md`, beside the audit. **Copy the blocks, not this
file.**

## Frontmatter

```yaml
---
type: response
title: Response to <audit>
responds_to: 2026-12-23-e286f3bd9c11
responded: YYYY-MM-DD
respondent: human:<id> | agent:<model> | process:<tool>
# round: 2      only when a verification reopened something
---
```

## Body

```markdown
# Response to <audit>

## F-001 — agreed | partially agreed | disagreed | accepted

<Your position, then the evidence.

 agreed — what changed, and where. Name the commit or file; "fixed" is not a
 response, because verification has to be possible without asking you.

 partially agreed — which part is correct, and why the rest is not.

 disagreed — why the finding is wrong. The criteria did not apply, the condition
 was misread. Disagreeing is a legitimate outcome.

 accepted — you agree and are choosing to carry it. Say what it would cost to
 fix and why that is the wrong trade. This is the most valuable record of the
 four, because later it is the difference between a decision and an oversight.>

## F-002 — …

<Every finding gets a position. Silence is indistinguishable from having missed
it, and an auditor cannot verify a position nobody took.>
```
