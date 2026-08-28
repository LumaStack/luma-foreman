---
type: bundle
version: 0.5.1
published: 2026-08-27
consumers: [project]
entrypoint: policy/merge-commits
description: How changes get integrated — merge commits rather than squash or rebase, and the repository settings that make it true.
---

# Git workflow

How changes land. Today that is one rule and the settings that enforce it;
branching and commit-message conventions are the obvious siblings and are not
here yet.

**It prescribes no branching model.** Nothing here says trunk-based, gitflow, or
anything between — only what happens at the moment a branch is integrated.

**It is not tied to a forge either.** The rule is a property of git: squash and
rebase produce commits that are ancestors of nothing, so merged-detection fails
on GitLab, Forgejo, Gitea and Bitbucket exactly as it does on GitHub. Only the
*enforcement* is host-specific, and the workflow says which host its commands
are for.

## What is here

- [[merge-commits]] — pull requests are integrated with merge commits, and why
  that survives the objection everyone raises. Read first.
- [[configure-merge-settings]] — disable squash and rebase at the forge, and
  verify they stayed disabled.

## Why this is a policy and not a preference

Squash and rebase merging **break the only reliable answer to "is this branch
merged?"** Both produce new commit SHAs, so a branch's commits never become
ancestors of the target, and every ancestry-based tool — `git branch --merged`,
forge auto-delete, every cleanup script — concludes it was never merged.

The branch then reads as unmerged forever, and stale branches accumulate until
somebody verifies each one by hand.

The cost is a non-linear `main`, which is the objection people actually have.
`git log --first-parent` recovers the linear view on demand — and that is the
asymmetry the policy rests on: **the prettier view is recoverable, and the
information squash destroys is not.**

## Consumers

`project` only. Merge strategy is a property of a repository, and an
organization's headquarters is a repository like any other rather than a level
this applies at.

## Version

`0.5.1` — **`entry_point` is now `entrypoint`.** One word, per LKF §11.1, so the same word names the same thing at every level it appears.

Patch: one key renamed. Same value, same meaning, same `optional` presence, and `luma-foreman` reads both spellings while the rename lands.

`0.5.0` — **`applies_to` is now `matches`.** The old name obliged an author to
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

`0.4.0` — **vocabulary.** `moment` becomes `event` — a moment is a point in
time and `applies_to` takes nouns. `compliance` is dropped wherever it was
saying nothing: a policy binds unless it says otherwise, so only a strong
default declares `recommended`, and a workflow's steps bind by being steps.
Type Definitions use `field_presence: required` for what was
`obligation: mandatory`, matching the format.

Minor. Nothing a reader is obliged to do has changed; what declares it has.

`0.3.0` — **`preload` is replaced by `compliance` and `applies_to`.** An author
now says how strongly a rule binds and when it governs; *when it is delivered* is
computed from those and never declared. Every rule here could state when it
applies, so **nothing in this bundle is loaded unconditionally any more** — it
arrives when the work matches and costs nothing before then.

Minor: a consumer reading `preload` finds nothing, and the loading behaviour of
every document changes.

`0.2.0` — **the manifest is `BUNDLE.md`.** Reserved markdown files are now
ALL CAPS across the estate, because nobody types all caps by accident: a file
becomes load-bearing only when somebody deliberately made it so, and writing
`bundle.md` now fails in the safe direction — ignored rather than silently wired
into machinery. Minor rather than patch, and pre-1.0 that is the tier for a
breaking change: anything naming the old path by hand stops resolving.

`0.1.0`. The reasoning comes from a repository that hit the stale-branch failure
twice in one week and changed strategy because of it — but this bundle has been
adopted nowhere, and the configuration workflow has been run against no forge
but GitHub.
