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
``foreman.lkf`` because ``adopt`` reads the same thing.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from ... import lkf
from ..finding import Finding, Result, Skipped

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


def _audit(root: Path, repo: Path) -> tuple[list[Finding], list[str]]:
    """Check one bundle. Returns findings and the paths it looked at."""
    findings: list[Finding] = []
    label = root.relative_to(repo).as_posix() or "."

    # A vendored bundle is somebody else's, and every remedy below says "fix
    # it" — which is the one thing you must not do to an adopted copy, because
    # the next adopt discards the fix and upstream never hears about the defect.
    # Reporting it is still right: you are the one carrying it.
    vendored = label.startswith(".luma/bundles/")

    def bad(sev: str, summary: str, evidence: list[str], remedy: str) -> None:
        if vendored:
            remedy += (
                "  This is an adopted copy — fix it upstream and re-adopt, "
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
        docs[rel[:-3]] = keys
        trapped.extend(f"{rel}: {m.group(1)}" for m in TRAP.finditer(front))

    manifest = docs.get("bundle")
    if manifest is None:
        return findings, seen

    if not manifest.get("version"):
        bad("high", "bundle.md declares no version", ["bundle.md"],
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

    entry = manifest.get("entry_point")
    if entry and entry not in docs:
        bad("high", f"entry_point points at nothing: {entry}", [f"bundle.md: {entry}"],
            "entry_point carries a full Document ID — the path within the Bundle, "
            "without the .md suffix.")

    slugs = {k.rsplit("/", 1)[-1] for k in docs}
    broken: list[str] = []
    escaping: list[str] = []
    missing: list[str] = []
    linked: set[str] = set()

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
            if target.rsplit("/", 1)[-1] not in slugs:
                broken.append(f"{rel}.md -> [[{target}]]")
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

    return findings, seen


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
             "--exclude-standard", "-z", "--", "*bundle.md", "bundle.md"],
            capture_output=True, text=True, timeout=120,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return sorted({repo / rel for rel in out.stdout.split("\0") if rel})


def check(repo: Path) -> Result:
    listed = _manifests(repo)
    if listed is None:
        return Result(
            skipped=[Skipped(RULE, "could not list files — not a git repository, or git failed",
                             "Bundles are found by asking git, so that gitignored worktrees and "
                             "dependency directories are not scanned as though they were part of "
                             "this repository.")]
        )
    manifests = [p for p in listed if p.is_file()]
    if not manifests:
        return Result(
            skipped=[Skipped(RULE, "no bundles found — nothing named bundle.md",
                             "Run inside a repository that publishes or vendors Bundles.")]
        )

    result = Result(ran=[RULE])
    nested = {m.parent for m in manifests}
    for manifest in manifests:
        root = manifest.parent
        # A Bundle inside a Bundle is not a concept the format has. Auditing the
        # inner one separately is right; auditing it twice is not.
        if any(other != root and other in root.parents for other in nested):
            continue
        findings, _ = _audit(root, repo)
        result.findings.extend(findings)
    return result
