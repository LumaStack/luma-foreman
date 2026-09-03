# Changelog

Notable changes to luma-foreman, newest first. Behaviour-affecting changes only;
wording, refactors and test-only edits are omitted. Commit messages carry the
full rationale — this file is for seeing what changed at a glance.

Format follows [Keep a Changelog](https://keepachangelog.com); versions follow
[semantic versioning](https://semver.org).

## [Unreleased]

### Added

- **`luma-foreman bundle new <name>` starts a bundle in this project.** It writes `.luma/bundles/local/<name>/BUNDLE.md` from a template and nothing else — `local/` because that is where a bundle with no published identity lives (ADR-0011), and it is the only namespace this writes into, since a name is a bundle's and a namespace is a catalog's to give. **A bundle needs no catalog to exist**, so this needs no network, no registry and no `--from`; it needs a `.luma/`, and says so when there is none.
  **It creates no directories it cannot fill.** `policy/` and `procedure/` are named in the output instead, following `init`'s rule: git will not commit an empty directory, so one made ahead of its contents exists only on the machine that ran the command — and an empty `policy/` is a question a reader has to answer about a bundle that has no policies.
  **One refusal, and it says which case it is.** An existing `BUNDLE.md` is never overwritten — that file is what makes a directory a bundle, so replacing it discards the bundle rather than the file. Written onto a directory somebody drafted by hand, it says so and names what was already there, because the template it just wrote describes none of it.
  *The description is a plain line, not a folded scalar.* `foreman.lkf` is a deliberate subset that reads `>-` as the value, so the YAML-shaped template would have shipped every new bundle announcing itself as `>-` in both generated indexes. No `published:` either — a bundle written in a project has no publish moment, which is the same fact that makes its index regenerate rather than freeze.

### Fixed

- **`get` no longer reports *no catalog* at a project that has one registered.** The refusal blamed the last resolution step it tried, `[catalog] source`, and sent an operator to `catalog add` for a catalog that was already there. Where the registry is not empty, the fault is in the ID rather than in the setup, and the message now says which: a **bare name** is not a bundle ID at all, since the ID is what carries the catalog's name; a **namespace nothing answers to** names a catalog this project does not have, which is not the same fact as having none. Both print the command per registered catalog — the last segment is the bundle's name either way, the guess `_resolve_id` already makes when it holds a single catalog — plus `catalog show` for what each publishes and `catalog add`/`--from` for a catalog that is not registered here. Both routes, because the bundle may not be in what this project already has.

## [0.1.0] - 2026-09-03

### Added

- **The CLI reports its own version — `--version`, `-V` or `version`.** `__version__` in `src/foreman/__init__.py` is the single place it is written, and the `v` stays on the tag: `git tag v0.1.0` against `__version__ = "0.1.0"`, so comparing the two is an lstrip rather than a guess about which end carries a prefix.
  Both spellings answer because both get typed, and the tests pin that all three agree — a version that varies by how it was asked is worse than none.
- **Catalogs are registered sources — `catalog add <source>`.** The model is apt's `sources.list`: register a catalog once, then `get <bundle-id>` with nothing restated — the ID starts with the catalog's name, and the registry in `.luma/config/luma-foreman.toml` (named entries under `[catalog."<name>"]`, committed) says where that name lives. See ADR-0012.
  **The name is never an argument.** `add` fetches the catalog and registers the namespace it answers — declared-beats-derived, exactly as `get` resolves it — which verifies the entry at write time instead of in a teammate's `get` next week. Same name and source again is a no-op; the same name from a different source is refused, naming the entry it would shadow. A catalog claiming `local/` is refused (ADR-0011).
  **Receipts go name-indirect.** A receipt for a registered catalog records the catalog *name* (`catalog:` subline) plus what it already pins, and the registry owns name-to-URL — a moved catalog is one config line, not every receipt going stale. A `--from` fetch from an unregistered catalog keeps its raw URL, like a hand-installed .deb. Old receipts keep working: unknown sublines were already ignored on read, so this is a behavior change, not a format change.
  **Resolution order for `get`:** explicit `--from`, then the registry by prefix-match on the bundle ID, then the receipt's recorded source, then the bare `[catalog] source` default — which stays read, because a config that quietly stopped being read would fail open. The registry outranks the receipt deliberately: a moved catalog makes the registry current truth and the receipt history.
  *`catalog list` heads a registered catalog by its registered name*, still offline; `bundle show` prints `catalog` where the receipt is name-indirect; `bundle outdated` resolves names through the registry and reports a name nobody registered as unanswerable rather than guessing.

- **`inspect --rule vocabulary` reports words this project retired.** Declared as `[[retired]]` in `.luma/config/luma-foreman.toml` with what replaced each and where that was decided. **Nothing is retired by default** — a tool shipping opinions about English would be wrong everywhere at once.
  **Every hit is a notice, never a finding.** A grep cannot tell a revival from a legitimate use: *projection* has a mathematical sense, *jobs* means something real about CI, and a quotation is not a revival. So it hands over what the judgement needs — the term, the replacement, the deciding record, and the line as written — and the reader decides.
  *Exempt without being asked:* a published `## Version` history, a `CHANGELOG.md`, the config that declares the term, a vendored bundle, and the record that retired the word. A rule that cannot express **everywhere except history** gets switched off in a week. Anything else is listed per term in `except`.
- **`inspect` has a third outcome: a notice.** Something worth a reader's judgement that is not a defect — printed as loudly as a finding, counted separately, and never part of the exit code. `--json` carries `notices` and a `notices` count in the summary.
  **A finding says what is wrong; a notice says what to look at.** The difference is who decides, so a notice carries more context than a finding rather than less: somebody is being asked to make a call and needs the basis for it.
  *The first one already existed as a finding.* `matches: always` was reported at `low` with a remedy that said it was *"worth confirming rather than fixing"* — a notice by its own words, exiting 1 over a legal and deliberate choice.
- **`luma-foreman init` is built.** It creates `.luma/PROJECT.md` and `.luma/config/luma-foreman.toml`, and nothing else — `bundles/` arrives on the first `get` and `records/` on the first decision or audit. Both files have contents on the day they are written, which matters because git will not commit an empty directory: one created ahead of use exists only on the machine that ran `init`.
  **`--catalog <source>` records where bundles come from**, so the next command is `get <namespace>/<bundle>` with no `--from`.
  **It is idempotent and never destructive.** A second run adds whatever is missing and leaves every existing file exactly as it is — including an edited descriptor. Refusing would make somebody do by hand the work the refusal had just finished diagnosing.
  *`migrate-into-luma` is named only when there is something to migrate*, by looking for `DECISIONS.md`, `docs/DECISIONS.md`, `docs/decisions/` or `.records/` — the same places `record-decision` searches. A standing pointer to a migration workflow is noise in the common case.
  **The config carries overrides and as little else as possible.** A value written there is one an upgrade cannot move, so defaults stay in the tool. Nothing is shipped commented-out either: a commented default is a behavioural override one keystroke away, frozen at whatever it said the day `init` ran. What is settable is deliberately not listed: where documentation for it exists, the header should point at that rather than copy it. The single exception is `[catalog] source`, which is written out because it has no default at all.
  **It refuses once.** Outside a git repository it writes nothing: a descriptor describing a repository, placed where there is not one, is wrong in a way nobody notices until it travels.
  *No `.gitignore` entry, deliberately.* `.luma/` is committed in full, and a project whose `.luma/` differs between two machines is two projects. The output says so.
  Follows `luma-layout`'s `initialize-luma`, which is the specification.

- **`luma-foreman bundle` and `luma-foreman catalog` — two nouns that only report.** `bundle list` prints what this project holds and the shape each copy is in; `bundle show <name>` prints one bundle's receipt and the Documents inside it; `catalog list` prints where knowledge comes from; `catalog show <name>` prints what a catalog publishes.
  **The inventory always existed and nothing read it.** `adopted.toml` has carried the version, source, commit and checksum since adoption was built. `outdated` came closest to printing it but needs a network and answers a different question, and the command whose name sounded right — `adopt --list` — returned the *catalog's* contents.
  *Only `catalog show` reaches the network.* The other three read committed state, so they hold in a bare clone — the guarantee `inspect` already carries.
  **The set of catalogs is derived, not registered.** There is no `catalog add`: a catalog is an argument, and `list` reads the distinct sources in `adopted.toml` plus `[catalog] source` if one is set.

- **`luma-foreman apply --explain`** prints what each Document derives to, beside what produced it. The class names live here rather than in anybody's head — a derived column printed next to its input is a lookup table, not a glossary.
- **`inspect` reports any Document still using `applies_to`.** The migration's own ledger: *what is left* is a command rather than a checklist, and it goes quiet when the work is done.

- **`luma-foreman get` — a bundle from a catalog becomes part of this project.** It copies into `.luma/bundles/<org>/<name>/` and writes `adopted.toml` with the version, the catalog's origin, the commit it came from and a checksum of exactly what landed. Nothing is resolved and nothing is fetched later: bundles depend on nothing, which is what keeps adoption a directory copy rather than an install.
  **The copy is committed, and that is the difference from a package cache.** A fresh clone with no network reproduces the project, because the knowledge is in the repository rather than in a cache directory a teammate does not have.
  `--from` takes a local checkout or a git URL; a URL is cloned into `~/.cache/luma/catalogs/`, which is genuinely cache — deleting it loses nothing, since everything adopted from it is already committed. With no `--from`, `[catalog] source` in `.luma/config/luma-foreman.toml` is used.
  **Two refusals rather than an overwrite.** A vendored copy that has been edited locally is never silently replaced — that is somebody's work, and the message says where the change should go instead. A bundle with no version cannot be adopted at all, because nothing about it could be honestly reported afterwards.

- **`luma-foreman apply` — adopted knowledge reaches an agent without anybody pointing at it.** Two outputs: one Claude Code skill per `workflow`, and one managed block in `CLAUDE.md` indexing everything adopted.
  **Thin adapters, never copies.** A generated skill carries the harness-specific frontmatter, a pointer to the real document under `.luma/`, and the standing context that document assumes. It deliberately does not carry the workflow body — a copy is a second source of truth, and it would charge every session for content meant to load only when the work matched.
  **The index is the part that closes the gap.** `preload: mandatory` documents are hoisted into a *read these first* section; everything else is one line saying what it is. Make existence cheap and content expensive.
  Only the region between the `luma:begin` and `luma:end` markers in `CLAUDE.md` is touched, so a hand-written file keeps everything else. `--check` reports staleness and writes nothing, for continuous integration.

- **`inspect` gained an `adoption` rule** covering the three ways an adopted bundle stops being what was adopted: **edited** in place, **missing** from disk, and **unapplied** — present, checksummed, reported clean, and never shown to an agent. The third is the one nothing else would surface, because it looks correct from every angle.
  It cannot say whether a newer version exists: that needs the catalog, and `inspect` runs in a bare clone with no network.


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

- **`get` refuses a bundle whose ID is already here from a different catalog.** It compared ID and version only, so the same name at the same version from a different origin reported `nothing to do` — with the content it had been asked for left unfetched, and the run exiting 0.
  A change of origin is a change of **lineage**, not an upgrade. The refusal names both sources; `--force` takes it and reports `switched to <version> from another catalog`, because the version may not have moved at all.
  *Derivation makes this unreachable by accident* — two catalogs can only share an ID by both declaring the same namespace. This catches the deliberate case and the misconfigured one, and both are somebody's decision rather than a tool's.
- **A catalog's namespace derives from where it lives.** The last two path segments of the source, `.git` stripped, lowercased — `https://github.com/LumaStack/luma-catalog.git` becomes `lumastack/luma-catalog`. A `namespace:` in `CATALOG.md` still wins; most catalogs no longer need one.
  **This is what makes a fork safe.** A fork lives somewhere else, so it is named something else without anybody arranging it, and its bundles sit beside the originals in one project instead of colliding with them. Only a catalog that declares a namespace can be impersonated by a fork, and that catalog chose to be nameable.
  **No hosting is assumed.** Any URL with a path derives, a LAN git server included, and a local checkout resolves through its `origin` so `--from ../luma-catalog` gives the same namespace as the URL it was cloned from. A plain directory with no remote derives nothing and must either declare a namespace or be given one at the call site.
  *A namespace may now be any number of segments.* `lumastack/luma-catalog/widgets` is one bundle, not a nested one — the name is the last segment and the namespace is everything before it.
- **The foreman config is `.luma/config/luma-foreman.toml`**, named for the binary rather than truncated to `foreman.toml`. Nothing has ever written the old name, so nothing reads it.
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

- **`bundles` findings against a vendored copy say to fix it upstream.** Every remedy in that rule assumed you own the bundle, which is the one thing you must not do to an adopted one — the next `adopt` discards the fix and upstream never hears that anybody wanted it. Reporting the defect is still right; you are the one carrying it.
- **The frontmatter subset parser moved to `foreman/lkf.py`.** `adopt` needed the same reader `inspect` had, and a tool growing its own second parser is a known failure being reproduced locally rather than a new one.

- **`luma-foreman policy` is now `luma-foreman agent-permissions`.** `policy` became a built-in type in the knowledge format — *a course of action adopted, kept as standing context* — and the command means something else entirely: which tool calls an agent may make in this repository. Two meanings of one word in one ecosystem, close enough that *"where is the policy?"* had two correct answers.
  `agent-permissions` rather than `permissions` because *permissions* is among the most overloaded words in computing — file modes, repository access, OAuth scopes — and because it leaves `agent` free for a command group.
  **The gating patterns were the dangerous part.** `CLI_WRITE` and `CLI_INVOCATION` recognise an invocation of this command *in order to gate it*, so a pattern that no longer matched its own name would have failed **open** and reported nothing. Tests for the new name were written before the rename and eight of them failed first, proving it.
  Also renamed: the module to `foreman/agent_permissions/`, the tests, and `docs/claude-agent-permissions.md`. `permission-gate.sh` keeps its name — the gate is the mechanism, permissions are the thing.
  *Migration:* the global file is now `permissions.toml`. An existing `policy.toml` is still read when the new name is absent, because a permission file that silently stops being read fails open too. Writes go to the new name, so the first change migrates it.


- **Machine-local directories nest under the organization: `~/.config/luma/luma-foreman/`**, and likewise under `~/.local/share/` and `~/.cache/`. The second segment is the repository name exactly, so a directory maps to a repository with nothing to translate.
  This reverses an earlier decision that rested on two claims which did not survive checking. The XDG specification does **not** mandate a flat `<application>/` — it says `$XDG_CONFIG_HOME/subdir/` and leaves depth to the application, so both shapes conform. And *"a path reading `luma/foreman` implies a suite the user may never install"* was true when foreman stood alone; there is now a catalog, a headquarters, a format, and shared configuration anticipated in the same document.
  What decides it is that a rule covering every tool must be writable once. The deny rules are now `Edit(~/.config/luma/**)` and `Edit(~/.local/share/luma/**)` — **one entry per directory, no wildcard, and no edit when a second tool arrives.** The organization directory is what matches, so repository names are free: a tool called `atlas` is covered by the same rule. The flat layout needed one entry per application or a `luma-*` wildcard, and that wildcard held only while every tool happened to be named `luma-something`.
  It matters because this rule **fails open**: a pattern matching nothing produces no error, and the first sign would be an agent editing the policy that governs it.
  *Migration:* the previous `~/.config/luma-foreman/` and `~/.local/share/luma-foreman/` are reported by `policy doctor` as legacy directories and are **not** deleted — `settings.json` may still point into one, and removing it before the wiring moves would leave a session unguarded. Re-run `policy install` and update `settings.json`, then remove the old directories by hand.


- **The permission gate was ported from shell to Python**, with the existing
  test suite as the acceptance criterion — an interface contract survives a
  language rewrite where an implementation test does not. Foreman is Python
  3.11+ with no dependencies beyond the standard library and git.

### Fixed

- **`agent-permissions install` left retired gate modules on disk.** It wrote the current payload and never removed files that had dropped out of it, and `status()` could not notice because it only compares files it knows about — so it reported *already current* while a stale copy sat beside the real one. That is not untidiness: every file under `gate/foreman/` is a working piece of a gate, so an abandoned `gate.py` is **an older set of matching rules, still present and still runnable.** The rename below left exactly that on a real machine. Pruning is scoped to `gate/foreman/` and to `.py`, because it deletes files and must only touch a directory foreman entirely owns.

- **`policy install` printed a deny rule that did not match what it installs.** The help text told users to add `Edit(~/.config/luma/**)` while the snippet emitted `Edit(~/.config/luma-foreman/**)`. Fixed by the move above, which makes both correct.
- **`policy doctor` told you to delete a legacy directory before the wiring had moved**, contradicting the migration rule then in `docs/standards.md`, now in the adopted `luma-config` bundle — the old location may still be referenced by `settings.json`, and removing it first leaves the session unguarded. It now gives the order: install, apply the printed settings changes, then delete.
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

[Unreleased]: https://github.com/LumaStack/luma-foreman/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/LumaStack/luma-foreman/releases/tag/v0.1.0
