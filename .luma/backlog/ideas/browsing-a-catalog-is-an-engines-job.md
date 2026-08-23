---
type: luma/idea
title: Browsing a catalog is an engine's job, not a catalog's
created: { by: human:benlinton, at: 2026-08-18T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: someday
scope: project
lifecycle_status: draft
---

# Browsing a catalog is an engine's job, not a catalog's

A web interface for browsing bundles is wanted eventually. It must not live
inside a catalog.

An organization with a private catalog wants the same view of its own bundles.
A browser that lives inside the universal catalog is welded to that catalog's
content, so every organization wanting it has to fork — which is the thing the
architecture spends its effort avoiding. **A browser has to point at *a*
catalog, not be a feature of *the* catalog**, for the same reason foreman is
separate from an hq: it has to run against content it does not contain.

Whether that is its own repository or a foreman capability is open. Foreman is
already what talks to catalogs at apply time, and `list what is available here`
is close to `outfit` and `refit` in what it has to read, so a subcommand may
earn it before a second program does.

A secondary reason to keep it out regardless: an application gives the one
repository that is meant to be pure content a dependency tree, a lockfile, a
build, and a vulnerability feed. Every organization fetches content from that
repository. Dependency alerts on a catalog are a category error.

If the browser is a static site, the answer is the same with different
mechanics — the generator is an engine and lives elsewhere; the output is a
build artifact and is not committed to the content branch.

## Notes

Migrated from `docs/IDEAS.md` on 2026-08-21. `created.at` is a day-level
estimate from git history.

**The constraint this argues for has since become a settled decision, reached
independently.** `luma-leader/docs/DECISIONS.md`, *"Only the engines are never forked;
everything else is yours"* — settled 2026-08-18, clarified 2026-08-21 — names
`luma-leader` and `luma-foreman` as the engines and everything else, bundles and
catalogs included, as forkable. A browser is engine-shaped, so it cannot be
catalog content. The conclusion here holds.

**One phrase above is off against that decision.** Forking is not *"the thing the
architecture spends its effort avoiding"* — forking is expected for everything
except the engines. The argument survives: the objection is that an organization
would be forking to obtain a *feature* rather than to own content. Left as
written rather than corrected, since the entry is the record of what was thought
at the time.

**A related decision already anticipates this.** The same file calls bundle
categories *"browsing metadata, not routing"* and pre-commits a shape: *"if
browsing gets hard, that is a multi-valued field, never a directory."* Whoever
builds this inherits that constraint.

**If it becomes its own repository rather than a foreman subcommand**, the
question of which repository the organization needs belongs to `luma-leader`,
which holds an idea called *decide what to build next* covering exactly that.
Filed here because the decision to build it gets made against foreman's scope
first.
