---
type: procedure
title: Verify an audit response
description: Check whether each finding is genuinely resolved and record a disposition. Use after a response is filed — this is what closes the loop.
---

# Verify an audit response

## 1. This is the auditor's job, not the respondent's

Whoever wrote the findings verifies the answers, and the respondent must not
write this file. **Marking your own work closed is the failure the whole shape
exists to prevent.**

**The auditor coming back is the design, not a breach of independence.** The
party that raised a finding is the one entitled to say whether the answer
resolved it — that is what makes this follow-up rather than a second opinion, and
it is why the auditor legitimately writes two of the three documents.

**Come back in a fresh session.** You are verifying against the record, and a
session still holding its own reasoning checks its memory rather than the file —
which is how a finding gets closed on what the auditor meant instead of on what
the response actually did. See [[audit-layout]].

*One exception:* a deterministic command may verify findings it produced, because
re-running it is evidence rather than an opinion about its own work — it carries
nothing between runs. **That is the same reason the session boundary exists**,
which is why the exception is narrow and does not extend to agents.

## 2. Check, do not accept

**Do not close a finding because the response says it was fixed.** Look at the
change. Where the response named a commit, read the commit; where it named a
file, read the file.

A finding closed on assurance is worse than one left open — it converts an
unresolved problem into a documented resolution, which is the state nobody
re-examines.

## 3. Record a disposition per finding

| disposition | when |
| --- | --- |
| **closed** | addressed, and you checked |
| **closed — accepted** | not fixed, and the reasoning for carrying it holds |
| **open** | not addressed, or addressed in a way that does not resolve it |
| **withdrawn** | the finding was wrong. You were mistaken, and you say so |

**Withdrawn matters more than it looks.** An audit process whose findings are
never wrong is one nobody trusts, and a record that cannot show the auditor
conceding has a thumb on the scale.

**Accepting an acceptance is a real decision.** *We are carrying this* is
sometimes right and sometimes an unexamined risk. If the reasoning does not hold,
that is `open`, not a disagreement to avoid.

## 4. If anything is open, say what would close it

Specifically enough to act on without a conversation. An open finding with no
stated remedy is an argument rather than a record.

That produces round two — `response.md` round 2, then `verification.md` round 2 —
rather than an edit to either original.

## 5. Write `verification.md` even when everything closed

**An audit that ends with no verification is indistinguishable from an abandoned
one.** A reader a year later cannot tell whether the findings were resolved or
whether everybody simply stopped.

Ending with findings open is a complete audit. Ending with nothing saying so is
not.

[The verification template](../templates/verification.md).
