# Claude Code permission policy

Per-project control over what Claude Code is allowed to do, changed with a
command instead of by editing a hook.

Claude Code's own permission rules are global: one `settings.json`, one answer
for every repository. That is right for "never read `.env`" and wrong for "this
repo may ssh to the build box." This adds a per-project layer underneath, so
loosening a rule for one repository does not loosen it everywhere.

## Install

```bash
luma-foreman policy install
```

That copies the gate into `~/.config/luma/foreman/`, then prints the two changes
you have to make to `~/.claude/settings.json` yourself. It does not edit that
file — it is yours, and it is where your own rules live. Re-run it after every
upgrade; it is idempotent and tells you when there is nothing to do.

Hook changes need a Claude Code restart, because Claude Code snapshots hook
*configuration* at session start. Everything after that is live: policy changes
take effect on the next tool call, which is the whole reason policy lives in a
file the hook reads rather than in `settings.json`.

## The two enforcement layers

1. **Native rules** in `settings.json` under `permissions.deny` / `.ask` /
   `.allow`. Patterns look like `Bash(git push *)`, are gitignore-style, and are
   **anchored to the start of the command** — so they do not match a command
   buried in a compound like `foo && git push`. Global: no per-project dimension.

2. **The PreToolUse hook**, `permission-gate.sh`. It reads the command,
   `permission_mode` and `cwd` from stdin and can return `ask` or `deny`. It
   matches **anywhere in the command string**, so it catches compounds and odd
   flag forms the native rules miss — and it is the only layer that can answer
   differently per project.

Keep both in mind when changing either. Removing a native `ask` rule does
nothing if the hook still gates the same command.

## Precedence

Most-restrictive-wins: **deny → hook decision → ask → allow**.

| Layer | Normal modes | `bypassPermissions` | `trust = "full"` |
|---|---|---|---|
| native `deny` | yes | yes | yes |
| native `ask` | yes | **yes** | **yes** |
| hook `always` / `deny` | yes | **yes** | **yes** |
| hook `ask` / `trusted` / `safe` | yes | **no** | **no** |
| native `allow` prompt | n/a | skipped | skipped |

`bypassPermissions` skips the allow-stage prompting and the hook's lower tier.
It does **not** skip native `deny`, native `ask`, or the hook's `always` tier.
That asymmetry is the design: `always` means "prompt even in bypass", `ask`
means "prompt except in bypass".

**The native layer is global, so it wins the argument.** The hook can only
tighten what `settings.json` already permits, never loosen it. If a project-level
`allow` appears to do nothing, look for a native rule covering the same command.

## The values, and what each is for

- **`allow` — "routine, never worth a prompt."** The hook expresses no opinion
  and the normal flow decides.

- **`ask` — "confirm normally, but trust me in bypass."** The bucket this exists
  for. Risky enough to check during ordinary work (`ssh`, `curl`, `sudo`,
  non-force `git push`), not so dangerous it should interrupt a session where you
  deliberately opted into "stop asking me about routine things."

- **`always` — "confirm in every mode, and don't let anything slip past."** Same
  intent as a native `ask` rule, but enforced in the hook because you need
  matching the native list cannot do: compounds (`cd x && rm -rf y`), flag
  variants (`-r`, `-R`, `-rf`, `--recursive`), absolute paths (`/bin/rm`). Pair
  it with a native `ask` as a backup so the guard survives the hook going
  missing.

- **`deny` — "not in this project."** A project-scoped hard block. It cannot
  loosen anything: a native `allow` plus a hook `deny` still blocks.

Two questions decide where something goes. **Reversible?** If no, `always` or a
native `ask`. **Should bypass skip the prompt?** If yes, `ask`; if no, `always`.
And a third that decides the layer: **is the answer the same in every
repository?** If yes, a native rule; if no, policy.

## Per-project policy

Resolved on every call, per key, most specific wins:

```
~/.config/luma/foreman/projects/<slug>.toml   the project the session is in
~/.config/luma/foreman/policy.toml            global fallback
built-in defaults in the gate                 shipped
```

`<slug>` is the project's absolute path with `/` and `.` both replaced by `-`,
matching how Claude Code names directories under `~/.claude/projects`. The path
is the **repository root** — nearest ancestor holding a `.git` — so every session
in a repo shares one policy regardless of which subdirectory it started in.
Outside a repo it is the session cwd. Worktrees have their own `.git` and so
their own policy, deliberately.

Nothing is stored inside the project, so none of it can be committed by
accident. `$LUMA_FOREMAN_HOME` overrides the location; `$XDG_CONFIG_HOME` is
honored.

```bash
luma-foreman policy                    # effective policy here, and where each value came from
luma-foreman policy keys               # every key, what it gates, what it accepts
luma-foreman policy keys curl          # the long version for one key, including its limits

luma-foreman policy allow curl         # shorthand for the three common values
luma-foreman policy ask curl
luma-foreman policy deny curl
luma-foreman policy set curl safe      # general form — reaches safe, trusted, always
luma-foreman policy set -g sudo ask    # global fallback
luma-foreman policy reset curl         # drop one override
luma-foreman policy reset              # drop every override in this scope

luma-foreman policy projects           # every project that has a config
```

The config format is a documented subset of TOML: top-level `key = "value"`
lines and `#` comments. Tables are skipped, not parsed.

### Two values that are not just tiers

- **`ssh = "trusted"`** allows a host listed in `ssh_hosts` and prompts for
  anything else. Anything it cannot parse confidently — no host, two `ssh`
  invocations in one compound — prompts.
- **`curl`/`wget = "safe"`** allows a plain fetch and prompts when the command
  writes to disk (`-o`, `-O`), uploads a body (`-T`, `-d`, `-F`), or pipes into
  an interpreter. **It cannot tell you what a URL returns** — the hook sees only
  the command string. `safe` is a claim about the *shape* of the command, never
  about the bytes that come back.

### Why the commands are named that way

Modelled on prior art so the muscle memory transfers:

| | precedent |
|---|---|
| bare invocation / `list` = effective config | `claude auto-mode config`, `git config list`, `npm config list`, `kubectl config view` |
| `reset [<key>]` = back to defaults | `claude auto-mode reset`. `unset` also works — `git config` and `kubectl config` spell it that way — but it reads as "turn off", which is the wrong meaning |
| `allow` / `ask` / `deny` | `ufw allow`/`deny`, and Claude Code's own `permissions.allow`/`.ask`/`.deny`. **Not** `disallow` — nothing in this space uses that word |
| `projects` | `defaults domains`, `docker context ls`, `git worktree list` |
| `install` | `pre-commit install` — write what you own, print what you don't |

## What this layer is not

The hook matches text. `$(echo curl)`, a renamed binary, or a Python script
using `urllib` all walk straight past it, and `downloads` can only list the
common package-manager front doors.

It is a guard against your own slips and an agent's carelessness, not against an
adversary. For an actual boundary use Claude Code's
[sandboxing](https://code.claude.com/docs/en/sandboxing) — OS-level filesystem
and network limits on Bash and its children — with this on top for ergonomics.

Related: the hook matches textually, so it over-prompts on string literals like
`echo "rm -rf /"`, and on `luma-foreman policy keys curl` because the word
`curl` is in there. That is intentional; it fails safe toward prompting.

## Keeping the agent out of its own rulebook

Two things stop a session editing the policy that governs it:

- `Edit(~/.config/luma/**)` in `permissions.deny` — absolute, covers the file
  tools.
- The `policy_write` key, `always` by default — catches Bash writes to those
  paths and the CLI's own writing subcommands, in every mode including bypass.

The gate script lives in the **same directory as the policy it reads**, so one
deny rule protects both. A gate an agent can rewrite is not a gate.

Reads stay ungated: `luma-foreman policy` and `cat`ting the files are fine, and
being able to see the policy is what makes a refusal legible.

## Two ways a Claude Code rule silently does nothing

Neither is visible from the config. The rules look right and match nothing.

**A single leading `/` is not the filesystem root.** It resolves relative to the
settings file's own root, so in `~/.claude/settings.json`, `Read(/tmp/**)`
matches `~/.claude/tmp/**`. The four forms: `//path` = filesystem root, `/path` =
relative to the settings source, `~/path` = home, `path` = relative to cwd.
**There is no warning for getting this wrong.**

**Only some tool names are consulted for file rules.** `Write(...)`,
`NotebookEdit(...)` and `MultiEdit(...)` are inert — write `Edit(...)`, which
covers every file-editing tool. `Glob(...)` is inert too; use `Read(...)`. This
one does warn at startup, so start a session once after adding a file rule and
read the first screen.

The general lesson: a permission rule can only be verified against the running
product, never by inspecting the config.

## Adding a new gated command class

Three edits in `libexec/permission-gate.sh`, one place each: a `def_<key>` with
the shipped default, the key in `KEYS`, and an arm in `matches()`. The two
decision passes are data-driven and need no change. Then add the key to `SPEC`
in `libexec/policy`, or the CLI rejects it as unknown. Then tests.

Start every `matches()` arm with a cheap shell `case` pre-filter before its
`grep`:

```sh
docker) case $cmd in *docker*) ;; *) return 1 ;; esac; has_word docker ;;
```

The hook runs on every Bash call; the pre-filter keeps the common path from
forking a `grep` per key.

## Verify

```bash
luma-foreman policy doctor         # is it actually working on this machine
sh tests/run                       # hermetic: never touches your real config
jq . ~/.claude/settings.json       # still valid JSON
luma-foreman policy                # what the hook thinks the policy is here
```

`doctor` is the one to reach for first. `install` answers "is it wired up";
`doctor` answers "is it working", which is a different question and the one that
catches real breakage — a gate that is installed, wired, and silently returning
nothing looks perfect to `install` and protects you from nothing.

It runs the **installed** gate, the file Claude Code actually executes, against a
temporary policy directory, so it never reads or writes the policy you rely on.
Beyond wiring it checks that defaults fire, that ordinary commands are *not*
gated, that the always-tier survives `bypassPermissions`, that the gate refuses
writes to itself, that `deny` blocks, that policy changes apply with no restart,
that subdirectories resolve to the repository policy, and that a `deny` rule does
not block its own undo. It also warns about a stale gate left in `~/.claude`,
about `trust = "full"`, and about `policy_write` set below `always`.

Exercise the hook directly — `cwd` selects the project, and gated commands need
testing in both modes:

```bash
echo '{"tool_name":"Bash","cwd":"'"$PWD"'","tool_input":{"command":"sudo reboot"},"permission_mode":"default"}' \
  | ~/.config/luma/foreman/permission-gate.sh
```

A gate that stops firing after a policy edit is almost always one of: the value
is `allow` when you meant `ask`, `trust = "full"` is set on the project, or you
are looking at a different project than the hook is. `luma-foreman policy` prints
the resolved project path and the source of every value — check it first.
