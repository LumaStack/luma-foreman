---
type: luma/idea
title: agent-permissions returns 1 where every other command returns 2
created: { by: agent:claude-opus-5, at: 2026-09-06T00:00:00Z }
contributors: [agent:claude-opus-5, human:benlinton]
horizon: next
scope: project
stage: draft
---

# `agent-permissions` returns 1 where every other command returns 2

**ADR-0013 splits *the tool declined* from *the tool could not try*, and
`agent-permissions` does not make that split.** Its `_err` returns 1 for a usage
error — an unknown verb, a missing argument — where `get`, `bundle`, `catalog`,
`publish` and `remove` all return 2.

`src/foreman/agent_permissions/commands.py`:

```python
def _err(message: str) -> int:
    print(f"{CMD}: {message}", file=sys.stderr)
    return 1
```

Every other command's `_err` returns 2 and has a separate `_refuse` returning 1.
This one has no `_refuse` and no third code at all.

## Why it matters more here than it would elsewhere

**A refusal is an answer and a broken invocation is not**, which is the whole
reason ADR-0013 pays for a third code. Conflating them means a caller cannot
tell *this permission is denied* from *you typed the command wrong* — and this
is the command whose entire job is denying things.

It also means the one command a script is most likely to wrap is the one whose
exit codes say least.

## What makes it awkward

**Changing an exit code can break a caller.** Nothing in this repository reads
these codes, but the gate is installed on machines and somebody's shell function
may. The change is right and is not free, which is why it was left alone rather
than made quietly during a cosmetic pass over the help text.

**Its help now states what it does rather than what the record says**: `0 fine
1 refused, or something is wrong`. That is honest and it is not the target — the
`EXIT CODES` section is written to be corrected when this is.

## What deciding it needs

Whether ADR-0013's three codes are meant to reach a command that predates the
record, or whether the record should say some commands use two. **Two codes is
what CLIG's letter asks for**, and ADR-0013 lists it as the deferred
alternative — so *make everything else match this one* is a real option and not
obviously the wrong one.

## Notes

Found while restyling the help after `gh`, where writing an `EXIT CODES` section
meant reading what the codes actually were.
