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

# Assembled, not written literally — see the note above. This exact line was
# committed as a literal once and the scanner promptly reported its own repo.
PK=$(printf -- '-----BEGIN %s PRIVATE KEY-----' OPENSSH)
d=$(repo pkey 'dev@example.com' "$PK")
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

# --- bundles ---------------------------------------------------------------------
# A bundle whose defects are all legal under the format: it publishes cleanly,
# every adopter copies it, and nothing else notices. That gap is what this rule
# is for.

# bundle <name> — a repo containing one minimal, valid bundle
bundle() {
  d=$T/$1; mkdir -p "$d/b" && git -C "$d" init -q 2>/dev/null
  printf -- '---\ntype: bundle\nversion: 0.1.0\n---\nfine\n' > "$d/b/BUNDLE.md"
  printf '%s' "$d"
}

d=$(bundle bok)
run 'valid bundle is quiet' 0 "$d"
lacks 'rule=bundles'

# No bundles at all is a skip, never a pass.
run 'no bundles is a skip' 0 "$clean"
has 'no bundles found'

d=$(bundle bver)
printf -- '---\ntype: bundle\n---\nno version\n' > "$d/b/BUNDLE.md"
run 'missing version' 1 "$d"
has 'declares no version'

# --- a reserved name in the wrong case ------------------------------------------
#
# `bundle.md` is not a broken BUNDLE.md — it is an ordinary Document, and the
# tools ignore it completely. That is the casing rule working as designed, and
# it is also exactly why it needs surfacing: the bundle simply is not there, and
# nothing else says so. Somebody who meant lowercase is free to keep it.

d=$T/wrongcase; mkdir -p "$d/b" && git -C "$d" init -q 2>/dev/null
printf -- '---\ntype: bundle\nversion: 0.1.0\n---\nfine\n' > "$d/b/BUNDLE.md"
mkdir -p "$d/c"
printf -- '---\ntype: bundle\nversion: 0.1.0\n---\nx\n' > "$d/c/bundle.md"
run 'reserved name in the wrong case' 1 "$d"
has 'wrong case'
has 'c/bundle.md'

# Not every lowercase match is a mistake, and the rule itself says which. A
# template is a pattern for making a bundle, and a Type Definition describes
# what one is — neither is the thing its directory is, so both are correct.
d=$(bundle casefine)
mkdir -p "$d/b/templates" "$d/b/_types"
printf -- '---\ntype: bundle\nversion: 0.1.0\n---\n[t](templates/bundle.md)\n' > "$d/b/BUNDLE.md"
printf -- 'copy this\n' > "$d/b/templates/bundle.md"
printf -- '---\ntype: type_definition\ndefines: catalog\n---\nx\n' > "$d/b/_types/catalog.md"
run 'templates and _types keep their casing' 0 "$d"
lacks 'wrong case'

# --- triggers that can never fire -----------------------------------------------
#
# A misspelled trigger kind is the worst shape of defect this format produces: it
# parses, it publishes, every adopter copies it, and the rule it guards simply
# never fires. Nothing distinguishes that from a rule whose moment has not come.

d=$(bundle trigkind)
printf -- '---\ntype: policy\ntitle: T\ncompliance: mandatory\napplies_to:\n  - patth: "src/**"\n---\nx\n' > "$d/b/p.md"
run 'unknown trigger kind' 1 "$d"
has 'not a trigger'
has 'patth'

# `moment` is a closed vocabulary for the same reason: a name nobody fires is
# indistinguishable from a moment that has not arrived.
d=$(bundle trigmoment)
printf -- '---\ntype: policy\ntitle: T\ncompliance: mandatory\napplies_to:\n  - event: before-lunch\n---\nx\n' > "$d/b/p.md"
run 'unknown event' 1 "$d"
has 'before-lunch'

d=$(bundle trigok)
printf -- '---\ntype: policy\ntitle: T\ncompliance: mandatory\napplies_to:\n  - event: before-commit\n  - path: "**/*.css"\n  - command: git commit\n  - topic: doing the thing\n---\nx\n' > "$d/b/p.md"
run 'well-formed triggers are quiet' 0 "$d"
lacks 'rule=bundles'

# --- mandatory with nowhere to fire ---------------------------------------------
#
# Legal, and the most expensive thing a bundle can do: it loads into every
# session of every adopter, forever. Worth saying out loud rather than leaving
# somebody to discover it in a context budget.

d=$(bundle alwayson)
printf -- '---\ntype: policy\ntitle: T\ncompliance: mandatory\n---\nx\n' > "$d/b/p.md"
run 'mandatory with no trigger is surfaced' 1 "$d"
has 'every session'

# The silent one. [[..]] is YAML flow-sequence syntax, so unquoted it parses as
# a nested array and the link never resolves — with no parser complaining.
d=$(bundle btrap)
printf -- '---\ntype: workflow\nparent: [[somewhere]]\n---\nbody\n' > "$d/b/w.md"
run 'unquoted frontmatter wikilink' 1 "$d"
has 'unquoted wikilink'
lacks 'resolve to nothing'      # reported once, as the trap — not twice

# ...and quoted is correct, so it must stay quiet when the target exists.
d=$(bundle bquoted)
printf -- '---\ntype: workflow\n---\nbody\n' > "$d/b/target.md"
printf -- '---\ntype: workflow\nparent: "[[target]]"\n---\nbody\n' > "$d/b/w.md"
run 'quoted wikilink that resolves' 0 "$d"
lacks 'rule=bundles'

d=$(bundle btype)
printf -- '---\ntitle: no type\n---\nbody\n' > "$d/b/w.md"
run 'frontmatter without a type' 1 "$d"
has 'no type'

d=$(bundle bentry)
printf -- '---\ntype: bundle\nversion: 0.1.0\nentry_point: workflows/nope\n---\nx\n' > "$d/b/BUNDLE.md"
run 'entry_point resolves to nothing' 1 "$d"
has 'entry_point points at nothing'

# Self-containment: a bundle must be copyable and still work.
d=$(bundle bescape); mkdir -p "$d/elsewhere"; printf 'x\n' > "$d/elsewhere/x.md"
printf -- '---\ntype: bundle\nversion: 0.1.0\n---\n[out](../elsewhere/x.md)\n' > "$d/b/BUNDLE.md"
run 'link escaping the bundle' 1 "$d"
has 'point outside the Bundle'

d=$(bundle bmiss)
printf -- '---\ntype: bundle\nversion: 0.1.0\n---\n[gone](templates/absent.md)\n' > "$d/b/BUNDLE.md"
run 'missing attachment' 1 "$d"
has 'missing attachment'

d=$(bundle borphan); printf 'nobody links me\n' > "$d/b/stray.txt"
run 'orphaned asset is low, not high' 1 "$d"
has 'nothing links to'

# The load-bearing negative: documents that explain syntax are full of
# illustrative links. Reporting those is how a checker gets switched off.
d=$(bundle bcode)
{ printf -- '---\ntype: workflow\n---\n'
  printf 'Inline `[[not-real]]` and a fence:\n\n```yaml\nparent: [[also-not-real]]\n```\n'
} > "$d/b/w.md"
run 'illustrative syntax in code is ignored' 0 "$d"
lacks 'rule=bundles'

# A bundle inside a bundle is audited once, by itself.
d=$(bundle bnest); mkdir -p "$d/b/inner"
printf -- '---\ntype: bundle\nversion: 0.2.0\n---\nx\n' > "$d/b/inner/BUNDLE.md"
run 'nested bundle audited once' 0 "$d"

# Bundles are found by asking git, not by walking the filesystem. A gitignored
# worktree holds a whole second checkout, and reporting another agent's
# in-progress work as this repository's problem is worse than useless.
d=$(bundle bwt)
git -C "$d" add -A >/dev/null 2>&1
GIT_AUTHOR_NAME=T GIT_AUTHOR_EMAIL=d@e.com GIT_COMMITTER_NAME=T GIT_COMMITTER_EMAIL=d@e.com \
  git -C "$d" commit -q -m base 2>/dev/null
printf '.wt/\n' > "$d/.gitignore"
git -C "$d" worktree add -q "$d/.wt/task" -b task 2>/dev/null
printf -- '---\ntype: bundle\n---\nno version\n' > "$d/.wt/task/b/BUNDLE.md"
run 'gitignored worktree is not scanned' 0 "$d"
lacks 'declares no version'

# ...but an untracked bundle in the working tree still is. Not yet committed is
# not the same as not this repository's.
mkdir -p "$d/fresh"
printf -- '---\ntype: bundle\n---\nno version\n' > "$d/fresh/BUNDLE.md"
run 'untracked bundle is still audited' 1 "$d"
has 'declares no version'

run 'bundles rule alone' 0 --rule bundles "$clean"
has 'no bundles found'

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
