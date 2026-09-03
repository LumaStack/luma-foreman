"""What a project sets, and where.

**A config holds overrides and as little else as possible.** What is absent
follows the tool and improves with it; what is written down is frozen, so the
smallest file is the one that ages best. That is `luma-layout`'s rule for
`.luma/config/`, and it is why the settings here stay few.

**The catalog registry is the sources list.** A named entry under
``[catalog."<name>"]`` says where one catalog lives, the way an apt source
does — registered once, committed, and shared by every clone. The receipts in
`MANIFEST.md` then record the *name*, so a moved catalog is one line here
rather than every receipt going stale. The bare ``[catalog] source`` default
predates the registry and is still read.

This lives apart from the commands that read it. `get`, `catalog` and `init`
all ask, and none of them owns the answer — a config reached through whichever
command happened to define it is a config nobody can find.
"""

from __future__ import annotations

import os
import tempfile
import tomllib
from pathlib import Path


CONFIG = "luma-foreman.toml"


def config_path(project_root: Path) -> Path:
    return project_root / ".luma" / "config" / CONFIG


def _read(project_root: Path) -> dict:
    path = config_path(project_root)
    if not path.is_file():
        return {}
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return {}


def catalog_source(project_root: Path) -> str | None:
    """``[catalog] source``, or None where the project does not set one."""
    source = _read(project_root).get("catalog", {}).get("source")
    return str(source) if isinstance(source, str) and source else None


def registry(project_root: Path) -> dict[str, str]:
    """The registered catalogs, name to source, in file order.

    A name is the catalog's namespace — ``lumastack/luma-catalog`` — which is
    what lets `get` resolve a bundle ID with nothing but this dict: the ID
    starts with the name of the catalog that publishes it.
    """
    return {
        name: str(table["source"])
        for name, table in _read(project_root).get("catalog", {}).items()
        if isinstance(table, dict) and isinstance(table.get("source"), str)
        and table["source"]
    }


def register_catalog(project_root: Path, name: str, source: str) -> None:
    """Append one ``[catalog."<name>"]`` entry to the config.

    Appended rather than re-rendered, because the file is the operator's — it
    carries their comments and their `[[retired]]` terms, and a writer that
    round-trips TOML would need to own all of it. A table header is position-
    independent, so the end of the file is as correct a place as any.

    The caller has checked the name is free; this only writes. Atomic the way
    `agent_permissions/store.py` writes: a temp file beside the target, then
    `os.replace`, so a crash leaves the old config rather than half of one.
    """
    path = config_path(project_root)
    text = path.read_text(encoding="utf-8")
    if text and not text.endswith("\n"):
        text += "\n"
    text += f'\n[catalog."{name}"]\nsource = "{source}"\n'
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{CONFIG}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        os.replace(tmp, path)
    except OSError:
        Path(tmp).unlink(missing_ok=True)
        raise
