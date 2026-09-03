# luma-foreman

Predictable intelligence and reliable governance — for every project.

- Seamlessly distribute your knowledge, policy and procedures between projects
- Effortlessly wire up each agent harness; so it uses your knowledge correctly
- Continuously verify your shared knowledge remains true

## Why use Foreman

**Standards are easy to ignore.** Somebody writes down how projects are
supposed to work, everyone agrees — and six months later no two repositories
look alike. The standards spread through best intentions, which means drift
and failure are inevitable.

Agents can either amplify this problem or **become the solution**. An unaware
agent will confidently violate our shared standards; an informed
agent will relentlessly uphold them — in every project, every time.
So **foreman standardizes knowledge delivery** for agents. It runs inside a
repository: distributing shared knowledge, wiring up each harness, and
reporting back when a project falls short.

## What usage looks like

```bash
luma-foreman init
luma-foreman catalog add https://github.com/LumaStack/luma-catalog
luma-foreman get lumastack/luma-catalog/git-workflow
luma-foreman apply

# SUCCESS! Agents now use git correctly for this project.
```

A bundle is distributed knowledge containing policy, procedures, and more.
- `catalog add` registers where knowledge comes from, once per catalog. 
- `get` downloads shared bundles into this project.
- `apply` wires up each agent harness with thin adapters, so all agents use the knowledge bundle at the right time without hand holding.

## Where distributed knowledge lives

Shared knowledge is saved inside bundles and then uploaded to a 
[catalog](https://github.com/LumaStack/luma-catalog). 

>You can think of a catalog as a library of knowledge, that you can pick and choose from. And the foreman tool helps distribute selected bundles of knowledge to every project that needs them. 

Foreman can support as many or as few catalogs as you'd like.

## Where to go next

- **[Getting started](docs/getting-started.md)** — install it, and run the loop
  above for real.
- **[Commands](docs/commands.md)** — every command, what it writes, and what it
  refuses to.
- **[Architecture](docs/architecture.md)** — the invariants, and where state
  lives. Read before adding a capability.

Requires Python 3.11+ and git. No dependencies, no build step.
