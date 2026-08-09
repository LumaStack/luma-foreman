---
name: design-first-working-mode
description: The maintainer works spec-first — nail the design docs before any implementation, and expects sessions scoped to one or the other
metadata:
  type: feedback
---

Projects run design-first: the specification is developed and settled in markdown docs before implementation starts. A session may be explicitly scoped to design-only ("I do not want to write any code for this session"), and that scope is expected to hold for the whole session, not just the first reply.

**Why:** This mirrors how the sibling repository `luma-knowledge-format` is run — a docs-only specification repository (SPEC / PRINCIPLES / ROADMAP / GUIDELINES / CHANGELOG) whose GUIDELINES.md encodes the rule that agents draft and a human ratifies. The same trust model applies to working sessions: get the thinking right on paper, under human sign-off, before code exists to argue with.

**How to apply:** When a session is scoped to design, produce and iterate on markdown docs — do not scaffold projects, write source files, or reach for code as a way of "showing" a design. Prefer discussion plus doc edits. Also prefer few, well-argued recommendations over exhaustive option surveys; a formal multi-question prompt was pushed back on in favor of open discussion.
