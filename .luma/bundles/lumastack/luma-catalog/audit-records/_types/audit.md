---
type: type_definition
defines: audit
fields:
  audited:
    field_presence: required
    field_type: date
    desc: "when the audit was performed"
  commit:
    field_presence: required
    field_type: text
    desc: "the full or 12-character commit the audit examined — what it says is true of"
  scope:
    field_presence: required
    field_type: text
    desc: "what was examined, and what deliberately was not"
  auditor:
    field_presence: recommended
    field_type: actor
    desc: "who or what performed it (§7.4)"
  also_examined:
    field_presence: optional
    desc: "other repositories examined, each with the commit it was at — see below. No field_type: it is a list of records, which §10.2 cannot yet express"
---

# Audit

The record of one audit: what was examined, at which commit, by whom, and what
was deliberately left out. **It is not the findings** — those are separate
Documents beside it — it is the frame that makes them interpretable.

## `commit` is what makes an audit meaningful

An audit without a commit says *something was wrong once*. With one it says
*this was true of exactly this code*, which is the difference between a finding
somebody can act on and a finding somebody has to re-derive.

Record at least **12 characters**. Git's 7-character default begins colliding in
repositories large enough to need auditing, and an ambiguous commit makes the
whole record unverifiable.

## `scope` must say what was *not* examined

The half people skip, and the one that decides whether a clean audit means
anything. *"Reviewed the HTTP layer; did not examine authentication or the data
model"* is a useful record. *"Reviewed the codebase"* is not, because a reader
cannot tell the difference between *examined and clean* and *never looked*.

**A skipped check is not a pass**, and an audit that does not say what it skipped
manufactures confidence it never earned.

## `also_examined`, for an audit that crosses repositories

One repository owns the record and its commit names the directory. Everything
else examined is pinned here:

```yaml
also_examined:
  - repository: ../luma-foreman
    commit: 07c062e1a2b3
  - repository: ../luma-catalog
    commit: fc7a2a8b91de
```

**Without this the audit is unreproducible.** The owning repository's commit
pins one side of a claim about several, and the others move immediately —
a finding about how two repositories interact cannot be checked against
"whatever those were at the time".

Record the path as it was used, and the commit at twelve characters or more.

## No status field

An audit does not carry a state, and neither does a finding. What happened to a
finding is written by whoever acted on it, in their own Document — a response,
then a verification.

**Current state is derived by reading the exchange, never stored.** Records are
append-only, so a status field would have to be edited by somebody who did not
write the record, which is the one thing this shape exists to prevent.
