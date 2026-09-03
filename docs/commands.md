# Commands

Verbs that act, nouns that only report, and a permissions subsystem that shares
none of their machinery.

Most commands take `--to <project>` to work on a repository other than the
current one — `inspect` takes a positional path instead, and
`agent-permissions` takes neither.

**Exit code 0 means fine and 2 means the command could not run.** What 1 means
is the command's own: refused, stale, behind, or findings present. Each section
below says.

## init — stand `.luma/` up

```bash
luma-foreman init
luma-foreman init --catalog <source>    # ...and record where bundles come from
```

Creates `.luma/PROJECT.md` and `.luma/config/luma-foreman.toml`, **and nothing
else**. `bundles/` appears on the first `get`, `records/` on the first decision
or audit.

**No empty directories, deliberately.** An empty directory is a question a
reader has to answer, and git will not commit one anyway.

**No `.gitignore` entry either** — `.luma/` is committed in full, and a project
whose `.luma/` differs between two machines is two projects.

Idempotent: run it again and it adds what is missing.

## get — take a bundle

```bash
luma-foreman get lumastack/luma-catalog/decision-records \
  --from https://github.com/LumaStack/luma-catalog
luma-foreman get <bundle> --force       # replace a copy that no longer matches
```

`--from` takes a catalog checkout or a git URL, and defaults to `[catalog]
source` in the project config.

**A fetch with a receipt.** The bundle lands in
`.luma/bundles/<namespace>/<bundle-name>/` — the namespace derives from the
catalog's address (`lumastack/luma-catalog`), so two catalogs from one
organization vendor side by side — and `MANIFEST.md` records the version, origin,
catalog commit, and a checksum of exactly what landed.

**Nothing is fetched later.** Commit the copy — a fresh clone with no network
then reproduces the project exactly.

**A bundle with no version cannot be adopted at all**, because a project holding
one could say nothing honest about what it has.

**The namespace is the catalog's**, derived from where it lives:
`github.com/LumaStack/luma-catalog` becomes `lumastack/luma-catalog`, unless
`CATALOG.md` declares one, which wins. A fork gets its own namespace without
anybody arranging it.

## apply — put it where an agent will meet it

```bash
luma-foreman apply
luma-foreman apply --check       # is anything stale? exit 1 if so, write nothing
luma-foreman apply --explain     # what each Document derives to, and from what
```

Writes a skill per procedure, `.luma/bundles/INDEX.md` naming everything
adopted, and a managed block in `CLAUDE.md` pointing at it.

**Thin adapters, never copies.** Each skill points at the real document under
`.luma/` and names the standing context that document assumes.

**Only the region between the `luma:begin` and `luma:end` markers is touched**,
so a hand-written file keeps the rest. Everything written is generated and
disposable — commit it or gitignore it, but regenerate rather than edit.

**`--check` answers *is this stale*, not *what would change*.** It writes
nothing and exits 1 when a regenerate is due, which is what makes it a gate — the
same sense `black`, `prettier` and `rustfmt` give the flag, rather than Ansible's
dry run.

## inspect — check the project

```bash
luma-foreman inspect                # 0 nothing found, 1 findings, 2 could not run
luma-foreman inspect --json         # machine-readable, for continuous integration
luma-foreman inspect --rule adoption
```

Checks a repository against the baseline and reports where it falls short.
**Every check works in a bare clone with no configuration.**

### What each rule catches

| rule | catches |
| --- | --- |
| **identity** | personal information published through git — machine-derived author identities, malformed addresses, home directory paths in tracked content |
| **secrets** | provider-issued credentials in tracked content, and files that normally hold them. Findings never quote the secret, because they end up in continuous integration logs |
| **vocabulary** | words this project retired, still in use. Notices only — see below |
| **bundles** | dangling links, unquoted wikilinks in frontmatter, templates carrying live frontmatter. **A bundle with any of these still validates**, so nothing else reports it and the defect travels to every adopter |
| **adoption** | a bundle edited in place, missing from disk, or **adopted and never written anywhere an agent reads**. The last passes every other check: present, checksum matching, nothing edited, and no agent has seen a line of it |

### Notices

**A notice is worth a reader's judgement without being a defect.** It prints as
loudly as a finding and **never changes the exit code**, so a check that cannot
be certain can speak without blocking a merge — which is what stops somebody
disabling it.

**`vocabulary` emits nothing else.** A grep cannot tell a revival from an
ordinary use of the same word, so it hands over the term, what replaced it,
where that was decided, and the line. Nothing is retired by default.

### Skipped checks never pass

**An inspection that reads clean while silently skipping half
its checks is worse than no inspection**, because it manufactures confidence
nobody earned.

## bundle — what this project holds

```bash
luma-foreman bundle list
luma-foreman bundle show <name>      # one bundle's receipt and contents
luma-foreman bundle outdated         # which have a newer version published
```

**`list` and `show` read committed state and work offline. `outdated` reaches
each bundle's catalog and needs a network.**

## catalog — where knowledge comes from

```bash
luma-foreman catalog list
luma-foreman catalog show <name>     # what a catalog publishes
```

`<name>` is a short name from `list`, a path to a checkout, or a git URL.

**`list` is derived from what has been adopted and works offline; `show` reaches
the catalog and needs a network.**

## agent-permissions — what an agent may do here

```bash
luma-foreman agent-permissions              # the effective permissions here
luma-foreman agent-permissions allow curl   # ...and change one
luma-foreman agent-permissions doctor       # ...and confirm it is actually working
luma-foreman agent-permissions install      # install or update the gate
```

Per-project control over what an agent may do, changed by command rather than by
editing configuration.

**Claude Code already has per-project permission rules.** What this adds is
decisions those rules cannot express, because they match a command string and
this reasons about one:

| | |
| --- | --- |
| **a floor that survives bypass** | `always` prompts in every mode, `bypassPermissions` included. A skip-permissions run cannot lift it |
| **rules that read the command** | `safe` on `curl`/`wget` allows a plain fetch and prompts when the command writes to disk, uploads a body, or pipes into an interpreter |
| **rules that consult a list** | `trusted` on `ssh` allows a host in `ssh_hosts` and prompts for everything else |
| **a mode** | `trust: full` silences every `ask` at once, without touching each key |

`allow` means *no opinion* — the normal Claude Code flow decides. `deny` refuses
outright in every mode.

**Changes take effect on the next tool call**, because the hook re-reads these
files each time it runs. Hook *wiring* is the exception and needs a restart.

**See [Agent permissions](claude-agent-permissions.md)** for the model, the keys,
and how the gate decides.
