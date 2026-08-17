#!/bin/sh
# Tests for `luma-foreman inspect`.
#
#   sh tests/inspect-test.sh
#
# Every case builds a throwaway repository with known contents, so these assert
# what the rules actually detect rather than what they were meant to. Nothing
# here reads the machine's own repositories or configuration.
#
# The load-bearing cases are the negative ones. A scanner that finds problems is
# easy; one that stays quiet on clean input is the hard half, and a false
# positive in a check people run in continuous integration gets the check
# switched off.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}
export PYTHONDONTWRITEBYTECODE=1

T=$(mktemp -d /tmp/inspect.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM

pass=0 fail=0
ok()  { pass=$((pass + 1)); }
bad() { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

# repo <name> <author-email> [file-content] — a repository with one commit
repo() {
  d=$T/$1
  mkdir -p "$d" && git -C "$d" init -q 2>/dev/null
  printf '%s\n' "${3:-hello}" > "$d/file.txt"
  git -C "$d" add -A
  GIT_AUTHOR_NAME=Test GIT_AUTHOR_EMAIL=$2 \
  GIT_COMMITTER_NAME=Test GIT_COMMITTER_EMAIL=$2 \
    git -C "$d" commit -q -m "first" 2>/dev/null
  printf '%s' "$d"
}

# run <label> <expect-exit> <args...>
run() {
  label=$1 want=$2; shift 2
  LAST=$("$CLI" inspect "$@" 2>&1); got=$?
  [ "$got" -eq "$want" ] && ok || bad "$label (exit $got, wanted $want)"
}
has()    { case $LAST in *"$1"*) ok ;; *) bad "expected output to contain '$1'" ;; esac; }
lacks()  { case $LAST in *"$1"*) bad "expected output NOT to contain '$1'" ;; *) ok ;; esac; }

# --- clean input stays quiet ---------------------------------------------------
clean=$(repo clean 'dev@example.com')
run 'clean repo' 0 "$clean"
has '0 finding(s)'
lacks 'HIGH'

# --- machine-derived identities -------------------------------------------------
for host in 'alice@laptop.local' 'root@nas.lan' 'bob@box.localdomain' 'svc@build.internal'; do
  d=$(repo "m$(printf '%s' "$host" | tr -cd 'a-z')" "$host")
  run "machine identity $host" 1 "$d"
  has 'machine-derived'
  has "$host"
done

# A real domain that merely ends in something similar is not machine-derived.
d=$(repo realdomain 'dev@example.localhost.com')
run 'real domain not flagged' 0 "$d"
lacks 'machine-derived'

# --- malformed identities --------------------------------------------------------
d=$(repo malformed 'first.last.com')
run 'malformed identity' 1 "$d"
has 'not valid email addresses'
has 'first.last.com'

# --- home paths in tracked content -------------------------------------------------
# Fixtures are assembled at run time rather than written literally. A scanner
# whose own test file contains what it detects reports itself, and the fix is
# not to exclude tests from scanning — it is to not commit the literal.
U=alice; V=bob
d=$(repo homepath 'dev@example.com' "see /Users/$U/notes.txt for details")
run 'home path in content' 1 "$d"
has 'home directory paths'
has 'alice'

d=$(repo linuxhome 'dev@example.com' "path is /home/$V/src")
run 'linux home path' 1 "$d"
has 'bob'

# Constructed and placeholder paths are not people. The first of these shipped
# as a false positive against this repository's own test suite.
d=$(repo dotdir 'dev@example.com' 'export TMPHOME=$T/home/.config/tool')
run 'dot-directory is not a username' 0 "$d"
lacks 'home directory paths'

d=$(repo ci 'dev@example.com' "workdir: /home/runner/work/project")
run 'CI runner path ignored' 0 "$d"
lacks 'home directory paths'

# --- a check that cannot run is not a pass -------------------------------------------
mkdir -p "$T/notrepo"
run 'not a git repository' 0 "$T/notrepo"
has 'SKIPPED'
has 'A skipped check is not a pass.'
has 'could not run'

# --- machine-readable output -----------------------------------------------------
d=$(repo jsonrepo 'alice@laptop.local')
run 'json output' 1 --json "$d"
printf '%s' "$LAST" | python3 -c '
import json,sys
d = json.load(sys.stdin)
assert d["summary"]["findings"] >= 1, "expected findings"
assert d["findings"][0]["severity"] == "high", "expected high first"
assert d["findings"][0]["rule"] == "identity"
assert d["findings"][0]["surface"] == "commit-metadata"
assert "skipped" in d and "ran" in d
' 2>/dev/null && ok || bad 'json output is not the documented shape'

# Skips are visible in JSON too, or continuous integration cannot see them.
run 'json reports skips' 0 --json "$T/notrepo"
printf '%s' "$LAST" | python3 -c '
import json,sys
d = json.load(sys.stdin)
assert d["summary"]["skipped"] >= 1, "skip not reported"
assert "identity" in [s["rule"] for s in d["skipped"]], "identity skip missing"
' 2>/dev/null && ok || bad 'json does not report skipped checks'

# --- secrets ---------------------------------------------------------------------
# Fake credentials are assembled at run time, never written literally, for the
# same reason as the home paths above: this file is tracked and scanned.
AWSK="AKIA$(printf 'ABCDEFGHIJKLMNOP')"
GHT="ghp_$(printf 'abcdefghijklmnopqrstuvwxyz0123456789')"

d=$(repo awskey 'dev@example.com' "aws_access_key_id = $AWSK")
run 'aws key in content' 1 "$d"
has 'credential'
has 'AWS access key id'
# The finding must NOT contain the secret — these land in CI logs.
lacks "$AWSK"
has 'AKIA'          # a short prefix is fine, the full value is not

d=$(repo ghtoken 'dev@example.com' "token: $GHT")
run 'github token in content' 1 "$d"
has 'GitHub personal access token'
lacks "$GHT"

d=$(repo pkey 'dev@example.com' '-----BEGIN OPENSSH PRIVATE KEY-----')
run 'private key block' 1 "$d"
has 'private key block'

# Files that are the finding by their name alone.
d=$(repo envfile 'dev@example.com')
printf 'SECRET=x\n' > "$d/.env"; git -C "$d" add -A
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=d@e.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=d@e.com \
  git -C "$d" commit -q -m env
run 'tracked .env' 1 "$d"
has 'normally hold credentials'
has '.env'

# ...but templates exist to be committed, and flagging them trains people to
# ignore the scanner.
d=$(repo envexample 'dev@example.com')
printf 'SECRET=replace-me\n' > "$d/.env.example"; git -C "$d" add -A
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=d@e.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=d@e.com \
  git -C "$d" commit -q -m example
run 'env template not flagged' 0 "$d"
lacks 'normally hold credentials'

# Things that merely look secret-ish must stay quiet.
d=$(repo lookalike 'dev@example.com' 'password = "changeme"  # not a real credential')
run 'placeholder not flagged' 0 "$d"
lacks 'credential'

d=$(repo shortsk 'dev@example.com' 'sk-tooshort')
run 'short sk- string not flagged' 0 "$d"
lacks 'credential'

# History is not scanned, and the report says so rather than implying clean.
run 'history limitation stated' 0 "$clean"
has 'history was not scanned'

run 'secrets rule alone'  0 --rule secrets "$clean"

# --- argument handling ---------------------------------------------------------------
run 'unknown rule'      2 --rule nonsense "$clean"
has 'unknown rule'
run 'missing rule name' 2 --rule
run 'not a directory'   2 "$T/nope"
run 'named rule'        0 --rule identity "$clean"
run 'help'              0 --help
has 'Exit codes'

printf '%s\n' "pass=$pass fail=$fail"
[ "$fail" -eq 0 ]
