# Changelog

Notable changes to luma-foreman, newest first. Behaviour-affecting changes only;
wording, refactors and test-only edits are omitted. Commit messages carry the
full rationale — this file is for seeing what changed at a glance.

Format follows [Keep a Changelog](https://keepachangelog.com); versions follow
[semantic versioning](https://semver.org).

## [Unreleased]

Everything so far. Foreman has not cut a release; `main` is the current state.

### Added

- **A `bundles` rule for `inspect`** — structural checks on Knowledge Bundles.
  A bundle with a dangling link, an unquoted frontmatter wikilink, or a template
  carrying live frontmatter is *still conformant*: the format tolerates all
  three by design and never rejects, so the bundle publishes cleanly and every
  adopter copies the defect. This closes the gap between legal and correct on
  the side that rejects.
  - Catches a missing `version`, frontmatter without a `type`, an `entry_point`
    resolving to nothing, unresolved wikilinks, links escaping the bundle,
    missing attachments, and assets nothing links to.
  - The **unquoted frontmatter wikilink** is the one worth having: `[[…]]` is
    YAML flow-sequence syntax, so unquoted it parses as a nested array rather
    than a string. No parser complains, and the link silently never resolves.
  - Fenced blocks and inline code are stripped before checking links, because
    documents explaining wikilink syntax are full of illustrative ones. A
    checker that cries wolf gets switched off, which protects nothing.
  - **Structural checks only.** Directory conventions, workflow naming and
    version discipline are an organization's opinions, arrive by adoption, and
    are not compiled in — foreman enforces standards it does not decide.
  - Skips with a reason when no bundle is present, since a skipped check is
    never a pass.

- **`luma-foreman policy`** — per-project control over what Claude Code may do,
  changed by command rather than by editing a hook. Claude Code's own permission
  rules are global; this adds a per-project layer, so loosening a rule for one
  repository does not loosen it everywhere.
  - Values are Claude Code's own vocabulary — `allow`, `ask`, `deny` — plus
    `always` for bypass-proof gating, and refinements `trusted` (ssh) and `safe`
    (curl/wget).
  - Policy resolves per key: project, then a global fallback, then built-in
    defaults. Projects are keyed by repository root, slugged the way Claude Code
    names `~/.claude/projects`.
  - `policy install` writes the gate and **prints** the `settings.json` changes
    rather than making them, following `pre-commit install`: a tool writes
    freely into the directory it owns and never silently edits the user's.
  - `policy doctor` checks the gate actually works, not merely that it is wired
    up — a gate can be installed, connected, and silently returning nothing.
  - `--json` on `policy`, `keys` and `doctor`.
- **`luma-foreman inspect`** — checks a repository against the baseline and
  reports where it falls short. Exit codes: 0 nothing found, 1 findings, 2 could
  not run.
  - **identity** rule — machine-derived author identities, malformed addresses,
    home directory paths in tracked content. Detected by *shape*, so it needs no
    configuration and runs in a bare clone.
  - **secrets** rule — provider-issued credentials in tracked content, and files
    that normally hold them. Findings never contain the secret.
  - A check that cannot run is reported as **skipped**, never as a pass.

- **`tests/run` runs `inspect` against this repository** and fails if it finds
  anything. A tool that enforces a standard and does not meet it is not
  credible.

### Changed

- **The permission gate was ported from shell to Python**, with the existing
  test suite as the acceptance criterion — an interface contract survives a
  language rewrite where an implementation test does not. Foreman is Python
  3.11+ with no dependencies beyond the standard library and git.

### Fixed

- The gate **fails closed**. An earlier shell implementation parsed its input
  with `jq`; on a machine without `jq` it fell through to "no opinion", so
  `sudo rm -rf /` went from prompting to unguarded, silently.
- A malformed policy file can no longer *loosen* the gate. Line-by-line parsing
  honoured whichever lines happened to parse; real TOML parsing rejects the file
  whole and falls back to defaults, so a broken policy can only be stricter.
- A `deny` rule no longer blocks its own undo. With `curl = deny`, the string
  "curl" inside `luma-foreman policy reset curl` matched the curl rule and
  refused the one command that would lift it.
- Configuration and program files are separate, per XDG. Clearing
  `~/.config/luma-foreman` no longer deletes the gate — which would have failed
  it open, since a missing hook is a non-blocking error in Claude Code.
