---
type: luma/idea
title: Routers — conditional decision logic for what gets loaded
created: { by: human:benlinton, at: 2026-08-19T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: someday
scope: project
lifecycle_status: draft
---

# Routers — conditional decision logic for what gets loaded

**Loose, and worth pursuing.** A `router` is a Document whose content is
*decision logic* — not knowledge, but the rules for reaching knowledge. Where to
go next, when to load what, which bundle answers a given question, whose
catalog to consult for more.

## What is actually missing

**`preload` is unconditional.** A Document is `mandatory`, `recommended` or
`optional` always, decided once by its author. There is no way to say
*mandatory when auditing*, *irrelevant unless this is a release*, or *load the
release policy only if somebody is cutting one*.

That is the gap in one sentence, and everything else a router might do is
adjacent to it:

- **Progressive disclosure with conditions.** `preload` and links between them
  give eager and lazy loading. Neither gives *conditional*.
- **Which bundle answers this.** A project with eleven adopted bundles has no
  index from question to bundle. An agent either loads everything or guesses.
- **When to reach outside.** Into another corpus, another catalog, another
  organization's published knowledge. The catalog `upstream` chain does a
  narrow version of this for bundles and nothing does it for knowledge.

## It would earn a type easily

By §10.4's test, this is the strongest dispatch case yet seen: a consumer does
not merely read a router, it **evaluates** one — reads conditions, tests them,
and decides what to load as a result. Nothing else in a Bundle is executed that
way.

Whether it should be *built in* is open and unmeasurable, since none exist. But
unlike bundle migrations, this one has a genuine claim on the format rather than
on the tooling: `preload` is already a core field, so conditional loading is
territory the format has entered rather than declined.

## The central design question

**Is a router prose an agent follows, or data a tool evaluates?**

*Prose* is a workflow with a different name, and it inherits every good property
of one: no syntax to design, no expressiveness ceiling, and an agent can reason
about a condition nobody anticipated. Its cost is that nothing mechanical can
use it — no tool can pre-compute a context budget or verify a router is total.

*Data* is a condition language, and **that is where policy systems die.** The
catalog's tag rules already say so: any-of matching, no booleans, and a
composite condition becomes a named tag somebody has to claim. A router that
grows operators one reasonable step at a time ends up a small programming
language nobody can predict.

The middle worth exploring: **data for the conditions the tag vocabulary can
already express, prose for everything else.** A router row keys on the same tags
a project already declares, and anything beyond that is a paragraph rather than
a new operator.

## Open, and worth settling before building

**Whose router is it?** A bundle routing within itself, a catalog routing to
bundles, and a project routing over what it has adopted are three different
scopes. They plausibly chain — which is itself routing, and a chain that can
loop.

**Does it reintroduce dependencies?** A router that says *for this, use bundle
X* is a bundle reference. That must stay a mention rather than a requirement,
or it becomes resolution wearing a new name. A router pointing at a bundle
nobody adopted should degrade to silence, not to an error.

**What does it overlap?** `preload`, `entry_point`, `tags` and a catalog's
`requires` each do a slice of this today. A router should absorb or defer to
each explicitly rather than quietly duplicating them — two mechanisms answering
one question is how they drift into disagreeing.

**Can it be verified?** A router with a gap routes somebody nowhere, silently.
Whether totality is checkable depends entirely on the prose-or-data answer
above, which is another reason that question comes first.

## Notes

Migrated from `docs/IDEAS.md` on 2026-08-21. `created.at` is a day-level
estimate from git history.

**The central design question has been partly answered elsewhere since this was
written.** `docs/scope.md` lists routing under *needs a decision before it can be
built*, and adds a conditional this entry does not have: *"If `apply` must
evaluate a router to decide what to write, it has to be **data** — a tool cannot
follow prose."* That reframes *prose or data?* as *who evaluates it?*, which is
the more tractable question and probably where a design should start.

**Filed here against the entry's own argument, and the disagreement is recorded
rather than settled.** The entry argues for the knowledge format, since `preload`
is a core field and conditional loading is territory the format has entered. It
is filed with foreman instead because a router's substance is *evaluation*, which
is behaviour, and the routing policy holds that a contract is dumb about how
things get used — an idea about what a consumer should do with a field belongs
with the consumer, even when the field is the format's. **If the answer turns out
to be a `preload_when` on the existing field rather than a new document type, the
format is the right home and this should move.**

**Nothing else anywhere mentions routers** — not `luma-leader/docs/DECISIONS.md`, not
any of the fifteen catalog bundles. This entry and that one line in `scope.md`
are the whole record.

**One adjacent decision not to collide with.** `luma-leader/docs/DECISIONS.md` defers
letting adopters override `preload` per document, because "the author renames a
file in the next version and the override silently stops applying". A different
question — *who* decides preload rather than *when* — but the same field.
