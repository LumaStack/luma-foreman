#!/bin/sh
# `luma-foreman lint` — the LKF Validation table, implemented as its own
# command. The properties worth holding: validation never rejects by default,
# --strict escalates only what the table says it may, unknown fields and
# undefined types are never reported, and type_version currency stays info in
# every mode — old-but-labelled is the system working.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/lint-test.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

LAST=
run() {
  label=$1 want=$2 dir=$3; shift 3
  LAST=$("$CLI" lint "$@" "$dir" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}
has()   { case $LAST in *"$1"*) ok ;; *) bad "expected output to contain '$1'" ;; esac; }
lacks() { case $LAST in *"$1"*) bad "expected output to lack '$1'" ;; *) ok ;; esac; }

# One tree per case, built fresh: a root-level type store and documents under
# it — the directory-root resolution the LKF roadmap tracks, and the shape
# clarify already uses.
fixture() {
  d=$T/$1
  mkdir -p "$d/type_definitions/widget" "$d/records"
  cat > "$d/type_definitions/widget/DEFINITION.md" <<'EOF'
---
type: type_definition
type_version: "0.0.1"
defines: widget
version: "0.2.0"
fields:
  name: { field_presence: required, field_type: text }
  size: { field_presence: optional, field_type: enum, values: [small, large] }
  seen: { field_presence: recommended, field_type: date }
  old:  { field_presence: deprecated, field_type: text }
---
x
EOF
  printf '# Changelog\n## 0.2.0\n- x\n' > "$d/type_definitions/widget/CHANGELOG.md"
  printf '%s' "$d"
}

# --- a conforming document is quiet ----------------------------------------------

# Not asserted as 'clean': the fixture definition is itself a document, and
# the built-in chain reports its missing recommended title/modified as info —
# which is the one-engine design working, not noise to fixture away.
d=$(fixture clean)
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nname: fine\nseen: 2026-09-20\n---\nx\n' > "$d/records/a.md"
run 'a conforming document' 0 "$d"
lacks 'warning'
lacks 'error'

# --- the table, row by row --------------------------------------------------------

d=$(fixture required)
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nseen: 2026-09-20\n---\nx\n' > "$d/records/a.md"
run 'missing required is a warning, never a rejection' 0 "$d"
has 'missing required field `name`'
run 'strict escalates missing required' 1 "$d" --strict
has 'error'

d=$(fixture enum)
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nname: n\nseen: 2026-09-20\nsize: gigantic\n---\nx\n' > "$d/records/a.md"
run 'an enum value not listed' 0 "$d"
has 'not among'
run 'strict escalates the enum row' 1 "$d" --strict

d=$(fixture shape)
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nname: n\nseen: yesterday\n---\nx\n' > "$d/records/a.md"
run 'a value that does not look like its field_type' 0 "$d"
has 'does not look like date'

# Deprecated stays a warning even under --strict — still valid, just
# discouraged — so on its own it never fails a run.
d=$(fixture deprecated)
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nname: n\nseen: 2026-09-20\nold: y\n---\nx\n' > "$d/records/a.md"
run 'deprecated is a warning' 0 "$d"
has 'deprecated'
run 'deprecated does not escalate' 0 "$d" --strict
has 'warning'
lacks 'error'

# Unknown fields and undefined types: never reported — the permissive
# conformance law.
d=$(fixture openworld)
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nname: n\nseen: 2026-09-20\nextra_field: y\n---\nx\n' > "$d/records/a.md"
printf -- '---\ntype: mystery\nwhatever: y\n---\nx\n' > "$d/records/b.md"
run 'unknown fields and undefined types are never reported' 0 "$d"
lacks 'warning'
lacks 'extra_field'
lacks 'mystery'

# --- currency: the check the migration bought -------------------------------------

d=$(fixture currency)
printf -- '---\ntype: widget\ntype_version: "0.1.0"\nname: n\nseen: 2026-09-20\n---\nx\n' > "$d/records/a.md"
run 'stale type_version is hidden info by default' 0 "$d"
lacks 'written against'
has 'info is hidden'
run 'verbose lists the stale citation' 0 "$d" --verbose
has 'written against widget 0.1.0'
has 'definition is at 0.2.0'
run 'currency never escalates' 0 "$d" --strict

# --- what generic validation cannot see: layout ------------------------------------

d=$(fixture layout)
printf -- '---\ntype: type_definition\ndefines: stray\n---\nx\n' > "$d/type_definitions/stray.md"
run 'the single-file shape is retired' 0 "$d"
has 'single-file shape was'
run 'strict escalates a resolution-breaking shape' 1 "$d" --strict

d=$(fixture nochangelog)
rm "$d/type_definitions/widget/CHANGELOG.md"
run 'a contract without a changelog' 0 "$d"
has 'no CHANGELOG.md'
run 'the changelog warning does not escalate' 0 "$d" --strict

d=$(fixture mismatch)
mkdir -p "$d/type_definitions/thing"
printf -- '---\ntype: type_definition\ndefines: other\nversion: "0.0.1"\n---\nx\n' > "$d/type_definitions/thing/DEFINITION.md"
printf '# c\n' > "$d/type_definitions/thing/CHANGELOG.md"
run 'a folder not named for its type' 0 "$d"
has 'resolution never finds this contract'

d=$(fixture empty)
mkdir -p "$d/type_definitions/hollow"
run 'a type folder with no DEFINITION.md' 0 "$d"
has 'no DEFINITION.md'

# --- what generic validation cannot see: the fields grammar ------------------------

d=$(fixture grammar)
mkdir -p "$d/type_definitions/loose"
cat > "$d/type_definitions/loose/DEFINITION.md" <<'EOF'
---
type: type_definition
defines: loose
version: "0.0.1"
fields:
  - name: a_field
    obligation: required
---
x
EOF
printf '# c\n' > "$d/type_definitions/loose/CHANGELOG.md"
run 'list-shaped fields validate nothing, and say so' 0 "$d"
has 'declares a mapping'

d=$(fixture enumvalues)
mkdir -p "$d/type_definitions/mood"
cat > "$d/type_definitions/mood/DEFINITION.md" <<'EOF'
---
type: type_definition
defines: mood
version: "0.0.1"
fields:
  level: { field_presence: optional, field_type: enum }
---
x
EOF
printf '# c\n' > "$d/type_definitions/mood/CHANGELOG.md"
run 'an enum with no values' 0 "$d"
has 'enum with no `values`'

# --- what generic validation cannot see: relations ---------------------------------

d=$(fixture orphanparent)
mkdir -p "$d/type_definitions/child"
printf -- '---\ntype: type_definition\ndefines: child\nversion: "0.0.1"\nextends: nowhere\n---\nx\n' > "$d/type_definitions/child/DEFINITION.md"
printf '# c\n' > "$d/type_definitions/child/CHANGELOG.md"
run 'extends that resolves to nothing' 0 "$d"
has 'resolves to nothing'
run 'strict escalates a broken definition' 1 "$d" --strict

d=$(fixture weakened)
mkdir -p "$d/type_definitions/loosewidget"
cat > "$d/type_definitions/loosewidget/DEFINITION.md" <<'EOF'
---
type: type_definition
defines: loosewidget
version: "0.0.1"
extends: widget
fields:
  name: { field_presence: optional }
  seen: { field_presence: recommended, field_type: text }
---
x
EOF
printf '# c\n' > "$d/type_definitions/loosewidget/CHANGELOG.md"
run 'inheritance is add-only, presence never weakened' 0 "$d"
has 'weakens presence'
has 'restates field_type'

# --- the built-ins ship with the tool ----------------------------------------------

d=$T/builtin; mkdir -p "$d"
printf -- '---\ntype: bundle\ntitle: t\ndescription: d\n---\nx\n' > "$d/BUNDLE.md"
printf -- '---\ntype: policy\ntitle: t\non_violation: shrug\n---\nx\n' > "$d/p.md"
run 'built-in contracts validate without vendoring' 0 "$d"
has 'missing required field `version` (bundle)'
has 'not among'

# --- resolution walks up to the root, not just one bundle --------------------------

d=$(fixture chain)
mkdir -p "$d/deep/nested"
printf -- '---\ntype: widget\ntype_version: "0.2.0"\nseen: 2026-09-20\n---\nx\n' > "$d/deep/nested/a.md"
run 'a nested document resolves the root store' 0 "$d"
has 'missing required field `name`'

# --- refusals ----------------------------------------------------------------------

LAST=$("$CLI" lint "$T/does-not-exist" 2>&1); got=$?
[ "$got" -eq 2 ] && ok || bad "a missing directory should refuse (2): $LAST"
LAST=$("$CLI" lint --nonsense 2>&1); got=$?
[ "$got" -eq 2 ] && ok || bad "an unknown flag should refuse (2): $LAST"

printf '\n%s passed, %s failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
