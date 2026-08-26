---
type: luma/idea
title: A promotion reminder needs somewhere to live, and inspect does not fit
created: { by: human:benlinton, at: 2026-08-26T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: project
lifecycle_status: draft
---

# A promotion reminder needs somewhere to live

`luma/decision-records` 0.9.0 says a record stays `draft` until its owner
promotes it, that citing a draft is discouraged, and that a citation **should
trigger a promotion request**. It does not say what does the triggering.

**Written into a policy, a reminder is soft.** An agent that does not read that
document today reminds nobody, and the person who needs the nudge is the one who
forgot the record exists. A rule whose enforcement depends on remembering the
rule is the shape this whole bundle exists to avoid.

## `inspect` is the hard version and does not fit as it stands

Every severity is a finding — `high`, `medium`, `low` — and **any finding exits
1**. A nudge would fail continuous integration over something that is not
broken, which is worse than not nudging: it teaches people that a red run means
nothing.

Two ways out.

**A tier that reports without failing.** `luma-catalog-curator` already has one
and calls it a *notice*: *"A notice is for a second reader, and never fails a
run."* It has earned its place there — it caught a real meaning shift during the
2026-08-26 vocabulary sweep, in a change that read as a rename. The same
distinction would serve here, and adopting the word the sibling tool already
uses beats inventing a second one.

The cost is real: a tier nothing fails on is a tier people stop reading. Whether
a notice belongs in the gate at all, or only in a command somebody runs on
purpose, is the question.

**Its own command.** `luma-foreman records` or similar — drafts in use, records
never promoted, citations pointing at something not in force. Nothing to fail,
because nobody runs it in CI. The cost is that it only helps whoever thinks to
run it, which is close to where policy text already leaves us.

## What it needs first

**A definition of "in use" that something can check.** The honest meaning is
*the thing it decided got implemented*, and nothing can detect that. The
checkable one is **citation** — an `ADR-NNNN` appearing in a commit message,
another record, a policy, or a code comment.

That is the same measurement
[[edit-ceremony-should-key-on-citations]] wants, and building it twice would be
the mistake. One count of inbound citations decides when to prompt *and* whether
a record can still be revised in place.

## Notes

The policy half shipped in `luma/decision-records` 0.9.0, published from this
repository on 2026-08-26 after a record was written straight to `provisional`
and had to be walked back. This is the half that did not ship, and it is a
foreman change rather than a bundle one — which is why it is filed here.
