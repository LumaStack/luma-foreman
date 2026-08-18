# Changelog

Notable changes to luma-foreman, newest first. Behaviour-affecting changes only;
wording, refactors and test-only edits are omitted. Commit messages carry the
full rationale — this file is for seeing what changed at a glance.

Format follows [Keep a Changelog](https://keepachangelog.com).

## [Unreleased]

Everything so far. Foreman has not cut a release; `main` is the current state.

### Added

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

### Notes

- Written in Python 3.11+; no dependencies beyond the standard library and git.
  The permission gate was ported from shell, with the existing test suite as the
  acceptance criterion.
- `tests/run` runs `inspect` against this repository and fails if it finds
  anything. A tool that enforces a standard and does not meet it is not
  credible.
