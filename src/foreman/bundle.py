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

  luma-foreman bundle list            every bundle this project carries
  luma-foreman bundle show <name>     one bundle's receipt and contents
  luma-foreman bundle outdated        which have a newer version published

  luma-foreman bundle new <name>      start a bundle in this project, under
                                      the reserved local/ namespace
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

The reads come first, and the writes below them. `list` and `show` read
committed state and `new` writes one bundle, so all three work offline;
`outdated` reaches each bundle's catalog and does not.

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


# Lives in `adoption` since `remove` needs the same answer, and two commands
# resolving a name differently is the failure that would be hardest to see.
_resolve = adoption.resolve


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
        # Not "nothing adopted": a bundle written here was never adopted, and
        # this listing now shows those too. The manifest is a receipt of what
        # is aboard, however it got there — which is the whole reason it is
        # not still called `adopted.toml`.
        print("no bundles — .luma/bundles/MANIFEST.md holds no entries.")
        print()
        print("  luma-foreman get <bundle> --from <catalog>   take one")
        print("  luma-foreman bundle new <name>               write one here")
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
    print(f"{len(rows)} bundle(s)" + (f", {len(wrong)} not as recorded." if wrong else "."))
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
    # recorded by name and the registry owns where that name lives. A bundle
    # written here has neither, and blank rows would report the absence as a
    # missing value rather than as what it is — no custody, because nothing
    # was taken from anywhere. The shape says which (ADR-0011), so one line
    # says it in words instead of three saying nothing.
    # A bundle written here that has been offered to a catalog: the entry
    # carries the destination and the outstanding request, and no custody yet
    # because the request may still be declined. This is where publication
    # state is *read* — `publish` advances the handover, and somebody who only
    # wants to know where it stands should not have to run the thing that
    # moves it.
    # Told apart by the invariant rather than by which fields are set: a
    # vendored copy always carries a commit and a checksum. On a bundle written
    # here `catalog` means the opposite direction — where it has been offered —
    # so reading it as custody would report an unpublished bundle as adopted,
    # with a blank where the commit belongs.
    vendored = bool(entry.commit and entry.checksum)
    if vendored and entry.catalog:
        print(f"  catalog    {entry.catalog}")
        print(f"  commit     {entry.commit}")
    elif vendored:
        print(f"  source     {entry.source}")
        print(f"  commit     {entry.commit}")
    elif entry.request:
        print(f"  offered    {entry.catalog}")
        print(f"  request    {entry.request}")
        print("  written    here — not published until that request merges")
    elif entry.catalog:
        print(f"  offered    {entry.catalog} — no request open")
        print("  written    here — nothing has taken it yet")
    else:
        print("  written    here — no catalog, and nothing to compare against")
    print(f"  at         {home.relative_to(project_root)}")
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

    **It writes two things: the bundle's own manifest, and its line in the
    project's.** A `MANIFEST.md` entry is what `bundle list`, `show` and `set`
    read, and without one a bundle written here exists to `apply` and
    `inspect` — which walk disk — and to nothing else. The entry is bare: no
    source, no commit, no checksum, because those are custody facts and a
    bundle written here has no custody. The shape *is* the distinction
    (ADR-0011 and the MVP design); there is no `local: true`, because a flag
    restating what the lines already show is a second copy of one fact.

    **It writes no directories.** Which ones a bundle needs depends on what it
    turns out to hold, and an empty `policy/` is a question a reader has to
    answer — as well as a directory git will not commit, so one created ahead
    of its contents exists only on the machine that ran this. The output names
    them instead.

    **Idempotent, and never destructive — `init`'s contract.** It adds
    whatever is missing and leaves every existing file exactly as it is. So it
    is also the claiming command: run it on a directory somebody drafted by
    hand and it supplies the missing half, whichever half that is. Refusing
    would make somebody do by hand the work the refusal had just finished
    diagnosing, and a `BUNDLE.md` is safe either way because this never
    overwrites one — that file is what makes a directory a bundle, so
    replacing it discards the bundle rather than the file.
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

    # Said out loud below, because the two cases differ in what the file that
    # lands is worth. Written fresh, the directory holds exactly what the
    # template says. Written onto something already there — a bundle drafted
    # by hand before this command existed — the version, stage and description
    # are placeholders sitting over documents that already exist.
    found = sorted(
        p.relative_to(home).as_posix() + ("/" if p.is_dir() else "")
        for p in home.iterdir()
    ) if home.is_dir() else []

    where = manifest.relative_to(project_root)
    wrote_manifest = not manifest.is_file()
    if wrote_manifest:
        home.mkdir(parents=True, exist_ok=True)
        manifest.write_text(TEMPLATE.format(name=name), encoding="utf-8")

    # The version comes from whichever BUNDLE.md is now on disk — the template's
    # 0.1.0 for a new bundle, the author's own for one being claimed. Read after
    # the write rather than assumed, so the two paths cannot diverge.
    version = lkf.unquote((lkf.read(manifest) or {}).get("version", ""))

    entries = adoption.read(project_root)
    record = adoption.manifest_path(project_root).relative_to(project_root)
    wrote_record = bundle_id not in entries
    if wrote_record:
        entries[bundle_id] = adoption.Adopted(
            bundle=bundle_id, version=version, source="", commit="", checksum="",
        )
        adoption.write(project_root, entries)

    print(f"{bundle_id}:")
    report = [
        (str(where), "created" if wrote_manifest else "already there, left alone"),
        (str(record), f"recorded {version}".rstrip() if wrote_record
                      else "already recorded, left alone"),
    ]
    width = max(len(p) for p, _ in report)
    for path, note in report:
        print(f"  {path:<{width}}  {note}")

    if not wrote_manifest and not wrote_record:
        print()
        print("Nothing to do.")
        return 0

    if found and wrote_manifest:
        print()
        print(f"  Written into a directory already there — it holds: "
              f"{', '.join(found)}")
        print("  The manifest is a template, so its description, version and")
        print("  stage describe none of it. Make them true of what is here.")
    print()

    # Only what this run actually left undone. Claiming a bundle somebody
    # wrote by hand and then telling them to fill in TODOs names placeholders
    # that are not in their file, which reads as the command not having
    # noticed what it just looked at.
    at = home.relative_to(project_root)
    steps = []
    if wrote_manifest:
        steps += [
            (f"edit {where}", "the TODOs — a bundle nobody can describe is not one"),
            (f"{at}/policy/",
             "what this obliges — create it only when something goes in it"),
            (f"{at}/procedure/",
             "what it tells an agent to do — same rule"),
        ]
    steps += [
        (f"luma-foreman bundle index {at}",
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

    # A bare noun shows what the noun can do. `luma-foreman` itself already
    # answers that way, and this noun holds four verbs that write — a bare
    # word that silently picks one of them is a guess that gets worse with
    # every verb added. `--help` stays the explicit route and is handled
    # above, so which verb a bare noun resolves to can change again without
    # touching the way anybody asks for help on purpose.
    verb = args[0] if args else "help"
    operands = args[1:]

    if verb == "help":
        print(USAGE)
        return 0
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
