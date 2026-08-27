---
type: luma/tutorial_step
title: Put cheap models where they cannot cost you anything
step: 5
pause: apply_here
---

# Put cheap models where they cannot cost you anything

A good share of what you ask for is small. Rename these files. Write a release
message. Tidy up this list. Those should run on smaller, cheaper models.

The general rule of thumb is to pick the model that is **the least capable model that will still finish the job**.
Fortunately, there are places you can apply smaller models without touching your current session's cache:

**Subagents.** A subagent's model is set in its own frontmatter, and it runs in
its own context. Point it at a small model and the isolated work gets several
times cheaper while your main session's cache sits untouched.

**Skills and commands.** Same idea. The grunt work runs on the model you
configured for it rather than on whatever your session happens to be using.

That is how to collect the saving without paying the switching cost. Reaching for
`/model` in the middle of a session is how to pay the cost and not collect any
saving.

## Takeaways

- Choosing your model once does not force one tier for everything.
- Use **the least capable model that will finish the job**.
- **Subagents** set their own model in frontmatter and run in their own context — a small model there is free of your cache.
- **Skills and commands** work the same way.
- Collect the saving of using smaller models without paying the switching cost.
