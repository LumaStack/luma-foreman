---
type: luma/idea
title: A bundle should carry migrations, one version at a time so they chain
created: { by: human:luma-foundry, at: 2026-09-10T06:38:27Z }
contributors: [human:luma-foundry, agent:claude-opus-5]
scope: project
stage: draft
---

# A bundle should carry migrations, one version at a time so they chain

**How to migrate the bundle, and any scripts required for upgrading bundle
versions — one version at a time, so migrations can be chained together
safely.**

Split from [[classify-bundle-contents]], where it is one item in a larger list.

## The problem it addresses

**Publishing a new version does nothing for anyone who already has the old
one.** Adopters hold vendored copies, which is the guarantee the model exists to
provide — nothing changes underneath a project — and the cost is that
`update-bundle` has to say plainly that **you cannot fix an adopter's copy by
publishing.** A serious defect needs the version bumped *and* every adopter
told, by hand.

**There is no mechanism between those two facts.** `migrate-bundle` exists but
answers a different question — moving a bundle between catalogs, or
restructuring it in place. Nothing takes an adopter from `0.15.1` to `0.16.0`.

**One version at a time is what makes it composable.** A migration written
`N → N+1` can be chained across any gap without anybody writing the
combinations; a migration written *from whatever you had* cannot be, and goes
stale the moment a third version exists.

## Notes

**Distinct from [[frontmatter-needs-a-version-and-types-need-migrations]], and
easily confused with it.** That one migrates *a document's frontmatter* across
**type** versions, and proposes `_types/<type>/` as a directory holding the
schema beside its migrations. This one migrates *a bundle* across **its own**
versions. Same word, different subject — and they may well share machinery,
which is a reason to keep the distinction explicit rather than a reason to merge
them.

**The estate has already felt this.** The catalog carries bulk commits like
*"Migrate every bundle to LKF spec v0.0.19"* and *"Migrate every bundle to LKF
spec v0.0.20"* — sweeps done by hand across every bundle at once, exactly the
work a chained migration would carry. The version log in `bundle-manager` also
jumps `0.13.1` → `0.15.1` because those sweeps bumped versions without recording
per-bundle entries.

**Worth deciding early:** whether a migration is a script, a procedure an agent
follows, or prose an adopter reads. Bundles are mostly prose, so many migrations
will not be executable at all — *rename this field in your own documents* is a
real migration with nothing to run. A design that assumes scripts will not cover
the common case.

**Interacts with `foreman get`**, which is where an adopter would meet a
migration. Also with the vendored-copy checksum in `MANIFEST.md`: a migration
that edits adopted files has to leave the receipt consistent, or the next
`inspect` reports the repair as damage.
