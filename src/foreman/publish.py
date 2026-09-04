"""`publish` — offering a bundle written here to a catalog.

**Publishing is a custody handover, and the project ends up an adopter of its
own bundle.** That is what makes this unlike a package registry. When you
`npm publish`, your local source stays authoritative forever. Here, the moment
the bundle lands in the catalog this project stops owning it: the bare manifest
entry becomes a receipt with a catalog, a commit and a checksum, and editing
the bundle afterwards is divergence rather than authorship.

**The handover cannot complete until the recipient accepts**, so it spans a gap
that belongs to somebody else — minutes or weeks. Everything below exists to
cross that gap without guessing.

**Two operands, because where a bundle is going is not in its name.** `get` and
`remove` take one bundle ID and need nothing else, since the namespace already
says which catalog. A bundle written here has no namespace to read, and the
same bundle may legitimately go to more than one catalog. The command shapes
differ because the acts differ.

**Foreman writes; the catalog's gate judges.** There is no protocol here and no
service to talk to. This opens a pull request containing the bundle at its
final path; the catalog's own pre-merge job runs `luma-catalog-curator check`
against it; a maintainer merges. That is approve-or-reject, realised through
git rather than through something new.

**The only automatic transition is the merged one.** Every other answer reports
and waits for a person, because every other answer is somebody's decision. An
earlier design resolved the phase by looking for a pushed branch, which is
wrong: a maintainer who closes a request and deletes the branch leaves no
trace, so the tool would conclude *never asked* and re-open what was just
declined — manufacturing exactly the noise a curated catalog exists to avoid.
`request:` in the manifest is what makes the difference visible.
"""

from __future__ import annotations

import contextlib
import datetime
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

from . import adoption, catalog as catalogs, config, lkf, project, remove as removal

USAGE = """Offer a bundle written here to a catalog, and finish the handover once it lands.

  luma-foreman publish <bundle> <catalog>            open a request, or finish one
  luma-foreman publish <bundle> <catalog> --again    open a fresh request anyway
  luma-foreman publish <bundle> --abandon            stop tracking the recorded request

<bundle> is a bare name — command-line-interface — meaning the bundle written
here under local/. The local/ prefix is accepted and redundant. A full bundle
ID names whichever bundle is meant, which is how a bundle already in one
catalog is offered to another.

<catalog> is a registered catalog's name, which is its namespace. Register one
with: luma-foreman catalog add <url>

Run it again whenever. It advances the handover as far as it can and says where
it stopped: opening the request, reporting one still under review, or — once a
maintainer has merged it — taking the published bundle back as a vendored copy
and retiring the local one. To read the state without advancing anything, use
`luma-foreman bundle show <bundle>`.

  --to <project>     the project to publish from (default: this repository)

Opening a request needs `gh`, authenticated, and write access to the catalog.

Exit codes: 0 fine, 1 refused or waiting on somebody, 2 could not run."""


def _err(message: str) -> int:
    print(f"luma-foreman publish: {message}", file=sys.stderr)
    return 2


def _refuse(summary: str, remedy: str) -> int:
    print(f"luma-foreman publish: {summary}", file=sys.stderr)
    for line in remedy.splitlines():
        print(f"  {line}", file=sys.stderr)
    return 1


# --------------------------------------------------------------------------
# the forge


def _git(cwd: Path, *args: str) -> str | None:
    """Run git in *cwd* and return stripped stdout, or None if it could not."""
    try:
        out = subprocess.run(
            ["git", "-C", str(cwd), *args],
            capture_output=True, text=True, timeout=300,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def _gh(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess | None:
    """Run `gh` and hand back the result, or None if it could not run at all.

    Shelled out to the way `git` already is, so "no dependencies" stays true —
    it means no Python packages, not no programs.
    """
    try:
        return subprocess.run(
            ["gh", *args],
            capture_output=True, text=True, timeout=120,
            cwd=str(cwd) if cwd else None,
        )
    except (OSError, subprocess.SubprocessError):
        return None


def _gh_ready() -> str | None:
    """None if `gh` can be used, otherwise the message saying what to fix."""
    out = _gh("auth", "status")
    if out is None:
        return (
            "gh is not installed — it is what opens the request.\n"
            "  Install it: https://cli.github.com\n"
            "  Then: gh auth login"
        )
    if out.returncode != 0:
        return "gh is not authenticated.\n  Run: gh auth login"
    return None


def request_state(url: str) -> str | None:
    """``open``, ``merged``, ``closed``, ``missing`` — or None if it could not ask.

    **A 404 is not proof of anything.** GitHub answers 404 rather than 403 for a
    private resource you cannot see, so *not found* covers a declined request
    cleaned up, a catalog renamed, a catalog gone private, a token expired, and
    being authenticated as somebody else. That is why `missing` is reported
    with its possibilities rather than concluded from.

    None is separated from all of those on purpose: reaching the forge and
    being told nothing is there is an answer, and not reaching it is not.
    """
    if _gh_ready() is not None:
        return None
    out = _gh("pr", "view", url, "--json", "state")
    if out is None:
        return None
    if out.returncode != 0:
        return "missing"
    match = re.search(r'"state"\s*:\s*"(\w+)"', out.stdout)
    if not match:
        return "missing"
    return match.group(1).lower()


# --------------------------------------------------------------------------
# preparing the bundle


def _normalise(home: Path, new_id: str, published: str) -> str | None:
    """Give the copy its published identity. Returns a message on failure.

    Three edits, and they are the whole of what promotion changes in a bundle:
    the frontmatter title, the H1 that repeats it, and a `published:` date the
    local template deliberately omits because a bundle written in a project has
    no publish moment.
    """
    manifest = home / "BUNDLE.md"
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return f"cannot read {manifest}"

    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return f"{manifest} has no frontmatter — it cannot be published as a bundle"
    try:
        close = lines.index("---", 1)
    except ValueError:
        return f"{manifest} has no closing --- on its frontmatter"

    out: list[str] = []
    seen_title = False
    seen_published = False
    for i, line in enumerate(lines):
        if 0 < i < close:
            if line.startswith("title:"):
                out.append(f"title: {new_id}")
                seen_title = True
                continue
            if line.startswith("published:"):
                out.append(f"published: {published}")
                seen_published = True
                continue
        out.append(line)

    if not seen_title:
        out.insert(1, f"title: {new_id}")
        close += 1
    if not seen_published:
        # After the frontmatter's other keys rather than at the top: it is a
        # fact about this copy, not part of what the bundle is.
        out.insert(close, f"published: {published}")

    # The H1 repeats the title, so leaving it saying `local/` would put the
    # unpublished name in the one line a reader sees first. Substituted over
    # the body alone: `#` starts a comment in YAML, so a frontmatter line could
    # otherwise be rewritten as the heading.
    head = "\n".join(out[: close + 1])
    body = re.sub(
        r"(?m)^#\s+\S.*$", f"# {new_id}", "\n".join(out[close + 1:]), count=1
    )
    try:
        manifest.write_text((head + "\n" + body).rstrip("\n") + "\n", encoding="utf-8")
    except OSError as exc:
        return f"cannot write {manifest}: {exc}"
    return None


def _record(
    project_root: Path, entry: adoption.Adopted, catalog_name: str, url: str
) -> None:
    """Note the outstanding request against the bundle's own entry.

    The entry stays under `local/`, which is the invariant doing the work: a
    namespaced entry always carries a commit and a checksum, so a bundle whose
    request is still under review cannot be mistaken for one that landed.
    """
    entries = adoption.read(project_root)
    entries[entry.bundle] = adoption.Adopted(
        bundle=entry.bundle,
        version=entry.version,
        source=entry.source,
        commit=entry.commit,
        checksum=entry.checksum,
        register=entry.register,
        catalog=catalog_name,
        request=url,
    )
    adoption.write(project_root, entries)


def _open_request(
    project_root: Path,
    entry: adoption.Adopted,
    home: Path,
    catalog_name: str,
    source: str,
) -> int:
    ready = _gh_ready()
    if ready is not None:
        return _refuse("cannot open a request", ready)

    checkout = catalogs.work_clone(source)
    if checkout is None:
        return _err(f"could not clone {source}")
    catalog = catalogs.find(str(checkout))
    if isinstance(catalog, str):
        return _err(catalog)
    namespace = catalog.namespace or catalog_name
    name = entry.name
    new_id = f"{namespace}/{name}"

    if catalog.bundle(name) is not None:
        return _refuse(
            f"{catalog_name} already publishes {name}",
            f"Publishing does not overwrite. If this is meant to be a new\n"
            f"version of that bundle, that is an update to it in the catalog,\n"
            f"not a publication from here.",
        )

    dest = catalog.root / "bundles" / name
    shutil.copytree(
        home, dest, ignore=shutil.ignore_patterns(*adoption.IGNORED, ".git")
    )
    today = datetime.date.today().isoformat()
    problem = _normalise(dest, new_id, today)
    if problem:
        return _err(problem)

    # Regenerated, not copied: the local bundle's index names it under
    # `local/`. Its output is swallowed because it reports the path it wrote,
    # which here is a cache directory the reader has no business knowing about
    # — what matters is the request, and the file is in its diff.
    from . import bundle_index
    with contextlib.redirect_stdout(io.StringIO()):
        indexed = bundle_index.main([str(dest)])
    if indexed != 0:
        return _err(f"could not regenerate the index for {name}")

    branch = f"publish-{name}-{entry.version}"
    commit_message = (
        f"Publish {name} {entry.version}\n\n"
        f"Written in a project and offered here by `luma-foreman publish`.\n"
        f"Its namespace becomes {namespace}, derived from where this catalog\n"
        f"lives, so the bundle is addressed {new_id}.\n"
    )
    for args in (
        ("checkout", "-q", "-B", branch),
        ("add", "--", str(dest)),
        ("commit", "-q", "-m", commit_message),
    ):
        if _git(checkout, *args) is None:
            return _err(f"git {args[0]} failed in {checkout}")

    # The branch may already be on the remote from a run that pushed and then
    # failed to open the request — the one partial state this can leave. If a
    # request already references it, that request is the answer and recording
    # it is the repair. If nothing does, the branch is an orphan of our own
    # making and replacing it destroys nothing anybody is looking at.
    existing = _git(checkout, "ls-remote", "--heads", "origin", branch)
    overwrite: list[str] = []
    if existing:
        found = _gh(
            "pr", "list", "--head", branch, "--state", "open",
            "--json", "url", cwd=checkout,
        )
        if found is not None and found.returncode == 0:
            match = re.search(r'"url"\s*:\s*"([^"]+)"', found.stdout)
            if match:
                _record(project_root, entry, catalog_name, match.group(1))
                print(f"open    {match.group(1)}")
                print("  A request for this branch was already open — recorded "
                      "it here.")
                print("  Run this again once a maintainer has merged it.")
                return 0
        overwrite = ["--force-with-lease"]

    pushed = subprocess.run(
        ["git", "-C", str(checkout), "push", "-q", *overwrite,
         "--set-upstream", "origin", branch],
        capture_output=True, text=True, timeout=300,
    )
    if pushed.returncode != 0:
        return _refuse(
            f"could not push to {catalog_name}",
            f"{pushed.stderr.strip().splitlines()[-1] if pushed.stderr.strip() else 'push refused'}\n"
            f"Opening a request needs write access to the catalog. Forking on\n"
            f"your behalf is not built yet — fork it, then publish against\n"
            f"your fork and open the request by hand.",
        )

    created = _gh(
        "pr", "create",
        "--title", f"Publish {name} {entry.version}",
        "--body", commit_message,
        cwd=checkout,
    )
    if created is None or created.returncode != 0:
        detail = (created.stderr.strip() if created else "gh could not run")
        return _err(f"could not open the request: {detail}")

    url = ""
    for line in created.stdout.splitlines():
        if line.startswith("http"):
            url = line.strip()
    if not url:
        return _err("the request was opened but gh did not print its URL")

    _record(project_root, entry, catalog_name, url)

    print(f"opened  {url}")
    print(f"  bundle   {entry.bundle} {entry.version}")
    print(f"  becomes  {new_id}")
    print()
    print("  Not published yet — a maintainer has to merge it.")
    print("  Run this again afterwards to finish the handover.")
    return 0


# --------------------------------------------------------------------------
# finishing


def _repoint(project_root: Path, old_id: str, new_id: str, home: Path) -> list[str]:
    """Rewrite references to *old_id*, and return the files changed.

    Only exact occurrences of the bundle ID and of its path under
    `.luma/bundles/`. Anything looser would edit prose on a guess, and this
    runs unattended at the end of a handover.
    """
    changed = []
    old_path = f".luma/bundles/{old_id}"
    new_path = f".luma/bundles/{new_id}"
    for rel in removal.references(project_root, old_id, home):
        path = project_root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        # The longer path first, or rewriting the bare ID leaves a mangled path
        # behind it.
        updated = text.replace(old_path, new_path).replace(old_id, new_id)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed.append(rel)
    return changed


def _complete(
    project_root: Path,
    entry: adoption.Adopted,
    catalog_name: str,
    source: str,
    url: str,
) -> int:
    from . import apply, get

    catalog = catalogs.find(source)
    if isinstance(catalog, str):
        return _err(catalog)
    namespace = catalog.namespace or catalog_name
    new_id = f"{namespace}/{entry.name}"

    if catalog.bundle(entry.name) is None:
        return _refuse(
            f"{url} is merged, but {catalog_name} does not publish "
            f"{entry.name}",
            "The request landed and the bundle is not there. Something else\n"
            "changed it after the merge — look at the catalog before rerunning.",
        )

    landed = lkf.read(catalog.bundle(entry.name) / "BUNDLE.md") or {}
    version = lkf.unquote(landed.get("version", ""))

    print(f"merged  {url}")
    taken = get.run(new_id, source, project_root, force=False)
    if taken != 0:
        return taken

    home = adoption.vendored(project_root, entry.bundle)
    changed = _repoint(project_root, entry.bundle, new_id, home)

    entries = adoption.read(project_root)
    if entry.bundle in entries:
        del entries[entry.bundle]
        adoption.write(project_root, entries)
    if home.is_dir():
        shutil.rmtree(home)

    print()
    print(f"  removed    {entry.bundle}")
    if changed:
        print(f"  repointed  {len(changed)} file(s):")
        for rel in changed:
            print(f"    {rel}")
    if version and version != entry.version:
        print()
        print(
            f"  note: {entry.version} was offered and {version} landed — the "
            f"catalog's copy is what this project now holds."
        )
    print()
    apply.main(["--to", str(project_root)])
    return 0


# --------------------------------------------------------------------------


def run(
    project_root: Path,
    requested: str,
    catalog_name: str | None,
    again: bool,
    abandon: bool,
) -> int:
    entries = adoption.read(project_root)
    found = adoption.resolve(entries, requested)
    if isinstance(found, str):
        return _err(found)
    entry = found

    if abandon:
        if not entry.request:
            print(f"{entry.bundle}: no request recorded — nothing to abandon")
            return 0
        dropped = entry.request
        entries[entry.bundle] = adoption.Adopted(
            bundle=entry.bundle,
            version=entry.version,
            source=entry.source,
            commit=entry.commit,
            checksum=entry.checksum,
            register=entry.register,
            # The destination stays. It was a decision somebody made, and it is
            # still true that this is where the bundle was meant to go — only
            # the request died. Keeping it means a retry needs no re-typing.
            catalog=entry.catalog,
            request="",
        )
        adoption.write(project_root, entries)
        print(f"{entry.bundle}: stopped tracking {dropped}")
        if entry.catalog:
            print(f"  still intended for {entry.catalog}")
        return 0

    if catalog_name is None:
        catalog_name = entry.catalog
    if not catalog_name:
        return _err("usage: luma-foreman publish <bundle> <catalog>")

    registered = config.registry(project_root)
    source = registered.get(catalog_name)
    if source is None:
        known = "\n".join(f"    {n}" for n in sorted(registered))
        return _err(
            f"no catalog registered as {catalog_name}.\n"
            + (f"  Registered here:\n{known}\n" if registered else "")
            + f"  Register one: luma-foreman catalog add <url>"
        )

    if entry.request and not again:
        state = request_state(entry.request)
        if state is None:
            return _err(
                f"could not reach the forge to check {entry.request} — "
                f"nothing changed"
            )
        if state == "open":
            print(f"open    {entry.request} — nothing to do yet")
            print(f"  {entry.bundle} {entry.version} is waiting on a maintainer.")
            return 0
        if state == "merged":
            return _complete(
                project_root, entry, catalog_name, source, entry.request
            )
        if state == "closed":
            return _refuse(
                f"{entry.request} was declined",
                f"{entry.bundle} {entry.version} was not taken, and nothing\n"
                f"here has changed.\n"
                f"To ask again:\n"
                f"  luma-foreman publish {requested} {catalog_name} --again\n"
                f"To stop tracking it:\n"
                f"  luma-foreman publish {requested} --abandon",
            )
        return _refuse(
            "the recorded request is no longer visible",
            f"bundle   {entry.bundle} {entry.version}\n"
            f"catalog  {catalog_name}\n"
            f"request  {entry.request} — not found\n"
            f"\n"
            f"It may have been declined and cleaned up, or the catalog may\n"
            f"have moved, become private, or stopped granting you access.\n"
            f"\n"
            f"To open a fresh request:\n"
            f"  luma-foreman publish {requested} {catalog_name} --again\n"
            f"To stop tracking this one:\n"
            f"  luma-foreman publish {requested} --abandon",
        )

    home = adoption.vendored(project_root, entry.bundle)
    if not home.is_dir():
        return _err(f"{entry.bundle} is recorded but not on disk at {home}")
    if not entry.version:
        return _refuse(
            f"{entry.bundle} declares no version",
            "A bundle a catalog cannot pin is a bundle nobody downstream can\n"
            "decide about. Give it a version in its BUNDLE.md first.",
        )
    return _open_request(project_root, entry, home, catalog_name, source)


def main(argv: list[str]) -> int:
    target: Path | None = None
    again = False
    abandon = False
    operands: list[str] = []

    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            return 0
        if arg == "--again":
            again = True
        elif arg == "--abandon":
            abandon = True
        elif arg == "--force":
            # `--force` overrides a guard protecting something. Asking a
            # catalog a second time defends nothing and destroys nothing, so it
            # is a different word — and saying so beats letting it read as a
            # typo.
            return _err(
                "--force is not a publish option — to ask a catalog again, "
                "use --again"
            )
        elif arg == "--to":
            if not rest:
                return _err("--to needs a project directory")
            target = Path(rest.pop(0))
        elif arg.startswith("-"):
            return _err(f"unknown option: {arg}")
        else:
            operands.append(arg)

    if target and not target.is_dir():
        return _err(f"not a directory: {target}")
    project_root, _ = project.resolve(target or Path.cwd())

    if again and abandon:
        return _err("--again and --abandon ask for opposite things")
    if not operands or len(operands) > 2:
        return _err("usage: luma-foreman publish <bundle> <catalog>")
    if len(operands) == 1 and not abandon:
        return _err(
            f"name the catalog: luma-foreman publish {operands[0]} <catalog>.\n"
            f"  A bundle can go to more than one, so there is nothing to infer.\n"
            f"  Registered catalogs: luma-foreman catalog list"
        )

    bundle = operands[0]
    catalog_name = operands[1] if len(operands) == 2 else None
    return run(project_root, bundle, catalog_name, again, abandon)
