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

## Keep the noticing, drop the acting

The clause was pointing at something real — a draft that has gone into use
probably *should* be promoted. The error is doing it automatically. Keep the
observation and turn it into a prompt:

- **When a draft goes into use**, say so and ask whether to promote it.
- **When a draft has been in use for a while**, say so again.

Neither changes the record. Both put the decision in front of the only person
who can make it.

**"For a while" is legitimate here, even though recency was rejected above** —
because nothing is being authorised. A time-based *nudge* costs nothing when it
misfires; a time-based *permission* is what slides. Same word, different job.

## Two things this needs and does not have

**A definition of "in use."** The checkable one is citation: an `ADR-NNNN`
reference appearing in a commit message, another record, a policy, or a code
comment. *The thing it decided got implemented* is the honest meaning and
nothing can detect it.

That is the same measurement the edit ceremony really wants. The ladder keys how
much ceremony an edit needs on `lifecycle_status`, when what it is protecting is
**exposure** — how many places cite the number and would be wrong if the
position moved. Those usually correlate, and on a days-old repository they do
not at all. One count of inbound citations serves both: it decides when to
prompt, and it decides whether a record can still be revised in place.

**Somewhere for the reminder to live.** Agent behaviour written into a policy is
soft — an agent that does not read the policy that day does not remind anybody.
`luma-foreman inspect` is the hard version and does not fit as it stands: every
severity is a finding (`high`, `medium`, `low`) and any finding exits 1, so a
nudge would fail continuous integration over something that is not broken.

Either inspect grows a tier that reports without failing, or the reminder
belongs in a command somebody runs on purpose rather than in the gate. Worth
deciding before building, because the answer determines whether this is a
`decision-records` change, a `foreman` change, or both.

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

The policy half belongs upstream in `luma-catalog` — `luma/decision-records` is
vendored here and cannot be edited in place. The reminder half may belong in
`foreman` instead, which is why *where the reminder lives* is called out above
rather than assumed.

Filed in this project because the failure happened here: `luma-foreman`
ADR-0003, 2026-08-26.
