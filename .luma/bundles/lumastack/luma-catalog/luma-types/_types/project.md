---
type: type_definition
defines: luma/project
version: "0.1.0"
extends: document
fields:
  description:
    field_presence: recommended
    field_type: text
    desc: "when somebody should open this repository. Strengthened from the root's optional (§10.3) — the field this type exists to carry"
  lifecycle_status:
    field_presence: recommended
    field_type: enum
    values: [draft, provisional, stable, archived]
    desc: "how mature the repository is. Strengthened from the root's optional (§10.3); absent means nobody has said"
  disclosure_level:
    field_presence: recommended
    field_type: enum
    values: [public, internal, confidential, restricted]
    desc: "how widely this repository is disclosed. Absent refuses sensitive content — undeclared is not permission"
  owns:
    field_presence: recommended
    field_type: list of text
    desc: "what this repository is responsible for. A claim, which its organization may adjudicate"
  must_not_own:
    field_presence: optional
    field_type: list of text
    desc: "what belongs to somebody else. The half that prevents scope creep"
---

# luma/project

**A repository describing itself, to be read by something outside it.** It lives
at `.luma/PROJECT.md`.

## Why this is not a format built-in

**Nothing in the specification needs it.** A Document ID, type resolution and
reserved files are all defined in terms of a Bundle; none of them mention a
repository. The format works completely without this type — only *tooling built
on it* does not.

**And it changes at this project's rate.** It gained two fields the day it was
written. A built-in's contract is versioned with the format, so a type that grows
as tooling matures would drag the format's version behind it.

The prefix is what makes that safe: `luma/project` cannot collide with anybody
else's `project`, including the several other things in the industry already
using the word.

## It answers one question

**When should somebody open this repository?**

That is `description`, and it is the field the whole type exists to carry. A
project descriptor that is one good sentence has done its job.

**It is not a summary of the code.** *"Next.js application"* describes an
implementation and helps nobody decide anything. *"The customer-facing storefront
— anything a buyer sees, checkout, or the payment integration"* is what somebody
needs in order to know this is the repository they want.

**The test:** could somebody choose between this repository and four others using
only this sentence? If two would read the same, it is not specific enough.

## Inherited fields that are strengthened

Permitted by §10.3, which allows a subtype to raise an inherited field_presence and
never to lower one.

**`description` moves `optional` → `recommended`** because a consumer reads it to
decide whether to load this at all, before anything else about the repository is
fetched. A project descriptor without one has no reason to exist.

**`lifecycle_status` moves `optional` → `recommended`** because how mature a
repository is changes how everything inside it should be treated — a position
recorded in a two-week-old repository binds differently from the same position in
a five-year-old one, and nothing else in the descriptor says which this is.

**Absent means nobody has said.** §6 gives `lifecycle_status` a default of
`provisional`, and that default answers *what is the value*. It does not answer
*may I act on it*: anything making a consequential choice on the strength of
maturity should require an explicit declaration, because **a default is not a
declaration.** The same asymmetry `disclosure_level` states below.

## `disclosure_level` — how widely this repository is disclosed

**The scale is people, not sensitivity.** `public` is the widest and `restricted`
the narrowest:

| | who sees it |
| --- | --- |
| `public` | anyone |
| `internal` | the whole organization |
| `confidential` | a named group within it |
| `restricted` | a named few |

**Content may only go where disclosure is no wider than its own
classification.** That is the entire rule, and it is one comparison.

### It is a declaration, not a state

**This is the property the field exists for.** A repository's hosting visibility
is ambient — true today, changeable tomorrow — and reading it answers a different
question than the one being asked.

A repository can be private for months while *planned to be published*, and its
`disclosure_level` should be `public` throughout — so it refuses sensitive
content the entire time it is still private. **Checking the host would return
private and permit the write**, which is exactly how a repository ends up holding
something that becomes public later.

**Never derive this from the host.** If it can be inferred from ambient state, it
is not doing the job.

### Absent refuses

**Undeclared is not permission.** A repository with no `disclosure_level` does
not accept sensitive content, and nothing may be written there on the strength of
it looking safe.

**The tempting mistake is to treat absent as the most restrictive value.** That
reads as *safest*, and the safest value is the one that permits the most — so the
default would grant maximum access to every repository that never said anything.
**Absent means undeclared, and undeclared refuses. You declare to gain a
capability, never to lose one.**

### It never causes anything to be published

**This field constrains writes. It is not an instruction about visibility.** A
tool that reads `disclosure_level: public` and makes the repository public has
turned a safety limit into a command. **Nothing may publish a repository, widen
its access, or treat its contents as publishable on the strength of this field.**

The asymmetry is the point: **it may only ever narrow what happens, never widen
it.** A control that can widen access is not a safety control.

### Neither drives the other

**The value must never drive reality.** A tool that publishes a repository
because a line in a file changed has made a text edit into an irreversible
disclosure.

**The value must not be derived from reality either.** That sounds safe and
destroys the property the field exists for — a repository private today and
planned for publication would be recorded as `internal`, and would then accept
sensitive content right up until the day it is published.

So it is an independent assertion, checked against an independently observed
reality, **with the gap between them reported**.

### Syncing to reality is not housekeeping

**The most dangerous edit to this field is the one that looks like tidying up.** A
repository declares `public` because publication is planned; somebody notices it
is *currently* private, treats the declaration as stale, and "corrects" it to
`internal`. Sensitive content is now writable into a repository about to be
published — and the change reads, in the diff, as making a file agree with the
world.

**Warn on any edit that loosens this field. Warn harder when the reason given is
that it had fallen out of sync**, because that is the most plausible-sounding
justification for the most dangerous change available here.

**Require the reason to be about the content, not the metadata.** *Nothing
sensitive will ever live here* is a reason. *It didn't match* is an observation,
and observations do not grant permissions.

### When declared and actual disagree

| declared | actually | | |
| --- | --- | --- | --- |
| `public` | private | more restricted than declared | **report. Not an error** |
| `internal` or narrower | **public** | **more permissive than declared** | **error. Stop** |

**More permissive than declared is a showstopper.** Content believed internal is
publicly readable *right now*. **Error immediately, say what is exposed, and
change nothing** — the exposure has already happened, and quietly flipping the
repository private destroys the record of a decision somebody made without
un-publishing anything.

### The asymmetry every rule here rests on

**Being wrong toward restriction is an inconvenience. Being wrong toward
permission is unrecoverable.** Every rule above fails toward restriction
deliberately: absent refuses, the declaration beats the observation, a check that
cannot be performed is a failure rather than a pass, and the field can narrow but
never widen. **Those are one principle applied four times.**

## `owns` and `must_not_own`

What lets somebody detect that **two repositories are about to collide** — a
question no single repository can answer and every organization eventually asks.

```yaml
owns: [storefront, checkout, payment-integration]
must_not_own: [inventory levels, pricing rules]
```

**`must_not_own` is the more useful half.** Everything owns something; an
explicit *this is not ours* is a boundary somebody argued about, and it is what
stops a repository quietly absorbing a neighbour's job over two years.

**They are claims, not rulings.** A repository states what it believes it owns;
its organization may disagree, and that disagreement is exactly the finding worth
having.

**Only what was actually decided.** Invented boundaries are read as settled, and
a wrong claim looks exactly like a right one. Leave both out rather than
guessing — absent means nobody has said, which is findable.

## It does not record its own location

**Not its URL, its visibility, or its language.** A repository that names its own
location is wrong the moment it is forked, mirrored or transferred, and every one
of those facts is already knowable by whoever is holding it. **A Document should
not state what its reader already knows.**

## Why the repository owns this and not its organization

An organization can cache a description; it cannot keep one true. The repository
changes, the cache does not, and nothing announces the drift.

**Written here, it changes in the same commit as the change that invalidated
it** — reviewed by the people who caused it, where they still remember why.
Whoever collects these is then doing something safe: **combining, not
authoring.**

## What it is not

**Not a README.** A README is a front door for a human deciding whether to keep
reading. This is a machine-read fact for something deciding whether this
repository is relevant at all.

**Not a manifest.** Nothing is built, installed, or resolved from it.

**Not a mandate.** What a repository *must* do is an obligation, and obligations
are declared by a `luma/catalog`, never by the thing they bind.
