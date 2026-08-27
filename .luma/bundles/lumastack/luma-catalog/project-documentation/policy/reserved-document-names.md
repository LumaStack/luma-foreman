---
type: policy
title: Reserved document names
description: Which filenames are claimed by an outside convention or matched by a tool, where the capitals are load-bearing and where they are only typography, and the one distinction no convention gives you.
matches:
  - topic: naming a new file at a repository root
---

# Reserved document names

**Some filenames are not yours to choose.** A tool matches them, or a reader
arrives expecting them, and getting the name wrong fails silently — nothing
reports a `CONTRIBUTING.md` that GitHub did not pick up.

**The capitals are the part people copy without knowing why.** They are
load-bearing in one place and decoration everywhere else, and it is worth
knowing which is which before inventing a name.

## Where the convention actually comes from

There is **no single standard**. There are several sources of different weight,
and they do not agree with each other.

| source | what it claims | how binding |
| --- | --- | --- |
| **GNU Coding Standards** | `README`, `INSTALL`, `NEWS`, `ChangeLog`, `AUTHORS`, `COPYING` | convention. It prescribes *which files a distribution carries*, not their case |
| **`LICENSE`** | the licence text, at the repository root | **matched by a tool, and the highest-stakes one.** GitHub detects it to populate the repository's licence field and badge |
| **GitHub community health files** | `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `GOVERNANCE.md`, `FUNDING.yml`, issue and pull request templates | **matched by a tool.** Recognised in the repository root, `.github/`, or `docs/` |
| **Keep a Changelog** | `CHANGELOG.md` | a specification, and the reason this one is consistently capitalised where GNU's is not |
| **`AGENTS.md`** | `AGENTS.md` at the repository root | **explicitly not a specification** — its own site calls it *"an open format"*. Read by twenty-plus agents by convention alone |

**`ChangeLog` is CamelCase in the GNU list**, which quietly demolishes the idea
that all-caps is *the* convention. Whatever the industry is following, it is not
one rule.

**The licence is where two of these sources disagree outright, so take a
position: use `LICENSE`.**

GNU says `COPYING`; GitHub looks for `LICENSE`. Both are correct within their
own tradition and **only one of them gets detected** — a repository named the
GNU way silently presents as having no licence at all, which is the most
consequential failure on this page and the least visible.

`LICENSE`, `LICENSE.md` and `LICENSE.txt` are all detected. **Extensionless is
the default here**: it reads as a legal text rather than as documentation, and
it keeps the file out of anything that globs `*.md`.

**GitHub does not document whether its matching is case-sensitive.** Every
example is capitalised and the behaviour is unstated, so match the documented
spelling exactly rather than relying on tolerance nobody promised.

## Why they are capitalised at all

**ASCII sort order, in the 1970s.** Uppercase occupies 65–90 and lowercase
97–122, so in a byte-ordered listing `README` floated above `src/`. Modern
listings usually collate case-insensitively and the mechanism has faded — **the
signal outlived it.**

What it came to mean is *root level, read me first, you are arriving cold*. That
is the whole of it. **It says nothing about who wrote the file**, which is the
assumption most often made about `CLAUDE.md` and `AGENTS.md`: both are
capitalised because they are entry points addressed to a reader with no context,
not because an agent produced them.

## The rule

**Capitals are load-bearing only where a tool matches the name.** There, spell it
exactly as its source documents it, because the failure is silent.

**Everywhere else the rule is: an entry point shouts, a record does not.**

| | |
| --- | --- |
| **`SHOUTING.md`** | the front door of a directory — `README.md`, `SPEC.md`, `DECISIONS.md` |
| **`lowercase.md`** | anything carrying a `type:` — `BUNDLE.md`, `PROJECT.md`, a policy, a workflow, a record |

**A record is not a front door.** It has a contract, a lifecycle, and something
that reads it by path; the capitals would be claiming an attention it does not
want.

**And a directory where everything shouts is a directory where nothing does.**
The cost of extending the convention past entry points is that it stops
distinguishing anything.

## What no convention gives you, and you will want

**Nothing in a filename says whether a document is authored or generated.**
`README.md` is somebody's writing and `CLAUDE.md` is regenerable output, and
they are indistinguishable — same case, same extension, same directory.

That gap is why generated files carry a marker *inside* them instead. If a file
is written by a tool, it says so in its first lines, and where it shares a file
with hand-written content it owns a delimited region rather than the whole
thing. **The filename cannot carry it, so the content must.**
