# Closing a slice

Copy the block below when a slice ends. **Copy the block, not this file** — it
is a message shape, like [the presentation template](file-presentation.md).

Three parts, in order. The reasoning — why a slice boundary is the cheapest
moment to clear, and when not to — is in step 11 of the `review-next` workflow.

## The block

```markdown
## What this slice did

<Three or four lines. Not the slice note, which is the record — this is the
reader remembering what just happened before they choose what is next.>

- `docs/args.py` closed — reviewed by human:fsmith, findings, not signed off
- `docs/flags.py` closed — approved
- two findings routed to the backlog, one fixed in place
- the practice gained a rule about removals

## Where the sweep stands

| | |
| --- | --- |
| closed | `cli.py`, `args.py`, `flags.py`, `parse.py` |
| skipped | `generated/` — reader's exclusion; `vendor/` — not ours |
| open | `docs/gate.md` |
| untouched | the transport layer, the test suites, the migration scripts |

<Names in the first three rows. Groups in the last — a reader wants to know
which files are done and roughly what is left, and ninety filenames under
`untouched` is the index printed twice.>

<Then one line saying what the table makes obvious: "two clusters closed and
none of `src/` reached".>

## Clear or carry on

<A recommendation, not a decision. The check is: is anything left that exists
only in this session?>

Nothing here is unwritten — the slice note, the index and the journal all
landed, and the next cluster is a different subsystem. **Clearing is free and
I'd take it.**
```

## The three shapes the last part takes

**Recommend clearing.** Nothing exists only in the session, and the next slice
is elsewhere. The usual case, and the reason a slice boundary exists.

**Write something down first.** Something is still only in the session — that
is a defect rather than a reason to hold the context. Name it, write it to the
journal, then clear.

**Recommend carrying on.** The next slice is the same cluster, so orientation
carries over and clearing buys a re-read of files about to be discussed. Say
which of the three it is, and why, in a line.
