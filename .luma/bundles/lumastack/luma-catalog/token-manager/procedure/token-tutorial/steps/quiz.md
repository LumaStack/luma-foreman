---
type: luma/tutorial_quiz
title: Quiz
after_step: 20
---

# Quiz

Ask these one at a time, in order. Present each question with its options through
the interactive picker if the harness has one; a numbered list is a fine fallback.

**Never show the answer, or hint at it, before they have chosen.**

**After every answer, say whether they got it right and why.** If they got it
wrong, give the right answer, say why it is right, and say what is wrong with the
one they picked — that last part is where the learning is. Everything you need is
below the question.

A wrong answer is not a failure state. Do not re-ask it, do not keep a running
score out loud, do not make it a big deal. Say what was wrong, why, and move on.

---

## 1. You are thirty turns into a forty-turn session and your agent reads a 4,000-token file. What does that read cost you?

- **A.** 4,000 tokens, once.
- **B.** Nothing — it goes straight into the cache.
- **C.** 4,000 tokens, and then again on every remaining turn.
- **D.** It depends which model you are on.

**Correct: C.**

The model has no memory, so the whole conversation — that file included — is
resent from the top on every subsequent turn. After the first turn you are paying
the cheaper cache-read rate for it rather than the full rate, but you are paying
for it every single turn until you clear. The number that matters is size
multiplied by turns remaining.

- **A** is the intuition this whole tutorial exists to break. A one-off charge is
  how it would work if the model remembered what it had already been told.
- **B** confuses cheaper with free. Caching reduces the rate on a re-send; it
  never stops the re-send. Nothing in your context is ever not sent again.
- **D** is a real effect on the wrong axis. The model changes the price per
  token. It does not change whether the token is resent.

---

## 2. You are mid-session, and you switch from Opus to Sonnet to make the rest of the session cheaper. What happens?

- **A.** The rest of the session gets cheaper.
- **B.** Your cache is invalidated and the whole conversation is reprocessed at full price. It was cheaper to `/clear`.
- **C.** Nothing, until your next message.
- **D.** Your context is summarised down to fit the smaller model.

**Correct: B.**

The model is part of the cache key. Change it and none of your existing history
matches any more, so the entire conversation is re-read at the full rate instead
of the cache-read rate. On a large context that is roughly a tenfold charge on
that one turn, paid immediately, against a saving that would only have arrived
gradually. If you really want the cheaper model, `/clear` and start again on it.

- **A** is true per token and false in total. The per-token rate does drop — but
  the one-off charge for rebuilding the cache usually swamps whatever was left to
  save.
- **C** is nearly right and lands on the wrong conclusion. The invalidation does
  happen on the next message, and that next message is precisely the expensive
  one.
- **D** describes compaction, which is a different thing you also should not do
  for cost reasons. Switching model summarises nothing.

---

## 3. Which of these can you do mid-session without rebuilding your cache?

- **A.** Turning on fast mode.
- **B.** Raising your effort level.
- **C.** Editing your memory file.
- **D.** Disconnecting an MCP server, on a setup where tools load up front.

**Correct: C.**

Editing a file — including your memory file — is ordinary work appended to the
conversation. It does not touch the cache key, so nothing gets rebuilt.

- **A** and **B** are both part of the cache key, exactly like the model. Fast
  mode and effort level look like preferences and behave like a model switch.
- **D** depends entirely on deferral, and the question specified the bad case.
  Where tools are deferred, connecting and disconnecting just appends and is
  safe. Where they load up front they sit in the cached prefix, so changing the
  set rebuilds it — which is why the tools line in `/context` is worth checking.

---

## 4. When is delegating to a subagent actually worth it?

- **A.** Always — a subagent runs in its own context, so it is free.
- **B.** When you are near the end of a session and want to finish cheaply.
- **C.** Whenever the subagent runs a cheaper model than your main session.
- **D.** When the output/input is high volume, you will not need the detail again, and the session has many turns left.

**Correct: D.**

A subagent spends real tokens — its own system prompt, its own copy of your
memory file, its own tools, and then the reading. In isolation it often spends
more than it saved. What makes it pay is that the tokens it kept out of your
context would otherwise have been resent on every remaining turn, so the return
scales with how much session is left. All of them have to hold together.

- **A** is the myth. Delegation moves tokens rather than saving them, and end to
  end it can be a net loss.
- **B** is the specific way to lose. You pay the whole setup cost and then end the
  session before any of the return accrues.
- **C** is a good idea attached to the wrong question. A cheap model makes the
  delegated work cheaper; it does not make delegating the right call.

---

## 5. You are finished here. To end this tutorial, should you compact or clear?

- **A.** Clear — and rename first, if you might want to come back to it.
- **B.** Compact, so a summary of what you learned carries into the next job.
- **C.** Neither — just close the terminal.

**Correct: A.**

Clearing is free, and it resets the base that every other saving in this tutorial
is a fraction of. This session is done, and nothing in it needs resending on every
turn of whatever you do next. `/rename` first costs nothing and leaves `/resume` a
way back if you want one.

- **B** is the trap the tutorial spent a step on, and picking it here is the
  most understandable wrong answer available. Compacting sends your entire
  conversation again so a summary can be written, then discards the cache on
  purpose. It buys continuity — which you do not need, because the tutorial is
  over — and never savings.
- **C** ends nothing that was costing you. The session sits there with all of its
  history intact, ready to be resumed. Closing a window is not clearing, and it is
  not the habit worth building.
