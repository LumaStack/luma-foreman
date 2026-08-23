---
type: luma/idea
title: A shared language for workflows invoking other workflows
created: { by: human:benlinton, at: 2026-08-21T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
---

# A shared language for workflows invoking other workflows

A workflow should be able to say that another workflow or command runs before it,
during it, or after it — and every workflow and tool should read that the same
way. The motivating case: `migrate-ideas` running `index-repositories` when the
index is stale, rather than reading a stale one and mentioning it.

## The problem it addresses

**Workflows already do this in prose, informally.** `index-repositories` says
*"read [[the-repository-index]] first"* and *"[[create-internal-hq]] is a
prerequisite"*. Nothing can act on either. An agent reads it, or does not.

**And the cross-cutting cases have no expression at all** — logging, journalling,
record keeping, rot checking, auditing. Every workflow needs them; none can say
so.

## The shape, as far as it got

**Declared in frontmatter with a slug, referenced by that slug in the body.**

```yaml
---
type: workflow
invokes:
  record-the-run: { workflow: acme/journal, level: require }
  refresh-index:  { workflow: luma/organization-internal-hq#index-repositories, level: recommend, absent: silent }
  need-gh:        { command: "gh", level: require }
  load-security:  { bundle: luma/git-secrets, level: recommend }
before: [record-the-run]
---
```

A marker sits at the point in the body where it should play:

```
luma-invoke: refresh-index
```

**`luma-invoke:` — namespaced, consistent with `.luma/` and the format's own
name.** Bare `invoke:` would probably survive prose, since *invoke* is rare in
ordinary writing where *run* is constant. It is not worth the residual risk: a
marker that can occur by accident is one that eventually will, and this one
changes what an agent does.

**The namespace is a settled position, not a new one.** The same reasoning chose
a vendor-named `.luma/` over a generic directory — the namespace is owned, so
nobody can claim it out from under you — and the format itself is
`luma-knowledge-format`. A prefix here is consistent rather than exceptional.

**The field and the marker share a root** — declare it in `invokes:`, place it
with `luma-invoke:`. Nothing to remember.

### `luma-invoke:` is reserved, and reserving prose is new

The format already reserves names — `document`, `concept`, `workflow`, `policy`,
`bundle`, `type_definition` belong to it and a bundle should not redefine them.
Those are **frontmatter type names**. This would be the **first token the format
reserves inside prose**, which needs two things a type name does not.

**Where it is active.** A line whose first non-whitespace content is
`luma-invoke:`. **Inert inside a fenced code block.**

**What a tool that has not implemented it must do.** The permissive-conformance
law says no consumer rejects a bundle over something it does not understand, so
rejecting is out. **But ignoring is worse**: a `require`-level invocation that
silently does not happen is the failure this whole design exists to prevent. So
the rule is neither — **a tool that meets `luma-invoke:` and cannot act on it says
so.** Unimplemented is not absent, and the difference has to reach the person.
That is the `inform`-versus-`silent` distinction, applied one layer down to the
tool itself.

**Reserving it means nothing else may use the token** — not as a heading, not as a
field, not as prose. That is the cost of a keyword, and the reason it is
namespaced: `luma-invoke:` is unlikely to be wanted for anything else, where a
bare `invoke:` might be.

### Showing the marker without firing it, and the `noop` that makes it work

**Needed: a way to write about `luma-invoke:` in documentation.** Code fences and
inline backticks cover most of it, and a line prefix technically works — but
relying on indentation is fragile, since a formatter reflowing a document can
unindent a line and turn a quoted example into a live directive.

**The mechanism is the one already established: the frontmatter is the
authority.** A marker means something because a slug declares it, so an example
with no declaration is inert on its own. What that leaves is a collision between
two cases that look identical:

| | |
| --- | --- |
| marker with a matching entry | fires |
| marker with a `noop` entry | **silently nothing** — declared, deliberate |
| marker with no entry at all | **error** — that is a typo |

**Without the `noop`, unmatched has to mean one or the other**, and both are bad:
silently ignoring makes a mistyped slug vanish, erroring makes documentation
impossible.

```yaml
invokes:
  show-the-syntax: { noop: "documentation example" }
```

**Silent, and it does not explain itself at run time** — no warning, no note that
something was skipped. The reason string is for whoever reads the file, not for
the output.

**A reserved escape token was the alternative** — `luma-example:` prefixing a
quoted directive. Not taken: it reserves a second keyword, it infers intent from
syntax rather than declaration, and it gives up typo detection, since a quoted
example and a mistyped slug become indistinguishable again.

**This is past where reasoning without an implementation is useful.** Recorded as
something that has to work rather than as a settled mechanism.

### The target set is open, and starts at three

Exactly one target key per entry, **declared rather than inferred** from the shape
of the value; more than one, or none, is a publish-time error.

| target | horizon | |
| --- | --- | --- |
| `workflow:` | **next** | the core case, and the only one needed to prove the mechanism |
| `command:` | **later** | narrow — only when the *absence* behaviour is invisible |
| `bundle:` | **later** | resolves to its `entry_point` |
| `policy:` | **someday** | brings rules into force |
| `concept:` | **deferred** | fails the test three ways, and is not on the ladder — see below |

*Same three words the `idea` type uses, deliberately — a second scale beside an
existing one is a second thing to learn.*

**Ship `workflow:` alone first.** It is the case the whole design was reasoned
from, and it exercises every part of the mechanism — slug, marker, levels,
`absent`, `noop`, prose `when`. The others add target kinds to a thing already
working, which is a smaller change than it looks and a much smaller risk than
building four at once and finding the shape wrong.

### The admission test — all four, not a general impression

A new target kind is admitted only if every one of these holds. They are ordered
so the mechanical checks come first and the judgement call comes last.

**1. Is it opaque from where the caller stands?** Can a reader of the calling
workflow see what they are agreeing to without leaving the page? A fenced command
shows its whole self. A `[[wikilink]]` can be followed and changes nothing. **If
it is visible, it needs no declaration** — that is what keeps commands and plain
documents out.

**2. Does it have one unambiguous starting point?** A workflow starts at the top.
A bundle starts at its `entry_point`. A command is itself. **Something with no
defined place to begin cannot be invoked, only read** — and this is why a bundle
without an `entry_point` is not invocable, which fell out of the test rather than
being decided separately.

**3. Does all four levels mean something on it?** This is the sharpest check
because it is nearly mechanical. `optional` on a concept is nonsense — nobody
pauses to ask permission before reading something. **If a level reads as
gibberish for the kind, the mechanism does not fit it**, and stretching it there
will produce entries nobody knows how to write.

**4. Does absence need an answer?** If *it is not there* is unremarkable, the
levels buy nothing and the entry is ceremony. This is what narrows `command:` to
its escape-hatch role: an ordinary fenced command does not need one, and `gh`
being missing does.

**Applied to the candidates:**

| | opaque | one entry point | four levels fit | absence matters |
| --- | --- | --- | --- | --- |
| `workflow` | yes | yes | yes | yes |
| `command` | only its absence | yes | yes | **only sometimes** — hence narrow |
| `bundle` | yes, and it persists | `entry_point`, or not invocable | yes | yes |
| `policy` | in effect, though readable | probably its own top | plausibly | yes |
| `concept` | **no** | **no** | **no** | no |

**`concept` fails three of four**, which is the point of writing the test down:
adding it would be symmetry for its own sake, and it would teach people that every
reference wants a slug — the ceremony this design exists not to become.

**Deferred rather than rejected, with a trigger.** It is recorded because it has a
defensible-sounding case — *it is a document type too* — that will be raised again
by somebody who has not seen the test. **Re-open if a real case appears that a
`[[wikilink]]` cannot express**: most likely a concept that might not be adopted,
where absence needs an answer, or one costly enough to load that asking first
makes sense. Either would flip two of the four checks, and that is the bar.

**When a candidate passes three and fails one, the answer is no.** A partial pass
is how a mechanism grows into something nobody can explain, one reasonable
exception at a time.

**Conditions are prose in the body, introduced by *when*, beside the marker.**

> Refresh the index first when it is past its `stale_after`. `[[refresh-index]]`

**Because the consumer is an agent reading markdown, not a machine evaluating a
predicate.** A `when:` expression in frontmatter would be structured data, which
needs a vocabulary or an expression language — and that is the failure the tags
decision holds hardest against: *every policy system that collapsed did so by
growing one more operator at a time, each individually reasonable.* Prose has no
parser to grow.

**It also keeps the halves honest.** Frontmatter is machine-facing and answers
*could this run* — which is what pre-flight needs. The body is agent-facing and
answers *should it, here, now*. A condition refines **when**, not **what**, so it
belongs with the marker rather than the manifest.

**A condition must turn on something observable** — a date, a file's presence, a
declared value. *When the index is past its `stale_after`* is checkable and two
agents will agree. *When it seems out of date* is a vibe, and will be judged
differently every run.

### Writing a `when` two agents read the same way

**A loose, extendable contract — not a spec.** Nothing validates these and
nothing should. The point is enough shared shape that two readers reach the same
conclusion; breaking one should feel like writing badly rather than like an
error, and the consequence is a misread rather than a rejection.

**Extendable the way tags are.** These forms are a starting set, not a closed
list. An organization that keeps hitting a shape not covered here adds its own and
records it where its people will find it — the same move as extending a tag
vocabulary or a starter. **What must survive any extension** is the small part
that makes conditions readable at all: they turn on something observable, they
are testable when read, and an unevaluable one runs rather than skipping.

New forms are additive by construction. A reader who knows only the ones below
still reads those correctly, which is what makes extending safe.

```
When <artifact> <is | is not> <state observable right now>.
```

**Name the artifact, not the situation.** *When `repositories/index.md` is past
its `stale_after`* — not *when the index is out of date*. An agent can open a
file; it cannot open a situation.

**Prefer one condition to a compound.** *When A and B* is where prose starts
growing operators, and *and* invites *or*, which invites precedence. Where two
things genuinely gate it, that is often two invocations — or the same marker
placed in a step that only runs under the first.

**Testable at the moment it is read.** Present tense, checkable now. *When the
descriptor is absent* works; *when this will be needed later* is a prediction, and
two agents will predict differently.

**Do not restate the level.** *When it matters* is not a condition, it is the
difference between `require` and `recommend`. A condition says whether the
situation applies; the level says how much it costs to skip.

**If it cannot be evaluated, run it — this one is firm.** An agent that cannot tell whether the index
is stale should refresh it. This is safe precisely because of the standing
consequence below — anything invocable is cheap to invoke redundantly — and the
alternative fails silently: skipping when unsure means the thing quietly does not
happen and nothing says so.

**Most invocations need no condition at all.** Three things absorb the common
cases: a callee that is idempotent no-ops when nothing changed, so *skip if
fresh* never reaches the caller; placement answers *only in this branch*, since
the marker goes in the step where the condition already holds; and `optional`
answers *genuinely uncertain and expensive*, because if the callee cannot cheaply
decide, the caller — which has less information — certainly cannot.

**Standing consequence: a workflow that can be invoked must be cheap to invoke
redundantly.** That is the price of not having machine conditions, and
`index-repositories` already pays it — *it is idempotent or it is worthless*.

**Re-open trigger:** if anything ever *executes* workflows rather than reading
them, conditions have to become machine-evaluable. The bounded version is the
tags pattern — the invoked workflow publishes the conditions it understands,
callers pick from that list, and anything outside it is an error. A closed list
cannot grow an operator at a time.

**A trigger is conditional on presence, never a dependency.** Bundles are
self-contained and depend on nothing — that is what makes promotion a directory
copy. A workflow naming another bundle's workflow must still work standalone with
every invocation absent.

**The caller may demand a pause, and the callee owns destructive consent.** A
caller knows things the callee cannot — *this is about to spend a minute on
network calls the user did not ask for*. But creating a repository or publishing
requires agreement no matter who called it.

## Two questions, closed

**Organization-imposed invocations: not a mechanism.** The worry was that an
organization wants behaviour inside workflows it did not write and cannot edit.
It dissolves into two cases that already have answers. **One workflow needing an
organization-specific change** is a fork into your own catalog — supported,
cheap, and the promotion path back upstream is designed for it. **Every workflow
should journal** is a *runner* concern: whatever executes workflows writes the
record, no workflow declares anything, and nothing needs an attachment point. It
felt like injection only because journaling was being pictured as something a
workflow *does*, when it is something that happens *around* a workflow being done.

**Deferred: extension points, or plugins.** A workflow declaring named interior
places that others may attach to, filled by an organization's catalog. Rejected
for now as overkill — it charges every workflow author a maintenance obligation
in exchange for a case nobody can name concretely. **Re-open when somebody can
name a real instance** of wanting custom behaviour at interior points of several
workflows they did not write, which forking the few that matter does not serve.

**The name: `invokes:` for the field, `luma-invoke:` for the marker.** `trigger` was
unavailable — *re-open trigger* runs through `DECISIONS.md` and is the tightest
term in the vocabulary. `runs:` held it while the targets were workflows and
commands, and lost the moment bundles joined: you do not run a bundle. `uses:`
replaced it and was too vague to carry anything. `needs:` names a dependency
where the design insists on none. `cues` and `checkpoints` were considered
earlier and did not survive.

## Notes

Designed in conversation on 2026-08-21 across several exchanges. **Everything
above is unbuilt and unvalidated** — no workflow declares an invocation, nothing
reads one, and the four levels have met no real case except the one that produced
them.

**`horizon: next`** — set deliberately on 2026-08-21, not defaulted. The first
target kind is `next` and the idea cannot trail its own contents.

**Filed here, after two wrong turns worth recording.** It began in `luma-catalog`
because it looked like bundle machinery — a topic association, not a build site. It
was then moved to `luma-knowledge-format` on the reasoning that `invokes:` is a
field on `workflow` and fields belong with their type. That is true about the
*artifact* and irrelevant to *routing*: **the format supplies a field declaration;
this repository supplies the behaviour**, and the behaviour is the idea. Resolution,
the levels, absence handling, install prompts, the `noop`, prose conditions — all of
it is work that happens here.

**The precedent was already on disk.** `declared-maturity-and-behaviour.md`, filed
here, is the same shape: the format supplies `lifecycle_status`, this repository
supplies what to do about it, and the reason given was *a contract should be dumb
about how things get used*. Checking the ideas already filed would have caught both
wrong turns.

**Nothing here is unresolved any more, but nothing is built either.** The design
settled over one long conversation; no workflow declares an `invokes:` block, nothing
reads one, and the four levels have met no real case except the one that produced
them. **The first workflow to declare an invocation is the test**, and it will
probably find something this could not.

**This is the caller's half only.** [[bundle-routines]] raises the other one —
whether a bundle exposes several named callables rather than the single
`entry_point` the `bundle:` target assumes here.
