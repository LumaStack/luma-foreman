---
type: bundle
version: 0.11.1
published: 2026-08-26
consumers: [project, organization]
entry_point: policy/luma-directory-layout
description: The .luma directory every luma tool writes into — the four tiers, what belongs in each, and the committed-only invariant that makes it trustworthy.
---

# Luma layout

Every luma tool writes into the same directory. Foreman puts audits in
`records/` and vendors bundles into `bundles/`; a backlog tool owns `backlog/`;
anything with settings drops a file in `config/`. **This is the contract they
all honour**, which is why it is written down once rather than implied by four
tools' behaviour.

The same idea as a filesystem hierarchy standard, scoped to a repository: any
tool writing into `.luma/` is bound by this the way anything writing to `/var`
is bound by FHS.

## What is here

- [[luma-directory-layout]] — the four tiers, what belongs in each, and the one
  invariant. Read first.
- [[initialize-luma]] — initialize `.luma/` in a repository that has none.
- [[migrate-into-luma]] — move an existing project's scattered material into it.

## Adopting this does not make it apply

Unusual for a bundle, and worth saying plainly. **The layout binds you whether
you adopt or not** — it is what the tools do. You adopt this so an agent working
in the repository can read the contract locally, without reaching for anything
remote.

Which means declining it does not opt you out of anything. It only means nobody
here can look the answer up.

## The two rules that carry the weight

**Lifecycle is the only axis.** Directories are cut by *what happens to a thing
over time* — intended, in force, happened — never by topic. A glossary and a
guardrail share a directory because they share a lifecycle, not because they are
alike. Adding a second axis means two questions deciding one location.

**Everything in `.luma/` is committed, no exceptions.** If uncommitted files
can live here, two agents on two machines read different rules for the same
project — a correctness failure in the one system whose job is saying what the
rules are. Machine-local state lives in `~/.config/luma/`.

## Consumers

Both levels. An organization's headquarters is a repository and keeps the same
four tiers; the fractal is deliberate.

## On the name, and where it may go

**`luma-layout` because it is what somebody guesses correctly with no context.**
A bundle name's job is to get the right reader to open it, not to summarise what
is inside — and the entry point covers the rules the moment they do.

**There is no special noun for it, deliberately.** An earlier draft called it
*the store*, and that word is claimed several times over — a Redux store, an app
store, browser storage, a retail store. Prose here says `.luma/` where the path
is meant and *the luma directory* where a noun is needed, and needs nothing
further.

**If this bundle ever grows past layout** — acquiring the luma model, the
vocabulary, what adoption and promotion mean — that is the point at which
something larger absorbs it, and `luma-base` or `luma-core` is the name for the
result. Neither is right today: `core` would promise the model this bundle does
not contain, and an agent opening it for that would find a directory layout.

## Version

`0.11.1` — **bundle IDs in this catalog gained their namespace.** A bundle here
is `lumastack/luma-catalog/<name>` rather than `luma/<name>`, because the
namespace now derives from where the catalog lives instead of being declared.
Every reference in this bundle's prose is updated.

**A fork can no longer publish under this catalog's name.** It lives somewhere
else, so it is named something else, and its bundles sit beside these in a
project rather than colliding with them.

*Type names are unaffected.* `type: luma/catalog` and its siblings name the
format, not this catalog, and resolve separately.

Patch: nothing but the identifiers a reference points at.

`0.11.0` — **a config file is named for its tool, and a config holds
overrides.** The layout showed `foreman.toml`; the binary is `luma-foreman`, and
a truncation makes a reader guess which tool a file belongs to. One file per
tool, named for the tool.

**And the directory now has a policy rather than only a purpose.** What is
absent from a config follows the tool and improves with it; what is written down
is frozen, so the smallest file ages best. Commented-out defaults are ruled out
for the same reason — uncommenting is one keystroke, and a stale copy of a
default becomes a frozen override pinned to the day the file was written. Point
at documentation or a command that reads live values instead.

**`initialize-luma` no longer creates `records/`.** The step existed because
something writes a decision or an audit almost immediately — but if that is
true the directory appears on its own, and git cannot commit an empty one, so
what it created existed on one machine and reached no clone. The workflow now
creates the two files that have contents on day one and lets every directory
arrive with its first entry.

Breaking, which below 1.0 the minor position carries: a project with
`.luma/config/foreman.toml` has to rename it, and `luma-foreman` reports the old
name rather than silently reading past it.

`0.10.1` — **"commit it before using it" asked for something git cannot do.**
`initialize-luma` says to create `.luma/records` and then commit `.luma/`, but
git tracks files rather than directories, so an empty `records/` cannot be
committed at all. Whoever followed the step committed `PROJECT.md`, saw
`records/` missing from a fresh clone, and concluded something had deleted it —
the exact outcome the step exists to prevent.

The step now names the exception and says what actually happens: `records/`
joins the repository with whatever is written into it first.

**No `.gitkeep`.** `.luma/` holds things that mean something, and a placeholder
would be the only entry that does not.

Patch: the instruction is the same one, no longer asking for an unreachable
state.

`0.10.0` — **the foreman commands were renamed.** `initialize-luma` now says
`luma-foreman get`, and the `CLAUDE.md` marker example shows `luma-foreman
apply`. `adopt` and `outfit` no longer exist.

Breaking, which below 1.0 the minor position carries: `initialize-luma` is a
sequence somebody runs, and on an older engine its first command fails.

`0.9.0` — **`applies_to` is now `matches`.** The old name obliged an author to
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

`0.8.0` — **vocabulary.** `moment` becomes `event` — a moment is a point in
time and `applies_to` takes nouns. `compliance` is dropped wherever it was
saying nothing: a policy binds unless it says otherwise, so only a strong
default declares `recommended`, and a workflow's steps bind by being steps.
Type Definitions use `field_presence: required` for what was
`obligation: mandatory`, matching the format.

Minor. Nothing a reader is obliged to do has changed; what declares it has.

`0.7.0` — **`preload` is replaced by `compliance` and `applies_to`.** An author
now says how strongly a rule binds and when it governs; *when it is delivered* is
computed from those and never declared. Every rule here could state when it
applies, so **nothing in this bundle is loaded unconditionally any more** — it
arrives when the work matches and costs nothing before then.

Minor: a consumer reading `preload` finds nothing, and the loading behaviour of
every document changes.

`0.6.0` — **the manifest is `BUNDLE.md`.** Reserved markdown files are now
ALL CAPS across the estate, because nobody types all caps by accident: a file
becomes load-bearing only when somebody deliberately made it so, and writing
`bundle.md` now fails in the safe direction — ignored rather than silently wired
into machinery. Minor rather than patch, and pre-1.0 that is the tier for a
breaking change: anything naming the old path by hand stops resolving.

`0.5.0` — how a tool writes into a file it does not own. New content; existing
use is unaffected.

**Written the day a tool first had to.** *Generated files are never the source*
was true and unhelpful the moment something needed to put an index into a
`CLAUDE.md` somebody had already written by hand — owning the file destroys
their work, owning none of it means nothing reaches an agent. A delimited
region is the answer, and the marker on generated output is the same problem
from the other side: a tool cannot clean up after itself unless it can tell
what it wrote.

`0.4.0` — two corrections and one addition. Existing use is unaffected; both
corrections remove a copy rather than requiring one.

**`.luma/_types/` states which contract wins; it is not the project's spare
copy.** `0.3.0` said it holds one contract *"whatever the adopted bundles happen
to carry individually"*, which endorses a second copy sitting beside an adopted
bundle that already has the type. **Vendoring is for travel** — a copy inside one
repository goes nowhere and drifts for free. Three cases now decide it, and only
two of them put a file there.

**`adopted.toml` records the commit.** A version says which release of a bundle
and a checksum says which bytes; neither says **alongside what**. Two bundles
adopted from one commit came from an internally consistent set, and that is worth
a line while nothing has written this file yet.

`0.3.0` — `.luma/_types/` is documented: contracts for Documents that live in no
bundle. New content; existing use is unaffected, and the directory is absent in
most repositories.

**It exists because `PROJECT.md` has no bundle to resolve its type from.** The
format resolves a contract from the bundle a Document lives in, and this one
lives above the tiers — so the repository has to answer for it. It is also the
project's *single* answer, where a bundle's `_types/` is scoped to that bundle:
adopted bundles may legitimately disagree about a type used inside them, but the
one file at `.luma/PROJECT.md` cannot have two contracts.

`0.2.0` — `.luma/PROJECT.md` is a reserved path this layout did not previously
document. New content; existing use is unaffected.

It is also the **first thing at the root of `.luma/` rather than inside a tier**,
which is a shape worth watching. The justification is that it has no lifecycle of
its own — it names the repository the tiers belong to — and **if a second file
ever claims the same exemption, that is the moment to check whether the four
tiers are actually short one.**

The layout was reasoned through carefully and **has never been used** — nothing
has adopted anything yet, and the first real project to migrate into it will
find things this could not.
