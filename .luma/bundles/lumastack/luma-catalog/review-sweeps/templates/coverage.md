# Coverage template

Copy the blocks to `.luma/backlog/sweeps/<slug>/coverage.md`. **Copy the
blocks, not this file.**

**This is the index, and nothing else.** Why the sweep exists, what it is aimed
at and what it taught live in `sweep.md` beside it — they are written once and
this is edited at every slice, and keeping them together buries one under the
other.

## Frontmatter

```yaml
---
type: coverage
title: Coverage — <the sweep>
indexed_at: <12-character commit this was last reconciled against>
---
```

## Body

```markdown
# Coverage

## Progress

<Derived from the rows below, never typed. A wrong number here is the rot the
writing conventions warn about, and this is the one table a reader trusts
without checking.>

| | |
| --- | --- |
| approved | |
| reviewed | |
| skipped | |
| pending | |
| total rows | |

<And the rate, re-taken here at every slice: a range across every slice so far,
with how many there have been.>

## The index

`pending` · `reviewed` · `approved` · `skipped` **with a reason, always**

**`reviewed`** — read and satisfactory; either party may set it. **`approved`** —
signed off, and only a person gives it. The `by` column records who.

| cluster | file | read by | status | by | slice |
| --- | --- | --- | --- | --- | --- |
| entrypoint | `src/cli.py` | both | approved | human:fsmith | 001 |
| entrypoint | `src/args.py` | agent | reviewed | agent:opus-5 | 001 |
| gate | `src/gate.py` | both | pending | | |
| — | ~~`src/old.py`~~ | — | removed | — | 001 — deleted |
| — | `src/generated_api.py` | — | skipped — generated | | |

<Every file in scope gets a row, including the boring ones. A file missing from
here can never be shown to have been read.>

<Strike a deleted file through rather than removing the row, so the index still
explains itself.>

```
