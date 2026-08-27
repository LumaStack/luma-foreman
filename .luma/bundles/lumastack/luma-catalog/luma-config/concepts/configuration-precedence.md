---
type: document
title: Configuration precedence
description: Six layers, and why the committed file appears twice. What a project may suggest, what it may mandate, and what an operator may override.
---

# Configuration precedence

Lowest to highest. The last one to speak wins.

```
1. built-in defaults                              in code
2. ~/.config/<org>/<tool>/config.toml             yours, every project
3. .luma/config/<tool>.toml   [defaults]          project suggests — overridable
4. ~/.config/<org>/<tool>/projects/<id>.toml      yours, this project
5. .luma/config/<tool>.toml   [require]           project mandates — not overridable
6. environment variables and flags                this invocation only
```

## The committed file appears twice, on purpose

Layers 3 and 5 are **the same file**, read at two priorities, because it holds
two different kinds of statement.

```toml
[defaults]
log_level = "info"      # a starting value. Change it if you like

[require]
strict = true           # a rule this project holds. Your preference does not lift it
```

An earlier version of this said *the committed declaration always wins*, which
was too broad — it forbids a project suggesting a sensible starting value for
newcomers. **The invariant worth protecting is narrower: a local setting must
not switch off something the project requires.** A project may both suggest and
mandate, and splitting the file into two tables puts the precedence *in the
file* rather than in a rule somebody has to remember.

## What belongs in each table

**`[defaults]`** — anything an operator might reasonably want different. Log
level, verbosity, concurrency, output format. The project has an opinion and
does not care very much.

**`[require]`** — anything where an override would mean the project's rules no
longer hold. If a value being changed locally would make two people on the same
commit get different verdicts, it belongs here.

**When in doubt, `[defaults]`.** Moving a value from `[defaults]` to `[require]`
later tightens something nobody was relying on being loose. Going the other way
loosens a rule people may have been relying on, silently.

## Flags win, and never persist

Layer 6 affects one invocation and writes nothing. A flag that quietly persisted
would produce state nobody remembers setting — the worst kind, because the
symptom appears long after the cause and in a different session.

Keep the two acts distinct: **a command that writes configuration and a flag
that overrides it for one run are different commands**, and naming them the same
way invites exactly that confusion.

## Read per invocation, never memoize

Re-read the files every run. A short-lived process pays nothing for this, and it
is what makes *"change it and the next command sees it"* true rather than
approximately true.

The cost only appears when something long-lived exists, and at that point it
must re-read or watch. Building a cache before then is optimising a cost nobody
is paying.

## Build the chain at one site, even before you need it

Only one layer may exist today. Put the lookup behind a single resolution
function anyway, so the rest slot in at one place rather than being threaded
through everywhere a setting is read.

**Reserving the shape is free. Building the whole chain before there is anything
to resolve is not** — it is the same premature extraction that a shared package
before a second consumer would be.
