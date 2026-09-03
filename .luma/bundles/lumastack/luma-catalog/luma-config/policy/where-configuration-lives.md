---
type: policy
title: Where configuration lives
description: Two homes and one cache — what is committed, what belongs to the machine, and the test that tells them apart.
matches: eager
sources:
  - id: xdg
    resource: https://specifications.freedesktop.org/basedir-spec/latest/
    title: XDG Base Directory Specification
    author: team:freedesktop.org
  - id: direnv-move
    resource: https://github.com/direnv/direnv/blob/master/CHANGELOG.md
    title: direnv — per-directory approvals moved from XDG_CONFIG_HOME to XDG_DATA_HOME
---

# Where configuration lives

```
.luma/config/foreman.toml                         committed — what this project declares
~/.config/luma/luma-foreman/config.toml           yours, every project
~/.config/luma/luma-foreman/projects/<id>.toml    yours, this project
~/.cache/luma/luma-foreman/projects/<id>/         derived — safe to delete at any moment
```

## The rule of thumb

**`.luma/config/` is committed. `~/.config/<org>/` is not.**

That is the shape of it, and it holds almost always. The exception worth
allowing for: an operator who wants their own settings to travel between their
own machines may version `~/.config/` in a dotfiles repository. That is their
repository and their choice, and it does not make those settings part of any
project.

**What must never happen is the reverse** — something under `.luma/` that is
not committed. Committed-but-personal is somebody's private business;
uncommitted- but-in-the-project is two agents reading different rules for the
same code.

## Machine-local paths follow XDG

The [XDG Base Directory Specification][^xdg] is what decides these paths, and
it is worth reading once rather than guessing:

| | holds |
| --- | --- |
| `~/.config/<org>/<application>/` | **configuration** — things a person edits |
| `~/.local/share/<org>/<application>/` | **data** — things a program installs and manages |
| `~/.local/state/<org>/<application>/` | **state** — logs, history, work already done |
| `~/.cache/<org>/<application>/` | **cache** — regenerable, safe to delete |
| `~/.local/bin/` | **executables** — flat, because it has to be on `PATH` |

**`<application>` is never truncated.** The name in full, prefix included —
`~/.config/luma/luma-foreman/`, never `~/.config/luma/foreman/`. **A shortened
segment is the tell that a path drifted**, and it is the only mistake this
shape actually attracts.

**`~/.local/bin/` is the one genuine exception and the reason is mechanical:**
a binary nested under `~/.local/bin/<org>/<application>/` is not on `PATH` and
does not run. Nothing else here has a reason to be flat.

**State and cache are different tiers and folding them loses the test below.**
Logs and history are state; anything regenerable is cache. *If deleting it
loses a decision somebody made, it is not cache* — a rule that needs a cache
tier to point at.

### Why nest under the organization

`~/.config/luma/luma-foreman/`, so a directory maps to a repository with
nothing to translate.

**The specification does not choose this for you.** It says
`$XDG_CONFIG_HOME/subdir/filename` — generic placeholder language — and leaves
naming and depth to the application. Both flat and nested conform.

*This was argued more than once and settled on nesting. **What goes wrong in
practice is truncation, not the shape** — `luma/foreman` written for
`luma/luma-foreman` — and it goes wrong silently, because a path nobody wrote
to before is created on demand and nothing reports the old one is now empty.*

Flat is the common shape, but the tools usually cited for it are single-tool
vendors with nothing to nest under, which makes them poor evidence either way.
JetBrains ships several tools and nests across config, data and cache alike.

**What decides it is that a rule covering every tool has to be writable once:**

```json
"deny": ["Edit(~/.config/luma/**)", "Edit(~/.local/share/luma/**)"]
```

One entry per directory, no glob support required, and nothing to widen when a
second tool arrives. **The organization directory is what matches, so
application names are free** — a tool called `atlas` lands at
`~/.config/luma/atlas/` and is covered by the same rule.

The flat alternative needs one entry per application, or a `luma-*` wildcard
that holds only while every tool happens to be named `luma-something`. That is
a convention nobody commits to, and one product-named tool leaves no single
rule to write.

This matters beyond tidiness because such a rule **fails open**: a pattern
matching nothing produces no error and no warning.

Shared configuration across tools is **its own repository** —
`~/.config/luma/luma-shared/` — rather than something at the organization
level, so `<org>/<application>` holds without exception.

### Choosing between config, data and state

**The question is who authors the contents, not who writes the bytes.**

- A person opens it, reads it, and changes meaningful choices → **config**
- The program generates and manages it; a person never edits it → **data**
- It accumulates as a by-product of running — logs, caches, history → **state**

direnv settled this the hard way and is worth borrowing from: its per-directory
approvals began in `XDG_CONFIG_HOME` and were moved to `XDG_DATA_HOME`, on the
grounds that *the config folder should stay for user-editable
configuration*.[^direnv-move] Those files were hash-named opaque markers — a
record, not a document.

### The split is not cosmetic

**Program files must not live in the config directory.** Somebody clearing
`~/.config/<application>/` to reset their settings would otherwise delete
working code.

The sharp case: a permission gate installed under config. Clearing config
deletes the gate, a missing hook is a *non-blocking* error, and the tool call
proceeds — so a reset that looks entirely safe silently disarms the thing that
was protecting you. **A reset must not be able to disarm anything.**

### Moving a path is a user-visible event

Changing where a tool keeps its files breaks whatever points at the old
location. Report the old directories, say what has to happen and in what order,
and **do not delete them** — the previous location may still be wired up
somewhere, and removing it first leaves a gap rather than a migration.

*This is the one place `.luma/` and the machine-local side differ in shape, and
the reason is that they answer to different authorities. `.luma/` is one
directory because a project has one set of rules. The machine-local side is one
directory per application because XDG says so and every other tool on the
machine agrees.*

## The test that decides which

**If deleting it loses a decision somebody made, it is not cache.**

That single question resolves almost every case. A timeout somebody tuned is
configuration. A parsed index is cache. Putting a decision under a cache path
means clearing caches silently reverts behaviour with no trace of why — and
nobody suspects the cache, because caches are supposed to be safe to clear.

## Only one kind of configuration is committed

**Declarations** are the project stating its own rules: which policies apply,
which exemptions were granted, what *done* means here. They are the same
statement as a policy document, in machine-readable form. **Committed**, in
`.luma/config/`.

**Machine-local settings** are timeouts, log levels, cache locations,
concurrency, and whichever mode an operator prefers. They belong to a person on
a machine rather than to the project, and they live under `~/.config/luma/`
where no repository can see them.

**Everything in `.luma/` is committed. No exceptions.** If uncommitted files
can live there, a reader cannot distinguish an authoritative rule from
somebody's local tweak, and two agents on two machines read different rules for
the same project — a correctness failure in the one place whose job is saying
what the rules are.

*The tempting alternative is a gitignored `foreman.local.toml` sitting beside
the committed one, which several tools do and which is more ergonomic. It is
not taken here for exactly the reason above: an uncommitted file inside
`.luma/` breaks the promise the directory exists to make.*

## Machine-local settings are keyed by an identifier, not a path

```toml
# .luma/config/foreman.toml — committed
id = "8f2c1e9a"
```

A checkout path breaks the moment a repository moves or somebody makes a second
clone. A remote URL breaks for repositories that have none, or that get
migrated. **The identifier is the only durable key**, so it is generated once
and committed.

**Committing an identifier is not committing the settings.** The identifier
says *which project this is*; what a particular operator chose for it stays on
their machine.

## Name files for the tool that reads them

`foreman.toml`, not `config.toml`, inside `.luma/config/`. Several tools will
eventually write there, and a shared file means they negotiate a schema — which
is a coordination problem nobody needs when a filename solves it.

`~/.config/luma/config.toml` is the exception and keeps the generic name,
because it holds settings that are not any one tool's.

## Configuration references secrets; it never holds them

A value is an environment variable name, a path, a keychain reference — never
the secret itself. `.luma/` is committed, so a secret written there is a secret
published, and no amount of care afterwards unpublishes it.

## Vendor configuration is generated

`.claude/settings.json` and its equivalents stay wherever their tool looks for
them, and are **generated from what is in `.luma/config/`** rather than
maintained by hand.

Editing a generated file means editing something that will be overwritten. If
the value should be different, change what generated it.
