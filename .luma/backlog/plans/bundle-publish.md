# Publishing a bundle to a catalog

## Context

`.luma/bundles/local/command-line-interface/` is a bundle written here and
published nowhere. ADR-0013 says outright that it "is written to be promoted".
There is no way to promote it.

ADR-0011 anticipated the gap and delegated it to `migrate-bundle`, adding that
"a dedicated command can follow if the procedure proves fiddly". **The
delegation points at a hole**: `grep -rn "local/"` across `bundle-manager/` and
`luma-maintainers/` returns nothing. Neither `migrate-bundle` nor
`publish-to-the-catalog` mentions `local/`, the move, or the `MANIFEST.md`
entry that has to change. The procedure it named was never written.

The outcome wanted: `local/command-line-interface` ends up as
`lumastack/luma-catalog/command-line-interface`, vendored with a real receipt,
with nothing in the repository still pointing at the old identity.

## The model this is built on

**Publishing is a custody handover, and the project ends up an adopter of its
own bundle.** This is what makes it unlike a package registry. When you
`npm publish`, your local source stays authoritative forever. Here, the moment
the bundle lands in the catalog the project stops owning it: the bare manifest
entry becomes a receipt with a catalog, a commit and a checksum, and editing
the bundle afterwards is divergence rather than authorship.

**The handover cannot complete until the recipient accepts**, so it spans a gap
of minutes or weeks that belongs to somebody else. That gap is the only reason
this is not one atomic command, and everything below follows from handling it
without guessing.

## The manifest, and the invariant that must not bend

**A namespaced entry always carries `sha256` and says where it came from.** No
exceptions, because an exception is where a bug hides — and because `inspect`
can then assert it outright: every namespaced entry is verifiable, or it is a
finding.

> **Corrected during implementation.** This said `commit` and `sha256`, and
> `commit` had to come out. A catalog that is not a git checkout has none to
> record, and `get` already reports that as `(not a git checkout)` rather than
> treating it as an error — so requiring it made a sanctioned adoption report
> as broken, which the existing `derived()` fixture in `adopt-test.sh` caught
> immediately. The checksum is what actually makes a copy verifiable: without
> it `state()` skips the drift comparison entirely and the check passes
> silently forever. The commit is custody that may honestly not exist.

That means the bundle keeps its `local/` identity for the entire time a request
is outstanding. Before the merge it genuinely has not been published; the
request may be declined. ADR-0011 says "the move is the moment identity is
acquired", and that moment is the merge, not the ask.

Three states, and only these:

```
- `local/command-line-interface` 0.1.0
```
*Written here. Nothing asked of anyone.*

```
- `local/command-line-interface` 0.1.0
  - catalog: lumastack/luma-catalog
  - request: https://github.com/LumaStack/luma-catalog/pull/41
```
*Written here, and a request is outstanding.*

```
- `lumastack/luma-catalog/command-line-interface` 0.1.0
  - catalog: lumastack/luma-catalog
  - commit: ce13c21e65900542c1570a6afdf903d8ac4fbf73
  - sha256: c86f02985e5b0986532193c35b5a4793e5f676fd71a4118957109c4d30564329
```
*Handed over. Vendored like anything else.*

**`catalog:` is continuous across the whole motion** — written once when the
request is opened, unchanged when the handover completes. It names the catalog
that has or will have custody. Which side of the merge you are on is carried by
the bundle ID and by whether `request:` is present, which is the same
distinguish-by-shape mechanism ADR-0009 already uses for bare entries. ADR-0012's
rule holds throughout: exactly one of `catalog:` and `source:` on an entry.

**`request:` earns its place by ADR-0009's own test** — the manifest holds
facts that cannot be recomputed. A pull request number is exactly that. You
cannot derive it, and the other party can destroy the evidence. Without it the
tool cannot tell *declined* from *never asked*, and would silently re-open a
request a maintainer had just closed.

No date is recorded. The request carries its own timestamps and git history
carries when the subline landed; a third copy is the one that drifts.

## Who owns what

**Foreman writes; the catalog's existing gate judges.** Curator gains nothing.

It has no write path anywhere in its source — two verbs, `check` and `report` —
and its charter forbids growing one: *"It never adopts. A curator that also
adopted would have collapsed the split it exists to express."* The gate already
exists and is wired: `luma-catalog/.github/workflows/ci.yml` runs
`curator check .`, `curator check --against origin/main .` and
`foreman inspect` as a required pre-merge job, with branch protection behind it.

So there is nothing for curator to accept or place. Foreman opens a PR
containing the bundle at its final path; curator runs in CI against that PR; a
maintainer merges. That *is* approve-or-reject, realised through git rather
than a protocol nobody has to build.

## The commands

Three verbs, each naming a goal rather than a procedure.

```
luma-foreman get      lumastack/luma-catalog/command-line-interface
luma-foreman remove   lumastack/luma-catalog/command-line-interface
luma-foreman publish  command-line-interface lumastack/luma-catalog
```

`get` and `remove` take one bundle ID because the ID fully determines them —
the namespace already says which catalog. **`publish` takes two operands
because where a bundle is going is not in its name and cannot be**, and the
same bundle may go to more than one catalog. The shapes differ because the acts
differ: `get` and `remove` are unilateral and instant, `publish` is gated and
slow.

Operand one is *which bundle*, operand two is *which catalog*:

```
luma-foreman publish command-line-interface        lumastack/luma-catalog
luma-foreman publish local/command-line-interface  lumastack/luma-catalog
luma-foreman publish acme/catalog/deploy           lumastack/luma-catalog
```

A bare name means `local/`. The `local/` prefix is accepted and redundant,
never refused. A full bundle ID names whichever bundle is meant, which is how
the promotion ladder's upper rungs work without a flag.

**Operand two is required** — an exact key lookup against the registry, whose
keys are namespaces. Inferring it from "there happens to be one registered
catalog" was rejected: it stops working the day a second is added, and it fails
by publishing somewhere nobody meant.

Flags: `--again` to open a fresh request despite a recorded one, `--abandon` to
stop tracking a request.

**`--again`, not `--force`.** `--force` means *override a guard protecting
something* — `get --force` overwrites an edited copy, `remove --force` destroys
unrecoverable work. Asking a catalog a second time defends nothing and destroys
nothing, so it earns its own word. `--retry` was rejected because a declined
request did not fail, it was answered; `--reopen` because GitHub already uses it
for restoring a closed PR, which is a different operation than opening a new one.
Each flag in the tool then means exactly one thing:

```
--force     override a guard protecting work nothing else holds   (remove, get)
--again     ask a catalog a second time                           (publish)
--abandon   stop tracking a request                               (publish)
```

### `publish` is one idempotent command

Run it whenever. It advances the handover as far as it can and reports where it
stopped.

```
$ luma-foreman publish command-line-interface lumastack/luma-catalog
opened  LumaStack/luma-catalog#41
  not published yet — a maintainer has to merge it.
  run this again afterwards to finish.

$ luma-foreman publish command-line-interface lumastack/luma-catalog
open    LumaStack/luma-catalog#41 — nothing to do yet

  ... weeks ...

$ luma-foreman publish command-line-interface lumastack/luma-catalog
merged  lumastack/luma-catalog/command-line-interface 0.1.0
  vendored   .luma/bundles/lumastack/luma-catalog/command-line-interface
  removed    local/command-line-interface
  applied    5 files
```

### Resolution, which asks rather than infers

| recorded state | what it does | exit |
| --- | --- | --- |
| no `request:` | open one | 0 |
| request open | report pending, change nothing | 0 |
| request merged | complete the handover, clear `request:` | 0 |
| request closed unmerged | report **declined**, change nothing | 1 |
| request not visible | report the possibilities, change nothing | 1 |
| cannot reach the forge | say so, change nothing | 2 |

**The only automatic transition is the merged one.** Everything else reports
and waits for a person, because everything else is somebody's decision.

An earlier draft resolved phase by looking for a pushed branch on the remote.
That was wrong: a maintainer who closes a PR and deletes the branch leaves no
trace, so the tool would conclude *never asked* and re-open the same request —
generating exactly the maintainer noise this is meant to avoid.

### When the request is not visible

**A 404 is not proof.** GitHub returns 404 rather than 403 for a private
resource you lack access to, so "not found" covers: declined and cleaned up,
the catalog renamed or moved, the catalog gone private, a token expired, or a
different authenticated identity. Concluding *declined* and clearing the record
would silently erase a live request, and the retry would duplicate it.

So enumerate, and make the retry explicit:

```
luma-foreman publish: the recorded request is no longer visible.

  bundle   local/command-line-interface 0.1.0
  catalog  lumastack/luma-catalog
  request  LumaStack/luma-catalog#41 — not found

  It may have been declined and cleaned up, or the catalog may have moved,
  become private, or stopped granting you access.

  To open a fresh request:
    luma-foreman publish command-line-interface lumastack/luma-catalog --again

  To stop tracking this one:
    luma-foreman publish command-line-interface --abandon
```

Reaching the forge and failing is different from not reaching it: an outage is
"could not run", exit 2, changing nothing, per the existing convention that an
outage is not a property of the repository.

### What opening a request does

Against a full clone of the catalog in `~/.cache/`, which is safe to lose
because the branch is pushed to the remote:

- copy the bundle to `catalog/bundles/<name>/`
- rewrite `title:` and the H1 from `local/<name>` to `<namespace>/<name>`
- add `published:` — catalog bundles carry it and `bundle new` deliberately
  omits it, because "a bundle written in a project has no publish moment"
- regenerate `INDEX.md` with the existing `bundle index`
- branch, commit, push, open the PR
- record `catalog:` and `request:` on the local entry

The version is left exactly as authored. Whether it is honest is the author's
call, and curator's `--against` check is what reviews it.

`gh` is shelled out to the way `git` already is, so "no dependencies" stays
true — it means no Python packages. It is also what makes the stranger case
work: `gh` forks transparently when push rights are absent.

### What completing the handover does

- take the published copy and write the receipt (`catalog`, `commit`, `sha256`)
- remove `local/<name>` — no `--force` needed, which is the tell the guard is
  positioned correctly
- repoint references to the old ID
- run `apply`
- report the version that landed, and say so plainly if it differs from what
  was sent

Completion reads what is actually in the catalog rather than what was sent, so
a reviewer bumping the version in the PR simply works.

**Reference repointing.** Exact occurrences of the old bundle ID and its path
prefix are rewritten in tracked files, and each changed file is named. Anything
ambiguous is reported rather than edited. This matters because ADR-0011
rejected leaving a symlink behind on the grounds that "a missed one fails
loudly — `inspect` reports dangling wikilinks". That is currently truer of the
record than of the code: ADR-0013 cites this bundle as a bare path, not a
wikilink, so nothing would catch it.

> **Reversed by the first real handover.** Rewriting was wrong almost
> everywhere. Of the files naming `local/command-line-interface`, one was a
> genuine pointer and the other was this plan — which discusses the unpublished
> identity throughout, including the three manifest states it illustrates.
> Substituting the new ID collapsed all three into the same line and turned the
> context paragraph into *"a bundle written here and published nowhere"* naming
> a published bundle. ADR-0013 would have gone the same way had it argued about
> the namespace rather than merely citing a path.
>
> **Nothing separates a pointer from prose about the old state by inspection**,
> because the difference is what the sentence means. So `publish` reports and
> exits 1, which is what `remove` already does with the same question, and what
> ADR-0011 counted on: a missed reference fails loudly rather than being
> prevented.

### `remove`

Top-level, mirroring `get`, and the primitive `publish` uses to retire the
local copy. It removes the vendored directory and its manifest entry; `apply`
then unwires the generated skills and index lines.

**The refusal keys on recoverability, not on the `local/` prefix:**

| state | recoverable by |
| --- | --- |
| vendored, clean | `get` — byte-identical, the checksum proves it |
| local, committed | git |
| local, uncommitted or never committed | nothing |
| vendored, edited | nothing, for the edits at least |

The rule is one sentence covering both kinds: **refuse when removing would lose
work nothing else holds.** That generalises what `get --force` already does for
an edited copy rather than inventing a second, differently-shaped guard.

```
luma-foreman remove: local/command-line-interface has uncommitted work
  Nothing else holds it — not git, and no catalog.
  Commit it first, or:
    luma-foreman remove local/command-line-interface --force
```

Recoverable cases proceed and say how to undo, which is ADR-0013's
name-the-literal-command rule applied to success:

```
removed  local/command-line-interface
  it was committed — recover with:
    git checkout HEAD -- .luma/bundles/local/command-line-interface
```

**Refuse rather than warn.** A warning after the fact is useless; one before it
needs a prompt, and this tool has none anywhere and would break the moment
anyone scripted it.

**Why recoverability rather than "local always needs `--force`":** if every
local removal required forcing, `publish` would have to pass `--force`
internally when it retires the local copy. A command forcing past its own
safety check means the guard is in the wrong place.

## Questions that were open, and how they were settled

**Announce-then-advance is not implementable, and `--check` was not needed.**
The plan chose announce-then-advance to answer the consent problem — one verb
spanning "open a request against someone else's repository" and "rewrite my own
project". It cannot be built: announcing *merged, run again to finish* and then
finishing on the next run requires distinguishing "the first time I saw this"
from "you have been told", which is state, and removing state is the whole
point of resolving from the request itself.

The answer was already in the design. **`publish` advances; `bundle show`
reports.** The reading verbs live under that noun already, so checking where a
handover stands never means running the thing that moves it, and no flag is
needed to make that safe.

**What survives a decline: `catalog:` stays, `request:` is cleared.** The
destination was a decision somebody made and is still true; only the request
died. A retry needs no re-typing.

**`--abandon` was built.** A dead record reporting itself every run is harmless
exactly once, and thereafter is how real warnings get ignored.

**`gh` is a hard requirement for opening a request**, refused with the install
and auth commands when it is missing. It is shelled out to the way `git` is, so
"no dependencies" — meaning no Python packages — still holds.

**One path, one gate, whoever owns the catalog.** If the curator exists so a
catalog is never corrupt, exempting the people who touch it most defeats it.
Homebrew's two tiers exist because taps are deliberately unreviewed, which is a
different promise than this makes.

**Curator auto-fixing stayed out**, and looks unnecessary rather than deferred:
because foreman normalises before the request is opened, the easy-defect class
largely never reaches the catalog. What is left is an author's judgment call or
a real fault, and neither is safe to auto-commit.

**The reference sweep exits non-zero** when something still cites a bundle
that left — and it reports rather than rewrites; see the correction above.

**`published:` is set when the request is opened.** Early if review runs long,
and nothing else sets it.

## Still open

**Publishing the same bundle to a second catalog.** Expressible under the
two-operand shape, but the second catalog then receives a bundle whose custody
trail says it came from the first. Nothing special is done about it.

**Forking is not automated.** A contributor without write access is told to
fork and open the request by hand — accepted for the MVP, and tracked as
[[publishing-should-fork-when-it-cannot-push]].

## Two bugs the first real run found

Worth recording because neither would have been obvious from reading the code.

**The work clone stayed on the branch it built.** A second run started from
there rather than the catalog's default branch, so the bundle appeared to be
published already and the run refused — a stale cache reporting itself as the
catalog's state. Reused checkouts now reset to the default branch and clean.

**`remove` asked "was this committed?" after deleting.** Git reports the
deletion itself as a change, so the answer was always *no*, and the recovery
line would have been wrong in exactly the case somebody needs it. It is asked
before anything is removed.

## Files

Foreman is stdlib-only Python with a hand-rolled `argv` loop and no CLI
library. Two new top-level verbs is a well-worn shape: a module, a lazy-import
branch, a `USAGE` line, a test suite.

| file | change |
| --- | --- |
| `src/foreman/publish.py` | new — resolution, normalisation, branch/push/PR |
| `src/foreman/remove.py` | new — the recoverability guard and the sweep |
| `src/foreman/cli.py` | dispatch branches at ~`:184-207`, `USAGE` at ~`:15-28` |
| `src/foreman/catalog.py` | reuse `find()`, `derive_namespace()`, `_root()`; add a writable clone beside the read-only cached one at ~`:109` |
| `src/foreman/adoption.py` | `catalog:`/`request:` on a local entry; rewrite an entry's ID; remove an entry |
| `src/foreman/bundle_index.py` | reuse to regenerate the staged bundle's `INDEX.md` |
| `src/foreman/inspect/rules/adoption.py` | assert the strictness invariant |
| `tests/publish-test.sh`, `tests/remove-test.sh` | new suites; `tests/run` globs, so no registration |

Sublines are already forward-compatible: ADR-0009's grammar ignores unknown
keys on read, so `request:` is a behaviour change rather than a format change,
and an older foreman reading a newer manifest still works.

Every module carries a docstring arguing why the command exists — that is where
this project keeps its design reasoning, and these need real ones.

## Records

- An ADR for the split, the verb, the two-operand shape and the strictness
  invariant, at `stage: draft`.
- A note on ADR-0011 that the mechanics landed as a command rather than in
  `migrate-bundle`, which its own text anticipated.
- `migrate-bundle` and `publish-to-the-catalog` claim mechanics they do not
  carry. Either they gain the `local/` steps or they point at the command.
  **Worth fixing whether or not this gets built**, and it is a catalog change,
  so it goes through the catalog's own publishing procedure.

## Verification

- `sh tests/run` — the suites plus foreman inspecting its own repository.
- New suites against a throwaway catalog built inline per existing conventions.
  Assert the exit code on every call, which is how the three-code rule is
  pinned here. The load-bearing cases are the refusals and the resolution
  table — especially closed-unmerged, not-visible, and unreachable, since those
  are what stop maintainers being spammed.
- `remove` refusals: uncommitted local, edited vendored, and both `--force`
  paths.
- The real one: publish `command-line-interface` into `luma-catalog`, let the
  gate run on the PR, merge, complete the handover here, and confirm `inspect`
  is clean and nothing still says `local/`.

## Defects found while exploring, not part of this work

- `src/foreman/bundle_index.py:181` tests `entry.source` alone. A bundle from a
  *registered* catalog records `catalog:` and leaves `source` empty, so its
  frozen index could be regenerated — the drift the function exists to prevent.
  Every other local-versus-vendored test checks both fields.
- Curator's word-count column keys on a trigger keyword the catalog has
  migrated off, so it reports 0 for every bundle and prints "Zero is the
  expected reading". That is the number its README says the tool exists to
  produce.
- `luma-catalog` CI pins a curator SHA three merges behind.
- `luma-catalog-curator`'s own adopted bundles are stale — old `luma/`
  namespace, `workflows/` rather than `procedure/`, `adopted.toml`.
