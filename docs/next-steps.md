# Next steps

**This file is consumable.** It says what to do next, it is worked through, and
then it is deleted. Anything in it that outlives the work belongs somewhere
durable *before* it is deleted — a decision, an idea, a bundle — not here.

Rewritten 2026-08-23. Everything previously here is either done, moved, or below.

---

## The goal

**Bundles load into a project's context automatically, and workflows can be
invoked, without anybody telling an agent where to look.**

Today the knowledge exists and nothing consumes it. A person points an agent at
`luma-catalog` by hand every time. That is the gap, and closing it is worth more
than any further design.

**Race toward wired-up.** Some of the building blocks were implemented naively,
incompletely, or wrong. Finding out which is the point — none of it has been run
end to end, so every part of the design is a guess until a project loads a bundle
and an agent uses it.

## What is already standing

- **15 bundles** in the catalog, all `0.x`, none adopted anywhere.
- **The format is at `v0.0.11`**, with vendoring, provenance and namespaced
  shared types settled this week.
- **`foreman inspect` and `agent-permissions` work.** `bootstrap`, `outfit` and
  `refit` exit 2.
- **Four repositories have `.luma/`** — a project descriptor and a backlog each.
  **None has `.luma/bundles/`**, and no `adopted.toml` exists anywhere.

## The path, in order

**1. `adopt`.** Copy a bundle from a catalog into `.luma/bundles/<org>/<name>/`,
write `adopted.toml` with source, version, commit and checksum. No resolution and
no dependency graph — bundles depend on nothing, which is what makes this a
directory copy rather than a package manager.

**2. Adopt one bundle into foreman itself**, and find out what the layout gets
wrong in a repository that already has opinions about its own files.
`luma/decision-records` is the suggestion: pure knowledge, no executable content,
so *did adoption work* has an unambiguous answer — and foreman records its
decisions nowhere today, so the bundle has a job the moment it lands.

**3. `outfit` — the projection.** This is the one that matters, because it turns
an adopted bundle into something a harness can actually use. **Thin adapters**:
a workflow becomes a Claude Code skill, and later a Codex equivalent, with the
adapter carrying the harness-specific shape and nothing else. `.claude/` is
generated and disposable — the source is `.luma/`.

**4. Loading.** What lands in context without being asked for. `preload` is
declarative and nothing reads it. Start by honouring `preload: mandatory` and
report the rest.

**5. Drift.** `inspect` compares the vendored copy against the checksum in
`adopted.toml`. This is what makes adoption mean something rather than being a
one-time copy.

## What is deliberately not on the path

- **Bundle dependencies.** Drafted, unadopted, and nothing depends on anything.
- **Conditional or situational loading.** Two backlog ideas cover it. Do the
  unconditional version first and find out whether the budget actually hurts.
- **A cataloger.** Designed in `luma-leader/docs/cataloger.md`, and publication
  is not an event yet, so there is nothing to gate.
- **Anything requiring a released artifact.** Foreman installs by clone and
  symlink and has no tags. That is a real problem and it blocks nothing here.

## Open questions this work will answer or sharpen

**Do the standards used to build luma tooling live outside luma tooling?** If
foreman's own release process lives in a bundle it has to adopt — is that elegant
or a permanent headache for maintainers? **Adoption is what settles it**, and
step 2 is the first real evidence.

**Will anything ship natively in foreman, or is everything fetched?** The same
question from the other side. It decides whether logging is a bundle.

**Does the projection design survive contact?** It has been reasoned and never
run. Step 3 is where it either works or teaches something.

## Before deleting this file

Check that nothing here has become durable and homeless. The last rewrite found
five items that would have been lost — they are now in `.luma/backlog/ideas/`.
