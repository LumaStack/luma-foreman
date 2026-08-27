---
type: luma/tutorial_step
title: Turn off the tools you never use
step: 7
pause: apply_here
---

# Turn off the tools you never use

Connecting an MCP server takes one prompt and feels free. It is not. **Every tool
arrives with an instruction manual** — what it does, what to send it, what comes
back — and your agent has to read the manual before it is allowed to touch the
tool. A single large server can run to tens of thousands of tokens on its own,
and it loads before you have typed a word.

Newer harness versions fix most of this with tool deferral: the agent loads a contents
page and opens a section only when it actually needs that tool. Same tools
available, a fraction of the weight. It is on by default.

**But you still pay for the contents page, and it grows every time you connect
something new.** So run `/mcp`, look at the list of everything you have ever
connected, and switch off anything you have not used in about a month. Nothing is
deleted — it stays configured and stops loading.

Then run `/context` and find the tools line. **If it says deferred, you are on
the new behaviour**, and toggling servers mid-session is safe: connecting and
disconnecting appends rather than rebuilding your cache. The audit at the end of
this tutorial checks that line for you, along with the thing that silently
switches deferral off — a proxy or gateway in front of the API, which nothing
warns you about.

## Takeaways

- Every connected tool loads an instruction manual before you type a word.
- **Tool deferral** cuts most of this and is on by default — the agent opens a section only when it needs it.
- The contents page still costs, and grows with every server you add.
- Run **`/mcp`** and switch off anything unused for a month. It stays configured.
- Check **`/context`** says *deferred* — if so, toggling servers mid-session is free.
