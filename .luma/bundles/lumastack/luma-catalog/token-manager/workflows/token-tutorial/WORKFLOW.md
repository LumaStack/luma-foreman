---
type: workflow
title: Walk me through token usage best practices
description: A paced tutorial on where an agent session's tokens actually go — presented a step at a time, pausing after each one for questions or practice, and ending in a short quiz. Use when somebody wants to learn the material rather than measure a setup.
---

# Walk me through token usage best practices

**A tutorial, not a briefing.** The subject is where an agent session's tokens
actually go and what to do about it. The material is split into steps, each sized
to be read in one go, with a pause after each — because an idea somebody stopped
and applied is one they keep, and a wall of good advice read straight through is
one they agree with and forget.

| | |
| --- | --- |
| **run it** | when somebody wants to understand where their tokens go |
| **ends with** | a quiz, and the session cleared |

Its sibling [[token-audit]] answers the neighbouring question — *what is wrong
with this setup specifically* — and the tutorial sends the reader there early. If
somebody wants numbers about their own machine rather than an explanation, they
want the audit and not this.

**It sends them there in a second session, never in this one**, which is the same
rule as everything else the tutorial tells somebody to go and do. See *sending
somebody away* below before running the first pause.

## Say what this assumes, before step 1

**The steps are written for Claude Code**, and they name its commands
directly — `/rename`, `/clear`, `/context`, `/mcp`, `/usage`, `/cost`, `/rewind`.
Tell the reader that up front, in a line, before you present anything.

**The mechanism underneath is not specific to any harness.** No memory, the whole
conversation resent every turn, a cache that a model switch invalidates, tool
definitions loaded before you type — that is how these tools work, and it will
still be true wherever they are running.

**What will not survive the trip is the operating instructions.** Command names,
the `/mcp` panel, deferral being on by default, the burn-rate indicator, where
session logs are written. On another harness those are somewhere between renamed
and absent.

So if this is not Claude Code, say so plainly rather than presenting the commands
as though they will work: **the reasoning transfers and the keystrokes may not.**
Then run the tutorial anyway — the reader will have to find their own equivalent
of each command, and that is a much smaller gap than not knowing what to look
for.

**Open with this, then go straight into step 1.** On Claude Code, as written; on
anything else, replace the first line with the warning above.

> These steps name Claude Code's commands directly — `/rename`, `/clear`,
> `/context`, `/mcp`, `/usage`, `/cost`, `/rewind` — so they will work as
> written.
>
> This is about where your tokens actually go, and what to do about it. There's a
> short quiz at the end.

**Do not describe the pacing, and do not announce how many steps there are.** No
*one step at a time*, no *I'll pause after each*, no count.

**Saying a pause is coming usually buys the reader nothing.** They find out when
it arrives, and stopping there reads as natural because it is the obvious thing
to do at that point. Described in advance it is just a procedure they have been
enrolled in, and a step count turns the whole thing into a queue to get through.

**Announce one where it earns announcing**, which is the exception rather than
the rule: when the reader has to be mentally prepared for it, or when arriving at
it unwarned would be jarring. A wait long enough that silence would look like
something had broken is the clear case. **Nothing in this tutorial is that** —
every pause here ends a step with an offer and a way to continue, in view.

## The first step is the one they act on immediately

Step 1 teaches `/rename` and has them run it, then and there. **Note the name
they give you** — you will need it if this session has to be recovered later.

**This is the one step where sending them to a second window is exactly
wrong**, and the mistake is easy to make once the `apply_elsewhere` habit sets in.
It is marked `pause: apply_here` and means it: the command has to run *here*,
because the entire purpose is to make *this* session findable again. Renaming a
different one accomplishes nothing.

**Do not advance until they have actually run it** and told you what they called
it. Everything after this leans on it: the tutorial ends by telling them to throw
this conversation away, and the whole reason that is a comfortable thing to do is
that they named it in the first minute.

If they would rather skip it, say what they are giving up — this session becomes
unfindable the moment it is cleared — and then move on. It is their call, not a
gate.

## Read one step at a time

**Read the file for the step you are presenting, and no others.** Not the next
one, not a batch of them, not all of them up front to plan ahead. If you need to
know what a later step covers, the running order below has the titles.

This is not fussiness. A tutorial about the cost of loading things into context
that begins by loading twenty steps into context has refuted itself before the
first pause, and the reader is paying for every one of them on every turn of the
walkthrough.

**Present the step in full.** Do not summarise, condense or paraphrase it, and do
not skip its `## Takeaways`. The steps are already short, so a summary saves the
reader nothing and costs them the wording that was chosen.

**Then stop.** Never advance on your own, however brief the step was.

## How a step is presented

**Never say *screen*.** They are steps. The word does not appear in anything the
reader sees, and it is not what the heading below says.

Head each one exactly like this, with the number and title from its frontmatter:

```
**Step 4 — Clear between jobs**
```

Then the step's body verbatim, `## Takeaways` and all. **Then the closing block
below, and nothing else.** No summary of your own, no observation about what was
interesting, no preview of what is coming. The reader has just read it.

## The closing block, word for word

**Print the block matching the step's `pause` field, changing only the step
number.** These are written out rather than described because an improvised
version is where the tutorial stops sounding like it is talking to the reader and
starts sounding like it is talking to itself.

`apply_here`:

> **Practice this here.** It is safe to do in this window — go ahead, I'll wait.
>
> Ask questions, or say **next** for step 5.

`apply_elsewhere`:

> **Practice this elsewhere.** Don't run it in this window — it would cost or
> clear the session we are in. Open a second window if you want to do it now, and
> I'll be here.
>
> Ask questions, or say **next** for step 5.

`practice`:

> **Nothing to change here** — this one is how the thing works. If you want to go
> and watch it happen in another session, I'll wait.
>
> Ask questions, or say **next** for step 5.

`none`:

> Ask questions, or say **next** when you're ready.

**On the last step, say *for the quiz* instead of a step number.** There is no
step after it, and *next for step 21* points at nothing:

> Ask questions, or say **next** for the quiz.

**Answer questions from the steps already presented** and from what you can see of
their setup. If the answer is a later step, say which one is coming rather than
reading ahead — that is what the running order is for.

**If they take the offer, wait.** Do not fill the silence with the next step.

**Never skip the block because a step seemed obvious, and never print the wrong
one.** Offering to wait while somebody applies a fact they cannot act on is
filler, and it teaches them the pause is ceremony they can ignore. See
[[tutorial_step]] for what each value is claiming.

## Sending somebody away, and getting them back

**A pause that strands the reader has done more damage than skipping the pause
would have.** Much of what this tutorial recommends would wreck this session if it
were done in this session — and the reader cannot possibly know which, because the
step that says *clear between jobs* does not say *except right now*. **Knowing
that is your job, not theirs.**

**Say where they are before they go, every time.** *"You're on step 7, turning
off unused tools — say next when you're back."* A number and a title cost you one
line and turn the trip back into a single word.

**Never do these in this session, however reasonably they are asked for:**

| | what it would do |
| --- | --- |
| `/clear` | destroys the tutorial. It is also the tutorial's closing instruction, so this is a *later*, not a *no* |
| `/compact` | the lesson from step 13, ignored, at the worst possible moment |
| `/model`, effort level, fast mode | rebuilds this session's cache — step 11, exactly |
| running [[token-audit]] | its report would sit in this context and be resent on every remaining step |
| building the output-filter hook | real work with real output, and it belongs in a session that is not this one |

**When they ask for one of these, do not simply decline it.** Say what it would do
to this session, name the step that already covered it, and say where to do it
instead. **The tutorial is far more convincing for refusing to break its own rule
in front of the reader** than it is for stating the rule.

Every step that recommends one of those is marked `pause: apply_elsewhere`: a
second window, this session left untouched, back here with a single *next*.
Nothing is being withheld.

## If it goes wrong anyway

Somebody will clear this session, close the window, or run the audit inside it.

**Recover; do not restart.** Ask which step they had reached and resume from
there — a number, or a half-remembered title matched against the running order, is
enough. **Do not replay steps they have already sat through**, which is the
response that makes people abandon a tutorial for good.

If they renamed the session at the start, `/resume` brings the original back and
nothing at all is lost.

## Running order

**Setup, then the mechanism.** Step 1 is the only thing they do before learning
anything; step 2 is the fact everything else is a consequence of.

| | step | |
| --- | --- | --- |
| 1 | [[01-rename-this-session]] | Name this session before we start |
| 2 | [[02-how-the-cost-compounds]] | How the cost actually compounds |

**What to do.**

| | step | |
| --- | --- | --- |
| 3 | [[03-clear-between-jobs]] | Clear between jobs |
| 4 | [[04-choose-model-and-effort-once]] | Choose your model and effort once, at the start |
| 5 | [[05-cheap-models-where-they-cost-nothing]] | Put cheap models where they cannot cost you anything |
| 6 | [[06-filter-noisy-tool-output]] | Put a filter in front of noisy commands |
| 7 | [[07-turn-off-tools-you-do-not-use]] | Turn off the tools you never use |
| 8 | [[08-delegate-when-the-session-has-far-to-run]] | Delegate when the session still has a long way to run |
| 9 | [[09-match-schedules-to-the-cache-lifetime]] | Check what your scheduled tasks do at three in the morning |
| 10 | [[10-watch-the-meters]] | Watch the meters |

**What not to do.**

| | step | |
| --- | --- | --- |
| 11 | [[11-do-not-switch-model-mid-session]] | Do not switch to a cheaper model to save money |
| 12 | [[12-what-breaks-the-cache-and-what-does-not]] | Do not treat every change as expensive |
| 13 | [[13-do-not-compact-to-save-tokens]] | Do not compact to save tokens |
| 14 | [[14-do-not-shorten-your-prompts]] | Do not write shorter prompts to save money |
| 15 | [[15-do-not-screenshot-text]] | Do not screenshot text |
| 16 | [[16-do-not-feed-raw-pdfs]] | Do not hand over a PDF as it is |
| 17 | [[17-do-not-treat-subagents-as-free]] | Do not assume subagents save tokens |
| 18 | [[18-do-not-blame-background-sessions]] | Do not chase the wrong culprit |

**The close, then the one thing to go and do.** Present 19, take questions, then
20 — which sends them off to measure their own setup, deliberately at the end
where wandering off costs nothing.

| | step | |
| --- | --- | --- |
| 19 | [[19-nobody-else-will-fix-this]] | One honest note to finish on |
| 20 | [[20-audit-your-own-setup]] | Now go and measure your own setup |

## The quiz

Read [[quiz]] once the close is done and they have said they are ready. **Not
before** — it carries every answer, and having it in context while you are still
presenting steps is how a hint leaks. Its `after_step` field says the same
thing in a form a tool can check.

**One question at a time**, through the harness's interactive picker if there is
one, otherwise a numbered list.

**Never show or hint at the answer before they have chosen.**

**Then say whether they got it right, and why.** If they were wrong, give the
right answer with its reasoning, and say what is wrong with the option they
picked — that last part is the one that changes what they do next. The quiz file
carries all of it.

A wrong answer is not a failure state. **Do not re-ask it, do not keep score out
loud, do not soften it into being sort of right.** Say what was wrong, say why,
move on to the next question.

## Ending

The last question asks whether to compact or clear to end the tutorial. **The
answer is clear, and it is also the tutorial's final instruction rather than a
hypothetical.**

Once they have answered it, tell them to do it. They named this session on step
1, so the way back already exists and all that is left is `/clear` — which is
also the pair from that step closing, an hour later, exactly as promised.

**Then stop.** Do not offer to start something else in this session, do not
summarise what was covered, do not compact. Beginning a new job in the session
that just ended a tutorial about clearing between jobs is the whole lesson
discarded in its last minute — and the reader will notice.
