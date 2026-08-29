---
type: workflow
title: Create a bundle
description: Scaffold a new bundle, decide where it belongs, and get it to a publishable state. Use when asked to create, start, or extract a bundle.
---

# Create a bundle

## 1. Is it one bundle?

**The test: would anyone adopt half of it?** If yes, it is two bundles. If
adopting half would leave someone with rules and no procedure for following
them, it is one.

Bundles have no dependencies, so splitting is cheap now and expensive later —
two bundles that need each other cannot say so.

## 2. Decide where it belongs

See [[where-a-bundle-belongs]]. The short version: a project and a catalog are
both valid first homes, and which is right depends on how many adopters you
already know about. **When you cannot tell, start in the project** — not because
it is better, but because it is the cheaper mistake to correct.

## 3. Scaffold

Copy [the bundle template](../templates/bundle.md) to `<bundle>/BUNDLE.md` and
create the directories you need — see [[organizing-a-bundle]]. Create only the
directories that will have contents; an empty `policy/` is noise.

## 4. Fill in the manifest

```yaml
type: bundle
version: 0.1.0
consumers: [project]
entrypoint: workflows/<the-way-in>
description: <one line — what this holds and who it is for>
```

- **`version`** starts at `0.1.0`, not `1.0.0`. The conventions in a new bundle
  are extracted from one place's practice at best.
- **`consumers`** — `project`, `organization`, or both. Both is right when the
  same content is wanted at either level by different adopters; that is not the
  publisher's call to force.
- **`entrypoint`** — the full Document ID of where a reader starts.
- **`description`** is what a consumer reads when deciding whether to adopt.

## 5. Write the entry point first

Whatever a reader must understand before anything else makes sense. **Say what
surfaces it** — `matches: topic: …` for a subject, `matches: command: …` for a
moment — so it arrives when the work matches and costs nothing before then.

**Reach for `matches: always` as rarely as you can.** It asks for a permanent
seat in every adopter's context, in every session, forever. A document that says
nothing is available on request, which is the right default for almost
everything: its name and line are in the index, so nothing is missed out of
ignorance, and its body waits to be asked for.

## 6. Add types only if they change something

Declare a Type Definition when a consumer must **validate, load, or behave**
differently — not because a distinction reads well.

If the bundle uses `workflow` or `policy`, copy the definition from a bundle
that already has it. Bundles are self-contained: carry your own copy.

## 7. Audit before publishing

Run [[audit-bundle]]. A bundle published with a broken link or an unquoted
frontmatter wikilink is one every adopter copies.
