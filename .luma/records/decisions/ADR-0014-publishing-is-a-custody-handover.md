---
type: decision
title: Publishing is a custody handover
decided: 2026-09-03
stage: draft
reopen_trigger: A catalog wants to receive something other than a pull request — a queue, a staging area, or a bot that materializes a submission — at which point foreman is no longer talking to the forge and the resolution table has nothing to ask.
---

# ADR-0014: Publishing is a custody handover

`publish` offers a bundle written here to a catalog and, once a maintainer has
merged it, takes it back as a vendored copy and retires the local one. It is
one idempotent command spanning a gap that belongs to somebody else.

## Problem

A bundle written in a project lives under `local/`, and nothing could move it
anywhere. [[ADR-0011-local-bundles-live-under-local]] said publication was the
rename and delegated the mechanics to `migrate-bundle`, adding that "a
dedicated command can follow if the procedure proves fiddly".

**The delegation pointed at a hole.** `migrate-bundle` and
`publish-to-the-catalog` never mentioned `local/`, the move, or the manifest
entry that has to change. The procedure named as the owner was never written,
so the fiddliness could not be assessed — there was nothing to find fiddly.

## Decision

**Publishing is a custody handover, and the project ends up an adopter of its
own bundle.** That is what makes it unlike a package registry: `npm publish`
leaves your source authoritative forever, and this does not. The moment the
bundle lands, the bare manifest entry becomes a receipt and editing the bundle
is divergence rather than authorship.

**Foreman writes; the catalog's existing gate judges.** There is no protocol
and no service. `publish` opens a pull request containing the bundle at its
final path; the catalog's pre-merge job runs `luma-catalog-curator check`
against it; a maintainer merges. Approve-or-reject realised through git.

**The curator gains nothing.** It has no write path and its charter forbids
one — *"It never adopts. A curator that also adopted would have collapsed the
split it exists to express."* A design where foreman sends a request and the
curator materializes it was considered and rejected: it needs a transport
nobody has built, makes the curator a writer, turns a submission into a new
shared type, and — decisively — stops the pull request being what a maintainer
approves. The diff is the contract; that is why fork-and-pull-request works for
strangers across all of open source.

**Two operands, `publish <bundle> <catalog>`.** `get` and `remove` take one
bundle ID because the namespace already says which catalog. A bundle written
here has no namespace to read, and the same bundle may go to more than one
catalog, so the destination cannot be inferred and is required. A bare name
means `local/`; the prefix is accepted and redundant; a full ID names whichever
bundle is meant, which is how the promotion ladder's upper rungs work without a
flag.

**One idempotent command, and the only automatic transition is the merged
one.** Everything else reports and waits for a person, because everything else
is somebody's decision. `bundle show` reads the state without advancing it, so
nobody has to run the thing that moves it in order to find out where it stands.

**A namespaced manifest entry always carries a checksum and says where it came
from.** No exceptions, so there is no exception for a bug to hide in, and
`inspect --rule adoption` asserts it. The commit is deliberately not required:
a catalog that is not a git checkout has none, which `get` already reports
rather than treats as an error.

**So the bundle keeps its `local/` ID while a request is outstanding.** Before
the merge it has not been published and may yet be declined. ADR-0011 says the
move is the moment identity is acquired, and that moment is the merge.

**`request:` on the entry, because nothing else can answer *declined* versus
*never asked*.** [[ADR-0009-the-manifest-records-custody-and-intent]]'s test is
that the manifest holds what cannot be recomputed, and a request URL cannot be:
you would have to go searching, and the other party can destroy the evidence.
`catalog:` is the same field a vendored receipt uses, written once when the
request opens and unchanged when the handover completes — it names the catalog
that has or will have custody. No date is recorded; the request carries its own
and git carries when the subline landed.

**`--again`, not `--force`.** `--force` overrides a guard protecting something.
Asking a catalog a second time defends nothing and destroys nothing, so it gets
its own word, and each flag then means exactly one thing.

## Why

**A 404 is not proof.** GitHub answers 404 rather than 403 for a private
resource you cannot see, so *not found* also covers a catalog moved, gone
private, a token expired, or a different identity. Concluding *declined* and
clearing the record would erase a live request, and the retry would duplicate
it in a maintainer's queue with no human having decided to send it. So the
possibilities are enumerated and asking again is explicit.

**An earlier design resolved the phase by looking for a pushed branch, and it
was wrong.** A maintainer who closes a request and deletes the branch leaves no
trace, so the tool would conclude *never asked* and re-open what had just been
declined — manufacturing exactly the noise a curated catalog exists to prevent.
That failure is what `request:` buys its place with.

**One path, one gate, whoever you are.** If the curator exists so a catalog is
never corrupt, exempting the people who touch it most defeats it — you can
break your own catalog as easily as a stranger can, and more often. Homebrew's
two tiers exist because taps are deliberately unreviewed, which is a different
promise. The difference between a maintainer and a stranger is handled by git.

## Alternatives

**`propose` or `submit`.** Nearly taken: curated repositories reach for those
words and self-service registries say `publish`, so the convention cuts against
it. Rejected because this tool's verbs name goals rather than procedures — `get`
does not say fetch-and-copy-and-write-a-receipt — and the command does deliver
publication, across invocations. What makes it honest is the output saying a
maintainer still has to merge.

**`share`, `push`.** Rejected. `push` is git's word for sending commits
unilaterally with no review, which is the opposite of what happens, and this
runs `git push` inside itself. `share` implies no gatekeeper, and *shared*
already means read-by-many here.

**A composed `vendor` verb for the second half.** Rejected: it is the shorthand
objection filed in [[adopt-or-install-as-shorthand]]. The act decomposes into
`get` and `remove`, both wanted anyway.

**`--check`.** Rejected as a weak answer to one verb spanning two acts.
`bundle show` is the reading path, and reading verbs already live under that
noun.

## Standing consequences

**`remove` exists, and its guard keys on recoverability rather than on where a
bundle came from** — refuse when removing would lose work nothing else holds.
That generalises the refusal `get` already makes over an edited copy. It is
also the tell that the guard sits in the right place: `publish` retires the
local copy without forcing anything, because by then the bundle is in the
catalog and in git.

**Forking is not automated.** A contributor without write access is told to
fork and open the request by hand. `gh` would do it; the flow is not built or
tested here, and half-doing it would fail in the case that matters.

**`migrate-bundle` and `publish-to-the-catalog` now claim mechanics they do not
carry.** They are catalog content, so fixing them goes through the catalog's
own publishing procedure rather than this repository.
