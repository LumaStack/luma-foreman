# Finding template

Copy the blocks to `findings/F-NNN-<short-slug>.md`. **Copy the blocks, not this
file.** Guidance in `../policy/writing-findings.md`.

## Frontmatter

```yaml
---
type: finding
title: <the problem in one line, not the fix>
finding_id: F-001
severity: high | medium | low
location: <file, line, or the part of the system>
---
```

**Severity is consequence, never effort.** `high` means what it costs if nobody
ever fixes it — not that it is hard to fix.

## Body

```markdown
# F-001: <the problem in one line>

## Condition

<What *is*. Specific and checkable — a reader must be able to find it.>

## Criteria

<What *should* be, and **by whose rule**. A project convention, a specification
section, a stated invariant. Where no rule exists, say you are proposing one —
dressing a proposal up as a violation is how audits stop being read.>

## Cause

<Why it is this way. Where several findings share a cause, say so — five
findings with one cause are one problem.>

## Effect

<What it costs if nothing changes. This is what makes it rankable against
everything else.>

## Recommendation

<What would resolve it. Enough that a respondent does not have to guess.>

## Evidence

<Optional. Tool output, a reproduction, a link. Cite it here rather than filing
it as findings of its own.>
```
