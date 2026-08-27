"""The rules Inspect knows about.

A dict, not a configuration format. Nothing yet wants configuring: every rule is
shape-based, every rule runs everywhere, and none has a knob worth exposing. The
moment one needs per-project tuning is the moment to design a schema — and not
before, because a schema drawn around today's rules would be wrong in ways
nobody can see yet.
"""

from __future__ import annotations

from pathlib import Path

from .finding import Result
from .rules import adoption, bundles, identity, secrets, vocabulary

RULES = {
    identity.RULE: identity.check,
    secrets.RULE: secrets.check,
    bundles.RULE: bundles.check,
    adoption.RULE: adoption.check,
    vocabulary.RULE: vocabulary.check,
}


def run(repo: Path, only: str | None = None) -> Result:
    result = Result()
    for name, check in RULES.items():
        if only and name != only:
            continue
        result.extend(check(repo))
    return result
