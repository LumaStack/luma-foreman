---
type: luma/idea
title: The gate test asserts on a path that has never held a gate
created: { by: human:benlinton, at: 2026-08-29T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle: draft
---

# The gate test asserts on a path that has never held a gate

`tests/permission-gate-test.sh:265-267` is the block that proves an agent
cannot rewrite the permission gate. Its own comment:

> *"The gate script lives in the policy directory so the same protection covers
> it. A gate an agent can rewrite is not a gate."*

**The gate does not live in the policy directory.** `install.py:76` —
`gate_path()` returns `store.data_home() / "permission-gate.sh"`, and its
docstring says *"program data, not configuration."* Nothing calls
`config_home()` at all.

So the test writes to `~/.config/luma/foreman/permission-gate.sh` — **the wrong
tier, and the application name truncated on top of it.** A path where no gate
has ever existed.

## Why it passes anyway

`match.py:53` matches `config/luma/` at the organization level, so **anything**
under that directory is caught, including a path that means nothing. The
assertion succeeds without ever touching what it claims to protect.

## The protection itself looks intact

The real gate is under `~/.local/share/luma/luma-foreman/`, which is covered by
`install.py:214`'s `Edit(~/.local/share/luma/**)` deny and by `share/luma/` in
`match.py:53`. **This is a testing defect, not an open door** — but the test
would keep passing if that coverage were removed tomorrow, which is the whole
job it was written to do.

## What to do

- **Assert on `gate_path()` rather than on a literal**, so the test cannot
  drift from the code again. A literal path in a test is a second record of
  where something lives.
- **Fix the comment**, which states the wrong tier and is what made the error
  look deliberate.
- **`:11`, `:22` and `:260`** carry the same truncated `~/.config/luma/foreman`.
  `:11` and `:22` are isolation claims — they promise the real directory is
  never touched, and name a directory that does not exist.

## The shape worth noticing

**`docs/scope.md` warned about exactly this**, at the lines that became
`docs/architecture.md`'s *"a regex that stops matching a command name fails
open"*. The warning was about `match.py`'s patterns drifting from the command
name. **The same drift happened one layer out, in the test that guards them**,
and the document naming the hazard did not prevent it.

## Notes

Found in slice 003 of the sweep, cross-checking `docs/standards.md` against the
code before dropping it. **Nothing reported it**: the test passes, `inspect` has
no rule for it, and the truncated path is created on demand by whatever writes
there first.
