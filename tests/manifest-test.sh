#!/bin/sh
# Tests for the manifest — MANIFEST.md as the record, the legacy adopted.toml
# fallback, and the migration between them.
#
#   sh tests/manifest-test.sh
#
# The properties worth holding: the legacy file is still read where no
# manifest exists (a receipt that quietly stopped being read fails open); any
# write completes the migration; the line grammar round-trips byte-stably (a
# canonical file rewritten is the same file); and intent (`register:`)
# survives a rewrite, because a fact the tool drops on rewrite is a fact the
# file never really held.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/manifest.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }
grepped() { grep -q -- "$1" "$2" 2>/dev/null && ok || bad "expected '$1' in $(basename "$2")"; }
ungrep()  { grep -q -- "$1" "$2" 2>/dev/null && bad "expected '$1' NOT in $(basename "$2")" || ok; }

P=$T/proj
mkdir -p "$P/.luma/bundles/org/thing"
cat > "$P/.luma/bundles/org/thing/BUNDLE.md" <<'EOF'
---
type: bundle
title: org/thing
version: 1.2.0
description: A vendored fixture.
---
EOF

M=$P/.luma/bundles/MANIFEST.md
L=$P/.luma/bundles/adopted.toml

# -- legacy fallback ----------------------------------------------------------

cat > "$L" <<'EOF'
["org/thing"]
version  = "1.2.0"
source   = "https://catalog.invalid/example"
commit   = "1111111111111111111111111111111111111111"
checksum = "sha256:2222222222222222222222222222222222222222222222222222222222222222"
EOF

OUT=$( cd "$P" && "$CLI" bundle list )
printf '%s\n' "$OUT" | grep -q 'thing' && ok || bad "legacy adopted.toml should still be read by bundle list"

# -- migration ----------------------------------------------------------------

( cd "$P" && "$CLI" bundle migrate-manifest ) > "$T/migrate.out" 2>&1
[ $? -eq 0 ] && ok || bad "migrate-manifest should exit 0"
grepped 'retired adopted.toml' "$T/migrate.out"
[ -f "$M" ] && ok || bad "MANIFEST.md should exist after migration"
[ -f "$L" ] && bad "adopted.toml should be gone after migration" || ok

grepped 'Written by `luma-foreman`' "$M"
grepped '# Bundles' "$M"
grepped '- `org/thing` 1.2.0' "$M"
grepped '  - source: https://catalog.invalid/example' "$M"
grepped '  - commit: 1111111111111111111111111111111111111111' "$M"
grepped '  - sha256: 2222222222222222222222222222222222222222222222222222222222222222' "$M"
ungrep  'register:' "$M"
ungrep  'sha256:sha256' "$M"

# The record reads back identically through the new file.
OUT=$( cd "$P" && "$CLI" bundle show org/thing )
printf '%s\n' "$OUT" | grep -q 'https://catalog.invalid/example' && ok || bad "bundle show should read the manifest"

# -- round-trip stability -----------------------------------------------------

cp "$M" "$T/first"
( cd "$P" && "$CLI" bundle migrate-manifest ) >/dev/null 2>&1
cmp -s "$M" "$T/first" && ok || bad "a canonical manifest rewritten should be byte-identical"

# -- intent survives a rewrite ------------------------------------------------

printf '  - register: nothing\n' >> "$M"
( cd "$P" && "$CLI" bundle migrate-manifest ) >/dev/null 2>&1
grepped '  - register: nothing' "$M"

# And a second rewrite of that state is stable too.
cp "$M" "$T/second"
( cd "$P" && "$CLI" bundle migrate-manifest ) >/dev/null 2>&1
cmp -s "$M" "$T/second" && ok || bad "register-carrying manifest should rewrite byte-identically"

# -- a name-indirect receipt survives a rewrite -------------------------------
#
# `catalog:` records the registered catalog by name; the registry in the
# project config owns name-to-URL. An unrecoverable fact the tool dropped on
# rewrite is a fact the file never really held.

printf '  - catalog: corp/kit\n' >> "$M"
( cd "$P" && "$CLI" bundle migrate-manifest ) >/dev/null 2>&1
grepped '  - catalog: corp/kit' "$M"
cp "$M" "$T/third"
( cd "$P" && "$CLI" bundle migrate-manifest ) >/dev/null 2>&1
cmp -s "$M" "$T/third" && ok || bad "catalog-carrying manifest should rewrite byte-identically"

# -- bare entries: a bundle written here --------------------------------------

mkdir -p "$P/.luma/bundles/org/local"
cat > "$P/.luma/bundles/org/local/BUNDLE.md" <<'EOF'
---
type: bundle
title: org/local
version: 0.1.0
description: Written here.
---
EOF
printf -- '- `org/local` 0.1.0\n' >> "$M"
( cd "$P" && "$CLI" bundle migrate-manifest ) >/dev/null 2>&1
grepped '`org/local` 0.1.0' "$M"
OUT=$( cd "$P" && "$CLI" bundle list )
printf '%s\n' "$OUT" | grep -q 'local' && ok || bad "a bare entry should appear in bundle list"

# -- set and unset record intent; apply performs it later ---------------------
#
# set writes a field's line, unset removes it, and absence is the default —
# the same shape as the manifest's own divergence-only grammar. The fixture
# still carries register: nothing from the round-trip section, so restoring
# the default comes first and asserts the transition.

OUT=$( cd "$P" && "$CLI" bundle unset thing register 2>&1 ); got=$?
[ "$got" -eq 0 ] && ok || bad "unset by bare name should exit 0: $OUT"
ungrep 'register:' "$M"

OUT=$( cd "$P" && "$CLI" bundle set thing register nothing 2>&1 ); got=$?
[ "$got" -eq 0 ] && ok || bad "set by bare name should exit 0: $OUT"
printf '%s\n' "$OUT" | grep -q 'luma-foreman apply' && ok || bad "set should point at apply"
grepped '  - register: nothing' "$M"

OUT=$( cd "$P" && "$CLI" bundle set org/thing register nothing 2>&1 )
printf '%s\n' "$OUT" | grep -q 'nothing to do' && ok || bad "setting the same intent twice should be a no-op"

OUT=$( cd "$P" && "$CLI" bundle unset org/thing register 2>&1 ); got=$?
[ "$got" -eq 0 ] && ok || bad "unset by full ID should exit 0: $OUT"
ungrep 'register:' "$M"

OUT=$( cd "$P" && "$CLI" bundle set org/thing register everywhere 2>&1 ); got=$?
[ "$got" -eq 2 ] && ok || bad "an unknown value should be refused (2)"

OUT=$( cd "$P" && "$CLI" bundle set org/thing lifecycle draft 2>&1 ); got=$?
[ "$got" -eq 2 ] && ok || bad "an unknown field should be refused (2)"

OUT=$( cd "$P" && "$CLI" bundle set org/absent register nothing 2>&1 ); got=$?
[ "$got" -eq 2 ] && ok || bad "an unrecorded bundle should be refused (2)"

# Two bundles sharing a bare name: the guess must stop, and the error says
# to use the fully qualified form rather than picking a side silently.
printf -- '- `other/thing` 2.0.0\n' >> "$M"
OUT=$( cd "$P" && "$CLI" bundle set thing register nothing 2>&1 ); got=$?
[ "$got" -eq 2 ] && ok || bad "an ambiguous bare name should be refused (2)"
printf '%s\n' "$OUT" | grep -q 'fully qualified' && ok || bad "the ambiguity error should say fully qualified: $OUT"
OUT=$( cd "$P" && "$CLI" bundle set other/thing register nothing 2>&1 ); got=$?
[ "$got" -eq 0 ] && ok || bad "the full ID should resolve past the ambiguity: $OUT"
grep -v '`other/thing`' "$M" | grep -v '^  - register: nothing$' > "$M.tmp" && grep -q 'org/thing' "$M.tmp" && mv "$M.tmp" "$M"
( cd "$P" && "$CLI" bundle migrate-manifest >/dev/null 2>&1 )

# -- nothing to migrate -------------------------------------------------------

Q=$T/empty
mkdir -p "$Q"
OUT=$( cd "$Q" && "$CLI" bundle migrate-manifest 2>&1 )
printf '%s\n' "$OUT" | grep -q 'nothing recorded' && ok || bad "empty project should say nothing recorded"
[ -f "$Q/.luma/bundles/MANIFEST.md" ] && bad "no manifest should be created for an empty project" || ok

printf '%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
