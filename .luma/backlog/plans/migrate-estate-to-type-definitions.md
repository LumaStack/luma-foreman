---
type: document
type_version: "0.0.1"
title: Migrate the estate to type_definitions
description: What each Luma repository must do to conform to LKF v0.0.21's versioned type system — the recipe, the order of operations, per-repository directives, and the linter decision brief.
stage: provisional
survival: temporary
created: { by: agent:claude-fable-5, at: 2026-09-19T00:00:00Z }
sources:
  - resource: https://github.com/LumaStack/luma-knowledge-format/releases/tag/v0.0.21
    title: LKF v0.0.21 release notes
  - resource: https://github.com/LumaStack/luma-knowledge-format/releases/tag/v0.0.22
    title: LKF v0.0.22 release notes
---

# Migrate the estate to type_definitions

**A work order, not a policy — `survival: temporary` says so.** It is done when
every repository below conforms, and it should be pruned then. It lives in
foreman's plans because foreman drives the re-adopt wave; the estate has no
headquarters repository yet, which is where a cross-repo directive like this
one properly belongs — that gap is noted at the end.

This directive supersedes the estate-wide halves of two ideas in this backlog:
[[rename-types-to-type-definitions]] (now the work order for foreman's own
code, below) and [[frontmatter-needs-a-version-and-types-need-migrations]]
(answered upstream — LKF shipped the sibling-field design it leaned toward).

## What changed in the format

LKF `v0.0.21` (with an examples-only `v0.0.22` behind it) is a breaking
release, shipped as a patch under the pre-1.0 tier. Six rules, in the order
they bite:

1. **`_types/` is renamed `type_definitions/`.** The reserved directory is
   named for what it holds. `_types/` is retired and free.
2. **Every Type Definition is a folder.**
   `type_definitions/<name>/DEFINITION.md` is the contract and the only name
   resolution reads. Beside it: `CHANGELOG.md` (expected), `migrations/`
   (allowed), and prior versions kept as `DEFINITION-<version>.md`. The
   single-file shape no longer exists.
3. **Every Type Definition declares its own `version`**, independent of
   `lkf_version` and of the Bundle's version. New types start at `0.0.1`.
4. **Every Document carries `type_version`** — a core field, `recommended`
   everywhere: the `version` of the Document's type's definition it was
   written against, copied from the definition, never minted. Written
   **directly beneath `type`**, so the two lines read as one claim. Absence is
   legal and means *unstated*.
5. **One rule sorts every version field.** Bare `version` is what a Document
   publishes; a qualified `*_version` is what it conforms to. A Type
   Definition is the one kind of Document with both: its own `version`
   (published to its instances) beside `type_version` (tracking the
   `type_definition` contract).
6. **Failure stays safe.** A consumer that has not updated finds no `_types/`
   and resolves no bundle-local types. Documents still read as conformant;
   types are tolerated as unknown; the absence should be reported, never
   fatal.

The target shape, on one worked example:

```
type_definitions/work_item/
  DEFINITION.md          # the contract. Required.
  CHANGELOG.md           # what changed in each version, and why
  migrations/            # how to bring a Document up to the current version
  DEFINITION-0.0.1.md    # a prior version, kept while consumers cross
```

```yaml
# DEFINITION.md frontmatter          # any instance Document
type: type_definition                # type: work_item
type_version: "0.0.1"                # type_version: "0.0.1"
defines: work_item                   # title: Fix the flaky deploy check
version: "0.0.1"
```

## The recipe, per bundle

Mechanical, and the same everywhere a bundle holds types:

1. `git mv _types type_definitions`
2. For each type: make a folder named for the type, move the file in as
   `DEFINITION.md` (`type_definitions/work_item.md` →
   `type_definitions/work_item/DEFINITION.md`).
3. In each `DEFINITION.md` frontmatter: add `type_version: "0.0.1"` directly
   under `type`, and — if the type declares no `version` — add
   `version: "0.0.1"` directly under `defines`. **Types that already declare
   a version keep it.**
4. Start a `CHANGELOG.md` beside each definition: keyed by the type's own
   version, newest first, naming the release or date each bump shipped. No
   retroactive backfill — open at the current version.
5. Stamp instance Documents with `type_version` (copy the type's current
   `version`) beneath their `type` line. Recommended, not required —
   stamping in bulk during this wave is cheapest, but a straggler is legal.
6. Update any prose, templates, or generated `INDEX.md` that says `_types/`.

## Order of operations

The dependency chain matters: foreman, backlog, and leader hold **vendored
copies** of catalog bundles under `.luma/bundles/`, and those migrate by
**re-adopting from the catalog**, never by hand-editing.

1. **luma-catalog** migrates first — it is the source every other repo
   re-adopts from.
2. **luma-foreman's code** learns the new layout (a clean cut with the
   re-adopt wave is simpler than a both-shapes transition; the estate is
   small).
3. **The re-adopt wave**: foreman, backlog, and leader re-adopt their vendored
   bundles; each repo also migrates anything locally owned and stamps its own
   Documents.
4. **Independent stores**: clarify (own code and own root types) and
   catalog-curator (documents only) move on their own clocks, after steps 1–2
   give them a settled target.

## Per-repository directives

### luma-catalog — goes first (~241 documents)

The source of truth: every other repo re-adopts its bundles, so its migration
is the estate's.

- Run the recipe on all **13 bundles carrying `_types/`**: audit-records,
  backlog-ideas, decision-records, incident-records, luma-types,
  organization-internal-hq, project-documentation, retirement-records,
  review-sweeps, session-manager, token-manager, tutorial-workflow-maker,
  violation-records.
- **Versions**: luma-types already versions its types (`catalog` 0.3.0,
  `project` 0.2.0, `idea` 0.1.0, `tutorial_step` 0.3.0, `tutorial_quiz`
  0.1.0) — keep those. The unversioned rest (audit, finding, response,
  verification, decision, decision_log, incident, repository, retirement,
  coverage, journal, slice, sweep, session_note, violation) start at `0.0.1`.
- **Fix a real drift found during the survey behind this directive**:
  `project-documentation/_types/project.md` declares `0.1.0` while upstream
  `luma-types` is at `0.2.0`. Re-vendor it during the move and update its
  `vendored_from`. This drift is exactly what the new rules exist to make
  loud.
- Sweep prose and templates: `bundle-manager`'s `organizing-a-bundle.md`,
  `audit-bundle.md`, and `templates/type-definition.md` (the template should
  now model the folder shape and both version fields);
  `luma-layout/policy/luma-directory-layout.md`;
  `luma-maintainers/policy/the-estate.md`;
  `tutorial-workflow-maker/procedure/create-tutorial.md`;
  `decision-records/procedure/record-decision.md`; `CATALOG.md`; `README.md`.
- Regenerate every bundle's `INDEX.md` — most mention `_types/` and all are
  derived anyway.
- Bump each migrated bundle's `version` in its `BUNDLE.md` (layout changed),
  and give `BUNDLE.md` itself `type_version: "0.0.1"` beneath its `type`.

### luma-foreman — code, then re-adopt (~248 documents)

The engine: the only repo where this is a code change before it is a file
move.

- `src/foreman/apply.py:82` — `SKIP = ("_types",)` becomes
  `("type_definitions",)`; update the comment above it. The skip should also
  cover a type folder's `CHANGELOG.md` and `migrations/`, which are record,
  not reading material.
- `src/foreman/inspect/rules/bundles.py:57` —
  `EXEMPT_DIRS = ("templates", "_types")` gains the new name; `:323` — the
  `doc_id.startswith("_types/")` check follows.
- Anywhere a contract is resolved: the lookup is now
  `type_definitions/<name>/DEFINITION.md` — one shape, no file fallback.
- Re-adopt all vendored bundles under `.luma/bundles/lumastack/luma-catalog/`
  once the catalog has migrated; `adopted.toml` checksums refresh with the
  wave.
- Backlog hygiene: [[rename-types-to-type-definitions]] is now the work
  order — execute its blast-radius list and prune it.
  [[frontmatter-needs-a-version-and-types-need-migrations]] is answered
  upstream — prune, pointing at LKF `v0.0.21`.
- [[retire-the-migration-tolerances]] gains its missing gate: once documents
  carry `type_version`, "every repository migrated" becomes a query, not a
  belief.

### luma-backlog — own bundle, then re-adopt (~347 documents)

- One locally-owned bundle to hand-migrate:
  `.luma/bundles/local/backlog/_types/` holding `work-item.md` and
  `outcome.md` — both unversioned, both start at `0.0.1`. Note while moving:
  the folder is named for the *type*, so if the type is `work_item`
  (snake_case, per the format's casing recommendation) the folder is
  `type_definitions/work_item/`, whatever the old filename's hyphenation
  said.
- Everything under `.luma/bundles/lumastack/` is vendored — re-adopt after
  the catalog migrates.
- The big stamping job lives here: the backlog's items are the estate's
  largest body of typed Documents. Stamp `type_version` from each type's
  current version (`luma/idea` instances cite `0.1.0`; local work items cite
  `0.0.1`).

### luma-clarify — code and own types, independent clock

Self-contained: nine types of its own at the repo root, and Python that
resolves them.

- Code first: `src/clarify/resolve.py:22` — `TYPES = "_types"`;
  `find_types()` and `config.py:78/81` (the packaged copy at
  `clarify/_types` and the checkout copy at the repo root) all learn
  `type_definitions/<name>/DEFINITION.md`; the packaged data directory ships
  under the new name; `tests/test_small_gaps.py` follows.
- Then the store: `_types/` → `type_definitions/`, folders for `input`,
  `original`, `reference`, `fidelity`, `extraction`, `source`,
  `verification`, `finding`, `coverage` — all unversioned today, all start
  at `0.0.1`.
- Worth knowing: this store sits at a repo root, not inside a Bundle — the
  exact case LKF's roadmap tracks under *"Where type_definitions resolves."*
  The likely spec fix keys resolution on the directory root a Document is
  found under, which is what clarify already does. Migrating the layout now
  keeps clarify aligned with wherever that lands.
- Notebook documents get `type_version: "0.0.1"` stamps as they are next
  touched.

### luma-leader — re-adopt and stamp (~103 documents)

- No locally-owned types: everything under `.luma/bundles/lumastack/` is
  vendored — re-adopt after the catalog migrates.
- Stamp `type_version` on locally-authored Documents (backlog ideas cite
  `luma/idea` at `0.1.0`, and so on per type).

### luma-catalog-curator — documents only

- No `_types/` anywhere: nothing structural to migrate. Stamp its handful of
  Documents with `type_version` once the types they cite have settled
  versions.

## Version numbers, settled

| What | Rule |
| --- | --- |
| A type gaining a version now | Starts at `0.0.1` — the earliest, most-unstable tier, same as the format itself began. |
| A type already versioned | **Keeps its number.** Restarting `idea` at 0.0.1 would run history backwards and break every `vendored_from` already citing 0.1.0. |
| Every Document | Gains `type_version` beneath `type`, copied from its type's current version. Absent stays legal (means *unstated*) — so stamping can ride any convenient wave. |
| A vendored copy | Its `vendored_from.version` is the type's own version; refresh it whenever re-vendoring. |
| What a bump means | Deliberately undefined for now — compare for equality and difference, infer nothing from the tier. The semver-tier semantics for types remain an open LKF roadmap item. |

A type's version moves when its contract changes — a new field, a changed
presence, a renamed key — and each bump earns a `CHANGELOG.md` entry and, once
real migrations exist, a file in `migrations/`.

## The linter — decision brief

Two distinct jobs travel under the word "linter," and they should be named
separately:

- **Linting Type Definitions themselves** — folder shape present,
  `DEFINITION.md` exists and declares `defines`, `version` present,
  `CHANGELOG.md` present, fields well-formed, inheritance add-only, presence
  strengthened never weakened.
- **Validating Documents against their type** — required fields present,
  values match their `field_type`, enum values legal, deprecated fields
  flagged — plus the new check that pays for this whole migration:
  **`type_version` currency**, i.e. *which Documents were written against an
  older contract than the one beside them*. That query is the migration
  gate.

Three constraints are already decided by the format's own documents:

- Validation is **optional and never rejects by default** — the spec's
  Validation section is a suggested framework with a defined severity table,
  and `--strict` is the opt-in escalation. A linter is an implementation of
  that table, not a new authority.
- **It cannot live in luma-knowledge-format.** The format repo's own boundary
  says it plainly: *"It is a specification, not an implementation. Nothing
  here reads a document or validates one."*
- Whatever hosts it should implement *against the spec's table*, so a second
  consumer can implement the same checks and agree with the first.

Where it could live:

| Option | For | Against |
| --- | --- | --- |
| **foreman's `inspect/`** (new rule modules) | The machinery exists — inspect rules, bundle indexing, adopt/audit hooks. Ships this week, guards the re-adopt wave as it lands. | Couples the estate's only validator to one tool; other adopters get nothing. |
| **A standalone `lkf-lint`** (own repo, CLI) | Usable by any LKF adopter; the spec's validation table gets a reference implementation; foreman shells out. | A new repo to run for one consumer today; premature until a second consumer exists. |
| **A catalog bundle procedure** (agent-run checks) | Travels with adoption like all estate policy; no new code surface. | Prose checklists drift and cannot be a gate; shape checks want code, not judgment. |

**Recommendation: build it in foreman's `inspect/` now; write it against the
spec's validation table so it can be extracted later.** Two rule modules:
`type_definitions.py` (the definition lint) and a `type_version` currency
check added to document validation. Wire both into the audit that already runs
at adopt time, so the re-adopt wave is checked by the thing it ships with. The
catalog's `audit-bundle` procedure then *points at* the tool rather than
restating its checks. Extract to a standalone `lkf-lint` the day a second
consumer wants it — the spec-table discipline makes that a move, not a
rewrite. Severities follow the spec exactly: missing-required warns,
shape-mismatch warns, unknown fields never error, `--strict` escalates; the
currency check reports *out of date* as info, because old-but-labeled is the
system working.

**Left for the maintainer to rule on:** whether a stale `type_version` should
ever block an adopt under `--strict` (recommendation: no — report only), and
whether the definition lint's *missing `CHANGELOG.md`* finding is warning or
info while the estate migrates (recommendation: info until the wave completes,
warning after).

## Where this document belongs, eventually

This is organization-level coordination — the kind of record the catalog's
`organization-internal-hq` bundle says belongs in a headquarters repository.
No such repository exists yet; this plan sits in foreman's backlog because
foreman drives the wave. **If an HQ is ever stood up, this document (and the
question it keeps raising) moves there.**

## Done when

Every repository above conforms; the `type_version` currency query runs clean
or reports only known stragglers; the two superseded foreman ideas are pruned.
Then prune this plan — `survival: temporary` is a promise.

## Reference

Spec: [lkf.md](https://github.com/LumaStack/luma-knowledge-format/blob/main/luma-knowledge-format/specification/lkf.md)
— sections *Type extensions → One folder per type*, *type_version*, *Reserved
files*, *Versioning*. Releases:
[v0.0.21](https://github.com/LumaStack/luma-knowledge-format/releases/tag/v0.0.21)
(the change, with upgrade notes) ·
[v0.0.22](https://github.com/LumaStack/luma-knowledge-format/releases/tag/v0.0.22)
(examples). Worked models: the format's own Bundle —
`luma-knowledge-format/type_definitions/*/` — is the layout, stamped and
changelogged, to copy from.
