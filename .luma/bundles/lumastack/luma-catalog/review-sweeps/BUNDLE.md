---
type: bundle
title: lumastack/luma-catalog/review-sweeps
version: 0.31.1
published: 2026-09-02
stage: draft
survival: probationary
consumers: [project]
description: The review sweep — reading a whole codebase with an agent beside you, ordered and resumable, with the reader's own read as the thing being protected.
---

# Review sweeps

Reading your own project properly is a thing people intend and do not do. It
has no natural unit, no end, and no way to tell at any moment how much is left
— so it starts, covers whatever was interesting, and stops without anybody
deciding it had.

A **review sweep** gives it the three things it lacks: an order chosen on
purpose, an index that makes coverage checkable, and a unit of work small
enough to finish in an evening. It runs for weeks and survives every session
boundary in between, because all of its state is on disk rather than in a
conversation.

*Called a **sweep** in everyday use.* The full name is worth having because
each half fixes the other's weakness — *review* says careful reading with
judgement and nothing about coverage; *sweep* says complete ordered coverage
and nothing about depth.

## What is here

**Policy**

- [[how-a-sweep-is-stored]] — where it lives, why it is backlog rather than a
  record, and the two units that get confused. Read first.
- [[the-pairing-turn]] — orientation before the reader reads, judgement only
  after they have spoken, and what the reader is owed from the other party.
  The rule the practice is built around.
- [[who-does-the-reading]] — the two parties, why neither has to be human, and
  what changes when no human is in it.
- [[presenting-a-file]] — how a file is put in front of the reader: the shape,
  the order it arrives in, and deep against shallow.
- [[choosing-an-order]] — five orders including a led one, what each buys and
  costs, and why the choice is recorded rather than defaulted to.
- [[what-a-slice-produces]] — a slice records and does not rewrite, why a
  proposed fix is a suggestion rather than law, and when a fix may land at all.

**Procedures**

- [[start-a-sweep]] — the goal, then scope, order, index, and an honest
  estimate of the size.
- [[review-next]] — one slice. This is the loop, and it is also how
  a sweep is resumed.
- [[close-a-sweep]] — finish or abandon one without the index telling a lie
  afterwards.

**Background**

- [[sweeps-and-audits]] — why these are different practices rather than two
  rigours of the same one. Read when deciding which you want, or when the two
  look interchangeable.

**Templates** — [a charter](templates/charter.md) · [its
coverage](templates/coverage.md) · [its journal](templates/journal.md) · [a
slice](templates/slice.md) · [presenting a
file](templates/file-presentation.md)

## Worth knowing before reading further

**The reader's own read is the product.** An agent that opens a file with a
list of findings has already done the review, and what is left for the reader
is to agree — which they will. The sweep then produces the agent's judgement
with somebody's name on it, and it looks exactly like success.

Everything about the turn order follows from that. **Facts may be offered at
any time; verdicts wait until the reader has spoken.** *This is called from
three places, one of them holding no lock* is orientation. *This is
over-engineered* is a verdict.

**It is not an audit, and the difference is not rigour.** An audit pins a
commit and separates the party that finds from the party that answers. A sweep
has neither: the code moves as you go, and the reader finding is the reader
fixing. Filing a sweep as an audit produces a commit pin that is false by the
third file and a response written by its own auditor.

**Coverage is derived, not stored.** Each slice says which files it covered;
the index in `charter.md` is a cache of that. When they disagree, the slices
win.

**A row records three separate facts.** `reviewed_by` — who read it, any party.
`approved_by` — who signed it off, a human only. `outcome` — `clean` or
`findings`, what the reading concluded. Both are needed, because a sweep does
not always have a human in it — a status only a person could set would leave an
agent-agent sweep unable to finish a single row.

**Neither party may withhold a status the other is entitled to set**, and
challenge is not veto. The agent's job before a status is to argue: say the
awkward thing, name a goal the reader has drifted from, offer a better idea.
Its job after is to write down what they decided. **Ask, hear the answer, move
on** — a concern raised twice after it is answered is a veto wearing a question
mark.

**Rows are independent.** Approving a file makes no claim about what it links
to. The alternative is unbounded: in a project where content moves between
files, nothing could ever be approved, because every approval would drag in
more.

**Nothing worth keeping stays in the sweep.** It is backlog — it gets archived
and eventually deleted — so a fix, an idea, a decision or a finding leaves at
the slice that produced it. A slice that ends with six observations in a note
has produced nothing.

## What it does not own

**The destinations.** A fix becomes a pull request, an unresolved defect
becomes an idea or a finding, and a *why is it like this* becomes a decision
record. Those shapes belong to `backlog-ideas`, `audit-records` and
`decision-records` respectively, and this bundle names them without requiring
them — where one is not adopted, the destination is whatever the project
already uses, and the routing rule is unchanged.

**Ending a session.** A sweep spans many, and what to write when one stops
belongs to `session-manager`. What this bundle guarantees is that there is
little to hand over: the index and the slices are on disk and committed, so a
sweep survives a crash without anybody having prepared for one.

## Consumers

`project` only, for now. The practice is written against a working tree and a
call graph, and while a headquarters could be read the same way, nobody has —
adding `organization` on that basis would be claiming a fit nothing has tested.

## Version

`0.29.0` — **at the close, rename the sweep if it is far enough off.**

A sweep's scope moves — exclusions arrive, whole areas get deferred — and
**nothing said what to do about a name that had stopped being true.**
`the-whole-of-foreman` that skipped every source file is a directory whose name
is false, and **the directory name is the first thing anybody sees**, before the
charter or the index could correct it.

**Slug and title both.** The slug is not sacred; it is a handle, and a handle
that misdescribes what it opens is worse than an ugly one.

**Only when it is far enough off** — the test is whether the name would mislead
somebody deciding whether to read it, not whether it is imprecise. **Most sweeps
drift a little and should be left alone.**

**At the close, not during.** Mid-sweep you do not yet know what it became, and
renaming while slices are still being written is churn against a moving target.

**Then grep the old slug and repair what points at it** — which is why **a slug
must be greppable**: two or three distinctive words, never one common one.
`the-docs-of-foreman` can be found; `docs` cannot. **A slug that cannot be
grepped is a slug that cannot be renamed.**

**No opaque identifier**, deliberately. One would make renaming mechanical at
the price of meaningless characters in every path forever, to insure an artifact
**designed to be spent**. *Decision records carry `ADR-NNNN` because they are
kept indefinitely; a sweep is not.* **Three things would change that**: sweeps
collected across repositories, sweeps becoming kept records, or a second rename.

**Provenance keeps the old name.** *"Raised during sweep X, slice 001"* says what
it was called then, and rewriting it makes a true sentence false.

**Also fixed: the status template hardcoded a real project's sweep slug** in its
paste-block example, so every adopter got a worked example naming a sweep that
exists in one repository.

`0.28.0` — **prove nothing is stranded; do not remember it — and `git-workflow`
owns how.**

The clear check asked *is anything left that exists only in this session?* and
rested on a claim that **by the time a slice closes, everything worth keeping
is on disk — the note, the index, the journal, the commit.**

**A commit on an unmerged branch satisfies all of that and is still
invisible.** A sweep lost forty-three skipped rows exactly that way: the slice
was committed, no pull request was ever opened, a detour began with a branch
switch, and the next slice branched from an integration branch that had never
seen it. **The check passed honestly and the record was gone.**

**So the question widens** — the session, the working tree, the branch, a
worktree, anywhere work can be stranded — **and most of it is checkable rather
than recalled.**

**How to check it is not this bundle's business.** `git-workflow`'s
`proving-work-landed` is the source of truth: the commands, the fetch, the
remote ref, showing the output, and the two levels of gate. **Every bundle
whose work can be stranded on a branch has the same problem**, and each
inventing its own commands produces a set of near-identical checks that drift.

*This bundle had already written the rule and walked past it —
`what-a-slice-produces` ends "How changes get integrated is not this bundle's
to say."*

**What stays here is the obligation and where it falls**: at a slice's close,
and again before the next branch is cut. Plus which sweep failures are worth a
hook — losing a slice's record is; a misrouted finding or a stale count is not,
because both are visible on the next read.

**And step 10 is now *land the slice*, not *commit* it.** A record on a branch
nobody merged is the same failure as one in a session nobody saved — one
`checkout` instead of one restart.

**The one thing no command reaches is the session.** You cannot grep for an
observation you failed to write, so it stays a judgement — and it is the one
that gets trusted. Making everything around it checkable leaves it standing
alone and visible instead of hidden in a row of equally confident claims.

`0.27.0` — **`What's next` and `Should you /clear` are two sections.**

They were one, and the clear decision sat at the tail of a paragraph — **the
only part of the message with an action in it, in the place a reader stops
reading.**

**One is a report; the other asks for an answer**, and the heading says so by
carrying the literal command. *Should you clear* is a question about
housekeeping; *should you `/clear`* is a thing to type. **The command is filled
in for whatever harness this runs in** — `/clear` in Claude Code, its
equivalent elsewhere, and where a harness has none, *start a fresh session*
with the paste block kept.

**And the clear answer is weighed, never asserted.** *A section that always
says yes is one a reader stops reading.*

**The weighing rule is `what-a-slice-produces`' and is cited rather than
restated** — both choices taxed, recommend the smaller. **What is specific here
is which taxes:** clearing costs a re-read of whatever the next slice needs and
this session already holds; carrying on costs the irrelevant context, paid
again on every remaining turn. It turns on how much of what is loaded the next
slice actually wants — almost none after a detour, most of it mid-cluster.

*Something existing only in the session is a defect rather than a cost.* Write
it down and then clear; it is never a reason to hold context.

**`What's next` over `How to proceed`**, because it is the question readers
actually ask.

**And the paste block gets a label on its own line, immediately above the
fence.** A fence at the tail of a long message with its instruction buried
mid-paragraph is a fence nobody notices. **A fence and never a blockquote** — a
terminal renders a blockquote with a prefix character on every line, and the
prefix comes along when the reader selects it.

`0.26.0` — **one status output, emitted at two moments.**

Where things stand, how to proceed, and whether to clear were written into the
close and **fired only at a close**. **It is the same message at the start of a
slice** — not a variant, not a subset — and the only difference is what
triggers it:

| moment | trigger |
| --- | --- |
| **a slice ends** | **automatic and unprompted**, every time |
| **a slice starts** | **only after a detour**, and then only when the reader asks to get back on track or you recommend it |

**Back-to-back slices get it once, at the close.** Saying it again immediately
is the same message twice with nothing between them to have changed it.

**`templates/slice-close.md` is now `templates/sweep-status.md`**, named for
the output rather than for one of the two moments that produce it. Its first
section is *what just happened* — the slice at a close, the detour at a start.

**A detour is the strongest case for clearing there is.** It loads context
built for something else, and none of it helps read the next file. **A close
asks whether the session still has value; the start of a slice already knows**
— whatever the detour loaded, the next cluster does not want it.

**And *what is next* is not answered by naming the next cluster.** *Prose, ten
files, cheapest available* is half of it; *and you can clear first, here is the
paste* is the half that saves the reader something.

**Found by running it.** A sweep spent hours on an unrelated estate-wide
rename, returned, and offered the next cluster with no mention of clearing —
having written the rule for exactly that situation four releases earlier.

`0.25.0` — **`lifecycle_status` is now `lifecycle`.**

**Same values, same meaning, shorter name**, renamed in the knowledge format
and carried here. The old name was chosen against `status` — so it never
collided with a tool's own `todo | in-progress | done` — and **`lifecycle`
avoids that collision equally well**, because the word at risk was `status` and
this name does not contain it.

**Breaking for an adopter**, shipped as minor under the pre-1.0 allowance:
**every Document declaring the old key has to be renamed.** It fails visibly
rather than quietly — `lifecycle` is unrecognised where `lifecycle_status` was
expected, and an unrenamed Document reads as having no lifecycle declared at
all.

`0.24.1` — **the template starts a new Document at `draft`, not
`provisional`.**

**The example value in a template becomes the estate's default**, and this one
was teaching every new Document to be born promoted. **The lifecycle ladder
measures what a reader is owed when a Document changes**, and use by its own
authors does not promote it — `provisional` begins when somebody who did not
write it can rely on it, and promoting is the author's explicit act.

`0.24.0` — **the slice close ends with priced options and something to paste.**

**Two parts where there was one.** *Whether to clear* was a paragraph of prose
carrying the only actionable content in the message, which is exactly where a
reader stops reading.

**And the row close is separated from the slice close.** They are two events —
a file ended, and the slice ended *because* it was the last one. Step 7d's line
stands alone with a rule under it; running them into one heading leaves a
reader unable to tell whether the slice was skipped, the file was, or both.

**What is worth the reader's attention gets a heading.** Consequences,
observations, and decisions that are theirs — including the ones deliberately
not taken. **An unheaded paragraph reads as commentary and gets skimmed**,
which is the opposite of what it is for.

**How to proceed is bullets with prices.** Each option gets its cost in a
clause — *seven files, roughly a slice's worth*; *one turn, changes how every
remaining slice runs*. **A reader choosing between three unpriced options is
guessing**, and the agent is the one who can price them.

**Then the clear decision in a sentence, and a paste block** — three or four
lines in a fence, because the reader is going to select it with a mouse.

**The paste is a pointer, never a handoff note:** the sweep's path, what to
read, what to invoke, where to resume. **If it needs to carry findings,
something was not written down** — the same test as the clear decision one line
above it.

**Found by running it.** A reader read a slice close, said the first two parts
worked, and named the rest: the middle wanted a heading, and the actionable
half was buried in a paragraph.

`0.23.0` — **a slice has a close routine: what it did, where the sweep stands,
and whether to clear.**

**What it did** in three or four lines — not the slice note, which is the
record, but the reader remembering what happened before choosing what is next.

**Where the sweep stands**, as a table with four rows — **closed**,
**skipped**, **open**, **untouched** — shown without being asked, because the
reader has spent the slice inside one or two files and needs the whole thing
back in front of them.

**Names in the first three rows, groups in the last.** A reader wants to know
which files are finished and roughly what is left; **ninety filenames under
`untouched` is not a status, it is the index printed twice.**

**The shape lives in `templates/slice-close.md`**, beside the presentation
template it is modelled on — a message shape rather than a document, and the
procedure points at it instead of carrying a second copy.

**Derived and never stored.** It is rebuilt from `coverage.md` each time and
discarded. Writing it into a file would be a third copy of what the index
already holds — and it would start rotting immediately, which
[[how-a-sweep-is-stored]] covers under counts.

**And it is asked to draw its own conclusion**, in a line: *two clusters closed
and none of `src/` reached* is the sentence the table exists to produce.

**Whether to clear the context** is the third part, and **a slice boundary is
the cheapest moment there will ever be to drop a session** — for a structural
reason: by the time a slice closes, everything worth keeping is already on
disk. That is what the preceding steps are for.

**So it is a check, not a judgement:** *is anything left that exists only in
this session?* If no, clearing is free and gets recommended. **If yes, that is
a defect rather than a reason to keep the context** — write it down, then
clear.

**Never inside a slice**, because the turn order depends on both parties
holding the same file. **And say so when the next slice is the same cluster**,
where orientation carries over and holding is genuinely cheaper.

**Found by running it.** A sweep produced this table once, unprompted, and the
reader asked to see it after every slice. Nothing in the bundle had asked for
it — which is the whole reason it only appeared once.

`0.22.0` — **a count in the charter is almost always wrong to write.**

**The charter is the file that should get truer, and a count never does.** It
is right when written and wrong the moment anything changes, with **nothing to
announce it** — a stale number reads exactly like a current one.

**This is the authored-and-derived test applied to a sentence rather than a
file.** The split decides which *file* something belongs in and is rarely asked
of a paragraph, so an authored file fills with derived sentences that rot at a
derived file's rate **with none of the reconciliation.** The test: *can this
sentence go wrong without anybody editing this file?*

**Point at the number, do not copy it.** Where one is already kept current —
the index, a version history, the repository itself — cite that place. A copy
is a second answer that goes wrong on its own.

**Not banned, and the exception is said out loud.** Some count may genuinely
earn its place, and forbidding all of them would be a guess about cases nobody
has met. Where one is written anyway, **the reader is told as it is written**:
that it is a count, that it will go stale, and why it is not in the index. **An
exception nobody was told about is indistinguishable from an oversight**, which
is how they accumulate — every one was written by somebody who thought that one
was fine.

**Dating it is not the fix.** *Forty-two files, as of slice 004* stops being
wrong silently and still never gets truer.

**Found by running it.** A sweep's charter accumulated eight counts, three
already false within a day — including one claiming *seventeen releases, six
files* when it was twenty-one and eight.

`0.21.0` — **fix now or route it is the reader's call, and the recommendation
is the agent's job.**

**Both choices are taxed, and the call is which tax is smaller.** Doing it now
taxes the session: context that does not belong to this file enters it and
stays, and **a slice that keeps paying that stops being about anything.** Doing
it later taxes the finding twice over — **the code moves**, so the note may
describe a version nobody can find, and **the context is gone**, because
framing rots faster than facts and a successor can re-derive *what was wrong*
but not *why it mattered here*.

**The economy decides between them.** A fix needing only what is on screen
costs one turn now against a full reload later plus the risk of rot. A fix
needing files nobody has opened costs that load whenever it happens — **paying
it here buys nothing and pollutes the slice for free.**

**Two turns is where the saving generally disappears** — a heuristic, not a
line. One turn is the fix, two is the fix and the check; past that you are
usually loading new context mid-slice, which is the *while I'm here* failure
wearing an efficiency argument. **The count is a proxy** for whether the fix
needs context nobody has loaded, and where the two disagree the context wins: a
three-turn fix inside an open file is still cheap, and a one-turn fix in an
unread subsystem is not.

**Never just ask.** *Fix it now, or route it?* with no recommendation hands the
reader an accounting problem they have no numbers for — **they cannot see what
the fix would cost and the agent can.**

**Two forces, and only one is the agent's to weigh.** Token economy is
computable — what the fix would load against what deferring would reload.
**Cohesion is not.** A slice holds together because it is about one thing, and
so does a reader's attention; whether they want to be pulled sideways right now
changes by the hour and nothing in the sweep can see it.

**And the strongest reason to overrule the economy is the reader's own
clarity** — *I understand this now and I will not understand it as well in a
fortnight* is a direct read on the rot tax, and only they can take it.

**That is a rational trade rather than an indulgence.** Tokens are renewable: a
session can be re-run and a context rebuilt, at a price that is only time and
money. **A reader's understanding right now is not** — it exists in one head at
one moment, and unwritten it is not recoverable at any price. **Spending tokens
to keep knowledge that would otherwise be forgotten is the economy working.**
The recommendation prices the context and cannot price the thing being bought.

So: **make the call on the numbers, hand it over, and do not argue the
preference.**

**One case overrides the economy: a fix that edits the file under review.**
Until it is shown and re-confirmed, the reader is holding a verdict on a state
of the file they have not read.

**And routing defers the fix, never the record.** The finding is written either
way; it was never part of the choice.

`0.20.0` — **a file closes on a verdict, never on momentum.**

**An instruction to act is not a verdict on the row.** *Drop it. Fix that.
Next. Proceed.* Every one is direction about the work and none says what the
index should record — and acting on the instruction while inferring the row is
how a file gets marked by the agent with the reader believing they never said
so. **Three things close a row**: a sign-off, a statement that the reading is
done, or a skip with a reason.

**The per-file loop is step 7, written as a gate rather than as advice.** Show
what changed and how to check it, ask for what this sweep's `approval` calls
for, wait, then say out loud who closed the row and with what. **A re-opened
file needs all of it again** — it is not still closed from before, because
whatever brought the reader back may change what they want it to say.

**Two mechanisms rather than an argument**, because prose that argues is what
kept getting drifted from. **The gate is repeated at step 3**, where the
violation actually happens: presenting the next file is the act, so the check
sits there and not only beside the rule it enforces. **And closing a row
requires stating who closed it and with what** — a row closed by inference
produces a sentence with nobody in it, and that sentence is unwritable before
it is noticed.

**Step 7c lists what is not a confirmation**, by the words readers actually
use: *proceed*, *next*, *drop it*, *merge it*, *agreed*. Every one leaves the
row open. Ambiguous wording is not a confirmation either — **guessing right
nine times does not make the tenth safe.**

**A diff command has to run from where the reader is standing**, unmodified,
and the writer runs it first. A command that needs repairing is worse than
none: they discover it was wrong only after deciding to trust it. Reflowed
prose wants `--word-diff`, or a line diff shows every paragraph that moved and
buries the words that changed.

**Also: step 8 still described `reviewed` and `approved` as statuses**, which
0.18.0 replaced with three columns four releases ago. The procedure was telling
a reader to write a shape the type no longer has.

**Found by running it.** A sweep dropped a document on the instruction *"drop
standards.md"*, and the agent set the row itself without ever asking what it
should say.

`0.19.0` — **a slice that removes a document owes a ledger.**

**A removed file cannot be re-read**, so what a slice concluded about it is the
only surviving record of what it held. Everything else a slice produces can be
checked against its source; this cannot.

**Two rules.** The removal and every destination its content reached land in
**one commit**, so the diff is the whole story rather than two diffs that do
not mention each other — and it fails safely, because a half-landed scatter
leaves live references pointing at a file that is already gone.

**And every range of the removed file gets a verdict**: moved, rewritten,
dropped as duplicate, or **dropped as wrong**. That last one carries no
destination on purpose, and **a diff cannot tell it from content lost by
accident** — both are red lines with nothing corresponding anywhere. The ledger
is the only thing that separates them, which is what lets somebody trust a
removal they did not perform. A *dropped as wrong* row names what it was
checked against, so the reader can go and look rather than take your word.

**Proportional to what was removed**, not to the sweep: a stub nobody cited
needs a line; a document eleven files point at needs every range accounted for.

**Found by running it.** A sweep deleted its own repository's first document,
and the reader asked to be able to verify afterwards that the right things
survived — which a diff alone cannot answer.

`0.18.0` — **a row records three facts, not one status.**

**Reading, sign-off and what was found are different things**, and one column
could not carry them. `reviewed_by`, `approved_by`, `outcome` — **empty means
it has not happened**, so there is no `pending` value able to drift out of step
with the actors beside it.

**It makes a common state visible that a single status hid.** `reviewed_by:
agent:opus-5` with `approved_by: human:fsmith` is *an agent read the file and a
person signed off without reading it* — which is the declared arrangement
wherever a sweep says the reader takes a summary rather than the file. **Plain
`approved` silently claimed the person read it.** The reverse matters too: read
closely, approval withheld, is an ordinary and honest place for a row to stop.

**`outcome` is past tense, deliberately.** *This reading found problems* stays
true however often the file is fixed afterwards. A column describing present
quality would have to be maintained as files are fixed — **coverage tracking
fixing rather than reading** — and would duplicate what the backlog already
holds.

**Two values, and not a ladder.** Severity and what to do about it are the
finding's job; `outcome` answers only *did this read produce anything*, which
is the question a close needs and nothing else records in one place.

**And the charter says how strongly sign-off is expected** — `approval:
required | recommended | optional | prohibited`, RFC 2119's ladder borrowed
whole, because a reader who has met must / should / may / must not anywhere
else already knows what the rungs mean. **Not every sweep wants a signature**:
an agent-agent sweep cannot have one, and one aimed at coverage rather than
endorsement does not need one. **Assuming it is wanted turns every unsigned row
into a shortfall nobody intended to fill.**

The counts print under all four; what the field decides is whether *twelve
reviewed and never signed off* is a failure, a known compromise or a plain
fact. **Nothing is hidden by any value**, which is what makes a permissive
default safe. `recommended` is that default, because wanting sign-off
everywhere and not getting to all of it is the ordinary case for a sweep with a
person in it.

**`prohibited` is the one rung with a defect of its own.** Under it unsigned
rows are the expectation met and go unreported, but **a signature that exists
is reported at close as a defect** — somebody claimed an endorsement the sweep
had ruled out. That is why it is not spelled `unused` or `excluded`: those
describe a column nobody filled in, where this one says *do not sign these off*
and means it.

**Breaking**, shipped as minor under the pre-1.0 allowance: one column becomes
three, and the charter gains a field. Every previous state remains expressible,
plus one that was not.

`0.17.0` — **`strictness` becomes three disciplines, and adaptive is the
default.**

`strictness: adaptive` said the strictness was adaptive, which is nonsense —
**a field names the thing being held fixed, not the value.** And one flag was
too coarse: **goals, scope and strategy move independently.** The common mature
configuration is **strict goals, strict scope, adaptive strategy** — do not
wander, but do improve how you read.

So: `goal_discipline`, `scope_discipline`, `strategy_discipline`, each
`strict`, `adaptive` or `exploratory`.

**The three values are a ladder of what you already know**, which is the only
line that holds — *how much change feels warranted* is undrawable, because
every improvement feels warranted in the moment. `strict`: you know what you
are doing, so do not touch it. `adaptive`: you know the shape, so refine and
tune it. **`exploratory`: you do not know the shape yet, so go and find what it
should be.**

**`exploratory` cannot be estimated**, and that is a property rather than a
failing: a sweep still working out what it is has nothing to estimate against,
and a number produced anyway was never true. Disregard for time is the
consequence of not knowing, not the definition.

**Three flat fields rather than one nested record**, so each can declare a
`field_type` and be validated. A record would have to say `field_type` cannot
express it, which is a known gap in the format and not worth inheriting where
the shape does not require it.

**Absent means `adaptive`, on every axis, because that is what actually
happens.** A sweep that has not thought about this will adapt — and a default
of `strict` would have sweeps sprawl anyway while the record claimed a
discipline they never had. **An honest record of sprawl is worth more than a
flattering one.**

**Most *mature* sweeps should be strict on goals and scope**, and the default
should flip once that is the common case. Until then it describes behaviour
rather than aspiration, which is the only way a field stays worth reading.

**Breaking**, shipped as minor under the pre-1.0 allowance: one field becomes
three. Nothing else changes.

`0.16.0` — **the authored file is `charter.md`, not `sweep.md`.**

**A filename outlives the vocabulary around it.** It is linked, bookmarked,
cited in commit messages and pasted into conversations, so it is the part of a
practice most expensive to rename later — and *sweep* is a word this bundle may
well abandon.

**`charter` names what the file actually is**: a written statement of the aims
and principles of an undertaking. It begins as intent — goal, scope, strategy,
strictness — and ends as account, carrying the learnings and the closing
summary. **Nothing else in the world records either half.**

*`README.md` was the most legible candidate and was rejected*: this estate
already says never make a README load-bearing, because people edit them without
knowing rules exist. Overriding that for one directory needs a bigger
conversation than a filename.

**The type stays `sweep`.** It names the practice, and if the practice is
renamed the type goes with it — which is fine and expected. The filename is the
cheaper thing to make durable.

**Breaking**, shipped as minor under the pre-1.0 allowance: an existing sweep
renames one file. Nothing inside it changes.

`0.15.0` — **`evolving` becomes `adaptive`.**

**`evolving` was compatible with the failure the rule forbids.** Things evolve
on their own, over time, without anybody deciding — which is drift, and
`0.14.0` says two paragraphs later that a sweep must never drift into moving
its own goal. The word permitted what the rule prohibited.

**`adaptive` implies adapting *to* something.** The plan moves because the
sweep learned, not because time passed. It also pairs with `strict`: both are
adjectives describing a posture a sweep is declared to have.

*`adapting` was considered and rejected — a participle describes an activity in
progress, and this field declares a disposition chosen before anything has
adapted.*

Minor: one enum value renamed, shipped as minor under the pre-1.0 allowance. A
sweep declaring `evolving` reads correctly to a person; nothing parses it yet.

`0.14.0` — **the bundle declares `survival: experimental`.** Nobody has
finished a sweep. The practice has been corrected at every turn by the one that
is running, and the honest statement is that it may not earn its keep — LKF's
`experimental` says exactly that: *no intentions, out in the world to find
out.*

`lifecycle_status: draft` was already saying half of it. **The two answer
different questions** — draft says how settled the writing is, `experimental`
says how much to expect it to last — and this bundle is genuinely both.

*It is the first bundle in this catalog to declare `survival` at all, which is
appropriate: it is the one with the least claim to permanence.*

Plus **a sweep declares whether its own plan may move.** — **a sweep declares
whether its own plan may move.**

**`strict`** fixes the goal, scope and strategy for the duration.
**`evolving`** expects them to move as the sweep learns. **Both record
everything they find** — the difference is what they do about the findings that
would rewrite the sweep itself.

**A strict sweep is not a blind one.** It routes findings exactly as any sweep
does; what it declines is redirecting itself. *That is a real observation and
this is not the sweep for it* is a legitimate journal entry.

**Choose `evolving` when the practice or the material is genuinely new, and
expect to pay for it.** The first sweep ever run was evolving and produced
**thirteen releases of this bundle while covering six files** — correct for a
first sweep and ruinous for a tenth. **Most sweeps should be strict**: once
neither the practice nor the material is new, evolving is a licence to be
distracted by whatever is more interesting than the next file.

**And it is declared, never drifted into.** A sweep that quietly starts
rewriting its own goal was evolving all along and nobody said so — so nobody
budgeted for it, and its estimate is wrong for a reason the record does not
show.

Minor: a new required field, a step in starting, and a line in the slice loop.

`0.13.0` — **an optional `journal.md`, for the space between noticed and
concluded.**

**A finding routes out at the slice that produced it; a learning goes in the
sweep once it is settled. Neither holds a suspicion that spans three slices and
is not yet either** — a pattern starting to show, a term that may be retired
with nothing enforcing it, a claim to verify when the right file comes up.

**It is authored and spent, which is the third combination.** `sweep.md` is
authored and kept. `coverage.md` is derived and spent *because it regenerates*.
The journal is spent because **its contents graduate**: an entry that mattered
became a finding, an idea or a learning, and one that did not was never worth
keeping.

**The failure to watch for is that it becomes a queue**, which is the exact
pile [[what-a-slice-produces]] exists to prevent — *filed by nobody, because
the reasoning that made each one worth capturing is gone within a day*. So:
anything actionable goes to its real destination at the slice that produced it,
and **an entry still sitting in the journal three slices later, while being
actionable, was routed wrongly rather than journalled correctly.**

**`close-a-sweep` reads it and empties it.** Its step for things trapped in
notes is exactly this file: every entry leaves or is dropped deliberately, and
the journal goes with the sweep either way.

*Optional. A sweep that does not want one does not have one, and nothing here
degrades without it.*

Minor: a new optional file, its type and template, and one step in closing.

`0.12.0` — **the index is derived *given the strategy*, and the strategy has to
be written down.**

**`0.11.0` claimed `coverage.md` rebuilds exactly. It does not, unless the
rules that produced it are stated** — and one of them routinely is not. Scope
decides which files get rows and who-reads-what decides a column, but
**clustering decides which cluster a row lands in, and it usually lives in
somebody's head.**

**Clusters are not derivable from paths**, which is why they get left unstated:
grouping feels obvious while you do it. A cluster groups **what must be
understood together**, and that is routinely not what sits together — four
documents in three directories may answer one question, and one directory may
hold three clusters sharing nothing but a path. Found by checking a real
sweep's clusters against the tree and watching a directory rule fail on every
one.

**So a sweep names its clusters and says what each is about**, and **a file
that fits none of them means the strategy is incomplete.** Add the cluster to
the sweep rather than improvising one in the index — improvising is how an
index quietly stops being a cache and becomes a record of judgements nothing
else holds.

Minor: new content in the layout policy, both procedures and the sweep template.

`0.11.2` — **retention is stated, and why it is safe.** An audit is kept
indefinitely because the exchange *is* what it produced — discard it and
nothing else records that anybody was accountable for anything. A sweep is
**spent**: everything worth keeping left at the slice that produced it, so what
remains is bookkeeping, and it is archived then deleted like anything else in a
backlog.

**A sweep still holding something worth keeping has failed to route it**, which
is a defect in the sweep rather than a reason to preserve it.

It is the same test that separates `sweep.md` from `coverage.md`: could this be
rebuilt, or would losing it lose something nothing else records? **An audit
fails that test by design; a sweep is built to pass it.**

Patch: background only. It sharpens a claim `0.1.0` already made — *churns,
then evaporates* — and obliges nothing new.

`0.11.1` — **progress goes above the index in `coverage.md`.** The summary a
reader wants is *how far along*, and a table of every file in scope should not
sit between them and it. Detail below the thing that summarises it, as in any
document.

Patch: the same content, in the order a reader needs it.

`0.11.0` — **the index moves out of `sweep.md` into `coverage.md`.**

**One is authored and the other is derived**, and everything else follows.
`coverage.md`'s rows are the scope rule applied to the tree and its statuses
are what the slices record — **delete it and it rebuilds exactly.** `sweep.md`
is derivable from nothing: delete it and the goal, the reasoning and the
learnings exist nowhere else.

**So they lag differently.** A derived thing ages with every commit, which is
what reconciliation is for; an authored thing changes only when its author
changes their mind, and should get *truer* as the sweep teaches something. **A
stale index is ordinary. A stale sweep is a defect** — it says the sweep is
aimed at something it is not.

**A derived file must not live inside an authored one**, or nobody can tell
which half has gone off. **The test, where something is ambiguous:** could this
be rebuilt from the repository and the slices? If yes it is coverage; if losing
it would lose something nothing else records, it is the sweep.

The practical annoyances follow from that rather than motivating it: a `git
diff` of the sweep's thinking buried under status changes, and a rebuild of the
index putting the reasoning in its blast radius.

**The scope rule stays with the sweep; the enumeration goes with the index.**
*Everything tracked except the generated adapters and the vendored bundles*
does not change when a file is added — the list of rows does, and is supposed
to.

**`indexed_at` moves too**, because it is a fact about the index. `sweep` now
carries no commit at all, which is right: a sweep is true of a moving target by
construction.

**Breaking**, shipped as minor under the pre-1.0 allowance: an existing sweep
has to split its file in two and move `indexed_at`. The rows move verbatim.

`0.10.0` — **what the first slice taught, once it had run.**

**`cross-check` is a method rather than a habit.** In the first sweep ever
conducted, **every mechanical finding came from executing the thing a document
described** — `--help`, the rules on disk, the code behind a claim about it —
and none from reading attentively. Careful reading found only the claims
nothing could verify. **A document is most confident exactly where nobody has
checked it.** So: prefer a check you can run over a claim you can only read,
and say when there was none, because *I could not verify this* is a finding
about the file's checkability.

**`commits` decides which question to ask.** A file with one commit cannot have
drifted, so *did this rot* is unanswerable and *was this ever true* is all that
is left. **Sweeps aimed at churn quietly assume every file has a history**, and
new files are exactly where that fails — three of the first slice's four files
would have been out of scope under its original goal.

**Which is why correcting the goal is a legitimate outcome of a slice.** A goal
is written before anything has been read; the early slices are the first
evidence it was aimed correctly. Change it in the sweep, say what the slice
found, and **say how many of that slice's files would have been out of scope
under the old goal** — that is the measure of how wrong it was.

**A sweep does not review its own record.** A scope of *everything under
`.luma/`* grows the sweep's own index and slice notes inside itself, and
**approving your own coverage ledger proves nothing about coverage.** It
appears mid-sweep rather than at the start, so reconciliation adds those files
as ordinary pending rows without noticing what they are.

**Progress counts are derived, never typed.** A wrong number in a progress
table is precisely the rot the writing conventions warn about, and it is the
one table a reader trusts without checking.

**And the practice gets fixed in batches, never mid-slice.** The first slice
spent its first three files on presentation rather than on documents. **That is
what a `draft` practice costs once**, and only once — a second slice producing
as many changes to this bundle as findings about the code is a sweep that has
stopped sweeping.

**And the rate is re-measured at every slice rather than once.** It costs a
count of rows, so the only argument for waiting was that an early number is
noisy — which is a reason to present it honestly, not to withhold it. **A range
with the number of slices behind it, never a point estimate**: *three slices,
four to nine files each* is honest at small samples where *2.1 files per slice*
is false precision a reader will plan against. **Slices that measured something
else are discarded and said to be** — a first slice of a `draft` practice
measures the practice, not the material.

Minor: new content, and one procedure step added.

`0.9.1` — **examples name a fictional person, not a real one.**

`templates/sweep.md` and [[how-a-sweep-is-stored]] carried a real workstation
account, taken from a filesystem path. The catalog already had a convention for
this — `human:fsmith`, used across five bundles — and it was missed.

**Two faults, and they are separate.** Naming a real person in a published
example is a **disclosure**, and in some organizations a workstation username
is secret. And the value came from the **OS user** rather than a git or forge
identity, which is wrong provenance anywhere: the logged-in account is not
necessarily who acted.

**Patch, and it needed to be one.** *Examples only* was the wrong reason not to
bump — an adopter whose vendored copy carries the leaked value has no way to
learn a fix exists unless the number moves, which is the whole point of a
version.

`0.9.0` — **opening a file is often the reader's job, and the file is live
while you present it.**

**`0.8.0` said *run the command; do not print a path and hope*, which is wrong
whenever the reader's editor runs in a terminal.** An agent whose `EDITOR` is
`vim` cannot open anything — a non-interactive call has no terminal to give it,
so the attempt hangs or dies. **Printing the reference is not a failure to
help; it is the mechanism**, because the reader's terminal already knows how to
resolve one. It is also better: nothing steals focus, and they open what they
want when they want it.

**So references are written in full — `path/to/file.md:10`, never a bare
`:10`.** Terminals that turn a reference into an editor jump match a path
followed by a line; an offset alone matches nothing and cannot be made to. It
costs the agent nothing and decides whether a reference opens or has to be
retyped.

**The file is live while you are presenting it.** A reader in deep mode has it
open and may edit while you talk — the arrangement working, not a problem. But
**the copy you presented is already history**, so re-read before editing rather
than applying changes against remembered text. That failure looks like a no-op
rather than an error, which is why it needs saying.

**And a finding may be about more than the file it was found in.** A claim
repeated in six places is a finding about all six. **Route it at its real scope
and say where it was found** — but do not chase it inside the slice, because
following a finding out of the sweep's scope is how a slice becomes an
afternoon.

Minor: new content, and one instruction corrected.

`0.8.0` — **how a file is presented, and going first as a declared
arrangement.**

**Found by the first slice, which spent its first three files arguing about
presentation rather than about the files.** [[presenting-a-file]] settles it,
with [the shape in a template](templates/file-presentation.md) for both modes:
**one file at a time** — a cluster presented at once buys nothing, since the
reader can only read one while the others scroll away — then a data block, a
summary of what the file *is*, what the agent makes of it, and **only then the
file opened.** A reader wants to know what they are looking for before they
change windows.

**The data block has to earn each row**, and the one that repays most is
`cross-check`: a documented list against the code it lists, a count against
what it counts, a flag against `--help`. **It is where a stale document
announces itself, and it costs one command.** The starting set is six rows and
is explicitly not a contract.

**Open the file rather than printing a path.** A path is clickable in some
terminals and not others, and a reader who has to select and paste has been
given a chore. Ask once what opens files on this machine, then use it — at the
line under discussion, not the top.

**Deep and shallow are different presentations**, declared per area beside the
pairing: deep gives the file in full and says what to attend to, shallow
summarises and says what is wrong.

**And going first is now a declared arrangement rather than a per-file
exception**, which closes a gap this sweep recorded before its first slice. A
reader may decide at the start that a whole area works that way — *show me the
file with your read attached* — and it is roughly twice as fast. **What it
costs is not nothing**: anchoring still operates, and some of what they would
have seen unaided is gone. The protection is reduced rather than removed,
because they have the file itself. **So it is declared, never drifted into** —
a sweep that slid into it one file at a time lost the property without anybody
choosing to.

Minor: new content, and one procedure step restated.

`0.7.0` — **a row finishes two ways, and challenge is not veto.**

**The bundle never said who sets a status**, so an agent filled the gap with
*the process decides* and started policing whether a proper slice had happened
— refusing a status over a file the reader had read, written, and pronounced
good. **The bundle exists to protect the reader's judgement, and it was being
used to overrule it.**

**One status could not carry it.** `reviewed` names a process, which invites
the question *was a real review done* — the argument the agent picked.
`approved` names a judgement, and a judgement implies somebody making it.

**So there are two, because they are two different acts.** `reviewed` is *I
read this and it is fine*, and **any party may say it, an agent included** —
without that, [[who-does-the-reading]]'s agent-agent sweep could not finish a
row, since a status only a person can give would strand every one of them at
`pending`. `approved` is *signed off*, and **only a person may give it**.

**Neither party may withhold a status the other is entitled to set.** An agent
records `approved` whatever it thinks and however the file got that way. Its
own view lives in `reviewed`, where it has no veto over anybody.

**A `pairing` field declares who is in the sweep** — `human-agent` or
`agent-agent` — before the first slice, and a slice may declare its own where
it differs. **Every row now records its actor** as well as its status, because
`reviewed` by an agent and `reviewed` by a person are different facts. The two
are not redundant: the status says how strong the claim is, the actor says who
made it, and **a person may legitimately mark a row `reviewed` rather than
`approved`** — *read, fine for now, not signing off* — which an actor alone
cannot express.

**The declaration and the actors come apart, and that gap is the useful part.**
A sweep declared `human-agent` whose rows are all `agent:` became something
else without anybody deciding, so the close reports coverage by actor.

**What this does not solve, and says so:** two sessions of one model both
record `agent:opus-5`, so the index cannot show the independence the
arrangement rests on. `audit-records` hit the same wall and declined to invent
a field in passing; that reasoning holds, no agent-agent sweep has run, and
until one does the disclosure belongs in a slice's prose. The trigger for
solving it properly is somebody needing to check an independence claim and
being unable to.

*`covered` was considered for the agent-side status and rejected: like
`reviewed` it is process-shaped, but unlike `reviewed` it is also the noun the
index measures, and using one word for the measure and the act is what let them
collapse in the first place.*

**Challenge is the job; veto is not**, and [[the-pairing-turn]] now says what
the reader is owed: brutal honesty, a better idea argued for, the goals they
may have forgotten on a run this long, and ways to sweep faster. It also says
where that stops — *did you consider X* is the agent's to ask, *this is not
approved* is not its to say. **Raising a concern twice after it has been
answered is the veto wearing a question mark.**

**Rows are independent**, which is the flaw the same conversation exposed. If a
row could only be approved once everything it linked to was, then a project
where content moves — a document split into four — becomes one where nothing
can ever be approved, because every approval drags in more. A split owes a
**note** that the new rows exist and which approval created them; it does not
owe a dependency.

**And a slice now records what it half-finished**, in
[[what-a-slice-produces]]. Content that moved and work that was started and not
completed both get written where the next slice will meet them. **A sweep that
generates its own loose ends and does not track them is worse than one that
changed nothing**, because the index looks complete.

*A `rewritten` status was considered and rejected. A file rewritten with its
author present and approved by them is covered — that is what having a reader
is for, and the status was solving a problem that only exists if you distrust
them.*

Minor: new content, and one status value renamed. An index using `reviewed`
still reads correctly to a person; nothing parses it yet.

`0.6.1` — **references to the knowledge format name sections instead of
numbering them.** The format removed section numbers, so every `§n` here
pointed at a position that no longer exists — and a stale number resolves to
the wrong section rather than to nothing, which is why none of them were
reported. Decorative citations are dropped; the rest name what they meant.

Patch: wording only. No rule, field or procedure changed.

`0.6.0` — **the comparison with audits is a background document, and it is no
longer wrong.**

**Three of its five rows had gone false in `0.5.0`.** It still said fixing
happens in the slice, that independence is *impossible, and not wanted*, and
that a sweep is one person reading for themselves — all true when written, all
untrue within a day. A comparison table is exactly the shape that rots quietly,
because nothing breaks when it does.

**Rewritten around what actually separates them.** An audit answers a question
and can be complete after three files; a sweep covers a territory and is
complete only when every row is accounted for. **The one to remember is
obligation** — an audit puts somebody accountable on the hook to answer every
finding, and a sweep puts nobody on the hook at all. The lifecycles follow from
that rather than standing on their own.

**Both need independence, for opposite reasons**, which is the part worth
having written down: an audit's protects against self-grading, a sweep's
against anchoring. Same mechanism, different failure, and a sweep needing it at
all is days old.

**It is `concepts/`, and the bundle's first.** The argument had grown longer
than the rule it justified and was sitting in the entrypoint policy, so every
reader of the bundle paid for an audit comparison most of them were not asking
for. Background is read *through* the rules that reach it, and the operational
half — *do not file a sweep as an audit* — stays in the policy where somebody
about to do it will meet it.

**It lives here rather than in `audit-records`, and there is no second copy.**
Audits are a known practice; sweeps are not, so the new one is what has to say
what it is not. Two copies would drift, which is a finding rather than a merge.

Minor: new content and a correction to prose that had gone stale.

`0.5.0` — **the parties, and what each of them may do.**

**A sweep records; it does not rewrite.** It used to route *this is wrong and I
understand it* straight to a fix in the slice's own branch, which spent the
sweep's output on the replaceable half of the work — **a finding outlives every
attempt at it**, while a fix can be wrong, superseded, or better made by
somebody with context the reader never had. Fixing also pulls you out of
reading, which is what the slice was for.

**A fix may land during the sweep only where a person is in it and says so.**
Otherwise nothing lands: a third party works from the record afterwards,
separate from both sweep parties on the same reasoning that separates the
reader from whoever orients. **The gap is the point rather than the overhead**
— it is the only moment anybody can look at the findings as a set before code
has moved, drop the wrong ones, merge the four that are one finding, and notice
the one that changes what the others mean.

**A proposed fix is a suggestion, not law**, for two independent reasons. It
has no standing — the reader saw the file for twenty minutes and whoever fixes
it may own the subsystem — and **it is stale from the moment it is written**,
staler by the day, with the gap longest exactly where nobody human ever saw the
file. So the reasoning is recorded rather than only the diff: a stale diff is
worth nothing, while stale reasoning can still be read and judged in a minute.
Whoever fixes re-derives, and *not fixing it* stays a legitimate outcome.

### Neither seat has to be human

The bundle assumed a person reading with an agent, and said so in language that
made anything else read as a degradation — *no human here is the signal*, *a
sweep is a person reading their own system*. **The turn order was never about
humanness.** It exists because a reader shown findings first is framed by them
and forms no independent view, which is a property of reading. If anything it
binds harder between two agents: an agent handed a findings list agrees more
compliantly than a person would, with no irritation to push back with.

**So the parties are now the reader and whoever orients**, and the language
throughout says *reader* where it said *person*. Independence is the
load-bearing property, and it is **the session rather than the model** — one
session playing both parts is not a weak sweep, it is one agent reviewing with
extra steps, and claiming otherwise asserts a property the record does not
have.

**Three things change when no human is in it**, none of them a prohibition. The
goal stops being optional, because *I want to know this system* is checkable by
the one who wanted it and there is no such fallback with two agents. Nothing is
retained, so an agent-agent sweep is worth exactly the artifacts it left. And
**the agreement check loses its observer** — the tell is a reader who agrees
with everything, which assumes somebody notices, so it now has to be run
deliberately by reading back three slices and asking whether the reader ever
disputed anything.

**Landing changes with nobody human in the loop is not forbidden here**,
because what gates a merge is the project's business rather than this bundle's.
It is named for what it is: an unsupervised agent editing a codebase with a
review-shaped record attached.

Minor: new content and a vocabulary shift. Nothing an adopter must do has
changed, and a human-agent sweep behaves identically.

`0.4.1` — **concurrent sweeps are ordinary when they share neither owner nor
territory.** The old wording led with *permitted, and usually a mistake* and
then granted an exception, which made the common case read as a tolerated
deviation. It also missed a dimension: it spoke only about overlapping scopes,
never about who is reading.

**The scarce resource is attention, and the failure is about the reader rather
than the count.** Two sweeps are fine; one person running two is not. So the
rule now states the ordinary case first, names the actual failure second, and
gives one test — **overlap in either owner or territory collapses two sweeps
into one.**

Patch: a clarification. Nobody who read the old wording correctly behaves
differently.

`0.4.0` — **`sweep_session` is now `slice`, and a slice is no longer a pull
request.**

**The name failed twice for the same hidden reason**, which was worth finding.
`sitting` and `session` both named *the human experience of doing the work* —
you sit down, you have a session — and the thing is not defined by the
experience. It is defined by the material: you stop when the cluster is read,
not when you are tired. **A slice is material-side**, it implies the whole it
was cut from and the siblings beside it, and it needs nobody taught.

**It also settled a design question the word was quietly hiding.** *Slice* and
*pass* differ on whether the same file can be covered twice — and the bundle
had it both ways, with an index that partitioned and a reconciliation step that
sent rows back to `pending`. **Slices partition the sweep**: each file is read
once, and re-covering is an exception the index records with the earlier slice
named. So `review-next` no longer resets a row unilaterally — it says what
changed and asks, because the person who read it is the one who can tell.

**The gain is visibility.** A ledger that churns silently looks the same at 60%
whether nothing drifted or half of it did.

**A slice is not a pull request boundary**, which was the last of the four
flagged guesses to fall. Most slices produce no change at all — *reviewed and
clean* is the common result — so the rule generated empty pull requests and
buried the ones that mattered. The two sizes answer different questions: a
slice is sized by what you can comprehend together, a pull request by what
reviews well. **Fixes now batch by kind across slices**, which is also how the
sweep learns, since slice 009 routinely reveals that 003 and 005 had the same
problem. The only surviving constraint is staleness — do not read on top of
your own large unlanded pile — and integration is left to `git-workflow`.

**The path is `.luma/backlog/sweeps/<slug>/`.** It was `reviews/`, which was a
slip: the container should carry the parent's name.

**A sweep is now aimed at something.** It had a scope and no goal, which meant
nothing to check a slice against on a run that takes weeks — *read the whole
project* is the method, not the reason. `start-a-sweep` asks what should be
true afterwards before it asks what to cover, pushes once for an observable
version, and takes the honest vague answer if that is what there is. The `goal`
field is what a drifting sweep is compared against: three slices running that
do not touch it mean the goal was wrong or the sweep has wandered, and neither
is visible without it.

**The estimate now warns about churn, not just length.** A sweep that takes six
weeks reviews a codebase that gets six weeks of commits, and nothing said so
until slice nine when rows started coming back. `start-a-sweep` measures how
much of the scope moved in a window the length of the estimate, names the hot
areas rather than reporting one percentage — churn concentrates, and the
average hides the only part worth acting on — and offers the three responses,
of which *freeze it* is available more often than people expect on a project
with two committers. **The number is a prompt rather than a forecast**: a
migration that just finished looks identical in the log to one that is half
done, and only a person can say which it was. `close-a-sweep` compares the
prediction against what actually drifted.

**Two smaller additions.** Orientation now has to disclose its own uncertainty
— a confident wrong orientation frames the person's read exactly as a verdict
would, so unfamiliar territory is a reason to orient *less*, not harder. And a
first sweep is asked to note where the practice fought it, since the bundle is
`draft` and that is the only way the remaining guesses get corrected.

**Breaking**, shipped as minor under the pre-1.0 allowance: the type, three
documents and the directory are renamed, the storage path moved, and `sweep`
gains a required `goal`. No adopters, so the migration cost is zero.

*On the name: the full form is a **review sweep**, the short form a **sweep** —
each half of the compound covers the other's blind spot, since* review *says
nothing about coverage and* sweep *says nothing about depth.*

`0.3.0` — **`sitting` is now `sweep_session`, and the bundle is marked
`draft`.**

**The old name had to be taught.** *Sitting* was invented vocabulary carrying
no clue about what it belonged to, so a reader met it cold and either guessed
or looked it up. `sweep_session` says what it is, and the compound is always
qualified — it never appears as a bare *session*, which this estate spends on
agent sessions.

**The rename surfaced the thing actually missing**, which was never a name: a
sweep session and an agent session do not line up in either direction. One
cluster can span three conversations; three clusters fit in one long
conversation when the material is prose. So a sweep session closes when the
cluster has been read, argued about and routed — **never because a conversation
ended, and never held open because one is still going.** That is now stated
where the units are defined.

**`lifecycle_status: draft survival: experimental`**, which should have been
there at `0.1.0`. Nothing has run a sweep; two of four flagged guesses have
already been corrected by a single conversation, and a bundle changing that
fast is not `provisional`.

**Breaking**, shipped as minor under the pre-1.0 allowance: the type `sitting`
is renamed, and `policy/what-a-sitting-produces` and `templates/sitting.md` are
renamed with it. The `sittings/` directory becomes `sweep-sessions/`. There are
no adopters, so the migration cost is zero — but it is a rename and reads as a
mistake later if not said.

`0.2.0` — **first contact, and two of the four guesses were wrong.**

**A person steering the sweep was treated as drift.** The orders were all
computable — narrative, risk-weighted, dependency, directory — so *I want to
look at the transport layer today* had nowhere to be recorded and read as a
failure of discipline. It is neither: for somebody who knows the system, their
instinct about what to read next is better information than any rule written
down at the start. **`led` is now an order**, with the discipline that keeps it
honest — look at what is still pending before choosing, so the choice is made
with the cost visible. That is the only difference between steering and
avoiding. Led-over-a-backbone is named too, because it is the common real
shape.

**The estimate was computed from a file count**, which is the wrong denominator
by more than an order of magnitude. A hundred short documents is days; a
hundred files of concurrency logic is months; the old arithmetic said the same
number for both and would have mis-sold the sweep in both directions at once.
**Estimate from the material, split the estimate when the scope is several
kinds of thing, and stop guessing after the second sweep session** — a measured
rate is worth more than any care taken over the initial band.

**The related claim went with it.** *A sweep session that covers thirty files
is a skim* was false for prose. The bound is comprehension, not a count: could
you still say what each file did afterwards? A sweep session of three dense
files fails that as easily as one of thirty pages.

Minor: new content and two corrections. Nothing an adopter must do has changed,
and a sweep run under `0.1.0` is still valid under this.

`0.1.0` — **nothing has run a sweep yet.**

It was written straight into this catalog rather than in the project that
wanted it, which is a legitimate route and has a known cost: the conventions
here are reasoned rather than observed, and the parts real use would have
sanded down are still sharp. Stating that is how the cost is managed, so it is
stated here rather than discovered by the first adopter.

**The parts most likely to be wrong**, named now so the first sweep can watch
for them:

- ~~**Three to eight files per sweep session**~~ — wrong, and corrected in
  `0.2.0`. It was an application-code number stated as a universal one.
- ~~**One pull request per sweep session**~~ — wrong, and corrected in `0.4.0`.
  Most slices produce no change at all, so it generated empty pull requests.
- **The index as a table in one file** is chosen against this estate's usual
  one-file-per-item instinct, on the grounds that a coverage ledger's whole
  value is being readable at a glance and that a sweep has one writer. If sweeps
  turn out to run with several readers at once, that reasoning fails and the
  shape has to change.
- **Whether `close-a-sweep` earns being a procedure** rather than a paragraph.

**No retention period for archived sweeps**, deliberately. Nobody has run
enough of them to know what one should be, and a number invented now would be
enforced for years on no evidence.
