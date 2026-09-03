#!/bin/sh
# Tests for how `luma-foreman apply` derives delivery from what a Document
# declares.
#
#   sh tests/apply-test.sh
#
# `adopt-test.sh` covers apply end to end — that a skill appears, that
# CLAUDE.md is spliced rather than owned, that orphans leave. This file covers
# the part that decides *what* gets written: an author declares `matches`, and
# the loading posture is derived — never chosen by hand:
#
#   eager     required reading the moment its bundle is in play
#   offered   named in its bundle's index, opened when it matches
#   standby   reachable, not announced
#
# Postures are container-relative: eager on a document means required reading
# when the bundle opens; eager on the bundle itself lifts its required
# documents into every session's floor, imported by the project index. And
# `register: nothing` in the manifest parks a bundle entirely — landed, not
# wired.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

# Hermetic: the operator's own harness wiring must not decide what these cases
# see.

T=$(mktemp -d /tmp/apply.XXXXXX) || exit 2
export CLAUDE_CONFIG_DIR=$T/no-harness
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

exists()  { [ -e "$1" ] && ok || bad "expected to exist: $1"; }
absent()  { [ -e "$1" ] && bad "expected NOT to exist: $1" || ok; }
grepped() { grep -q -- "$1" "$2" 2>/dev/null && ok || bad "expected '$1' in $(basename "$2")"; }
ungrep()  { grep -q -- "$1" "$2" 2>/dev/null && bad "expected '$1' NOT in $(basename "$2")" || ok; }

apply() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" apply "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

# --- a project with one bundle written into it ----------------------------------

PROJECT=$T/project
B=$PROJECT/.luma/bundles/acme/rules
mkdir -p "$B/policy" "$B/concepts" "$B/_types" \
         "$B/procedure/run-the-thing/steps" "$PROJECT/.claude"
(cd "$PROJECT" && git init -q . 2>/dev/null) || true

cat > "$B/BUNDLE.md" <<'EOF'
---
type: bundle
title: acme/rules
version: 0.1.0
description: Rules for widget work.
---
EOF

# eager: required reading the moment this bundle is in play.
cat > "$B/policy/house-rules.md" <<'EOF'
---
type: policy
title: House rules
description: The rules that govern all work here.
matches: eager
---
Everything here is always in force.
EOF

# offered: it governs stylesheets, and costs nothing before they come up.
cat > "$B/policy/stylesheets.md" <<'EOF'
---
type: policy
title: Stylesheet rules
description: How stylesheets are written here.

matches:
  - path: "**/*.css"
---
Rules for CSS.
EOF

# offered, with teeth: fired by a command, blocking on violation.
cat > "$B/policy/no-credentials.md" <<'EOF'
---
type: policy
title: Never commit a credential
description: Credentials must not reach a commit.

on_violation: block
matches:
  - command: git commit
---
Do not commit credentials.
EOF

# standby: no matches, so nothing volunteers it. Reached by request.
cat > "$B/concepts/why-widgets.md" <<'EOF'
---
type: document
title: Why widgets
description: Background on why widgets exist.
---
Rationale.
EOF

# a procedure that owns a directory, and the steps it owns.
cat > "$B/procedure/run-the-thing/PROCEDURE.md" <<'EOF'
---
type: procedure
title: Run the thing
description: Run the thing. Use when the thing needs running.
---
Step one, step two.
EOF

cat > "$B/procedure/run-the-thing/steps/01-first.md" <<'EOF'
---
type: acme/step
title: First step
---
Do the first bit.
EOF

cat > "$B/_types/widget.md" <<'EOF'
---
type: type_definition
defines: widget
title: Widget
description: The shape of a widget record.
---
Fields go here.
EOF

CLAUDE=$PROJECT/CLAUDE.md
INDEX=$PROJECT/.luma/bundles/INDEX.md
SKILLS=$PROJECT/.claude/skills

apply 'projects a bundle written in place' 0

# --- the split: a project index, and an adapter that only points at it ----------

grepped 'INDEX.md' "$CLAUDE"
grepped '@.luma/bundles/INDEX.md' "$CLAUDE"
[ -f "$INDEX" ] && ok || bad 'expected the project index to be written'
grepped 'Every container has an index' "$INDEX"

# --- the project index is bundle-grained ----------------------------------------
#
# One entry per bundle, under the posture its own declaration derives. What is
# inside a bundle is its own index's business — which is what keeps the floor
# per-bundle rather than per-document.

grepped 'acme/rules' "$INDEX"
grepped 'Rules for widget work.' "$INDEX"
grepped 'Offered — open a bundle' "$INDEX"
ungrep 'house-rules' "$INDEX"
ungrep 'stylesheets' "$INDEX"
ungrep 'why-widgets' "$INDEX"

# --- procedures are carried by skills, and are not named twice ------------------

grepped 'run-the-thing' "$SKILLS/run-the-thing/SKILL.md"
ungrep 'run-the-thing' "$INDEX"

# --- an eager bundle assembles the floor ----------------------------------------
#
# eager on the bundle lifts its required documents into every session: the
# adapter imports the project index, the project index imports the documents.
# The whole floor is auditable by reading one file.

BASE=$PROJECT/.luma/bundles/acme/base
mkdir -p "$BASE/policy"
cat > "$BASE/BUNDLE.md" <<'EOF'
---
type: bundle
title: acme/base
version: 0.2.0
description: How work is done here, in force everywhere.
matches: eager
---
EOF
cat > "$BASE/policy/core.md" <<'EOF'
---
type: policy
title: Core conduct
description: The floor rules.
matches: eager
---
Always in force.
EOF

apply 'projects an eager bundle' 0
grepped 'Required — imported here' "$INDEX"
grepped 'acme/base' "$INDEX"
grepped '@acme/base/policy/core.md' "$INDEX"
# The import lives in the index, not the adapter — one file assembles the floor.
ungrep '@acme/base/policy/core.md' "$CLAUDE"
# An ordinary bundle's eager document is scoped to its bundle, never the floor.
ungrep '@acme/rules/policy/house-rules.md' "$INDEX"

# --- a bundle declaring nothing is adopted, and never volunteered ---------------

QUIET=$PROJECT/.luma/bundles/acme/quiet
mkdir -p "$QUIET"
cat > "$QUIET/BUNDLE.md" <<'EOF'
---
type: bundle
title: acme/quiet
version: 0.1.0
description: A reference shelf nobody should be told about twice.
matches: nothing
---
EOF

apply 'projects a by-request bundle' 0
grepped 'By request — adopted, and never volunteered' "$INDEX"
grepped 'acme/quiet' "$INDEX"

# --- register: nothing parks a bundle everywhere --------------------------------
#
# Intent from the manifest: deliberately landed and not wired. No index entry,
# no skills — and the run says so, because a silent skip reads as a bug.

PARKED=$PROJECT/.luma/bundles/acme/parked
mkdir -p "$PARKED/procedure"
cat > "$PARKED/BUNDLE.md" <<'EOF'
---
type: bundle
title: acme/parked
version: 0.1.0
description: Landed, not wired.
---
EOF
cat > "$PARKED/procedure/do-parked-things.md" <<'EOF'
---
type: procedure
title: Do parked things
description: A procedure that must not become a skill.
---
Steps.
EOF
cat > "$PROJECT/.luma/bundles/MANIFEST.md" <<'EOF'
<!-- Written by `luma-foreman`. Change it with commands, not by hand. -->

# Bundles

- `acme/parked` 0.1.0
  - register: nothing
EOF

apply 'parks a register-nothing bundle' 0
ungrep 'acme/parked' "$INDEX"
absent "$SKILLS/do-parked-things"
case $LAST in *parked*) ok ;; *) bad "expected the parked bundle reported: $LAST" ;; esac
rm -rf "$PARKED" "$PROJECT/.luma/bundles/MANIFEST.md"

# --- subordination --------------------------------------------------------------
#
# The steps under a procedure's directory belong to that procedure. They are
# reachable only through it — one adopted bundle once put twenty-one step
# titles into every session before anybody noticed.

apply 'reapplies after the parked bundle left' 0
ungrep '01-first' "$CLAUDE"
ungrep '01-first' "$INDEX"
absent "$SKILLS/01-first"

# --- the procedure itself, and the name its directory gives it ------------------

exists "$SKILLS/run-the-thing/SKILL.md"
grepped 'name: run-the-thing' "$SKILLS/run-the-thing/SKILL.md"
grepped 'Use when the thing needs running' "$SKILLS/run-the-thing/SKILL.md"
# Thin: a pointer, never a copy.
ungrep 'Step one, step two' "$SKILLS/run-the-thing/SKILL.md"
grepped '.luma/bundles/acme/rules/procedure/run-the-thing' "$SKILLS/run-the-thing/SKILL.md"
# The bundle's eager documents ride along as required reading, by pointer.
grepped 'Required reading' "$SKILLS/run-the-thing/SKILL.md"
grepped 'house-rules' "$SKILLS/run-the-thing/SKILL.md"

# --- the routing table ----------------------------------------------------------
#
# Kept while the permission gate consumes it: the gate reads the rows that
# block, and a deleted table is an adopted block rule failing open.

ROUTING=$PROJECT/.luma/bundles/routing.toml
exists "$ROUTING"
grepped 'policy/stylesheets' "$ROUTING"
grepped 'path:\*\*/\*.css' "$ROUTING"
grepped 'command:git commit' "$ROUTING"
grepped 'matches = \["eager"\]' "$ROUTING"
ungrep 'why-widgets' "$ROUTING"
ungrep '01-first' "$ROUTING"

# --- blocking is compiled, and reported when nothing can honour it --------------

grepped 'on_violation = "block"' "$ROUTING"
case $LAST in *"nothing here enforces"*) ok ;; *) bad "expected apply to say blocking is unenforced here: $LAST" ;; esac

# --- `preload` is reported, never honoured --------------------------------------

cat > "$B/policy/legacy.md" <<'EOF'
---
type: policy
title: Legacy rule
description: Still using the old field.
preload: mandatory
matches: eager
---
Old-style declaration.
EOF

apply 'reports a bundle still using preload' 0
case $LAST in *preload*) ok ;; *) bad "expected apply to report the legacy preload field: $LAST" ;; esac
rm "$B/policy/legacy.md"

# --- a trigger nothing can honour fails loudly ----------------------------------

cat > "$B/policy/needs-approval.md" <<'EOF'
---
type: policy
title: Needs a person
description: Someone has to approve this.

on_violation: require_approval
matches:
  - command: git push
---
Ask first.
EOF

apply 'refuses an intervention it cannot perform' 2
case $LAST in *require_approval*) ok ;; *) bad "expected the unsupported value named: $LAST" ;; esac
rm "$B/policy/needs-approval.md"

# --- an inert trigger is reported -----------------------------------------------

cat > "$B/policy/nonexistent.md" <<'EOF'
---
type: policy
title: Rules for a directory that is not here
description: Governs a place this project does not have.

matches:
  - path: "nowhere-at-all/**"
---
Rules.
EOF

apply 'reports a trigger that matches nothing' 0
case $LAST in *nowhere-at-all*) ok ;; *) bad "expected the inert trigger reported: $LAST" ;; esac
rm "$B/policy/nonexistent.md"

# --- asking by name is the floor, and it does not scale with adoption -----------

exists "$SKILLS/list-bundles/SKILL.md"
exists "$SKILLS/load-bundle/SKILL.md"
grepped 'INDEX.md' "$SKILLS/list-bundles/SKILL.md"
ungrep 'acme/rules' "$SKILLS/list-bundles/SKILL.md"
grepped '.luma/bundles/<bundle-id>/INDEX.md' "$SKILLS/load-bundle/SKILL.md"
ungrep 'acme/rules' "$SKILLS/load-bundle/SKILL.md"

# A procedure named `load-bundle` must not be able to replace the floor.

cat > "$B/procedure/load-bundle.md" <<'EOF'
---
type: procedure
title: Load a bundle
description: Somebody else's idea of loading a bundle.
---
Not the navigation skill.
EOF

apply 'a procedure cannot take a reserved name' 0
grepped 'luma-foreman apply' "$SKILLS/load-bundle/SKILL.md"
exists "$SKILLS/acme-rules-load-bundle/SKILL.md"
rm -f "$B/procedure/load-bundle.md"
apply 'and it goes when the procedure does' 0
absent "$SKILLS/acme-rules-load-bundle"

# --- legacy artifacts from earlier builds are swept -----------------------------
#
# The prototype generated a per-project entrypoint and a rings tree. A stale
# generated artifact that still reads as current is worse than a missing one —
# it names documents by a shape nothing writes any more.

mkdir -p "$PROJECT/.luma/bundles/rings/acme"
printf '<!-- Generated by `luma-foreman apply`. Edits are lost. -->\nold ring\n' \
  > "$PROJECT/.luma/bundles/rings/acme/rules.md"
printf '<!-- Generated by `luma-foreman apply`. Edits are lost. -->\nold entrypoint\n' \
  > "$PROJECT/.luma/bundles/entrypoint.md"

LAST=$(cd "$PROJECT" && "$CLI" apply --check 2>&1); got=$?
[ "$got" -eq 1 ] && ok || bad "check should flag legacy artifacts (exit $got)"
case $LAST in *entrypoint.md*) ok ;; *) bad "check did not name the legacy entrypoint: $LAST" ;; esac

apply 'sweeps legacy artifacts' 0
case $LAST in *legacy*) ok ;; *) bad "expected the sweep reported: $LAST" ;; esac
absent "$PROJECT/.luma/bundles/entrypoint.md"
absent "$PROJECT/.luma/bundles/rings"

# --- a bundle that leaves takes its entry and skills with it --------------------

rm -rf "$B"
apply 'sweeps after a bundle leaves' 0
ungrep 'acme/rules' "$INDEX"
absent "$SKILLS/run-the-thing"

printf '\n%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
