"""What a project sets, and where.

**A config holds overrides and as little else as possible.** What is absent
follows the tool and improves with it; what is written down is frozen, so the
smallest file is the one that ages best. That is `luma-layout`'s rule for
`.luma/config/`, and it is why there is one setting here rather than a schema.

This lives apart from the commands that read it. `get`, `catalog` and `init`
all ask, and none of them owns the answer — a config reached through whichever
command happened to define it is a config nobody can find.
"""

from __future__ import annotations

import tomllib
from pathlib import Path


CONFIG = "luma-foreman.toml"


def config_path(project_root: Path) -> Path:
    return project_root / ".luma" / "config" / CONFIG


def catalog_source(project_root: Path) -> str | None:
    """``[catalog] source``, or None where the project does not set one."""
    path = config_path(project_root)
    if not path.is_file():
        return None
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return None
    source = data.get("catalog", {}).get("source")
    return str(source) if source else None



