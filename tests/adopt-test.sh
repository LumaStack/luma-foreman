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
mkdir -p "$CATALOG/catalog/bundles/widgets/procedure" \
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
description: Everything about widgets.
---
EOF

cat > "$CATALOG/catalog/bundles/widgets/procedure/make-a-widget.md" <<'EOF'
---
type: procedure
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
MANIFEST=$PROJECT/.luma/bundles/MANIFEST.md

# --- listing a catalog ----------------------------------------------------------
# `get --list` is retired: browsing a catalog was never an adoption operation.

get 'get --list is retired' 2 --list --from "$CATALOG"
has 'catalog show'

catalog 'catalog show by path' 0 show "$CATALOG"
# The namespace is a header, not a column: identical on every row and wide
# enough to cost a quarter of a laptop screen.
has 'acme'
has 'widgets'
lacks 'acme/widgets'
# Three states, because the tool has two steps — a bundle can be here and still
# reach no agent. Nothing is adopted in this project yet, so all are empty.
has '○ widgets'
has 'not taken'
has '0.1.0'
has 'Everything about widgets'

# --- adopting -------------------------------------------------------------------

get 'adopt' 0 acme/widgets --from "$CATALOG"
has 'adopted 0.1.0'
exists "$VENDORED/BUNDLE.md"
exists "$VENDORED/procedure/make-a-widget.md"
exists "$MANIFEST"
grepped '`acme/widgets` 0.1.0' "$MANIFEST"
grepped "  - commit: $COMMIT" "$MANIFEST"
grepped '  - sha256: ' "$MANIFEST"

# Re-taking an adopted bundle needs no --from: the receipt records the
# source, and demanding it back made an operator repeat the tool's own
# record to it. A bundle nothing records still requires one.
get 're-get defaults to the recorded source' 0 acme/widgets
get 'an unrecorded bundle still needs --from' 2 acme/unheard-of

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

# --- writing it out -------------------------------------------------------------

apply 'check before apply' 1 --check
has 'stale'

apply 'apply' 0
exists "$PROJECT/.claude/skills/make-a-widget/SKILL.md"
exists "$PROJECT/CLAUDE.md"
grepped 'name: make-a-widget' "$PROJECT/.claude/skills/make-a-widget/SKILL.md"
grepped 'Produce one widget' "$PROJECT/.claude/skills/make-a-widget/SKILL.md"

# The adapter points at the source and does not copy it.
grepped '.luma/bundles/acme/widgets/procedure/make-a-widget.md' \
  "$PROJECT/.claude/skills/make-a-widget/SKILL.md"
grep -q 'Steps go here' "$PROJECT/.claude/skills/make-a-widget/SKILL.md" \
  && bad 'the adapter copied the workflow body' || ok

# `preload` is read only so it can be reported. Honouring it would let a
# half-migrated bundle behave correctly and stall there forever, so this bundle
# — which still declares it — reaches the index as nothing at all.
case $LAST in *preload*) ok ;; *) bad "expected the legacy preload reported: $LAST" ;; esac
# It is named in the ring and its body is not delivered, which is correct and is
# not what the legacy field asked for: it declares no `matches`, so nothing
# surfaces it and it waits to be asked for. The legacy field is reported and
# ignored — a rule nobody can see governs nothing, so it is still named.
RING=$PROJECT/.luma/bundles/INDEX.md
grepped 'acme/widgets' "$RING"
# The project index is bundle-grained: document names stay in the bundle's own
# index, which ships inside the bundle rather than being generated here.
grep -q 'widget-rules' "$RING" \
  && bad 'document names do not belong in the project index' || ok
grep -q '@.luma/bundles/acme/widgets/policy/widget-rules.md' "$PROJECT/CLAUDE.md" \
  && bad 'no bundle content is imported by the adapter' || ok

apply 'check after apply' 0 --check
has 'up to date'

inspect 'projected adoption is clean' 0

# --- apply owns a block, not the file -------------------------------------------

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
# rename to `apply` orphaned every existing block and appended beside it.
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
# Two next steps: what is on offer, then how to take one. The first question is
# always the former and the command for it is not guessable.
has 'catalog show <catalog>'
has 'get luma/<bundle> --from <catalog>'
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

# The two fields luma/project 0.2.0 dropped are not scaffolded any more.
grep -q 'owns:' "$FRESH/.luma/PROJECT.md" \
  && bad 'owns: should no longer be scaffolded' || ok
grep -q 'must_not_own:' "$FRESH/.luma/PROJECT.md" \
  && bad 'must_not_own: should no longer be scaffolded' || ok

# --catalog writes the one setting that has no default, and makes the next
# command shorter by exactly the argument it records.
WITHCAT=$T/withcat
mkdir -p "$WITHCAT"
git -C "$WITHCAT" init -q
LAST=$(cd "$WITHCAT" && "$CLI" init --catalog "$CATALOG" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "init --catalog (exit $got): $LAST"
grep -q "^source = \"$CATALOG\"" "$WITHCAT/.luma/config/luma-foreman.toml" \
  && ok || bad 'init --catalog did not record the source'
# The next steps name the catalog rather than leaving a placeholder, and drop
# the --from the config now answers.
has 'Next steps'
has "catalog show $(basename "$CATALOG")"
case $LAST in *"--from <catalog>"*) bad 'told to pass --from with a source set' ;; *) ok ;; esac
# ...and `get` with no --from now resolves through it.
LAST=$(cd "$WITHCAT" && "$CLI" get acme/widgets 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "get without --from (exit $got): $LAST"

# Idempotent. A second run adds whatever a newer version writes and touches
# nothing that is already there — refusing would make somebody do by hand the
# work the refusal had just finished diagnosing.
init 'init runs again cleanly' 0
has 'already there, left alone'
has 'Nothing to do'

# ...and it really is non-destructive.
printf 'MINE\n' >> "$FRESH/.luma/PROJECT.md"
init 'init leaves an edited descriptor alone' 0
grepped 'MINE' "$FRESH/.luma/PROJECT.md"

# A missing piece is added rather than reported.
rm "$FRESH/.luma/config/luma-foreman.toml"
init 'init adds what is missing' 0
has 'created'
[ -f "$FRESH/.luma/config/luma-foreman.toml" ] && ok || bad 'init did not restore the config'
grepped 'MINE' "$FRESH/.luma/PROJECT.md"

# migrate-into-luma is named only where there is something to migrate.
lacks 'migrate-into-luma'
MIG=$T/migrate
mkdir -p "$MIG/docs"
git -C "$MIG" init -q
printf '# Decisions\n' > "$MIG/docs/DECISIONS.md"
LAST=$(cd "$MIG" && "$CLI" init 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "init beside an existing structure (exit $got): $LAST"
case $LAST in *"migrate-into-luma"*) ok ;; *) bad 'existing records not noticed' ;; esac
case $LAST in *"docs/DECISIONS.md"*) ok ;; *) bad 'did not say what it found' ;; esac

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
has 'acme'
has 'widgets'
lacks 'acme/widgets'
has '0.1.0'

bundle 'bundle show' 0 show acme/widgets
has 'Everything about widgets'
has 'source'
has 'commit'
bundle 'bundle show resolves a bare name' 0 show widgets
has 'acme/widgets'
bundle 'bundle show refuses an unknown name' 2 show acme/nothing
has 'not recorded'

catalog 'catalog list' 0 list
has "$CATALOG"
has '1 catalog,'
# How many a catalog publishes is the part worth knowing — `1 taken` says
# nothing you did not already know. The fixture gains bundles as the file runs,
# so the shape is what matters rather than the number.
case $LAST in *" of "*" taken"*) ok ;; *) bad "no published count: $LAST" ;; esac

# Unreachable is reported per row and does not fail the run. A blank where a
# number belongs reads as zero, which is the one thing that must not happen.
GONE=$T/gone; mkdir -p "$GONE/.luma/bundles/acme/x"; git -C "$GONE" init -q
printf -- '["acme/x"]\nversion  = "1.0.0"\nsource   = "https://example.invalid/nope.git"\ncommit   = "c"\nchecksum = "sha256:c"\n' \
  > "$GONE/.luma/bundles/adopted.toml"
printf -- '---\ntype: bundle\nversion: 1.0.0\n---\nb\n' > "$GONE/.luma/bundles/acme/x/BUNDLE.md"
LAST=$(cd "$GONE" && "$CLI" catalog list 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "unreachable catalog failed the run (exit $got): $LAST"
case $LAST in *"? published"*) ok ;; *) bad "did not mark the count unknown: $LAST" ;; esac

# One repository, four spellings: .git, a scheme, scp with and without a user.
# A listing keyed on the raw string showed one catalog as two, each claiming
# half the bundles.
mkdir -p "$GONE/.luma/bundles/acme/y"
printf -- '---\ntype: bundle\nversion: 1.0.0\n---\nb\n' > "$GONE/.luma/bundles/acme/y/BUNDLE.md"
printf -- '\n["acme/y"]\nversion  = "1.0.0"\nsource   = "https://example.invalid/nope"\ncommit   = "c"\nchecksum = "sha256:c"\n' \
  >> "$GONE/.luma/bundles/adopted.toml"
LAST=$(cd "$GONE" && "$CLI" catalog list 2>&1); got=$?
case $LAST in *"1 catalog,"*) ok ;; *) bad "two spellings of one catalog were listed twice: $LAST" ;; esac
lacks 'nope.git' '' 2>/dev/null || true
case $LAST in *"nope.git"*) bad "the longer spelling was chosen for display" ;; *) ok ;; esac
case $LAST in *"could not"*) ok ;; *) bad "did not say why: $LAST" ;; esac
case $LAST in *"1 could not be reached"*) ok ;; *) bad 'no summary of what was missed' ;; esac

# A short name is derived from the source, and resolves back to it.
catalog 'catalog show by short name' 0 show "$(basename "$CATALOG")"
has 'widgets'

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
# An empty project is a state, not an error. It used to exit 2, which made the
# one case that has to be correct the one case never exercised — a repository
# whose last bundle just left still needs its skills and rings swept, and it
# still needs an adapter pointing at something true.
apply 'nothing adopted is not an error' 0
grepped 'Nothing is adopted yet' "$RING"

# Sweeping reaches what foreman wrote and stops there, which is the point of
# the marker: the generated skill goes and the hand-written one is untouched.
absent "$PROJECT/.claude/skills/make-a-widget"
exists "$PROJECT/.claude/skills/hand-written/SKILL.md"

# With a different bundle adopted, the hand-written skill still stays.
mkdir -p "$CATALOG/catalog/bundles/gadgets/procedure"
cat > "$CATALOG/catalog/bundles/gadgets/BUNDLE.md" <<'EOF'
---
type: bundle
version: 0.1.0
description: Gadgets, not widgets.
---
EOF
cat > "$CATALOG/catalog/bundles/gadgets/procedure/make-a-gadget.md" <<'EOF'
---
type: procedure
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

# --- the same ID from a different catalog ---------------------------------------
#
# Derivation makes this impossible by accident, so reaching it means two
# catalogs both declared the same namespace — deliberately, or by a fork
# copying the line. Either way it is a change of lineage rather than an
# upgrade, and the one case where doing nothing is the wrong answer: before
# this, `get` compared ID and version only and said "nothing to do" while the
# content it was asked for sat unfetched.

declaring() {        # declaring <dir> <bundle-description>
  mkdir -p "$1/catalog/bundles/widgets"
  printf -- '---\ntype: luma/catalog\nnamespace: shared\ndescription: d\n---\nc\n' \
    > "$1/catalog/CATALOG.md"
  printf -- '---\ntype: bundle\nversion: 1.0.0\ndescription: %s\n---\nb\n' "$2" \
    > "$1/catalog/bundles/widgets/BUNDLE.md"
  git -C "$1" init -q
}
declaring "$T/lup" upstream
declaring "$T/lfk" fork

LIN=$T/lin; mkdir -p "$LIN"; git -C "$LIN" init -q
LAST=$(cd "$LIN" && "$CLI" get widgets --from "$T/lup" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "first adoption (exit $got): $LAST"

LAST=$(cd "$LIN" && "$CLI" get widgets --from "$T/lfk" 2>&1); got=$?
[ "$got" -eq 1 ] && ok || bad "lineage switch not refused (exit $got): $LAST"
case $LAST in *"different catalog"*) ok ;; *) bad 'refusal did not say why' ;; esac
case $LAST in *"$T/lup"*) ok ;; *) bad 'refusal did not name what is held' ;; esac
case $LAST in *"$T/lfk"*) ok ;; *) bad 'refusal did not name what was asked for' ;; esac
grep -q "$T/lup" "$LIN/.luma/bundles/MANIFEST.md" \
  && ok || bad 'a refused switch changed the receipt'

# A trailing slash is not a different catalog. The check compares origins rather
# than strings, because the workaround for a false refusal is --force, and
# --force performs the real switch too — teaching somebody to reach for it while
# the check is pedantic is how they reach for it on the day it is right.
LAST=$(cd "$LIN" && "$CLI" get widgets --from "$T/lup/" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "a trailing slash read as a new lineage (exit $got): $LAST"
grep -q "$T/lup" "$LIN/.luma/bundles/MANIFEST.md" \
  && ok || bad 'the receipt moved for a cosmetic difference'

# --force takes it, and reports a lineage change rather than a version event —
# the version may not have moved at all.
LAST=$(cd "$LIN" && "$CLI" get widgets --from "$T/lfk" --force 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "forced switch (exit $got): $LAST"
case $LAST in *"from another catalog"*) ok ;; *) bad "not reported as a switch: $LAST" ;; esac
grep -q "$T/lfk" "$LIN/.luma/bundles/MANIFEST.md" \
  && ok || bad 'the receipt did not record the new source'

# --- a namespace derives from where the catalog lives ---------------------------
#
# Declaring one is allowed and always wins. Not declaring is the common case,
# and it is what makes a fork safe: the fork lives somewhere else, so it is
# named something else without anybody thinking about it.

derived() {          # derived <dir> <origin> <bundle-description>
  mkdir -p "$1/catalog/bundles/widgets"
  printf -- '---\ntype: luma/catalog\ndescription: d\n---\nc\n' > "$1/catalog/CATALOG.md"
  printf -- '---\ntype: bundle\nversion: 1.0.0\ndescription: %s\n---\nb\n' "$3" \
    > "$1/catalog/bundles/widgets/BUNDLE.md"
  git -C "$1" init -q && git -C "$1" remote add origin "$2"
}

derived "$T/up"   "https://github.com/LumaStack/luma-catalog.git" upstream
derived "$T/fk"   "git@github.com:acme/luma-catalog.git"          fork

DERIV=$T/deriv; mkdir -p "$DERIV"; git -C "$DERIV" init -q
LAST=$(cd "$DERIV" && "$CLI" get widgets --from "$T/up" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "derived namespace (exit $got): $LAST"
case $LAST in *"lumastack/luma-catalog/widgets"*) ok ;; *) bad "not derived: $LAST" ;; esac

# The fork is a different namespace, so both live in one project at once —
# which is the collision the source alone could not prevent.
LAST=$(cd "$DERIV" && "$CLI" get widgets --from "$T/fk" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "fork alongside upstream (exit $got): $LAST"
case $LAST in *"acme/luma-catalog/widgets"*) ok ;; *) bad "fork not distinct: $LAST" ;; esac
[ -f "$DERIV/.luma/bundles/lumastack/luma-catalog/widgets/BUNDLE.md" ] \
  && ok || bad 'upstream not vendored under its own namespace'
[ -f "$DERIV/.luma/bundles/acme/luma-catalog/widgets/BUNDLE.md" ] \
  && ok || bad 'fork not vendored under its own namespace'

# A multi-segment namespace addresses as one bundle, not a nested one.
LAST=$(cd "$DERIV" && "$CLI" get lumastack/luma-catalog/widgets --from "$T/up" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "full id (exit $got): $LAST"
LAST=$(cd "$DERIV" && "$CLI" bundle show lumastack/luma-catalog/widgets 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "bundle show on a full id (exit $got): $LAST"

# A declaration beats derivation.
derived "$T/dec" "https://github.com/LumaStack/luma-catalog.git" declared
printf -- '---\ntype: luma/catalog\nnamespace: chosen\ndescription: d\n---\nc\n' \
  > "$T/dec/catalog/CATALOG.md"
DEC=$T/decp; mkdir -p "$DEC"; git -C "$DEC" init -q
LAST=$(cd "$DEC" && "$CLI" get widgets --from "$T/dec" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "declared namespace (exit $got): $LAST"
case $LAST in *"chosen/widgets"*) ok ;; *) bad "declaration did not win: $LAST" ;; esac

# A multi-segment namespace has to survive every stage, not just `get`. Bundle
# discovery globbed exactly two levels, so a three-segment ID was invisible:
# `apply` reported "nothing adopted" and `inspect` reported the same bundles as
# recorded-but-not-on-disk. Both read identical to an empty project.

DEEP=$T/deep; mkdir -p "$DEEP"; git -C "$DEEP" init -q
LAST=$(cd "$DEEP" && "$CLI" get widgets --from "$T/up" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "deep adoption (exit $got): $LAST"
LAST=$(cd "$DEEP" && "$CLI" apply 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "apply on a deep namespace (exit $got): $LAST"
case $LAST in *"1 bundle(s) written out"*) ok ;; *) bad "apply found nothing: $LAST" ;; esac
LAST=$(cd "$DEEP" && "$CLI" inspect --rule adoption 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "inspect on a deep namespace (exit $got): $LAST"
case $LAST in *"not on disk"*) bad 'inspect could not see a deep bundle' ;; *) ok ;; esac

# The mark tracks both steps, not just the first. A bundle that was taken and
# never applied reaches no agent, which is the state `inspect` calls unapplied
# and the one somebody browsing a catalog cannot otherwise see.
MARK=$T/mark; mkdir -p "$MARK"; git -C "$MARK" init -q
LAST=$(cd "$MARK" && "$CLI" get acme/widgets --from "$CATALOG" 2>&1)
LAST=$(cd "$MARK" && "$CLI" catalog show "$CATALOG" 2>&1); got=$?
[ "$got" -eq 0 ] && ok || bad "catalog show after get (exit $got): $LAST"
case $LAST in *"◐ widgets"*) ok ;; *) bad "taken-not-applied not marked: $LAST" ;; esac
LAST=$(cd "$MARK" && "$CLI" apply 2>&1)
LAST=$(cd "$MARK" && "$CLI" catalog show "$CATALOG" 2>&1)
case $LAST in *"● widgets"*) ok ;; *) bad "applied not marked: $LAST" ;; esac
case $LAST in *"1 taken"*) ok ;; *) bad "header did not count what is taken: $LAST" ;; esac

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
has 'acme'
has 'gadgets'
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
