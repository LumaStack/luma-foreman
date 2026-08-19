"""Where policy lives, and how it resolves.

Per key, most specific wins:

    <home>/projects/<slug>.toml   the project the session is in
    <home>/policy.toml            global fallback
    the built-in defaults         shipped

Nothing is stored inside the project being governed, so none of it can be
committed by accident. What an agent may do in a repository is the operator's
call on their own machine, not a property every clone inherits.
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path

from ..project import resolve
from . import model


def home() -> Path:
    """The policy directory — configuration the operator edits.

    XDG puts configuration in ~/.config and program-installed files in
    ~/.local/share, and the split matters here beyond tidiness: someone clearing
    the config directory to reset their settings must not thereby delete the
    gate. A missing hook is a non-blocking error in Claude Code, so the tool call
    proceeds — the gate would fail OPEN because a config reset looked safe.

    Nested under the vendor: ~/.config/luma/luma-foreman/.

    The app segment is the repository name in full, prefix included, so a
    directory maps to a repository by inspection with nothing to translate.

    The specification does not choose for us — it says $XDG_CONFIG_HOME/subdir/
    and leaves naming and depth to the application. Flat is the common shape
    among single-tool vendors (gh, git, nvim) for the obvious reason that they
    have nothing to nest under. JetBrains ships multiple tools and nests, across
    config, data and cache alike.

    What decides it is that a rule covering every tool has to be writable once.
    Flat needs one entry per application or a `luma-*` wildcard, and the wildcard
    holds only while every tool is named `luma-something` — a convention nobody
    has committed to, and one product-named tool breaks it with no single rule
    left to write. Nesting is indifferent to what things are called.
    """
    if override := os.environ.get("LUMA_FOREMAN_HOME"):
        return Path(override)
    config = os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")
    return Path(config) / "luma" / "luma-foreman"


def data_home() -> Path:
    """Where the installed gate lives — code foreman writes and overwrites."""
    if override := os.environ.get("LUMA_FOREMAN_DATA"):
        return Path(override)
    data = os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share")
    return Path(data) / "luma" / "luma-foreman"


def legacy_dirs() -> list[Path]:
    """Directories left by earlier layouts, newest first.

    Reported rather than deleted: settings.json may still point into one, and
    removing it before the wiring moves would leave the running session
    unguarded.
    """
    config = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
    data = Path(os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share"))
    return [
        d for d in (data / "luma-foreman", config / "luma-foreman",
                   data / "luma" / "foreman", config / "luma" / "foreman")
        if d.exists()
    ]


def _read(path: Path) -> dict[str, str]:
    """Parse one policy file, tolerating a broken one.

    A malformed file must not silently disable the gate, so a parse failure
    yields no keys and the caller falls back to less specific sources — never
    to "no opinion". Values are coerced to str so a stray `curl = true` cannot
    smuggle a non-string through.
    """
    try:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
    except (OSError, tomllib.TOMLDecodeError):
        return {}
    return {
        k: str(v)
        for k, v in data.items()
        if isinstance(k, str) and isinstance(v, (str, int, float, bool))
    }


@dataclass(frozen=True)
class Resolved:
    project_dir: Path
    slug: str
    project_file: Path
    global_file: Path
    values: dict[str, str]
    sources: dict[str, str]  # key -> "project" | "global" | "default"

    def __getitem__(self, key: str) -> str:
        return self.values[key]


def resolve_for(cwd: str | os.PathLike[str], root: Path | None = None) -> Resolved:
    base = root or home()
    project_dir, project_slug = resolve(cwd)
    project_file = base / "projects" / f"{project_slug}.toml"
    global_file = base / "policy.toml"

    values = model.defaults()
    sources = {k: "default" for k in values}
    for path, label in ((global_file, "global"), (project_file, "project")):
        for k, v in _read(path).items():
            if k in values:
                values[k], sources[k] = v, label
    return Resolved(project_dir, project_slug, project_file, global_file, values, sources)


def write_key(path: Path, key: str, value: str, project_dir: Path | None) -> None:
    """Set one key, preserving the rest of the file and its comments."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if path.exists():
        lines = path.read_text().splitlines()
    else:
        lines = [
            "# Claude Code permission policy.",
            "# Read by the permission gate on every Bash tool call.",
            *([f"# Project: {project_dir}"] if project_dir else []),
            "# Edit with `luma-foreman policy`, not by hand from an agent session.",
            "",
        ]

    out, done = [], False
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", "[")) and "=" in line:
            if line.split("=", 1)[0].strip() == key:
                if not done:
                    out.append(f'{key} = "{value}"')
                    done = True
                continue
        out.append(line)
    if not done:
        out.append(f'{key} = "{value}"')
    _atomic_write(path, "\n".join(out) + "\n")


def drop_key(path: Path, key: str) -> None:
    if not path.exists():
        return
    out = []
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(("#", "[")) and "=" in line:
            if line.split("=", 1)[0].strip() == key:
                continue
        out.append(line)
    _atomic_write(path, "\n".join(out) + "\n")


def _atomic_write(path: Path, text: str) -> None:
    """Write via a temp file in the same directory, then rename.

    The gate may read this file at any moment — it runs on every tool call —
    so a partially written policy must never be observable.
    """
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text)
    os.replace(tmp, path)
