# Standards

This is a temporary stop gap until we have a proper standards system + ecosystem.

## For distributed tooling, follow XDG standards

XDG is explicit about where config, data, and executables live:

- `~/.config/<application>/` — configuration: things the user edits
- `~/.local/share/<application>/` — data: things a program installs and manages
- `~/.local/state/<application>/` — state: logs, history, caches of work done
- `~/.local/bin/` — executables

### Name the directory after the application, not the vendor

`~/.config/luma-foreman/`, not `~/.config/luma/foreman/`.

XDG says `$XDG_CONFIG_HOME/<application>/`, and nearly every tool follows it —
`gh`, `git`, `kitty`, `chezmoi`, `nvim` are all flat. A vendor level also
contradicts the point of a standalone tool: a path that reads `luma/foreman`
implies a suite the user may never install.

Shared configuration across tools, if it is ever wanted, is its own application
— `~/.config/luma-shared/` — sitting beside the others rather than above them.
Nothing nests under a vendor.

### Deciding between config, data and state

The question is **who authors the contents**, not who writes the bytes.

- A human opens it, reads it, and changes meaningful choices → **config**
- The program generates and manages it; a human never edits it → **data**
- It accumulates as a by-product of running: logs, caches, history → **state**

direnv settled this the hard way and is worth borrowing from. Its per-directory
approvals started in `XDG_CONFIG_HOME` and were moved to `XDG_DATA_HOME`, with
the reasoning: *"it's better to keep that folder for user-editable configuration,
so the data is being moved."* Those files are hash-named opaque markers — a
record, not a document.

Applied to `luma-foreman`: per-project policy is config (you wrote `curl =
"deny"`, and `policy edit` opens it in your editor); the installed gate is data
(generated, overwritten on every upgrade, never hand-edited).

### The split is not cosmetic

Program files must not live in the config directory. Someone clearing
`~/.config/<application>/` to reset their settings would otherwise delete
working code — and for a permission gate that fails open, because a missing hook
is a non-blocking error and the tool call proceeds. A reset that looks safe must
not disarm anything.

### Migrating a path is a user-visible event

Changing where a tool keeps its files breaks anything pointing at the old
location. Report the old directories, say what has to happen and in what order,
and do not delete them — the previous location may still be wired up, and
removing it first leaves a gap.
