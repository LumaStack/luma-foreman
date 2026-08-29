# luma-foreman

**Every repository set up right, and kept that way.**

Foreman moves knowledge, policy and workflows to where they're needed, it wires
up agents to use knowledge correctly, and verifies the knowledge remains true.

## How it works with catalogs

Everything a bundle *knows* — the layout a project should have, what tooling to
install, what policy a project should follow — belongs in a catalog, unless it's
truly specific to a single project. **A catalog holds knowledge; the foreman tool
helps transfer and enforce that knowledge.**

> **Status: early.** Getting, applying, inspecting and initializing work end to
> end. Interfaces still move.

## Why it exists

**A standard that lives only in prose is a standard that's easy to ignore.** Somebody
writes down how projects here are supposed to work, everyone agrees, and six
months later no two repositories look alike — because nothing carries the
standard into them and nothing noticed when it drifted.

Agents make that worse and better at once. Worse, because an agent that has not
been told a convention will confidently violate it. Better, because an agent
*will* follow a rule it is actually given — the problem was never willingness,
it was delivery.

**So foreman standardizes knowledge delivery.** It runs inside a repository that
may know nothing about any of it: copying knowledge in, applying it into each harness,
and reporting where each project falls short.

## What it looks like

```bash
luma-foreman init
luma-foreman get lumastack/luma-catalog/decision-records \
  --from https://github.com/LumaStack/luma-catalog
luma-foreman apply
```

A bundle is distributed knowledge containing workflows, policy, concepts, and more.
The `get` copies any bundle into `.luma/bundles/` with a receipt — version,
origin, catalog commit, checksum. The `apply` writes thin adapters into whatever
this project's harness reads, so an agent can use the knowledge bundle at the right time
without hand holding.

Everything is committed in git so agents can use history to learn and improve your process.

## Where to go next

- **[Getting started](docs/getting-started.md)** — install it, and run the loop
  above for real.
- **[Commands](docs/commands.md)** — every command, what it writes, and what it
  refuses to.
- **[Architecture](docs/architecture.md)** — the invariants, and where state
  lives. Read before adding a capability.

Requires Python 3.11+ and git. No dependencies, no build step.
