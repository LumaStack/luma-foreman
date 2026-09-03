#!/bin/sh
# Tests for bin/luma-foreman and libexec/permission-gate.
#
#   sh tests/agent-permissions-cli-test.sh
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
export LUMA_FOREMAN_HOME=$T/home/.config/luma/luma-foreman
# The gate is program data, not configuration, and lives apart from policy.
export LUMA_FOREMAN_DATA=$T/home/.local/share/luma/luma-foreman
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
for f in "$CLI" "$ROOT/libexec/permission-gate.py" "$ROOT"/src/foreman/*.py "$ROOT"/src/foreman/agent_permissions/*.py; do
  case $f in
    *.py) python3 -m py_compile "$f" 2>/dev/null && ok || bad "syntax error in $f" ;;
    *)    head -1 "$f" | grep -q python && { python3 -m py_compile "$f" 2>/dev/null && ok || bad "syntax error in $f"; } \
             || { sh -n "$f" 2>/dev/null && ok || bad "syntax error in $f"; } ;;
  esac
done

# --- dispatcher -----------------------------------------------------------------
run 'help'            0 help;            contains 'help' 'Commands:'
run 'unknown command' 1 not-a-command

# All three spellings answer, and all three answer the same thing — a version
# that disagrees with itself depending on how it was asked is worse than none.
run 'version command' 0 version;     contains 'version command' 'luma-foreman '
VERSION_SAID=$LAST
run 'version flag'    0 --version;   [ "$LAST" = "$VERSION_SAID" ] && ok || bad '--version disagrees with version'
run 'version short'   0 -V;          [ "$LAST" = "$VERSION_SAID" ] && ok || bad '-V disagrees with version'

# The printed version must be the one the package declares. Pinning the literal
# here would mean every release edits a test, so ask the package instead.
DECLARED=$(cd "$ROOT" && PYTHONPATH=src python3 -c 'import foreman; print(foreman.__version__)')
[ "$VERSION_SAID" = "luma-foreman $DECLARED" ] && ok || bad "version output '$VERSION_SAID' is not 'luma-foreman $DECLARED'"

# The v is on the tag, never in the field — a string comparison between a tag
# and this value silently fails if the prefix drifts in here.
case $DECLARED in v*) bad "__version__ carries a v prefix: $DECLARED" ;; *) ok ;; esac

# Discoverable, or it is half-built.
run 'version in usage' 0 help; contains 'version in usage' '--version'

# Renamed commands are a hard error with no alias (ADR-0003), so the message is
# the whole migration path. Pin it: a bare "unknown command" would strand people.
run 'adopt renamed'     1 adopt;     contains 'adopt renamed'     'renamed to: get'
run 'outfit renamed'    1 outfit;    contains 'outfit renamed'    'renamed to: apply'
run 'bootstrap renamed' 1 bootstrap; contains 'bootstrap renamed' 'renamed to: init'
run 'refit is gone'     1 refit;     contains 'refit is gone'     'removed, with no replacement'
run 'outdated moved'    1 outdated;  contains 'outdated moved'    'renamed to: bundle outdated'

# The two read-only nouns. Both default to `list` with no verb.
run 'bundle help'       0 bundle --help;   contains 'bundle help'  'bundle show <name>'
run 'catalog help'      0 catalog --help;  contains 'catalog help' 'catalog show <name>'

run 'permissions default'  0 agent-permissions;          contains 'permissions default' 'KEY'

# --- reads work before anything is configured ------------------------------------
run 'keys'            0 agent-permissions keys;     contains 'keys' 'recursive_rm'
run 'keys <key>'      0 agent-permissions keys curl
contains 'keys curl' 'It CANNOT tell you what a URL returns'
run 'list'            0 agent-permissions list;     contains 'list' 'default'
run 'projects'        0 agent-permissions projects; contains 'projects' 'no project configs'
run 'path'            0 agent-permissions path;     contains 'path' "$SLUG"

# --- install --------------------------------------------------------------------
run 'install'         0 agent-permissions install
contains 'install' 'gate installed'
contains 'install' 'TODO PreToolUse'
[ -x "$LUMA_FOREMAN_DATA/permission-gate.sh" ] && ok || bad 'install did not produce an executable gate'
# The installed gate is generated, not copied: a shim next to a private copy of
# the modules it needs. That is deliberate — a shim pointing back at a checkout
# would fail OPEN the moment the checkout moved, because a hook that exits
# non-zero is a hook Claude Code ignores.
grep -q 'gate/run.py' "$LUMA_FOREMAN_DATA/permission-gate.sh" \
  && ok || bad 'installed gate does not reference its runner'
[ -f "$LUMA_FOREMAN_DATA/gate/foreman/agent_permissions/gate.py" ] \
  && ok || bad 'install did not place the gate modules'
# ...and it must still refuse to run rather than exit non-zero when broken.
grep -q 'permissionDecision' "$LUMA_FOREMAN_DATA/permission-gate.sh" \
  && ok || bad 'installed gate cannot fail closed'
run 'install twice'   0 agent-permissions install
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
  && ok || bad 'permissions directory was not created'
[ -x "$LUMA_FOREMAN_DATA/permission-gate.sh" ] \
  && ok || bad 'gate is not under the data directory'

# Directories are named for the application, not nested under a vendor. XDG says
# $XDG_CONFIG_HOME/<application>/, nearly every tool does that, and the charter
# agrees: foreman must be worth installing where no organization exists, so a
# path implying a suite is wrong.
case $LUMA_FOREMAN_HOME in *-foreman) ok ;; *) bad 'config dir is not application-named' ;; esac
case $LUMA_FOREMAN_DATA in *-foreman) ok ;; *) bad 'data dir is not application-named' ;; esac

# The gate must not write bytecode into its own install directory — that is
# inside the deny rule protecting it, and it goes stale on upgrade.
jq -nc '{tool_name:"Bash",permission_mode:"default",cwd:"/tmp",tool_input:{command:"sudo ls"}}' \
  | "$LUMA_FOREMAN_DATA/permission-gate.sh" >/dev/null 2>&1
[ -z "$(find "$LUMA_FOREMAN_DATA" -name '__pycache__' 2>/dev/null)" ] \
  && ok || bad 'the gate wrote bytecode into its install directory'

# A hook pointing at some OTHER permission-gate.sh must be reported, not passed.
# Matching the filename rather than the installed path once made an upgrade look
# complete while the old gate was still the one running.
SETTINGS=$T/home/.claude/settings.json
jq '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:"/somewhere/else/permission-gate.sh"}]}]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'stale hook'      0 agent-permissions install
contains 'stale hook reported' 'somewhere'
contains 'stale hook not passed' 'TODO PreToolUse'

# The correct path is accepted.
jq --arg g "$LUMA_FOREMAN_DATA/permission-gate.sh" \
  '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:$g}]}]
   | .permissions.deny = ["Edit(~/.config/luma/**)"]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'wired hook'      0 agent-permissions install
contains 'wired hook accepted' 'Nothing left to do'

# The same path spelled the other legitimate ways must also be accepted. A hook
# command is a shell string, and "$HOME/..." is what you get if you wrote the
# settings by hand rather than pasting the absolute path.
for form in '"$HOME/.local/share/luma/luma-foreman/permission-gate.sh"' \
            '${HOME}/.local/share/luma/luma-foreman/permission-gate.sh' \
            '~/.local/share/luma/luma-foreman/permission-gate.sh'; do
  jq --arg g "$form" '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:$g}]}]' \
    "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
  run "hook spelled $form" 0 agent-permissions install
  contains "accepts $form" 'Nothing left to do'
done

# --- writes ----------------------------------------------------------------------
run 'allow'           0 agent-permissions allow curl
run 'set refined'     0 agent-permissions set ssh trusted
run 'set free-form'   0 agent-permissions set ssh_hosts build01,git.example.com
run 'show after set'  0 agent-permissions
contains 'project value wins' 'trusted'
grep -q 'curl = "allow"' "$PROJECT_FILE" && ok || bad 'allow did not reach the file'

# A subdirectory of the repo resolves to the same project file.
out=$( cd "$REPO/sub" && "$CLI" agent-permissions path )
[ "$out" = "$PROJECT_FILE" ] && ok || bad "subdirectory resolved to $out"

# --- validation ------------------------------------------------------------------
run 'unknown key'     1 agent-permissions set nonsense x
run 'bad value'       1 agent-permissions set curl bogus
contains 'bad value names the key' 'keys curl'
run 'verb on free-form key' 1 agent-permissions allow ssh_hosts
contains 'free-form guard' 'takes a value, not a verb'
run 'unknown subcommand'    1 agent-permissions frobnicate

# --- reset ------------------------------------------------------------------------
run 'reset one'       0 agent-permissions reset curl
grep -q 'curl' "$PROJECT_FILE" && bad 'reset left the key behind' || ok
run 'reset all'       0 agent-permissions reset
[ -e "$PROJECT_FILE" ] && bad 'bare reset left the file behind' || ok
run 'reset with nothing to reset' 1 agent-permissions reset

# --- global scope is separate from project scope ------------------------------------
run 'global set'      0 agent-permissions set -g sudo allow
run 'show sources'    0 agent-permissions
contains 'global source shown' 'global'
[ -e "$PROJECT_FILE" ] && bad 'global write touched the project file' || ok

# --- doctor -----------------------------------------------------------------------
# The point of doctor is catching a gate that is installed and wired and still
# does nothing. A doctor that only ever agrees with `install` is worthless, so
# the load-bearing cases here are the failing ones.
run 'doctor healthy'  0 agent-permissions doctor
contains 'doctor checks behaviour' 'behaviour'
contains 'doctor reports no failures' 'fail=0'

# A gate that returns nothing: installed, wired, and silently protecting nothing.
GATE=$LUMA_FOREMAN_DATA/permission-gate.sh
cp "$GATE" "$T/gate.bak"
printf '#!/bin/sh\nexit 0\n' > "$GATE"; chmod 755 "$GATE"
run 'doctor catches a no-op gate' 1 agent-permissions doctor
contains 'no-op gate reported' 'default gating is not firing'
cp "$T/gate.bak" "$GATE"; chmod 755 "$GATE"
run 'doctor healthy again' 0 agent-permissions doctor

# A gate that gates everything, including things it must not.
printf '#!/bin/sh\nprintf %s "{\\"hookSpecificOutput\\":{\\"hookEventName\\":\\"PreToolUse\\",\\"permissionDecision\\":\\"ask\\"}}"\n' > "$GATE"
chmod 755 "$GATE"
run 'doctor catches an over-gating gate' 1 agent-permissions doctor
contains 'over-gating reported' 'ordinary commands are being gated'
cp "$T/gate.bak" "$GATE"; chmod 755 "$GATE"

# No gate at all.
mv "$GATE" "$T/gate.gone"
run 'doctor catches a missing gate' 1 agent-permissions doctor
contains 'missing gate reported' 'no executable gate'
mv "$T/gate.gone" "$GATE"; chmod 755 "$GATE"

# Wired to some other gate entirely — the upgrade case.
jq '.hooks.PreToolUse = [{matcher:"Bash",hooks:[{type:"command",command:"/elsewhere/permission-gate.sh"}]}]' \
  "$SETTINGS" > "$SETTINGS.t" && mv "$SETTINGS.t" "$SETTINGS"
run 'doctor catches wrong wiring' 1 agent-permissions doctor
contains 'wrong wiring reported' 'no PreToolUse hook points at the gate'

printf '%s\n' "pass=$pass fail=$fail"
[ "$fail" -eq 0 ]

# The global file was renamed from policy.toml when the command became
# agent-permissions. The old name is still read when the new one is absent,
# because a permission file that silently stops being read fails OPEN.
rm -f "$LUMA_FOREMAN_HOME/permissions.toml"
printf 'curl = "allow"\n' > "$LUMA_FOREMAN_HOME/policy.toml"
out=$("$CLI" agent-permissions 2>&1)
case "$out" in *allow*) ok;; *) bad 'legacy policy.toml was not read';; esac

# ...and the new name wins when both exist, so a migration is one write away.
printf 'curl = "deny"\n' > "$LUMA_FOREMAN_HOME/permissions.toml"
out=$("$CLI" agent-permissions 2>&1)
case "$out" in *deny*) ok;; *) bad 'permissions.toml did not take precedence';; esac
rm -f "$LUMA_FOREMAN_HOME/policy.toml"

# A module dropped from GATE_MODULES must not survive on disk. Every file under
# gate/foreman/ is a working piece of a gate, so an abandoned gate.py is an
# older set of matching rules — still present, still runnable — and status()
# would never notice because it only compares files it knows about.
mkdir -p "$LUMA_FOREMAN_DATA/gate/foreman/policy"
printf 'stale\n' > "$LUMA_FOREMAN_DATA/gate/foreman/policy/gate.py"
printf '# force an update\n' >> "$LUMA_FOREMAN_DATA/gate/foreman/agent_permissions/gate.py"
"$CLI" agent-permissions install >/dev/null 2>&1
[ ! -e "$LUMA_FOREMAN_DATA/gate/foreman/policy/gate.py" ] \
  && ok || bad 'install left a stale gate module on disk'
[ ! -d "$LUMA_FOREMAN_DATA/gate/foreman/policy" ] \
  && ok || bad 'install left an empty stale module directory'
[ -f "$LUMA_FOREMAN_DATA/gate/foreman/agent_permissions/gate.py" ] \
  && ok || bad 'pruning removed a module that is still part of the gate'

# Every other suite ends this way, and this one did not — so its assertions
# could not fail the build. `[ ... ]` as the last command is the exit status.
[ "$fail" -eq 0 ]
