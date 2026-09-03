---
type: luma/tutorial_step
title: Do not assume subagents save tokens
step: 17
pause: practice
---

# Do not assume subagents save tokens

The advice everybody repeats is that delegating to subagents saves tokens.
**It does not save them. It moves them.**

Run the arithmetic on a typical delegation. The subagent reads several thousand
tokens of files and hands back a summary a fraction of that size, and your
context is clearly better off. But before it read anything it loaded its own
system prompt, its own copy of your memory file and its own tool definitions —
and end to end it can spend more than it saved.

The published figures are blunt about the scale. **Agents use in the region of
four times the tokens of ordinary chat, and multi-agent systems around fifteen
times.**

None of that makes delegation wrong. It makes it a trade rather than a saving,
and the earlier step gave the conditions under which the trade pays.

**What is wrong is delegating on the belief that it is free** — and above all,
delegating and then ending the session, which is paying the whole setup cost and
collecting none of the return.

## Takeaways

- Subagents **move** tokens, they don't save them.
- A subagent loads its own system prompt, memory file and tools before it reads a line.
- Published figures: agents use around **4×** the tokens of ordinary chat, multi-agent systems around **15×**.
- That makes delegation a trade, not a saving — worth it under the conditions from earlier.
- The mistake is believing it's free, and especially delegating then ending the session.
