"""Bundles that are broken in ways nothing else notices.

A bundle with a dangling link, an unquoted frontmatter wikilink, or a template
carrying live frontmatter is **still conformant** — the knowledge format
tolerates all three by design, and never rejects. So it publishes cleanly, every
adopter copies it, and the defect travels. That gap between *legal* and *correct*
is the whole reason this rule exists: the format tolerates, and foreman rejects.

**Structural checks only.** Everything here follows from the format and the
bundle model, so it holds for any bundle regardless of whose conventions it
follows. Which directories a bundle uses, how its workflows are named, when it
may call itself `1.0.0` — those are an organization's opinions, they arrive by
adoption rather than by being compiled in, and a tool that hardcoded them would
be deciding standards rather than enforcing them.

The frontmatter parser is deliberately a small subset, and lives in
``foreman.lkf`` because ``get`` reads the same thing.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from ... import lkf
from ..finding import Finding, Notice, Result, Skipped

# The closed vocabularies `matches` draws on. Closed is the point: anything
# outside them is a typo that would otherwise publish silently.
#
# `always` is absent deliberately — it is a value of the field, never a member
# of this list. As a list member it could sit beside a condition it silently
# rendered dead, since OR semantics make everything next to it unreachable.
TRIGGER_KINDS = ("path", "tool", "command", "event", "topic")
# The scalar forms. Anything else in that position is a typo, and it resolves
# to `nothing` — the safe direction, and reported rather than absorbed.
# `eager` is the spec's word as of LKF v0.0.19; `always` is its retired
# spelling, still read until the apply rewrite retires it everywhere at once.
KEYWORDS = ("eager", "always", "nothing")
# `event` reaches what no other trigger can: a lifecycle point, fired however
# it is arrived at. Four of these overlap with `command` on purpose — a command
# trigger catches a literal invocation, an event catches the point itself — and
# under OR semantics that is belt and braces rather than redundancy.
EVENTS = ("session-start", "session-end", "before-commit", "before-push",
          "before-merge", "before-release")

# Reserved names, keyed by their lowercase spelling so a miscased file can be
# recognised and named.
RESERVED_BY_LOWER = {"bundle.md": "BUNDLE.md", "catalog.md": "CATALOG.md",
                     "index.md": "INDEX.md",
                     "log.md": "LOG.md", "project.md": "PROJECT.md"}

# Where a lowercase match is correct rather than a mistake, and the rule is what
# says so: a template is a pattern for making a bundle and a Type Definition
# describes what one is. Neither is the thing its directory is.
EXEMPT_DIRS = ("templates", "_types")

RULE = "bundles"

TRAP = lkf.TRAP
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)]+)\)")

# Illustrative syntax is everywhere in documents that explain syntax — a policy
# describing wikilinks is full of `[[…]]` pointing at nothing on purpose. A
# checker that reports those cries wolf, and a checker that cries wolf gets
# switched off, which protects nothing.
FENCE = re.compile(r"^```.*?^```", re.M | re.S)
INLINE = re.compile(r"`[^`\n]*`")


_split = lkf.split
_keys = lkf.keys


def _prose(text: str) -> str:
    return INLINE.sub("", FENCE.sub("", text))


def _audit(root: Path, repo: Path) -> tuple[list[Finding], list[Notice], list[str]]:
    """Check one bundle. Returns findings, notices, and the paths it looked at."""
    findings: list[Finding] = []
    notices: list[Notice] = []
    label = root.relative_to(repo).as_posix() or "."

    # A vendored bundle is somebody else's, and every remedy below says "fix
    # it" — which is the one thing you must not do to an adopted copy, because
    # the next `get` discards the fix and upstream never hears about the defect.
    # Reporting it is still right: you are the one carrying it.
    vendored = label.startswith(".luma/bundles/")

    def bad(sev: str, summary: str, evidence: list[str], remedy: str) -> None:
        if vendored:
            remedy += (
                "  This is an adopted copy — fix it upstream and take it again, "
                "never here."
            )
        findings.append(
            Finding(
                rule=RULE,
                severity=sev,
                surface="working-tree",
                summary=f"{label}: {summary}",
                evidence=tuple(sorted(evidence)[:10]),
                remedy=remedy,
            )
        )

    docs: dict[str, dict[str, str]] = {}
    assets: list[str] = []
    untyped: list[str] = []
    trapped: list[str] = []
    seen: list[str] = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        seen.append(rel)
        if rel == "INDEX.md":
            # The bundle's generated rendering (LKF v0.0.19, Reserved files).
            # Nothing links to it because everything reaches it the other way
            # around — calling it an orphaned Asset would flag every bundle
            # that ships one.
            continue
        if path.suffix != ".md":
            assets.append(rel)
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        front, _ = _split(text)
        if front is None:
            assets.append(rel)
            continue
        keys = _keys(front)
        if "type" not in keys:
            untyped.append(rel)
            continue
        # A directory whose top-level all-caps Document owns it *is* that
        # Document, so its ID is the directory. `WORKFLOW.md` is a local detail
        # nothing references — entry points and links name the directory.
        stem = rel.rsplit("/", 1)[-1][:-3]
        owns = stem.isupper() and stem != "README" and "/" in rel
        docs[rel.rsplit("/", 1)[0] if owns else rel[:-3]] = keys
        trapped.extend(f"{rel}: {m.group(1)}" for m in TRAP.finditer(front))

    # --- triggers that can never fire ---------------------------------------------
    #
    # A misspelled trigger kind is the worst shape this format produces: it
    # parses, it publishes, every adopter copies it, and the rule it guards
    # never fires. Nothing distinguishes that from a rule whose moment has not
    # come, which is the failure the whole applicability design exists to end.
    unknown_kind: list[str] = []
    unknown_event: list[str] = []
    always_on: list[str] = []
    triggered: set[str] = set()
    kinds: dict[str, str] = {}
    for doc_id, keys in docs.items():
        if doc_id == "BUNDLE":
            continue
        owned = root / doc_id / f"{doc_id.rsplit('/', 1)[-1].upper()}.md"
        path = owned if owned.is_file() else root / f"{doc_id}.md"
        triggers = lkf.matches(path)
        for trigger in triggers:
            kind, _, value = trigger.partition(":")
            if ":" not in trigger:
                if trigger not in KEYWORDS:
                    unknown_kind.append(f"{doc_id}: {trigger}")
                continue
            if kind not in TRIGGER_KINDS:
                unknown_kind.append(f"{doc_id}: {kind}")
            elif kind == "event" and value not in EVENTS:
                unknown_event.append(f"{doc_id}: {value}")
        if triggers == ("always",):
            always_on.append(doc_id)
        if triggers:
            triggered.add(doc_id)
        kinds[doc_id] = str(keys.get("type", "")).strip()

    if unknown_kind:
        bad("high", f"{len(unknown_kind)} trigger(s) name something that is not a trigger",
            unknown_kind,
            "matches takes a closed vocabulary — " + ", ".join(sorted(TRIGGER_KINDS)) +
            ", or the bare word eager or nothing. Anything else parses, "
            "publishes, and never fires, which is indistinguishable from a rule "
            "whose moment has not come.")
    if unknown_event:
        bad("high", f"{len(unknown_event)} event(s) are not events anybody fires",
            unknown_event,
            "event is a closed vocabulary — " + ", ".join(sorted(EVENTS)) +
            ". A name nothing fires is a rule that never arrives.")
    if always_on:
        # Not a defect, and the old remedy said so outright — "worth confirming
        # rather than fixing" is a notice by definition, and it was exiting 1
        # over a choice somebody made deliberately.
        notices.append(
            Notice(
                rule=RULE,
                summary=f"{label}: {len(always_on)} document(s) load whenever this bundle opens",
                evidence=tuple(sorted(always_on)),
                remedy=(
                    "matches: always asks to arrive unasked every time this "
                    "bundle is opened, in every adopter, forever. Confirm it "
                    "was meant: if the rule governs a particular activity, say "
                    "so and it arrives when that activity does."
                ),
            )
        )

    manifest = docs.get("BUNDLE")
    if manifest is None:
        return findings, notices, seen

    if not manifest.get("version"):
        bad("high", "BUNDLE.md declares no version", ["BUNDLE.md"],
            "A Bundle without a version cannot be pinned, compared, or reported as "
            "outdated — a consumer can say nothing honest about it.")

    if untyped:
        bad("high", f"{len(untyped)} file(s) have frontmatter but no type", untyped,
            "Frontmatter plus a type makes a Document; no frontmatter makes an Asset. "
            "Frontmatter without a type is the one shape the format has no name for.")

    if trapped:
        bad("high", f"{len(trapped)} unquoted wikilink(s) in frontmatter", trapped,
            'Quote them: parent: "[[target]]". Unquoted, [[…]] is YAML flow-sequence '
            "syntax and parses as a nested array — no parser complains, and the link "
            "never resolves.")

    # `entry_point` was renamed to `entrypoint`, one word, so that the same word
    # names the same thing at every ring. Both are read during the migration and
    # the old one still fires this check — a reader that only knew the new name
    # would go quiet against every bundle not yet republished, and a check that
    # stops firing is indistinguishable from one that passes.
    entry = manifest.get("entrypoint") or manifest.get("entry_point")
    if entry and entry not in docs:
        bad("high", f"entrypoint points at nothing: {entry}", [f"BUNDLE.md: {entry}"],
            "entrypoint carries a full Document ID — the path within the Bundle, "
            "without the .md suffix.")

    slugs = {k.rsplit("/", 1)[-1] for k in docs}
    broken: list[str] = []
    escaping: list[str] = []
    missing: list[str] = []
    linked: set[str] = set()
    wiki_linked: set[str] = set()

    for rel in sorted(docs):
        path = root / f"{rel}.md"
        try:
            front, body = _split(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        # Frontmatter is scanned for resolution but not for prose links: an
        # unquoted wikilink there is already reported as the trap, and reporting
        # the same defect twice teaches people to skim findings.
        targets = {m.group(1).strip() for m in WIKILINK.finditer(_prose(body))}
        if front:
            for value in _keys(front).values():
                if value.startswith('"') or value.startswith("'"):
                    targets |= {m.group(1).strip() for m in WIKILINK.finditer(value)}
        for target in targets:
            tail = target.rsplit("/", 1)[-1]
            if tail not in slugs:
                broken.append(f"{rel}.md -> [[{target}]]")
            else:
                wiki_linked.add(tail)
        for target in {m.group(1).strip() for m in MDLINK.finditer(_prose(body))}:
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (path.parent / target).resolve()
            try:
                inside = resolved.relative_to(root.resolve()).as_posix()
            except ValueError:
                escaping.append(f"{rel}.md -> {target}")
                continue
            linked.add(inside)
            if not resolved.exists():
                missing.append(f"{rel}.md -> {target}")

    # **Nothing may exist that no transport can reach.** Three routes get a
    # Document to a reader: it declares a trigger, it is named on its bundle's
    # ring, or something reachable links to it. A Document with none is present,
    # conformant, and invisible — and invisible is indistinguishable from
    # absent, which is the one thing this whole design exists to end.
    #
    # **Depth is not the problem and is never reported.** Being reached through
    # three hops is the intended outcome; being reached through none is not.
    #
    # A notice rather than a finding, because a tool cannot tell an orphan from
    # something reached by a route it cannot model — a person typing a path, an
    # agent browsing. The reader decides whether the indirect path is real.
    def _owned(doc_id: str) -> bool:
        """Is this reached through the Document owning its directory?

        A tutorial's steps live under the workflow that runs them and are
        reachable only through it, which is the intended shape rather than a
        defect — twenty-one steps with no trigger apiece is the design working.
        """
        parts = doc_id.split("/")
        return any("/".join(parts[:i]) in docs for i in range(1, len(parts)))

    unreachable = sorted(
        doc_id for doc_id in docs
        if doc_id != "BUNDLE"
        and doc_id != entry
        and doc_id not in triggered
        # A workflow reaches its harness as a skill, and a policy is named on
        # its bundle's ring whatever its class — both are already routed.
        and kinds.get(doc_id) not in ("workflow", "policy")
        # A Type Definition is resolved by the format when writing a Document of
        # its type. It is a contract consulted on demand, never reading material,
        # and nothing should link to it to make it look reachable.
        and not doc_id.startswith("_types/")
        and not _owned(doc_id)
        and doc_id.rsplit("/", 1)[-1] not in wiki_linked
    )
    if unreachable:
        notices.append(
            Notice(
                rule=RULE,
                summary=f"{label}: {len(unreachable)} document(s) nothing can reach",
                evidence=tuple(unreachable),
                remedy=(
                    "No trigger, no line on this bundle's ring, and nothing "
                    "links to it — so it is present and cannot be arrived at. "
                    "Give it a matches, link it from something that is "
                    "reachable, or delete it. Being buried is fine; being "
                    "unreachable is not."
                ),
            )
        )

    if broken:
        bad("medium", f"{len(broken)} wikilink(s) resolve to nothing", broken,
            "A link to a Document nobody has written yet is legal and often correct — "
            "check whether each is a typo or a genuine gap before deleting it.")

    if escaping:
        bad("high", f"{len(escaping)} link(s) point outside the Bundle", escaping,
            "A Bundle must be copyable and still work. A path that escapes breaks the "
            "property the whole distribution model rests on.")

    if missing:
        bad("high", f"{len(missing)} missing attachment(s)", missing,
            "A Document links to an Asset that is not there. This breaks when applied, "
            "not when published.")

    orphans = [a for a in assets if a not in linked]
    if orphans:
        bad("low", f"{len(orphans)} asset(s) nothing links to", orphans,
            "Nothing owns an Asset, so unreferenced files accumulate in silence. "
            "Delete them, or link them from the Document that needs them.")

    return findings, notices, seen


def _manifests(repo: Path) -> list[Path] | None:
    """Bundle manifests git can see. None if git cannot answer.

    A plain filesystem walk finds far too much. A gitignored worktree under
    `.claude/worktrees/` holds a whole second checkout, so every bundle appears
    twice and an agent auditing its own repository is shown findings from
    another agent's uncommitted work. `node_modules` and build output are the
    same shape of problem, arriving from a different direction.

    Asking git rather than the filesystem also keeps this rule honest with the
    other two, which are already git-scoped: what is not tracked or trackable is
    not this repository's to report on.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "--cached", "--others",
             "--exclude-standard", "-z", "--", "*BUNDLE.md", "BUNDLE.md"],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return sorted({repo / rel for rel in out.stdout.split("\0") if rel})


def _miscased(repo: Path) -> list[str]:
    """Reserved names spelled in a case no tool will match.

    `bundle.md` is not a broken `BUNDLE.md` — it is an ordinary Document, and
    every tool ignores it. That is the casing rule working, and exactly why this
    needs saying: **the bundle is simply not there, and nothing else reports an
    absence.** A directory holding only a lowercase manifest is invisible to the
    rest of this rule, which is why the check cannot live inside the per-bundle
    audit — it has to run before anything decides where the bundles are.
    """
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "--cached", "--others",
             "--exclude-standard", "-z", "--", *(f"*{n}" for n in RESERVED_BY_LOWER),
             *RESERVED_BY_LOWER],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0:
        return []
    found = []
    for rel in out.stdout.split("\0"):
        if not rel:
            continue
        name = rel.rsplit("/", 1)[-1]
        if name == RESERVED_BY_LOWER.get(name.lower()):
            continue  # already correct
        if name.lower() not in RESERVED_BY_LOWER:
            continue
        if any(part in EXEMPT_DIRS for part in rel.split("/")[:-1]):
            continue
        found.append(f"{rel} -> {RESERVED_BY_LOWER[name.lower()]}")
    return sorted(found)


def check(repo: Path) -> Result:
    listed = _manifests(repo)
    if listed is None:
        return Result(
            skipped=[Skipped(RULE, "could not list files — not a git repository, or git failed",
                             "Bundles are found by asking git, so that gitignored worktrees and "
                             "dependency directories are not scanned as though they were part of "
                             "this repository.")]
        )
    miscased = _miscased(repo)
    extra = []
    if miscased:
        extra.append(Finding(
            rule=RULE, severity="medium", surface="working-tree",
            summary=f"{len(miscased)} reserved name(s) in the wrong case",
            evidence=tuple(miscased[:10]),
            remedy="ALL CAPS names a file that speaks for the thing containing it, so "
                   "these read as ordinary Documents and every tool skips them. Nothing "
                   "reports the absence, which is the whole reason this is worth saying. "
                   "Rename in two steps on a case-insensitive filesystem, and check "
                   "git ls-files afterwards — git records a case-only rename in neither "
                   "the index nor the working tree reliably, and the two can disagree. "
                   "If the lowercase name was deliberate, nothing is wrong and this is "
                   "only a notice.",
        ))

    manifests = [p for p in listed if p.is_file()]
    if not manifests:
        # A miscased manifest is the likeliest reason there are none: the
        # directory looks like a Bundle to a person and like nothing to a tool.
        if extra:
            return Result(ran=[RULE], findings=list(extra))
        return Result(
            skipped=[Skipped(RULE, "no bundles found — nothing named BUNDLE.md",
                             "Run inside a repository that publishes or vendors Bundles.")]
        )

    result = Result(ran=[RULE], findings=list(extra))
    nested = {m.parent for m in manifests}
    for manifest in manifests:
        root = manifest.parent
        # A Bundle inside a Bundle is not a concept the format has. Auditing the
        # inner one separately is right; auditing it twice is not.
        if any(other != root and other in root.parents for other in nested):
            continue
        findings, notices, _ = _audit(root, repo)
        result.findings.extend(findings)
        result.notices.extend(notices)
    return result
