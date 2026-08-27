---
type: luma/tutorial_step
title: Do not compact to save tokens
step: 13
pause: practice
---

# Do not compact to save tokens

This one is exactly backwards, and people recommend it to each other constantly.

**To write you a summary, the model has to be sent your entire conversation one
more time.** So the message you sent in order to save money is the single most
expensive message of the session. And then it discards your cache on purpose,
because the conversation it was caching no longer exists.

**Compaction buys continuity, not savings.** Continuity is a perfectly good thing
to want — you are mid-task, you are running out of room, and you need to keep
going. Pay for it knowingly and for that reason. Never as a cost-control measure.

Clearing is the free one.

And if what you actually want is to undo a few bad turns, `/rewind` takes you
back to a point the cache already knows, so nothing has to be re-read.

## Takeaways

- Compacting sends your **entire conversation one more time** so a summary can be written.
- It is the single most expensive message of a session, and it then discards your cache on purpose.
- **It buys continuity, never savings.** Pay for it knowingly, mid-task, for that reason alone.
- Clearing is the free one and usually the better choice.
- Undoing a few bad turns? **`/rewind`** returns to a point the cache already knows.
