---
type: luma/tutorial_step
title: Do not chase the wrong culprit
step: 18
pause: apply_here
---

# Do not chase the wrong culprit

A popular claim is that leaving Claude Code open in the background quietly burns
your limits. **It does not.** Background usage is documented at under four cents
a session. It is not your problem, and going after it means the real drain keeps
running while you feel like you did something.

Here is what genuinely consumes while you are not looking.

**Scheduled tasks**, for the reason a few steps back — full context on every
fire, and a guaranteed cache miss every time if the interval is longer than the
cache lives.

**Live agent teams.** Each agent keeps consuming until it exits. An agent left
running is not idle in the way an open terminal is idle.

**The general shape is the thing to keep.** What is expensive is whatever repeats
without you: something that fires on a schedule, something re-read on every turn,
something still running after you stopped paying attention. Not the window you
left open.

## Takeaways

- Leaving Claude Code open in the background is **not** your problem — it's documented at under four cents a session.
- **Scheduled tasks are**: full context every fire, guaranteed cache miss if the interval outruns the cache.
- **Live agent teams are**: each agent keeps consuming until it exits.
- The shape to remember: what's expensive is whatever **repeats without you**, not the window you left open.
