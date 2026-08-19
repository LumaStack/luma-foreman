# Next steps

This will be a short lived file.

## Where things stand

Ten bundles exist in `luma-catalog`, the format is at `v0.0.9`, and
`luma-hq/DECISIONS.md` carries twenty-one settled decisions. **Nothing has
adopted anything** — no repository has a `.luma/` directory, so every layout
decision, the vendoring path, `adopted.toml` and the skill projection are
reasoned and untested.

That is the largest open item, and two things this week made the case for it:
three repositories did not have the merge settings their own bundle prescribes,
and merged branches piled up unnoticed. Both are what adoption plus `inspect`
would surface without anybody remembering to look.

## Answered, and where the answer lives

The rehoming questions this file opened with are mostly settled.

- **Catalog and bundle design** → `luma-hq/DECISIONS.md`. The reach and
  obligation axes, starters, tags, most-restrictive-wins, catalogs not
  inheriting, the `.luma/` store, and the single-valued-and-permanent rule for
  what a path may carry.
- **Bundle conventions** → the `bundle-manager` bundle. Layout, promotion, the
  audit checklist, and the overlap stance.
- **Structural checks** → `foreman inspect --rule bundles`.
- **Format questions** → `luma-knowledge-format/docs/ROADMAP.md`.

## Still open, in roughly the order they matter

**Adopt something.** `luma-foreman` adopting `luma/git-secrets` would exercise
the whole path — vendor into `.luma/bundles/`, write `adopted.toml`, and find
out what the layout gets wrong in a repository that already has opinions about
its own files. Nothing else will teach as much per hour.

**Do the standards used to build luma tooling live outside luma tooling?** The
question this file opened with, and the one still genuinely unanswered. If
`luma-foreman`'s own release process lives in a bundle it has to adopt, is that
elegant or an ever-present headache for maintainers? Adoption is what settles
it — the answer is currently a guess either way.

**Will anything ship natively in foreman or hq, or is everything fetched?** Same
question from the other side. Unanswered.

**How `Rejected` gets expressed.** Recorded in
`decision-records/_types/decision.md` with three options and no choice. Waiting
on whether another document type needs the same distinction.

**Whether `concept` survives.** On the format's roadmap, waiting on a durable
knowledge base — the thing it was written for and which nobody has built.

## Wanted, not built

Captured here rather than in `IDEAS.md` because each is a bundle somebody could
sit down and write, not a capability needing design.

- **Incident response** — the `IDEAS.md` entry has the reasoning; it needs a
  bundle. Records go under `.luma/records/`, so it is `incident-records`.
- **`log-records`** — named in passing when the `*-records` family was decided,
  never written.
- **Testing strategy** — including where a project states what *done* means,
  which `project-documentation` currently points at and nothing owns.
- **Prose conventions** — spelling, terminology, house style. Would apply to
  every bundle including the ones already written.
- **Logging** — whether it is a bundle or something foreman does natively is
  itself part of the open question above.
- **Working-style preferences** — how an agent should behave here, as adoptable
  content rather than as `CLAUDE.md` prose nobody versions.

## Foreman capabilities still stubbed

`bootstrap`, `outfit` and `refit` exit 2. `outfit` is the one that matters
first, since it is what turns an adopted bundle into something a harness can
use — and the projection design in `IDEAS.md` has been reasoned but never run.
