# luma-foreman

Predictable intelligence and reliable governance, for every project.

- Seamlessly distribute your knowledge, policy and procedures between projects
- Effortlessly wire up each agent harness — so it uses your knowledge correctly
- Continuously verify our shared knowledge remains true

## Why use Foreman

**Standards are easy to ignore.** Somebody writes down how projects are
supposed to work, everyone agrees — and six months later no two repositories
look alike. The standards spread through best intentions, which means drift
and failure are inevitable.

An agent either amplifies this problem or becomes the solution. An unaware
agent will confidently violate the standards everyone agreed to; an informed
agent will uphold them just as confidently — in every project, every time.
Agents can solve our standards problems once and for all through reliable
distribution and governance.

**So foreman standardizes knowledge delivery** for agents. It runs inside a
repository: distributing shared knowledge, wiring up each harness, and
reporting back when a project falls short.

## What usage looks like

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

## Where distributed knowledge lives

A shared **bundle** is usually found inside a **catalog**. You can think of a
catalog as a library of knowledge; and the foreman tool helps distribute
individual knowledge bundles to each project that needs them.

## Where to go next

- **[Getting started](docs/getting-started.md)** — install it, and run the loop
  above for real.
- **[Commands](docs/commands.md)** — every command, what it writes, and what it
  refuses to.
- **[Architecture](docs/architecture.md)** — the invariants, and where state
  lives. Read before adding a capability.

Requires Python 3.11+ and git. No dependencies, no build step.
