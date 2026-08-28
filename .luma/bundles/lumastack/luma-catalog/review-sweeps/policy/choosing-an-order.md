---
type: policy
title: Choosing an order
description: The orders a sweep can run in, what each buys and costs, and why the choice is made once per sweep and written down rather than defaulted to.
matches:
  - topic: deciding what to review first
---

# Choosing an order

**Decided once, at the start, and recorded in `sweep.md` with the reason.**

Not because one order is right — none is — but because an unrecorded order is
not an order. It becomes *whatever seemed next*, which drifts toward the files
that are pleasant to read and leaves the sweep's coverage looking complete
while its attention was not.

## The orders

| order | buys | costs | good for |
| --- | --- | --- | --- |
| **narrative** — entrypoints, then down the call graph | a model that compounds; each file arrives with its callers already read | slow to reach the risky parts; leaves unreachable files stranded for a final pass | *I want to know this system* |
| **risk-weighted** — churn × size, most-changed first | defects early, while attention is fresh | you meet the hardest code while your model of the system is weakest | *this thing keeps breaking* |
| **dependency** — leaves first, upward | nothing is read before what it depends on | utilities read with no idea what uses them, which is the stranger problem in its purest form | correctness work, small codebases |
| **directory** — top to bottom, alphabetical | zero decisions, obviously complete, trivially resumable | adjacency means nothing; two files beside each other may share no ideas | prose, config, anything without a call graph |
| **led** — the reader picks the next cluster each slice | attention goes where the interest is, which is the resource that actually runs out | coverage goes uneven, and the dull corners are never what anybody picks | *I know this codebase and I want to steer* |

**Narrative is the usual answer for a first sweep**, because a first sweep is
almost always somebody wanting to know their own system, and it is the only
order in which understanding accumulates rather than resets.

**Led order is a real order, not the absence of one.** Steering deliberately —
*today I want to look at the transport layer* — is a choice made per slice
rather than up front, and it is the right one when the reader knows the system
well enough that their instinct about what to read next is better information
than any rule you could write down at the start.

**Directory order is underrated and not a failure of nerve.** For a
documentation tree, a config directory, or a package of independent leaf
modules, there is no structure for a cleverer order to follow, and inventing
one costs a decision per slice to buy nothing.

## Risk-weighted is often the wrong tool wearing the right name

**If you already know what you are looking for, you want an audit rather than a
sweep.** A sweep covers everything and takes weeks; a targeted audit answers
the question this week and produces findings somebody else can answer. Ordering
a sweep by risk is a way of getting an audit slowly.

*The `audit-records` bundle covers that shape.* Choose risk-weighted when you
genuinely want full coverage **and** want the frightening parts read while you
are still fresh — which is a real preference, just a rarer one than it sounds.

## The order changes the sequence, never the set

**Every file in scope is covered whatever order you chose.** An order that
quietly drops files is a scope decision pretending to be an ordering one, and
scope belongs in `sweep.md` under what was excluded, where a reader can see it.

**Narrative order needs a final pass** for everything no entrypoint reaches —
utilities, generated files, dead code. That pass is where dead code is found,
which is a large part of why the order is worth using.

## Led order, and what keeps it honest

**The index is the whole discipline.** Picking what to read next is fine;
picking it while unable to see what is left is how a sweep becomes a tour of
the interesting parts with a completion bar attached.

So a led sweep does one extra thing at every slice: **look at what is still
pending before choosing.** Not to be shamed into the dull corners — to make the
choice with the cost visible, which is the only difference between steering and
avoiding.

**Expect the last fifth to be joyless**, and decide about it deliberately
rather than by attrition. Everything nobody wanted to pick is still there, all
at once, and that is the moment a led sweep either finishes or quietly stops.
Both are allowed; being surprised by it is what is not.

### Led inside another order

**The common real shape**, and legitimate: *narrative, but I will jump when
something catches me*. Record it that way — `led, over a narrative backbone` —
so the sweep says what it is doing.

The backbone is what you return to. Without one, jumping is the whole method
and the sweep should say `led` plainly instead of claiming a structure it
abandons every slice.

## Changing order mid-sweep

**Allowed, and worth doing when the first choice is clearly not working.**
Write it in the sweep as a dated line: what it was, what it is now, why.

**What is not allowed is changing it silently**, one convenient slice at a
time. That is how an order becomes *whatever seemed next* without anybody
deciding to abandon it — and the sweep loses the only record of why its
coverage looks the way it does.

**Declared steering is not this.** A sweep recorded as `led` and then led is
doing exactly what it said; the failure is a sweep recorded as `narrative` that
is being led in practice. **The defect is the mismatch, not the steering** —
and the fix is usually to change the recorded order to `led` rather than to go
back to obeying the old one.

## Grouping by concern is not an order

*Read all the error handling, then all the configuration* is a legitimate
review, and it is not a sweep: it covers aspects rather than files, so nothing
can be marked off and the index never retires anything.

**Run it as its own thing if it is what you want.** Do not run it inside a
sweep and expect coverage to mean anything afterwards.
