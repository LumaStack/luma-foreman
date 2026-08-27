---
type: workflow
title: Describe a project
description: Write or refresh the descriptor a repository publishes about itself at .luma/PROJECT.md. Use when a repository is one of several, or when what it is for has changed.
---

# Describe a project

**One sentence is a complete descriptor.** Everything below step 2 is optional
and most of it will stay empty. Read [[the-project-descriptor]] for why the
repository owns this rather than whoever collects it.

## 1. Check there is somewhere to put it

```sh
ls -d .luma 2>/dev/null
```

**No `.luma/` means stop.** Do not create one to hold a descriptor — having
something to file is not a reason to bring a directory structure into a project
that has not adopted it. Say that the repository has nowhere for this yet, and
leave it.

If one exists and `.luma/PROJECT.md` does too, this is a refresh: read it first
and change what is no longer true, rather than rewriting it.

## 2. Write the sentence

**Answer: when should somebody open this repository?**

Not what it is built with. Not what it does internally. The thing a person or an
agent needs in order to know this is the one they want.

> *"The customer-facing storefront — anything a buyer sees, checkout, or the
> payment integration."*

not

> *"Next.js application with a Postgres backend."*

**The test: could somebody choose between this repository and four others using
only this sentence?** If two of them would read the same, it is not specific
enough yet.

```yaml
---
type: luma/project
title: <repository name>
description: <when somebody should open this>
---
```

That is a finished descriptor. Everything after this point is worth doing only
if it is true and known.

## 3. Add boundaries, if any have been decided

```yaml
owns: [storefront, checkout, payment-integration]
must_not_own: [inventory levels, pricing rules]
```

**Only what somebody actually decided.** Inventing boundaries here creates
claims the organization never agreed to, and they will be read as settled.

**`must_not_own` is the more valuable half** — everything owns something, and an
explicit *this is not ours* is a boundary somebody argued about. It is what
stops a project quietly absorbing a neighbour's job over two years.

**Leave both out rather than guessing.** Absent means nobody has said, which is
findable. A wrong claim looks exactly like a right one.

## 4. Say why it exists, if it is not obvious

```markdown
## Why it exists

<One paragraph. The problem it solves, and what would be true if it did
not exist. Not how it works.>
```

**Skip it when the sentence already covers it.** A heading with a restatement
under it is worse than no heading — it teaches the next reader that this file
is padding.

## 5. Leave out what the reader already has

**Not** the URL, the language, the visibility, the default branch, when it was
last pushed, or how to build it.

Every one of those is knowable in seconds by whoever is holding the repository,
and every copy of a moving fact is a second answer that will eventually
disagree. A repository that names its own location is wrong the moment it is
forked, mirrored, or transferred.

**The test: could the reader get this from the repository itself in ten
seconds?** Then it does not belong here.

## 6. Commit it, and keep it in the same commit as the change

`.luma/` is committed in full, so there is nothing to ignore.

**The habit that matters is afterwards.** When what this repository is for
changes, the descriptor changes in the same pull request — reviewed by the
people who caused the change, while they still remember why.

**That is the whole reason the repository owns this file.** A descriptor updated
in a separate pass, later, by somebody else, is a cache with extra steps.

## When somebody else proposes one

An organization collecting descriptors may offer to write one for you. That is
useful and often the only way a gap gets closed.

**It arrives as a pull request, and it is yours to judge.** Read it as a claim
somebody made about your project from the outside — usually close, occasionally
describing what the repository used to be. Correct it before merging rather than
after.
