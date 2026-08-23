"""Reading just enough of the knowledge format to act on it.

**A deliberate subset, and the subset is the point.** Top-level ``key: value``
and enough of the block syntax to catch the nested-array trap. Anything that
needs real YAML is a job that belongs somewhere else, not a reason to grow this.

It lives here rather than inside a rule because two callers now need it —
``inspect`` reports on bundles and ``adopt`` copies them — and the second caller
is exactly when a private helper becomes a shared one. A tool that grew a second
frontmatter reader would be doing to itself what the estate already does to
itself across three languages, which is a known problem rather than a new one.

**Reading a value here is never validation.** A missing key comes back as None
and an unparseable one comes back as text; §4 puts a MUST on consumers not to
reject a Document for what they do not understand, and a reader that raised
would make every caller responsible for remembering that.
"""

from __future__ import annotations

import re
from pathlib import Path

KEY = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$", re.M)

# `[[…]]` is YAML flow-sequence syntax, so an unquoted wikilink in frontmatter
# parses as a nested array rather than a string — silently, with no parser
# complaining. The document stays valid and the link never resolves. This is the
# single most likely defect in a hand-written bundle.
TRAP = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*\[\[", re.M)


def split(text: str) -> tuple[str | None, str]:
    """Frontmatter block and body. Frontmatter must open on the first line."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[4:end], text[end + 4 :]


def keys(front: str) -> dict[str, str]:
    """Top-level scalars. Nested keys collapse into the same flat dict."""
    return {m.group(1): m.group(2) for m in KEY.finditer(front)}


def read(path: Path) -> dict[str, str] | None:
    """A Document's frontmatter keys, or None if it has none.

    None means *this is an Asset* — a file with no frontmatter — which is a
    legitimate thing for a Bundle to contain and never an error.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    front, _ = split(text)
    return None if front is None else keys(front)


def unquote(value: str) -> str:
    """Strip the quotes a YAML scalar may carry.

    ``version: "0.2.0"`` and ``version: 0.2.0`` are the same version, and a
    caller comparing one spelling against the other would report drift that is
    not there.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value
