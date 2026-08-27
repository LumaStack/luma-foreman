# Audit template

Copy the blocks to `.luma/records/audits/<DATE>-<SHA>/audit.md`. **Copy the
blocks, not this file.**

## Frontmatter

```yaml
---
type: audit
title: <what was audited, in a few words>
audited: YYYY-MM-DD
commit: <at least 12 characters>
scope: <what was examined — and say what was not, in the body>
anchor: targeted | open-ended
auditor: human:<id> | agent:<model> | process:<tool>
---
```

## Body

```markdown
# Audit: <what was audited>

## Scope

<What was examined.>

**Anchor:** <targeted, and what at — or open-ended. If nobody was interviewed,
say so: an audit nobody anchored reads differently from one where nobody was
asked.>

**Not examined:** <the half people skip. Without it a reader cannot tell
"examined and clean" from "never looked". Say which exclusions you were given
and which you chose.>

## Method

<How. Tools run, what was read, what was sampled rather than exhausted.>

## What it was aimed at

<Targeted audits only, and required even when the answer is nothing.>

> *Asked to look for: <the worry, in their words>.*
> *Found: <instances, by id — or "none", with what that claim covers>.*

**A negative is a result.** An audit that reports only what it found cannot tell
somebody to stop worrying.

## Findings

<A line per finding — id, severity, one clause. Not a restatement: a reader
should be able to decide from this table alone whether to read further.>

| id | severity | summary |
| --- | --- | --- |
| F-001 | high | … |

<Or, if a single auditor kept findings in this file rather than in findings/,
each finding as a section here — accepting that they are then not addressable
individually. See the layout policy.>

## Summary

<What the state of this thing is, in a few sentences. The part somebody reads
when deciding whether this audit changes their plans.>
```
