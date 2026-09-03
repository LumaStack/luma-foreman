---
type: luma/tutorial_step
title: Do not treat every change as expensive
step: 12
pause: practice
---

# Do not treat every change as expensive

The opposite mistake is becoming afraid to touch anything. Most of what you do in
a session leaves the cache completely alone, and both lists are worth knowing —
guessing produces paralysis in one direction and surprise bills in the other.

| rebuilds your cache | leaves it alone |
| --- | --- |
| switching model | editing files in your repo |
| changing effort level | editing your memory file |
| turning on fast mode | changing output style |
| connecting or disconnecting an MCP server, where tools load up front | changing permission mode |
| enabling a plugin that ships an MCP server | invoking a skill or a command |
| compacting | recaps and rewinds |
| upgrading Claude Code, then resuming a long session | spawning a subagent |

**Upgrading Claude mid-session is the nastiest**, because it does not feel like a
change to the session at all. Anthropic's own documentation describes resuming a
long session after an upgrade as about the most expensive request you will send.

And note where a subagent sits. **Spawning one is cache-safe** — which is a
different question from whether it was worth spawning.

## Takeaways

- **Rebuilds your cache:** switching model, changing effort, fast mode, compacting, toggling MCP servers where tools load up front, enabling a plugin that ships one.
- **Leaves cache alone:** editing files, editing your memory file, output style, permission mode, invoking skills and commands, recaps, rewinds, spawning a subagent.
- **Upgrading then resuming a long session** is the worst offender.
- Spawning a subagent is cache-safe, which is a different question from whether it was worth it.
