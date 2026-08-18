# Next steps

This will be a short lived file.

## Rehome catalog and bundle ideas

We need to move ideas related to catalog and how bundles work into their durable places.  They landed here because it was the project that had the most context at the time of inception.  But that context needs a long term home.

And we need to decide how much of it only lives in luma-hq vs repeating some or much of it in luma-catalog and luma-foremand so claude has enough context to work within those proejcts as well.

- First let's decide if this content should live in the catalog and get pulled in or if it lives directly in luma-hq
- In either case, what needs to be repeated in luma-foremand and/or luma-catalog so agents can work in those project with enough context to understand how catalogs, bundles, promotion, and etc function smoothly.
- Should workflows and standards always belong in luma-catalog or is that going to make it difficult to work on luma-foreman and luma-hq because the standards used to develop the tools will exist outside of the tooling unless you install it.  Will that be an elegant solution for maintainers of luma tooling or an ever present headache?  I'm not sure yet without more pondering.
- Will there be any native workflows/skills that live directly in foreman or hq or will they always be fetched via the catalog?  Even for maintainers.

Once we answer these questions then I want to add the following shortly after.

For foreman, create:
- Default release standards and workflow
- Incident creation workflow
- Decision guidelines and workflow
- TDD stategy
- American spelling standardization
- Default README sections
- Default docs to build on
- Logging strategy with scripts? Or is this built-in to foreman?
- Security standards
- Flawless git workstree workflow
- Memory to disk guardrail standard
- Workstyle preferences

For hq, create:
- Design standards (I imagine we'll end up with many different design standards and workflows so keep that in mind when making our first one, it will become one of many)
- Tool evaluation
- Language evaluation
- Branding strategy
- Licensing strategy workflow
- Project organizater
- Architect advisor agent

Eventually:
- CSS standards
- Typescript best practices
- Python best practices
- Timezone best practices
- Public contribution