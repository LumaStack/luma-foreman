---
type: luma/idea
title: Nothing validates frontmatter against the type that declares it
created: { by: human:benlinton, at: 2026-09-08T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: later
scope: project
stage: draft
---

# Nothing validates frontmatter against the type that declares it

**The schema is already written, in every type definition, and nothing reads
it as one.** `_types/idea.md` declares its fields machine-readably:

```yaml
fields:
  horizon:
    field_presence: recommended
    field_type: enum
    values: [next, later, someday]
  archived:
    field_presence: optional
    field_type: date
```

Nothing checks that an idea's `horizon` is one of those three, that `archived`
parses as a date, or that a required field is present at all. `inspect --rule
bundles` catches shallower things — frontmatter with no `type`, an unquoted
wikilink, a template carrying live frontmatter — and stops there.

So a document can declare `type: luma/idea`, invent a horizon nobody defined,
and be reported clean.

## Two ways in, and they buy different things

**[remark-lint-frontmatter-schema](https://github.com/JulianCataldo/remark-lint-frontmatter-schema)**
and
**[remark-lint-frontmatter-validation](https://github.com/Nick2bad4u/remark-lint-frontmatter-validation)**
validate YAML frontmatter against JSON Schema, inside the remark ecosystem.

**What that buys is the editor.** remark runs in editors, so a wrong `horizon`
underlines while somebody is typing it — which is where the mistake is cheapest
to fix, and something a checker run later cannot do.

**What it costs is a Node toolchain**, in a tool that is stdlib-only Python with
no dependencies and no build step, deliberately. It also needs the schema as
JSON Schema, and the schema is currently LKF frontmatter — so something has to
generate one from the other, and now there are two artifacts that can disagree.

**The other route is teaching `inspect` to read `fields:`.** No new dependency,
no translation, and it uses the declaration that already exists. What it cannot
give is feedback while writing.

**These are not exclusive.** Generating JSON Schema from the type definitions
would serve both — editors get remark, continuous integration gets `inspect` —
provided the generated file is treated as derived and never edited, which is a
rule this estate already applies to everything `apply` writes.

## Why it is worth more than it looks

**A type definition currently describes rather than binds.** Its `fields:` block
reads as documentation, and the only thing enforcing any of it is whoever
happens to be paying attention. That is the same shape as a policy nobody
checks — the thing [[verification-beyond-inspect]] calls the rot with no
referent.

**It is also the missing half of
[[frontmatter-needs-a-version-and-types-need-migrations]].** A version on a
document is only useful if something reads the schema that version names. One
without the other is a number nobody acts on, or a check that cannot tell an
old document from a wrong one.

## Related

**[[nothing-checks-that-a-citation-resolves]] is the sibling gap.** That one
asks whether the things a document *names* exist; this asks whether the fields
it *declares* are the ones its type allows. Both are cases of the format
describing something nothing verifies, and a single validation pass might
reasonably cover both.

## Open

**Where it runs.** In `inspect` (works in a bare clone, no configuration —
which is the guarantee that rule set carries), as a pre-commit hook, in
continuous integration, or in the editor. The editor is the only one that
catches a mistake before it is committed, and the only one needing a toolchain
this project does not have.

**Whether `field_presence: recommended` is enforceable at all.** Required and
optional are checkable; *recommended* is a judgement, and reporting it as a
finding would make every honest document fail. It is probably a notice, which
is the tier `inspect` already has for exactly this.
