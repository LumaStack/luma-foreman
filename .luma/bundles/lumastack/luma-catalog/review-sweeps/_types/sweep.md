---
type: type_definition
defines: sweep
fields:
  goal:
    field_presence: required
    field_type: text
    desc: "what the sweep is for — what you want to be true afterwards, stated so it can be checked against"
  goal_discipline:
    field_presence: optional
    field_type: enum
    desc: "strict | adaptive | exploratory — how freely the aim may move. Default adaptive"
  scope_discipline:
    field_presence: optional
    field_type: enum
    desc: "strict | adaptive | exploratory — how freely the boundary may move. Default adaptive"
  strategy_discipline:
    field_presence: optional
    field_type: enum
    desc: "strict | adaptive | exploratory — how freely the method may move. Default adaptive"
  scope:
    field_presence: required
    field_type: text
    desc: "what is being read — and, in the body, what deliberately is not"
  ordering:
    field_presence: required
    field_type: text
    desc: "the order units are taken in: narrative, risk-weighted, dependency, directory, or led"
  approval:
    field_presence: optional
    field_type: enum
    desc: "required | recommended | optional | prohibited — how strongly a person's sign-off is expected on each row. Default recommended"
  pairing:
    field_presence: required
    field_type: text
    desc: "who is in this sweep — human-agent, or agent-agent. Declared before the first slice"
  contributors:
    field_presence: recommended
    field_type: list of actor
    desc: "everyone reading in this sweep, human and agent alike"
  archived:
    field_presence: optional
    field_type: date
    desc: "when the sweep was closed and moved to archived/"
---

# Sweep

One long read of a codebase, by a reader with a second party beside them. The
Document carries the scope, the order, and the index of what has been covered.

**It is not a record**, and the fields say so: `indexed_at` moves, the index is
edited at every slice, and there is no commit pinning what the sweep is true of
— because a sweep is true of a moving target by construction. What it does
carry is enough to resume it and enough to check its coverage.

*Only what the format does not already have is declared here.* `created`,
`lifecycle_status` and `title` are core fields and are used as they come.

## `goal` is what the sweep is checked against

**Not what it covers — what it is for.** *Read the whole project* is the
method; the goal is what you want to be true afterwards, and it is the only
thing that makes *on track* and *off track* mean anything during a run that
takes weeks.

**Checkable beats precise.** Not a metric — something that could be observed.
*I can answer questions about any part without opening the file* is a goal. *I
want to understand it* is the same wish with the test removed.

**It decides what is worth stopping on.** Two readers with different goals flag
different things in the same file; with nothing written down the agent chooses
for them, silently.

**It is what a drifting sweep is compared against.** Three slices running that
turn up nothing related to the goal mean the goal was wrong or the sweep has
wandered — and neither shows without this field.

## The three disciplines say which parts of the plan may move

**Three fields, because they move independently.**

```yaml
goal_discipline: strict
scope_discipline: strict
strategy_discipline: adaptive
```

| | `strict` | `adaptive` *(default)* | `exploratory` |
| --- | --- | --- | --- |
| **`goal_discipline`** | the aim is fixed | the aim is known — **sharpen it** as slices show what it really meant | **the aim is not known yet** — find out what the sweep should be for |
| **`scope_discipline`** | what is in and out is settled | the boundary is roughly right — **adjust it** where a slice shows it was drawn wrongly | **the boundary is not known yet** — absorb what turns out to belong |
| **`strategy_discipline`** | clustering, order and who-reads-what are fixed | the method works — **tune it** where it demonstrably fought you | **the method is not known yet** — build it while you use it |

### The ladder is about what you know, not about how much you spend

**That is the line, and it is the only one that holds.** *How much change feels
warranted* is undrawable — every improvement feels warranted in the moment.
*What do we already know* is answerable before the sweep starts.

| | you know | so you |
| --- | --- | --- |
| `strict` | what you are doing | do not touch it |
| `adaptive` | the shape | **refine and tune** |
| `exploratory` | **that you do not know the shape** | **go and find what it should be** |

**`adaptive` is enhancement.** The goal, the boundary and the method are all
roughly right, and slices sand them down. A change owes a line saying what
moved and why, and the estimate is revised rather than abandoned.

**`exploratory` is discovery.** You are not refining a thing, you are working
out what the thing is — so you add whatever you find, and the shape gets bigger
as you learn what belongs in it. **The estimate is abandoned rather than
revised**, because there is nothing yet to estimate against.

**Disregard for time and budget is the consequence, not the definition.** It
follows from not knowing what you are looking for, which is why `exploratory`
is a legitimate choice rather than an excuse: **a sweep that does not know its
own shape cannot be estimated, and pretending otherwise produces a number that
was never true.**

*The first sweep ever run was exploratory on all three axes, and correctly so —
nobody knew what a sweep was. It produced seventeen releases of this bundle
while covering six files, which is what discovery costs.*

### Absent means adaptive, on every axis

**Because that is what actually happens.** A sweep that has not thought about
this will adapt — and if the default were `strict`, sweeps would sprawl anyway
while the record claimed a discipline they never had. **An honest record of
sprawl is worth more than a flattering one**, and a default describing an
aspiration rather than behaviour is how a field stops being read.

**Most *mature* sweeps should be strict on goals and scope.** The default
reflects where this practice currently is rather than where it should end up —
**and it should flip once strict is the common case.** A change to make on
evidence, not on principle.

## `approval` says how strongly sign-off is expected

**Not every sweep wants it.** An agent-agent sweep cannot have it; one aimed at
coverage rather than endorsement does not need it. **Assuming it is wanted
turns every unsigned row into a shortfall nobody ever intended to fill.**

| | a signature is | unsigned rows at close are |
| --- | --- | --- |
| **`required`** | owed on every row — a row is unfinished without one | **a shortfall** — work the sweep set out to do and did not |
| **`recommended`** *(default)* | wanted on every row, and a row may finish without it | **a known compromise**, named rather than glossed |
| **`optional`** | welcome, and nobody is waiting for it | **a description** — how this sweep works, and nothing owed |
| **`prohibited`** | **not to be given** — a signature here would claim something untrue | **not reported.** There is nothing to count |

**This is RFC 2119's ladder** — must, should, may, must not — and it is
borrowed on purpose. A reader who has met those four anywhere else already
knows what the four rungs mean here.

**`prohibited` is the only value with a defect of its own.** Unsigned rows are
the expectation met, so they go unreported — but **a signature that exists is
reported as a defect**, because somebody claimed an endorsement this sweep had
ruled out. Every other value can be satisfied by doing nothing. This one can be
violated.

**Which is why it is not spelled `unused` or `excluded`.** Those describe a
column nobody filled in. This one says *do not sign these off*, and means it.

**The counts print under all four.** *Fifty-three approved, twelve reviewed and
never signed off* is reported whatever the setting; what the field decides is
whether that second number is a failure, a compromise or a fact. **Nothing is
hidden by any value**, which is what makes a permissive default safe.

**`recommended` is the default because it is honest for most sweeps with a
person in them.** You would like to sign off on everything and you will not get
to all of it — that is the ordinary case, and it deserves neither the guilt of
`required` nor the indifference of `optional`.

**`prohibited` is the honest value for an agent-agent sweep**, where a human
signature would not merely be unlikely but would misrepresent what happened.
Leaving it at `recommended` there would report a compromise against a standard
that could never have been met; leaving it at `optional` would invite the very
signature that makes the record false.

## `scope` must say what was left out

The half people skip, and the one that decides whether finished coverage means
anything. *"Everything under src/ and docs/; not the vendored tree, not the
generated clients"* is a scope. *"The repository"* is not — a reader cannot
then tell an empty row from an excluded one.

**Say which exclusions were given to you and which you chose.** An area the
owner ruled out reads differently from one you ran out of appetite for.

## `ordering` is not decorative

It is what makes the sequence checkable afterwards, and what a slice consults
when the convenient next unit is not the correct one. Record the reason in the
body — the field carries the name, the prose carries why.

**Changing it mid-sweep is legitimate and gets a dated line in the body.**
Silently drifting from it is what the field exists to make visible.

**`led` is a value, not a blank.** A sweep whose person picks the next cluster
each slice is running a declared order and says so; the defect the field
catches is a sweep claiming `narrative` while being led in practice.

## The index is not here

**A sweep states what it is for; `coverage` records what has been covered.**
The two have opposite lifecycles — this file is written once and rarely
touched, while the index is edited at every slice — and keeping them together
buries every change of reasoning under a hundred rows of bookkeeping.

`indexed_at` goes with the index, because it is a fact about the index.

## No coverage field

**Coverage is derived from the slices, never stored.** Each slice says what it
covered; the index in the body is a cache of that, and the number in a closing
summary is computed at closing time.

The table in the body is edited constantly and will eventually be wrong. That
is tolerable precisely because it can be rebuilt — **when the index and the
slices disagree, the slices win.**
