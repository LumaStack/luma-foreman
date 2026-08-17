#!/usr/bin/env python3
"""Executable entry for the PreToolUse hook, runnable straight from a checkout.

Measured at ~23ms per call against the shell implementation's ~21ms. The two
milliseconds buy: failing closed instead of open, no dependency on jq, real TOML
parsing so a malformed policy cannot partially apply, and one implementation of
the project-slug logic instead of two kept in sync by hand.

Startup flags were tried and dropped: -S -E measured within noise of plain
python3, and are not worth a non-portable `env -S` shebang.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from foreman.policy.gate import main  # noqa: E402

raise SystemExit(main())
