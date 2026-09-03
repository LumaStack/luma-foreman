---
type: type_definition
defines: response
fields:
  responds_to:
    field_presence: required
    field_type: text
    desc: "the audit this answers — its directory name, e.g. 2026-12-23-e286f3bd9c11"
  responded:
    field_presence: required
    field_type: date
    desc: "when the response was filed"
  respondent:
    field_presence: recommended
    field_type: actor
    desc: "who or what answered"
  round:
    field_presence: optional
    field_type: number
    desc: "1 unless a verification reopened something and a second answer was needed"
sources:
  - id: management-response
    resource: https://www.v-comply.com/glossary/management-response/
    title: "Management Response in Audits: Definition, Elements & Examples"
---

# Response

The respondent's answer to an audit: a position on every finding, written by
whoever is accountable for the thing audited rather than by the auditor.

**Independence is the point.** An auditor who also writes the response is
grading their own work, and the record loses the property that made it worth
keeping.

## A position on every finding, including the ones you disagree with

Four positions, mirroring the agree / partially agree / disagree split of a
management response.[^management-response] The last two are first-class outcomes
rather than failures:

| position | means |
| --- | --- |
| **agreed** | the finding is correct and has been addressed |
| **partially agreed** | part is correct; say precisely which part, and why the rest is not |
| **disagreed** | the finding is wrong. State why — the criteria did not apply, the condition was misread |
| **accepted** | the finding is correct and will not be addressed. The cost of fixing exceeds the cost of living with it |

**Accepted is not disagreed.** *You are right and we are choosing to carry this*
is a legitimate answer and a valuable record — six months later it is the
difference between a decision somebody made and something everybody forgot.

**Answer every finding.** Silence on one is indistinguishable from having missed
it, and the auditor cannot verify a position that was never taken.

## Say what changed, not that something changed

*"Fixed"* is not a response. **A response points at the change** — a commit, a
pull request, a file. Verification has to be possible without asking, or the
loop is trust rather than record.

## Round

Absent means the first answer. A verification that reopens a finding produces a
second response — `round: 2` — rather than an edit to the first, because the
first is a record of a position genuinely held at the time.

Most audits never reach round two.
