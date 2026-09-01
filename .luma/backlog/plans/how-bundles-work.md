---
type: document
title: How bundles work
description: The end-to-end design for bundles — how knowledge reaches context, what a bundle is, what a document is, what a project records, how it reaches a harness, and how it reaches a repository. Written forward, entry by entry, rather than derived from what exists.
lifecycle: draft
created: { by: human:benlinton, at: 2026-08-30T00:00:00Z }
modified: { by: agent:claude-opus-5, at: 2026-08-31T00:00:00Z }
---

# How bundles work

**Written forward.** What exists today is a prototype that grew into artifacts
answering overlapping questions — a manifest, a routing table, a project ring
and a per-bundle ring — and the way out is not to reconcile them. This document
designs the thing that should exist and lets the prototype be measured against
it, never the reverse.

**Built entry by entry.** Each section is settled before the next one starts. An
entry states what it is, what problems it has to solve, and only then what
fields or files that implies — in that order, because deriving fields from a
mock-up is how a design acquires columns nobody can justify later.

**Earlier plans are raw experimental material, not sources.** *How bundles compose* 
worked through capabilities, `needs` and `provides`; *knowledge delivery* and *hook
delivery* worked through transports. Whatever survives from them gets restated
in an entry here and argued on its own. Nothing is carried forward by citation.

## The entries, and why in this order

Each one depends on the entries above it and on none below.

| | entry | reaches where | answers |
| --- | --- | --- | --- |
| 0 | established vocabulary | — | the words every later entry depends on |
| 1 | how knowledge reaches context | a model's context | what everything else is classified by |
| 2 | what a bundle is | — | the unit everything else references |
| 3 | what a document is | — | the thing a bundle holds |
| 4 | what a project records about them | — | membership, provenance, integrity |
| 5 | how knowledge reaches a harness | files a harness reads | what implements each category |
| 6 | how a bundle reaches a catalog | a catalog | publishing |
| 7 | how a bundle reaches a repository | a directory on disk | `get`, and adoption |

**Every destination was being called the same thing.** A bundle **lands** on
disk — in a catalog when it is published, in a repository when `get` copies it —
is **registered** into a harness when `apply` writes adapters, and **loads**
into context when a model reads it. Naming the destination is what keeps Entries
1, 5, 6 and 7 from collapsing into each other — which they did twice while this
document was being cut. **There is
no word for the whole path**, deliberately: nobody observes that arrival failed,
only that something did not load, and the stages behind it are walked by name.

**Problems are stated once, where they are decided.** An entry that depends on a
problem it does not own says so and points at the owner rather than restating
it — a problem written twice is a problem that will be answered twice, and
differently.

## Settled before this document opened

- **The bundle boundary does not decide relevance.** `git-secrets` holds
  credentials and identity, whose first moves are opposite, so a bundle's
  contents need not share one profile. Reading may therefore be decided per
  document — or per bundle, where that genuinely is the right grain. Which
  grain applies where is open, and Entry 5 is where it gets decided.
- **Presence and reading are separate axes.** What must be *fetched* is
  bundle-grained, because fetching is. What is *read* has its own grain, settled
  per case rather than by the fetch boundary. A claim about one is not a claim
  about the other, and conflating them is what made bundle-level dependency look
  like it contradicted the bullet above.

## Prevention and detection

**Almost everything here reports a violation rather than stopping one**, and
that is a pattern rather than a run of unrelated choices.

| | prevention | detection |
| --- | --- | --- |
| a vendored bundle edited locally | — | the checksum reports it |
| a stray directory | — | the manifest reports it |
| a local bundle's version drifting | — | `inspect` compares it |
| a governing body's rule | put it out of reach | check compliance afterwards |
| `expose` | a boundary the model cannot cross | — |

`expose` is the only place this design prevents rather than reports, and a
governing body's rule is the only case still open. **A design that detects
everywhere except one place should know why that place is different** — whether
prevention is genuinely required there, or whether nobody asked the question.

## Checks key on state, not on the route

**A bundle can arrive many ways.** `get` is one. It can be written here, copied
in by hand, arrive as a submodule, or come from something that does not exist
yet. **Anything attached to a command misses whatever arrived by another
route** — which is why the manifest detects strays at all: a directory that
landed without being adopted is precisely what a command-keyed check never sees.

So verification, resolution and reporting run over what is present, whenever
they run, rather than at the moment something arrived. Two consequences follow.
They have to be **re-runnable**, and they have to produce **the same answer from
the same state**, or each run churns what the last one settled.

**And a check over state can warn where one bound to a command would block.**
Taking a second provider is not a mistake to prevent — the adopter may be doing
it deliberately, meaning to silence the first. Detection lets them; prevention
at the moment of fetch would not.

---

# Entry 0 — established vocabulary

Pinned because the later entries cannot be cut without it.

### Places and movements

**context** — what a model can actually see at the moment it acts. The scarce
resource, and the destination Entry 1 is about. Distinct from *disk*, where a
bundle lands, and from a *harness*, which reads files a model never sees.

**land** — reaching disk. What `get` does: a bundle lands in the repository as a
committed copy and stays there whether or not anything ever reads it.

**register** — writing the binding into one harness's own format so that harness
can consult it. **One binding, registered once per harness** — the deciding
happens once and the writing happens per consumer, which is what makes an
adapter thin rather than merely small.

**load** — reaching context. Content entering what a model can see, by whatever
mechanism put it there. `/load-bundle` and `/load-context` are named for this,
so the concept and the command agree.

### What declares, and what it resolves to

**matcher** — a declaration on a document, or on a bundle, of the conditions
under which it loads. Written by an author who has never seen the adopting
project, so it claims *when this content applies*, not what any project will do
about it. *When* is certain. Whether a matcher also determines *how* it loads —
or whether that is derived from its shape — is open, and belongs to Entry 5.
*Where* has no case behind it yet and is deliberately not claimed.

**binding** — the resolved correspondence for one project: which content answers
which condition, and which name each workflow takes. `apply` produces it by
resolving every adopted bundle's matchers against each other and against
whatever the project has settled. Where a matcher is what an author claimed, a
binding is what this project decided — it is where two bundles claiming one name
get separated, and where an adopter's override takes effect. **The override is an
input to resolution rather than an edit of the result**, since the binding is
recomputed on every `apply`. Mostly harness-agnostic: resolving name collisions
assumes a harness that addresses things by name, which most do.

**adapter** — what `register` leaves behind: harness-specific files that let one
harness find what a binding decided. The harness-specific twin of a binding —
the same correspondence, expressed in whatever shape that harness reads.

*Thin* is the goal and still needs a testable meaning. A pointer is cheap and
cannot drift; a copy is a second source of truth and can. Whether an adapter
may ever inline content — for a harness that cannot follow a pointer, or where
inlining is the only way to get an acceptable outcome — is open. Optimize for
reliability, followed closely by minimizing duplication.

*Open: whether an adapter is one file or a set.* `apply` writes several per
harness — a skill per workflow, a table a hook reads, a block in a memory file —
so the word is either collective for all of it, or each file is an adapter and a
harness gets many.

### Asking for something

**request** — the act of naming something so it enters context. Available to a
person, to another agent, to a document citing another, and to a mechanism whose
checks caught a miss. Where `guaranteed` fires on a declared condition, a request
fires on a decision that this thing is needed now. It is also how anything on
`standby` loads.

**request helper** — whatever performs a request. It has to be announced before
anything can invoke it, which would be the one announcement `standby` pays for.
**Deliberately unspecific about form** — a command, a tool call, something not
yet determined — because an adapter provides it and Entry 5 decides what it is.
Naming it for a form it may not take is how a word starts lying.

### Governance

**governing body** — whoever sets rules an adopter may not overrule. Security,
compliance, whoever answers for the organization. **What separates them from
another opinion is that the adopter cannot override them back** — enforced
either by putting their rules beyond the adopter's reach, which prevents a
violation, or by checking afterwards that a repository still complies, which
reports one. Which of those is right, and where a rule lives under either, is
open.

**expose** — control over what a model can reach at all, as opposed to what it
should load. Where a matcher and a binding say *when this applies*, exposure
says whether the model may open it — **and whether it can see there is anything
to open.** Enforced by something standing between the model and the content,
rather than by anything the model is told. The governance half: a boundary
rather than a correspondence.

What enforces it, who sets it, **whether visibility and openability are one
control or two**, and whether it introduces a permission axis crossing Entry 1's
categories are all open.

### Who decides

**adopt** — a project taking a bundle and becoming answerable for what it does
here. The bundle **lands** as a committed copy and the project records that it
belongs. **Landing and adopting are not the same event**: a copy that landed
without being adopted is a stray, and detecting that is most of why the record
is worth keeping.

**adopter** — whoever takes a bundle into a project and answers for what it does
there.

**author** — whoever wrote the bundle, having never seen the projects that adopt
it. Everything a bundle declares about how it loads is the author's claim, made
without knowing any particular project — which is why an adopter needs some way
to disagree.

### What it costs

**residency** — the state of currently occupying context, as distinct from
having loaded. **Residency ends**: a compaction can summarize it away, `/clear`
empties it, a long session pushes it out. So *it loaded* and *it is here* are
different claims, and the gap between them is where a guarantee quietly stops
being true without anything reporting it. The adjective is *resident*; *loaded*
is ambiguous between the event and the state.

**session floor** — the residency every session pays before the work is known,
whether or not the work turns out to touch it. What `expected` and `optional`
pay an announcement for, and what `standby` pays only once.

### Avoided vocabulary

Some words below are retired rather than defined: a name for a mechanism that 
does not exist yet attracts meanings, and each of these did. Just because a word
is retired does not mean it has to stay retired — if a use case turns up that
proves its worth, it comes back out.

**Retired: `router`.** A name for something that did not exist, so every reader
filled it differently. What it reached for — *help a model or harness know when
to load what* — is `matcher` plus a mechanism plus an index, with no residue
left for a fourth word to name. It returns only if something turns up that the
others cannot express.

**Retired: `bundle entrypoint`.** Already stated twice over: a bundle's
self-description says what to read first, and each document's matcher says what
loads it. A third statement of the same fact is three places to disagree.

**Avoided: `delivery`, `triggers`.** *Delivery* spans every category in Entry 1
at once and hides the differences between them. *Triggers* is `matcher` under
another name.

---

# Entry 1 — how knowledge reaches context

**Everything downstream is classified by these.** This entry comes first because
it depends on nothing and is depended on by all of them: a bundle's
self-description, a document's matcher, and every adapter written for a harness
all have to say which of these they are producing.

## What it has to solve

1. **What an absence means.** Whether a document not being present is a defect,
   and if so, whose.
2. **What can be verified.** Which loads a tool can check or enforce 
   (e.g. forcibly inject), and which nothing yet can.
3. **What each costs.** A mechanism, standing context, or nothing.
4. **What the default is.** What a document gets by declaring nothing at all.
5. **Whether strength is the same question.** How badly something is wanted,
   versus whether it loads.
6. **What an announcement may cost.** `expected` and `optional` are only cheap
   while their announcements stay small, and nothing yet holds them there.
7. **Who declares, and who may overrule whom.** An author states how their
   document or bundle loads, having never seen the adopting project. An adopter
   may disagree with good reason — too noisy here, only under `src/`, adopted
   for one workflow and not for its policies. A governing body may need to
   overrule the adopter in a way the adopter cannot undo. Whether that is one
   mechanism with a precedence order or several with different reach, where a
   governing body's declaration lives given a project must not be able to edit
   it, and what happens when two of them disagree.
8. **What a matcher means at each grain.** Whether a bundle, a document and a
   section can all mean the same thing by it. **This turns on whether a bundle
   has a body**, which Entry 2 owns: if a bundle's self-description is itself
   loadable, a bundle matcher is one job at its coarsest grain; if a bundle has
   nothing of its own to load, the declaration has to mean something else,
   nearer to *is this in play at all*. Also whether all three grains exist, how
   they compose when they disagree, what a section-level matcher implies about a
   document needing an index of its own, and whether a document may therefore
   span categories rather than sitting in one.
9. **What survives a context reset.** Loading happens at a moment; context does
   not persist. `/clear` empties it, `/compact` may summarize things away, and a
   long session may push them out — in every case silently. **Both halves fail,
   and differently.** An announcement that vanishes takes the model's map with
   it, so it can no longer request what it no longer knows exists. A
   `guaranteed` document that vanishes is absent while still reading as
   guaranteed to its author, its adopter, and any check that verified the
   mechanism is wired. Which of those costs more depends on what was lost, and
   is not decidable here. Whether a promise holds across these events, what
   re-establishes it, and how anything knows it needs to.
10. **How a trend is gathered.** `expected` is improvable only if somebody can
    see whether the right things are being loaded more often than they used to
    be. What produces that signal, who reads it, and whether it can be collected
    at all without watching sessions closely enough to cost more than it saves.

## The categories

```
guaranteed  a mechanism puts it there
offered     the model decides
  ├─ expected   absence is a miss
  └─ optional   absence is fine
standby     nothing decides until somebody asks
```

**`offered` is a bracket rather than a fifth category.** It names the pair the
model chooses between, and it marks the line where verifiability stops:
`guaranteed` is the only one a tool can check, and nothing under `offered` can
be checked by anything.

**Each category describes what a document does on its own.** They are named as
statuses rather than as mechanisms, because the mechanism can change without the
word going stale.

**Nothing here is free — each category moves its cost somewhere else**, and the
columns exist so that where is visible. The **session floor** is context spent
before the work is known, in every session, whether or not it turns out to be
touched. **When it loads** is context spent in the one session where the content
actually loads. **What must exist** is machinery somebody builds and keeps
working, and in some cases runs on every tool call. Averaging any of these hides
which is being spent, and calling one of them *nothing* hides that it was spent
at all.

| | left alone, it… | session floor | when it loads | what must exist |
| --- | --- | --- | --- | --- |
| **guaranteed** | loads | set by its matcher | however much of it loads | a mechanism, and something evaluating it on every call |
| **expected** | announces itself, and should be taken | **its announcement** | however much of it loads | — |
| **optional** | announces itself, and may be taken | **its announcement** | however much of it loads | — |
| **standby** | does nothing until requested | **one announcement at most**, however many documents | however much of it loads | a way to reach it, and somebody who knows the name |

**`guaranteed` is priced by its matcher** — and that price is not yet computable.
A matcher that never narrows puts content into every session, which is the
highest floor anything here can set. A conditional one keeps the floor at zero
and pays instead for a mechanism that has to be built and kept working, plus an
evaluation that runs on every tool call whether or not it matches. The category
says it is forced; the matcher says how often; the bill follows the matcher.

**A category may be relative to its container, which would make that price
computable.** Under that reading, `guaranteed` means *guaranteed once the thing
holding me has loaded* — and the chain reaches the top only where every link is
guaranteed. A document is resident in every session only if its bundle is too.
The price is then the chance its container loads, times its size, recursively up
to something that is always there. At the top that chance is one; two levels in,
behind a bundle nobody opens, it is near zero.

**And it expresses something neither pure category can.** A bundle nobody loads
by default, which brings its own required policy the moment it is reached: the
policy costs nothing until the bundle is wanted, and is not optional once it is.
`guaranteed` alone would pay in every session. `expected` alone would let a
model skip what the bundle needs in order to work.

**How much of a document loads is not settled either, and this table does not
rule anything out.** Nothing here requires a whole body. A mechanism that
injects can inject a part; a model opening a file can stop at a marked point; a
document may be able to say in frontmatter or inline which of its parts belong
to which category, so that one file spans several.

**These may not be different mechanisms at all.** A document might mark where its
announcement ends and its body begins — in frontmatter, inline, however — and
that one marking could be honoured by whatever is doing the delivering: an
injector that pushes only the first part, a model that opens only the first
part, or a tool that hands over the first part and withholds the rest. Whether
that is three mechanisms or one declaration honoured three ways is not decided.

**What a tool adds there is enforcement rather than a different kind of
delivery**, and it cuts both ways. A model cannot over-fetch what it cannot see,
and cannot skip past a boundary it never learns about — which is both failures
this design worries about, closed by one thing. But a model reading a filtered
document believes it has the whole one, so anything withheld that qualified what
remains is acted on as though it did not exist. Both are worth knowing before
Entry 5 picks.

**Whether `matcher` is doing more than one job is itself open**, so the costs
above are a sketch rather than an accounting. A matcher on a document decides a
load; a matcher on a section, if sections can carry one, decides how much of
one. A bundle is the case in question: if its self-description is loadable, a
bundle matcher is the same job at a coarser grain, and one word is right. If a
bundle has nothing of its own to load, the declaration means something else
entirely and the word is covering two jobs. **Entry 2 decides whether a bundle
has a body**, and no cost stated here is settled until it does.

**An announcement has no natural size, and that is a problem.** A line is the
target for `expected` and `optional`, not a property of them. Nothing in the
design stops an author announcing a document with a paragraph, or with a summary
that grows until it is a second copy of the thing it points at — which has
been observed, and which quietly turns a cheap category into an expensive one. The
floor is set by whoever wrote the announcement, and nobody is checking.

**`standby`'s floor does not scale, and how high it sits is undecided.** If a
request helper is required, its announcement is the floor, and it is **paid once
for all of it** — five standby documents and five hundred cost the same, because
nothing is advertised per document. If a path handed to a model is enough, the
floor is nothing at all. Either way it is the only category whose floor does not
grow with how much content sits behind it, and that property holds whichever way
the question goes.

**The second price is discoverability, and it is not paid in tokens.** Somebody
has to know the name — a person who has seen it, an agent that searched, or a
document already in context that cites it. Where a citation carries the name,
the cost is amortised onto something already loaded, which is the cheapest this
design gets. Where nothing carries it, the content is present and unreachable,
and *that* is the risk `standby` trades its floor for.

Without it, anything a model might choose has to be advertised, so `optional`
would have to claim a floor it cannot — which is an error this document made
until `standby` surfaced.

**And it is not weaker than `optional`.** A long reference sits on `standby`
precisely because it is large and specific, not because it matters less. These
are four things a document can be, not one gradient with four stops.

## Request acts on a status

**Anything not already present can be requested**, and that is what keeps the
four above honest. A person types `/load-bundle`; an agent that noticed what
this one missed names a document; a document being read cites another.

**A request and `guaranteed` both force a load, and differ in what they fire
on.** `guaranteed` fires on a declared condition. A request fires on somebody or
something deciding that this particular thing is needed now — a person, another
agent, a citation, or a hook whose own checks caught a miss. **The initiator is
not the difference**, since a mechanism can request too. That is why a request
cannot be a fifth status: it is an action performed *on* a status, available to
`expected`, `optional` and `standby` alike.

**Against `guaranteed` it is usually redundant, and not always.** A guaranteed
document whose residency has ended is absent, so requesting it is a reload
rather than a no-op. Whether that is how a broken guarantee gets repaired — and
whether anything can tell that it needs repairing — belongs with problem 9.

**`standby` is the category that has nothing else.** For the other two a request
is recovery from a miss; for `standby` it is the only way in. That makes
whatever serves that purpose a dependency of one whole category rather than a
convenience bolted onto the rest.

## Whether the set is closed

**Binary questions, and one branch nothing yet fills.**

```
does anything deliver it by default?
├─ yes ──────────────────────────────────────── guaranteed
└─ no → is it advertised to the model?
        ├─ yes → what does an absence mean?
        │        ├─ a miss ──────────────────── expected
        │        └─ nothing ─────────────────── optional
        └─ no ───────────────────────────────── standby
```

The unexplored branch is *not advertised, and an absence is a miss* — a document
a model is supposed to load and was never told about. **Whether anything belongs
there is open.** A model that searches has been shown something without anything
advertising it, which would put content in that cell. And searching may itself
be mediated, by a hook or a command or whatever `expose` becomes, in which case
what is findable is a decision rather than a given. The tree is the set as it
stands, not a proof that nothing else fits.

## What each one obliges

**Guaranteed obliges a mechanism**, and somebody to keep it working. That is the
only obligation here that lands on the harness rather than on the context
budget.

**It is also the only promise anything can check.** A mechanism either exists or
it does not, which is decidable in a way nothing about the other three is. That
cuts both ways: where nothing checks, a declaration reads as kept when it is
not, and the author, the adopter, and anything auditing all stop worrying about
it on the strength of a word.

**Expected raises the session floor by the size of its announcement, and that
is its price.** For a model to notice something, the announcement has to be
present before the moment of noticing. This is the category where a model's
judgement is load-bearing and where a failure is silent.

**Optional obliges an announcement, the same as expected.** For a model to
choose something it has to see it, so the price is whatever that announcement
costs, and only the meaning of an absence differs.

**Standby obliges an address and some way to reach it**, plus whatever
announcing that way costs. Whether the way must be a helper, should be one, or
may be a path given to a model directly is open, and it is what decides whether
the floor is one announcement or none.

## The trade every category answers

**Both failures are opposite, and the whole design sits between them.** A floor
set too high and every session pays for context it never touches. Set too low
and the model does not know the right thing exists, so it either misses it or
over-fetches to be safe. **As low a session floor as possible, and still enough
to choose correctly** — getting that trade right is most of why these tools
exist.

**Each category answers it in its own currency.** `guaranteed` in how wide its
matcher is, `expected` and `optional` in how large an announcement, `standby` in
how findable it is willing to be. **Overuse any of them and the pain is the same
size in a different shape** — a floor nobody needed, a model that cannot find
what it needs, content nobody ever asks for. Which turns out to be the worst
failure in practice is not knowable from here, and nothing in this document
should be read as claiming otherwise.

**Where a single instance cannot be verified, a trend can be.** When no tool can
say *this should have been opened and was not* at the moment it happens, grading
one session is the same unanswerable question in smaller form. **What is
observable is longitudinal** — across many sessions, whether the right thing is
being opened more often than it used to be. An adopter who can see that can act
on it, by rewording an announcement, moving a document to `guaranteed`, or
dropping it to `standby`.

That is a weaker instrument than a check and a far stronger one than nothing,
and it is what makes `expected` improvable rather than merely hoped-for. **How
such a trend is gathered is unsolved** and belongs on the problem list rather
than being assumed here.

**A miss is recoverable, not terminal.** Anything offered can still be asked for
by name after the fact — by a person, by another agent that noticed what this
one did not, or by a hook whose own checks caught the miss. **What provides it
belongs to Entry 5; that it exists belongs here**, because it changes what a
miss costs and therefore how much skepticism the category actually deserves.

**And requesting is not only a safety net.** It is recovery here, and it is
`standby`'s only way in — so whatever Entry 5 provides for it carries a whole
category rather than a convenience.

## Candidates, neither settled

**The default is now a real question rather than an obvious one.** It used to
look settled: guaranteed costs a mechanism and expected costs an announcement,
so a document declaring nothing should fall into the cheapest thing. With
`standby` in the taxonomy the cheapest thing is no longer `optional` — it is
`standby`, whose floor does not grow however much sits behind it, and which is
also invisible.

That sharpens the trade rather than settling it. **`standby` as the default**
means an author who forgets a field ships something only a person who already
knows its name can reach, which is close to not shipping it. **`optional` as the
default** means forgetting a field buys standing context in every adopting
project, which is the cost this design exists to control. Problem 4 above owns
the answer; both readings are live.

**Strength may be a separate axis.** *Expected* says an absence is a miss; how
badly it is a miss is a different question. Keeping them apart costs nothing
now, and something may yet show that the useful combinations are few enough to
collapse them.

## What this is not

**Not the prototype's always-on / advertised / on-demand.** Those classify *when*
something loads. These classify *what its absence means*. The prototype
conflated the two, which is why it never produced a check worth running.

## Open

**The design has room for one voice and needs several.** Everything above is
declared by an author who has never seen the adopting project. An adopter knows
things the author could not — a bundle's expected content is too noisy here, or
should apply only under `src/`, or was adopted for one workflow and should stop
volunteering its policies. A governing body — security, compliance, whoever
answers for the organization — knows things the adopter is not entitled to
overrule.

**They may not want the same mechanism.** An adopter adjusting a category is an
override: the binding resolves differently. A governing body forbidding content
outright is a boundary nothing in the project can reach past, which is `expose`.
Whether those are one mechanism with a precedence order, or several with
different reach, is open.

**And authority need not mean an unreachable declaration.** A governing body's
rule could live somewhere the adopter cannot edit, which prevents a violation.
Or it could live in the repository like everything else, with something external
checking that the repository still complies — which reports a violation instead.
**This design already prefers the second shape elsewhere**: a vendored bundle is
editable and the checksum detects the edit rather than forbidding it. Which is
right here depends on whether a governing body needs violations stopped or
needs them found.

Several problems already on the list are facets of this rather than separate
things. Entry 4's *Enablement* is an override to never; its *Precedence* is what
happens when claims collide; its *Level* — bundles declaring who they are for —
is the same question seen from the bundle's side. If this is designed in one
place, those should point at it.

**A checking mechanism may be a cheaper `guaranteed`, and is worth
considering.** The obvious implementation loads on every match, including every
time the model would have loaded the content anyway. One that instead notices
the content is absent when it should be present pays the body only on a miss.
Same promise, different bill. Whether that is a better default, a special case,
or a thing only some harnesses can do belongs to Entry 5.

**What implements `guaranteed`, and what a harness has to have for it.** Hooks
are not the only route. An **unconditional** guarantee needs only a file the
harness always loads — `CLAUDE.md` and its equivalents, which nearly every
harness has — and it pays the whole body into the session floor for the
privilege. A **conditional** one needs something that evaluates the condition and
injects, which fewer harnesses offer.

**So the matcher decides which mechanisms can serve it**, not just what it costs.
A harness that cannot evaluate conditions can honour `matches: always` and
little else. What it should then do with a conditional guarantee — refuse it, or
degrade it to `expected` while it still reads as guaranteed to everyone who
declared it — belongs to Entry 5.

---

# Entry 2 — what a bundle is

**Not yet written.** Problems captured; the mock-up and the fields come after
they are settled.

## What it has to solve

1. **Identity.** How a bundle is named, whether that name survives moving
   between catalogs or the repository being renamed, and what a bundle written
   in a project takes as a namespace when there is no catalog behind it.
2. **Contents.** What a directory must contain to be a bundle, what it may
   contain besides, and what a well-formed one carries even where nothing
   requires it.
3. **Version.** What the number promises, and what counts as breaking when the
   thing versioned is knowledge rather than an API.
4. **Boundary.** What belongs in one bundle rather than two — a bundle is a
   distribution unit, so the test is what gets published together, not what gets
   read together.
5. **Self-description.** How a bundle says what it holds, and what that costs a
   reader who opens it.
6. **Local versus published.** Whether a bundle written here differs
   structurally from an adopted one, or only in what is recorded about it.
7. **Dependency.** How something says it assumes knowledge it does not contain,
   what gets named in that assumption — a bundle, a document, or a capability
   that is neither — and what happens when nothing present satisfies it.
8. **Interface.** What one bundle may rely on in another, and what stays private
   to it. If any document can be cited from anywhere, every internal path is
   public and nothing inside a bundle can be moved without breaking somebody.

**Inherits from Entry 1** — the loading categories, which *Self-description* has
to produce: what a bundle says about itself is a claim that some of its contents
are expected and the rest optional.

## Notes carried in with the problems

**Dependency and Interface are one question from two sides** — what may be
relied on, and how reliance is declared. If Interface resolves to *only
capabilities are public*, Dependency has no remaining choice to make and the two
collapse into one.

**Dependency's grain is open.** Presence is bundle-grained and reading is
settled per case, so declaring `needs` at either level is defensible and nothing
above rules out either. What decides it is who can act: the
adopter works in bundles, at fetch time, while a document's need surfaces at
delivery time to an agent mid-task who cannot adopt anything.

## What touches a bundle

**Every item below is a demand on what a bundle has to carry.** *Minimal* is the
least that would work; *ideal* is what would make it good. Prose is noted only
where it earns a line — most of these are read by tools, and silence means no.

They are collected here rather than in the entries that own each moment, because
the question this entry answers — what a bundle holds — is answered by all of
them at once rather than by any one.

### Authoring and publishing

**An author creates a bundle from nothing**
*Minimal.* A name and a version exist.
*Ideal.* A scaffold that cannot produce an invalid bundle, and a check that says
whether one is valid.

**An author adds or removes a document**
*Minimal.* The version moves, and nothing the bundle still declares points at
what left.
*Ideal.* The bundle's own index cannot fall out of date, and internal references
are checked rather than remembered.

**An author changes a rule's meaning, behavior, or outcome**
*Minimal.* The version moves at the level that says this breaks something.
*Ideal.* Plus what changed, and what an adopter has to do about it.
*Prose.* The *why* is the part a maintainer needs, and no field carries it.
And it should never get loaded into context unless requested or necessary.

**An author patches typos or prose without changing outcomes**
*Minimal.* The smallest part of the version moves.
*Ideal.* The record separates *nothing to do here* from *read this before
upgrading*, so an adopter can make informed upgrade decisions.

**An author, agent, or CI updates a changelog**
*Minimal.* Somewhere to append.
*Ideal.* Consistent enough in shape that something can answer *what changed
since the version I have*.
*Prose.* Almost entirely prose, which is exactly why it belongs outside anything
loaded during work.

**An author changes a bundle version**
*Minimal.* The version is stored in one place.
*Ideal.* Plus something that checks the size of the bump against the size of the
change.

**An author decides what belongs here rather than in a new bundle**
*Minimal.* What is already in the bundle.
*Ideal.* Plus a stated scope, so *does this fit* is answerable rather than felt.
*Prose.* A boundary is a judgement and does not reduce to fields.

**An author declares what the bundle provides**
*Minimal.* Some way to say it that does not name anything else.
*Ideal.* Plus knowing that another author, elsewhere, means the same thing.

**An author declares what it needs provided**
*Minimal.* The same, in the other direction.
*Ideal.* Plus what should happen when nothing satisfies it.

**A curator validates a bundle before it goes into a catalog**
*Minimal.* Whatever a bundle must have is present.
*Ideal.* Plus links resolve, matchers parse, and nothing collides with what the
catalog already holds.

**Someone browses a catalog deciding what to take**
*Minimal.* Its name, its version, and the long description.
*Ideal.* Plus what it provides and needs, who it is for, and some signal of what
it will cost in session floor.
*Prose.* Here the prose is the product — this reader is a person deciding.

**A bundle moves, promoted out of a project or between catalogs**
*Minimal.* An identity that does not encode where it currently lives.
*Ideal.* Plus a trace of where it came from, so an adopter can follow it.

### Fetching

**A project takes a bundle it has never had**
*Minimal.* A source, an identity, a version, and a way to tell that what arrived
is what was sent.
*Ideal.* Plus enough to know it will work here before taking it — its needs are
satisfiable, its level is appropriate, and nothing already present precludes it.
These might be prechecks, since apply is probably where the primary gate should reside.

**A project checks whether something newer exists upstream**
*Minimal.* The version it took, and somewhere to ask.
*Ideal.* Plus what changed, answerable **without fetching first**.
*Prose.* The answer to *should I care* is the changelog.

**A project verifies its copy is unmodified**
*Minimal.* A checksum over the copy.
*Ideal.* Plus which files differ, since *something changed* is not actionable.

**A project takes a newer version over an older one**
*Minimal.* The new copy replaces the old.
*Ideal.* Plus a refusal when the copy was edited here, and a statement of what
the adopter now has to do. A framework for mechanical migrations.
*Prose.* Upgrade instructions, where a version needs them.

**A project stops using a bundle**
*Minimal.* The directory and the record both go.
*Ideal.* Plus a warning when something else was relying on what it satisfied.

**A tool detects a directory nobody adopted, or a record with no directory**
*Minimal.* The record, and a walk of what is on disk.
*Ideal.* Nothing further — this one is already complete.

**A bundle requires a given tool or command to exist**
*Minimal.* The get system warns when the tool is missing.
*Ideal.* The get and/or apply system helps the user resolve missing tools, 
requiring prior user confirmation.

**A bundle's needs are unsatisfied and something says so**
*Minimal.* What this bundle requires, and what everything present offers.
*Ideal.* Plus what could be taken to fix it.
This is a more broad version of the use case above, outside of command line needs.

**A set of bundles is taken together rather than one at a time**
*Minimal.* Something naming what is in the set.
*Ideal.* Undecided, and it turns on whether a set is just a bundle that declares
needs and holds nothing.

**A bundle from one catalog satisfies a need declared by a bundle from another**
*Minimal.* Whatever expresses the need and whatever expresses the satisfaction
are comparable across catalogs that never coordinated.
*Ideal.* Plus confidence that both sides mean the same thing — which is the
unsolved problem below.

**An organization replaces part of a public bundle, keeping the rest**
*Minimal.* A way to stop one part applying without forking or dropping the
bundle.
*Ideal.* Plus detection that both the original and the replacement are present,
so the substitution is visible rather than silent.

**Something already present precludes the bundle being taken**
*Minimal.* Enough to detect the conflict at all.
*Ideal.* A warning rather than a refusal — the adopter may be doing it on
purpose, intending to silence the other.

### Registering

**A tool resolves what answers which condition, and what each workflow is called**
*Minimal.* Every document's matcher, type and name are discoverable.
*Ideal.* Discoverable without opening every file, which matters only at scale.

**A tool settles a collision between two bundles claiming one name**
*Minimal.* Both claims, and which bundle each came from.
*Ideal.* Plus a rule producing **stable** results, so a name an agent learned
yesterday is still there today.

**A tool applies whatever the adopter overrode**
*Minimal.* The overrides, and what each attaches to.
*Ideal.* Plus a complaint when an override points at something that no longer
exists, since it otherwise does nothing silently.

**A tool checks the mechanism a declaration depends on actually exists**
*Minimal.* What mechanism each declaration needs, and whether this harness has
it.
*Ideal.* Plus what to do when it does not — refuse, degrade, or warn.

**A tool detects that two providers contradict rather than compose**
*Minimal.* Both declarations, and whether the thing they share tolerates company.
*Ideal.* Plus which two, and what an adopter can do about it.

### Working

**An agent orients — what does this project know**
*Minimal.* A line for each thing this project holds. Whether "thing" means a
bundle, a document, or something else is undecided — and that choice sets the
session floor, which makes it the most consequential open question here.
*Ideal.* Whichever grain produces the most useful matches for the fewest bytes.

**An agent judges whether a bundle bears on the work**
*Minimal.* The bundle's announcement — the short string a model compares against
what it is currently doing.
*Ideal.* An announcement written to be matched against work rather than to
persuade somebody to adopt. Those are different jobs and one string will not do
both well.

**An agent opens a bundle to see what is inside**
*Minimal.* A line for each document, saying enough that a reader can pick one.
*Ideal.* Plus which to read first, and nothing listed that a reader cannot
actually open.
*Prose.* *Read this one first* is a judgement the author holds and no field
expresses.

**An agent loads one document**
*Minimal.* A path.
*Ideal.* Nothing further — already fully served.

**A mechanism injects a document because a condition fired**
*Minimal.* The condition that fired, the document to inject, and something able
to do the injecting.
*Ideal.* Plus a way to know the document is already in context. Without it, a
condition firing forty times injects the same body forty times. Injection is
logged so we can debug, observe, and improve.

**Somebody names a document and it loads**
*Minimal.* A name, and something that turns that name into content.
*Ideal.* Names stable enough that one learned in a previous session still works
in this one.

**A document cites another document**
*Minimal.* The citation resolves to something loadable.
*Ideal.* It still resolves after the target is renamed or moved, which
constrains what a citation may be made of.

**An agent needs part of a document rather than all of it**
*Minimal.* The document has parts that can be addressed separately.
*Ideal.* Those parts are declared by the author rather than inferred from
headings by whatever is reading.

**An agent finds something inside a bundle without reading the whole thing**
*Minimal.* Some way to look that is not reading everything.
*Ideal.* That way costs measurably less than reading would have. If it does not,
it is a name for the problem rather than a solution.

### Maintaining

**A maintainer reads what changed between two versions**
*Minimal.* A record of what changed, kept per version.
*Ideal.* Readable without having both copies to compare, and structured enough
to answer *since the version I hold*.
*Prose.* What changed and why it matters is a judgement, not a diff.

**A maintainer decides whether an upgrade is worth taking**
*Minimal.* What changed.
*Ideal.* Plus what it costs them specifically — whether anything they overrode
disappears, whether a name they rely on moves.
*Prose.* Whether a change matters here is exactly the judgement a changelog is
written to support.

**A maintainer diagnoses why something did not load when it should have**
*Minimal.* What was supposed to load, and what actually did.
*Ideal.* Plus which stage failed — it never landed, it landed but was never
registered, or it was registered and did not load. Three destinations, three
places to look.

**A maintainer finds what is costing the most session floor**
*Minimal.* What is resident before work starts, and how large each part is.
*Ideal.* Plus whether it was ever used, so cost can be weighed against benefit
rather than reported alone.

**A maintainer edits a vendored copy deliberately and wants that recorded**
*Minimal.* Some way to say the edit is intentional, so integrity checking stops
reporting it as damage.
*Ideal.* Plus what was changed, so a later upgrade knows what to preserve rather
than silently discarding it.
*Prose.* Why somebody diverged is the part that will not be reconstructable
later.

### Governance — the rule exists

Someone with authority says so. Nothing is enforced or checked by the saying.

**A governing body declares a rule that reaches repositories which did not ask
for it**
*Minimal.* Somewhere a rule can be stated that the projects it binds do not own.
*Ideal.* Plus a project being able to see that a rule applies to it, rather than
finding out when something fails.

**A governing body forbids content, or restricts which bundles a session, agent
or model type may load**
*Minimal.* A way to name what is forbidden that survives the thing being renamed.
*Ideal.* Plus restricting by **who is asking** and not only by what is asked
for — a rule that holds for one model and not another is a different axis from a
rule about content.

**A governing body mandates that something load and the project may not demote
it**
*Minimal.* A declaration that outranks the project's own.
*Ideal.* Plus the project being able to see that it was outranked, rather than
wondering why its override did nothing.

**An adopter attempts an override they are not entitled to make**
*Minimal.* The attempt does not take effect, and says so.
*Ideal.* Plus naming who forbade it and where that came from, so the adopter can
go argue with a person rather than with a tool.

### Enforcement — the rule happens

Mechanical, in the harness, at the moment of action.

**A harness refuses to load content the rules forbid**
*Minimal.* The harness can see the rule at the moment of loading.
*Ideal.* Plus refusing in a way the agent can tell apart from the content simply
not existing.

**A harness restricts what an agent may touch**
*Minimal.* A boundary the harness can apply.
*Ideal.* Mostly outside a bundle's concern — a bundle contributes the rule at
most, never the mechanism.

**Something loads because a rule required it, not because anyone chose it**
*Minimal.* The same mechanism `guaranteed` needs.
*Ideal.* Plus the agent knowing it arrived by mandate rather than by relevance,
since that changes how much weight it should carry against what the work
actually is.

### Compliance — the rule is checked

Outside the harness, after the fact.

**A check runs against a repository and reports what does not match**
*Minimal.* The rules and the repository state, in comparable terms.
*Ideal.* Plus running without the harness at all, since whoever checks
compliance is generally not the person running the agent.

**A violation nobody prevented gets found**
*Minimal.* Detection after the fact.
*Ideal.* Plus when it started, so the blast radius is knowable rather than
assumed.

**A project proves it conformed, to somebody who was not watching**
*Minimal.* A report.
*Ideal.* Plus something the project being checked cannot forge — self-reported
compliance is worth roughly what it costs to produce.
*Prose.* An exception is a judgement somebody has to explain and somebody else
has to accept.

## Findings already out of this list

**Prose earns a line in eleven of fifty-two use cases, and never for a tool.**
Registering, governance and enforcement want it in none of their rows — those
are the most mechanical moments in the design. Where it does appear it clusters
on three things: **a change** (what moved and whether it matters), **a
judgement** (does this fit, read this first, is this exception acceptable), and
**a sell** (is this worth taking). That is most of the answer to *what value
does prose have*, arrived at by counting rather than by asserting.

**A bundle carries two descriptions, not one.** Catalog copy answers *is this
worth having* for somebody deciding whether to adopt, and is read once, before
the bundle is here. An announcement answers *does this bear on what I am doing*
for a model, and is paid for in every session forever. Different audiences,
different lengths, different costs — and the prototype's single `description` is
the catalog string, which is part of why the announcement has no natural size.

**The long description is sidecar material.** It has to travel with the bundle
so somebody deciding whether to take it can read it, and nothing needs it once
the bundle is here. That puts it in the same class as a changelog: present in
the bundle, rarely in the session, never in the floor. A catalog is one
consumer of it rather than the reason it exists — a bundle with no catalog
behind it still wants one.

**Whatever expresses these relationships should ideally cross organizations
that never spoke.** A bundle from one catalog can satisfy something a bundle
from another declared, and an organization can replace part of a public bundle
while keeping the rest. Both are wanted. Both mean the vocabulary spans
boundaries nobody governs — so two organizations can coin one term meaning
different things, a substitution silently succeeds, and the wrong policy
applies with nothing to catch it. **Nothing discussed so far solves this**, and
it is the hardest problem this list has produced. It is a constraint on any
shape, not an argument for one.

**And it is not an MVP problem.** It cannot happen until two organizations
publish independently, so there is nothing yet to test a solution against and no
way to tell a good one from a plausible one. What is worth having near MVP is
the **shape of the declaration** settled — changing that later is expensive,
while changing what it means is not.

**A name alone would not carry enough.** Whether a thing tolerates more than one
provider cannot come from the providers — two bundles cannot settle between
themselves whether what they share admits company. And *what could satisfy this*
has to be answerable from somewhere when nothing does. Both are demands on
whatever shape is chosen; neither says where the knowledge lives, when it is
computed, or that a name is the right unit at all.

**Substitution may need no precedence rule**, under at least one shape.
Replacing part of a public bundle with your own looks like it requires deciding
which wins. It does not, if two answers to one question can be detected as a
conflict: the adopter silences one and theirs stands. That is adopter override,
which is needed anyway. **Precedence — nearer or later automatically wins —
would be a resolver**, and this is the second feature that looked like it needed
one and did not. In any case, warning the adopter is ideal, so nothing about it
is a surprise.

## What Dependency and Interface have to solve

**These are the part of this section to trust.** They hold whatever shape ends
up chosen, and they were derived from the use cases above rather than from any
mechanism. The shapes that follow them are parked, not proposed.

**A bundle assumes knowledge it does not contain.** A sweep workflow that says
*check whether work landed* assumes an integration policy exists somewhere. If
nothing provides one, the agent proceeds anyway on whatever it invents. → *An
unmet assumption has to be detectable.*

**Two independently-authored bundles say contradictory things and nothing
notices.** One says never squash, another says squash freely. Both load, the
model follows whichever it saw, and nothing crashes. → *Contradiction between
bundles that never met has to be detectable.* Bundles should be curated rather
than greedily consumed, but curation cannot solve this on its own.

**An organization wants most of a public bundle and not one part of it.** Their
merge policy differs; the rest is fine. → *A project has to be able to
substitute its own answer for part of an adopted bundle without forking it.*
I'm not sure if this is a good idea, but it's something to consider.

**A bundle cannot know what else exists.** It is authored once and adopted into
projects that do not exist yet, beside bundles that do not exist yet. →
*Relationships have to be expressible without naming anything.*

**More than one thing may legitimately answer the same question differently.**
Landing work from a worktree and landing it normally are both *did this land*,
under different conditions, and both are right. → *Coverage from several sources
has to be expressible without reading as conflict.*

### Shapes that have come up, none of them chosen

Most of this should get handled later in the roadmap because some or most of it 
will not be necessary for the MVP.

**Recorded so the reasoning is not rebuilt, and kept subordinate on purpose.**
Each was reached by elaborating a mechanism rather than by working from the
problems above, which is the wrong direction and how a design acquires
machinery nobody asked for. `provides` and `needs` is one to consider, not the
answer.

**Capabilities** — a document declares what it provides and what it needs, by
name rather than by pointing at anything. Handles *name nothing* well. Struggles
to separate contradiction from coverage, and pushes a vocabulary problem across
organizational boundaries with nobody to govern it. The reason we name needs is
because users need to be able to replace the default with their own version 
and naming specific bundles does not work for that use case.

**Direct references** — a bundle names another. Simplest, and fails *name
nothing* outright: the reference goes stale when the other bundle is renamed,
moved, or replaced by an equivalent. Direct references may still be viable with
eyes open, but cannot be the only option.

**Project-level declaration** — the project states what it has and what it
wants; bundles declare nothing. Puts the knowledge where the facts actually are,
at the cost of every adopter doing work an author could have done once.

**Convention** — documents about the same subject collide by path or type, and
the collision is the signal. No new vocabulary at all; weak precision.

**Read the content.** A model notices that two policies contradict without
either having declared anything. The only shape that catches contradictions
nobody anticipated. Expensive, unreliable, and newly plausible in a way it was
not a few years ago.

### What the index might be

**Unsettled, and this one does block things.** *The index* means whatever a
reader gets on opening a bundle — the listing of what is inside.

**Authored.** Written by hand. Carries judgement no document can: *read this
first*, grouping, and prose explaining how the parts relate — none of which
lives in any single document, because no document knows about the others. Goes
stale, duplicates every description, and makes each addition two edits.

**Derived at read time.** Computed from the documents whenever wanted. Cannot go
stale, duplicates nothing, needs no maintenance. But it requires the tool to
exist in order to see it, which cuts against `.luma/` being committed so a clone
reproduces with nothing installed — and ordering falls back to something
arbitrary.

**Generated at publish, shipped as a file.** Fresh whenever publishing happens,
readable with no tooling, nothing maintained by hand. Stale for anything that
skips publishing, and it is a generated file living inside what a checksum
covers.

**Split — facts derived, judgement authored.** A small authored piece saying
*read this first, these belong together, that one is an exception*, with the
listing computed. Each half sits where it cannot go wrong; the cost is two
things instead of one and a boundary that has to stay sharp.

**Three places structure could come from**, and only the first is an index.
Authored, as prose in the bundle. Declared, as a field on each document —
ordering is the obvious candidate. Or **read off the links between documents**:
a self-contained bundle whose documents cite each other already carries a graph,
and relatedness can be derived from it without anything declaring a group.

*Interface does not forbid that.* It exists to stop a bundle reaching into
another bundle's internals; documents inside one bundle ship, move and version
together, and the wikilink convention already assumes they name each other.

**The question that decides it, then:** does a bundle need to say anything about
its documents that neither a field nor the links can express? What a link does
not carry is the **nature** of a relation — that one document is the exception
to the others, or supersedes them, is not something *A cites B* says. Whether
that belongs in an index, in the documents themselves, or nowhere is open.

**What it blocks.** Entry 1's problem 8 waits on it, because *does a bundle have
a body* is the same question wearing different clothes. So does **Contents** —
whether an index is something a bundle must contain. And so does the sidecar
question, since a derived index is not bundle data at all.

**What will force it:** writing anything that opens a bundle, or the first
bundle whose documents change often enough that a stale listing bites somebody.

### What the shapes have in common

**Four of the five problems are detection problems**, and detection is where
this design keeps landing. The one that is not — substitution — turned out to
reuse adopter override rather than needing a mechanism of its own. So it is
possible the whole area needs less declaration than any of these shapes assume,
and that is worth testing before any of them is built.

---

# Entry 3 — what a document is

**Not yet written.** Problems captured.

## What it has to solve

1. **Assets.** Templates and examples are not documents. What distinguishes a
   file an agent should read from one that is only material for a workflow.
2. **Adapter input.** The least a workflow must declare for a harness to install
   it as something invocable, given the document cannot know which harness will
   read it.

**Inherits from Entry 1** — the loading categories, which a document's matcher
has to select one of. **From Entry 2** — *Contents*, which decides what may sit
in a bundle at all, and *Interface*, which decides whether a document is
addressable from outside its own bundle.

---

# Entry 4 — what a project records about them

**`.luma/bundles/MANIFEST.md`** — every bundle this project has, vendored or
written here. It is the project's statement of what it carries, which is a
different thing from what happens to be on disk.

## What it has to solve

1. **Membership.** What is part of this project — so a stray directory and a
   missing one are both reportable.
2. **Provenance.** Where a copy came from, and at what point in that source's
   history.
3. **Integrity.** Whether a copy has been changed here since it landed.
4. **Currency.** Whether something newer exists upstream.
5. **Divergence.** Whether an edit to a copy is *intentional*, so the integrity
   check stops reporting it. See
   [a bundle should be able to diverge](../ideas/a-bundle-should-be-able-to-diverge.md).
6. **Reproducibility.** Whether a copy could be re-fetched exactly from what a
   record holds — and whether that is a promise worth making at all.
7. **Level.** Bundles declare who they are for. Whether adoption at a level
   records anything here.
8. **Enablement.** Whether a bundle can be present and switched off.
9. **Precedence.** Whether this file decides anything when two bundles collide.

**Inherits from Entry 2** — *Identity*, because a record is keyed by a name this
entry does not define; and *Version*, because Currency compares against a number
whose meaning is set there.

## Mock-up

```markdown
---
type: manifest
---

# Bundles

Every bundle this project has. Add a line to claim one; `luma-foreman get`
fills in the rest when it copies one in. A line with no source came from
nowhere but here.

- `lumastack/git-secrets` 0.5.1
  source: https://github.com/LumaStack/luma-catalog
  commit: 8ec0cce285bb27f0b6c58bacb62d37bd62a702ee
  sha256: 2eb6115374ff3202da0fccc0452e044f6011dde17948bef76df2ab56243ac72d

- `lumastack/adoption-internals` 0.1.0
```

## What the mock-up is asserting

**The record's existence is the fact.** A directory holding a bundle is
indistinguishable from one that wandered in; only a manifest can say which
belong. That is what a directory walk structurally cannot provide — whatever a
walk finds is by definition what is there, so it can never report a stray.

**The kinds are distinguished by shape, not by a flag.** Presence of
source/commit/sha256 marks a copy. No `local: true`, because a flag restating
what the other lines already show is a second copy of one fact.

**Every entry carries a version.** For a copy it is the version taken, frozen
until it is taken again. For a bundle written here it is what the bundle
currently is, and nothing but the author keeps it current — so `inspect`
compares it against the bundle's own self-description and reports disagreement.

**The file is authored, not generated.** `get` edits it the way
`npm install --save` edits `package.json`. It carries no *do not edit* banner,
and that single property decides the format below.

## Why markdown rather than TOML

**Python's standard library reads TOML and cannot write it.** `tomllib` is a
parser only. A tool that must edit an authored TOML file has three options and
all of them are bad: regenerate the whole file and destroy its comments and
ordering, take `tomlkit` as a dependency, or hand-roll a partial TOML editor out
of regexes.

**And no dependencies is a published promise** — *"Requires Python 3.11+ and
git. No dependencies, no build step."* TOML was the right format for a generated
receipt, which is what this file used to be. It is the wrong one for an authored
manifest, which is what it now is.

Markdown wins on the properties that actually apply:

- **Editing is line-oriented, so round-tripping is free.** A tool finds one
  entry and replaces its block; everything else on disk is untouched by
  construction.
- **Diffs are cleaner than TOML's.** Adding a bundle is four contiguous added
  lines; bumping a version is one changed line.
- **It carries prose.** Not comments bolted onto a data file — a document that
  explains itself.
- **It matches the estate.** Every reserved file is ALL-CAPS markdown. A lone
  `.toml` among them is the odd one out.
- **There is precedent for the parser.** `lkf.py` is 125 hand-rolled lines that
  deliberately chose a subset over a dependency, for this same reason.

**The cost, stated plainly:** a format nobody else knows, and a malformed
hand-edit gives a parse question rather than TOML's clean error. Keeping the
grammar dumb — one bullet per bundle, `key: value` sublines, nothing nested — is
what holds that cost down.

## Open — the fields are not derived yet

`commit` is in the mock-up and has no problem behind it. It earns its place only
if Reproducibility resolves to *yes, a copy can be re-fetched exactly* — and if
that is not a promise this makes, the line comes out and provenance is `source`
alone.

**This is the entry's own method applied to itself.** The mock-up above began as
the prototype's four columns with problems retrofitted underneath. Every field
still has to survive the question *if the prototype did not exist, would this be
here?*

## Open — placement, and scope

`.luma/bundles/MANIFEST.md` assumes the directory stays `bundles/`. If the
knowledge tree is renamed the file moves with it and the name still holds. Also
open: whether membership belongs in a file of its own at all, rather than in a
project configuration alongside other settings.

**And whether this file records more than what landed.** A manifest that only
says *what landed on this machine* excludes bundles written here, which never
landed from anywhere — which would make it a receipt again, take the
stray-directory check with it, and reopen the format decision above.

---

# Entry 5 — how knowledge reaches a harness

**Not yet written.** Problems captured.

## What it has to solve

1. **Granularity of loading.** What must be declared so the right part loads
   at the right moment, and at what grain that is decidable: the bundle, the
   document, or something smaller.
2. **Harness independence.** What a bundle may assume about whatever is reading
   it, and where harness-specific work lives instead — thin enough that a second
   harness is an adapter rather than a fork.
3. **What implements each category.** Carried from Entry 1: what makes something
   guaranteed in a harness that has hooks, and what happens in one that does not.
4. **Declared or derived.** Whether a matcher states how a document loads, or
   whether that is computed from the matcher's shape.

**Inherits from Entry 1** — the categories themselves. This entry decides what
implements them; it does not get to redefine them. **From Entry 2** —
*Self-description*, which decides what a reader gets on opening a bundle. **From
Entry 3** — *Adapter input*, which decides what a harness has to work with.

## How loading might be structured

**Parked, and recorded so none of it is re-derived.** Nothing here is chosen.

### The shape this started from

| ring | holds | fired by |
| --- | --- | --- |
| **`1-project`** | what this repository knows | the harness, at session start |
| **`2-bundle`** | what one bundle holds | reaching for that bundle |
| **`3-document`** | what one document holds | opening that document |
| **`4-section`** | content — the leaf, with no map of its own | reading it |

**Numbers go inward**, so what is outside everything you have is `0`.

**One rule at every level: a map names the members of the next ring in.**
`1-project` names bundles, `2-bundle` names documents, `3-document` names
sections. Nothing to memorise beyond that.

**Firing a ring delivers two things and only two:** what is always true at that
level, and the map of the next ring in — every item's name, what it is for, and
what fires it.

**What it buys.** One rule at every level, so the same model works everywhere. A
floor that is O(bundles) by construction rather than by discipline. And it
anticipates sections, which answers *needing part of a document* before anyone
asked.

**What it costs.** Ring 1 names bundles, so the floor becomes a set of
predictions that everything inside each bundle is relevant together — which the
settled bullet says is false. When a bundle's line does not match, everything
inside it is unreachable however well one document would have matched. And
strict nesting assumes traversal is the only route, which it no longer is:
`guaranteed` content is injected without any map firing, a request names a
document directly, and a citation jumps sideways.

### Announcement grain

**Only bundles announce.** Cheapest floor. A document is unreachable when its
bundle's line does not match.

**Only documents announce.** Better matching, a floor several times larger, and
no line saying what a bundle is *for*.

**Both, always.** Most reliable, most expensive, and the two layers largely
restate each other.

**Bundles by default, documents opt in** where a bundle's line would not surface
them. This is the four categories doing the work at both grains. Its weakness is
that an author decides the opt-in while guessing about work they will never see.

**The tension:** the uniform rule and the missed-bundle failure come from the
same property. Relaxing the nesting so ring 1 may name something deeper fixes
the failure and costs the rule.

**Unsettled, and it can stay that way for now.** It blocks nothing — the four
categories work at any grain, and every use case in Entry 2 is served either
way. **What it does decide is the session floor**, which is the only cost paid
whether or not the work touches it, so no project's floor can be sized until it
is chosen. **What will force it:** the first real measurement of a floor, or the
first project carrying enough bundles that the difference between eighteen lines
and ninety stops being theoretical.

### Arriving without traversing

A workflow invoked by name, a request, or a citation all arrive part-way in.
What should come with them:

**The container's guarantees, transitively** — one rule for every route, at the
cost of a workflow's price never being just the workflow.

**Nothing** — standalone, predictable, and the workflow may assume a policy it
does not get.

**The thing's own declared needs** — precise, reuses a mechanism the design
needs anyway, and fails quietly when an author forgets.

**An announcement of the container's guarantees, without loading them** — cheap,
and it converts a guarantee into an offer, which is the degradation Entry 1
warns about.

**Nothing guaranteed below ring 1** — simplest possible model, and the
offered-bundle-with-required-policy case becomes inexpressible.

**The entry point declares its own behaviour** — control, at the cost of the
uniform rule and of an author guessing again.

### What would decide any of it

**Is a workflow ever safe to run without its bundle's policy?** If never, the
pull is mandatory. If usually, it is waste most of the time.

**How large can a container's guarantees get?** Cheap at a paragraph, ruinous at
a bundle's worth of policy — and nothing bounds it, which is problem 6 arriving
at another level.

**Uniform or per-case?** Every shape but the last applies one rule everywhere.

**Unsettled, and safe to leave so.** Nothing structural waits on it — this is
runtime behaviour that can be added or changed without disturbing what a bundle
holds. **What it does decide is what invoking a workflow actually costs**, and
whether a workflow may assume the policy its bundle guarantees. **What will
force it:** the first workflow that misbehaves because it did not get its
bundle's policy, or the first time anyone measures what invoking a skill drags
in behind it.

### Settled for MVP

**Workflows announce at ring 1 eagerly**, because the harness registers every
skill's name and description at startup and an adapter cannot know which bundles
a session will open. **That is a harness limit rather than a design choice.**
Past MVP a dispatching super-skill, commands, files regenerated between turns,
or hooks that register mid-session each change it.

---

# Entry 6 — how a bundle reaches a catalog

**Not yet written.** Publishing is a different movement from fetching — a
different actor, at a different moment, into a repository nobody adopting has
written to. Splitting it out is what stops the two being reasoned about as one.

**Inherits from Entry 2** — *Identity*, which decides what a bundle is called
where others will find it; *Version*, which decides what a release promises; and
*Boundary*, which decides what is released together.

---

# Entry 7 — how a bundle reaches a repository

**Not yet written.** No problems are unique to it yet, and saying so is more
honest than inventing some.

**Inherits from Entry 2** — *Identity*, since a copy is keyed by it. **From
Entry 4** — *Provenance*, *Integrity*, *Currency*, *Divergence* and
*Reproducibility*, each of which is recorded there and exercised here. This is
also where a bundle is **adopted** rather than merely landing, and the
difference between those is Entry 4's to detect.
