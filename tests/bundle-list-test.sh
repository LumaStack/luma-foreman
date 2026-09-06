#!/bin/sh
# Tests for what `luma-foreman bundle list` and `catalog show` report about state.
#
#   sh tests/bundle-list-test.sh
#
# Every case builds a throwaway catalog and project, so these assert what the
# commands actually print rather than what they were meant to.
#
# The load-bearing cases are agreement and suppression. The four marks are
# shared between two commands that see the same bundles from opposite sides, and
# the failure that hides best is those two answering differently about one
# bundle — `catalog show` called a bundle whose directory had been deleted
# "taken and applied", because it asked the manifest and never asked the disk.
# The other half is that a legend only explains marks that are on the screen: a
# key listing states nothing is in is a key people stop reading.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/bundlelist.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

has()   { case $LAST in *"$1"*) ok ;; *) bad "expected output to contain '$1': $LAST" ;; esac; }
lacks() { case $LAST in *"$1"*) bad "expected output NOT to contain '$1': $LAST" ;; *) ok ;; esac; }

# list <label> <expect-exit>
list() {
  label=$1 want=$2
  LAST=$(cd "$PROJECT" && "$CLI" bundle list 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

catshow() {
  label=$1 want=$2
  LAST=$(cd "$PROJECT" && "$CLI" catalog show "$CATALOG" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

# --- a catalog with one bundle of each posture -----------------------------------

CATALOG=$T/catalog
mkdir -p "$CATALOG/catalog/bundles"
cat > "$CATALOG/catalog/CATALOG.md" <<'EOF'
---
type: luma/catalog
namespace: acme
description: Four bundles.
---
EOF

# widgets and gears take the default posture; nuts is eager; bolts is silent.
for b in widgets gears; do
  mkdir -p "$CATALOG/catalog/bundles/$b/procedure"
  printf -- '---\ntype: bundle\nversion: 1.0.0\ndescription: The %s bundle.\n---\n' "$b" \
    > "$CATALOG/catalog/bundles/$b/BUNDLE.md"
  printf -- '---\ntype: procedure\ntitle: Do %s\ndescription: Do it.\n---\nx\n' "$b" \
    > "$CATALOG/catalog/bundles/$b/procedure/do-$b.md"
done
mkdir -p "$CATALOG/catalog/bundles/nuts/procedure" "$CATALOG/catalog/bundles/bolts"
printf -- '---\ntype: bundle\nversion: 1.0.0\nmatches: eager\ndescription: Required.\n---\n' \
  > "$CATALOG/catalog/bundles/nuts/BUNDLE.md"
printf -- '---\ntype: procedure\ntitle: Do nuts\ndescription: Do it.\n---\nx\n' \
  > "$CATALOG/catalog/bundles/nuts/procedure/do-nuts.md"
printf -- '---\ntype: bundle\nversion: 1.0.0\nmatches: nothing\ndescription: Silent.\n---\n' \
  > "$CATALOG/catalog/bundles/bolts/BUNDLE.md"

git -C "$CATALOG" init -q
git -C "$CATALOG" add -A
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com \
GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
  git -C "$CATALOG" commit -q -m first

PROJECT=$T/project
mkdir -p "$PROJECT"
git -C "$PROJECT" init -q
(cd "$PROJECT" && "$CLI" init >/dev/null 2>&1)
for b in widgets gears nuts bolts; do
  (cd "$PROJECT" && "$CLI" get "acme/$b" --from "$CATALOG" >/dev/null 2>&1)
done

# --- adopted and never applied ---------------------------------------------------
# Everything is here and nothing reaches an agent. One state, so one legend line.

list 'unapplied is not a failure' 0
has '◐'
has 'adopted, not applied'
has 'luma-foreman apply'
lacks '⊘'
lacks 'turned off'

# Posture is read from each bundle's own matcher, not guessed — and shown only
# where it is not the default. Nineteen rows saying `offered` is the word
# becoming wallpaper, and `eager`, the posture that costs something in every
# session, was the one lost among them. The `·` attaches the tag to the row
# rather than to the skill count beside it.
has '· eager'
has '· standby'
lacks 'offered'

# Rows are tied to the heading above them, last one closing the group.
has '├─'
has '└─'

# Counted in words rather than with a `(s)` that makes the reader do the work.
has 'bundles'
lacks 'bundle(s)'

# The count is what a bundle holds, and says so in the singular where it is one.
has '1 skill'

# --- wired -----------------------------------------------------------------------

(cd "$PROJECT" && "$CLI" apply >/dev/null 2>&1)

list 'a healthy project is quiet' 0
has '●'
# No state needs explaining, so nothing is explained. This is the assertion that
# stops the legend becoming permanent furniture.
lacks 'adopted, not applied'
lacks 'turned off'
lacks 'not on disk'

# --- turned off ------------------------------------------------------------------
# Deliberate, so it is not reported as a failure and does not change the exit code.

(cd "$PROJECT" && "$CLI" bundle set acme/gears register nothing >/dev/null 2>&1)

list 'turned off is a choice, not a fault' 0
has '⊘'
has 'turned off'
has 'bundle set acme/gears register'

# --- gone from disk --------------------------------------------------------------

rm -rf "$PROJECT/.luma/bundles/acme/bolts"

list 'a missing copy is reported and fails' 1
has '○'
has 'recorded, not on disk'
has 'luma-foreman get acme/bolts'

# --- the two commands must agree -------------------------------------------------
# bolts is recorded, and not on disk. Browsing the catalog has to say the same
# thing as listing the project, or one of them is lying about the same bundle.

catshow 'catalog show agrees about a deleted copy' 0
has '○ bolts'
has 'not taken'
lacks '● bolts'

# ...and about one turned off, which it used to report as merely not applied.
has '⊘ gears'
has 'taken, turned off'

# --- an edited copy is not an unapplied one --------------------------------------
# Both are `◐`, deliberately — each means *look at this*. The remedy differs, and
# offering `apply` to somebody whose copy is applied and edited does nothing.

(cd "$PROJECT" && "$CLI" get acme/bolts --from "$CATALOG" >/dev/null 2>&1)
(cd "$PROJECT" && "$CLI" apply >/dev/null 2>&1)
echo 'drifted' >> "$PROJECT/.luma/bundles/acme/widgets/procedure/do-widgets.md"

list 'drift gets the remedy for drift' 1
has '◐'
has 'not as recorded'
has 'inspect --rule adoption'
lacks 'adopted, not applied'

# --- ◐ is a residual, not a pair of conditions -----------------------------------
# Asserted below the CLI because no unnamed state exists to drive it through one,
# which is exactly why it would rot unnoticed. The failure direction is the whole
# point: enumerating the bad states and calling everything else healthy means a
# condition nobody thought of reports as ●, and a bundle broken in a new way
# claiming to work is the reading that costs most.

MARK=$(cd "$ROOT" && python3 -c "import sys; sys.path.insert(0,'src'); from foreman import adoption; print(adoption.mark('a-condition-nobody-has-named'))" 2>&1)
[ "$MARK" = "◐" ] && ok || bad "an unnamed standing should mark as ◐, got '$MARK'"

for pair in ':●' 'disabled:⊘' 'absent:○' 'drifted:◐' 'unapplied:◐'; do
  state=${pair%:*} want=${pair#*:}
  MARK=$(cd "$ROOT" && python3 -c "import sys; sys.path.insert(0,'src'); from foreman import adoption; print(adoption.mark('$state'))" 2>&1)
  [ "$MARK" = "$want" ] && ok || bad "standing '$state' should mark as $want, got '$MARK'"
done

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
