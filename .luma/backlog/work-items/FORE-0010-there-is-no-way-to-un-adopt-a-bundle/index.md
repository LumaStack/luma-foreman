---
type: work-item
key: FORE-0010
title: There is no way to un-adopt a bundle
workflow_status: captured
rank: 010.0090.000
kind: idea
stage: draft
created: {by: 'agent:claude-opus-5', at: '2026-08-26T00:00:00'}
description: '`get` adds a bundle and writes a receipt. Nothing removes one. Dropping a bundle means deleting its directory and editing `adopted.toml` by hand — a file whose own header says "Written by luma-foreman. Do not edit by hand." The 2026-08-26 namespace change moved every bundle from `luma/<name>` to `lumastack/luma-catalog/<name>`. Re-adopting wrote the new ones and left the old three behind — six entries, three orphaned directories, and no command for the second half of a migration the tool had just caused.'
modified: {by: 'agent:claude-opus-5/luma-backlog', at: '2026-09-24T19:43:37Z'}
---

# There is no way to un-adopt a bundle

`get` adds a bundle and writes a receipt. Nothing removes one. Dropping a bundle
means deleting its directory and editing `adopted.toml` by hand — a file whose
own header says *"Written by luma-foreman. Do not edit by hand."*

**The tool tells you not to do the only thing it leaves you.**

## Where it bit

The 2026-08-26 namespace change moved every bundle from `luma/<name>` to
`lumastack/luma-catalog/<name>`. Re-adopting wrote the new ones and left the old
three behind — six entries, three orphaned directories, and no command for the
second half of a migration the tool had just caused.

That case is one-off. The general one is not: a bundle you tried and did not
want, a bundle a catalog retired, a bundle superseded by one from somewhere
else.

## What it has to do

More than delete a directory, which is why it is a command rather than a note
telling somebody to use `rm`:

- drop the entry from `adopted.toml`, so the receipt matches what is there
- remove the vendored copy
- **and then `apply`**, because the generated skills and the `CLAUDE.md` index
  still name it. `apply` already removes a skill whose bundle left, so the last
  step is *run apply*, not *delete more files*

## What has to be decided

**Whether it refuses when the copy was edited.** `get` refuses to overwrite an
edited bundle, on the grounds that the edit is somebody's work. Deleting it is
the same loss with less warning. Probably the same refusal and the same
`--force`.

**Whether it can tell you what breaks.** A bundle is often linked from a
project's own documents. Removing it silently turns those into dangling links
that `inspect --rule bundles` reports afterwards — a warning before is worth
more than a finding after.

**What it is called.** `bundle remove` sits with the other bundle commands.
`drop` is shorter and says *this is not a deletion of your work, it is
un-taking somebody else's*. Neither is obviously right, and
[[work-items/FORE-0037-adopt-or-install-as-shorthand-for-get-plus-apply]] is relevant: if a compound verb ever lands,
the reverse should pair with it — an `install` that summons `uninstall` is the
objection filed there.

## Related work

- Born from the idea it replaces: [`no-way-to-un-adopt`](../../ideas/no-way-to-un-adopt.md)
