---
name: load-bundle
description: Open one adopted bundle and see what it holds — its rules, what fires each one, and anything that applies throughout it. Use when a bundle's line looks relevant, or when asked to load a bundle by name.
---

<!-- luma-foreman:generated navigation. Regenerate with `luma-foreman apply`; edits are lost. -->

# Open a bundle

Read `.luma/bundles/rings/<bundle-id>.md`, where the bundle ID is the full name
including its namespace — `lumastack/luma-catalog/git-secrets`, not
`git-secrets`.

`.luma/bundles/entrypoint.md` has every adopted bundle and the path to its ring. Use
`/list-bundles` if you do not know the name.

**What you get.** Anything the bundle says applies throughout it, to read now;
then every rule it holds, with what fires each. **Bodies are not included** —
open the ones that match the work, and not the rest.

**If the path does not exist**, the bundle is not adopted here. That is an
answer, not an error.
