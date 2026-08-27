---
type: luma/tutorial_step
title: Measure your own setup
step: 20
pause: apply_elsewhere
---

# Measure your own setup

Everything up to here has been general, and general fixes rank differently on
different machines. Someone with a dozen MCP servers connected has a different
top problem from someone with a bloated memory file, and both have a different
one from someone with a scheduled task firing every three hours.

This bundle carries an audit workflow for exactly that. It reads your memory
files and reports their size, checks whether tool deferral is genuinely on, lists
your MCP servers, finds scheduled tasks whose interval is longer than your cache
lifetime, and parses a real session log to work out how much of it was re-reading
history rather than doing new work.

**It changes nothing.** It reports, sorted by cost, and finishes with the single
highest-leverage change available to you.

**Run it in a second window, not this one.** It produces a substantial report,
and you want that somewhere you will still be working tomorrow rather than in a
tutorial session.

**Then run it again every few weeks.** Setups drift in one direction only: you
add a server, install a plugin, change a setting, and six weeks later you are
back to wondering why you keep hitting limits. Nothing announces that it has
happened.

## Takeaways

- Run the audit **now that the findings mean something** — it ranks your problems, not everybody's.
- It reads memory files, MCP servers, deferral status, schedule intervals and cache hit rate.
- **It changes nothing.** It reports, sorted by cost, and names your single highest-leverage fix.
- **Run it in a second window** — you want the report where you work, not in a tutorial session.
- Re-run it every few weeks. Setups only ever drift one way.
