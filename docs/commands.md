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
luma-foreman get lumastack/luma-catalog/decision-records
luma-foreman get <bundle> --from <catalog>   # a catalog nobody registered
luma-foreman get <bundle> --force            # replace a copy that no longer matches
```

**Without `--from`, the bundle ID resolves itself.** It starts with the name
of the catalog that publishes it, so `get` prefix-matches it against the
registered catalogs in `.luma/config/luma-foreman.toml`, then falls back to
the source an existing receipt records, then to the bare `[catalog] source`
default. The registry outranks the receipt deliberately: a moved catalog
makes the registry current truth and the receipt history.

**A fetch with a receipt.** The bundle lands in
`.luma/bundles/<namespace>/<bundle-name>/` — the namespace derives from the
catalog's address (`lumastack/luma-catalog`), so two catalogs from one
organization vendor side by side — and `MANIFEST.md` records the version,
catalog commit, a checksum of exactly what landed, and where it came from: the
catalog's *name* when it is registered, so a moved catalog is one config line
rather than every receipt going stale, or the raw source when it is not —
like a hand-installed .deb.

**Nothing is fetched later.** Commit the copy — a fresh clone with no network
then reproduces the project exactly.

**A bundle with no version cannot be adopted at all**, because a project holding
one could say nothing honest about what it has.

**The namespace is the catalog's**, derived from where it lives:
`github.com/LumaStack/luma-catalog` becomes `lumastack/luma-catalog`, unless
`CATALOG.md` declares one, which wins. A fork gets its own namespace without
anybody arranging it.

## remove — drop a bundle

```bash
luma-foreman remove lumastack/luma-catalog/git-secrets
luma-foreman remove local/widgets --force
```

The inverse of `get`, and shaped like it: one bundle ID, this project only,
finished the moment it returns. A bare name works where only one namespace
holds it.

**It refuses when removing would lose work nothing else holds.** That is one
rule covering two cases — a bundle written here that is not committed, and a
vendored copy somebody edited. Everything else is recoverable, and the output
says how: `get` restores a clean vendored copy byte-identical, git restores a
committed local one, and the literal command to do it is printed.

**Exit 1 also means something still points at it.** Removing a bundle turns
anything citing it into a dangling reference, and the files are named. `inspect`
catches a dangling wikilink afterwards; a bundle cited as a bare path in prose
is exactly what it does not catch.

Run `apply` afterwards, so the generated skills and the project index stop
naming what left.

## publish — offer a bundle to a catalog

```bash
luma-foreman publish command-line-interface lumastack/luma-catalog
luma-foreman publish command-line-interface lumastack/luma-catalog --again
luma-foreman publish command-line-interface --abandon
```

**Two operands, because where a bundle is going is not in its name.** `get` and
`remove` need one ID since the namespace already says which catalog; a bundle
written here has no namespace to read, and the same bundle may legitimately go
to more than one catalog.

**Publishing is a custody handover.** Once the bundle lands, this project stops
owning it and starts vendoring it like anything else — the bare manifest entry
becomes a receipt, and editing the bundle afterwards is drift rather than
authorship.

**It is one idempotent command, run whenever.** It advances the handover as far
as it can and says where it stopped: opening a pull request against the
catalog, reporting one still under review, or — once a maintainer has merged
it — taking the published bundle back and retiring the local one. To read the
state without advancing anything, use `bundle show`.

**The only automatic transition is the merged one.** A declined request, or one
that is no longer visible, reports and changes nothing. A 404 is not proof of
rejection — it also means moved, private, or a token that expired — so the
possibilities are named rather than guessed between, and asking again takes
`--again` so a maintainer is never sent a duplicate nobody decided to send.

**A bundle keeps its `local/` identity until the merge**, because until then it
has not been published. A namespaced entry always carries a checksum and says
where it came from; `inspect --rule adoption` reports one that does not.

Opening a request needs `gh`, authenticated, and write access to the catalog.

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
luma-foreman catalog add <source>    # register one, so `get` needs no --from
```

`<name>` is a registered name, a short name from `list`, a path to a
checkout, or a git URL.

**`add` registers a catalog the way apt registers a source** — once,
committed, by the namespace it serves. The name is never an argument: `add`
fetches the catalog and asks, which is what verifies the entry at write time
instead of in a teammate's `get` next week. Same name and source again is a
no-op; the same name from a different source is refused, naming the entry it
would shadow.

**`list` reads the registry and the receipts and works offline; `add` and
`show` reach the catalog and need a network.**

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
