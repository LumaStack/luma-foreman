# Inspect

```bash
luma-foreman inspect                # 0 nothing found, 1 findings, 2 could not run
luma-foreman inspect --json         # for continuous integration
luma-foreman inspect --rule adoption
```

Checks a repository against the baseline and reports where it falls short.
**Every check works in a bare clone with no configuration.**

## What each rule catches

| rule | catches |
| --- | --- |
| **identity** | personal information published through git — machine-derived author identities, malformed addresses, home directory paths in tracked content |
| **secrets** | provider-issued credentials in tracked content, and files that normally hold them |
| **bundles** | bundles broken in ways nothing else notices — a dangling link, an unquoted wikilink in frontmatter, a template carrying live frontmatter |
| **vocabulary** | words this project retired, still in use |
| **adoption** | an adopted bundle that is no longer what was adopted — edited in place, missing from disk, or adopted and never written anywhere an agent reads |

**`secrets` findings never contain the secret itself**, because findings end up
in continuous integration logs.

**All three bundle defects are conformant**, which is why they need a checker:
the bundle publishes cleanly and the defect travels to everyone who adopts it.

**The last adoption case reads green from every angle** — the bundle is present,
the checksum matches, nothing is edited — while the project quietly carries
rules no agent has ever seen.

## A notice is the third outcome

Something worth a reader's judgement that is **not** a defect. It prints as
loudly as a finding and **never changes the exit code**.

**`vocabulary` emits only notices**, and the reason generalises. A grep cannot
tell a revival from an ordinary use of the same word, so it hands over the term,
what replaced it, where that was decided, and the line — and the reader judges.
Nothing is retired by default.

**A heuristic wired to a merge gate is a heuristic somebody switches off.** That
is the whole argument for the third outcome: a check that cannot be certain
still earns a voice, as long as it cannot block.

## A check that cannot run is reported as skipped

Never as passed. **An inspection that reads clean while silently skipping half
its checks is worse than no inspection**, because it manufactures confidence
nobody earned.
