# examples/

Parked material. Nothing here is ratified, and nothing here is loaded or enforced by anything yet.

These are working rules that accumulated as machine-local agent memory while building `luma-backlog`. They were captured on one machine, keyed to one directory, and would have been lost with it — so they are parked here to make them durable while the repository is still too young to have a real home for them.

## What has to be settled before these move out of `examples/`

- **Where they belong.** Some are organization-level facts about how work is done and arguably belong in `luma-leader`; some are repository-level rules that `luma-foreman` should install and check. They are not currently separated.
- **How they get loaded.** A committed file is durable but inert. Machine-local memory was live but fragile. Neither is the answer on its own, and the trade is the actual open question.
- **What scope each one has.** "Applies to every repository" and "applies to `luma-backlog` only" are both present below, and the distinction is currently written in prose rather than expressed in a way anything can act on.

## Contents

- `design-first-working-mode.md` — specification settles before implementation starts.
- `no-competitor-names-in-committed-docs.md` — committed output never names another project. Repository-scoped, with a recorded carve-out.
- `american-spelling.md` — American spelling across all committed text.

Original frontmatter is preserved as captured, including the metadata of the memory system they came from.
