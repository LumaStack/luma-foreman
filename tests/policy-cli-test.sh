#!/bin/sh
# Tests for bin/luma-foreman and libexec/policy.
#
#   sh tests/policy-cli-test.sh
#
# permission-gate-test.sh exercises the hook and never runs the CLI, which is
# how a quoting error in the SPEC table once shipped with a green suite. This
# file exists so that "the CLI still starts" is something the tests know.
#
# Hermetic: HOME and LUMA_FOREMAN_HOME both point into a temp dir, so the real
# ~/.config/luma/foreman and ~/.claude are never read or written.
set -u

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=$ROOT/bin/luma-foreman

T=$(mktemp -d /tmp/pct.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM
mkdir -p "$T/home/.claude" "$T/repo/.git" "$T/repo/sub"
REPO=$(cd "$T/repo" && pwd -P)
SLUG=$(printf '%s' "$REPO" | tr '/.' '--')
export HOME=$T/home
export LUMA_FOREMAN_HOME=$T/home/.config/luma/foreman
PROJECT_FILE=$LUMA_FOREMAN_HOME/projects/$SLUG.toml
echo '{"permissions":{"allow":["Bash(ls *)"]}}' > "$T/home/.claude/settings.json"

pass=0 fail=0
ok()   { pass=$((pass + 1)); }
bad()  { fail=$((fail + 1)); printf 'FAIL  %s\n' "$1"; }

# run <label> <expect-exit> <args...>  — runs the CLI from inside $REPO
run() {
  label=$1 want=$2; shift 2
  out=$( cd "$REPO" && "$CLI" "$@" 2>&1 ); got=$?
  if [ "$got" -ne "$want" ]; then
    bad "$label (exit $got, wanted $want)"; printf '      %s\n' "$out" | head -3
  else ok; fi
  LAST=$out
}
# contains <label> <needle>  — assert against the last run's output
contains() {
  case $LAST in *"$2"*) ok ;; *) bad "$1: output missing '$2'" ;; esac
}

# --- syntax: every shipped script must parse -----------------------------------
for f in "$CLI" "$ROOT/libexec/policy" "$ROOT/libexec/permission-gate.sh"; do
  if sh -n "$f" 2>/dev/null; then ok; else bad "syntax error in $f"; fi
done

# --- dispatcher -----------------------------------------------------------------
run 'help'            0 help;            contains 'help' 'Jobs:'
run 'unknown job'     1 not-a-job
run 'unbuilt job'     2 inspect
run 'policy default'  0 policy;          contains 'policy default' 'KEY'

# --- reads work before anything is configured ------------------------------------
run 'keys'            0 policy keys;     contains 'keys' 'recursive_rm'
run 'keys <key>'      0 policy keys curl
contains 'keys curl' 'It CANNOT tell you what a URL returns'
run 'list'            0 policy list;     contains 'list' 'default'
run 'projects'        0 policy projects; contains 'projects' 'no project configs'
run 'path'            0 policy path;     contains 'path' "$SLUG"

# --- install --------------------------------------------------------------------
run 'install'         0 policy install
contains 'install' 'gate installed'
contains 'install' 'TODO PreToolUse'
[ -x "$LUMA_FOREMAN_HOME/permission-gate.sh" ] && ok || bad 'install did not produce an executable gate'
cmp -s "$ROOT/libexec/permission-gate.sh" "$LUMA_FOREMAN_HOME/permission-gate.sh" \
  && ok || bad 'installed gate differs from source'
run 'install twice'   0 policy install
contains 'idempotent install' 'already current'

# A hook pointing at some OTHER permission-gate.sh must be reported, not passed.
# Matching the filename rather than the installed path once made an upgrade look
# complete while the old gate was still the one running.
SETTINGS=$T/home/.claude/settings.json
jq '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:"/somewhere/else/permission-gate.sh"}]}]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'stale hook'      0 policy install
contains 'stale hook reported' 'somewhere'
contains 'stale hook not passed' 'TODO PreToolUse'

# The correct path is accepted.
jq --arg g "$LUMA_FOREMAN_HOME/permission-gate.sh" \
  '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:$g}]}]
   | .permissions.deny = ["Edit(~/.config/luma/**)"]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'wired hook'      0 policy install
contains 'wired hook accepted' 'Nothing left to do'

# The same path spelled the other legitimate ways must also be accepted. A hook
# command is a shell string, and "$HOME/..." is what you get if you wrote the
# settings by hand rather than pasting the absolute path.
for form in '"$HOME/.config/luma/foreman/permission-gate.sh"' \
            '${HOME}/.config/luma/foreman/permission-gate.sh' \
            '~/.config/luma/foreman/permission-gate.sh'; do
  jq --arg g "$form" '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:$g}]}]' \
    "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
  run "hook spelled $form" 0 policy install
  contains "accepts $form" 'Nothing left to do'
done

# --- writes ----------------------------------------------------------------------
run 'allow'           0 policy allow curl
run 'set refined'     0 policy set ssh trusted
run 'set free-form'   0 policy set ssh_hosts build01,git.example.com
run 'show after set'  0 policy
contains 'project value wins' 'trusted'
grep -q 'curl = "allow"' "$PROJECT_FILE" && ok || bad 'allow did not reach the file'

# A subdirectory of the repo resolves to the same project file.
out=$( cd "$REPO/sub" && "$CLI" policy path )
[ "$out" = "$PROJECT_FILE" ] && ok || bad "subdirectory resolved to $out"

# --- validation ------------------------------------------------------------------
run 'unknown key'     1 policy set nonsense x
run 'bad value'       1 policy set curl bogus
contains 'bad value names the key' 'keys curl'
run 'verb on free-form key' 1 policy allow ssh_hosts
contains 'free-form guard' 'takes a value, not a verb'
run 'unknown subcommand'    1 policy frobnicate

# --- reset ------------------------------------------------------------------------
run 'reset one'       0 policy reset curl
grep -q 'curl' "$PROJECT_FILE" && bad 'reset left the key behind' || ok
run 'reset all'       0 policy reset
[ -e "$PROJECT_FILE" ] && bad 'bare reset left the file behind' || ok
run 'reset with nothing to reset' 1 policy reset

# --- global scope is separate from project scope ------------------------------------
run 'global set'      0 policy set -g sudo allow
run 'show sources'    0 policy
contains 'global source shown' 'global'
[ -e "$PROJECT_FILE" ] && bad 'global write touched the project file' || ok

printf '%s\n' "pass=$pass fail=$fail"
[ "$fail" -eq 0 ]
