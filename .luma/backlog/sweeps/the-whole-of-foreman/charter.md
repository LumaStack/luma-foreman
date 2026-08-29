---
type: sweep
title: The whole of luma-foreman
created: 2026-08-28
lifecycle_status: provisional
survival: experimental
goal: Nothing in this repository states something false — whether it drifted there or was created that way
scope: All tracked content except the generated .claude/ adapters and the vendored .luma/bundles/ copies
goal_discipline: exploratory
scope_discipline: exploratory
strategy_discipline: exploratory
ordering: led
approval: recommended
pairing: human-agent
contributors:
  - human:benlinton
  - agent:opus-5
---

# The whole of luma-foreman

## Goal

**Nothing here should state something false.** Two ways that happens and the
sweep is aimed at both:

- **Churn damage.** A young repository under continuous heavy change,
  including a week of estate-wide automated substitution — section references,
  field renames, a vocabulary change carried through every bundle in the
  catalog. Statements that were true when written and are not now.
- **False on creation.** Statements that were never true, written confidently
  and never checked.

**On track means:** every claim holds when checked against the thing it
describes, and the sweep can name what is wrong rather than only that something
is.

**Corrected after slice 001.** The goal was churn damage alone, and the first
slice found three documents that were false *when written* — no history, no
drift, nothing for a churn-aimed sweep to catch. **Three of its four files would
have been out of scope under the original goal.**

**It makes `cross-check` the primary method rather than a habit.** Every
mechanical finding in slice 001 came from running the thing a document
described — `--help`, the rules on disk, the code behind a claim about it — and
none from reading carefully. Careful reading found only what could not be
checked.

**It is also expected to produce a summary** of what foreman does so far and
what its live problems are. That is an ask rather than the goal, recorded so it
does not get lost — a sweep aimed only at churn would skip it.

## The second goal: make the practice work

**This is the first sweep anybody has run, and improving it is not overhead.**
`review-sweeps` was `draft` and `survival: experimental` when this started.
Every rule in it that now reads as obvious was absent or wrong until this sweep
hit the case that exposed it — the reader owning the row, three facts instead of
one status, a ledger owed when a document is removed, a file closing on a
verdict rather than on momentum. **That is the material, not a distraction from
it.**

**It is measured the same way as the first goal**: a rule earns its place by
having been broken here, against a case that actually occurred. **Improving the
practice speculatively is not this** — a rule nobody has needed yet is a guess,
and guesses are what the first slices spent their time deleting.

**It stays out of the frontmatter `goal:` on purpose.** That field states what
should be true of *this repository* when the sweep is done. This one is about
the sweep, which is a different subject, and folding them into one line would
make the field answer neither question cleanly.

**And the two goals compete for time, deliberately.** A sweep that covers ninety
files and teaches nothing has failed one half. A sweep that produces a polished
bundle having read a fraction of the scope has failed the other — **and that is
the half at risk here.** The close reports both.

## The other two files

**[`coverage.md`](coverage.md)** carries every file in scope and three facts
about each — who read it, who signed it off, and what the reading concluded —
plus `indexed_at`, the commit it was last reconciled against.

**[`journal.md`](journal.md)** carries what was noticed along the way and is not
yet a finding. Append-only, harvested at the close into backlog items and
learnings, then discarded with the rest of the sweep.

**This file is authored; that one is derived.** Its rows are the scope rule and
the clustering strategy below applied to the tree, and what fills its rows is what the
slices record — delete it and it rebuilds exactly, **which is only true because
the strategy is written down here.** Delete this one and the goal, the reasoning and the
learnings exist nowhere else.

## Scope

**The rule is the frontmatter `scope:` field, and this section does not
restate it.** What is *in* is every tracked file the rule does not exclude, and
[`coverage.md`](coverage.md) is that enumeration — derived, and reconciled at
every slice.

**An enumeration here would be the rule copied by hand, and it drifted within
two slices.** This section listed nine paths, `.gitignore` was not among them,
and reconciliation at slice 003 found a tracked file with no row. **The rule had
always included it; the list had never said so.** Scope stated twice is scope
that will disagree with itself, and the copy is the half that goes wrong.

**Not included.** The first three were chosen; the fourth was given:

- **`.claude/`.** Generated by `luma-foreman apply`. Reviewing
  generated output tells you about the generator, which is in scope as `apply.py`.
- **`.luma/bundles/`.** Vendored copies owned upstream in
  `luma-catalog`. Editing them here is drift by definition, so reading them here
  can produce nothing actionable.
- **`.luma/backlog/sweeps/` — this sweep's own record.** A sweep reviewing the
  file that records it is circular, and approving your own coverage ledger
  proves nothing about coverage.
  Added as an exclusion once the sweep's files appeared inside its own scope.
- **`docs/examples/`. Given, at slice 003.** The reader excluded them
  rather than the sweep reasoning its way there, which is the distinction this
  list exists to keep. They are worked examples of the standards in
  `docs/standards.md`, which is read.

## Who reads the source is not uniform, and `coverage.md` says so

**Everything is read in full. What varies is who reads it.**

| area | read by | and so |
| --- | --- | --- |
| prose — `docs/`, `.luma/`, root | **both** | the reader forms their own view before the agent gives one |
| code — `src/`, `tests/`, `bin/`, `libexec/` | **agent, then a summary the reader skims** | the reader's view is downstream of the agent's |

**This is the division of labour [[the-pairing-turn]] already permits**, declared
at the start for a whole area rather than discovered file by file. It is not a
shallower read: the agent reads every line, and the summary is what gets skimmed.

**What it costs is the protection the turn order exists for.** On code slices
the reader is not forming an independent view first — they are reacting to one
already formed. That is a real weakness and a chosen one, and every code slice
records it, because a reader can discount a stated weakness and an unstated one
is the harder problem.

**Where the summary raises something, the reader can always go to the file.**
The arrangement is a default for pace, not a rule against reading.

## How files are grouped into clusters

**Clusters are authored, not derived from paths.** They group what has to be
understood together, which is often not what sits together: `README.md`,
`CLAUDE.md`, `.luma/PROJECT.md` and `docs/scope.md` live in three directories and
answer one question, while `src/foreman/` holds three clusters that share a
directory and little else.

**Three rules produced the ones below:**

1. **Group by what must be read together** — a subsystem, an execution path, a
   set of documents answering one question. Not by directory.
2. **Cap a cluster at one slice's worth**, and split in path order when it
   exceeds that. `ideas A` and `ideas B` are one directory split on size alone.
3. **A file big enough to be a slice on its own gets its own cluster.** `apply`
   is one file of 947 lines.

| cluster | what it is |
| --- | --- |
| what it says it is | the documents that tell a newcomer what this project is |
| standards and permissions | the standards documents and their worked examples |
| decisions | the decision records |
| plans, config, changelog | project state that is neither a decision nor an idea |
| ideas A · B · C | the idea backlog, split on size in path order |
| entry and shared | the command-line entry point and the modules everything uses |
| adoption path | `get`, `init`, adoption, catalog, outdated |
| apply | the projection engine |
| inspect | the checker and its rules |
| agent permissions | the gate, its model, and its command surface |
| tests | the suites |

**`split from README` was folded at slice 003's reconciliation**, as it was
declared it would be. All four of its rows closed in slices 001 and 002, and
they now sit in `what it says it is` with the documents they were split from.
**A transitional cluster that outlives its transition is just a cluster**, and
the fold is what keeps the strategy above true.

**`ideas B` became `ideas A · B · C`** when slice 002 created four new idea
files. Seventeen rows exceeded one slice's worth, so rule 2 applied: re-split
in path order across three. Every row was `pending`, so nothing was lost by
re-cutting them.

**A file that fits no cluster means this list is incomplete.** Add the cluster
here rather than improvising one in `coverage.md` — **the index applies this
strategy and does not invent it**, which is what keeps the index derivable.
Reconciliation places a new file by asking which of these it belongs to.

## Discipline

**`exploratory` on all three axes**, which is what this sweep has actually been.
The practice was `draft` when it started and nobody knew what a sweep was — so
the goal moved, the scope gained exclusions mid-flight, and the strategy went
from unstated judgement to written rule. **That is discovery, not indiscipline.**

**It cannot be estimated, and that is a property rather than a failing.** A sweep
still working out what it is has nothing to estimate against; the estimate below
is honest about being abandoned rather than revised.

**Discovery has cost far more releases of `review-sweeps` than files read**,
and the next sweep should compare itself against that rather than repeat it.

**The numbers are not written here.** `review-sweeps`' own version history says
how many releases this sweep produced; [`coverage.md`](coverage.md) says how far
it got. **Both are kept current, and copying either into this file only creates
a third answer that goes wrong on its own.**

**Worth revisiting at slice 003.** The practice has largely stopped being new
while the material has not been read — which is the profile of a sweep that
should move to **strict goals, strict scope, adaptive strategy**: do not wander,
but do keep improving how you read.

## Approval

**`recommended`.** Sign-off is wanted on every row and some rows will not get
it — which is the ordinary case and is neither `required`'s guilt nor
`optional`'s indifference. **A row read and left unsigned is a known compromise
here, named at the close rather than counted as a failure.**

`.luma/PROJECT.md` is the first of them: read closely, findings recorded, and
deliberately not signed off. **That is a finished row, not a stalled one** —
coverage tracks reading, and the backlog tracks fixing.

## Order

**`led`, over a prose-then-code backbone.** The reader chose the sequence: all
prose first, then code by subsystem, entry point downward.

**Why it holds:** the prose is where the churn landed hardest and where a wrong
statement is invisible, and reading it first builds the model that makes the
code orientation cheap.

## Size

**Prose at a cluster a slice; code at a subsystem a slice.** That is the shape
the estimate assumed, and the shape is what survives — the totals it produced
were a guess made before anything had been read, and
[`coverage.md`](coverage.md) carries the measured rate that replaced them.

**The code slices are cheaper for the reader and not for the agent** — the
reading is the same, only the reader's part is a summary. So they will feel
faster and should not be assumed lighter when measuring the rate.

**Expected drift: total.** Every file in scope was touched recently. The
repository is young, commits heavily, and the churn is ongoing rather than
finishing.

**So this sweep has to be short.** At that rate a sweep running for weeks
reviews a repository that changed completely underneath it. Days, not weeks —
or slow the commits while it runs.

*The measured rate lives in [`coverage.md`](coverage.md) and is re-taken at
every slice.*

## Half-finished, and where it came from

**Approving `README.md` created four rows.** The README was rewritten to the
`project-documentation` readme policy, and what it had been carrying moved out —
install, the command reference, the inspect rules, the invariants. Those four
documents were written by the agent and **the reader has not read any of them.**

**They do not block the README's approval** — rows are independent, and the
alternative would mean nothing can ever be approved in a project where content
moves. They are pending rows with their provenance recorded, and the *split from
README* cluster is where the next slice should start.

## Where the practice fought us

**This is the first sweep ever run, and the bundle is `survival: experimental`.**
Every slice keeps a line for where the practice got in the way — an order that
stopped working, an estimate wrong by double, a step that produced nothing.

Everything below was found before slice 001, and all of it is now fixed in
`review-sweeps` `0.7.0` — the bundle was corrected four times by a sweep that
had not yet reviewed a single cluster.

**The agent refused a status the reader had given.** The reader read the README,
rewrote it, edited the draft and said it was good; the agent would not mark it,
on the grounds that no proper slice had run. **The bundle exists to protect the
reader's judgement and was used to overrule it.** Cause: nothing said who sets a
status. Fixed by saying so, and by splitting `reviewed` from `approved`.

**Rows appeared to depend on each other.** The agent implied the README could not
be finished while the documents split out of it were unread — which in a project
where content moves means nothing can ever be finished. Fixed: rows are
independent, a split owes a note rather than a dependency.

**Nothing tracked what a slice half-finished.** Fixed in `what-a-slice-produces`.

**Two sessions of one model are indistinguishable in the index**, and an
agent-agent sweep's independence rests on them being two. Recorded rather than
fixed: no such sweep has run, and `audit-records` declined to invent a field for
the same problem.

**The agent-reads-first exception is framed per file, not per area.** [[the-pairing-turn]] permits it for *"generated code, a
vendored dependency, a file in a language they do not read"* — one-off cases
noticed in the moment. It has no shape for *the reader decides at the start that
a whole area will be read for them*, which is what happened here and is probably
the commoner arrangement. The index had to invent a column for it.

## Closing summary

*Written at close, not before.*
