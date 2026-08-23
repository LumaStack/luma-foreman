---
type: luma/idea
title: Named permission profiles, applied in one command
created: { by: human:benlinton, at: 2026-08-17T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
lifecycle_status: draft
---

# Named permission profiles, applied in one command

I want to be able to setup a mode in the config or via the command line or both.

It will make it so when I say I want to be in "foobar" mode it auto applies all
my permissions to the way I set them. The simpliest way is the setting sits as a
mapping in the config. The nice to have would be taking a snapshot of my current
settings, name it, and then the current settings get added to config as a new
mapping set.

**Clarified by the author during migration**, and this is the clearer statement
of the want:

> i want to run 1 alias or subcommand to change all my permission sets to a fixed
> state that i predefine, and i can create multiple aliases. so i can ratchet up
> or down trust or define presets that are tailored to a given workflow or use
> case

## The problem it addresses

`agent-permissions` sets keys one at a time. There is no way to move every key to
a predefined state in one step, and no way to name such a state.

## Notes

Migrated from `docs/IDEAS.md` on 2026-08-21, verbatim including its typo.
`created.at` is a day-level estimate from git history.

**Retitled at migration, because `mode` is already taken twice in this tool.**
The original entry calls this a mode, and that word carries two other meanings
here:

- **Foreman's own `mode`**, a settled decision in `luma-leader/docs/DECISIONS.md` —
  `luma mode set strict` versus `luma --mode strict`, kept deliberately distinct
  — governing *"how much foreman says, how much it runs, and whether it blocks
  locally"*, with the standing consequence that **mode must never change pass or
  fail**.
- **Claude Code's `permission_mode`** — `default`, `bypassPermissions` — which
  the gate reads on every call.

A third meaning on the same command surface is the objection `DECISIONS.md`
already raised against `bundles.toml` sitting one letter from `bundle.md`:
near-identical names for unrelated jobs read fine to whoever wrote them and
confuse everyone else. *Profile* or *preset* says the same thing and collides
with nothing. The wording above is left as written.

**"Ratchet up or down trust" lands on existing vocabulary.** The gate already
carries a `trust` key with `full` as a value, so a profile that moves trust is
adjusting something the tool names rather than introducing a new axis. Whether
profiles are strictly ordered — a ratchet implies a line from loose to strict —
or are unordered presets per workflow is left open; the clarification names both,
and they are not obviously the same shape.

**Half the mechanism is already designed.** `luma-leader/docs/DECISIONS.md` lays out a
six-layer precedence chain for foreman configuration and directs that only layer
4 be built for now, *"behind one resolution function so the rest slot in at a
single site"*. A named profile is a value source that would slot into that chain
rather than needing machinery of its own.

**Not split, though there is a seam.** The config mapping and the snapshot-and-
name convenience are two steps, and the entry marks the second as a nice-to-have.
They are kept together because the snapshot half has no value without the
profiles half.

**Third of three ideas from the `agent-permissions` family**, with
[[committed-permission-floor]] and
[[distribution-beyond-clone-and-symlink]].
