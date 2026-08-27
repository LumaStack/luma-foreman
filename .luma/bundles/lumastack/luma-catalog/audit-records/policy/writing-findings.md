---
type: policy
title: Writing a finding
description: What makes a finding actionable rather than an opinion — the five parts, how to rate severity, and the failures that make audits get ignored.
matches:
  - topic: writing a finding in an audit
sources:
  - id: audit-findings
    resource: https://simplerqms.com/audit-findings/
    title: "Audit Findings: Definition, Categories, Requirements, and How to Write"
  - id: iia-glossary
    resource: https://www.moxo.com/blog/internal-audit-glossary
    title: Modern internal audit glossary
---

# Writing a finding

**A finding is a claim that something is wrong, offered so somebody else can
check it.** That framing decides everything below: it must be specific enough to
verify, and it must say by whose rule it is wrong.

## The five parts

Borrowed from established internal-audit practice, where a finding is expected to
carry condition, criteria, cause, effect and recommendation.[^audit-findings]
They hold for code as readily as for process.

| part | the question | the failure when it is missing |
| --- | --- | --- |
| **condition** | what *is* | nobody can find what you are talking about |
| **criteria** | what *should be*, by whose rule | it reads as taste, and gets dismissed as taste |
| **cause** | why it is that way | the symptom gets fixed and returns |
| **effect** | what it costs if nothing changes | it cannot be prioritized against anything else |
| **recommendation** | what would resolve it | the respondent guesses, and guesses wrong |

## Criteria is what separates a finding from an opinion

> *"This function is too long."*

That is a preference, and a respondent is entitled to disagree with it on
preference.

> *"This function is 400 lines, against the 50-line limit in the project's own
> conventions."*

That is a finding. It can be disagreed with **on the merits** — the limit is
wrong, the limit does not apply here, the convention was abandoned — and every
one of those is a better conversation than *yes it is / no it is not*.

**Where no criterion exists, say so.** *"There is no stated limit; I am proposing
one"* is honest and often valuable. Dressing a proposal up as a violation is what
makes people stop reading audits.

## Cause is where the value is

Five findings sharing one cause are **one problem**. Fixing the cause closes all
five; fixing five conditions closes none of them, and they return under different
names.

An audit that reports conditions without causes generates work rather than
improvement — which is what audit fatigue actually is.

## Severity is consequence, never effort

`high` does not mean *hard to fix*. It means **what it costs if nobody ever
fixes it**.

| | |
| --- | --- |
| `high` | data lost, a credential published, a rule silently unenforced, a check that passes when it should not |
| `medium` | real cost, contained — rework, confusion, a hazard that needs a second mistake |
| `low` | true, worth recording, harmless if it stays |

Internal-audit practice rates on impact and likelihood rather than on remediation
cost for the same reason.[^iia-glossary] **Rating by effort inverts the list
exactly when somebody is triaging under pressure**, which is the moment the list
has to be right. A one-line fix to a
published credential is `high`. A week of tedious renaming that harms nobody is
`low`.

## Failures that make audits get ignored

**Volume without severity.** Forty findings, all medium, is a list nobody starts.
If everything matters, the audit has not done its job — which is to say what
matters most.

**Mechanical output filed as judgement.** A scanner reporting eleven instances of
one pattern is *one* finding with eleven locations, not eleven findings. Padding
a count with tool output buries what a person actually reasoned about.

**Findings nobody can act on.** *"The architecture is unclear"* has no condition,
no criteria, and no recommendation. Either do the work to make it a finding, or
leave it out.

**Criticising the absent.** A finding is about the artifact, never about who
wrote it. *"This was rushed"* is not a finding, and including it costs you the
respondent's attention for everything else in the audit.
