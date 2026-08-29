---
type: workflow
title: Add a setting
description: Decide where a new configuration value lives and how strongly it binds. Use when introducing any value somebody might want to change.
---

# Add a setting

Four questions, in order. Each one eliminates a home.

## 1. Would deleting it lose a decision somebody made?

**No** — it is derived. `~/.cache/<org>/<application>/`, and nothing else needs
deciding.

**Yes** — continue.

## 2. Does it belong to the project, or to whoever is running it?

**To the person.** Timeouts, log levels, an operator's preferred mode, anything
that must not affect a colleague. `~/.config/<org>/<application>/` — either
`config.toml` for every project or `projects/<id>.toml` for this one.

**To the project.** Which policies apply, what *done* means, which checks run.
`.luma/config/<tool>.toml`, committed. Continue to step 3.

**The test when it is genuinely unclear:** would two people on the same commit
get different results? If yes it is the project's, because that difference is a
correctness problem rather than a preference.

## 3. May somebody override it locally?

**Yes** — `[defaults]`. The project is suggesting a starting value.

**No** — `[require]`. Overriding it would mean the project's rules no longer
hold.

**When in doubt, `[defaults]`.** Tightening later takes away something nobody
was relying on. Loosening later removes a guarantee people may have built on,
and they will not notice until it matters.

## 4. Is it a secret?

**Then it is not a value.** Store the name of an environment variable, a path,
a keychain reference — anything but the secret.

`.luma/` is committed, so a secret written there is a secret published, and
nothing done afterwards unpublishes it.

## Then

Add it to `.luma/config/<tool>.toml` under the right table, or document the
machine-local key if it belongs to the operator.

**If the tool reads more than one layer now, it needs the resolution function**
— see [[configuration-precedence]]. Reading two layers in two places is how
they drift into disagreeing.
