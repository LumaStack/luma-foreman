---
type: policy
title: How a sweep is stored
description: Where a review sweep lives, why it is backlog rather than a record, and the two units — the file that must be covered and the cluster actually reviewed in one go.
matches:
  - topic: running or resuming a review sweep
  - path: ".luma/backlog/sweeps/**"
---

# How a sweep is stored

A **sweep** is one party reading a codebase from one end to the other, with a
second beside it. **Usually a person with an agent, and not necessarily** — see
[[who-does-the-reading]]. It runs for as long as it takes — hours, days,
sometimes more — and survives every session boundary in between.

```
.luma/backlog/sweeps/the-cli-surface/
  charter.md                  why it exists, what it is aimed at, how it is run
  coverage.md                 every file in scope, and what has happened to it
  journal.md                  optional — what was noticed along the way
  slices/
    001-entrypoint-and-args.md
    002-the-permission-gate.md
```

### The three files, side by side

| | **`charter.md`** | **`coverage.md`** | **`journal.md`** |
| --- | --- | --- | --- |
| **what it holds** | the strategy, and what the sweep concluded | a point-in-time snapshot of what is covered and what remains | what was noticed along the way |
| **how it changes** | edited when the strategy or a conclusion changes | **reconciled, repeatedly**, against a tree that keeps moving | **appended to, never revised** |
| **its relation to truth** | should stay true, and get truer | **accurate at the moment of reconciliation, decaying immediately after** | true as of the moment each entry was written |
| **at close** | kept | discarded | **harvested, then discarded** |

**Drift is continuous; correction is periodic. They meet at each reconciliation
and part at the next commit.** The index is exactly right the moment a slice
reconciles it, and stays right until somebody commits — **which on a quiet
repository can be days, and on a busy one is minutes.**

**How long they stay met is the churn rate**, which is why a sweep measures it
at the start. A repository at thirteen commits a day has an index that is
accurate for about as long as it takes to read the next file.

**Which is what `indexed_at` is for.** Not a bookmark for the next
reconciliation, but the honest statement of when the two last met: *accurate as
of this commit, and claiming nothing since.* A reader deciding whether to trust
a row checks it against `HEAD` — and where nothing has moved, the answer is
that the index is still exactly right.

**The right-hand column is append-only, which is what makes it cheap.** Entries
are added and never revised, so writing one costs nothing to maintain, and the
chronology survives — *when did we start noticing this* is a question only an
unedited log can answer.

**Why they are separate files: one is authored, the other derived.**
`coverage.md`'s rows are the scope rule and the clustering strategy applied to
the tree, and its statuses are what the slices record — **delete it and it
rebuilds exactly.** `charter.md` is derivable from nothing: delete it and the
goal, the reasoning and the learnings exist nowhere else.

**That is why staleness means opposite things in them**, and why **a derived
file must not live inside an authored one** — nobody could tell which half had
gone off, a rebuild would put the reasoning in its blast radius, and a `git
diff` of the sweep's thinking would be buried under status changes.

**The journal is a third thing: authored, and temporary by design.** Nothing in
it is meant to survive — **the close harvests it**, and every entry becomes a
backlog item, a learning recorded in `charter.md`, or a deliberate drop.

**That is what makes the whole sweep disposable.** The rule that nothing worth
keeping stays in a sweep needs somewhere cheap to put a half-formed thing in
the meantime; without it an observation is routed prematurely, which files it
badly, or lost. **The journal is how that rule is kept rather than an exception
to it**, and a journal that was never harvested is a sweep that cannot safely
be thrown away.

**It is not a queue.** Anything already actionable goes to its real destination
at the slice that produced it — the journal holds what is *not yet* actionable,
and the harvest catches whatever became so along the way.

**The test, where something is ambiguous:** *could this be rebuilt from the
repository and the slices?* If yes it belongs in `coverage.md`. If losing it
would lose something nothing else records, it belongs in `charter.md` — or, if
it is a note you are not ready to act on, in the journal until the close.

### Derived *given the strategy*, which has to be written down

**The index is only rebuildable if the rules that produced it are stated.**
Scope decides which files have rows; who-reads-what decides a column; **and the
clustering strategy decides which cluster each row lands in.** Leave any of
those in somebody's head and the index stops being derivable — it becomes a
record of judgements nothing else holds, sitting in the file that was supposed
to be the cache.

**Clusters are the one people leave unstated**, because grouping feels obvious
while doing it. It is not derivable from paths: a cluster groups what must be
understood together, which is routinely not what sits together. Four documents
in three directories may answer one question, and one directory may hold three
clusters that share nothing but a path.

**So the sweep names its clusters and says what each is about**, and **a file
that fits none of them means the strategy is incomplete.** Add the cluster to
the sweep rather than improvising one in the index — improvising is how the
index quietly becomes authored.

**The scope rule stays in `charter.md`; the enumeration goes in
`coverage.md`.** *Everything tracked except the generated adapters and the
vendored bundles* does not change when a file is added. The list of
eighty-seven rows does, and is supposed to.

## It is backlog, not a record

**The tier is decided by lifecycle, and a sweep in progress is an intention.**
It churns — the index is edited at every slice, files are added when the tree
moves under it, rows go from pending to reviewed or approved. `records/` is
append-only and never edited, so a sweep filed there would break the tier on
its first day.

**A sweep evaporates; an audit settles.** That is the lifecycle half of a
larger distinction — what each is complete against, which one puts somebody on
the hook, and why both need independence for opposite reasons. It is in
[[sweeps-and-audits]] rather than here, because most work inside a sweep never
has to ask it.

**Do not file a sweep as an audit to make it look more rigorous.** It produces
a commit pin that is false by the third file, and a record nobody owes an
answer to, filed where things that settle are kept.

*Audits are `audit-records`'. Where a sweep turns up something that genuinely
wants an accountable answer, that is a finding to raise there — not a reason to
restructure the sweep.*

## The slices are the source; the index is a cache

`coverage.md` carries a table of every in-scope file and its status. **That
table is an index and can be rebuilt** — the truth is in the slices, each of
which says which files it covered.

This matters the first time the table and the notes disagree, which they will.
A slice note is written once and never revised; a table cell is edited every
time anything happens. **When they conflict, the notes win**, and the table is
regenerated from them rather than argued with.

*Storing derived status is a thing records must never do, for a reason that
does not reach here: it forces somebody to edit a document they did not write.
A sweep has one writer. The prohibition is about authorship, not about
derivation.*

## A count in the charter is almost always wrong to write

**The charter is the file that should get truer. A count never does.** It is
right at the moment of writing and wrong the moment anything changes, and
**nothing announces the change** — a stale number reads exactly like a current
one.

**This is the authored-and-derived test applied to a sentence rather than a
file.** The split above decides which *file* something belongs in; it is rarely
asked of a paragraph, so an authored file quietly fills with derived sentences.
Those rot at a derived file's rate **with none of the reconciliation**, because
nobody reconciles the authored one.

**The test:** *can this sentence go wrong without anybody editing this file?*
If yes, it is derived, whatever file it is sitting in.

### Point at the number; do not copy it

Where a count exists somewhere already kept current — the index, a version
history, the repository itself — **cite that place instead.** Copying it here
creates a second answer that goes wrong on its own, and a reader then has two
numbers and no way to tell which is live.

### Not banned, and the exception is said out loud

**Some count may genuinely earn its place**, and a rule forbidding all of them
would be a guess about cases nobody has met. So this is strong advice, not a
prohibition.

**Where one is written anyway, tell the reader as you write it** — that it is a
count, that it will go stale, and why it is here rather than in the index. **An
exception nobody was told about is indistinguishable from an oversight**, which
is precisely how they accumulate: every count in a charter was written by
somebody who thought that one was fine.

**Dating it is not the fix.** *Forty-two files, as of slice 004* stops being
wrong silently, and still never gets truer. It is a smaller failure of the same
kind.

### What this looks like when it goes wrong

The first sweep to run this practice accumulated eight counts in its charter —
file counts in the scope exclusions, a release-and-files cost, slice totals in
the estimate, the repository's age and commit rate. **Three were already false
within a day**, including one that had moved from *seventeen releases, six
files* to *twenty-one and eight* while the charter still claimed the first.

**None was reported by anything**, and none could have been: they were fluent,
plausible sentences in a document nobody had reason to re-check.

## Two units, and confusing them is the common failure

**The unit of coverage is the file.** Every file in scope appears in the index,
so *read with nothing found* stays distinguishable from *never looked at*. A
sweep that cannot tell those apart has produced confidence it did not earn.

**The unit of a slice is a cluster** — a module, an execution path, a directory
that means something. You review six files together because they only make
sense together.

Reviewing files in isolation because the index is a list of files is the
mistake this distinction exists to prevent. **A file read without its
collaborators is read as a stranger**: you can see that a function is called
and not whether the caller holds the lock it assumes. The index is a coverage
ledger, not a running order.

**One slice, one note, several files marked off.**

**The bound is comprehension, not a file count.** A slice that covers one file
is right when the file is dense enough to spend an evening on. A slice that
covers thirty short documents is also right, because thirty pages of prose is
an amount of material a reader can genuinely hold at once.

The test is whether you could still say what each file did afterwards. **A
slice that fails that is a skim with a note attached**, at any size — and a
slice of three files can fail it just as easily as one of thirty.

## Slices partition the sweep

**A file belongs to one slice.** All the slices together are the scope, and
each file is read once — which is what makes the coverage arithmetic mean
anything.

**Re-covering is an exception the sweep records, not a mode it runs in.** Code
moves under a sweep that takes weeks, and occasionally a file changes enough to
want reading again. That is a decision somebody makes and the index notes, with
the earlier slice named — never a row that quietly resets.

**The difference is what you can see.** A ledger that churns silently looks the
same at 60% whether nothing drifted or half of it did. One that records
re-coverings shows drift accumulating while there is still time to cut the
scope.

## A row records three separate facts

**Reading, sign-off and what was found are three different things**, and one
column cannot carry them. A file can be read by an agent and signed off by a
person who never opened it; a person can read one closely and withhold
approval. **Both are ordinary, and neither is expressible in a single status.**

| column | holds | who fills it |
| --- | --- | --- |
| **`reviewed_by`** | who read it | **any party**, agent included |
| **`approved_by`** | who signed it off | **a human only** |
| **`outcome`** | `clean` or `findings` — what the reading concluded | whoever read it |

**Empty means it has not happened.** A row with neither actor is pending; no
status value is needed to say so, and none can drift out of step with the
actors.

### The state that was previously invisible

`reviewed_by: agent:opus-5` with `approved_by: human:fsmith` is **an agent read
the file and a person signed off without reading it** — which is the declared
arrangement wherever a sweep says the reader takes a summary rather than the
file. **A single `approved` silently claims the person read it.**

The reverse matters too. `reviewed_by: human:fsmith` with `approved_by` empty
is **a person read it closely and withheld approval** — *I am not happy with
this and I am moving on* — which is an ordinary and honest place for a row to
stop.

### `outcome` is what the reading concluded, not what the file is now

**Past tense, deliberately.** *Slice 004 found problems here* stays true
however many times the file is fixed afterwards. A column describing the file's
current quality would have to be maintained — fix the file, and somebody must
return and change the row — which is coverage tracking fixing rather than
reading.

**It is also derivable**, from the slice notes, which is why it belongs in the
index at all.

**Two values, and it is not a ladder.** Severity, urgency and what to do about
it are the finding's job; `outcome` answers only *did this read produce
anything*, which is the question a close needs and nothing else records in one
place.

**Neither party may withhold a fact the other is entitled to record.** An agent
writes `approved_by` when the person gives it, whatever the agent thinks and
however the file got that way. Its own view lives in `reviewed_by` and
`outcome`, where it has no veto over anybody.

**Challenge belongs before the row is filled, never after.** Ask what they made
of it, name a goal they may have drifted from, say where you read it
differently. Then record what they decide. [[the-pairing-turn]] draws that
line.

**The close reports all three.** *Fifty-three approved, twelve reviewed and
never signed off, nine with findings* is a true sentence about a sweep, and one
status column cannot say it.

## Coverage tracks reading; the backlog tracks fixing

**A row can be finished while the file is still wrong.** It closes when the
reading is done and the findings are routed — not when the file is good. That
is why [[what-a-slice-produces]] says a slice produces a record rather than a
change.

*I do not approve of what is in there, but I am moving on* is therefore an
ordinary close, not an impasse: `reviewed_by` names who read it, `outcome` says
`findings`, `approved_by` stays empty, and the defect lives in the backlog
where somebody can act on it.

**Nothing is lost by that split, and a great deal is protected.** A column for
*has open findings* would be a second record of what the backlog already holds,
and the two would drift the moment either was updated alone. The index answers
*has this been read*; the backlog answers *is it fixed yet*. **Neither can
answer the other's question, and neither should try.**

## Rows are independent

**Approving a file makes no claim about anything it links to.** A document
approved today may point at four that are still `pending`, and that is an
ordinary state rather than an inconsistency.

**The alternative is unbounded.** If a row could only be approved once
everything it referenced was, then a project where things move — content split
out, a document broken in two — becomes one where nothing can ever be approved,
because every approval drags in more. **Coverage is per file, and the index is
what holds it together.**

**What a split does owe is a note**: the new rows exist, they are pending, and
the slice that created them says so. That is bookkeeping, not a dependency.

## A slice is not an agent session

**The word is qualified for a reason.** A slice is a unit of *reading* — one
cluster, one note, one coherent piece of reasoning. An agent session is a unit
of *conversation*, and it ends for reasons that have nothing to do with the
review: a context limit, a crash, going to bed.

**They do not line up, in either direction.** One slice may span three agent
sessions when the cluster is hard or the day keeps interrupting it. Three
slices may fit inside one long agent session when the material is light — which
is the ordinary case for prose.

**So never close a slice because a conversation ended, and never hold one open
because a conversation is still going.** It closes when the cluster has been
read, argued about, and routed. That is what the note records, and it is the
only thing that marks files off the index.

*What to write when the conversation itself ends is `session-manager`'s, not
this bundle's. A sweep needs little of it: the index and the notes are
committed, so a half-finished slice costs a paragraph to resume rather than a
handover.*

## A sweep does not review its own record

**Exclude `sweeps/` from any scope that would otherwise contain it.** A sweep
whose scope is *everything under `.luma/`* will grow its own index and its own
slice notes inside that scope, and reviewing them is circular — **approving
your own coverage ledger proves nothing about coverage.**

**It appears mid-sweep rather than at the start**, which is why it needs
stating: the directory does not exist when the scope is settled, and
reconciliation adds its files as ordinary pending rows without noticing what
they are.

*Another sweep may review this one's records. That is an ordinary sweep of
somebody else's work, and its findings are worth something.*

## Naming

**The sweep directory is a slug for what is being read** — `the-cli-surface`,
`everything`, `docs-and-prose`. No date, and no commit: a sweep spans many of
both, and pinning either in the name would be a claim it cannot keep.

**Slices are numbered and slugged** — `001-entrypoint-and-args.md`. The number
is the identity and the order they happened in; the slug is for finding one
again. Numbering from `001` rather than by date, because *what did we do first*
is the question anybody asks of a sweep and the date does not answer it.

## More than one sweep at a time

**Two sweeps sharing neither owner nor territory are ordinary**, and want no
apology. Somebody reading the prose while somebody else reads the CLI is two
sweeps, correctly — nothing is contended, and merging them would buy a single
index nobody can act on alone.

**What fails is two sweeps competing for one person's attention.** Neither
finishes, because attention is the only scarce resource involved and it does
not divide. That is the mistake the rule is about, and it is a mistake about
the reader rather than about the number.

**Overlap in either dimension collapses them into one.** Same reader, or the
same files, and what you have is one sweep with two indexes disagreeing about
its coverage.

## Archive when closed; delete later and deliberately

A closed sweep moves to `.luma/backlog/sweeps/archived/<slug>/`, keeping the
`slices/` beside it. **What the sweep produced has already left** — a merged
pull request, an idea, a decision, a finding — so what remains is working
notes, and their value decays.

Deleting them is fine eventually and is nobody's emergency. Archiving needs no
permission; deleting somebody else's sweep needs theirs.
