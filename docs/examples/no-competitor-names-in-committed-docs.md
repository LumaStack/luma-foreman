---
name: no-competitor-names-in-committed-docs
description: Committed luma-backlog output must never name other projects/competitors; positioning goes in as unattributed prior art
metadata:
  type: project
---

No file committed to `luma-backlog` may mention another project by name — not in docs, comments, commit messages, or the README. This includes competing or adjacent tools discovered during research.

**Why:** Stated as a standing rule for the project's final output (2026-08-04). Naming competitors in a specification repository dates the docs, invites comparison-shopping by readers, and reads as defensive positioning rather than a confident statement of what the project is.

**How to apply:** Research prior art freely and discuss it by name in conversation — the constraint is on committed output only. When a competitive insight needs to survive into the docs, write it as an unattributed design position ("the substrate is an auditable record, not a task list") rather than a contrast ("unlike X, we ..."). See [[design-first-working-mode]].

**Carve-out (2026-08-09, revised 2026-08-20):** the rule does not apply in an organization's internal headquarters. Holding competitive analysis is part of what that repository is for, and its audience is the organization rather than the public.

**The exemption ends at promotion.** An insight travelling outward — into a bundle, into a catalog, into anything published — is rewritten as an unattributed design position first, and the copy to inspect is the promoted one. *This carve-out previously named one specific repository as the exempt one, and that repository has since been published — which is exactly why an exemption has to rest on a stated property rather than on a name.*
