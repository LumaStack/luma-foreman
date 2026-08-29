---
type: workflow
title: Start a sweep
description: Settle what is being read and what is not, choose an order, and build the index that makes coverage checkable. Use when beginning a file-by-file review of a project.
---

# Start a sweep

## 1. Check that a sweep is what they want

**Three things get asked for in the same words**, and two of them are cheaper:

| what they said | what they may want |
| --- | --- |
| *review my changes* | a diff review. Minutes, not weeks — whatever this project already uses |
| *find out whether X is a problem* | a targeted audit. Answers one question, and somebody else can respond to it |
| *I want to read this whole thing properly* | **a sweep** |

**Say the cost out loud before agreeing** — see step 7 for how to arrive at it.
Somebody who wanted an afternoon's reassurance should find out at the start
rather than at file nine, and nobody is offended by being asked.

## 2. Settle what the sweep is for

**Ask this before scope, because the goal decides the scope.** *Everything* is
what people answer when nobody asked them what they were trying to find out.

**"Read the whole project" is a method, not a goal.** The goal is what you want
to be true afterwards.

> *For example: I inherited this and do not trust it. I want to answer questions
> about this system without opening it. We keep shipping the same class of bug.
> Somebody joins in a month and I want to know what will embarrass us. This is
> about to be made public.*

### Push once for a version you can check against

**A goal you cannot check against is a mood.** Not a metric — just something
that could be observed:

| vague | checkable |
| --- | --- |
| *I want to understand it* | *I can answer questions about any part without opening the file* |
| *make sure there are no mistakes* | *nothing here would embarrass us if a customer read it* |
| *clean it up* | *a new joiner can find where anything lives in a minute* |

**Understanding is a legitimate goal** and needs no apology. It gets sharper by
asking *understand it well enough to do what?* — the answer names the test.

**One push, then take what you get.** Somebody who genuinely just wants to read
their own code is allowed to, and interrogating them into a measurable
objective buys a worse answer than the honest vague one.

### What the goal does once the sweep is running

**It decides what is worth stopping on.** Two people with different goals
reading the same file flag different things. With no goal written down the
agent picks for them, silently, and its pick is the one that sticks.

**It is the drift check.** When three slices running turn up nothing related to
the goal, one of two things is true and both are worth saying out loud: the
goal was wrong, or the sweep has wandered. Neither is visible without something
to compare against.

### A sharp goal is safer here than in an audit

**A stated goal biases what you notice.** In a targeted audit that is a real
hazard, because an audit only looks where it was aimed.

**A sweep covers everything regardless.** The index does not care what you were
looking for, so the coverage stays honest even where the attention did not.
That is why a sweep can afford a sharper goal than an audit can.

## 3. Settle the scope, and what is excluded

**Ask; do not infer, and let the goal narrow it.** The obvious scope is *the
repository*, and it is usually wrong — vendored code, generated files,
lockfiles, a subtree somebody else owns and a test corpus are all things a
person will happily exclude when asked and will silently resent reviewing when
not.

**Write both halves down.** What is in, and what was deliberately left out —
separating what they excluded from what you did. A sweep that does not say what
it skipped cannot make its own coverage mean anything later.

## 4. Decide whether the plan may move

**`strict` or `evolving`, and it is a decision rather than a mood.**

**`strict`** — the goal, scope and strategy are fixed for this sweep. Anything
that would change them is **recorded and left for a later sweep**. This is not
a blind sweep: it routes findings exactly as any sweep does, and *that is a
real observation and this is not the sweep for it* is a legitimate journal
entry.

**`evolving`** — expect them to move, and budget for it. Right when the
practice or the material is genuinely new, and **expensive**: the first sweep
ever run was evolving and produced thirteen releases of this bundle while
covering six files. Correct for a first sweep, ruinous for a tenth.

**Most sweeps should be strict.** Once neither the practice nor the material is
new, `evolving` is a licence to be distracted by whatever is more interesting
than the next file.

**Say which, in `sweep.md`.** A sweep that quietly starts rewriting its own
goal was evolving all along and nobody said so — so nobody budgeted for it, and
the estimate is wrong for a reason the record does not show.

## 5. Choose an order and record why

See [[choosing-an-order]]. Narrative is the usual answer for a first sweep;
directory order is right more often than it sounds.

**One sentence of reason is enough**, and it is what makes the order survive
the slice where a different one would be more convenient.

## 6. Build the index

Enumerate every file in scope, in the chosen order, and record the commit you
enumerated at.

```sh
git rev-parse --short=12 HEAD
git ls-files <paths> | grep -vE '<exclusions>'
```

**Every file in scope gets a row, even the boring ones.** The index is a
coverage ledger — a file left out of it is a file nobody can later prove was
read or not read, and the ones omitted for being trivial are exactly where a
stale copy of something hides.

**Name the clusters in `sweep.md`, and say what each one is about.** Group by
what must be read together — a subsystem, an execution path, a set of documents
answering one question — which is routinely not what shares a directory.

**Cap a cluster at one slice's worth**, split an oversized one in path order,
and give a file big enough to be a slice on its own its own cluster.

**The naming is not decoration.** `coverage.md` is only derivable if the rules
that produced it are written down, and clustering is the one people leave in
their heads. **A file that fits no cluster means the strategy is incomplete** —
add the cluster to the sweep rather than improvising one in the index.

Do not over-plan the membership: the first grouping is a guess and every slice
will revise the one after it. It is the *strategy* that has to be stated, not
the perfect answer.

## 7. Say how long this will actually take

**Give a band, say it is a guess, and replace it with a measurement after two
slices.** A number said at the start is what stops a sweep dying at 15% with
somebody concluding they were slow rather than that it was long. A number said
*confidently* at the start is usually wrong.

### Estimate from the material, never from the file count

**File count is the wrong denominator**, and using it is how a sweep gets
mis-sold in both directions at once. What costs time is the reasoning a file
demands, and that varies by more than an order of magnitude across a single
repository.

| material | a slice is roughly | so |
| --- | --- | --- |
| **prose, docs, config** | a dozen files, sometimes thirty | **a hundred short documents is days, not months** |
| **ordinary application code** | three to eight files | the middle case, and where the guess is safest |
| **dense logic** — concurrency, parsing, anything with real invariants | one or two files, and sometimes half of one | a small directory can outlast a large one |

**Say which of these the scope actually is**, and split the estimate when it is
several. *Roughly four slices for `docs/`, and fifteen for `src/`* is a useful
sentence. *Nineteen slices* is not, because the two halves are not made of the
same stuff and the reader will plan against the wrong one.

### Then stop guessing, and keep re-measuring

**Re-measure at every slice, not once.** It costs a count of rows, and the only
argument for waiting is that an early number is noisy — which is a reason to
*present* it honestly, not to withhold it.

**Report a range with the number of slices behind it, never a point estimate.**
*Three slices, four to nine files each, roughly fifteen slices left* is honest
at small samples. *2.1 files per slice* is false precision wearing the costume
of data, and a reader plans against it.

**A small sample shows up as a wide range**, which is the correct behaviour
rather than a defect to hide.

**Keep the rates separate by material**, for the same reason the first estimate
was split: two prose slices tell you nothing about dense logic, and averaging
them produces a number true of neither.

**Every slice counts, including the odd ones.** A first slice of a `draft`
practice is atypical and there is no need for a rule about it: an outlier
widens the range, which is exactly the signal a reader wants. **Excluding it
would make the range narrower and more confident than the evidence supports.**

**And do not defend the original estimate against any of this.** The
measurement is on this material, by these people, at the depth they actually
settled into.

### Then say how much will move underneath it

**A sweep that takes six weeks is reviewing a codebase that gets six weeks of
commits.** The estimate is half the warning; the other half is how much of what
you cover will have changed by the time you finish.

Measure it over a window the length of the estimate:

```sh
git log --since="6 weeks ago" --name-only --pretty=format: -- <paths> \
  | sort -u | wc -l
```

Against the file count in scope, that is a rough *expect this much to move
while you sweep*. Record it in `sweep.md` beside the estimate, so the close can
compare what actually happened.

**Name the hot files, not just the percentage.** Churn concentrates — the usual
shape is one subsystem moving and everything else sitting still — and a single
number hides the only part worth acting on.

**Three responses, and the first is available more often than people expect:**

- **Freeze it.** On a project with one or two committers this is a genuine
  choice, and it is much the cheapest of the three.
- **Exclude the moving part and sweep it once it settles.** Reviewing code that
  is being rewritten is work you will do twice.
- **Accept it** and expect re-coverings — which the index records rather than
  absorbs.

**A hot area also argues about the order** ([[choosing-an-order]]): sweeping it
last gives it time to settle, sweeping it first gets a read before it moves
further. Which is right depends on whether the churn is finishing or starting,
which is the next paragraph.

**The number is a prompt, not a forecast.** Past churn predicts future churn
badly — **a migration that just finished looks identical in the log to one that
is half done**, and only the reader can tell you which it was. So ask, rather
than reporting the percentage as though it were a rate.

### If the number is unacceptable, cut the scope now

Not by quietly reviewing faster later. **A sweep of the four subsystems that
matter, finished, beats a sweep of everything, abandoned** — and cutting at the
start is a scope decision anybody can see, while cutting by acceleration is one
that only shows up as coverage nobody trusts.

## 8. If this is a first sweep, say so

The practice itself is `draft`. **Keep a line in each slice note for where it
fought you** — an order that stopped working, an estimate that was wrong by
double, a step that produced nothing.

That costs a sentence per slice and it is the only way the guesses get
corrected. A sweep that ran fine and taught nobody anything about sweeping is a
missed opportunity the second sweep pays for.

## 9. Write `sweep.md` and `coverage.md`, and commit them

[The sweep template](../templates/sweep.md) and [the coverage
template](../templates/coverage.md) have the shapes. **Two files, because one
should stay true as the work proceeds and the other is expected to go false and
be brought back** — see [[how-a-sweep-is-stored]].

Commit before the first slice — the index is the thing that makes the sweep
resumable, and a sweep that only exists in a conversation is one crash from
gone.
