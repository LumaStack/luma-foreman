"""What this project holds, and where each piece came from.

**The inventory existed before any command read it.** `adopted.toml` has always
carried the version, source, commit and checksum of every bundle; nothing
printed it. The closest thing was `outdated`, which needs a network and frames
the answer as a version comparison, and the command whose name sounded right —
`adopt --list` — returned the *catalog's* contents instead.

**These read committed state and nothing else**, so they work in a bare clone
with no configuration. That is the same guarantee `inspect` carries and the
reason `outdated` lives under this noun rather than inside `list`: asking
whether something *newer* exists is a different question, and it needs the
network.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import adoption, lkf, outdated, project

USAGE = """What this project has taken, and what shape it is in.

  luma-foreman bundle list            every adopted bundle
  luma-foreman bundle show <name>     one bundle's receipt and contents
  luma-foreman bundle outdated        which have a newer version published

  --to <project>   a project other than this repository

`list` and `show` read committed state and work offline. `outdated` reaches
each bundle's catalog and does not.

Exit codes: 0 fine, 1 something is wrong or behind, 2 could not run."""

STATE_NOTE = {
    "edited": "edited here — the next `get` discards it",
    "missing": "recorded but not on disk",
}


def _err(message: str) -> int:
    print(f"luma-foreman bundle: {message}", file=sys.stderr)
    return 2


def _documents(home: Path) -> list[str]:
    """Every Document in a vendored copy, by path relative to the bundle.

    `BUNDLE.md` is the bundle talking about itself rather than a Document, and
    templates are not intended to be read as rules — both would pad the list
    with things nobody can act on.
    """
    if not home.is_dir():
        return []
    out = []
    for path in sorted(home.rglob("*.md")):
        rel = path.relative_to(home).as_posix()
        if rel == "BUNDLE.md" or rel.startswith("templates/"):
            continue
        out.append(rel.removesuffix(".md"))
    return out


def listing(project_root: Path) -> int:
    entries = adoption.read(project_root)
    if not entries:
        print("nothing adopted — .luma/bundles/adopted.toml holds no entries.")
        print()
        print("  luma-foreman get <bundle> --from <catalog>")
        return 0

    rows = [(b, e, adoption.state(project_root, e)) for b, e in sorted(entries.items())]
    width = max(len(b) for b, _, _ in rows)
    held = max(len(e.version) for _, e, _ in rows)
    for bundle_id, entry, condition in rows:
        line = f"  {bundle_id:<{width}}  {entry.version:<{held}}"
        note = STATE_NOTE.get(condition)
        print(f"{line}  {note}" if note else line.rstrip())

    print()
    wrong = [c for _, _, c in rows if c != "ok"]
    print(f"{len(rows)} adopted bundle(s)" + (f", {len(wrong)} not as adopted." if wrong else "."))
    if wrong:
        print()
        print("  luma-foreman inspect --rule adoption    what to do about each")
    return 1 if wrong else 0


def show(project_root: Path, requested: str) -> int:
    entries = adoption.read(project_root)
    entry = entries.get(requested)
    if entry is None:
        # A bare name is what somebody types when only one namespace is in play.
        matches = [e for b, e in entries.items() if e.name == requested]
        if len(matches) > 1:
            names = ", ".join(sorted(m.bundle for m in matches))
            return _err(f"{requested} is ambiguous here: {names}")
        if not matches:
            known = ", ".join(sorted(entries)) or "nothing is adopted"
            return _err(f"not adopted: {requested} (have: {known})")
        entry = matches[0]

    home = adoption.vendored(project_root, entry.bundle)
    condition = adoption.state(project_root, entry)
    manifest = lkf.read(home / "BUNDLE.md") or {}

    print(f"{entry.bundle}  {entry.version}")
    description = manifest.get("description", "")
    if description:
        print(f"  {description}")
    print()
    print(f"  source     {entry.source}")
    print(f"  commit     {entry.commit}")
    print(f"  vendored   {home.relative_to(project_root)}")
    print(f"  copy       {condition}" + (f" — {STATE_NOTE[condition]}" if condition in STATE_NOTE else ""))

    documents = _documents(home)
    if documents:
        print()
        print(f"  documents  {len(documents)}")
        for name in documents:
            print(f"    {name}")

    # Deliberately not shown: what each Document derives to, and whether the
    # generated output is current. That is `apply --explain`, and a second
    # implementation of it here would be a second thing to keep true.
    return 0 if condition == "ok" else 1


def main(argv: list[str]) -> int:
    target: Path | None = None
    args: list[str] = []
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--to":
            if not rest:
                return _err("--to needs a directory")
            target = Path(rest.pop(0))
        else:
            args.append(arg)

    if target and not target.is_dir():
        return _err(f"not a directory: {target}")

    verb = args[0] if args else "list"
    operands = args[1:]

    if verb == "outdated":
        # The same command, reached under the noun it belongs to. Its own
        # options keep working, so `--json` and `--to` behave as documented.
        forwarded = list(operands)
        if target:
            forwarded += ["--to", str(target)]
        return outdated.main(forwarded)

    project_root, _ = project.resolve(target or Path.cwd())

    if verb == "list":
        if operands:
            return _err(f"list takes no arguments (got: {operands[0]})")
        return listing(project_root)
    if verb == "show":
        if len(operands) != 1:
            return _err("usage: luma-foreman bundle show <name>")
        return show(project_root, operands[0])
    return _err(f"unknown: bundle {verb} (try luma-foreman bundle --help)")
