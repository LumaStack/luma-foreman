---
type: type_definition
defines: luma/catalog
version: "0.3.0"
extends: document
fields:
  namespace:
    field_presence: recommended
    field_type: text
    desc: "the prefix every Bundle this catalog publishes is addressed under"
  tags:
    field_presence: recommended
    field_type: list of text
    desc: "the vocabulary a consumer may declare about itself, which requires keys on"
  requires:
    field_presence: optional
    desc: "obligations, with optional version constraints, deadlines and tags — see below"
  upstream:
    field_presence: optional
    field_type: uri
    desc: "the catalog this one sits below; where else to look, not content to inherit"
---

# luma/catalog

**A catalog publishes Bundles and says how strongly consumers should adopt
them.** A Document with `type: luma/catalog` sits at the root of a catalog's
content directory and is the only thing in that repository authoritative about
the five fields above.

## `namespace`

**Every Bundle is addressed `<namespace>/<name>`, and the namespace belongs to
the catalog rather than to the Bundle.** `lumastack/luma-catalog/decision-records` is *the
`decision-records` published by the `luma` catalog*; the same Bundle promoted
into another organization's catalog is that organization's to name.

**Without it a catalog cannot be addressed by a tool.** A catalog that writes
`lumastack/luma-catalog/git-secrets` in its own `requires` is naming a prefix nothing in the file
declares, so anything adopting from it has to be told out of band what to call
what it just took — and a name learned out of band is a name that gets typed
wrongly.

`recommended` rather than `mandatory` because an adopter may always name the
namespace explicitly, so an undeclared one costs a keystroke rather than
breaking anything. It is also the honest obligation for a field added after
catalogs existed.

**A namespace is not resolved and points at nothing.** It does not have to be
globally unique, no registry issues one, and two organizations may both publish
`acme/`. Collisions are visible in one place — an adopting project, whose
`.luma/bundles/` would hold both — rather than something a catalog can prevent.

## Why this is not a format built-in

**It is the other end of a distribution model, and distribution models are not
the format's business.** LKF defines the Bundle because its own machinery needs
one — a Document ID is a path within a Bundle, and types resolve from a Bundle's
`_types/`. Nothing in the specification needs a catalog to exist, and a Bundle is
perfectly usable from a git URL or a tarball.

**It also changes at this project's rate, not the format's.** A pending draft
would give Bundles dependencies, which alters what a catalog resolves. Were this
built in, adopting that draft would mean releasing the format.

So it is namespaced and vendored instead — the sharing mechanism the format already
describes. The prefix is what makes anyone else's `catalog` possible.

## Declaring a field without a `field_type`, deliberately

`requires` is a nested record, and the format's field declarations have no user-definable object shape —
`actor_event` is a fixed built-in, not a pattern to follow. Declaring it without
describing its shape is legal and buys the half that matters: discovery. The
shape is documented below instead.

## `tags`

A consumer states what it is, and `requires` keys on those values.

**The vocabulary is published rather than free-form for one reason.** If one
repository declares `infra` and another `infrastructure`, a requirement silently
fails to apply to the second and everything still reports green. **A requirement
that does not fire is the worst failure available here**, so a tag outside the
published vocabulary is an error rather than a miss.

A tag list means *any*. `tags: [design, infrastructure]` matches a consumer
tagged either one, never both-and-only-both. When both are genuinely required the
answer is a new tag the consumer declares, not a boolean the catalog evaluates —
that way the composite category acquires a name, someone must claim it in a
committed file, and it can be argued with.

## `requires`

```yaml
requires:
  - bundle: upstream/change-review
    field_presence: required
    version: ">= 2.0.0"
    by: 2026-10-01
    tags: [infrastructure]
```

`obligation` reuses the format's own field ladder rather than inventing a
parallel vocabulary — the same question, *how strongly is this expected*, asked
about a Bundle instead of a field:

| `obligation` | effect |
| --- | --- |
| `mandatory` | must be adopted — a countdown until `by`, a failure after; with no date, a failure immediately |
| `recommended` | reported as a gap, never fails |
| `optional` | a curated shortlist; never reported as missing |
| `deprecated` | reported if still adopted |

A Bundle may appear more than once. Every entry whose tags match applies, and the
strongest obligation among them is in force — so *mandatory for infrastructure,
recommended for everyone else* is two entries rather than a conditional. That is
the same most-restrictive-wins rule inheritance uses for inherited field obligations.

### `requires` does not say "if you take A, take B"

Worth stating, because it is the first thing people reach for it to do. Every
entry is an obligation **on a consumer**, optionally narrowed by what that
consumer declared itself to be. Nothing here links one Bundle to another.

**A coupling you cannot express is usually a Bundle boundary in the wrong
place**, not a missing mechanism. If adopting A without B leaves somebody with
rules and no procedure for following them, the split was wrong.

**Obligation governs whether a consumer must adopt a Bundle. It never governs how
hard conformance is checked once it has.** A recommended Bundle somebody chose to
adopt is checked exactly as strictly as a mandated one — drift is drift. What
`recommended` buys is the freedom not to adopt at all.

## `upstream`

A source pointer: where else to look, not content to inherit. A consumer
configured with one catalog reads the whole chain, which is why an organization's
consumers name only their organization's catalog.

**Single-valued and acyclic.** A linear chain is cheap to walk; a graph is the
resolution problem Bundles were designed to avoid, arriving through a side door.

**There is no catalog-level inheritance**, and what happens when two catalogs
speak at once differs by list:

| list | resolution |
| --- | --- |
| `tags` | union — extra tags are inert |
| `requires` | most-restrictive-wins |

Both merge additively, which is safe: more tags are inert and the strongest
obligation wins. **Nothing here subtracts**, and a list that needed to would
need explicit inheritance rather than a merge rule.

## No version

A catalog carries none. A version would imply its entries are guaranteed against
one another, which is what a distribution release buys and only because its
entries have dependencies. Bundles have none. *What did this catalog hold on a
given date* is a commit identifier.

## What a per-field check cannot reach

A catalog can be internally contradictory in ways no field validation finds: a
Bundle both mandated and deprecated, or a starter pinning a version the same
catalog's own mandate forbids, which would make every new consumer born failing.
These are cross-field rules and belong to whatever publishes the catalog, caught
where it is written rather than where it is applied.
