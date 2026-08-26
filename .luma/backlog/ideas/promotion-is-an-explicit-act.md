---
type: luma/idea
title: Promoting a decision out of draft is an explicit act, not a side effect of using it
created: { by: human:benlinton, at: 2026-08-26T00:00:00Z }
contributors: [human:benlinton, agent:claude-opus-5]
horizon: next
scope: organization
lifecycle_status: draft
---

# Promoting a decision out of draft is an explicit act

`luma/decision-records` tells a writer to record something *"as a `draft`, or as
`provisional` the moment you start acting on it"* (`policy/decision-guidelines`).
Two options, no gate, and the second one fires by itself.

**A new record should be born `draft` and stay there until its owner promotes
it.** Acting on a draft must not promote it.

## Why the automatic trigger is wrong

**It makes promotion happen without anybody deciding.** *Starting to act on it*
is not an event with an owner — it has no moment, no author, and nothing to
disagree with. Every other transition in the ladder is somebody's choice.

**It contradicts what `provisional` means.** The status is defined as *"decided
and in force, but on trial."* If reaching the trial requires promotion, then a
`draft` can never be tried, and the rung degrades into *not written up properly
yet*. Trying something is how a draft earns promotion, not a consequence of it.

**It costs the most on a young project.** `provisional` permits editing the
explanation but *"still not the decision"* — only `draft` allows the position
itself to move. So a record that auto-promoted is locked, and reversing it needs
supersession ceremony: a new number, an archival, a `superseded_by`. That
machinery exists to protect citations. A record written an hour ago and merged
in one pull request has none.

## The fix

Strike the automatic clause. A record is `draft` until its owner says otherwise,
and using it changes nothing.

**This is not a recency rule.** *It is only a day old* is unenforceable and
slides. The gate is authorship: the person who owns the decision promotes it,
whenever that is.

## What it would have caught

`luma-foreman` ADR-0003 was written straight to `provisional` by an agent, in
the same gesture as writing it. Two of its positions were the agent's
recommendations rather than anything the owner had ruled on. Both were reversed
within the hour and the record had to be walked back down to `draft` to allow
it.

A promotion step would also have caught the second defect for free: the record
bundled three independent choices, which `decision-guidelines` warns against
because *"the first one to change drags two unrelated positions with it."* Three
positions in one record is obvious to whoever has to read it and say *yes, this
is in force* — and invisible to whoever is still writing it.

## Notes

**Related and separate:** the ceremony for editing a record is keyed on
`lifecycle_status`, when what it is really protecting is **exposure** — how many
commits, conversations and other records cite the number. Those usually
correlate and on a days-old repository they do not at all. Exposure is also
mechanically checkable, unlike recency: a rule could count inbound `ADR-NNNN`
references and let an uncited record be revised in place. Worth its own entry if
this one does not absorb it.

Belongs upstream in `luma-catalog`, not here — `luma/decision-records` is
vendored. Filed in this project because the failure happened here.
