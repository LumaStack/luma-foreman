# Standards

This is a temporary stop gap until we have a proper standards system + ecosystem.

## For distributed tooling, follow XDG standards

XDG is explicit about where config, data, and executables live:

- `~/.config/<application>/` — configuration: things the user edits
- `~/.local/share/<application>/` — data: things a program installs and manages
- `~/.local/state/<application>/` — state: logs, history, caches of work done
- `~/.local/bin/` — executables

### Nest under the organization, then the repository name

```
~/.config/luma/luma-foreman/
~/.local/share/luma/luma-foreman/
~/.cache/luma/luma-foreman/
```

**`<org>/<repo>`, and the second segment is the repository name exactly** —
prefix included, nothing translated. A directory maps to a repository by
inspection.

**The specification does not choose this for us.** It says
`$XDG_CONFIG_HOME/subdir/filename`, generic placeholder language, and leaves
naming and depth to the application. Both shapes conform.

Flat is the common shape — `gh`, `git`, `kitty`, `nvim` — and the reason is that
those are single-tool vendors with nothing to nest under, which makes them poor
evidence either way. JetBrains ships several tools and nests across config, data
and cache alike.

**What decides it is that a rule covering every tool has to be writable once.**

```json
"deny": ["Edit(~/.config/luma/**)", "Edit(~/.local/share/luma/**)"]
```

One entry per directory, covering everything the organization ships, needing no
glob support and no edit when a second tool arrives.

**The organization directory is what the rule matches, so the repository name is
free.** A tool called `atlas` lands at `~/.config/luma/atlas/` and is covered by
the same rule as everything else. Nothing has to be named `luma-anything` for
the pattern to hold.

Flat cannot offer that. It needs one entry per application, or a `luma-*`
wildcard — and **the wildcard holds only while every tool happens to be named
`luma-something`, a convention nobody has committed to.** One tool named for a
product and there is no single rule left to write.

That matters more than tidiness because the rule in question **fails open**: a
pattern matching nothing produces no error and no warning, and the first sign is
an agent editing the policy that governs it.

*An earlier version of this section argued the opposite, on two grounds that did
not survive: that the specification mandates flat, which it does not, and that a
path reading `luma/foreman` implies a suite the user may never install — true
when foreman stood alone, and no longer true now that there is a catalog, a
headquarters, a format, and shared configuration anticipated in this very
document.*

Shared configuration across tools sits beside the others as its own repository —
`~/.config/luma/luma-shared/` — rather than at the organization level, so the
`<org>/<repo>` shape holds without exception.

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
