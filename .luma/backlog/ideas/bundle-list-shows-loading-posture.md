---
type: luma/idea
title: bundle list shows each bundle's loading posture, and standby is renamed on-demand
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5]
---

# bundle list shows each bundle's loading posture, and standby is renamed on-demand

`bundle list` prints name and version but not how each bundle reaches an
agent — eager, offered, or on demand — which is the fact a reader tending
context cost actually wants. Surfacing it makes the posture vocabulary
user-facing, and *standby* does not explain itself there the way *on-demand*
would.
