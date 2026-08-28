---
name: load-bundle
description: Open one adopted bundle and see what it holds — its rules, what fires each one, and anything that applies throughout it. Use when a bundle's line looks relevant, or when asked to load a bundle by name.
---

<!-- luma-foreman:generated navigation. Regenerate with `luma-foreman apply`; edits are lost. -->

# Open a bundle

Read `.luma/bundles/rings/<bundle-id>.md`.

**The bundle ID carries its namespace** — `lumastack/luma-catalog/git-secrets`,
never `git-secrets`. Guessing at one is the only way this fails, so take it from
`.luma/bundles/entrypoint.md`, which lists every adopted bundle beside the path to its ring. Use
`/list-bundles` if you do not have a name at all.

**What you get.** Anything the bundle says applies throughout it, to read now;
then every rule it holds, with what fires each, and a line naming anything that
reaches you by another route. **Bodies are not included** — open the ones that
match the work, and not the rest.

**If the path does not exist**, the bundle is not adopted here. That is an
answer, not an error.
