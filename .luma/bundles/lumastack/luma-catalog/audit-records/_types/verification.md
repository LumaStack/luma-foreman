---
type: type_definition
defines: verification
fields:
  verifies:
    field_presence: required
    field_type: text
    desc: "the audit whose response this checks — its directory name"
  verified:
    field_presence: required
    field_type: date
    desc: "when the check was performed"
  verifier:
    field_presence: recommended
    field_type: actor
    desc: "who or what checked (§7.4)"
  round:
    field_presence: optional
    field_type: number
    desc: "matches the response round it checks"
---

# Verification

The auditor's answer to the response: for each finding, whether it is now closed.
This is what makes the record a loop rather than two documents that never meet.

**Written by the auditor, not the respondent.** Marking your own work closed is
the failure this whole shape exists to prevent, and it is also the easiest one
to commit by accident when one agent is doing both jobs.

## A disposition per finding

| disposition | means |
| --- | --- |
| **closed** | the response addressed it, and that was checked rather than assumed |
| **closed — accepted** | the respondent declined to fix it, and the auditor accepts the reasoning |
| **open** | not addressed, or addressed in a way that does not resolve the finding. Say which |
| **withdrawn** | the finding was wrong. The auditor was mistaken and says so |

**Withdrawn matters more than it looks.** An audit process where findings are
never wrong is one nobody trusts, and a record that cannot show the auditor
conceding is a record with a thumb on the scale.

## Closed means checked

**Do not close a finding on the strength of the response saying it was fixed.**
Look at the change. A finding closed because somebody said so is worse than one
left open, since it converts an unresolved problem into a documented resolution.

Where the response pointed at a commit, read the commit.

## Open reopens, it does not accuse

A finding left open produces a second round — `round: 2` on both sides — rather
than an argument. Say what would close it, specifically enough that the
respondent can act without a conversation.

An audit that ends with findings open is a complete audit. **An audit that ends
with findings open and no verification saying so is an abandoned one**, and the
two are indistinguishable to anybody reading later.
