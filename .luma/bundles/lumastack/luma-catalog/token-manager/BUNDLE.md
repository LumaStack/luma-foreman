---
type: bundle
version: 0.10.1
published: 2026-08-26
consumers: [project, organization]
entry_point: workflows/token-tutorial
description: Where an agent session's tokens actually go — a paced tutorial on the mechanism and the fixes that follow from it, and an audit that measures a real setup instead of guessing at it.
---

# Token manager

**People run out of tokens and conclude they asked for too much.** Almost always
they did not. The model has no memory, so every turn resends the entire
conversation from the top — and what the human typed turns out to be a rounding
error next to the agent re-reading things it was already sent.

That single fact reorders everything. It makes the cheapest fix free and five
letters long, and it makes the move people reach for when they are trying to save
money — switching to a smaller model mid-session — the most expensive keystroke
available to them.

## What is here

**Workflows**

- [[token-tutorial]] — the mechanism and what follows from it, presented a step
  at a time with a pause after each, ending in a quiz.
- [[token-audit]] — measures one real setup and reports what is costing what.
  Changes nothing.

**Types** — [[tutorial_step]] · [[tutorial_quiz]], both vendored from
`lumastack/luma-catalog/luma-types` rather than invented here. They describe any paced walkthrough,
not this one, and the next tutorial takes the same copies.

The tutorial carries its steps beside it as documents of those types, read one
at a time and never all at once — both the cheap way to run a tutorial and the
only way this particular tutorial can run without contradicting itself.

**`tutorial_step` exists for one field.** A step declares whether the reader can
act on it here, must go elsewhere, or has nothing to act on at all, because
several of the recommendations would destroy the session delivering them and the
reader has no way to tell which. That is a behaviour a consumer dispatches on,
which is what earns a type rather than a label.

## Learn the mechanism, then measure

**The workflows answer different questions.** *What should I do about any of
this* is answered by the tutorial; *what is wrong with my setup specifically* is
answered by numbers from your own machine.

**The tutorial runs the audit as its last step**, and that ordering was got wrong
the first time. Measuring first sounds obviously right — you would be ranking
real problems instead of reading general advice — but **a finding you cannot
interpret is not a ranked problem, it is a line of output.** *Tool deferral is
not active* means nothing until you know what deferral was doing for you.

The other cost is worse and less obvious. **Sending somebody off to run an audit
three steps into a walkthrough is where they stop being in a walkthrough.** It is
a long, output-heavy job in another window, and the tutorial is competing with
whatever they find. At the end, wandering off costs nothing, because there is
nothing left to lose them from.

Somebody who already knows the material should run the audit on its own. It does
not need the tutorial; the tutorial needs it last.

## Nothing here changes a setting

The audit measures and reports; it edits no file and flips no switch. The
tutorial explains and waits; it applies nothing on the reader's behalf.

**That is deliberate, and it is not caution.** Every fix in here is a trade
against something the person actually wants — the tools they connected, the
schedule they chose, the model they prefer — and a bundle that quietly turned
those off would be optimising a number nobody asked it to optimise. The reader
makes the trade. This bundle makes sure they can see it.

## The numbers in here have a shelf life

Token costs, cache lifetimes, which servers are expensive, whether tool deferral
is on by default: all of it moves, and some of it has moved since these
workflows were written. The figures are here because a claim with a number
attached is one somebody can check, and a claim without one is one nobody ever
tests.

**So the mechanism is what to trust, and the figures are illustration.** If a
number here disagrees with what `/context` and `/usage` say on the machine in
front of you, the machine is right — and the tutorial ends by pointing at those
meters for exactly that reason.

**The same split applies to the harness.** Both workflows are written for Claude
Code and name its commands directly. The reasoning holds anywhere — no memory,
everything resent each turn, a cache a model switch invalidates — while the
keystrokes are between renamed and absent elsewhere. The tutorial says so before
its first step rather than letting somebody discover it at a command that does
not exist.

## Consumers

Both levels, because the fixes split across them. The output-filtering hook, the
memory files and the set of connected servers belong to a repository. The habits
— clear between jobs, choose the model once, check what fires overnight — are the
kind of thing an organization has an opinion about once rather than every person
rediscovering at their own expense.

## Version

`0.10.1` — **bundle IDs in this catalog gained their namespace.** A bundle here
is `lumastack/luma-catalog/<name>` rather than `luma/<name>`, because the
namespace now derives from where the catalog lives instead of being declared.
Every reference in this bundle's prose is updated.

**A fork can no longer publish under this catalog's name.** It lives somewhere
else, so it is named something else, and its bundles sit beside these in a
project rather than colliding with them.

*Type names are unaffected.* `type: luma/catalog` and its siblings name the
format, not this catalog, and resolve separately.

Patch: nothing but the identifiers a reference points at.

`0.10.0` — **vocabulary.** `moment` becomes `event` — a moment is a point in
time and `applies_to` takes nouns. `compliance` is dropped wherever it was
saying nothing: a policy binds unless it says otherwise, so only a strong
default declares `recommended`, and a workflow's steps bind by being steps.
Type Definitions use `field_presence: required` for what was
`obligation: mandatory`, matching the format.

Minor. Nothing a reader is obliged to do has changed; what declares it has.

`0.9.0` — **`preload` is replaced by `compliance` and `applies_to`.** An author
now says how strongly a rule binds and when it governs; *when it is delivered* is
computed from those and never declared. Every rule here could state when it
applies, so **nothing in this bundle is loaded unconditionally any more** — it
arrives when the work matches and costs nothing before then.

Minor: a consumer reading `preload` finds nothing, and the loading behaviour of
every document changes.

`0.8.0` — **the manifest is `BUNDLE.md`.** Reserved markdown files are now
ALL CAPS across the estate, because nobody types all caps by accident: a file
becomes load-bearing only when somebody deliberately made it so, and writing
`bundle.md` now fails in the safe direction — ignored rather than silently wired
into machinery. Minor rather than patch, and pre-1.0 that is the tier for a
breaking change: anything naming the old path by hand stops resolving.

`0.7.1` — wording in the opening three steps. No normative sentence moved, and a
reader who correctly understood `0.7.0` behaves identically.

The mechanism step counts in **turns** rather than messages and carries a bigger
number — a 3,000-token file read on turn one costs 300,000 tokens by turn one
hundred, which is the same arithmetic at a scale somebody feels. `/clear` leads
with the instruction instead of a claim about itself, and `/rename` before
`/clear` is put as muscle memory rather than as advice.

**The version check flags this patch for editing a sentence containing
*always*,** and the flag is answered rather than ignored: the edit was
*to keep it simple* becoming *for simplicity* in front of it. The rule that
follows the word is unchanged, so nobody behaves differently — which is the
patch test, and the reason a notice asks for a reader instead of failing.

`0.7.0` — the last step no longer points at a step that does not exist, and it
stops implying the tutorial is over.

**The closing block said *next for step 21*.** Every block takes the step number
and adds one, which is right nineteen times out of twenty. The last one now says
*next for the quiz*.

**And the audit step said this session ends with `/clear`.** It does, eventually,
but the quiz comes first — and the reader being told to clear before answering the
last question is the one instruction that could actually cost them the tutorial.
The reason to run the audit elsewhere is now simply that a substantial report
belongs where you work, which is true and does not reach for the ending.

**`exponentially` restored** in the mechanism step's takeaways. Its ordinary
sense — *increasing more and more rapidly* — is the one meant and the one a
reader will take; the correction to it was reading a plain word as a technical
claim.

`0.6.0` — **the audit moved from the third step to the last**, and the prose was
worked over throughout.

The ordering is the substantive change and the reasoning is above, under *learn
the mechanism, then measure*. Short version: a finding you cannot interpret is
not a ranked problem, and step three is where a reader stops being in a
walkthrough.

**The mechanism step now states the rule before the example.** It had asked the
reader to infer *each message re-buys everything before it* from a worked case;
it now says so, then walks the ladder. The file-cost example lost its arithmetic
step too — *read at the beginning of a forty-turn session* rather than *on turn
four*, which is one less thing to hold.

**`/rename` is framed as archiving**, which is a mental model rather than a
mechanism, and it survives the reader forgetting the details.

**Every step from 3 onward was renumbered**, so their Document IDs and wikilink
slugs moved — `04-clear-between-jobs` is now `03-clear-between-jobs`, and so on.
Nothing outside the tutorial links to an individual step, and the running order
moved with them, so an adopter re-adopts and it works. Anything that did cite a
step by ID does not.

Wording throughout is the author's, not tidied into house voice.

`0.5.0` — the opening stops narrating how the tutorial works.

It had been explaining the format before any of the material: one step at a time,
a pause after each, what the pause was for. **All of that is the agent's business
rather than the reader's**, and saying a pause is coming bought them nothing they
would not learn a moment later by reaching it.

The workflow keeps the reasoning — it is what needs to understand why the pause
matters — and gains a rule against describing it, beside the existing one against
announcing the step count. **Both are defaults with a named exception:** announce
a pause when the reader must be prepared for it, or when hitting it unwarned
would be jarring. Nothing here qualifies, since every pause ends a step with an
offer and a visible way to continue.

`0.4.0` — every step gains `## Takeaways`, and the workflow now specifies what the
reader sees rather than leaving it to be improvised.

**From a real run, which is why each of these is here.** The agent headed steps
*Screen 1 —* despite the word appearing nowhere in the material, so the workflow
now gives the exact heading format. It ad-libbed the closing line into something
that read as the model talking to itself, so the four closing blocks are written
out word for word and rendered from `pause`. And it announced the step count up
front, which turns a walkthrough into a chore to get through.

**The steps themselves were the larger gap.** Each argued its case well and left
the reader with nothing scannable — the instruction was in there, in a sentence,
in a paragraph. Every step now closes with the operative points as a list.

Minor: nothing an adopter must fix, and a step that somehow lacked takeaways
still presents.

`0.3.0` — the tutorial types moved to `lumastack/luma-catalog/luma-types` and are vendored back.
They are now `luma/tutorial_step` and `luma/tutorial_quiz`, and every step and the
quiz declare the namespaced names.

**Because they were never token-specific.** They describe a paced walkthrough,
and this bundle happens to be the first one. Left here, the second tutorial would
either link across bundles — which breaks self-containment — or declare its own
`step` under a different name, and both copies would validate cleanly while
meaning subtly different things. That is the failure that is invisible until
somebody has to reconcile them.

**Breaking, and shipped as a minor under the `0.y.z` permission.** Anything
dispatching on the un-namespaced `tutorial_step` must now match
`luma/tutorial_step`. No deprecation cycle, because nothing uses the old names —
they were published hours ago and this bundle has no adopters. Saying that
plainly is the condition on taking the exception; a dead name kept to protect
nobody would be worse.

`0.2.0` — the tutorial's steps became documents. They were assets with no
frontmatter; they are now [[tutorial_step]] and [[tutorial_quiz]], and the
walkthrough reads the same.

**The change worth knowing about is where the pause kind lives.** It was a column
in the workflow's running order and is now a `pause` field on each step. That
removes the copy that could drift, and it puts the answer in the document the
agent is already reading at the moment it needs it — rather than in a table it
has to look back at, one step removed from the thing being described.

**They are steps now, not screens.** The reader is walked through steps; *screen*
survives only as the sizing rule an author writes against, in [[tutorial_step]].
The directory moved with the word, so every Document ID under it changed from
`.../screens/…` to `.../steps/…`. Wikilinks address the slug alone and are
unaffected; anything referring to a full ID is not.

**Minor rather than patch**, because an adopter reading the running order for the
pause kind will no longer find it there, and because those IDs moved. Nothing
they must fix, so not major: re-adopt and it works.

`0.1.0`. **Untested as a walkthrough.** The material is drawn from real session
logs and holds up, but nobody has yet sat through the paced version of it, and
pacing is the thing most likely to be wrong: the steps may be too small, the
pause may come to feel like ceremony, and the *apply* offers on the middle
steps may interrupt more than they help.

**The split between what to do and what not to do is the structural bet.** It
reads well and it duplicates one idea across the halves — choosing a model at the
start and not switching mid-session are the same fact told twice. That is
defensible while the second half is where the surprises live, and it is the first
thing to collapse if the tutorial turns out to run long.
