# What a project's store contains

A working inventory of the material a project keeps about itself, split by
lifecycle: what happened, what is in force, and what a machine regenerated.

Captured verbatim from a working note (2026-08-16). Nothing here is settled —
it is the long form of the list summarized in `luma-hq` under *One directory for
everything a project knows about itself*, kept here because the summary drops
the per-item glosses and the derived tier entirely.

## The record — append-only, dated, never edited

- **Decisions** — settled positions, the reasoning, deferred alternatives, re-open triggers
- **Audits** — foreman's dated run output: findings, verdicts, what passed
- **Logs** — what was done, when, by which agent or human; session transcripts worth keeping
- **Learnings** — discovered once, never rediscover (already flagged: unclear if this is the same shape as a decision)
- **Incidents and postmortems** — what broke, why, what changed because of it
- **Migrations** — schema, dependency, architecture moves and the rationale at the time
- **Provenance** — where vendored code came from, licensing origins, what was copied from where
- **Measurements** — perf baselines, benchmark runs, dated so drift is visible

## Standing rules — live, edited, currently in force

- **Guardrails** — invariants; what an agent must never do in this project
- **Workflows** — repeatable procedures: how to release, add a migration, onboard
- **Skills** — generalized, vendor-neutral capability definitions
- **Conventions** — house style, naming, terminology rules, prose rules
- **Boundaries** — what this project owns and must not own (derived from luma-hq, mirrored locally so it's readable offline)
- **Standards conformance** — which org standards this project claims, plus exemptions granted and why
- **Architecture** — current shape and its invariants; the map, not the history
- **Orientation** — the "start here" an arriving agent reads first
- **Verification policy** — what must pass, what done means here
- **Escalation rules** — when an agent must stop and ask a human
- **Glossary** — domain vocabulary and disambiguation
- **Data handling** — secrets policy, what never leaves the repo, redaction rules
- **Harness config** — servers, permissions, allowed commands, in vendor-neutral form

## Derived — machine-written, regenerable, probably ignored

- Indexes: symbol maps, file inventories, embedding manifests
- Cached analysis too expensive to redo
- Rolled-up digests of the record
