"""What this project holds, and where each piece came from.

**The inventory existed before any command read it.** `MANIFEST.md` has always
carried the version, source, commit and checksum of every bundle; nothing
printed it. The closest thing was `outdated`, which needs a network and frames
the answer as a version comparison, and the command whose name sounded right —
`adopt --list` — returned the *catalog's* contents instead.

**The readers read committed state and nothing else**, so they work in a bare
clone with no configuration. That is the same guarantee `inspect` carries and
the reason `outdated` lives under this noun rather than inside `list`: asking
whether something *newer* exists is a different question, and it needs the
network.

**`new` is the one that writes, and it needs no network either.** A bundle
needs no catalog to exist — creating one is an act on a directory in a
project, complete in itself — so the command that starts a bundle belongs
under the same noun as the commands that report on one.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from . import adoption, lkf, outdated, project

USAGE = """What this project has taken, and what shape it is in.

  luma-foreman bundle new <name>      start a bundle in this project, under
                                      the reserved local/ namespace
  luma-foreman bundle list            every adopted bundle
  luma-foreman bundle show <name>     one bundle's receipt and contents
  luma-foreman bundle outdated        which have a newer version published
  luma-foreman bundle index <dir>     generate a bundle's INDEX.md (--check to
                                      verify instead) — an authoring act; it
                                      refuses a vendored copy
  luma-foreman bundle set <bundle> <field> <value>
                                      record intent in the manifest — e.g.
                                      set <bundle> register nothing marks it
                                      deliberately landed and not wired
  luma-foreman bundle unset <bundle> <field>
                                      back to the field's default
  luma-foreman bundle migrate-manifest
                                      rewrite the record canonically as
                                      .luma/bundles/MANIFEST.md, retiring a
                                      legacy adopted.toml if one remains

  --to <project>   a project other than this repository

`new` writes a bundle to start from; `list` and `show` read committed state,
and all three work offline. `outdated` reaches each bundle's catalog and does
not.

Exit codes: 0 fine, 1 something is wrong or behind, 2 could not run."""

STATE_NOTE = {
    "edited": "edited here — the next `get` discards it",
    "missing": "recorded but not on disk",
}

# One segment, the shape a directory name and a bundle ID's last part share.
# The namespace is always `local`, so a name carrying a slash is somebody
# addressing a catalog bundle with the command that cannot make one.
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# What a bundle declares on the day it is written, and nothing else.
#
# `published` is in the catalog's own template and deliberately absent here: a
# bundle written in a project has no publish moment, which is the same fact
# that makes its index regenerate rather than freeze. `survival` is absent
# because it defaults to `intended` and a line restating a default says
# nothing. `stage: draft` is present for the opposite reason — omitting it
# declares `unknown`, which reads as nobody having thought about it.
#
# The title is the bundle's ID, because that is what it is: `local/<name>`
# until somebody publishes it under a namespace that means something. The
# generated index renders it as the heading, the same way a vendored bundle's
# heading is its full ID.
#
# `description` is one line and not a folded scalar. The index renders this
# field verbatim as the bundle's announcement, and `foreman.lkf` is a
# deliberately small subset that reads `>-` as the value rather than folding
# what follows — so a template written the YAML way ships every new bundle
# announcing itself as `>-`.
TEMPLATE = """\
---
type: bundle
title: local/{name}
version: 0.1.0
stage: draft
consumers: [project]
description: TODO — what this holds, and who it is for.
---

# local/{name}

TODO — why this exists, in a paragraph. What goes wrong without it.

## What is here

TODO — one line per document on why to open it. Not an inventory: the
directory already lists the files.
"""


def _err(message: str) -> int:
    print(f"luma-foreman bundle: {message}", file=sys.stderr)
    return 2


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman bundle: {summary}", file=sys.stderr)
    print(f"  {remedy}", file=sys.stderr)
    return 1


def _resolve(entries: dict, requested: str):
    """One bundle from a full ID or a bare name, or an error message.

    A bare name is what somebody types when only one namespace is in play.
    Two bundles legitimately sharing a name is exactly when the guess must
    stop: the error says to use the fully qualified form rather than picking
    a side silently.
    """
    entry = entries.get(requested)
    if entry is not None:
        return entry
    named = [e for e in entries.values() if e.name == requested]
    if len(named) > 1:
        names = ", ".join(sorted(m.bundle for m in named))
        return (f"{requested} is ambiguous here — use the fully qualified "
                f"<namespace>/<bundle-name>. Held: {names}")
    if not named:
        known = ", ".join(sorted(entries)) or "nothing is recorded"
        return f"not recorded: {requested} (have: {known})"
    return named[0]


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
        print("nothing adopted — .luma/bundles/MANIFEST.md holds no entries.")
        print()
        print("  luma-foreman get <bundle> --from <catalog>")
        return 0

    rows = {b: (e, adoption.state(project_root, e)) for b, e in entries.items()}
    groups = adoption.by_namespace(list(rows))
    width = max(len(n) for _, names in groups for n in names)
    held = max(len(e.version) for e, _ in rows.values())

    for i, (namespace, names) in enumerate(groups):
        if i:
            print()
        print(namespace)
        for name in names:
            entry, condition = rows[f"{namespace}/{name}" if namespace else name]
            line = f"  {name:<{width}}  {entry.version:<{held}}"
            note = STATE_NOTE.get(condition)
            print(f"{line}  {note}" if note else line.rstrip())

    print()
    wrong = [c for _, c in rows.values() if c != "ok"]
    print(f"{len(rows)} adopted bundle(s)" + (f", {len(wrong)} not as adopted." if wrong else "."))
    if wrong:
        print()
        print("  luma-foreman inspect --rule adoption    what to do about each")
    return 1 if wrong else 0


def show(project_root: Path, requested: str) -> int:
    entries = adoption.read(project_root)
    entry = _resolve(entries, requested)
    if isinstance(entry, str):
        return _err(entry)

    home = adoption.vendored(project_root, entry.bundle)
    condition = adoption.state(project_root, entry)
    manifest = lkf.read(home / "BUNDLE.md") or {}

    print(f"{entry.bundle}  {entry.version}")
    description = manifest.get("description", "")
    if description:
        print(f"  {description}")
    print()
    # One of the two is on the receipt, never both: a registered catalog is
    # recorded by name and the registry owns where that name lives.
    if entry.catalog:
        print(f"  catalog    {entry.catalog}")
    else:
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


def new(project_root: Path, name: str) -> int:
    """Start a bundle in this project, under the reserved ``local/`` namespace.

    **A bundle needs no catalog to exist.** Creating one is an act on a
    directory in a project, complete in itself — a catalog is how bundles are
    distributed once they are worth sharing, never a precondition for one.
    `local/` is where a bundle with no published identity lives (ADR-0011),
    and it is the only namespace this writes into: a name is a bundle's, and
    a namespace is a catalog's to give.

    **It writes one file and refuses to guess the rest.** Which directories a
    bundle needs depends on what it turns out to hold, and an empty `policy/`
    is a question a reader has to answer — as well as a directory git will not
    commit, so one created ahead of its contents exists only on the machine
    that ran this. The output names them instead.
    """
    if not NAME.match(name):
        detail = (
            "A namespace is a catalog's to give, and this only writes "
            f"local/. Name the bundle alone: bundle new {name.rsplit('/', 1)[-1]}"
            if "/" in name else
            "Lowercase letters, digits and single hyphens — it is a "
            "directory name and the last part of the bundle's ID."
        )
        return _refuse(f"not a bundle name: {name}", detail)

    if not adoption.luma_dir(project_root).is_dir():
        return _refuse(
            "no .luma/ here to write a bundle into",
            "A bundle lives in a project. Run `luma-foreman init` first.",
        )

    bundle_id = f"local/{name}"
    home = adoption.vendored(project_root, bundle_id)
    manifest = home / "BUNDLE.md"

    # The one refusal. A BUNDLE.md is what makes a directory a bundle, so
    # overwriting one discards the bundle rather than the file — and every
    # other command here reads it as the truth about what this is.
    if manifest.is_file():
        return _refuse(
            f"{bundle_id} is already a bundle",
            f"{manifest.relative_to(project_root)} exists, and this never "
            f"overwrites one. Edit it, or `luma-foreman bundle new` under a "
            f"different name.",
        )

    # Said out loud, because the two cases fail differently later. Written
    # fresh, the directory holds exactly what the template says. Written onto
    # something already there — a bundle drafted by hand before this command
    # existed — whatever was there is now governed by a manifest nobody wrote
    # to match it, and the version, stage and description are all placeholders
    # describing documents that already exist.
    found = sorted(
        p.relative_to(home).as_posix() + ("/" if p.is_dir() else "")
        for p in home.iterdir()
    ) if home.is_dir() else []

    home.mkdir(parents=True, exist_ok=True)
    manifest.write_text(TEMPLATE.format(name=name), encoding="utf-8")

    where = manifest.relative_to(project_root)
    if found:
        print(f"{bundle_id}: wrote {where} into a directory already there")
        print(f"  it holds: {', '.join(found)}")
        print("  The manifest is a template — its description, version and")
        print("  stage describe nothing yet. Make them true of what is here.")
    else:
        print(f"{bundle_id}: created {where}")
    print()

    steps = [
        (f"edit {where}", "the TODOs — a bundle nobody can describe is not one"),
        (f"{home.relative_to(project_root)}/policy/",
         "what this obliges — create it only when something goes in it"),
        (f"{home.relative_to(project_root)}/procedure/",
         "what it tells an agent to do — same rule"),
        (f"luma-foreman bundle index {home.relative_to(project_root)}",
         "generate INDEX.md, once the documents exist"),
        ("luma-foreman apply", "wire it into the harness"),
    ]
    width = max(len(s) for s, _ in steps)
    print("Next steps:")
    for step, why in steps:
        print(f"  {step:<{width}}  {why}")
    return 0


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

    if verb == "index":
        # An authoring act on a directory, not a read of this project's
        # state — so it takes a path, resolves no project, and lives in its
        # own module.
        from . import bundle_index

        return bundle_index.main(operands)
    if verb == "outdated":
        # The same command, reached under the noun it belongs to. Its own
        # options keep working, so `--json` and `--to` behave as documented.
        forwarded = list(operands)
        if target:
            forwarded += ["--to", str(target)]
        return outdated.main(forwarded)

    project_root, _ = project.resolve(target or Path.cwd())

    if verb in ("set", "unset"):
        # Named for what they do — they record intent in the manifest and
        # perform nothing: `apply` is what writes it out, and the writer must
        # never author its own inputs. `set` writes a field's line, `unset`
        # removes it, and absence is the default — the same shape as the
        # file's own divergence-only grammar.
        want = 3 if verb == "set" else 2
        if len(operands) != want:
            return _err(f"usage: luma-foreman bundle set <bundle> <field> <value>"
                        if verb == "set" else
                        "usage: luma-foreman bundle unset <bundle> <field>")
        requested, field = operands[0], operands[1]
        value = operands[2] if verb == "set" else ""
        if field != "register":
            return _err(f"'{field}' is not a field this build knows (have: register)")
        if verb == "set" and value != "nothing":
            return _err(f"register takes 'nothing' — absence already means wired "
                        f"everywhere, which is what `unset` restores")
        entries = adoption.read(project_root)
        entry = _resolve(entries, requested)
        if isinstance(entry, str):
            return _err(entry)
        if entry.register == value:
            state = f"register: {value}" if value else "the default — wired everywhere"
            print(f"{entry.bundle} already at {state}; nothing to do.")
            return 0
        from dataclasses import replace
        entries[entry.bundle] = replace(entry, register=value)
        adoption.write(project_root, entries)
        said = f"register: {value}" if value else "the default — wired everywhere"
        print(f"{entry.bundle} -> {said}")
        print()
        print("  luma-foreman apply    make it so")
        return 0
    if verb == "migrate-manifest":
        if operands:
            return _err(f"migrate-manifest takes no arguments (got: {operands[0]})")
        entries = adoption.read(project_root)
        legacy = adoption.legacy_path(project_root)
        if not entries and not legacy.is_file():
            print("nothing recorded — no manifest and no legacy file to migrate.")
            return 0
        had_legacy = legacy.is_file()
        adoption.write(project_root, entries)
        target = adoption.manifest_path(project_root).relative_to(project_root)
        print(f"wrote {target} ({len(entries)} entr{'y' if len(entries) == 1 else 'ies'})"
              + (", retired adopted.toml" if had_legacy else ""))
        return 0
    if verb == "new":
        if len(operands) != 1:
            return _err("usage: luma-foreman bundle new <name>")
        return new(project_root, operands[0])
    if verb == "list":
        if operands:
            return _err(f"list takes no arguments (got: {operands[0]})")
        return listing(project_root)
    if verb == "show":
        if len(operands) != 1:
            return _err("usage: luma-foreman bundle show <name>")
        return show(project_root, operands[0])
    return _err(f"unknown: bundle {verb} (try luma-foreman bundle --help)")
