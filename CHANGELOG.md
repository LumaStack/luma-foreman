# Changelog

Notable changes to luma-foreman, newest first. Behaviour-affecting changes only;
wording, refactors and test-only edits are omitted. Commit messages carry the
full rationale — this file is for seeing what changed at a glance.

Format follows [Keep a Changelog](https://keepachangelog.com); versions follow
[semantic versioning](https://semver.org).

## [Unreleased]

### Added
- **`luma-foreman init` is built.** It creates `.luma/PROJECT.md` and `.luma/records/`, and nothing else — `bundles/` arrives on the first `get`, `config/` when a setting needs one. An empty directory is a question a reader has to answer, so none is created ahead of having contents.
  **It refuses twice.** Where `.luma/` already exists it stops and points at `migrate-into-luma`, because whether the answer is a migration or one missing directory depends on what is in there and this command cannot tell. Outside a git repository it stops too: a descriptor describing a repository, written where there is not one, is wrong in a way nobody notices until it travels.
  *No `.gitignore` entry, deliberately.* `.luma/` is committed in full, and a project whose `.luma/` differs between two machines is two projects. The output says so, and says that git will not track `records/` while it is empty.
  Follows `luma/luma-layout`'s `initialize-luma`, which is the specification.

### Added
- **`luma-foreman bundle` and `luma-foreman catalog` — two nouns that only report.** `bundle list` prints what this project holds and the shape each copy is in; `bundle show <name>` prints one bundle's receipt and the Documents inside it; `catalog list` prints where knowledge comes from; `catalog show <name>` prints what a catalog publishes.
  **The inventory always existed and nothing read it.** `adopted.toml` has carried the version, source, commit and checksum since adoption was built. `outdated` came closest to printing it but needs a network and answers a different question, and the command whose name sounded right — `adopt --list` — returned the *catalog's* contents.
  *Only `catalog show` reaches the network.* The other three read committed state, so they hold in a bare clone — the guarantee `inspect` already carries.
  **The set of catalogs is derived, not registered.** There is no `catalog add`: a catalog is an argument, and `list` reads the distinct sources in `adopted.toml` plus `[catalog] source` if one is set.

### Changed
- **The commands are named for what they do, not for the foreman metaphor.** `adopt` is now **`get`**, `outfit` is now **`apply`**, `bootstrap` is now **`init`**, `outdated` is now **`bundle outdated`**, `adopt --list` is now **`catalog show <name>`**, and `refit` is gone. `jobs` was already renamed to `commands` in the help text.
  **The old names are a hard error, not an alias.** `luma-foreman adopt` prints `unknown command: adopt (renamed to: get)` and exits 1. An alias would let the catalog's own documentation keep working while still being wrong, which removes the pressure to ever correct it — see ADR-0003.
  *`refit` says `removed, with no replacement`* rather than reading as a typo. Its three checks already exist as `outdated`, `inspect --rule adoption` and `apply --check`, and merging them would cross the offline/online line that keeps `inspect` runnable in a bare clone — see ADR-0004.

- **`applies_to` is read as `matches`, and the default reverses.** The format renamed the field in `v0.0.14`, and the meaning of *saying nothing* changed with it: a Document that declares no `matches` is now **available on request** rather than loaded into every session. `matches: always` is the only route to being present up front.
  **The old default made the lazy path the expensive one.** Forgetting a field bought a permanent seat in every adopter's context, and it failed in the direction that cannot be recovered from — under-delivering is fixable, over-delivering is a token bomb. Asking for the cost out loud makes it impossible by accident, which beats making it visible in a low finding somebody has to run a tool to read.
  **The type no longer decides anything.** It used to break the tie for a Document with no trigger — `policy` meant loaded-always, anything else meant findable. With the default reversed there is no tie to break.
  *`applies_to` is still read where `matches` is absent*, so upgrading the tools cannot silently drop every trigger a repository declared, and `inspect` reports each use. That fallback is scheduled for removal.

- **`always` is a value of `matches`, not a trigger kind.** `matches: always`, never an entry inside the list — where it could sit beside a condition that OR semantics rendered dead.
  It was previously in `TRIGGER_KINDS` and unwritable: `matches: always` and `- always:` were silently discarded, and `- always: true` parsed into a trigger that classed the Document as *cheap*. A rule declaring itself ever-present was the one rule that would not be there.

- **`standing` is now `always-on`**, in output, in generated files, and in the reasoning. A reader took *standing* to mean *left over from before* — which is the opposite of what it meant, and the fifth name this slot has worn.

- **The index lists every policy and workflow, not only the ones that match something.** A rule nobody can see governs nothing, and with the default reversed a policy that matches nothing would otherwise have vanished from `CLAUDE.md` entirely — turning a cost saving into silent absence. Background under `concepts/` stays unannounced on the format's own reasoning: it does not act, and is reached through the things that do.

### Added
- **`luma-foreman apply --explain`** prints what each Document derives to, beside what produced it. The class names live here rather than in anybody's head — a derived column printed next to its input is a lookup table, not a glossary.
- **`inspect` reports any Document still using `applies_to`.** The migration's own ledger: *what is left* is a command rather than a checklist, and it goes quiet when the work is done.

- **`luma-foreman get` — a bundle from a catalog becomes part of this project.** It copies into `.luma/bundles/<org>/<name>/` and writes `adopted.toml` with the version, the catalog's origin, the commit it came from and a checksum of exactly what landed. Nothing is resolved and nothing is fetched later: bundles depend on nothing, which is what keeps adoption a directory copy rather than an install.
  **The copy is committed, and that is the difference from a package cache.** A fresh clone with no network reproduces the project, because the knowledge is in the repository rather than in a cache directory a teammate does not have.
  `--from` takes a local checkout or a git URL; a URL is cloned into `~/.cache/luma/catalogs/`, which is genuinely cache — deleting it loses nothing, since everything adopted from it is already committed. With no `--from`, `[catalog] source` in `.luma/config/foreman.toml` is used.
  **Two refusals rather than an overwrite.** A vendored copy that has been edited locally is never silently replaced — that is somebody's work, and the message says where the change should go instead. A bundle with no version cannot be adopted at all, because nothing about it could be honestly reported afterwards.

- **`luma-foreman apply` — adopted knowledge reaches an agent without anybody pointing at it.** Two outputs: one Claude Code skill per `workflow`, and one managed block in `CLAUDE.md` indexing everything adopted.
  **Thin adapters, never copies.** A generated skill carries the harness-specific frontmatter, a pointer to the real document under `.luma/`, and the standing context that document assumes. It deliberately does not carry the workflow body — a copy is a second source of truth, and it would charge every session for content meant to load only when the work matched.
  **The index is the part that closes the gap.** `preload: mandatory` documents are hoisted into a *read these first* section; everything else is one line saying what it is. Make existence cheap and content expensive.
  Only the region between the `luma:begin` and `luma:end` markers in `CLAUDE.md` is touched, so a hand-written file keeps everything else. `--check` reports staleness and writes nothing, for continuous integration.

- **`inspect` gained an `adoption` rule** covering the three ways an adopted bundle stops being what was adopted: **edited** in place, **missing** from disk, and **unapplied** — present, checksummed, reported clean, and never shown to an agent. The third is the one nothing else would surface, because it looks correct from every angle.
  It cannot say whether a newer version exists: that needs the catalog, and `inspect` runs in a bare clone with no network.

### Changed
- **`bundles` findings against a vendored copy say to fix it upstream.** Every remedy in that rule assumed you own the bundle, which is the one thing you must not do to an adopted one — the next `adopt` discards the fix and upstream never hears that anybody wanted it. Reporting the defect is still right; you are the one carrying it.
- **The frontmatter subset parser moved to `foreman/lkf.py`.** `adopt` needed the same reader `inspect` had, and a tool growing its own second parser is a known failure being reproduced locally rather than a new one.

### Fixed
- **`agent-permissions install` left retired gate modules on disk.** It wrote the current payload and never removed files that had dropped out of it, and `status()` could not notice because it only compares files it knows about — so it reported *already current* while a stale copy sat beside the real one. That is not untidiness: every file under `gate/foreman/` is a working piece of a gate, so an abandoned `gate.py` is **an older set of matching rules, still present and still runnable.** The rename below left exactly that on a real machine. Pruning is scoped to `gate/foreman/` and to `.py`, because it deletes files and must only touch a directory foreman entirely owns.

### Changed
- **`luma-foreman policy` is now `luma-foreman agent-permissions`.** `policy` became a built-in type in the knowledge format — *a course of action adopted, kept as standing context* — and the command means something else entirely: which tool calls an agent may make in this repository. Two meanings of one word in one ecosystem, close enough that *"where is the policy?"* had two correct answers.
  `agent-permissions` rather than `permissions` because *permissions* is among the most overloaded words in computing — file modes, repository access, OAuth scopes — and because it leaves `agent` free for a command group.
  **The gating patterns were the dangerous part.** `CLI_WRITE` and `CLI_INVOCATION` recognise an invocation of this command *in order to gate it*, so a pattern that no longer matched its own name would have failed **open** and reported nothing. Tests for the new name were written before the rename and eight of them failed first, proving it.
  Also renamed: the module to `foreman/agent_permissions/`, the tests, and `docs/claude-agent-permissions.md`. `permission-gate.sh` keeps its name — the gate is the mechanism, permissions are the thing.
  *Migration:* the global file is now `permissions.toml`. An existing `policy.toml` is still read when the new name is absent, because a permission file that silently stops being read fails open too. Writes go to the new name, so the first change migrates it.


### Changed
- **Machine-local directories nest under the organization: `~/.config/luma/luma-foreman/`**, and likewise under `~/.local/share/` and `~/.cache/`. The second segment is the repository name exactly, so a directory maps to a repository with nothing to translate.
  This reverses an earlier decision that rested on two claims which did not survive checking. The XDG specification does **not** mandate a flat `<application>/` — it says `$XDG_CONFIG_HOME/subdir/` and leaves depth to the application, so both shapes conform. And *"a path reading `luma/foreman` implies a suite the user may never install"* was true when foreman stood alone; there is now a catalog, a headquarters, a format, and shared configuration anticipated in the same document.
  What decides it is that a rule covering every tool must be writable once. The deny rules are now `Edit(~/.config/luma/**)` and `Edit(~/.local/share/luma/**)` — **one entry per directory, no wildcard, and no edit when a second tool arrives.** The organization directory is what matches, so repository names are free: a tool called `atlas` is covered by the same rule. The flat layout needed one entry per application or a `luma-*` wildcard, and that wildcard held only while every tool happened to be named `luma-something`.
  It matters because this rule **fails open**: a pattern matching nothing produces no error, and the first sign would be an agent editing the policy that governs it.
  *Migration:* the previous `~/.config/luma-foreman/` and `~/.local/share/luma-foreman/` are reported by `policy doctor` as legacy directories and are **not** deleted — `settings.json` may still point into one, and removing it before the wiring moves would leave a session unguarded. Re-run `policy install` and update `settings.json`, then remove the old directories by hand.

### Fixed
- **`policy install` printed a deny rule that did not match what it installs.** The help text told users to add `Edit(~/.config/luma/**)` while the snippet emitted `Edit(~/.config/luma-foreman/**)`. Fixed by the move above, which makes both correct.
- **`policy doctor` told you to delete a legacy directory before the wiring had moved**, contradicting the migration rule in `docs/standards.md` — the old location may still be referenced by `settings.json`, and removing it first leaves the session unguarded. It now gives the order: install, apply the printed settings changes, then delete.


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
  - **Bundles are found by asking git, not by walking the filesystem.** A
    gitignored worktree under `.claude/worktrees/` holds a whole second
    checkout, so a walk reports every bundle twice and shows an agent findings
    from another agent's uncommitted work. `node_modules` and build output are
    the same problem arriving differently. Untracked-but-not-ignored bundles are
    still audited — not yet committed is not the same as not this repository's.

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
