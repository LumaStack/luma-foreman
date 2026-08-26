"""Rendering an inspection.

The summary line always states what ran AND what was skipped, so an inspection
can never read as clean when it was not. That is the whole contract: silence
about a check that did not run is the failure mode this is built to avoid.
"""

from __future__ import annotations

import json
import sys

from .finding import Result

MARK = {"high": "HIGH  ", "medium": "MEDIUM", "low": "LOW   "}


def render(result: Result, as_json: bool) -> int:
    if as_json:
        json.dump(
            {
                "findings": [f.as_dict() for f in result.sorted_findings()],
                "notices": [n.as_dict() for n in result.notices],
                "skipped": [s.as_dict() for s in result.skipped],
                "ran": result.ran,
                "summary": {
                    "findings": len(result.findings),
                    "notices": len(result.notices),
                    "skipped": len(result.skipped),
                    "checks_ran": len(result.ran),
                },
            },
            sys.stdout,
            indent=2,
        )
        print()
        return 1 if result.findings else 0

    for finding in result.sorted_findings():
        print(f"{MARK[finding.severity]}  {finding.summary}")
        print(f"          rule={finding.rule} surface={finding.surface}")
        for line in finding.evidence:
            print(f"            {line}")
        if finding.remedy:
            print(f"          {finding.remedy}")
        print()

    for notice in result.notices:
        print(f"NOTICE    {notice.summary}")
        print(f"          rule={notice.rule}")
        for line in notice.evidence:
            print(f"            {line}")
        if notice.remedy:
            print(f"          {notice.remedy}")
        print()

    for skip in result.skipped:
        print(f"SKIPPED   {skip.rule}: {skip.reason}")
        if skip.remedy:
            print(f"          {skip.remedy}")
        print()

    checks = len(result.ran)
    print(
        f"{len(result.findings)} finding(s) and {len(result.notices)} notice(s) "
        f"from {checks} check(s) that ran; {len(result.skipped)} check(s) could "
        f"not run."
    )
    if result.notices:
        print("A notice is somebody's judgement to make, and never fails a run.")
    if result.skipped:
        print("A skipped check is not a pass.")
    return 1 if result.findings else 0
