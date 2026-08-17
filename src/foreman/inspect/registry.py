"""The rules Inspect knows about.

A list, not a configuration format. There is one rule; a config schema designed
around one example would be wrong in ways nobody could yet see. The shape should
emerge from the second and third rules, not be guessed at now.
"""

from __future__ import annotations

from pathlib import Path

from .finding import Result
from .rules import identity

RULES = {
    identity.RULE: identity.check,
}


def run(repo: Path, only: str | None = None) -> Result:
    result = Result()
    for name, check in RULES.items():
        if only and name != only:
            continue
        result.extend(check(repo))
    return result
