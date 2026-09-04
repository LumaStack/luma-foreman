#!/bin/sh
# Tests for `luma-foreman remove`.
#
#   sh tests/remove-test.sh
#
# Every case builds a throwaway catalog and a throwaway project, so these assert
# what the command actually does to a filesystem. Nothing here reads the real
# catalog or the machine's own repositories.
#
# The load-bearing cases are the refusals, and specifically *which* refusal
# fires. The guard keys on recoverability rather than on where a bundle came
# from, so the cases that matter are the four states of that table: a vendored
# copy the catalog can restore, a local bundle git can restore, a local bundle
# nothing holds, and a vendored copy whose edits nothing holds. Getting the
# wrong one of those destroys somebody's work.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/remove.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

has()   { case $LAST in *"$1"*) ok ;; *) bad "expected output to contain '$1': $LAST" ;; esac; }
lacks() { case $LAST in *"$1"*) bad "expected output NOT to contain '$1': $LAST" ;; *) ok ;; esac; }
exists() { [ -e "$1" ] && ok || bad "expected to exist: $1"; }
absent() { [ -e "$1" ] && bad "expected NOT to exist: $1" || ok; }
grepped() {
  grep -q "$1" "$2" 2>/dev/null && ok || bad "expected '$1' in $2"
}
ungrepped() {
  grep -q "$1" "$2" 2>/dev/null && bad "expected NO '$1' in $2" || ok
}

# remove <label> <expect-exit> <args...>
remove() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" remove "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

commit_all() {
  git -C "$PROJECT" add -A
  GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com \
  GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
    git -C "$PROJECT" commit -q -m "$1" >/dev/null 2>&1 || true
}

# --- a catalog and a project ----------------------------------------------------

CATALOG=$T/catalog
mkdir -p "$CATALOG/catalog/bundles/widgets/policy"

cat > "$CATALOG/catalog/CATALOG.md" <<'EOF'
---
type: luma/catalog
namespace: acme
description: A catalog with one bundle in it.
---
EOF

cat > "$CATALOG/catalog/bundles/widgets/BUNDLE.md" <<'EOF'
---
type: bundle
version: 0.1.0
description: Everything about widgets.
---
EOF

cat > "$CATALOG/catalog/bundles/widgets/policy/widget-rules.md" <<'EOF'
---
type: policy
title: Widget rules
description: What a widget may and may not be.
---
Rules go here.
EOF

git -C "$CATALOG" init -q
git -C "$CATALOG" add -A
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com \
GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
  git -C "$CATALOG" commit -q -m first

PROJECT=$T/project
mkdir -p "$PROJECT"
git -C "$PROJECT" init -q
(cd "$PROJECT" && "$CLI" init >/dev/null 2>&1)

MANIFEST=$PROJECT/.luma/bundles/MANIFEST.md
VENDORED=$PROJECT/.luma/bundles/acme/widgets
LOCAL=$PROJECT/.luma/bundles/local/gadgets

# --- the shape of the command ---------------------------------------------------

remove 'help exits 0' 0 --help
has 'luma-foreman remove'
has 'Exit codes'

remove 'unknown option is could-not-run' 2 --nonsense
has 'unknown option'

remove 'no operand is could-not-run' 2
has 'usage:'

remove 'unknown bundle is could-not-run' 2 nothing-here
has 'not recorded'

# --- a bundle written here, never committed -------------------------------------
# Nothing holds it: not git, and no catalog. This is the one genuinely
# destructive removal, and it is the one that must refuse.

(cd "$PROJECT" && "$CLI" bundle new gadgets >/dev/null 2>&1)
exists "$LOCAL/BUNDLE.md"

remove 'uncommitted local refuses' 1 gadgets
has 'uncommitted work'
has 'Nothing else holds it'
has '--force'
exists "$LOCAL/BUNDLE.md"
grepped 'local/gadgets' "$MANIFEST"

# --- ...and --force is the way past it ------------------------------------------

remove 'uncommitted local yields to --force' 0 gadgets --force
has 'removed'
has 'not recoverable'
absent "$LOCAL"
ungrepped 'local/gadgets' "$MANIFEST"

# --- a bundle written here and committed ----------------------------------------
# git holds it, so removing is recoverable and says how.

(cd "$PROJECT" && "$CLI" bundle new gadgets >/dev/null 2>&1)
commit_all 'add gadgets'

remove 'committed local removes' 0 gadgets
has 'removed  local/gadgets'
has 'it was committed'
has 'git checkout HEAD --'
absent "$LOCAL"
ungrepped 'local/gadgets' "$MANIFEST"

# The recovery line has to be true, not decorative.
git -C "$PROJECT" checkout -q HEAD -- .luma/bundles/local/gadgets
exists "$LOCAL/BUNDLE.md"
git -C "$PROJECT" checkout -q HEAD -- .luma/bundles/MANIFEST.md

# --- a vendored copy, unedited --------------------------------------------------
# The catalog holds it byte-identical, so this is the cheapest removal there is.

(cd "$PROJECT" && "$CLI" get acme/widgets --from "$CATALOG" >/dev/null 2>&1)
exists "$VENDORED/BUNDLE.md"
commit_all 'adopt widgets'

remove 'vendored clean removes' 0 acme/widgets
has 'the catalog has it'
has 'luma-foreman get acme/widgets'
absent "$VENDORED"
ungrepped 'acme/widgets' "$MANIFEST"

# --- a vendored copy somebody edited --------------------------------------------
# Nothing holds the edits — the catalog has the unedited bundle, and this copy
# is no longer it. Same danger class as an uncommitted local bundle.

(cd "$PROJECT" && "$CLI" get acme/widgets --from "$CATALOG" >/dev/null 2>&1)
commit_all 'adopt widgets again'
echo 'edited here' >> "$VENDORED/policy/widget-rules.md"

remove 'edited vendored refuses' 1 acme/widgets
has 'edited here'
has '--force'
exists "$VENDORED/BUNDLE.md"

remove 'edited vendored yields to --force' 0 acme/widgets --force
absent "$VENDORED"

# --- an entry with nothing behind it --------------------------------------------
# Dropping a receipt for something that is not there is repair, not removal, so
# it never refuses whatever the guard would have said about missing content.

(cd "$PROJECT" && "$CLI" get acme/widgets --from "$CATALOG" >/dev/null 2>&1)
rm -rf "$VENDORED"

remove 'missing copy drops the entry' 0 acme/widgets
has 'entry dropped'
ungrepped 'acme/widgets' "$MANIFEST"

# --- a bare name that two namespaces answer to ----------------------------------
# Two bundles legitimately sharing a name is when the guess must stop.

(cd "$PROJECT" && "$CLI" get acme/widgets --from "$CATALOG" >/dev/null 2>&1)
(cd "$PROJECT" && "$CLI" bundle new widgets >/dev/null 2>&1)

remove 'ambiguous bare name refuses to guess' 2 widgets
has 'ambiguous'
exists "$VENDORED/BUNDLE.md"

remove 'fully qualified resolves it' 0 acme/widgets
absent "$VENDORED"

# --- something still pointing at it ---------------------------------------------
# Removing a bundle turns anything citing it into a dangling reference. A
# warning before is worth more than a finding that never comes — `inspect`
# catches a dangling wikilink, and a bundle cited as a bare path in prose is
# exactly what it does not catch.

mkdir -p "$PROJECT/docs"
echo 'See .luma/bundles/local/widgets for the rules.' > "$PROJECT/docs/notes.md"
commit_all 'a document citing the bundle'

remove 'a cited bundle reports what breaks' 1 local/widgets
has 'still name it'
has 'docs/notes.md'
absent "$PROJECT/.luma/bundles/local/widgets"

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
