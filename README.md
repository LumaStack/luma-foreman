# luma-foreman

**Every repository set up right, and kept that way.**<br>
Provide each project with consistent governance and predictable intelligence. 

Foreman moves knowledge, policy and procedures to where they're needed, it wires
up agent harnesses to utilize knowledge correctly, and verifies the knowledge 
remains true.

## Why it exists

**A standard that lives only in text is a standard that's easy to ignore.** Somebody
writes down how projects here are supposed to work, everyone agrees, and six
months later no two repositories look alike — because nothing carries the
standard into them and nothing noticed when it drifted.

An agent that has not been told a convention will confidently violate it. 
But an informed and governed agent *will* follow a rule it is actually given 
— the problem was never willingness, it was delivery.

**So foreman standardizes knowledge delivery.** It runs inside a repository: copying knowledge in, applying it into each harness, and reporting back where a project 
falls short.

## How it works with catalogs

A bundle belongs in a catalog, unless it's truly specific to a single project. 
**A catalog holds a library of knowledge; the foreman tool helps transfer 
and enforce that knowledge.**

## What it looks like

```bash
luma-foreman init
luma-foreman get lumastack/luma-catalog/decision-records \
  --from https://github.com/LumaStack/luma-catalog
luma-foreman apply
```

A bundle is distributed knowledge containing policy, procedures, and more.
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
