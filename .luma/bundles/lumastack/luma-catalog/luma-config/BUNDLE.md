---
type: bundle
version: 0.7.2
published: 2026-08-27
consumers: [project, organization]
entrypoint: policy/where-configuration-lives
description: Where luma configuration lives, what is committed and what belongs to the machine, and the order in which layers win.
---

# Luma config

Two homes and one rule of thumb:

```
.luma/config/          committed. What this project declares
~/.config/luma/        yours. Not committed, near enough always
```

**The reverse is the failure that matters.** Committed-but-personal is somebody's
private business. Uncommitted-but-inside-`.luma/` means two agents on two
machines read different rules for the same code, which is a correctness problem
in the one place whose job is saying what the rules are.

## What is here

- [[where-configuration-lives]] — the two homes, the XDG reasoning behind the
  machine-local side, and the test that tells configuration from cache. Read
  first.
- [[configuration-precedence]] — *background.* Six layers, and why the committed
  file appears twice. It describes how resolution behaves rather than obliging
  anybody, so it is a `document`.
- [[add-a-setting]] — the four questions that decide where a new value goes.

## The two ideas worth carrying

**If deleting it loses a decision somebody made, it is not cache.** One question
that resolves nearly every placement, and the failure it prevents is nasty:
putting a decision under a cache path means clearing caches silently reverts
behaviour, and nobody suspects the cache because caches are meant to be safe to
clear.

**A project may suggest and may mandate, and those are different tables.**
`[defaults]` is a starting value somebody may change; `[require]` is a rule a
local preference cannot lift. Splitting them puts the precedence in the file
rather than in something a reader has to remember — and it corrects an earlier
formulation, *the committed declaration always wins*, which was too broad and
would have forbidden a project offering newcomers a sensible default.

## Naming, on both sides

Inside `.luma/config/`, files are named for the tool that reads them —
`foreman.toml` rather than `config.toml` — so several tools coexist without
negotiating a schema.

Outside, the shape is `<org>/<repo>` — `~/.config/luma/luma-foreman/`, with the
second segment the repository name exactly. **One deny rule then covers every
tool the organization ships**, needs no wildcard, and keeps working whatever a
repository is called.

The two sides differ because they answer to different questions. A project has
one set of rules, so `.luma/` is one directory. The machine-local side has one
directory per repository, under one for the organization, so that a rule about
all of them can be written once.

## Consumers

Both levels. An organization's headquarters is a repository and configures its
own tooling the same way.

## Version

`0.7.2` — **`entry_point` is now `entrypoint`.** One word, per LKF §11.1, so the same word names the same thing at every level it appears.

Patch: one key renamed. Same value, same meaning, same `optional` presence, and `luma-foreman` reads both spellings while the rename lands.

`0.7.1` — **bundle IDs in this catalog gained their namespace.** A bundle here
is `lumastack/luma-catalog/<name>` rather than `luma/<name>`, because the
namespace now derives from where the catalog lives instead of being declared.
Every reference in this bundle's prose is updated.

**A fork can no longer publish under this catalog's name.** It lives somewhere
else, so it is named something else, and its bundles sit beside these in a
project rather than colliding with them.

*Type names are unaffected.* `type: luma/catalog` and its siblings name the
format, not this catalog, and resolve separately.

Patch: nothing but the identifiers a reference points at.

`0.7.0` — **`applies_to` is now `matches`.** The old name obliged an author to
write a false sentence: `applies_to: everything` claims a rule governs
everything, and none does — what a rule governs is stated in its body, where no
frontmatter value reaches. The field says what makes a Document *surface*, which
is smaller and true, and it reads as a sentence in every form it takes: matches
`git commit`, matches always, matches nothing.

**The default reverses with it.** A Document that says nothing is now available
on request rather than loaded into every session. Nothing here is affected —
every rule in this bundle already states what surfaces it — but a rule that
genuinely should always be present now says `matches: always` rather than
staying silent and being treated as though it had.

Minor. Nothing a reader is obliged to do has changed; the field it is declared
in has been renamed, and `applies_to` is still read while the rename finishes.

`0.6.0` — **`configuration-precedence` is background, not a policy.** It
describes how resolution behaves — *the last one to speak wins* — so that a
reader can predict it. Nobody can violate precedence. It is now `type: document`
under `concepts/` and carries no trigger.

Minor: the layers are unchanged; the claim that they bound anybody was the
error.

`0.5.0` — **`compliance` is gone.** A policy binds because it is a policy —
that is what the type means — and what happens when it is broken is what
`on_violation` says. The field between them restated the type on documents that
bind, and offered a soft tier to documents that arguably should not be policies
at all.

Minor. Nothing a reader is obliged to do has changed.

`0.4.0` — **vocabulary.** `moment` becomes `event` — a moment is a point in
time and `applies_to` takes nouns. `compliance` is dropped wherever it was
saying nothing: a policy binds unless it says otherwise, so only a strong
default declares `recommended`, and a workflow's steps bind by being steps.
Type Definitions use `field_presence: required` for what was
`obligation: mandatory`, matching the format.

Minor. Nothing a reader is obliged to do has changed; what declares it has.

`0.3.0` — **`preload` is replaced by `compliance` and `applies_to`.** An author
now says how strongly a rule binds and when it governs; *when it is delivered* is
computed from those and never declared. Every rule here could state when it
applies, so **nothing in this bundle is loaded unconditionally any more** — it
arrives when the work matches and costs nothing before then.

Minor: a consumer reading `preload` finds nothing, and the loading behaviour of
every document changes.

`0.2.0` — **the manifest is `BUNDLE.md`.** Reserved markdown files are now
ALL CAPS across the estate, because nobody types all caps by accident: a file
becomes load-bearing only when somebody deliberately made it so, and writing
`bundle.md` now fails in the safe direction — ignored rather than silently wired
into machinery. Minor rather than patch, and pre-1.0 that is the tier for a
breaking change: anything naming the old path by hand stops resolving.

`0.1.1` — a heading no longer says how many things are beneath it. Wording only.

Patch: no normative sentence moved and a reader who correctly understood
`0.1.0` behaves identically. See `writing-style` in `lumastack/luma-catalog/project-documentation`
for the rule and the failure it prevents.

`0.1.0`, and the precedence chain is **designed rather than built** — only one
layer is read today. The rules here are what the chain will be when it exists,
which makes them worth writing down now and worth re-checking against the first
tool that implements more than one.
