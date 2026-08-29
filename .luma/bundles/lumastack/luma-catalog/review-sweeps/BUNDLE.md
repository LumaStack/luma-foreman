---
type: bundle
version: 0.9.1
published: 2026-08-28
lifecycle_status: draft
consumers: [project]
entrypoint: policy/how-a-sweep-is-stored
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

**Workflows**

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

**Templates** — [a sweep](templates/sweep.md) · [a slice](templates/slice.md) ·
[presenting a file](templates/file-presentation.md)

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
the index in `sweep.md` is a cache of that. When they disagree, the slices win.

**A row finishes two ways, and they are not the same claim.** `reviewed` means
read and satisfactory and **any party may set it, agent included**; `approved`
means signed off and **only a person may give it**. Both are needed, because a
sweep does not always have a human in it — a status only a person could set
would leave an agent-agent sweep unable to finish a single row.

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

`0.9.1` — **examples name a fictional person, not a real one.**

`templates/sweep.md` and [[how-a-sweep-is-stored]] carried a real workstation
account, taken from a filesystem path. The catalog already had a convention for
this — `human:fsmith`, used across five bundles — and it was missed.

**Two faults, and they are separate.** Naming a real person in a published
example is a **disclosure**, and in some organizations a workstation username is
secret. And the value came from the **OS user** rather than a git or forge
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

Minor: new content, and one workflow step restated.

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

**`lifecycle_status: draft`**, which should have been there at `0.1.0`. Nothing
has run a sweep; two of four flagged guesses have already been corrected by a
single conversation, and a bundle changing that fast is not `provisional`.

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
- **Whether `close-a-sweep` earns being a workflow** rather than a paragraph.

**No retention period for archived sweeps**, deliberately. Nobody has run
enough of them to know what one should be, and a number invented now would be
enforced for years on no evidence.
