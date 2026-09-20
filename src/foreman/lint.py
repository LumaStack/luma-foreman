"""``luma-foreman lint`` — validate Documents against the Type Definitions they cite.

An implementation of the LKF specification's *Validation* section — the
suggested severity table, exactly, so that a second implementation written
against the same table agrees with this one. It is a command of its own:
linting needs no repository health check and no adoption record, only files.
``inspect`` is welcome to call the engine here; the dependency never points
the other way.

**Validation is optional and never rejects by default** (the spec's own rule).
Every finding is a warning or quieter unless ``--strict`` is given, and even
``--strict`` escalates only what the table says it may: a ``deprecated`` field
stays a warning, an unknown field or an undefined type is never reported at
all, and ``type_version`` currency stays info — a document that is
old-but-labelled is the system working, not failing.

**One engine, one walk.** A Type Definition is an ordinary Document
(``type: type_definition``), so it is validated against the built-in
``type_definition`` contract by the same code path as everything else. What
cannot ride that path is exactly three families, special-cased where the
format's own expressiveness runs out:

- **layout** — the folder shape of ``type_definitions/`` is files and paths,
  which frontmatter validation never sees;
- **nested grammar** — the ``fields:`` mapping's internal rules, invisible to
  generic shape checks because the contract declares ``fields`` as ``text``
  (LKF has no composite field type yet);
- **relations** — checks that need two documents: ``extends`` resolution,
  add-only inheritance, and ``type_version`` currency.

**Resolution keys on the directory root a Document is found under**: the
nearest ancestor holding ``type_definitions/<name>/DEFINITION.md`` wins. For a
Document inside a Bundle that is the Bundle (the spec's rule); for a root
store like a clarify notebook it is the root — the reading the LKF roadmap
tracks as the likely fix, and the one that needs no configuration.

**The built-in types ship here** (the spec says a tool MAY supply them),
transcribed from the format's own bundle at the versions noted below. A
``field_type`` this module cannot check — including the bespoke shapes the
built-ins themselves declare — passes silently: lenient is the direction the
format mandates, and a checker that flagged the format's own bundle would be
wrong by construction.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from . import lkf

# ---------------------------------------------------------------------------
# model

ERROR, WARNING, INFO = "error", "warning", "info"

# The spec's escalation column: these classes become errors under --strict.
# Everything else keeps its default level in both modes.
ESCALATES = frozenset({
    "required-missing", "shape-mismatch", "enum-unlisted", "extends-broken",
    "definition-missing", "single-file-shape", "folder-mismatch",
    "fields-grammar", "inheritance",
})


@dataclass(frozen=True)
class Finding:
    level: str
    path: str
    message: str
    kind: str  # the class, for escalation and for --json some day


@dataclass(frozen=True)
class FieldDecl:
    presence: str = ""      # required | recommended | optional | deprecated
    field_type: str = ""    # "" means undeclared — legal, and uncheckable
    values: tuple[str, ...] = ()


@dataclass
class Definition:
    defines: str
    version: str = ""
    extends: str = ""
    fields: dict[str, FieldDecl] = field(default_factory=dict)
    path: Path | None = None  # None for a built-in


PRESENCES = ("required", "recommended", "optional", "deprecated")
# Strength order for the never-weakened rule. `deprecated` is deliberately
# outside it: deprecating an inherited field is a lifecycle act the spec has
# not ruled on, and flagging it would be inventing a rule.
STRENGTH = {"optional": 0, "recommended": 1, "required": 2}

# ---------------------------------------------------------------------------
# built-ins — transcribed from luma-knowledge-format/type_definitions/*/
# (each at its own version 0.0.1, shipped with format release v0.0.21)

def _d(**kw: FieldDecl) -> dict[str, FieldDecl]:
    return dict(kw)


BUILTINS: dict[str, Definition] = {
    "document": Definition("document", "0.0.1", "", _d(
        type=FieldDecl("required", "text"),
        type_version=FieldDecl("recommended", "semver"),
        title=FieldDecl("recommended", "text"),
        description=FieldDecl("optional", "text"),
        tags=FieldDecl("optional", "list of text"),
        stage=FieldDecl("optional", "enum",
                        ("draft", "provisional", "stable", "archived", "unknown")),
        survival=FieldDecl("optional", "enum",
                           ("temporary", "probationary", "intended", "promised")),
        created=FieldDecl("optional", "actor_event"),
        modified=FieldDecl("recommended", "actor_event"),
        verified=FieldDecl("optional", "list of actor_event"),
        sources=FieldDecl("optional", "list"),
        stale_after=FieldDecl("optional", "date"),
        matches=FieldDecl("optional", "list_or_keyword", ("eager", "nothing")),
    )),
    "policy": Definition("policy", "0.0.1", "document", _d(
        on_violation=FieldDecl("optional", "enum",
                               ("allow", "audit", "warn", "require_reason",
                                "require_approval", "block")),
    )),
    "procedure": Definition("procedure", "0.0.1", "document", {}),
    "bundle": Definition("bundle", "0.0.1", "document", _d(
        version=FieldDecl("required", "semver"),
        published=FieldDecl("recommended", "date"),
        consumers=FieldDecl("optional", "list of text"),
    )),
    "type_definition": Definition("type_definition", "0.0.1", "document", _d(
        defines=FieldDecl("required", "text"),
        extends=FieldDecl("optional", "text"),
        fields=FieldDecl("recommended", "text"),
        version=FieldDecl("optional", "semver"),
    )),
}

# ---------------------------------------------------------------------------
# frontmatter, structured just enough
#
# lkf.py reads flat scalars on purpose and says richer parsing belongs
# elsewhere. This is elsewhere. Still a deliberate subset: top-level entries
# with their raw inline value and raw indented block, one flow-map/-sequence
# splitter, and the field-declaration grammar. Anything beyond that passes
# unjudged — lenient is the mandated direction.

TOP = re.compile(r"^([A-Za-z_][\w-]*)\s*:[ \t]*(.*)$")


@dataclass(frozen=True)
class Entry:
    inline: str
    block: tuple[str, ...]  # the raw indented lines that followed


def entries(front: str) -> dict[str, Entry]:
    out: dict[str, Entry] = {}
    name: str | None = None
    inline = ""
    block: list[str] = []
    for line in front.splitlines():
        m = TOP.match(line)
        if m:
            if name is not None:
                out[name] = Entry(inline, tuple(block))
            name, inline, block = m.group(1), m.group(2).strip(), []
        elif name is not None and (line.startswith((" ", "\t")) or line.strip() == ""):
            block.append(line)
    if name is not None:
        out[name] = Entry(inline, tuple(block))
    return out


def _split_flow(text: str) -> list[str]:
    """Split a flow collection's inside on commas, respecting quotes and nesting."""
    parts: list[str] = []
    depth = 0
    quote = ""
    current = ""
    for ch in text:
        if quote:
            current += ch
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            current += ch
        elif ch in "[{":
            depth += 1
            current += ch
        elif ch in "]}":
            depth -= 1
            current += ch
        elif ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    return parts


def flow_map(text: str) -> dict[str, str] | None:
    text = text.strip()
    if not (text.startswith("{") and text.endswith("}")):
        return None
    out: dict[str, str] = {}
    for part in _split_flow(text[1:-1]):
        key, colon, value = part.partition(":")
        if not colon:
            return None
        out[key.strip()] = value.strip()
    return out


def flow_seq(text: str) -> list[str] | None:
    text = text.strip()
    if not (text.startswith("[") and text.endswith("]")):
        return None
    return [lkf.unquote(p) for p in _split_flow(text[1:-1])]

# ---------------------------------------------------------------------------
# definitions

SUBKEY = re.compile(r"^(\s+)([A-Za-z_][\w-]*)\s*:[ \t]*(.*)$")


def parse_definition(path: Path) -> tuple[Definition | None, list[Finding]]:
    """The Definition at *path*, plus grammar findings from inside ``fields:``."""
    findings: list[Finding] = []
    try:
        front, _ = lkf.split(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return None, findings
    if front is None:
        return None, findings
    top = entries(front)
    if lkf.unquote(top.get("type", Entry("", ())).inline) != "type_definition":
        return None, findings

    rel = str(path)

    def gram(message: str) -> None:
        findings.append(Finding(WARNING, rel, message, "fields-grammar"))

    defn = Definition(
        defines=lkf.unquote(top.get("defines", Entry("", ())).inline),
        version=lkf.unquote(top.get("version", Entry("", ())).inline),
        extends=lkf.unquote(top.get("extends", Entry("", ())).inline),
        path=path,
    )

    fields_entry = top.get("fields")
    if fields_entry is None:
        return defn, findings
    if fields_entry.inline in ("{}", "[]"):
        return defn, findings
    if fields_entry.inline:
        gram("`fields:` carries an inline value — the spec declares a mapping "
             "of field declarations")
        return defn, findings

    # Block form: either `name:` items (the mapping the spec declares) or a
    # sequence of `- name: …` items (a shape the spec never had; some early
    # definitions carry it and their instances cannot be shape-checked).
    lines = [ln for ln in fields_entry.block if ln.strip()]
    if lines and lines[0].lstrip().startswith("-"):
        gram("`fields:` is a sequence — the spec declares a mapping keyed by "
             "field name, so these declarations validate nothing")
        return defn, findings

    base_indent: int | None = None
    current: str | None = None
    decl: dict[str, str] = {}

    def close() -> None:
        nonlocal current, decl
        if current is None:
            return
        presence = lkf.unquote(decl.get("field_presence", ""))
        ftype = lkf.unquote(decl.get("field_type", ""))
        raw_values = decl.get("values", "")
        values = tuple(flow_seq(raw_values) or ()) if raw_values else ()
        if presence and presence not in PRESENCES:
            gram(f"field `{current}` declares field_presence `{presence}` — "
                 "the vocabulary is " + ", ".join(PRESENCES))
        if ftype == "enum" and not values:
            gram(f"field `{current}` is an enum with no `values` — required "
                 "when field_type is enum")
        defn.fields[current] = FieldDecl(presence or "optional", ftype, values)
        current, decl = None, {}

    for line in lines:
        m = SUBKEY.match(line)
        if m is None:
            continue  # comments, continuation prose — not ours to judge
        indent, key, value = len(m.group(1)), m.group(2), m.group(3).strip()
        if base_indent is None:
            base_indent = indent
        if indent == base_indent:
            close()
            current = key
            fm = flow_map(value) if value else None
            if fm is not None:
                decl = fm
            elif value:
                gram(f"field `{key}` declares a scalar, not a declaration — "
                     "expected `{ field_presence: …, field_type: … }` or an "
                     "indented block")
                current = None
        elif current is not None and indent > base_indent:
            decl[key] = value
    close()
    return defn, findings

# ---------------------------------------------------------------------------
# resolution

class Scope:
    """Definition lookup, keyed on the directory root a Document sits under."""

    def __init__(self, root: Path):
        self.root = root.resolve()
        self._cache: dict[tuple[Path, str], Definition | None] = {}
        self.grammar: dict[Path, list[Finding]] = {}

    def _load(self, path: Path) -> Definition | None:
        defn, findings = parse_definition(path)
        if path not in self.grammar:
            self.grammar[path] = findings
        return defn

    def resolve(self, doc: Path, type_name: str) -> Definition | None:
        bare = type_name.rsplit("/", 1)[-1]
        directory = doc.resolve().parent
        while True:
            key = (directory, type_name)
            if key in self._cache:
                if self._cache[key] is not None:
                    return self._cache[key]
            else:
                candidate = directory / "type_definitions" / bare / "DEFINITION.md"
                found: Definition | None = None
                if candidate.is_file():
                    defn = self._load(candidate)
                    if defn is not None and defn.defines == type_name:
                        found = defn
                self._cache[key] = found
                if found is not None:
                    return found
            if directory == self.root or directory.parent == directory:
                break
            directory = directory.parent
        return BUILTINS.get(type_name)

    def effective_fields(self, defn: Definition, doc: Path) -> dict[str, FieldDecl]:
        """The definition's fields merged over its extends chain."""
        chain: list[Definition] = []
        seen: set[str] = set()
        node: Definition | None = defn
        while node is not None and node.defines not in seen and len(chain) < 12:
            chain.append(node)
            seen.add(node.defines)
            node = self.resolve(doc, node.extends) if node.extends else None
        merged: dict[str, FieldDecl] = {}
        for ancestor in reversed(chain):
            for name, decl in ancestor.fields.items():
                parent = merged.get(name)
                if parent is not None and not decl.field_type:
                    # Presence-only restatement inherits the parent's shape.
                    decl = FieldDecl(decl.presence, parent.field_type, parent.values)
                merged[name] = decl
        return merged

# ---------------------------------------------------------------------------
# shape checks — True: fine, False: mismatch, None: cannot judge (passes)

DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][\w.-]+)?$")
NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")


def _scalar(entry: Entry) -> str | None:
    if entry.inline and not entry.inline.startswith(("[", "{")):
        return lkf.unquote(entry.inline)
    return None


def _items(entry: Entry) -> list[str] | None:
    if entry.inline:
        return flow_seq(entry.inline)
    items = [ln.strip()[1:].strip() for ln in entry.block if ln.strip().startswith("- ")]
    return items or None


def _is_map(entry: Entry) -> bool:
    if entry.inline.startswith("{"):
        return True
    return any(SUBKEY.match(ln) for ln in entry.block)


def check_shape(ftype: str, entry: Entry) -> bool | None:
    if ftype.startswith("list of "):
        inner = ftype[len("list of "):]
        items = _items(entry)
        if items is None:
            return False if _scalar(entry) is not None else None
        verdicts = [check_shape(inner, Entry(item, ())) for item in items]
        return False if False in verdicts else True
    scalar = _scalar(entry)
    if ftype in ("text", "enum"):
        return None if scalar is None else True
    if ftype == "number":
        return None if scalar is None else bool(NUMBER.match(scalar))
    if ftype == "boolean":
        return None if scalar is None else scalar in ("true", "false")
    if ftype == "date":
        return None if scalar is None else bool(DATE.match(scalar))
    if ftype == "datetime":
        return None if scalar is None else bool(DATE.match(scalar[:10]) and "T" in scalar)
    if ftype == "semver":
        return None if scalar is None else bool(SEMVER.match(scalar))
    if ftype == "wikilink":
        return None if scalar is None else scalar.startswith("[[") and scalar.endswith("]]")
    if ftype == "uri":
        return None if scalar is None else "://" in scalar or scalar.startswith("mailto:")
    if ftype == "actor":
        return None if scalar is None else ":" in scalar
    if ftype == "actor_event":
        return True if _is_map(entry) else (False if scalar is not None else None)
    return None  # a shape this module cannot express an opinion on

# ---------------------------------------------------------------------------
# the checks

def validate_document(path: Path, rel: str, scope: Scope) -> list[Finding]:
    findings: list[Finding] = []
    try:
        front, _ = lkf.split(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return findings
    if front is None:
        return findings  # an Asset, never an error
    top = entries(front)
    type_entry = top.get("type")
    if type_entry is None:
        return findings  # untyped: nothing to validate against
    type_name = lkf.unquote(type_entry.inline)
    defn = scope.resolve(path, type_name)
    if defn is None:
        return findings  # a type with no Type Definition — never reported

    fields = scope.effective_fields(defn, path)
    for name, decl in sorted(fields.items()):
        entry = top.get(name)
        if entry is None:
            if decl.presence == "required":
                findings.append(Finding(
                    WARNING, rel,
                    f"missing required field `{name}` ({type_name})",
                    "required-missing"))
            elif decl.presence == "recommended":
                findings.append(Finding(
                    INFO, rel,
                    f"missing recommended field `{name}` ({type_name})",
                    "recommended-missing"))
            continue
        if decl.presence == "deprecated":
            findings.append(Finding(
                WARNING, rel,
                f"`{name}` is deprecated by {type_name}'s definition",
                "deprecated-present"))
        if decl.field_type == "enum" and decl.values:
            scalar = _scalar(entry)
            if scalar is not None and scalar not in decl.values:
                findings.append(Finding(
                    WARNING, rel,
                    f"`{name}: {scalar}` is not among {type_name}'s values — "
                    + ", ".join(decl.values),
                    "enum-unlisted"))
        elif decl.field_type and check_shape(decl.field_type, entry) is False:
            findings.append(Finding(
                WARNING, rel,
                f"`{name}` does not look like {decl.field_type} ({type_name})",
                "shape-mismatch"))

    # Currency — the check the migration bought. Info in every mode: a
    # document that is old and says so is the system working.
    cited = lkf.unquote(top.get("type_version", Entry("", ())).inline)
    if cited and defn.version and cited != defn.version:
        findings.append(Finding(
            INFO, rel,
            f"written against {type_name} {cited}; the definition is at "
            f"{defn.version}",
            "currency"))
    elif cited and not defn.version:
        findings.append(Finding(
            INFO, rel,
            f"cites {type_name} {cited}, but the definition declares no version",
            "currency"))
    return findings


def lint_type_dir(td: Path, root: Path, scope: Scope) -> list[Finding]:
    """The layout and relational checks for one ``type_definitions/`` directory."""
    findings: list[Finding] = []

    def rel(p: Path) -> str:
        try:
            return p.relative_to(root).as_posix()
        except ValueError:
            return str(p)

    for stray in sorted(td.glob("*.md")):
        findings.append(Finding(
            WARNING, rel(stray),
            "a Type Definition is a folder — the single-file shape was "
            "retired by LKF v0.0.21; expected "
            f"type_definitions/{stray.stem}/DEFINITION.md",
            "single-file-shape"))

    for folder in sorted(p for p in td.iterdir() if p.is_dir()):
        definition = folder / "DEFINITION.md"
        if not definition.is_file():
            findings.append(Finding(
                WARNING, rel(folder),
                "no DEFINITION.md — the one required file in a type's folder",
                "definition-missing"))
            continue
        defn, grammar = parse_definition(definition)
        findings.extend(Finding(g.level, rel(definition), g.message, g.kind)
                        for g in grammar)
        if defn is None or not defn.defines:
            continue  # the generic pass reports the missing `defines`
        if defn.defines.rsplit("/", 1)[-1] != folder.name:
            findings.append(Finding(
                WARNING, rel(definition),
                f"the folder is `{folder.name}` but the definition defines "
                f"`{defn.defines}` — a folder is named for its type, so "
                "resolution never finds this contract",
                "folder-mismatch"))
        if not defn.version:
            findings.append(Finding(
                INFO, rel(definition),
                "declares no `version` — legal, and its documents get "
                "nothing to cite in type_version",
                "version-absent"))
        if not (folder / "CHANGELOG.md").is_file():
            findings.append(Finding(
                WARNING, rel(definition),
                "no CHANGELOG.md beside the contract — a type is a contract, "
                "so its folder SHOULD carry one",
                "changelog-missing"))
        if defn.extends:
            parent = scope.resolve(definition, defn.extends)
            if parent is None:
                findings.append(Finding(
                    WARNING, rel(definition),
                    f"extends `{defn.extends}`, which resolves to nothing "
                    "here — a broken definition",
                    "extends-broken"))
            else:
                for name, decl in sorted(defn.fields.items()):
                    inherited = scope.effective_fields(parent, definition).get(name)
                    if inherited is None:
                        continue
                    if decl.field_type and inherited.field_type and \
                            decl.field_type != inherited.field_type:
                        findings.append(Finding(
                            WARNING, rel(definition),
                            f"field `{name}` restates field_type "
                            f"`{decl.field_type}` over the parent's "
                            f"`{inherited.field_type}` — presence is the only "
                            "thing a subtype may change",
                            "inheritance"))
                    child_s = STRENGTH.get(decl.presence)
                    parent_s = STRENGTH.get(inherited.presence)
                    if child_s is not None and parent_s is not None and \
                            child_s < parent_s:
                        findings.append(Finding(
                            WARNING, rel(definition),
                            f"field `{name}` weakens presence to "
                            f"`{decl.presence}` from the parent's "
                            f"`{inherited.presence}` — strengthened, never "
                            "weakened",
                            "inheritance"))
    return findings

# ---------------------------------------------------------------------------
# the walk

SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}


def run(root: Path) -> list[Finding]:
    root = root.resolve()
    scope = Scope(root)
    findings: list[Finding] = []
    type_dirs: list[Path] = []
    docs: list[Path] = []
    stack = [root]
    while stack:
        directory = stack.pop()
        for child in sorted(directory.iterdir(), reverse=True):
            if child.is_dir():
                if child.name in SKIP_DIRS:
                    continue
                if child.name == "type_definitions":
                    type_dirs.append(child)
                stack.append(child)
            elif child.suffix == ".md":
                docs.append(child)
    for td in sorted(type_dirs):
        findings.extend(lint_type_dir(td, root, scope))
    for doc in sorted(docs):
        try:
            rel = doc.relative_to(root).as_posix()
        except ValueError:
            rel = str(doc)
        findings.extend(validate_document(doc, rel, scope))
    return findings

# ---------------------------------------------------------------------------
# the command

USAGE = """Validate Documents against the Type Definitions they cite.

  luma-foreman lint [<path>]         lint a tree (default: the current directory)
  luma-foreman lint --strict         escalate real violations to errors
  luma-foreman lint --verbose        also list info-level findings

An implementation of the LKF spec's Validation table: validation never rejects
by default, --strict escalates only what the table says it may, and an unknown
field or an undefined type is never reported at all. type_version currency is
info in every mode — old-but-labelled is the system working.

Exit codes: 0 nothing at error level, 1 errors (--strict only), 2 could not run."""


def main(argv: list[str]) -> int:
    strict = False
    verbose = False
    target = Path.cwd()
    for arg in argv:
        if arg == "--strict":
            strict = True
        elif arg in ("-v", "--verbose"):
            verbose = True
        elif arg in ("-h", "--help"):
            print(USAGE)
            return 0
        elif arg.startswith("-"):
            print(f"luma-foreman lint: unknown flag: {arg}", file=sys.stderr)
            return 2
        else:
            target = Path(arg)
    if not target.is_dir():
        print(f"luma-foreman lint: not a directory: {target}", file=sys.stderr)
        return 2

    findings = run(target)
    if strict:
        findings = [
            Finding(ERROR, f.path, f.message, f.kind)
            if f.level == WARNING and f.kind in ESCALATES else f
            for f in findings
        ]

    counts = {ERROR: 0, WARNING: 0, INFO: 0}
    shown = 0
    for f in sorted(findings, key=lambda f: (f.path, f.message)):
        counts[f.level] += 1
        if f.level == INFO and not verbose:
            continue
        print(f"{f.level:<7} {f.path}: {f.message}")
        shown += 1

    if shown:
        print()
    summary = ", ".join(f"{counts[lv]} {lv}" for lv in (ERROR, WARNING, INFO)
                        if counts[lv])
    print(summary if summary else "clean — every checked claim holds")
    if counts[INFO] and not verbose:
        print("info is hidden by default — --verbose lists it")
    return 1 if counts[ERROR] else 0
