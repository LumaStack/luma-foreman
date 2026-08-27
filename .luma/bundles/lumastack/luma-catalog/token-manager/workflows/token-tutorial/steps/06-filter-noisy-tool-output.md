---
type: luma/tutorial_step
title: Put a filter in front of noisy commands
step: 6
pause: apply_elsewhere
---

# Put a filter in front of noisy commands

You ask for a package to be installed. The command runs and eight hundred lines
come back — package names, version numbers, warnings, a funding notice. You did
not read any of them. You wanted to know the command worked.

**Your agent does not get to skim.** All eight hundred lines land in the
conversation verbatim, and you pay for them again on every message until you
clear.

The fix is a small script sitting between the agent and the command, trimming the
output before the agent ever sees it — a `PreToolUse` hook that rewrites a noisy
command into a quieter one.

**You do not have to write it.** Ask your agent to. Anthropic ships a working
example it can copy from, and the claim on that example is reducing context from
tens of thousands of tokens to hundreds.

**This is a build-once fix**, which makes it unusually good value. Your agent
writes it, your agent installs it, and it keeps working in every session
afterwards without you thinking about it again.

## Takeaways

- Long command output lands in your context verbatim and is resent on every message until you clear.
- Your agent doesn't get to skim the 800 lines you ignored.
- Fix it with a **`PreToolUse` hook** that rewrites noisy commands into quiet ones.
- **Ask your agent to write it** — Anthropic ships an example to copy.
- Build once, works in every session after.
