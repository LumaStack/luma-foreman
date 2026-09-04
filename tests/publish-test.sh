#!/bin/sh
# Tests for `luma-foreman publish`.
#
#   sh tests/publish-test.sh
#
# Every case builds a throwaway catalog and a throwaway project, and `gh` is
# stubbed on PATH so nothing here reaches a forge. The stub is driven by a file
# the tests write, which is what makes every branch of the resolution table
# reachable without a network.
#
# The load-bearing cases are the resolution table and the strictness invariant.
# Publishing spans a gap that belongs to somebody else, so the failures worth
# preventing are the ones where the tool guesses across it: re-opening a request
# a maintainer just closed, concluding "declined" from a 404 that only means
# "you cannot see it", or writing a namespaced manifest entry for a bundle that
# has not landed. Each of those is a case below.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/publish.XXXXXX) || exit 2
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

# publish <label> <expect-exit> <args...>
publish() {
  label=$1 want=$2; shift 2
  LAST=$(cd "$PROJECT" && PATH="$T/bin:$PATH" "$CLI" publish "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want): $LAST"
}

commit_all() {
  git -C "$PROJECT" add -A
  GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=t@example.com \
  GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=t@example.com \
    git -C "$PROJECT" commit -q -m "$1" >/dev/null 2>&1 || true
}

# --- a stubbed forge ------------------------------------------------------------
# `gh` is a program, not a library, so it stubs the way `git` would. STATE holds
# what the next `pr view` should answer, which is how the resolution table below
# gets exercised without anybody merging anything.

mkdir -p "$T/bin"
STATE=$T/gh-state
AUTH=$T/gh-auth
echo OPEN > "$STATE"
echo yes > "$AUTH"

cat > "$T/bin/gh" <<EOF
#!/bin/sh
STATE=$STATE
AUTH=$AUTH
EOF
cat >> "$T/bin/gh" <<'EOF'
case "$1 $2" in
  "auth status")
    [ "$(cat "$AUTH")" = yes ] || { echo 'not logged in' >&2; exit 1; }
    exit 0 ;;
  "pr create")
    echo https://github.com/acme/catalog/pull/41
    exit 0 ;;
  "pr view")
    s=$(cat "$STATE")
    [ "$s" = MISSING ] && { echo 'no pull request found' >&2; exit 1; }
    printf '{"state":"%s"}\n' "$s"
    exit 0 ;;
  "pr list")
    echo '[]'
    exit 0 ;;
esac
exit 1
EOF
chmod +x "$T/bin/gh"

# --- a catalog and a project ----------------------------------------------------

CATALOG=$T/catalog
mkdir -p "$CATALOG/catalog/bundles"

cat > "$CATALOG/catalog/CATALOG.md" <<'EOF'
---
type: luma/catalog
namespace: acme/catalog
description: A catalog that publishes nothing yet.
---
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
(cd "$PROJECT" && "$CLI" catalog add "$CATALOG" >/dev/null 2>&1)
(cd "$PROJECT" && "$CLI" bundle new widgets >/dev/null 2>&1)
commit_all 'a bundle written here'

MANIFEST=$PROJECT/.luma/bundles/MANIFEST.md
LOCAL=$PROJECT/.luma/bundles/local/widgets
VENDORED=$PROJECT/.luma/bundles/acme/catalog/widgets

# --- the shape of the command ---------------------------------------------------

publish 'help exits 0' 0 --help
has 'luma-foreman publish'
has 'Exit codes'

publish 'unknown option is could-not-run' 2 --nonsense
has 'unknown option'

publish 'no operands is could-not-run' 2
has 'usage:'

# A bundle can go to more than one catalog, so there is nothing to infer from
# a single registered one.
publish 'a bare bundle needs a catalog named' 2 widgets
has 'name the catalog'

publish 'an unregistered catalog is could-not-run' 2 widgets nope/nope
has 'no catalog registered as'
has 'acme/catalog'

# `--force` overrides a guard protecting something. Asking a catalog twice
# defends nothing, so it is a different word, and saying so beats a bare
# failure.
publish '--force points at --again' 2 widgets acme/catalog --force
has '--again'

publish '--again and --abandon conflict' 2 widgets acme/catalog --again --abandon
has 'opposite'

publish 'abandoning nothing is a no-op that says so' 0 widgets --abandon
has 'nothing to abandon'

# --- opening a request ----------------------------------------------------------

publish 'opens a request' 0 widgets acme/catalog
has 'opened'
has 'pull/41'
has 'a maintainer has to merge it'

# The bundle keeps its local identity while the request is outstanding: it has
# not been published, and the request may yet be declined.
grepped 'local/widgets' "$MANIFEST"
grepped 'catalog: acme/catalog' "$MANIFEST"
grepped 'request: https' "$MANIFEST"
exists "$LOCAL/BUNDLE.md"

# The invariant that must not bend: a namespaced entry always carries a commit
# and a checksum, so nothing here may look like a vendored copy yet. Matched on
# the subline form — the manifest's own header explains the word `sha256`, and
# asserting on the bare word would pass for the wrong reason.
ungrepped 'acme/catalog/widgets' "$MANIFEST"
ungrepped '^  - sha256:' "$MANIFEST"
ungrepped '^  - commit:' "$MANIFEST"

# What landed on the branch is the bundle under its published identity.
BRANCH=publish-widgets-0.1.0
LAST=$(git -C "$CATALOG" show "$BRANCH:catalog/bundles/widgets/BUNDLE.md" 2>&1)
has 'title: acme/catalog/widgets'
has 'published:'
has '# acme/catalog/widgets'
lacks 'title: local/widgets'

# --- a request still under review -----------------------------------------------

echo OPEN > "$STATE"
publish 'an open request advances nothing' 0 widgets acme/catalog
has 'nothing to do yet'
has 'pull/41'
grepped 'local/widgets' "$MANIFEST"

# --- a request that was declined ------------------------------------------------
# Closed is definitive — the forge said so. Nothing here changes, and both ways
# out are named as literal commands.

echo CLOSED > "$STATE"
publish 'a declined request refuses and changes nothing' 1 widgets acme/catalog
has 'declined'
has '--again'
has '--abandon'
grepped 'request: https' "$MANIFEST"
exists "$LOCAL/BUNDLE.md"

# --- a request nobody can see ---------------------------------------------------
# A 404 is not proof: it also means moved, private, or a token that expired.
# Concluding "declined" and clearing the record would erase a live request.

echo MISSING > "$STATE"
publish 'an invisible request enumerates rather than concludes' 1 widgets acme/catalog
has 'no longer visible'
has 'become private'
has '--again'
grepped 'request: https' "$MANIFEST"

# --- the forge is unreachable ---------------------------------------------------
# Not reaching the forge is not an answer about the request. It is could-not-run,
# and nothing may change on the strength of it.

echo no > "$AUTH"
publish 'an unreachable forge is could-not-run' 2 widgets acme/catalog
has 'could not reach'
grepped 'request: https' "$MANIFEST"
echo yes > "$AUTH"

# --- abandoning ------------------------------------------------------------------
# The request dies; the destination stays, because where the bundle was meant to
# go was a decision somebody made and only the request was refused.

publish 'abandoning drops the request' 0 widgets --abandon
has 'stopped tracking'
has 'still intended for acme/catalog'
ungrepped 'request:' "$MANIFEST"
grepped 'catalog: acme/catalog' "$MANIFEST"

# --- finishing the handover -----------------------------------------------------
# Merge the branch for real, then let the tool find it. This is the only
# transition that happens without a person deciding again.

publish 're-open after abandoning' 0 widgets acme/catalog --again
has 'opened'

# The merge is what publication *is* — there is no tag, no release and no
# registry, and nothing notifies anybody.
git -C "$CATALOG" merge -q "$BRANCH" -m 'merge'
echo MERGED > "$STATE"

# Two documents naming the bundle's unpublished ID, and they are not the same
# kind of thing. One points at where the bundle lives; the other explains why it
# lives under local/ and would contradict itself if the ID were substituted in.
# Nothing tells them apart by inspection, because the difference is what the
# sentence means — so both are reported and neither is rewritten.
mkdir -p "$PROJECT/docs"
echo 'Adopted at .luma/bundles/local/widgets — see its policy.' \
  > "$PROJECT/docs/pointer.md"
echo 'A bundle written here is local/widgets until a catalog takes it.' \
  > "$PROJECT/docs/about.md"
commit_all 'documents naming the bundle'

publish 'a merged request completes the handover' 1 widgets acme/catalog
has 'merged'
has 'still name local/widgets'
has 'docs/pointer.md'
has 'docs/about.md'
has 'Only a reader can'

# The regression this pins: the first real handover rewrote every occurrence,
# which turned prose about the unpublished state into sentences that contradict
# themselves — including the record that argued for local/ in the first place.
grepped 'local/widgets' "$PROJECT/docs/about.md"
grepped 'local/widgets' "$PROJECT/docs/pointer.md"

# The project now vendors its own bundle, with a full receipt.
exists "$VENDORED/BUNDLE.md"
grepped 'acme/catalog/widgets' "$MANIFEST"
grepped 'sha256' "$MANIFEST"
grepped 'commit' "$MANIFEST"

# ...and the local identity is gone, entry and directory alike.
absent "$LOCAL"
ungrepped 'local/widgets' "$MANIFEST"
ungrepped 'request:' "$MANIFEST"

# --- the invariant, asserted directly -------------------------------------------
# A namespaced entry with no checksum is a receipt nothing can check, and
# `state()` skips the comparison when the checksum is empty — so the drift check
# would pass for it silently, forever. Hand-written here because no command
# produces this state, which is the point: if one ever starts to, this fails.

cat > "$MANIFEST" <<'EOF'
# Bundles

- `acme/catalog/widgets` 0.1.0
EOF
LAST=$(cd "$PROJECT" && "$CLI" inspect --rule adoption 2>&1); got=$?
[ "$got" -eq 1 ] && ok || bad "unverifiable entry should be a finding (exit $got): $LAST"
has 'without custody and a checksum'

# ...and a bundle written here is not held to it, request or no request.
cat > "$MANIFEST" <<'EOF'
# Bundles

- `local/widgets` 0.1.0
  - catalog: acme/catalog
  - request: https://github.com/acme/catalog/pull/41
EOF
LAST=$(cd "$PROJECT" && "$CLI" inspect --rule adoption 2>&1); got=$?
case $LAST in
  *'without custody and a checksum'*) bad 'a local bundle was held to the vendored invariant' ;;
  *) ok ;;
esac

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
