#!/bin/sh
# Tests for `luma-foreman get` and `luma-foreman apply`.
#
#   sh tests/adopt-test.sh
#
# Every case builds a throwaway catalog and a throwaway project, so these assert
# what the commands actually do to a filesystem rather than what they were meant
# to. Nothing here reads the real catalog or the machine's own repositories.
#
# The load-bearing cases are the refusals. Adopting is a directory copy, and a
# copy that overwrites somebody's edits or silently disagrees with its own
# checksum is worse than no adoption at all.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/adopt.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

has()   { case $LAST in *"$1"*) ok ;; *) bad "expected output to contain '$1'" ;; esac; }
lacks() { case $LAST in *"$1"*) bad "expected output NOT to contain '$1'" ;; *) ok ;; esac; }
exists() { [ -e "$1" ] && ok || bad "expected to exist: $1"; }
absent() { [ -e "$1" ] && bad "expected NOT to exist: $1" || ok; }
grepped() {
  grep -q "$1" "$2" 2>/dev/null && ok || bad "expected '$1' in $2"
}

# get <label> <expect-exit> <args...>
get() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" get "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

apply() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" apply "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

inspect() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" inspect --rule adoption "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

bundle() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" bundle "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

catalog() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" catalog "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

# --- a catalog and a project ----------------------------------------------------

CATALOG=$T/catalog
mkdir -p "$CATALOG/catalog/bundles/widgets/workflows" \
         "$CATALOG/catalog/bundles/widgets/policy" \
         "$CATALOG/catalog/bundles/widgets/_types"

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
entry_point: workflows/make-a-widget
description: Everything about widgets.
---
EOF

cat > "$CATALOG/catalog/bundles/widgets/workflows/make-a-widget.md" <<'EOF'
---
type: workflow
title: Make a widget
description: Produce one widget. Use when a widget is wanted.
---
Steps go here.
EOF

cat > "$CATALOG/catalog/bundles/widgets/policy/widget-rules.md" <<'EOF'
---
type: policy
title: Widget rules
description: What a widget may and may not be.
preload: mandatory
---
Rules go here.
EOF

# A Type Definition, to prove _types/ is never projected as reading material.
cat > "$CATALOG/catalog/bundles/widgets/_types/widget.md" <<'EOF'
---
type: type_definition
defines: widget
---
EOF

git -C "$CATALOG" init -q
git -C "$CATALOG" add -A
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com \
GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
  git -C "$CATALOG" commit -q -m first
COMMIT=$(git -C "$CATALOG" rev-parse HEAD)

PROJECT=$T/project
mkdir -p "$PROJECT"
git -C "$PROJECT" init -q

VENDORED=$PROJECT/.luma/bundles/acme/widgets
MANIFEST=$PROJECT/.luma/bundles/adopted.toml

# --- listing a catalog ----------------------------------------------------------
# `get --list` is retired: browsing a catalog was never an adoption operation.

get 'get --list is retired' 2 --list --from "$CATALOG"
has 'catalog show'

catalog 'catalog show by path' 0 show "$CATALOG"
has 'acme/widgets'
has '0.1.0'
has 'Everything about widgets'

# --- adopting -------------------------------------------------------------------

get 'adopt' 0 acme/widgets --from "$CATALOG"
has 'adopted 0.1.0'
exists "$VENDORED/BUNDLE.md"
exists "$VENDORED/workflows/make-a-widget.md"
exists "$MANIFEST"
grepped 'version  = "0.1.0"' "$MANIFEST"
grepped "commit   = \"$COMMIT\"" "$MANIFEST"
grepped 'checksum = "sha256:' "$MANIFEST"

# Adopting again is a no-op, not a second copy.
get 'adopt twice' 0 acme/widgets --from "$CATALOG"
has 'already at 0.1.0'

# --- the namespace belongs to the catalog ---------------------------------------

get 'wrong namespace refused' 2 other/widgets --from "$CATALOG"
has 'publishes acme/'

# A bare name resolves, because the catalog declares what to call things.
get 'bare name resolves' 0 widgets --from "$CATALOG"
has 'already at 0.1.0'

# --- refusals -------------------------------------------------------------------

get 'unknown bundle' 2 acme/nothing --from "$CATALOG"
has 'no bundle named nothing'

get 'no such catalog' 2 acme/widgets --from "$T/nowhere"
has 'no such catalog'

get 'not a catalog' 2 acme/widgets --from "$T"
has 'not a catalog'

# An edited copy is never silently overwritten — that is somebody's work.
printf '\nlocal edit\n' >> "$VENDORED/policy/widget-rules.md"
get 'edited copy refused' 1 acme/widgets --from "$CATALOG"
has 'has been edited here'
grepped 'local edit' "$VENDORED/policy/widget-rules.md"

get 'force overwrites' 0 acme/widgets --force --from "$CATALOG"
# --force at the same version re-copies. Reporting it as an upgrade
# would claim a version change that did not happen.
has 'took 0.1.0 again'
lacks '-> '
grep -q 'local edit' "$VENDORED/policy/widget-rules.md" \
  && bad 'force should have discarded the edit' || ok

# --- drift ----------------------------------------------------------------------

inspect 'clean adoption, unprojected' 1
has 'reach no agent'
lacks 'edited in place'

# --- projection -----------------------------------------------------------------

apply 'check before outfit' 1 --check
has 'stale'

apply 'outfit' 0
exists "$PROJECT/.claude/skills/make-a-widget/SKILL.md"
exists "$PROJECT/CLAUDE.md"
grepped 'name: make-a-widget' "$PROJECT/.claude/skills/make-a-widget/SKILL.md"
grepped 'Produce one widget' "$PROJECT/.claude/skills/make-a-widget/SKILL.md"

# The adapter points at the source and does not copy it.
grepped '.luma/bundles/acme/widgets/workflows/make-a-widget.md' \
  "$PROJECT/.claude/skills/make-a-widget/SKILL.md"
grep -q 'Steps go here' "$PROJECT/.claude/skills/make-a-widget/SKILL.md" \
  && bad 'the adapter copied the workflow body' || ok

# `preload` is read only so it can be reported. Honouring it would let a
# half-migrated bundle behave correctly and stall there forever, so this bundle
# — which still declares it — reaches the index as nothing at all.
case $LAST in *preload*) ok ;; *) bad "expected the legacy preload reported: $LAST" ;; esac
# It reaches the standing surface, and not because `preload` was read: it is a
# policy declaring `matches: always`, which is the one route to being loaded. The
# legacy field is reported and ignored; the cost comes from having no trigger.
grepped 'widget-rules' "$PROJECT/CLAUDE.md"

# A Type Definition is not reading material: it is consulted when writing a
# Document of its type, which is a job the workflow already sends you to.
grep -q '_types/widget' "$PROJECT/CLAUDE.md" \
  && bad '_types should not be indexed' || ok

apply 'check after outfit' 0 --check
has 'up to date'

inspect 'projected adoption is clean' 0

# --- outfit owns a block, not the file ------------------------------------------

MINE='# My project

Hand-written and mine.'
printf '%s\n' "$MINE" > "$PROJECT/CLAUDE.md"
apply 'splice into a hand-written file' 0
grepped 'Hand-written and mine' "$PROJECT/CLAUDE.md"
grepped 'luma:begin' "$PROJECT/CLAUDE.md"

# Running again replaces the block rather than appending a second one.
apply 'idempotent splice' 0
[ "$(grep -c 'luma:begin' "$PROJECT/CLAUDE.md")" -eq 1 ] \
  && ok || bad 'a second block was appended'
grepped 'Hand-written and mine' "$PROJECT/CLAUDE.md"

# A block written by an older version, whose marker line is worded differently,
# must still be found and replaced. Matching the whole marker string meant the
# outfit -> apply rename orphaned every existing block and appended beside it.
sed -i.bak 's|<!-- luma:begin[^>]*-->|<!-- luma:begin — generated by `luma-foreman outfit`. Edits between these markers are lost. -->|' \
  "$PROJECT/CLAUDE.md" && rm -f "$PROJECT/CLAUDE.md.bak"
apply 'block from an older wording' 0
[ "$(grep -c 'luma:begin' "$PROJECT/CLAUDE.md")" -eq 1 ] \
  && ok || bad 'a reworded marker orphaned the old block'
grepped 'Hand-written and mine' "$PROJECT/CLAUDE.md"

# --- init -----------------------------------------------------------------------
# A fresh repository of its own: init refuses to run where .luma/ already is,
# so it cannot share the fixture the rest of this file adopts into.

FRESH=$T/fresh
mkdir -p "$FRESH"
git -C "$FRESH" init -q

init() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$FRESH" && "$CLI" init "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

init 'init' 0
has 'PROJECT.md'
[ -f "$FRESH/.luma/PROJECT.md" ] && ok || bad 'init wrote no descriptor'
[ -f "$FRESH/.luma/config/luma-foreman.toml" ] && ok || bad 'init wrote no config'

# Only what will have contents, and git cannot commit an empty directory
# anyway. bundles/ arrives on the first get, records/ on the first record.
[ ! -e "$FRESH/.luma/bundles" ] && ok || bad 'init created bundles/ ahead of use'
[ ! -e "$FRESH/.luma/records" ] && ok || bad 'init created an empty records/'

# The config carries overrides, not a copy of the defaults: a commented default
# is a behavioural override one keystroke away, frozen at whatever it said the
# day init ran. The one value written out has no default to fall back to.
grepped 'catalog' "$FRESH/.luma/config/luma-foreman.toml"
grepped 'Kept minimal by design' "$FRESH/.luma/config/luma-foreman.toml"
grep -q '^source' "$FRESH/.luma/config/luma-foreman.toml" \
  && bad 'init set a catalog nobody asked for' || ok

# .luma/ is committed in full. An ignore rule here is the one edit that breaks
# the invariant the whole directory depends on.
[ ! -e "$FRESH/.gitignore" ] && ok || bad 'init wrote a .gitignore'

grepped 'type: luma/project' "$FRESH/.luma/PROJECT.md"
grepped 'TODO' "$FRESH/.luma/PROJECT.md"

# --catalog writes the one setting that has no default, and makes the next
# command shorter by exactly the argument it records.
WITHCAT=$T/withcat
mkdir -p "$WITHCAT"
git -C "$WITHCAT" init -q
LAST=$(cd "$WITHCAT" && "$CLI" init --catalog "$CATALOG" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "init --catalog (exit $got): $LAST"
grep -q "^source = \"$CATALOG\"" "$WITHCAT/.luma/config/luma-foreman.toml" \
  && ok || bad 'init --catalog did not record the source'
# ...and `get` with no --from now resolves through it.
LAST=$(cd "$WITHCAT" && "$CLI" get acme/widgets 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "get without --from (exit $got): $LAST"

init 'init refuses a second time' 1
has 'already exists'
has 'migrate-into-luma'

# A descriptor describing a repository, written where there is not one, is
# wrong in a way nobody notices until it travels.
NOGIT=$T/nogit
mkdir -p "$NOGIT"
LAST=$(cd "$NOGIT" && "$CLI" init 2>&1); got=$?
[ "$got" -eq 1 ] && ok || bad "init outside a repository (exit $got, wanted 1)"
case $LAST in *"not in a git repository"*) ok ;; *) bad 'init did not say why' ;; esac
[ ! -e "$NOGIT/.luma" ] && ok || bad 'init wrote .luma outside a repository'

# --- reading the inventory ------------------------------------------------------
# These read committed state only. Every one must hold with no network, which
# is what separates them from `bundle outdated`.

bundle 'bundle list' 0 list
has 'acme/widgets'
has '0.1.0'

bundle 'bundle show' 0 show acme/widgets
has 'Everything about widgets'
has 'source'
has 'commit'
bundle 'bundle show resolves a bare name' 0 show widgets
has 'acme/widgets'
bundle 'bundle show refuses an unknown name' 2 show acme/nothing
has 'not adopted'

catalog 'catalog list' 0 list
has "$CATALOG"
has '1 catalog(s)'

# A short name is derived from the source, and resolves back to it.
catalog 'catalog show by short name' 0 show "$(basename "$CATALOG")"
has 'acme/widgets'

catalog 'unknown verb refused' 2 nonsense
bundle  'unknown verb refused' 2 nonsense

# An edited copy is reported by `list` without needing a network, and the exit
# code says so — this is the offline half of what `inspect --rule adoption`
# turns into a finding.
printf 'edited\n' >> "$VENDORED/policy/rules.md"
bundle 'bundle list flags an edit' 1 list
has 'edited here'
bundle 'bundle show flags an edit' 1 show acme/widgets
has 'edited'
get 'restore the copy' 0 acme/widgets --force --from "$CATALOG"
bundle 'clean again' 0 list

# --- a skill for a bundle that left ---------------------------------------------

mkdir -p "$PROJECT/.claude/skills/hand-written"
cat > "$PROJECT/.claude/skills/hand-written/SKILL.md" <<'EOF'
---
name: hand-written
description: Not foreman's.
---
Mine.
EOF

rm -rf "$VENDORED"
rm -f "$MANIFEST"
apply 'nothing adopted' 2
has 'nothing adopted'

# Nothing was adopted, so outfit refused — and refusing left the hand-written
# skill alone, which is the point of the marker.
exists "$PROJECT/.claude/skills/hand-written/SKILL.md"
exists "$PROJECT/.claude/skills/make-a-widget/SKILL.md"

# With a different bundle adopted, the orphaned generated skill goes and the
# hand-written one stays.
mkdir -p "$CATALOG/catalog/bundles/gadgets/workflows"
cat > "$CATALOG/catalog/bundles/gadgets/BUNDLE.md" <<'EOF'
---
type: bundle
version: 0.1.0
description: Gadgets, not widgets.
---
EOF
cat > "$CATALOG/catalog/bundles/gadgets/workflows/make-a-gadget.md" <<'EOF'
---
type: workflow
title: Make a gadget
description: Produce one gadget.
---
EOF
get 'adopt a different bundle' 0 acme/gadgets --from "$CATALOG"
apply 'orphan removed' 0
absent "$PROJECT/.claude/skills/make-a-widget"
exists "$PROJECT/.claude/skills/hand-written/SKILL.md"
exists "$PROJECT/.claude/skills/make-a-gadget/SKILL.md"

# --- a bundle with no version cannot be adopted ---------------------------------

mkdir -p "$CATALOG/catalog/bundles/unversioned"
cat > "$CATALOG/catalog/bundles/unversioned/BUNDLE.md" <<'EOF'
---
type: bundle
description: Nothing can pin this.
---
EOF
get 'unversioned refused' 2 acme/unversioned --from "$CATALOG"
has 'declares no version'

# --- a catalog with no namespace ------------------------------------------------

BARE=$T/bare
mkdir -p "$BARE/bundles/thing"
cat > "$BARE/CATALOG.md" <<'EOF'
---
type: luma/catalog
description: Declares no namespace.
---
EOF
cat > "$BARE/bundles/thing/BUNDLE.md" <<'EOF'
---
type: bundle
version: 0.1.0
description: A thing.
---
EOF
get 'bare name needs a namespace' 2 thing --from "$BARE"
has 'name the namespace'
get 'explicit namespace works' 0 someone/thing --from "$BARE"
exists "$PROJECT/.luma/bundles/someone/thing/BUNDLE.md"

# --- outdated -------------------------------------------------------------------

outdated() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && "$CLI" bundle outdated "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

# Everything adopted is at the version the catalog publishes.
outdated 'all current' 0
has 'current'
lacks '->'

# The catalog moves on. Nothing tells the project — that is the whole point.
python3 - "$CATALOG/catalog/bundles/gadgets/BUNDLE.md" <<'PYEOF'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); p.write_text(p.read_text().replace("version: 0.1.0", "version: 0.4.0"))
PYEOF
git -C "$CATALOG" add -A >/dev/null 2>&1
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
  git -C "$CATALOG" commit -qm bump >/dev/null 2>&1

outdated 'behind is exit 1' 1
has 'acme/gadgets'
has '0.1.0'
has '0.4.0'
has 'are behind'
has 'Read what changed'

outdated 'json' 1 --json
has '"behind": true'
has '"available": "0.4.0"'

# A bundle the catalog stopped publishing is news, not breakage: the copy still
# works, and nothing will ever mention it again.
rm -rf "$CATALOG/catalog/bundles/gadgets"
git -C "$CATALOG" add -A >/dev/null 2>&1
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
  git -C "$CATALOG" commit -qm retire >/dev/null 2>&1
outdated 'retired upstream is not behind' 0
has 'no longer published here'
has 'could not be answered'

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
