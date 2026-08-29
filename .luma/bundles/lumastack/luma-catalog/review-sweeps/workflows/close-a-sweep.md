---
type: workflow
title: Close a sweep
description: Finish or abandon a sweep honestly — check coverage, confirm nothing worth keeping is still trapped in the notes, then archive it. Use when the last unit is done, or when it is being stopped early.
---

# Close a sweep

**Both endings use this**, and the difference is one honest sentence in the
summary. A sweep stopped at 40% is an ordinary outcome; a sweep stopped at 40%
and archived as though it were finished is a lie the index will tell for years.

## 1. Check `coverage.md`

Every row in `coverage.md` is `approved`, `reviewed`, `skipped` with a reason,
or `pending`.

**Pending rows at closing time are the point of this step.** Do not mark them
anything. They stay pending, and the summary says how many there are — that is
what makes the record honest and what lets somebody resume it later.

**A `skipped` row needs a reason** the way an exclusion does. *Generated*,
*vendored*, *reviewed last month under X* — anything except a blank, which
reads as an oversight forever.

## 2. Confirm nothing worth keeping is still in the notes

**Harvest `journal.md` first if there is one** — it is the file this step
exists for, and the reason the sweep can be thrown away at all. **Every entry
becomes a backlog item, a learning in `sweep.md`, or a deliberate drop.**
Nothing in a journal was ever meant to survive it.

**A journal that was never harvested is a sweep that cannot safely be
archived.**

**This is the step that gets skipped, and it is the one that loses things.**
Read the slices for anything phrased as *we should*, *worth revisiting*, or
*not sure about this yet*, and route each one now — an idea, a finding, a
decision, or a deliberate decision to drop it.

The sweep is about to be archived. **Anything still inside it is being thrown
away**, and doing that on purpose is fine while doing it by omission is not.

## 3. Write the closing summary

In `sweep.md`, under the index. Short, and answering what somebody would ask a
year later:

- **coverage** — approved, reviewed, skipped, pending, out of the total.
  **Report approved and reviewed separately, and report coverage by actor**: a
  row an agent was satisfied with and one a person signed off are different
  claims, and merging them overstates the weaker. **A sweep declared
  `human-agent` whose rows are all `agent:` quietly became something else** —
  say so
- **what it produced** — pull requests landed, ideas filed, decisions recorded,
  findings raised. Counts and where they went, not a restatement
- **what it changed about how you see the system** — the part worth writing.
  A sweep that taught you nothing about the shape of your own project was
  probably a skim
- **drift against what was predicted** — how many files were re-covered, versus
  the expectation recorded at the start. Both directions are worth a line: a
  sweep that predicted heavy churn and saw none learned something about the
  estimate, and one that was overrun learned something about the scope
- **why it stopped**, when it stopped early. *Ran out of appetite* is a real
  reason and a useful one to have written down

## 4. Archive it

```sh
git mv .luma/backlog/sweeps/<slug> .luma/backlog/sweeps/archived/<slug>
```

Set `lifecycle_status: archived` and the `archived` date in `sweep.md`.

**The slices go with it.** They are working notes whose value decays, and their
content has already been routed out — what remains is the trail, and git keeps
that whether or not the directory survives.

## 5. Deleting comes later, and separately

**Archiving needs nobody's permission. Deleting does**, and an agent never
deletes a sweep it did not run.

There is no retention period here, deliberately. Nobody has run enough sweeps
to know what one is, and a number invented now would be enforced for years on
no evidence.
