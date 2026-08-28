# Commands

Four verbs that act, two nouns that only report, and one subsystem that shares
none of their machinery.

Every command takes `--to <project>` to work on a repository other than the
current one. Exit codes are consistent: **0 fine, 1 something is wrong or
behind, 2 could not run.**

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
luma-foreman get <bundle> --force       # overwrite a copy edited here
```

`--from` takes a catalog checkout or a git URL, and defaults to `[catalog]
source` in the project config.

**A directory copy with a receipt.** The bundle lands in
`.luma/bundles/<org>/<name>/`, and `adopted.toml` records the version, origin,
catalog commit, and a checksum of exactly what landed.

**Nothing resolves and nothing is fetched later.** Bundles depend on nothing,
which is what keeps this a copy rather than an install. Commit it — a fresh
clone with no network then reproduces the project exactly.

**An edited copy is never silently overwritten**, and a bundle with no version
cannot be adopted at all.

**The namespace is the catalog's**, derived from where it lives:
`github.com/LumaStack/luma-catalog` becomes `lumastack/luma-catalog`, unless
`CATALOG.md` declares one, which wins. A fork gets its own namespace without
anybody arranging it.

## apply — put it where an agent will meet it

```bash
luma-foreman apply
luma-foreman apply --check       # report what would change, write nothing
luma-foreman apply --explain     # what each Document derives to, and from what
```

Writes a skill per workflow, `.luma/bundles/entrypoint.md` naming everything
adopted, and a managed block in `CLAUDE.md` pointing at it.

**Thin adapters, never copies.** Each skill points at the real document under
`.luma/` and names the standing context that document assumes.

**Only the region between the `luma:begin` and `luma:end` markers is touched**,
so a hand-written file keeps the rest. Everything written is generated and
disposable — commit it or gitignore it, but regenerate rather than edit.

`--check` exits 1 on staleness, which is what makes it usable as a gate.

## inspect — check the project

```bash
luma-foreman inspect
luma-foreman inspect --json
luma-foreman inspect --rule adoption
```

Checks a repository against the baseline and reports where it falls short.
**Works in a bare clone with no configuration**, and a check that cannot run is
reported as skipped, never as a pass.

**See [Inspect](inspect.md)** for what each rule catches, and for the third
outcome — a *notice*, which prints as loudly as a finding and never changes the
exit code.

## bundle — what this project holds

```bash
luma-foreman bundle list
luma-foreman bundle show <name>      # one bundle's receipt and contents
luma-foreman bundle outdated         # which have a newer version published
```

**`list` and `show` read committed state and work offline. `outdated` reaches
each bundle's catalog and does not.**

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

Per-project control over what Claude Code may do. **Claude Code's own permission
rules are global; this adds a per-project layer**, so loosening a rule for one
repository does not loosen it everywhere.

**Changes take effect on the next tool call** — no session restart, because the
hook re-reads these files each time it runs. Hook *wiring* is the exception and
needs a restart.

**This shares no machinery with adoption** and would work identically if bundles
had never existed. It is in the same binary because it is the same operator
working on the same repository.

**See [Agent permissions](claude-agent-permissions.md)** for the model, the keys,
and how the gate decides.
