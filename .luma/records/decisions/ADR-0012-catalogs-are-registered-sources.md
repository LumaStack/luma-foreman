---
type: decision
title: Catalogs are registered sources
decided: 2026-09-03
stage: draft
reopen_trigger: A project needs two registered catalogs to serve one namespace — mirrors, or a staged migration — which the one-name-one-source registry cannot express and pinning or priorities would.
---

# ADR-0012: Catalogs are registered sources

Register a catalog once, then `get` bundles without restating the source. The
model is apt: sources say where things come from, the installed-state says
what you have, and neither restates the other.

| apt | foreman |
| --- | --- |
| `sources.list` | catalog registry in `.luma/config/luma-foreman.toml` |
| `apt install foo` | `get <bundle-id>` |
| dpkg's installed-state | `MANIFEST.md` |
| installing a local .deb | `get --from <url>` |

## Problem

Every `get` without a receipt behind it needed `--from`, restating a URL the
project had already decided on. The derived catalog set answered *where does
my knowledge come from* but nothing answered *where should it come from* —
a teammate's first `get` in a cloned project had no way to resolve a bundle
ID except finding the URL in prose. And a receipt recording a raw URL goes
stale the day the catalog moves: eighteen receipts, eighteen edits.

## Decision

**The registry lives in foreman's own config, committed** — the existing
`[catalog]` section grown into named entries:

```toml
[catalog."lumastack/luma-catalog"]
source = "https://github.com/LumaStack/luma-catalog"
```

**A catalog's registered name is its namespace**, declared-beats-derived,
exactly as `get` already resolves it. The name is never an argument to
`catalog add` — it is what the catalog answers when asked, which is what
makes the entry verified rather than asserted.

**Receipts go name-indirect.** A receipt records the catalog *name* plus what
it already pins — version, catalog commit, checksum — and the registry owns
name-to-URL. A moved catalog is one config line, not every receipt going
stale. A `--from` fetch from an unregistered catalog keeps its raw URL, like
a hand-installed .deb. Exactly one of `catalog:` and `source:` appears on an
entry, because a receipt restating what the registry owns would go stale
with it.

**Resolution order for `get`:** explicit `--from`, then the registry by
prefix-matching the bundle ID against registered names, then the receipt's
recorded source, then the bare `[catalog] source` default. Registry beats
receipt because a moved catalog makes the registry current truth and the
receipt history.

**`catalog add <source>` verifies at add time** — it fetches and learns the
namespace the source serves, so a wrong entry fails when written, not when a
teammate runs `get` next week. Same name + same source is an idempotent
no-op; same name + different source is a refusal naming the existing entry.
A catalog claiming `local/` is refused — [[ADR-0011-local-bundles-live-under-local]]
reserves it for bundles with no published identity.

## Why

**The bundle ID already carries the routing.** IDs start with the namespace
of the catalog that publishes them, so a registry keyed by namespace resolves
any ID with a prefix match — nothing new to type, and the ID stays
copy-paste identical across MANIFEST.md, INDEX.md and receipts.

**The catalog name is the unrecoverable fact; the URL is derived.**
[[ADR-0009-the-manifest-records-custody-and-intent]] says the manifest
records what cannot be recomputed. Which catalog a bundle came from is
custody and cannot be recovered; where that catalog lives today is the
registry's single answer, and a receipt repeating it would be the derived
state ADR-0009 keeps out. The manifest's line grammar absorbs this as ADR-0009
predicted: unknown sublines are ignored on read, so `catalog:` is a behavior
change, not a format change — old receipts keep working, and an older foreman
reading a new receipt sees a bundle it can still verify.

**The registry is not a fetch-later mechanism.** Adoption stays a copy with
a receipt ([[ADR-0002-mvp-bundle-distribution]]); the registry only answers
where `get` reaches at the moment it runs. A bare clone with no network
still reproduces the project exactly, because nothing about resolution
happens after the copy lands.

## Alternatives

**Two-arg `get <catalog> <bundle>`.** Rejected: bundle IDs embed their
catalog's namespace, so the one-arg ID already contains everything
resolution needs.

**Registry in `PROJECT.md` frontmatter.** Rejected: `luma/project` is a
shared type read by other tools; which catalogs foreman pulls from is tool
configuration, not project identity, and foreman's own config file can
evolve without shared-type ceremony.

**An `apt update`-style index cache.** Rejected: catalogs are git
repositories fetched at `get` time; browsing is another tool's job — see
[[browsing-a-catalog-is-an-engines-job]].

**Pinning and priorities.** Rejected: apt needs them because package names
are flat; namespaced bundle IDs make ambiguity structurally impossible. The
re-open trigger above is the case that would change this.

**Migrating existing receipts to name-indirect on the next `get`.** Not
taken up here either way — a re-take through the registry naturally rewrites
the receipt name-indirect, and a receipt nobody re-takes keeps its raw URL
and keeps working.

## Standing consequences

**`add` is the one `catalog` command that writes.** It acts on the project
the way `get` does, and its exit codes follow the same convention — 0 fine
or idempotent no-op, 1 refused, 2 could not run. Everything else under the
noun only reports.

**`init`'s blank config points at `catalog add`** beside the commented
default. The bare `[catalog] source` stays read — a config that quietly
stopped being read would fail open.

**A registered entry is committed, so what it records must travel.** `add`
records the catalog's origin URL as `find` resolves it; registering a
checkout with no remote records a machine-local path, which works and is the
operator's own call to commit.

## References

The shape was settled in [[catalogs-as-registered-sources]], which carries
the apt table this record opens with.
