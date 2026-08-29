---
type: type_definition
defines: slice
fields:
  covers:
    field_presence: required
    field_type: list of text
    desc: "the repository-relative paths read in this slice — the source coverage is derived from"
  contributors:
    field_presence: recommended
    field_type: list of actor
    desc: "everyone present, human and agent alike"
---

# Slice

One session of a sweep: a cluster of files read together, what was concluded,
and where each conclusion went.

**A working note rather than a report.** It is written once, never revised, and
archived with the sweep — so anything that must outlive the sweep leaves it at
the time rather than living here.

## `covers` is the source of coverage

The index in `charter.md` is a cache of these lists. That is the whole reason
this field is required and the whole reason it is paths rather than prose: a
cache that cannot be rebuilt is a source, and this one has to be rebuildable
because it is edited at every slice.

**List every file read, including the ones where nothing was found.** A slice
that names only the interesting files makes *examined and clean*
indistinguishable from *never opened*, which is the distinction the index
exists to preserve.

## `contributors` is how you tell the pairing happened

**One name here is the signal.** A sweep has two parties — one orients, the
other reads and speaks first — so a slice naming only the party that oriented
records something that reviewed some files, which is a different and much
cheaper thing.

**Neither seat has to be human**; see [[who-does-the-reading]]. What has to be
true is that the reader was a separate session and that it actually answered.

The test is mechanical: *did I hand this over and get a reply?* An open session
is not a party being present — auto mode with nobody reading, or output nobody
surfaced, is nobody there whatever the session claims.

## Nothing records who read first

The pairing turn asks that one party orient without judging and that the reader
speak first. **When that was inverted — they asked you to go first, or the file
warranted it — say so in the prose**, the way any stated weakness is disclosed.

*No field for it, deliberately.* It is a property of how one conversation went
rather than of the Document, and inventing a boolean in passing would be worse
than the gap. A reader can discount a disclosed weakness; the undisclosed one
is the harder problem.
