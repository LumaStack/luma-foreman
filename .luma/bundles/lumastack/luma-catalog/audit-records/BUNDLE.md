---
type: bundle
version: 0.7.2
published: 2026-08-27
consumers: [project, organization]
entrypoint: policy/audit-layout
description: Audits as records — findings written by one party, answered by another, closed by the first. The whole exchange lives in git.
---

# Audit records

An audit is worth keeping only if somebody answers it. This bundle carries the
shape that makes the answer part of the record: **findings written by one party,
a position taken by another, and a closure written back by the first.**

The exchange is the point. An auditor can see whether a finding was genuinely
addressed rather than merely acknowledged, a respondent can disagree without the
disagreement being erased, and both survive in git long after anybody remembers
the conversation.

```
.luma/records/audits/2026-12-23-e286f3bd9c11/
  audit.md          scope, commit, what was NOT examined      auditor
  findings/F-001-*.md                                          auditor
  response.md       a position on every finding                respondent
  verification.md   closed, or open and what would close it    auditor
```

## What is here

**Policy**

- [[audit-layout]] — where audits live, how they are named, and the three-party
  loop. Read first.
- [[writing-findings]] — what makes a finding actionable rather than an opinion.

**Workflows**

- [[conduct-audit]] — pin the commit, scope it, write the findings.
- [[respond-to-audit]] — take a position on every one, and point at evidence.
- [[verify-audit]] — check rather than accept, and close the loop.

**Templates** — [audit](templates/audit.md) · [finding](templates/finding.md) ·
[response](templates/response.md) · [verification](templates/verification.md)

## The four ideas worth knowing before reading further

**Independence, and the unit it is measured in.** The respondent must not be the
auditor and the verifier must not be the respondent — but the auditor returning
to verify is the design, which is why they legitimately write two of the three.
**The boundary is the session, not the model.** What compromises a record is
carried context, so a fresh session of the same model is a real second party, a
different model is better, and one session playing two parts is permitted,
weakest, and has to be disclosed.

**Any of the three may be a person, an agent, or a command.** They are recorded
as actors — `human:fsmith`, `agent:opus-5`, `process:luma-foreman-inspect` — and
each means something different to a reader. A deterministic command may verify
its own findings, because re-running it is evidence rather than self-assessment;
that exception does not extend to agents.

**Nothing records its own status.** Findings are immutable. What happened to one
is written by whoever acted on it, in their own document, and the current state
is *derived* by reading the exchange. Storing a status would mean somebody
editing a record they did not write — the one thing an append-only record exists
to prevent.

**Disagreement and acceptance are outcomes, not failures.** *You are right and
we are carrying this deliberately* is a legitimate answer and the most valuable
record of the four: six months later it is the difference between a decision
somebody made and something everybody forgot.

## Consumers

Both levels. A project audits its code and its own practice; an organization
audits conformance across projects. The exchange is the same shape either way.

## Version

`0.7.2` — **`entry_point` is now `entrypoint`.** One word, per LKF §11.1, so the same word names the same thing at every level it appears.

Patch: one key renamed. Same value, same meaning, same `optional` presence, and `luma-foreman` reads both spellings while the rename lands.

`0.7.1` — **bundle IDs in this catalog gained their namespace.** A bundle here
is `lumastack/luma-catalog/<name>` rather than `luma/<name>`, because the
namespace now derives from where the catalog lives instead of being declared.
Every reference in this bundle's prose is updated.

**A fork can no longer publish under this catalog's name.** It lives somewhere
else, so it is named something else, and its bundles sit beside these in a
project rather than colliding with them.

*Type names are unaffected.* `type: luma/catalog` and its siblings name the
format, not this catalog, and resolve separately.

Patch: nothing but the identifiers a reference points at.

`0.7.0` — **independence is a session boundary, not a model boundary.** The rule
said *one party must not write two of these*, which was wrong twice. It
contradicted the table directly above it — the auditor writes rows 1 and 3 by
design — and it pointed at the wrong axis.

**What compromises a record is carried context, not identity.** An agent that
argued a finding into existence defends it rather than re-deriving it. The model
is not what does that; the retained working state is. So the old rule forbade
something harmless — the same model appearing twice — and permitted the real
failure, one continuous session playing two parts.

**Three arrangements, ranked and all permitted**: a different model in its own
session, the same model in a separate session, and one session doing both. The
last is discouraged rather than forbidden, on the grounds that a rule nobody can
satisfy gets ignored quietly instead of argued with — and it must be disclosed,
with a named tell, a response that agrees with every finding.

**This also unifies two ideas the bundle carried separately.** `0.6.0` said an
auditor who has just worked on the subject cannot run an open-ended audit of it,
because its own context is the anchor. That is the same boundary: anchoring and
self-grading are one problem, and what carries between them is the session. The
deterministic-command exception now rests on it too — a checker is exempt because
it carries nothing between runs.

Minor: no document changes shape, and every existing audit stays valid. What
changed is which arrangements the workflows ask for and what they ask to be
written down.

`0.6.0` — **an audit starts by asking what it is for.** `conduct-audit` opens
with three questions: is this targeted or open-ended, what problems is it aimed
at, and what is the scope. **The shape is asked first, deliberately** — otherwise
anybody with a complaint ready gets a targeted audit without having chosen one.

**Both shapes are biased and the workflow says so.** Targeting is biased toward
what is already suspected, and a problem is usually a symptom, so an audit aimed
at one never looks at its cause. Open-ended is biased toward what is easy to
notice — and an auditor who has just worked on the subject cannot run one, since
its own context is the anchor whether or not anybody named one.

**A targeted audit now owes an answer to what it was aimed at, including when
the answer is *nothing found*.** A negative is a result, and an audit reporting
only what it found cannot tell anybody to stop worrying.

Minor: an existing audit stays valid and readable, and nothing about the finding
or response format changes.

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

`0.1.1` — a heading no longer says how many things are beneath it. Wording only.

Patch: no normative sentence moved and a reader who correctly understood
`0.1.0` behaves identically. See `writing-style` in `lumastack/luma-catalog/project-documentation`
for the rule and the failure it prevents.

`0.1.0`. The structure is borrowed from internal-audit practice, which is
well-tested — but this particular compression of it, into files in a repository
answered by agents, has been run zero times. The round-two mechanics in
particular are reasoned rather than exercised.
