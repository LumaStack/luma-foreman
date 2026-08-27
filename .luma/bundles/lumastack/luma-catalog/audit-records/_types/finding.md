---
type: type_definition
defines: finding
fields:
  finding_id:
    field_presence: required
    field_type: text
    desc: "stable within its audit — F-001, F-002. What a response and a verification refer to"
  severity:
    field_presence: required
    field_type: enum
    values: [high, medium, low]
    desc: "how much it matters if left alone"
  location:
    field_presence: recommended
    field_type: text
    desc: "file, line, or the part of the system it concerns"
---

# Finding

One issue, in one Document. Written once and never edited — what happens next is
written by somebody else, elsewhere.

## One file per finding, and it is not a preference

**A swarm of auditors writing into one file is one merge conflict per auditor**,
which serialises the exact thing parallelism was for. Separate Documents also
make a finding individually addressable, individually closeable, and individually
citable long after the audit is closed.

`finding_id` is stable within its audit and is the handle everything else uses.

## The five parts

Borrowed from established audit practice, and they hold for code as well as for
process. A finding missing any of them is one somebody has to reconstruct.

| part | the question |
| --- | --- |
| **condition** | what *is* — observed, specific, checkable |
| **criteria** | what *should be*, and by whose rule |
| **cause** | why it is that way. Often the most useful part |
| **effect** | what it costs if nothing changes |
| **recommendation** | what would resolve it |

**Criteria is what separates a finding from an opinion.** *"This function is too
long"* is a preference. *"This function is 400 lines against the project's stated
limit of 50"* is a finding, and it can be disagreed with on the merits rather
than on taste.

**Cause is where the value is.** Five findings sharing one cause are one problem;
fixing the cause closes all five, and fixing five conditions closes none of them.

## Severity is about consequence, not effort

`high` is not *hard to fix*. It is **what it costs if nobody ever fixes it** —
data lost, a credential published, a rule silently unenforced. Something
laborious and harmless is `low`.

Rating by effort is the common failure, and it inverts the list precisely when
somebody is triaging under pressure.

## No status field

A finding never records whether it was addressed. That is written in a response,
and whether it was *accepted* is written in a verification.

**The finding is immutable.** Its state is derived by reading the exchange, which
is what lets an auditor and a respondent disagree in the record without either
overwriting the other.
