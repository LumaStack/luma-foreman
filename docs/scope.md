# What foreman does

**Working document.** The README's *four jobs* — bootstrap, outfit, inspect,
refit — were written before the catalog existed, and each was defined by
*knowing* something the catalog now knows. This is the replacement being
assembled. It is a list, not a design.

## Why the four jobs went stale

| the job assumed | now lives in |
| --- | --- |
| bootstrap knows the structure a project should have | `luma-layout` |
| outfit knows what tooling to install | `git-workflow`, `github-release`, `git-secrets` |
| inspect knows the baseline | every policy bundle |
| refit knows the latest learnings | `audit-records`, `versioning` |

The catalog took the **knowledge**. What is left for foreman is the
**mechanics** — moving knowledge to where it is needed, and verifying it stayed
true.

## The list

### Distribution

- Move knowledge to where it is needed.
- Verify it stayed true.
- **Resolve dependencies** between bundles.
- Share workflows, scripts and assets — not only skills, and **knowledge that is
  not a skill at all**.
- Be **independent of Claude Code**. Work for most agentic AI.

*No verb for adoption appears anywhere in the original four jobs. Fetching a
bundle, vendoring it, and recording its version and checksum is the connective
tissue for most of this list.*

### Projection

- **Load and unload skills** — possibly by symlink, possibly another mechanism.
- Hook universal workflows into each agent **via that agent's own adapter
  pattern**, so they trigger natively rather than through a shim.
- **Map mandated policy into `CLAUDE.md`, `AGENTS.md` or whatever a harness
  reads, so policy cannot go unread or ignored.**
- **Load and unload hooks.**
- Adopt frontmatter that lets tooling enforce governance.

### Routing

- Resolve what gets loaded into context **based on a scenario or situation** —
  something like real-time symlinks.
- Resolve **progressive disclosure routing**, and pull knowledge from external
  sources at the right time.
- Help with **token optimization and token management strategies**.

*Routing is the mechanism; token management is the objective. It is also the
only item on this list with a hard success metric — you can count tokens, where
"is this project in compliance" needs a judgement. That makes it the easiest
thing here to know you got right, and worth building against a measured baseline
rather than an intuition.*

*Three things already point at it and were not framed this way. `preload:
mandatory` is a context budget decision wearing an obligation's clothes.
Selecting what to project is the largest available saving. And the compact-plus-
full split — every rule with a one-clause reason, the full argument deferred —
was deferred for want of evidence that context was tight. Measurement is that
evidence.*

### Verification

- Set up tooling so projects stay in compliance.
- Make sure projects follow **mandates handed down from headquarters**, probably
  through the catalog.
- **Seek and destroy rot.**
- Aid with **observation and auditing** of the system.

### Feedback

- **Alert people when things do not work.**
- Provide ways the system can **learn and improve**.

### Already built, and unrelated to all of it

- **`policy`** — the per-repository permission gate. Working. It shares no
  machinery with anything above and would function identically if bundles had
  never existed.
- **`inspect`** — identity, secrets, and bundle structure. Working.

## What each of these costs

Honest annotations, so the list is not read as a plan.

**Buildable now, nothing external needed.** Adoption and vendoring. Checksum
drift. Projecting a workflow to `SKILL.md`. Projecting policy into whatever a
harness reads. Selecting *at projection time* which subset of adopted content is
written out — including by symlink.

**Needs cooperation that does not exist.** Loading and unloading **mid-session**.
Agent Skills' progressive disclosure loads every skill's name and description at
startup and the body on description match; there is no hook for *conditions
changed, drop these*. Projection-time selection gets most of the value; runtime
swapping does not currently have a mechanism in any harness.

**Needs a decision before it can be built.**

- *Routing:* prose an agent follows, or data a tool evaluates. If `outfit` must
  evaluate a router to decide what to write, it has to be **data** — a tool
  cannot follow prose — which means designing the condition language there are
  good reasons to be wary of.
- *Dependencies:* this **reverses a settled decision**. For content, resolution
  is more dangerous than for code: two versions of a library conflict and
  something crashes, two versions of a policy conflict and nothing happens.
  Declare and **detect**, rather than solve, keeps real dependencies without a
  solver — and keeps conflicts visible instead of silently reconciled.
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

## A failure that selection creates

Once foreman chooses what to project, **what is adopted and what is in context
diverge deliberately**. That is a third drift state beside *edited locally* and
*outdated*, and the one that looks fine from every angle: the bundle is present,
the checksum matches, and no agent has ever seen it.

`inspect` should be able to answer *what did I adopt that is routed to nothing*,
or a project quietly carries rules nobody reads.

## What the ecosystem already solved

Worth knowing before building any of it.

- **`SKILL.md` is an open standard** read by 40+ agents. Skill distribution is
  solved; do not compete on it. One projection to the standard, not adapters per
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
