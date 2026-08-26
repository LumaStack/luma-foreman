# What foreman does

**The catalog holds the knowledge; foreman holds the mechanics.** Moving
knowledge to where it is needed, writing it where an agent will meet it, and
verifying it stayed true. Everything a bundle *knows* — the layout a project
should have, what tooling to install, what the baseline is — belongs to the
catalog, and foreman is what carries it and checks it landed.

This is a working document. It says what is built, what is not, and what each
unbuilt thing would cost.

## What works

| | |
| --- | --- |
| `init` | `.luma/PROJECT.md` and `.luma/config/luma-foreman.toml`, and nothing that has no contents yet |
| `get` | vendoring a bundle into `.luma/bundles/`, with version, origin, catalog commit and checksum in `adopted.toml` |
| `apply` | a thin skill per workflow, and an index of everything adopted in a managed block in `CLAUDE.md` |
| `inspect` | identity, secrets, bundle structure, adoption drift |
| `bundle`, `catalog` | reading the inventory and where it came from |
| `agent-permissions` | the per-repository permission gate |

**`agent-permissions` is unrelated to all of the above.** It shares no machinery
with adoption and would function identically if bundles had never existed. It is
in the same binary because it is the same operator working on the same
repository, not because the two are one system.

## What is not built

### Distribution

- **Resolve dependencies** between bundles.
- Share workflows, scripts and assets — not only skills, and **knowledge that is
  not a skill at all**.
- Be **independent of Claude Code**. Work for most agentic AI.

### Writing it out

- Select *at write time* which subset of adopted content is written — including
  by symlink. Unbuilt because nothing yet decides the subset.
- **Load and unload skills.**
- Hook universal workflows into each agent **via that agent's own adapter
  pattern**, so they trigger natively rather than through a shim.
- **Load and unload hooks.**
- Adopt frontmatter that lets tooling enforce governance.

### Routing

- Resolve what gets loaded into context **based on a scenario or situation**.
- Resolve **progressive disclosure routing**, and pull knowledge from external
  sources at the right time.
- Help with **token optimization and token management strategies**.

*Routing is the mechanism; token management is the objective. It is also the
only item here with a hard success metric — you can count tokens, where "is this
project in compliance" needs a judgement. That makes it the easiest thing to
know you got right, and worth building against a measured baseline rather than
an intuition.*

*Three things already point at it and were not framed this way. `preload:
mandatory` is a context budget decision wearing an obligation's clothes.
Selecting what to write out is the largest available saving. And the
compact-plus-full split — every rule with a one-clause reason, the full argument
deferred — was deferred for want of evidence that context was tight.
Measurement is that evidence.*

### Verification

- Set up tooling so projects stay in compliance.
- Make sure projects follow **mandates handed down from headquarters**, probably
  through the catalog.
- **Seek and destroy rot.**
- Aid with **observation and auditing** of the system.

### Feedback

- **Alert people when things do not work.**
- Provide ways the system can **learn and improve.**

## What each of these costs

Honest annotations, so the list is not read as a plan.

**Needs cooperation that does not exist.** Loading and unloading
**mid-session**. Agent Skills' progressive disclosure loads every skill's name
and description at startup and the body on description match; there is no hook
for *conditions changed, drop these*. Selecting at write time gets most of the
value; runtime swapping has no mechanism in any harness.

**Needs a decision, and adoption is what will settle it.**

- *Do the standards used to build luma tooling live outside luma tooling?*
  Foreman adopts `luma/decision-records` and records its own decisions through a
  bundle it took from the catalog. If its release process, its versioning rules
  and its prose conventions go the same way, foreman is a consumer of the
  catalog it was built to serve. **Elegant, or a permanent headache for whoever
  maintains both ends?** Nobody knows yet, and the way to find out is to keep
  adopting until it either stops being convenient or does not.
- *Will anything ship natively in foreman, or is everything fetched?* The same
  question from the other side, and it decides whether logging is a bundle.

**Needs a decision before it can be built.**

- *Routing:* prose an agent follows, or data a tool evaluates. If `apply` must
  evaluate a router to decide what to write, it has to be **data** — a tool
  cannot follow prose — which means designing the condition language there are
  good reasons to be wary of.
- *Dependencies:* this **reverses a settled decision** — ADR-0002, *adoption
  copies a directory and never resolves anything*. For content, resolution is
  more dangerous than for code: two versions of a library conflict and something
  crashes, two versions of a policy conflict and nothing happens. Declare and
  **detect**, rather than solve, keeps real dependencies without a solver — and
  keeps conflicts visible instead of silently reconciled.
- *Zero dependencies:* the README promises no build step and nothing to install.
  Semver range resolution is not worth hand-rolling. That promise probably
  cannot survive dependency resolution.

**Not yet defined enough to build.**

- *Rot.* Some is mechanical — a dead link, a checksum mismatch, a bundle five
  versions behind. Some is not: a policy nobody follows, a document still
  accurate but no longer read, a re-open condition that quietly fired.
- *Learn and improve.* The most interesting item and the least specified.
- *Set up tooling* and *hooks* may not be foreman's at all. Both imply foreman
  writing configuration it invented, which puts it back to knowing things. They
  may be bundles carrying config that adoption copies.

## A regex that stops matching a command name fails open

`agent_permissions/match.py` carries `CLI_WRITE` and `CLI_INVOCATION`, which
recognise a `luma-foreman agent-permissions` invocation **in order to gate it**.
Rename or restructure that command and the patterns stop matching — silently,
and in the permissive direction. The subsystem exists to prevent exactly that.

**Write the gating test before the change, so it fails first.** Anything that
reads a command's own name to decide whether to gate it is in this category, and
the failure never announces itself.

The same shape applies to the config file: a `policy.toml` left by an older name
is still read when `permissions.toml` is absent, because a permission file that
quietly stops being read fails open too.

## What the ecosystem already solved

Worth knowing before building any of it.

- **`SKILL.md` is an open standard** read by 40+ agents. Skill distribution is
  solved; do not compete on it. One output to the standard, not adapters per
  harness — adapters are only needed for **hooks**, which have no standard.
- **Claude Code plugins** are a real package manager: semver, plugin-to-plugin
  dependencies with ranges, git sources pinned to tags resolved to SHAs, frozen
  lockfile installs with `--ignore-scripts`, lifecycle scripts disabled, path
  traversal blocked, and a **`managed` install scope that is organization-
  controlled and read-only**. That last one is an obligation mechanism already
  designed.
- **Nobody has a format for knowledge that is not a procedure.** `SKILL.md`
  answers *how do I do X*. A glossary, an architecture description, a standing
  rule and a record have no home except as attachments subordinate to some
  skill. That is the actual gap.
- **Plugins cache to `~/.claude/plugins/cache/` and are not committed.** A fresh
  clone with no network does not reproduce. Vendoring into the repository does,
  and that is a real difference rather than a stylistic one.
