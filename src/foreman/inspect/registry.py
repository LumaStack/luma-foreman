"""The rules Inspect knows about.

A dict, not a configuration format. Two rules in, nothing yet wants configuring:
both are shape-based, both run everywhere, and neither has a knob worth exposing.
The moment one needs per-project tuning is the moment to design a schema — and
not before, because a schema drawn around today's two rules would be wrong in
ways nobody can see yet.
"""

from __future__ import annotations

from pathlib import Path

from .finding import Result
from .rules import bundles, identity, secrets

RULES = {
    identity.RULE: identity.check,
    secrets.RULE: secrets.check,
    bundles.RULE: bundles.check,
}


def run(repo: Path, only: str | None = None) -> Result:
    result = Result()
    for name, check in RULES.items():
        if only and name != only:
            continue
        result.extend(check(repo))
    return result
