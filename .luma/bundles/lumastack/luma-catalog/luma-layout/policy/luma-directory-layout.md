---
type: policy
title: The .luma directory layout
description: The four directories every luma tool honours, what belongs in each, and the one invariant that makes the whole thing trustworthy.
matches:
  - path: ".luma/**"
---

# The `.luma` directory

```
.luma/
  PROJECT.md          what this repository is, for something outside it
  backlog/            what we intend
  bundles/            what is in force — adopted, or written here
    adopted.toml      what this project took, and proof of what it looked like
    lumastack/luma-catalog/git-secrets/
  config/
    luma-foreman.toml how a tool behaves here — one file per tool, named for it
  records/            what happened, and why
  _types/             contracts for documents that are in no bundle
```

**This describes what the tools already do.** Adopting this bundle does not make
the layout apply to you — anything writing into `.luma/` is bound by it whether
you adopt or not. You adopt it so an agent working here can read the contract
locally, without reaching for anything remote.

## `_types/` holds contracts for documents that are in no bundle

**Almost every Document gets its contract from the bundle it lives in.** The
knowledge format resolves a type from *that* bundle's `_types/`, which is what
lets two bundles hold different versions of one type without contradiction.

**`PROJECT.md` is in no bundle.** It sits above the tiers, describing the
repository the tiers belong to — so there is no bundle to resolve its `type`
from, and the format says outright that whoever puts a Document there owes it an
answer. `.luma/_types/` is that answer.

**It states which contract wins — it is not the project's spare copy.** That
distinction decides whether a file belongs here at all:

| | |
| --- | --- |
| **no adopted bundle provides the type** | this is the only answer. **Put it here** |
| **exactly one adopted bundle provides it** | **pure duplication.** Reference the adopted copy and put nothing here |
| **two adopted bundles provide it and disagree** | **put it here.** This is the disambiguation the directory exists for |

**Vendoring is for travel. Within one repository, reference.** A copy of a file
that already exists in the same checkout goes nowhere and drifts for free — it
takes all the cost of vendoring and none of the benefit, which is
self-containment when a bundle *moves*.

**Where a file does belong here, it carries `vendored_from`** with the version
taken. That matters more here than elsewhere: it is how anything collecting
descriptors across an organization can ask which contract a given project is
written against, instead of guessing from which fields happen to be present.

**Empty is the normal state.** A repository whose `.luma/` holds only a
descriptor and a backlog needs nothing here — the directory appears when
something outside a bundle needs a contract, and most projects never reach that.

*Not to be confused with a bundle's own `_types/`, which is reserved by the
format and scoped to that bundle. Same name, deliberately: same job, different
scope.*

## Why one directory, and why hidden

**One root.** A repository root is contested space — source, tests, manifests,
continuous integration config, licence, readme — and four more entries is real
clutter. One root also means an agent arriving cold does a single lookup and
cannot half-find it.

**Hidden**, because `.luma/` is not the product. It is how the project is run,
sitting beside the thing the project *is*, and a visible `luma/` next to `src/`
reads as a source module. The dot says *infrastructure, not shipped output*.

**Vendor-named**, because this layout is one product's opinion rather than a
universal truth. A generic name would claim a universality nothing has earned,
and `.luma/` is collision-proof by construction.

## The tiers are cut by lifecycle

Not by topic, and not by who wrote it:

| | |
| --- | --- |
| `backlog/` | **what we intend.** Churns — items are created and destroyed |
| `bundles/` | **what is in force.** Adopted whole, or written here |
| `records/` | **what happened, and why.** Append-only, dated, never edited |
| `config/` | how a tool behaves here |

### `PROJECT.md` sits above the tiers, not inside one

It is the only file at the root of `.luma/`, and deliberately so: **it names the
repository the tiers belong to.**

It has no lifecycle of its own — it is not intended, not in force, not a record
of what happened, and not how a tool behaves. Filing it under any of the four
would be filing identity as though it were content, and the directory it named
would then be wrong about what it holds.

**One file, and the bar for a second is high.** Anything else that seems to
belong at this level almost certainly has a lifecycle and belongs in a tier. The
content and shape are the `project-documentation` bundle's to define; this
layout says only that the path is reserved and what it is for.

A glossary and a guardrail live in the same place not because they are similar,
but because they have the same lifecycle: both are live, both are currently in
force. That is the only axis. Sorting by topic as well would mean two questions
deciding one location, and every new item needing both answered.

## A config holds overrides, and as little else

**One file per tool, named for the tool** — `luma-foreman.toml`, not
`foreman.toml`. The binary is what somebody is looking for when they open
`config/`, and a truncation makes them guess which tool a file belongs to.

**What is absent follows the tool and improves with it; what is written down is
frozen.** Every value in a config is one an upgrade cannot move, so the smallest
file is the one that ages best. A tool generating a config should write what has
no default and stop.

**Do not ship commented-out defaults.** They cannot change behaviour while they
are comments, and uncommenting is one keystroke — at which point a stale copy of
a default becomes a frozen override pinned to whatever it said the day the file
was written. Where a reader needs to know what is settable, point at
documentation or a command that reads the live values; a file cannot know them.

## Everything in `.luma/` is committed. No exceptions.

If uncommitted files can live here, a reader cannot distinguish an authoritative
rule from somebody's local tweak, and **two agents on two machines read
different rules for the same project.** That is a correctness failure in the one
system whose entire job is saying what the rules are.

Machine-local settings — timeouts, cache locations, per-operator choices — live
in `~/.config/luma/`, never here. The test: **if deleting it loses a decision
somebody made, it is not local state.**

## `bundles/` holds both what you adopted and what you wrote

The namespace tells them apart, and it is more reliable than a directory would
be:

```
.luma/bundles/lumastack/luma-catalog/git-secrets/     adopted — never edit it
.luma/bundles/acme-web/deploy/      ours — this project wrote it
```

`adopted.toml` is authoritative anyway, since only adopted bundles carry a
source and a checksum. A `vendor/` directory would put the same fact in the path
as well, and two copies of one fact can disagree.

**Editing an adopted bundle is drift**, and a check will say so. If you need it
to be different, that is a different bundle in your own namespace.

## `adopted.toml` is written by a tool, never by hand

```toml
["lumastack/luma-catalog/git-secrets"]
version  = "0.1.0"
source   = "https://github.com/LumaStack/luma-catalog"
commit   = "abc1234"
checksum = "sha256:9f2c…"
```

**`commit` records which state of the catalog this came from**, and it is the
cheapest thing here. Two bundles adopted from the same commit are known to have
come from one internally consistent set; from different commits, that is visible
and checkable. Nothing else answers that — a version says *which release of this
bundle*, and a checksum says *which bytes*, and neither says *alongside what*.

The checksum is the point: drift-checking compares it against the vendored files
to detect an edited copy. **A hand-edited checksum makes that check silently
start passing**, which is why the value lives nowhere near a file you are invited
to edit — and why it is not in `config/`.

It is **not a lockfile**, though it resembles one. Bundles are committed, so
nothing is ever restored from it. It answers three questions only: has anyone
edited this copy, is a newer version available, and what was this taken
alongside.

## Generated files are never the source

`.claude/`, `AGENTS.md`, `CLAUDE.md` and whatever replaces them live wherever
their tool looks, are generated from what is in `.luma/`, and are disposable.

Editing a generated file is editing something that will be overwritten. If the
content should be different, change what generated it.

### Some of them are only partly generated, and the boundary is marked

**`CLAUDE.md` is the awkward one.** It is a generated file by the rule above and
it is also where people write things by hand, which no amount of policy is going
to stop. A tool that owned the whole file would destroy that work; a tool that
owned none of it could not put anything in front of an agent.

So a tool owns a **delimited region** and nothing else:

```markdown
<!-- luma:begin — generated by `luma-foreman apply`. Edits between these markers are lost. -->
...
<!-- luma:end -->
```

**Three rules make this safe.** Only what is between the markers is rewritten,
and everything outside them survives untouched. A file with no markers gets the
block appended rather than replaced. And the opening marker names the command
that regenerates it, because a reader who does not know what wrote something
cannot fix it at the source.

**One tool, one block.** A second tool wanting a region of the same file uses its
own marker pair, and neither reads the other's.

### Generated output that says who made it can be cleaned up

The same problem in the other direction: a directory like `.claude/skills/`
holds both generated files and hand-written ones, so a tool regenerating it has
to be able to delete what it wrote and only what it wrote.

**A generated file carries a marker saying so.** Without one, a tool has two bad
choices — delete everything and take somebody's work with it, or delete nothing
and leave output for knowledge the project no longer has. Neither is
recoverable by the person who hits it.
