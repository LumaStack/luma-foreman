# Presenting a file

Copy the block below when putting a file in front of the reader. **Copy the
block, not this file** — it is a message shape rather than a document, so it is
never written to disk.

The reasoning, and when a row belongs in the data block at all, is in the
bundle's policy on presenting a file.

## Deep — the reader reads the file themselves

```markdown
Slice NNN · file N of M — path/to/file.ext

| | |
|---|---|
| lines | 50 — the shortest of the four |
| commits | 1 — created today |
| linked from | getting-started.md, commands.md |
| links out | none |
| churn | none |
| cross-check | 5 rules on disk, 5 documented — matches |

## Summary

What the file is, in two or three sentences. Not what is wrong with it.

## What I make of it

- Three or four bullets, strongest first. Line references in full, as
  `path/to/file.md:35` — a bare `:35` cannot be opened from a terminal.
- Say what you cannot vouch for as readily as what you can.
```

**Then get it open**, however files open on this machine — which may mean the
reader's own terminal resolving the reference rather than a command you run.
Either way, not before: the reader wants to know what they are looking for
before they change windows.

## Shallow — the agent reads, the reader takes the summary

```markdown
Slice NNN · file N of M — path/to/file.ext

| | |
|---|---|
| lines | 462 |
| commits | 14 — last touched yesterday |
| linked from | cli.py, get.py |
| churn | heavy, and ongoing |
| cross-check | every documented flag exists — matches |

## Summary

What the file does, in a short paragraph. Enough that the reader need not open
it.

## Problems

- What is wrong, with references in full as `path/to/file.md:35`. This is the
  section shallow exists for.
- Nothing found is a result: say so rather than leaving the section out.
```

**Then offer to open it** rather than opening it — in shallow mode the reader
chose not to read, and a window they did not ask for is an interruption.

## The rows are a starting set

Six is where this began, not a contract. Drop a row that does not change how
much attention the file deserves, and add one the sweep's own goal calls for.
