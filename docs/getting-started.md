# Getting started

Requires **Python 3.11+** and **git**. No dependencies to install, no build step.

## Install

```bash
git clone https://github.com/LumaStack/luma-foreman.git
ln -s "$PWD/luma-foreman/bin/luma-foreman" ~/.local/bin/luma-foreman   # or add bin/ to PATH
```

That is enough for everything except the permission gate, which needs one more
step and one manual edit.

## Wire up the permission gate

```bash
luma-foreman agent-permissions install
```

This installs the gate into `~/.local/share/luma/luma-foreman/` and then
**prints** the two changes to make in `~/.claude/settings.json`. It does not edit
that file, and the refusal is deliberate: foreman writes freely into directories
it owns and never silently edits configuration you own.

**The settings edit is the only thing you do by hand**, and `install` shows you
exactly what. Hook wiring needs a Claude Code restart to take effect; policy
changes after that are live.

**Re-run `install` after every upgrade.** It is idempotent and says when there is
nothing to do.

Confirm it actually works rather than merely being wired up:

```bash
luma-foreman agent-permissions doctor
```

## Run the loop

From inside a repository you want to set up:

```bash
luma-foreman init                                    # if .luma/ does not exist yet

luma-foreman catalog show https://github.com/LumaStack/luma-catalog
luma-foreman get lumastack/luma-catalog/decision-records \
  --from https://github.com/LumaStack/luma-catalog
luma-foreman apply

luma-foreman bundle list
```

**Commit what `get` wrote.** An adopted bundle lives in the repository — that is
what lets a fresh clone with no network reproduce the project exactly.

**What `apply` writes is generated and disposable.** Commit it or gitignore it,
but regenerate rather than edit.

## Check the project

```bash
luma-foreman inspect
```

Runs in a bare clone with no configuration. See [Inspect](inspect.md) for what
each check catches and how it behaves in continuous integration.

## Run the tests

```bash
sh tests/run
```

**Hermetic** — `HOME` and `LUMA_FOREMAN_HOME` are redirected into temporary
directories, so running them never touches your configuration.
