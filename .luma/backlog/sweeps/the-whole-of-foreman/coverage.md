---
type: coverage
title: Coverage — the whole of luma-foreman
indexed_at: aa467cc0657f
---

# Coverage

**Derived, and expected to lag.** The rows are [the charter](charter.md)'s scope
rule applied to the tree; what fills them is what the slices record. Every commit
ages this file, and every slice brings it back.

## Progress

| | |
| --- | --- |
| approved | 5 |
| reviewed, not signed off | 1 |
| with findings | 6 |
| skipped | 74 — `docs/examples/`, the idea backlog, the agent-permissions subsystem, and all remaining code, all excluded by the reader |
| removed | 3 — `docs/inspect.md`, `docs/scope.md`, `docs/standards.md` |
| pending | 10 |
| total rows | 93 |

**Rate: three slices, nine files.** Too few to be a range yet, and slice 001 was
atypical — it built the practice while it ran, producing five releases of
`review-sweeps`. **An outlier widens the range rather than being dropped from
it**, so it counts, and the range will say so once there is one.

## The index

**Three separate facts per row.** `reviewed_by` — who read it, any party.
`approved_by` — who signed it off, a human only. `outcome` — `clean` or
`findings`, what the reading concluded. **Empty means it has not happened**;
there is no `pending` value to keep in step.

**Approval is `recommended` here**, so a row that is read and never signed off is
a known compromise rather than a shortfall. `.luma/PROJECT.md` is the first.

**Four rows predate `review-sweeps` 0.20.0 and were closed by the agent
inferring a verdict** — `docs/scope.md`, `docs/standards.md`,
`docs/getting-started.md`, `docs/inspect.md`. The reader delegated rather than
re-confirming each. **They rest on general trust rather than on four specific
answers**, and the journal says which and why.

| cluster | file | read by | reviewed_by | approved_by | outcome | slice |
| --- | --- | --- | --- | --- | --- | --- |
| what it says it is | `README.md` | both | human:benlinton | human:benlinton | clean | 001 |
| what it says it is | `CLAUDE.md` | both | human:benlinton | human:benlinton | findings | 002 |
| what it says it is | `.luma/PROJECT.md` | both | human:benlinton |  | findings | 002 |
| what it says it is | ~~`docs/scope.md`~~ | both | human:benlinton |  | findings | 002 — scattered into eleven files, then deleted |
| what it says it is | `docs/getting-started.md` | both | human:benlinton | human:benlinton | findings | 001 |
| what it says it is | `docs/commands.md` | both | human:benlinton | human:benlinton | findings | 001 |
| — | ~~`docs/inspect.md`~~ | — | | | | 001 — collapsed into `commands.md` |
| what it says it is | `docs/architecture.md` | both | human:benlinton | human:benlinton | findings | 001 |
| standards and permissions | ~~`docs/standards.md`~~ | both | human:benlinton |  | findings | 003 — dropped, superseded by the adopted `luma-config` bundle |
| standards and permissions | `docs/claude-agent-permissions.md` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| standards and permissions | `docs/examples/README.md` | — |  |  |  | skipped — reader excluded `docs/examples/` from this sweep |
| standards and permissions | `docs/examples/american-spelling.md` | — |  |  |  | skipped — reader excluded `docs/examples/` from this sweep |
| standards and permissions | `docs/examples/design-first-working-mode.md` | — |  |  |  | skipped — reader excluded `docs/examples/` from this sweep |
| standards and permissions | `docs/examples/no-competitor-names-in-committed-docs.md` | — |  |  |  | skipped — reader excluded `docs/examples/` from this sweep |
| decisions | `.luma/records/decisions/ADR-0001-apply-writes-adapters-not-copies.md` | both |  |  |  |  |
| decisions | `.luma/records/decisions/ADR-0002-adoption-copies-and-never-resolves.md` | both |  |  |  |  |
| decisions | `.luma/records/decisions/ADR-0003-cli-speaks-convention-not-metaphor.md` | both |  |  |  |  |
| decisions | `.luma/records/decisions/ADR-0004-refit-is-removed-not-renamed.md` | both |  |  |  |  |
| decisions | `.luma/records/decisions/ADR-0005-a-retired-word-is-released-when-its-referent-goes.md` | both |  |  |  |  |
| plans, config, changelog | `.luma/backlog/plans/hook-delivery.md` | both |  |  |  |  |
| plans, config, changelog | `.luma/backlog/plans/knowledge-delivery.md` | both |  |  |  |  |
| plans, config, changelog | `.luma/config/luma-foreman.toml` | both |  |  |  |  |
| plans, config, changelog | `CHANGELOG.md` | both |  |  |  |  |
| plans, config, changelog | `.gitignore` | both |  |  |  |  |
| ideas A | `.luma/backlog/ideas/a-record-can-be-demoted.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/a-reminder-needs-somewhere-to-live.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/adopt-or-install-as-shorthand.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/apply-writes-an-entry-point-not-an-index.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/browsing-a-catalog-is-an-engines-job.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/bundle-routines.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/bundles-declare-what-they-work-with.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/bundles-wanted-not-built.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/committed-permission-floor.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas A | `.luma/backlog/ideas/declared-maturity-and-behaviour.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/distribution-beyond-clone-and-symlink.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/drive-an-incident.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/edit-ceremony-should-key-on-citations.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/feedback-and-learning.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/hook-against-leaking-internal-hq.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/independent-of-the-harness.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/knowledge-reaching-agents-elsewhere.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/named-permission-profiles.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/never-derive-an-actor-from-the-os-user.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas B | `.luma/backlog/ideas/new-repository-survey.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/no-format-for-non-procedural-knowledge.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/no-way-to-un-adopt.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/personal-skill-selection-not-committed.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/preload-levels-collapse-into-emphasis.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/prose-conventions.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/routers.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/the-gate-test-does-not-test-the-gate.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/scan-history-not-just-the-working-tree.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/verification-beyond-inspect.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/which-bundles-this-project-should-carry.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| ideas C | `.luma/backlog/ideas/workflows-invoking-workflows.md` | — |  |  |  | skipped — reader excluded the idea backlog from this sweep |
| entry and shared | `bin/luma-foreman` | — |  |  |  | skipped — code is a separate sweep |
| entry and shared | `src/foreman/cli.py` | — |  |  |  | skipped — code is a separate sweep |
| entry and shared | `src/foreman/config.py` | — |  |  |  | skipped — code is a separate sweep |
| entry and shared | `src/foreman/project.py` | — |  |  |  | skipped — code is a separate sweep |
| entry and shared | `src/foreman/bundle.py` | — |  |  |  | skipped — code is a separate sweep |
| entry and shared | `src/foreman/lkf.py` | — |  |  |  | skipped — code is a separate sweep |
| entry and shared | `src/foreman/__init__.py` | — |  |  |  | skipped — code is a separate sweep |
| adoption path | `src/foreman/get.py` | — |  |  |  | skipped — code is a separate sweep |
| adoption path | `src/foreman/adoption.py` | — |  |  |  | skipped — code is a separate sweep |
| adoption path | `src/foreman/catalog.py` | — |  |  |  | skipped — code is a separate sweep |
| adoption path | `src/foreman/outdated.py` | — |  |  |  | skipped — code is a separate sweep |
| adoption path | `src/foreman/init.py` | — |  |  |  | skipped — code is a separate sweep |
| apply | `src/foreman/apply.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/__init__.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/registry.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/finding.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/report.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/rules/__init__.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/rules/bundles.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/rules/adoption.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/rules/identity.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/rules/secrets.py` | — |  |  |  | skipped — code is a separate sweep |
| inspect | `src/foreman/inspect/rules/vocabulary.py` | — |  |  |  | skipped — code is a separate sweep |
| agent permissions | `src/foreman/agent_permissions/__init__.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/model.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/store.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/match.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/gate.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/commands.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/install.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `src/foreman/agent_permissions/doctor.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| agent permissions | `libexec/permission-gate.py` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| tests | `tests/run` | — |  |  |  | skipped — code is a separate sweep |
| tests | `tests/adopt-test.sh` | — |  |  |  | skipped — code is a separate sweep |
| tests | `tests/agent-permissions-cli-test.sh` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
| tests | `tests/apply-test.sh` | — |  |  |  | skipped — code is a separate sweep |
| tests | `tests/inspect-test.sh` | — |  |  |  | skipped — code is a separate sweep |
| tests | `tests/permission-gate-test.sh` | — |  |  |  | skipped — agent permissions are half-baked, and settling that is outside MVP |
