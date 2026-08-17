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

# py_compile would otherwise litter __pycache__ through the source tree.
export PYTHONDONTWRITEBYTECODE=1

ROOT=$(cd "$(dirname "$0")/.." && pwd -P)
CLI=${LUMA_FOREMAN_CLI:-$ROOT/bin/luma-foreman}

T=$(mktemp -d /tmp/pct.XXXXXX) || exit 2
trap 'rm -rf "$T"' EXIT INT TERM
mkdir -p "$T/home/.claude" "$T/repo/.git" "$T/repo/sub"
REPO=$(cd "$T/repo" && pwd -P)
SLUG=$(printf '%s' "$REPO" | tr '/.' '--')
export HOME=$T/home
export LUMA_FOREMAN_HOME=$T/home/.config/luma/foreman
# The gate is program data, not configuration, and lives apart from policy.
export LUMA_FOREMAN_DATA=$T/home/.local/share/luma/foreman
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

# --- syntax: every shipped executable must parse --------------------------------
# Checked per language rather than assuming shell, so this survives the port.
for f in "$CLI" "$ROOT/libexec/permission-gate.py" "$ROOT"/src/foreman/*.py "$ROOT"/src/foreman/policy/*.py; do
  case $f in
    *.py) python3 -m py_compile "$f" 2>/dev/null && ok || bad "syntax error in $f" ;;
    *)    head -1 "$f" | grep -q python && { python3 -m py_compile "$f" 2>/dev/null && ok || bad "syntax error in $f"; } \
             || { sh -n "$f" 2>/dev/null && ok || bad "syntax error in $f"; } ;;
  esac
done

# --- dispatcher -----------------------------------------------------------------
run 'help'            0 help;            contains 'help' 'Jobs:'
run 'unknown job'     1 not-a-job
run 'unbuilt job'     2 bootstrap   # inspect is built now; bootstrap is not
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
[ -x "$LUMA_FOREMAN_DATA/permission-gate.sh" ] && ok || bad 'install did not produce an executable gate'
# The installed gate is generated, not copied: a shim next to a private copy of
# the modules it needs. That is deliberate — a shim pointing back at a checkout
# would fail OPEN the moment the checkout moved, because a hook that exits
# non-zero is a hook Claude Code ignores.
grep -q 'gate/run.py' "$LUMA_FOREMAN_DATA/permission-gate.sh" \
  && ok || bad 'installed gate does not reference its runner'
[ -f "$LUMA_FOREMAN_DATA/gate/foreman/policy/gate.py" ] \
  && ok || bad 'install did not place the gate modules'
# ...and it must still refuse to run rather than exit non-zero when broken.
grep -q 'permissionDecision' "$LUMA_FOREMAN_DATA/permission-gate.sh" \
  && ok || bad 'installed gate cannot fail closed'
run 'install twice'   0 policy install
contains 'idempotent install' 'already current'

# Configuration and program files are separate, per XDG. This is not tidiness:
# someone clearing ~/.config/luma to reset their settings must not thereby
# delete the gate, because a missing hook is a NON-blocking error in Claude Code
# and the tool call proceeds. A config reset would fail the gate open.
[ -e "$LUMA_FOREMAN_HOME/permission-gate.sh" ] \
  && bad 'gate was installed into the configuration directory' || ok
[ -e "$LUMA_FOREMAN_HOME/gate" ] \
  && bad 'gate modules were installed into the configuration directory' || ok
[ -d "$LUMA_FOREMAN_HOME/projects" ] \
  && ok || bad 'policy directory was not created'
[ -x "$LUMA_FOREMAN_DATA/permission-gate.sh" ] \
  && ok || bad 'gate is not under the data directory'

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
jq --arg g "$LUMA_FOREMAN_DATA/permission-gate.sh" \
  '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:$g}]}]
   | .permissions.deny = ["Edit(~/.config/luma/**)"]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'wired hook'      0 policy install
contains 'wired hook accepted' 'Nothing left to do'

# The same path spelled the other legitimate ways must also be accepted. A hook
# command is a shell string, and "$HOME/..." is what you get if you wrote the
# settings by hand rather than pasting the absolute path.
for form in '"$HOME/.local/share/luma/foreman/permission-gate.sh"' \
            '${HOME}/.local/share/luma/foreman/permission-gate.sh' \
            '~/.local/share/luma/foreman/permission-gate.sh'; do
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

# --- doctor -----------------------------------------------------------------------
# The point of doctor is catching a gate that is installed and wired and still
# does nothing. A doctor that only ever agrees with `install` is worthless, so
# the load-bearing cases here are the failing ones.
run 'doctor healthy'  0 policy doctor
contains 'doctor checks behaviour' 'behaviour'
contains 'doctor reports no failures' 'fail=0'

# A gate that returns nothing: installed, wired, and silently protecting nothing.
GATE=$LUMA_FOREMAN_DATA/permission-gate.sh
cp "$GATE" "$T/gate.bak"
printf '#!/bin/sh\nexit 0\n' > "$GATE"; chmod 755 "$GATE"
run 'doctor catches a no-op gate' 1 policy doctor
contains 'no-op gate reported' 'default gating is not firing'
cp "$T/gate.bak" "$GATE"; chmod 755 "$GATE"
run 'doctor healthy again' 0 policy doctor

# A gate that gates everything, including things it must not.
printf '#!/bin/sh\nprintf %s "{\\"hookSpecificOutput\\":{\\"hookEventName\\":\\"PreToolUse\\",\\"permissionDecision\\":\\"ask\\"}}"\n' > "$GATE"
chmod 755 "$GATE"
run 'doctor catches an over-gating gate' 1 policy doctor
contains 'over-gating reported' 'ordinary commands are being gated'
cp "$T/gate.bak" "$GATE"; chmod 755 "$GATE"

# No gate at all.
mv "$GATE" "$T/gate.gone"
run 'doctor catches a missing gate' 1 policy doctor
contains 'missing gate reported' 'no executable gate'
mv "$T/gate.gone" "$GATE"; chmod 755 "$GATE"

# Wired to some other gate entirely — the upgrade case.
jq '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:"/elsewhere/permission-gate.sh"}]}]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'doctor catches wrong wiring' 1 policy doctor
contains 'wrong wiring reported' 'no PreToolUse hook points at the gate'

printf '%s\n' "pass=$pass fail=$fail"
[ "$fail" -eq 0 ]
