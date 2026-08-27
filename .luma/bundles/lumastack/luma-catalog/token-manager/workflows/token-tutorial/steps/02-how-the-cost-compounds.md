---
type: luma/tutorial_step
title: How the cost actually compounds
step: 2
pause: practice
---

# How the cost actually compounds

The model has no memory. Every time you press enter, the entire conversation
is packed up and sent again from the very beginning.

**So the price of a message is never the message being sent. It is the whole conversation,
paid over and over again.**

Turn #1 costs only one message. Turn #2 includes the cost of the first + the second.
And turn #3 costs one, two and three combined. By #20 you are paying for all twenty turns.
And a 3,000-token file your agent reads on turn #1 costs you 300,000 tokens by turn #100 —
in addition to the compounding costs of every other turn along the way.

For simplicity, always remember that your next message is more expensive than everything
that came before it; no matter how small or simple it is. Turns add together and compound as you go.

Another surprising fact is **what you personally type is a rounding error.** In token
optimization studies, everything the human actually wrote came to about 0.01% of the bill.
The rest was the agent re-reading things it had already been sent before or processing files.

## Takeaways

- Every turn resends the whole conversation from the beginning of this session.
- **Every new message costs everything that came before it.** Message #20 costs twenty messages, not one.
- Continuing a session rapidly accelerates costs — it's parabolic.
- What *you* type is a rounding error — around a hundredth of a percent. The spend is re-reading.
