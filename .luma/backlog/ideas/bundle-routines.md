---
type: luma/idea
title: A bundle exposes named routines, not a single entry point
created: { by: human:benlinton, at: 2026-08-23T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
---

# A bundle exposes named routines, not a single entry point

## The idea, as raised

**A bundle that loads another bundle should be able to call a routine.** That way
bundles are self-contained as much as possible, but they can communicate with
each other — and **this way there is not one single preload path for all.**

**The entry point needs rules about how it works.** Either:

- there is a **folder of entry points** and you reference them — they are the
  routines — but this seems wasteful maybe; or
- there is a **set of callables or routines** that you can call, and **if a
  called routine is missing, then we warn and say the framework is broken.
  Loudly.** Like code that called other code via a plugin or whatever and didn't
  work.

---

## Commentary — `agent:claude-opus-5`, not part of the idea

*Below the idea and separate from it. Evaluation is welcome here — it just does
not get to edit what was raised.*

### This is the half that was never designed

[[workflows-invoking-workflows]] designed the **caller**: an `invokes:` block, a
`luma-invoke:` marker, four levels, absence handling. Its `bundle:` target
resolves to the bundle's `entry_point` — **one way in, decided by the callee's
author, the same one for every caller.**

Nothing has ever described the **callee's** side. This does: a bundle has a
*surface*, and the surface has more than one door.

### "Not one single preload path" is the strongest line in it

Loading today is a property of documents, decided once. A bundle's cost is the
sum of its `preload: mandatory` documents, and every consumer pays the same
total no matter why they came.

**A routine is a named loading path.** Calling `decision-records#record` pulls
what recording needs; calling `#find` pulls what finding needs. That is
conditional loading **without a condition language** — the caller *names* the
path instead of a predicate evaluating into one. [[routers]] gets stuck on
*prose or data?* precisely because something has to decide; this sidesteps it by
letting the caller, who already knows, say so.

It is also the same move as [[an-index-of-what-exists]]: that policy makes
*existence* cheap, and says to try an index before reaching for a `when`. A
routine list is an index of callables. **Third rediscovery of the same shape.**

### The two shapes offered are the same thing, and there is a third

| | cost | what it buys |
| --- | --- | --- |
| **a folder of entry-point documents** | a file per routine, most of them a line pointing elsewhere | each routine is a real Document — it has a `description`, it is linkable, no new field needed |
| **a declared set in `bundle.md`** | one new manifest field | one place to look, and the manifest becomes the interface |
| **no field at all** — any workflow is callable as `bundle#workflow-id` | nothing | works today, and the existing idea already quietly assumed it |

*Wasteful* is the right instinct about the folder. A routine that is one line of
indirection is a file that exists to be a symlink.

**But the third option is the one that has to be argued against, and it can
be.** If every workflow is callable, then **renaming any workflow is a breaking
change**, because some other bundle may be calling it. A declared set draws the
line between *public* and *internal*: the routines are promised, everything else
is free to move. That is a real argument, and it is a **versioning** argument
rather than an aesthetic one — which makes it the kind that survives.

### Keep it separate from `entry_point` rather than extending it

`entry_point` answers *where does a reader start*. A routine answers *what can a
caller invoke*. **Those are two questions, and one field answering both is the
mistake already made once and fixed** — `preload` and `type` were overlapping
until they were split onto the engagement axis, at which point both got simpler.

So: `entry_point` stays the reading entrance; `routines:` is the calling
surface; a bundle may have either, both, or neither. A bundle of pure knowledge
has an entry point and no routines, and that should read as normal rather than
as incomplete.

### The loud failure is right, and it needs one distinction to stay legal

It sits against two settled positions:

- **§4 permissive conformance** — a consumer MUST NOT reject a file for
  unresolved links or things it does not understand.
- **[[workflows-invoking-workflows]]** — *"a trigger is conditional on presence,
  never a dependency… a workflow naming another bundle's workflow must still
  work standalone with every invocation absent."*

**The distinction that resolves it:**

| | |
| --- | --- |
| the bundle is **not adopted** | **silence** — degrade, carry on. This is the never-a-dependency rule and it holds |
| the bundle **is adopted** and the routine it promised is **missing** | **loud** — a promise was published and is not kept |

That is not a new principle. It is the existing rule that *unimplemented is not
absent* — written there about tools meeting a `luma-invoke:` they cannot act
on — applied one layer over.

### The best version of "loudly" is at adopt time, not run time

Everything is vendored. When both bundles sit in `.luma/bundles/`, **every
declared call can be checked against every declared routine without running
anything.** `foreman inspect` compares the two lists and reports the gap.

That is strictly better than the plugin analogy the idea reaches for: a plugin
system finds out at call time, in front of a user, in whatever half-done state
the work is in. This one finds out at adoption, which is the moment somebody is
already deciding whether to take the bundle.

### One thing to be precise about before it drifts

**"Communicate with each other" buys calling, not exchange.** A caller invokes a
routine; nothing comes back. No return value, no shared state, no protocol.

Worth saying out loud because *communicate* is the word that invites all three,
and a routine that returns something is a substantially larger design — it makes
bundles into modules, and the loose coupling that lets a bundle be a directory
copy is the first thing it would cost.

### This stops being *someday* the moment `apply` is built

`apply` writes an adopted bundle's workflows into harness adapters — a Claude
Code skill per *what?*

**That question is this idea.** Per workflow means the internal surface is the
public one and every rename breaks a caller. Per declared routine means this
gets designed first. **`apply` cannot be built without answering it**, which is
why the horizon is `next` rather than `someday` — and why the answer will
probably come from building rather than from more reasoning.

**Built the same day, and it took the third option.** `apply` writes *every*
`type: workflow` document as a skill, so a bundle's public surface is currently
whatever workflows it happens to contain. It works, and it makes the cost
concrete rather than hypothetical: **renaming any workflow in any bundle is now
a breaking change for anything that invoked it by name**, and nothing anywhere
records that a name was ever promised.

It also hit the collision case immediately in the design, before it happened in
practice — two bundles may both publish `audit-bundle`, and a silent first-seen
win would leave one permanently unreachable. `apply` prefixes both sides and
says so. **A declared routine list would have made that a publish-time error
instead of a runtime rename**, which is the clearest single argument for it.

### Related

[[workflows-invoking-workflows]] — the caller's half; this is the callee's.
[[routers]] — the same problem approached as evaluation rather than as naming.
[[conditional-preload]] — in `luma-leader`; a routine may be the cheap version
of it.

---

## Entry point variants, raised 2026-08-25 — captured, not chosen

**Dropped for now and deliberately kept.** Raised while asking whether
`entry_point` is a good design at all. None of these is decided and some may be
bad; they are here because forgetting them is the only outcome that is certainly
wrong.

### The reading that started it

**Entry point in the Docker sense: the thing that kicks off.** Not *where a
reader starts* — **what runs**. `ENTRYPOINT` is a process, not a signpost, and a
bundle's could be **the router of the bundle**: engage the bundle, and one thing
in it decides where you go next.

That is a third meaning, distinct from both the field we have and from routines.

### The variants, as raised

- **`entry_point` in `BUNDLE.md`** — the field as it exists, possibly given the
  running sense rather than the reading one.
- **`ENTRYPOINT.md`** — a reserved file at the bundle root. **Presence is the
  declaration**: no field to set, no default to remember, and a bundle without
  one behaves exactly as today. Convention over configuration.
- **Rename `routines` to `entrypoints`** — one word for the callable surface
  instead of two concepts that keep being confused for each other.
- **`ENTRYPOINT` as the *default* routine** — the one called when a caller names
  the bundle and nothing else. Routines stay plural; one of them is reachable
  without being named.

Spelling, if a file wins: **`ENTRYPOINT.md`** over `ENTRY_POINT.md`, because
every other reserved name is a single token — `BUNDLE`, `CATALOG`, `LOG`,
`PROJECT`, `WORKFLOW` — and Docker spells it as one word.

### Settled 2026-08-25: routines are frontmatter

**Agreed.** The callable surface lives in `BUNDLE.md`'s frontmatter, beside
`compliance` and `applies_to` and everything else the tools consume:

```yaml
routines:
  - name: record
    description: Write a decision record where this project keeps them.
    pulls: [policy/decision-guidelines, workflows/record-decision]
```

Six routines is about twenty lines. Not light, but **a contract is data**, and
the loud failure this idea insists on — *that name does not exist* — needs a
machine, which needs the surface machine-readable.

**So `ENTRYPOINT.md` is not needed.** The case for a file rested on prose needing
room to breathe; once each routine carries a `description` and its depth lives in
the documents it `pulls`, there is nothing left for the file to hold. The
variants above stay recorded in case that stops being true.

### And the rest, concluded but not settled

**`entry_point` as it stands probably does not survive**, and not because
routines replace it. **`BUNDLE.md` is already the reading entrance** — you open a
bundle, you read its manifest, and the manifest tells you where to go. A field
naming one document is a second answer to a question the manifest already
answers, and it is checked by two tools and consumed by none.

**The test that produced that answer** is worth keeping with the idea, since it
decides the rest of it: *data is what something checks; prose is what a person
or agent needs to understand — and an agent should prefer the mechanical answer
to the question the data answers.* By that test the callable surface is data. By
the same test, the *why* of each routine stays prose, in the documents it names.

### The thing to check before choosing

**Write out four real routines and see whether they fit.**
`decision-records` — `#record`, `#find`, `#migrate`, `#prune` — is the obvious
candidate. If they fit in twenty lines of frontmatter without straining, the
manifest wins and no reserved name is needed. If a routine turns out to want
conditions, ordering or arguments, it has outgrown a manifest entry and the file
comes back.

