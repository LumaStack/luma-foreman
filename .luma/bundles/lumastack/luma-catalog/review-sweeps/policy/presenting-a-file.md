---
type: policy
title: Presenting a file
description: How a file is put in front of the reader — the shape, the order it arrives in, and the difference between a deep presentation and a shallow one.
matches:
  - topic: showing a file to somebody during a review
---

# Presenting a file

**One file at a time.** Presenting a cluster at once buys nothing: the reader
can only read one, and the other three scroll away while they do.

*The slice still covers the cluster — the file is the unit of presentation, not
of coverage.*

## The shape

[The presentation template](../templates/file-presentation.md) carries it, for
both modes. In outline: a heading naming the file and its place in the slice, a
data block, a summary of what the file *is*, what you make of it — **then open
it**, and not before. The reader wants to know what they are looking for before
they change windows.

## The data block

**Every row has to earn its place by changing how much attention the file
deserves.** Drop one that does not.

| row | what it tells the reader |
| --- | --- |
| **lines** | how long this will take |
| **commits** | whether it has a history to have drifted from |
| **linked from** | how much rides on it. Nothing inbound may mean nothing depends on it |
| **links out** | whether approving it implies more reading |
| **churn** | recent movement, which is what most sweeps are aimed at |
| **cross-check** | any claim in the file checked against the thing it describes |

**`commits` decides which question to ask of the file.** A file with one commit
cannot have drifted — so *did this rot* is unanswerable and *was this ever
true* is the only question left. A file with forty commits has both available.
**Sweeps aimed at churn quietly assume every file has a history, and new files
are exactly where that assumption fails.**

**`cross-check` repays the most, and it is a method rather than a habit.** A
documented list against the code it lists, a count against what it counts, a
flag against `--help`.

**Prefer a check you can run over a claim you can only read.** In the first
sweep ever conducted, **every mechanical finding came from executing the thing
a document described** and none from reading it attentively — careful reading
found only the claims nothing could verify. **A document is most confident
exactly where nobody has checked it.**

**So look for the runnable check first, and say when there was none.** *Two
claims I could not verify* is itself a finding, about the file's checkability,
and worth as much as the claims that were checked.

**The block is not fixed.** These six are a starting set, not a contract — a
sweep aimed at something else will want other rows, and finding them out is
part of running one.

## Deep and shallow are different presentations

| | deep | shallow |
| --- | --- | --- |
| the file | **given in full**, or opened for the reader | **summarised** |
| the reader | reads it themselves | reads the summary |
| the agent | says what to attend to | says what is wrong |
| ends with | the file open | a way to open it if they choose |

**Which one applies is declared per area**, alongside the pairing — see
[[who-does-the-reading]]. A sweep may be deep on its prose and shallow on its
code, and the index says which.

## Getting the file open

**Settle once how files open here, and expect the answer to be the reader's
terminal rather than a command you run.**

| what opens files | who does it | the agent's job |
| --- | --- | --- |
| a **GUI editor** | the agent can launch it and it detaches | run the command, at the line under discussion |
| a **terminal editor** | **only the reader can** — it needs to own a terminal | emit the reference and stop |

**The second case is the common one and the easy one to get wrong.** An agent
whose `EDITOR` is `vim` cannot open anything: a non-interactive call has no
terminal to give it, so the attempt hangs or dies. **Printing the reference is
not a failure to help — it is the mechanism**, because the reader's terminal
already knows how to resolve one.

**So write references as `path/to/file.md:10`, never as a bare `:10`.**
Terminals that turn a reference into an editor jump match a path followed by a
line; an offset on its own matches nothing and cannot be made to. It costs the
agent nothing and it is the difference between a reference that opens and one
that has to be typed out.

*Where the reader's terminal does the opening, it is also better than the agent
doing it: nothing steals focus, and they open what they want when they want
it.*

**Settle it before the first file, not during one.** It is the cheapest
question in the sweep and the agent cannot tell it got it wrong — nothing
reports that a window failed to open, or that a reference nobody could click
was printed for the twentieth time.

## The file is live while you are presenting it

**A reader in deep mode has the file open and may edit it while you talk.**
That is the arrangement working, not a problem — but it means **the copy you
presented is already history.**

**So re-read before editing, never edit from what you presented.** An agent
applying a change against remembered text will silently miss where the reader
has already been, and the failure looks like a no-op rather than an error.

**Where an edit does not apply, say the file moved under you and re-read.** It
is a fact about the file, not a complaint about the reader.
