---
type: luma/idea
title: Building knowledge delivery
description: The sequence for building what how-knowledge-arrives describes — six steps, each shippable on its own, and the decisions each one will force.
lifecycle: draft
created: { by: human:benlinton, at: 2026-08-27T00:00:00Z }
modified: { by: agent:claude-opus-5, at: 2026-08-27T00:00:00Z }
---

# Building knowledge delivery

**The target is `luma-leader`'s `docs/how-knowledge-arrives.md`** — three
transports, rings fired by entrypoints, `matches` as the only declaration. This
is the order to build it in.

**Every step ships on its own and is reversible.** No step needs the next one to
be worth having, which is deliberate: the design was argued at length before
anything existed, and the fastest correction now comes from seeing it run.

## 1. The project ring becomes its own file

`apply` writes the project ring to `.luma/bundles/entry-point.md`. The managed
block in `CLAUDE.md` shrinks to an adapter that points at it.

**The adapter's one obligation applies immediately:** it must not render what the
harness already carries. Claude Code loads every skill's name and description at
startup, so the 40 workflow lines come out — 8,451 of 21,646 characters, paid
twice today.

Measurable the moment it lands, and it needs nothing else decided.

## 2. `always` becomes scoped to its ring

Today every document declaring `matches: always`, in any bundle, is imported into
`CLAUDE.md` and sits in every session. Under the target only the *project* ring's
`always` gets that seat.

**This forces a question the design does not answer: what is project-ring
`always`?** Every document lives in a bundle, so every `always` declaration is
bundle-scoped by construction. Three candidate answers — the project ring is
map-only and has no bodies of its own; a project may declare its own; or a bundle
may mark something as project-level.

**No document declares `always` today**, so the first honest answer is map-only,
and the question gets decided when something real needs the other behaviour.

## 3. Bundles get a ring of their own

A generated map per bundle: each document, what it is for, what fires it — plus
the bodies of anything that bundle declares `always`, which arrive when the ring
is fired rather than at session start.

This is where the saving actually is. It is also where `entry_point` stops being
a single pointer and becomes the thing that fires a ring.

## The platform fact 4 turns on, now checked

**`additionalContext` injects text into the model's context, and `PreToolUse`
supports it.** From the decision-control table in `hooks.md`:

| event | `additionalContext` | what it gives us |
| --- | --- | --- |
| `SessionStart` | **yes** | `1-project` without going through a harness file |
| `UserPromptSubmit` | **yes** | sees the prompt, so **`topic:` becomes deliverable** |
| `PreToolUse` | **yes** | `path:` / `command:` arrive **before** the tool runs |
| `PostToolUse` | yes | too late to govern the action it followed |

**Three things I had recorded as constraints are wrong.**

**`topic:` is not model-only.** Twenty of the twenty-nine routing rules declare a
`topic:`, and this plan called them a model judgement nothing could enforce. A
`UserPromptSubmit` hook sees the prompt text, so a topic can be matched and its
document delivered — the same route as any other trigger. **That is two-thirds of
the routing surface moving from advisory to deliverable.**

**Delivery is in time, not after the fact.** `PreToolUse` fires before the tool
runs, so a `path:` rule arrives before the edit it governs rather than after.
`how-knowledge-arrives` calling firing *the only guaranteed path* stands.

**`1-project` need not arrive through `CLAUDE.md` at all.** `SessionStart`
carries it, which is a second adapter for a harness that has one — and the
strongest evidence yet that ring and adapter were right to split.

**How this was checked, because the method mattered.** The published page at
`/docs/en/hooks` is truncated before the table, and the reference URL 404s. Two
fetches of the truncated page gave **opposite** answers about `PreToolUse`, and
the one that answered confidently had invented a row it could not have read.
`hooks.md` — the raw markdown behind the same page — serves the table whole.
**Ask for the source rather than the rendering.**

## 4. Firing a bundle ring

**`/list-bundles` and `/load-bundle` first**, because they are the floor: they
work when nothing notices, and neither costs more than one skill however many
bundles exist.

Automatic firing comes after, and the choice between a skill per bundle, a hook,
and prose the model follows should be made against a working step 3 rather than
in advance.

## 5. The reachability check

`inspect` reports anything no transport can reach — no trigger, on no ring's map,
and no inbound link from something reachable. A warning, not an error: a tool
cannot tell an orphan from something reached by a path it cannot model.

**The integrity rule is worthless unannounced**, so this is what makes the
target's central promise real rather than aspirational.

## 6. Deletions

`starters` comes out of `_types/catalog.md` and out of the live `CATALOG.md`, and
returns as an idea if it earns the place.

Then the sweep: the target strands mechanisms that exist only to express parts of
what rings now express. **Deleting them is the point, not the tidying-up
afterwards** — a half-migrated vocabulary is what produced the pile this replaces.

## Notes

**Steps 2 and 3 are the real behaviour change**; 1 is preparation and 4 makes 3
reachable. 5 and 6 can happen at any point after 3.

**What this plan does not do is decide names.** `entry-point.md` is what step 1
writes because something has to be typed; it is expected to change once there is
something to look at.
