---
type: document
type_version: "0.0.1"
title: Migrate an ideas corpus into the backlog
description: How to move a project's .luma/backlog/ideas/ into work items — the ordering rule, what each field becomes, the two passes that cannot be combined, and the refusals and silent failures this ran into the first time. Written from the luma-foreman migration so another project can repeat it without rediscovering the same things.
stage: draft
survival: durable
created: { by: human:luma-founder, at: 2026-09-24T00:00:00Z }
---

# Migrate an ideas corpus into the backlog

**For a project whose ideas live as individual files in `.luma/backlog/ideas/`
and should become work items instead.** Written from doing it once, in
luma-foreman, under FORE-0002. Everything here is a decision that was actually
made, including the ones that turned out wrong mid-run.

**This is not `migrate-ideas`.** That procedure splits a single `IDEAS.md` into
individual files. If a project already has individual files, that procedure has
already run and does not apply. `tend-ideas` does not apply either — it maintains
the separate corpus rather than emptying it.

## Settle this before touching anything

**Does every idea move, or only the ones ready to be judged?** If the intent is
to retire the `backlog-ideas` bundle afterwards, the answer is forced: all of
them, because the bundle has no reason to stay adopted once the corpus is empty.
Decide it explicitly rather than discovering it halfway.

**Read the corpus first.** Worked-out ideas of a hundred lines and one-line
thoughts migrate the same way mechanically but classify differently. If the
median body is substantial, these are not raw thoughts.

## The order

**Rank by `horizon` first, then by `created` ascending within each band.**
`next`, then `later`, then `someday`, then ideas with no horizon at all.

**Create them in that order and rank takes care of itself.** Each new record
lands at the back of the `captured` band, so creation order *is* the resulting
order. No `rank` calls are needed.

## What each field becomes

| idea field | becomes |
| --- | --- |
| `title` | `title`, verbatim |
| body | the work item's body, verbatim, with its `#` heading replaced by the title |
| `created` | `created`, **both `by` and `at` preserved by hand** |
| `stage` | `stage` |
| `horizon` | nothing — it has already done its job by setting the order |
| `scope` | nothing |
| `contributors` | nothing |
| `type: luma/idea` | `type: work-item` |
| — | `kind: idea`, on every one |
| — | a `description`, which ideas do not have and listings need |

**`kind: idea` for all of them, even the ones that look like defects.** They are
still ideas; nobody has judged them. Classifying during the move is a second
decision smuggled into a mechanical one, and `kind` is cheap to change later.

**`created` must be written by hand.** `work-item new` derives it from the clock
and the environment and has no flag to set it. Left alone, every migrated idea
reads as created today by an agent, and a corpus loses months of provenance in
one run.

**Set `LUMA_BACKLOG_ACTOR` before starting.** Unset, the actor falls back to the
OS account name and writes a workstation identity into every record.

**Derive the `description` from the idea's opening paragraphs**, not from a
summary you compose. These corpora are written with the idea stated plainly at
the top, so the lead is already the description. Strip emphasis, collapse
wikilinks to bare text, stop at a sentence boundary.

## Two passes, and they cannot be combined

**First create every work item. Then fix the links.**

Ideas cross-reference each other by slug — `[[some-other-idea]]` — and those
slugs resolve against the ideas directory. The moment an idea becomes a work
item, every link pointing at it breaks silently.

**Rewriting during the run is impossible**: the second record links to the
thirtieth, which has no key yet. So the bodies are knowingly wrong between the
first creation and the end of the link pass. Accept that rather than leaving
permanent dead citations.

**The link pass**, once every key exists:

1. Build a map from idea slug to new work-item directory name, matched on title.
2. In every migrated body, rewrite `[[slug]]` to `[[work-items/FORE-NNNN-…]]`.
3. Leave anything already namespaced — `work-items/…`, `plans/…`, an ADR.
4. Report what still does not resolve, and read the list rather than trusting it.

**Expect residue, and expect most of it to be innocent.** Prose examples — a
document explaining what a `[[wikilink]]` is — must not be rewritten. Links into
other repositories never resolved locally and still do not. Neither is damage
this migration caused, and saying so is part of the report.

## Ideas already marked archived

**They are deliveries, not work.** Close them `completed` rather than leaving
them open or dropping them.

**`close … completed` refuses a record with no outcomes** — *"nothing says it was
completed"* — and it is right to. Each one needs an outcome written from what its
own closing note claims, then verified, then closed.

**Verify by running the check, not by believing the note.** A note saying an
estate-wide invariant held on a date is evidence about that date. One of these
claimed every typed document carried `type_version`; the invariant had since
rotted, and the honest fix was to narrow the outcome to the delivery that
actually shipped rather than assert a condition that is no longer true.

## The back-link

**Give every migrated record a `## Related work` section pointing at the idea it
came from**, as a relative path so it resolves in an editor and on the forge:

```markdown
## Related work

- Born from the idea it replaces: [`the-slug`](../../ideas/the-slug.md)
```

**Which means the idea files stay, at least until the review is done.** Deleting
them is a separate decision, made after somebody has used these links to check
the migration.

## Things that will bite

**A script that runs the tool must check the exit code.** Three closes failed
silently on the first run because nothing read the result, and the records looked
migrated while sitting in the wrong state.

**`set <ref> title=…` changes the field, not the filename.** The record is still
addressed by its original slug afterwards, and a follow-up command using the new
title fails to resolve.

**An idea with no frontmatter is not a record.** Two here were raw notes — a
question list and a pasted `--help` transcript. They migrate, but the title has
to come from the `#` heading or the filename, and there is no `created` to
preserve.

**`work-item new` does not write `type_version`.** Every record this migration
creates is missing it, which is worth knowing before a linter is pointed at the
result.

**Python's `**` glob skips dot-directories.** Any verification sweep written that
way silently never opens `.luma/` and reports a clean estate. Use `os.walk`.
