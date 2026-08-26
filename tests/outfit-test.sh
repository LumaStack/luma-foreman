#!/bin/sh
# Tests for how `luma-foreman outfit` derives delivery from what a Document
# declares.
#
#   sh tests/outfit-test.sh
#
# `adopt-test.sh` already covers outfit end to end — that a skill appears, that
# CLAUDE.md is spliced rather than owned, that orphans leave. This file covers
# the part that decides *what* gets written: an author declares `compliance` and
# `matches`, and everything else is computed.
#
# Three classes come out of that computation, and the whole point is that none
# of them is chosen by hand:
#
#   standing     body present before work starts
#   advertised   name and description present, body on match
#   on-demand    neither; findable, not announced
#
# There is exactly one path to standing — `mandatory` with no trigger anyone
# could state — so the expensive outcome is something an author falls into
# rather than selects. Most of these cases exist to hold that line.
#
# Written before the behaviour, so a fresh checkout fails every case below.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

# Hermetic: the operator's own harness wiring must not decide what these cases
# see. Pointing CLAUDE_CONFIG_DIR at an empty directory means the gate reads as
# not installed here, whatever is true of this machine.

T=$(mktemp -d /tmp/outfit.XXXXXX) || exit 2
export CLAUDE_CONFIG_DIR=$T/no-harness
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

exists()  { [ -e "$1" ] && ok || bad "expected to exist: $1"; }
absent()  { [ -e "$1" ] && bad "expected NOT to exist: $1" || ok; }
grepped() { grep -q -- "$1" "$2" 2>/dev/null && ok || bad "expected '$1' in $(basename "$2")"; }
ungrep()  { grep -q -- "$1" "$2" 2>/dev/null && bad "expected '$1' NOT in $(basename "$2")" || ok; }

outfit() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" outfit "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

# --- a project with one bundle written into it ----------------------------------
#
# Written directly rather than adopted. `.luma/bundles/` holds both what a
# project took from a catalog and what it wrote itself, and outfit projects both
# — so this exercises the same path with none of the adoption machinery.

PROJECT=$T/project
B=$PROJECT/.luma/bundles/acme/rules
mkdir -p "$B/policy" "$B/concepts" "$B/_types" \
         "$B/workflows/run-the-thing/steps" "$PROJECT/.claude"
(cd "$PROJECT" && git init -q . 2>/dev/null) || true

cat > "$B/BUNDLE.md" <<'EOF'
---
type: bundle
version: 0.1.0
description: Rules for widget work.
---
EOF

# always-on: it asks for a permanent seat, which is now the only way to get one.
cat > "$B/policy/house-rules.md" <<'EOF'
---
type: policy
title: House rules
description: The rules that govern all work here.
matches: always
---
Everything here is always in force.
EOF

# advertised: mandatory, but it only governs stylesheets.
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

# advertised: a rule with teeth, fired by a command.
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

# on-demand: a concept obliges nothing, so it is never announced.
cat > "$B/concepts/why-widgets.md" <<'EOF'
---
type: document
title: Why widgets
description: Background on why widgets exist.
compliance: optional
---
Rationale.
EOF

# a workflow that owns a directory, and the steps it owns.
cat > "$B/workflows/run-the-thing/WORKFLOW.md" <<'EOF'
---
type: workflow
title: Run the thing
description: Run the thing. Use when the thing needs running.
---
Step one, step two.
EOF

cat > "$B/workflows/run-the-thing/steps/01-first.md" <<'EOF'
---
type: acme/step
title: First step
---
Do the first bit.
EOF

cat > "$B/workflows/run-the-thing/steps/02-second.md" <<'EOF'
---
type: acme/step
title: Second step
---
Do the second bit.
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
SKILLS=$PROJECT/.claude/skills

outfit 'projects a bundle written in place' 0

# --- standing: the one path to always-loaded ------------------------------------
#
# `mandatory` with no trigger is the only way a body reaches the session up
# front, and it has to actually arrive rather than be recommended. A list of
# paths under a heading saying "read these first" is a suggestion; delivery is
# the claim `mandatory` makes.

grepped 'house-rules' "$CLAUDE"
grepped '@.luma/bundles/acme/rules/policy/house-rules.md' "$CLAUDE"

# --- advertised: named up front, body withheld ----------------------------------
#
# A rule that governs stylesheets should be reachable the moment stylesheets are
# touched, and cost nothing before then. Its description is the routing entry;
# importing its body would charge every session for a rule most never hit.

grepped 'stylesheets' "$CLAUDE"
ungrep '@.luma/bundles/acme/rules/policy/stylesheets.md' "$CLAUDE"
grepped 'no-credentials' "$CLAUDE"
ungrep '@.luma/bundles/acme/rules/policy/no-credentials.md' "$CLAUDE"

# --- on-demand background: not announced at all ---------------------------------
#
# A concept obliges nothing. Announcing it spends the index on something no
# consumer is ever obliged to read, and it is reached through the rules and
# procedures that do act. A *policy* matching nothing is a different case and is
# still listed — see below — because a rule nobody can see governs nothing.

ungrep 'why-widgets' "$CLAUDE"

# --- subordination, which is the leak this exists to close ----------------------
#
# The steps under a workflow's directory belong to that workflow. They are
# reachable only through it, and the observed failure is that they were listed
# individually — one adopted bundle put twenty-one step titles into every
# session before anybody noticed.

ungrep '01-first' "$CLAUDE"
ungrep '02-second' "$CLAUDE"
absent "$SKILLS/01-first"
absent "$SKILLS/02-second"

# --- the workflow itself, and the name its directory gives it -------------------
#
# The owner of a document directory is the all-caps markdown file in it. The
# casing is the signal rather than any particular word, so a policy with
# diagrams gets POLICY.md and somebody's own type gets its own — nothing is
# centrally reserved, which matters because the type vocabulary is open.
#
# Borrowed from SKILL.md deliberately: anyone who has seen one reads this
# correctly with nothing to learn. A workflow is a skill that travels across
# harnesses and carries more, so it cannot take the name — but it can take the
# shape.
#
# The directory remains the identity. The document is `workflows/run-the-thing`,
# and WORKFLOW.md is visible only to somebody already standing in the directory.

exists "$SKILLS/run-the-thing/SKILL.md"
grepped 'name: run-the-thing' "$SKILLS/run-the-thing/SKILL.md"
grepped 'Use when the thing needs running' "$SKILLS/run-the-thing/SKILL.md"

# The adapter stays thin — a pointer, never a copy. A copy is a second source of
# truth, and it charges every firing for content the pointer costs nothing to
# reach.
ungrep 'Step one, step two' "$SKILLS/run-the-thing/SKILL.md"
grepped '.luma/bundles/acme/rules/workflows/run-the-thing' "$SKILLS/run-the-thing/SKILL.md"

# --- the routing table ----------------------------------------------------------
#
# Every Document with a trigger gets a row: when it fires and what happens. The
# gate reads the rows that block; a router will read the rest. Compiling it once
# is what keeps those two from drifting — and the gate cannot walk the bundles
# itself, because it runs before every tool call against a budget in
# milliseconds.

ROUTING=$PROJECT/.luma/bundles/routing.toml
exists "$ROUTING"
grepped 'policy/stylesheets' "$ROUTING"
grepped 'path:\*\*/\*.css' "$ROUTING"
grepped 'command:git commit' "$ROUTING"

# A Document that matches always earns a row saying so — it is a routing fact
# like any other, and the gate ignores it because no `always` entry names a
# command. What earns no row is a Document that matches nothing: there is
# nothing to route.
grepped 'house-rules' "$ROUTING"
grepped 'matches = \["always"\]' "$ROUTING"
ungrep 'why-widgets' "$ROUTING"

# Subordinate documents are invisible here too — they arrive with their owner.
ungrep '01-first' "$ROUTING"

# --- blocking is compiled, and reported when nothing can honour it --------------
#
# Declaring `block` where no gate is installed is a rule that reads as enforced
# and is not. Saying so is the difference between a guardrail and a label.

cat > "$B/policy/no-force-push.md" <<'EOF'
---
type: policy
title: Never force-push a shared branch
description: Force-pushing a shared branch destroys other people's work.

on_violation: block
matches:
  - command: git push --force
---
Do not force-push.
EOF

outfit 'compiles a blocking rule' 0
grepped 'no-force-push' "$ROUTING"
grepped 'on_violation = "block"' "$ROUTING"
case $LAST in *"nothing here enforces"*) ok ;; *) bad "expected outfit to say blocking is unenforced here: $LAST" ;; esac

# --- `preload` is reported, never honoured --------------------------------------
#
# The field it replaces has to stop working loudly. Honouring it during a
# transition means a half-migrated bundle behaves correctly and nobody finds
# out; reporting it means the migration cannot stall silently.

cat > "$B/policy/legacy.md" <<'EOF'
---
type: policy
title: Legacy rule
description: Still using the old field.
preload: mandatory
matches: always
---
Old-style declaration.
EOF

outfit 'reports a bundle still using preload' 0
case $LAST in *preload*) ok ;; *) bad "expected outfit to report the legacy preload field: $LAST" ;; esac

# It *is* imported — but not because `preload` was read. It says
# `matches: always`, which is the one route to being loaded up front. The old
# field is reported and otherwise ignored, so a half-migrated bundle cannot
# behave correctly and stall there forever.
grepped '@.luma/bundles/acme/rules/policy/legacy.md' "$CLAUDE"

# --- a trigger nothing can honour fails loudly ----------------------------------
#
# The first build has no degradation paths. A declared intervention the harness
# cannot perform is an error, not a quiet downgrade to the nearest thing that
# works — silently becoming `warn` is the failure this design exists to remove,
# arriving inside the design itself.

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

outfit 'refuses an intervention it cannot perform' 2
case $LAST in *require_approval*) ok ;; *) bad "expected the unsupported value named: $LAST" ;; esac

rm "$B/policy/needs-approval.md" "$B/policy/legacy.md"

# --- an inert trigger is reported -----------------------------------------------
#
# A glob matching nothing in this project never fires, and that is
# indistinguishable from a rule that has simply not come up yet. Both look like
# silence. Saying so is the difference between a rule that does not apply and a
# rule nobody will ever see.

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

outfit 'reports a trigger that matches nothing' 0
case $LAST in *nowhere-at-all*) ok ;; *) bad "expected the inert trigger reported: $LAST" ;; esac

printf '\n%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
