---
type: coverage
title: Coverage — the whole of luma-foreman
indexed_at: 52787ca6b968
---

# Coverage

**Derived, and expected to lag.** The rows are [the sweep](sweep.md)'s scope rule
applied to the tree; the statuses are what the slices record. Every commit ages
this file, and every slice brings it back.

## Progress

| | |
| --- | --- |
| approved | 4 |
| reviewed | 0 |
| skipped | 0 |
| removed | 1 — `docs/inspect.md`, collapsed into `commands.md` |
| pending | 82 |
| total rows | 87 |

**Rate: one slice, four files.** Too few to be a range yet, and slice 001 was
atypical — it built the practice while it ran, producing five releases of
`review-sweeps`. **An outlier widens the range rather than being dropped from
it**, so it counts, and the range will say so once there is one.

## The index

`pending` · `reviewed` · `approved` · `skipped` **with a reason, always**

**`reviewed`** — read and satisfactory; either party may set it. **`approved`** —
signed off, and only a person gives it. The `by` column records who.

| cluster | file | read by | status | by | slice |
| --- | --- | --- | --- | --- | --- |
| what it says it is | `README.md` | both | **approved** | `human:benlinton` | — |
| what it says it is | `CLAUDE.md` | both | pending | | |
| what it says it is | `.luma/PROJECT.md` | both | pending | | |
| what it says it is | `docs/scope.md` | both | pending | | |
| split from README | `docs/getting-started.md` | both | **approved** | `human:benlinton` | 001 |
| split from README | `docs/commands.md` | both | **approved** | `human:benlinton` | 001 |
| split from README | ~~`docs/inspect.md`~~ | both | **removed** | — | 001 — collapsed into `commands.md` |
| split from README | `docs/architecture.md` | both | **approved** | `human:benlinton` | 001 |
| standards and permissions | `docs/standards.md` | both | pending | | |
| standards and permissions | `docs/claude-agent-permissions.md` | both | pending | | |
| standards and permissions | `docs/examples/README.md` | both | pending | | |
| standards and permissions | `docs/examples/american-spelling.md` | both | pending | | |
| standards and permissions | `docs/examples/design-first-working-mode.md` | both | pending | | |
| standards and permissions | `docs/examples/no-competitor-names-in-committed-docs.md` | both | pending | | |
| decisions | `.luma/records/decisions/ADR-0001-apply-writes-adapters-not-copies.md` | both | pending | | |
| decisions | `.luma/records/decisions/ADR-0002-adoption-copies-and-never-resolves.md` | both | pending | | |
| decisions | `.luma/records/decisions/ADR-0003-cli-speaks-convention-not-metaphor.md` | both | pending | | |
| decisions | `.luma/records/decisions/ADR-0004-refit-is-removed-not-renamed.md` | both | pending | | |
| decisions | `.luma/records/decisions/ADR-0005-a-retired-word-is-released-when-its-referent-goes.md` | both | pending | | |
| plans, config, changelog | `.luma/backlog/plans/hook-delivery.md` | both | pending | | |
| plans, config, changelog | `.luma/backlog/plans/knowledge-delivery.md` | both | pending | | |
| plans, config, changelog | `.luma/config/luma-foreman.toml` | both | pending | | |
| plans, config, changelog | `CHANGELOG.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/a-record-can-be-demoted.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/a-reminder-needs-somewhere-to-live.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/adopt-or-install-as-shorthand.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/apply-writes-an-entry-point-not-an-index.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/browsing-a-catalog-is-an-engines-job.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/bundle-routines.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/bundles-wanted-not-built.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/committed-permission-floor.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/declared-maturity-and-behaviour.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/distribution-beyond-clone-and-symlink.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/drive-an-incident.md` | both | pending | | |
| ideas A | `.luma/backlog/ideas/edit-ceremony-should-key-on-citations.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/bundles-declare-what-they-work-with.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/never-derive-an-actor-from-the-os-user.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/hook-against-leaking-internal-hq.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/knowledge-reaching-agents-elsewhere.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/named-permission-profiles.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/new-repository-survey.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/no-way-to-un-adopt.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/personal-skill-selection-not-committed.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/preload-levels-collapse-into-emphasis.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/prose-conventions.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/routers.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/scan-history-not-just-the-working-tree.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/which-bundles-this-project-should-carry.md` | both | pending | | |
| ideas B | `.luma/backlog/ideas/workflows-invoking-workflows.md` | both | pending | | |
| entry and shared | `bin/luma-foreman` | agent | pending | | |
| entry and shared | `src/foreman/cli.py` | agent | pending | | |
| entry and shared | `src/foreman/config.py` | agent | pending | | |
| entry and shared | `src/foreman/project.py` | agent | pending | | |
| entry and shared | `src/foreman/bundle.py` | agent | pending | | |
| entry and shared | `src/foreman/lkf.py` | agent | pending | | |
| entry and shared | `src/foreman/__init__.py` | agent | pending | | |
| adoption path | `src/foreman/get.py` | agent | pending | | |
| adoption path | `src/foreman/adoption.py` | agent | pending | | |
| adoption path | `src/foreman/catalog.py` | agent | pending | | |
| adoption path | `src/foreman/outdated.py` | agent | pending | | |
| adoption path | `src/foreman/init.py` | agent | pending | | |
| apply | `src/foreman/apply.py` | agent | pending | | |
| inspect | `src/foreman/inspect/__init__.py` | agent | pending | | |
| inspect | `src/foreman/inspect/registry.py` | agent | pending | | |
| inspect | `src/foreman/inspect/finding.py` | agent | pending | | |
| inspect | `src/foreman/inspect/report.py` | agent | pending | | |
| inspect | `src/foreman/inspect/rules/__init__.py` | agent | pending | | |
| inspect | `src/foreman/inspect/rules/bundles.py` | agent | pending | | |
| inspect | `src/foreman/inspect/rules/adoption.py` | agent | pending | | |
| inspect | `src/foreman/inspect/rules/identity.py` | agent | pending | | |
| inspect | `src/foreman/inspect/rules/secrets.py` | agent | pending | | |
| inspect | `src/foreman/inspect/rules/vocabulary.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/__init__.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/model.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/store.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/match.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/gate.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/commands.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/install.py` | agent | pending | | |
| agent permissions | `src/foreman/agent_permissions/doctor.py` | agent | pending | | |
| agent permissions | `libexec/permission-gate.py` | agent | pending | | |
| tests | `tests/run` | agent | pending | | |
| tests | `tests/adopt-test.sh` | agent | pending | | |
| tests | `tests/agent-permissions-cli-test.sh` | agent | pending | | |
| tests | `tests/apply-test.sh` | agent | pending | | |
| tests | `tests/inspect-test.sh` | agent | pending | | |
| tests | `tests/permission-gate-test.sh` | agent | pending | | |
