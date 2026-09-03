---
type: luma/idea
title: Catalogs as registered sources, the way apt has sources.list
created: { by: human:benlinton, at: 2026-09-03T00:00:00Z }
contributors: [human:benlinton, agent:claude-fable-5]
horizon: next
scope: project
stage: draft
---

# Catalogs as registered sources, the way apt has sources.list

**Register a catalog once, then `get` bundles without restating the source.**
The model is apt: sources say where things come from, the installed-state says
what you have, and neither restates the other.

| apt | foreman |
| --- | --- |
| `sources.list` | catalog registry in `.luma/config/luma-foreman.toml` |
| `apt install foo` | `get <bundle-id>` |
| dpkg's installed-state | `MANIFEST.md` |
| installing a local .deb | `get --from <url>` |

## The settled shape

- **Registry in foreman's own config**, committed — evolving the existing
  `[catalog]` section into named entries:

  ```toml
  [catalog."lumastack/luma-catalog"]
  source = "https://github.com/LumaStack/luma-catalog"
  ```

- **Receipts go name-indirect.** A receipt records the catalog *name* plus
  what it already pins — version, catalog commit, checksum — and the registry
  owns name→URL. A moved catalog is one config line, not every receipt going
  stale. A `--from` fetch from an unregistered catalog keeps its raw URL,
  like a hand-installed .deb.

- **Resolution order for `get`:** explicit `--from`, then the registry by
  prefix-matching the bundle id against registered catalog names, then the
  receipt's recorded source (pre-registry adoptions). Registry beats receipt
  because a moved catalog makes the registry current truth and the receipt
  history.

- **`catalog add <url>` verifies at add time** — fetches and checks the URL
  serves the namespace it claims, so a wrong sources entry fails when
  written, not when a teammate runs `get` next week. Same name + same URL is
  an idempotent no-op; same name + different URL is an error naming the
  existing entry.

## Rejected, with reasons

- **Two-arg `get <catalog> <bundle>`.** Bundle ids embed their catalog's
  namespace, so the one-arg id already contains everything resolution needs,
  and it stays copy-paste identical to MANIFEST.md, INDEX.md and receipts.
- **Registry in PROJECT.md frontmatter.** `luma/project` is a shared type
  read by other tools; which catalogs foreman pulls from is tool
  configuration, not project identity, and foreman's own config file can
  evolve without shared-type ceremony.
- **An `apt update`-style index cache.** Catalogs are git repositories
  fetched at `get` time; browsing is another tool's job — see
  [[browsing-a-catalog-is-an-engines-job]].
- **Pinning and priorities.** Apt needs them because package names are flat;
  namespaced bundle ids make ambiguity structurally impossible.
