#!/usr/bin/env python3
"""Python round-trip conformance for the decision fixtures.

For every fixture in ./fixtures/, parses via overturo.models.parse_decision
and asserts the OverturoDecision-specific fields round-trip unchanged.
Passthrough fields (iss, oap_ver, etc.) are not part of the contract — the
corpus is pre-stripped to OverturoDecision-only.

Run: python3 test_corpus_roundtrip.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

# Standalone-load decision.py without triggering httpx import via __init__.
import importlib.util

HERE = Path(__file__).parent
DECISION_PATH = HERE.parent.parent / "overturo-py" / "src" / "overturo" / "models.py"
FIXTURES = HERE / "fixtures"

spec = importlib.util.spec_from_file_location("models", str(DECISION_PATH))
decision_mod = importlib.util.module_from_spec(spec)
# Register in sys.modules BEFORE exec — Python 3.14's dataclass needs to
# resolve cls.__module__ to a registered module to inspect KW_ONLY etc.
sys.modules["models"] = decision_mod
spec.loader.exec_module(decision_mod)
parse_decision = decision_mod.parse_decision

# OverturoDecision-specific fields the contract pins.
PINNED_FIELDS = [
    "decision",
    "mode",
    "request_id",
    "overturo_decision_schema_version",
    "reason_code",
    "denial_category",
    "cascade_step",
    "failed_bound",
    "decision_latency_ms",
    "chronicle_id",
]


def assert_roundtrip(fixture_path: Path) -> None:
    original = json.loads(fixture_path.read_text())
    parsed = parse_decision(original)
    re_serialized = asdict(parsed)
    for key in PINNED_FIELDS:
        expected = original.get(key)
        actual = re_serialized.get(key)
        assert expected == actual, (
            f"{fixture_path.name}: field {key!r} mismatch — "
            f"original={expected!r} parsed={actual!r}"
        )
    # block_invocations: count + ascending position
    orig_inv = original.get("block_invocations", []) or []
    parsed_inv = re_serialized.get("block_invocations", []) or []
    assert len(orig_inv) == len(parsed_inv), (
        f"{fixture_path.name}: block_invocations length "
        f"original={len(orig_inv)} parsed={len(parsed_inv)}"
    )
    for i, (o, p) in enumerate(zip(orig_inv, parsed_inv)):
        for k in ("position", "block_slug", "decision", "latency_ms", "evaluator_class"):
            assert o.get(k) == p.get(k), (
                f"{fixture_path.name}: block_invocations[{i}].{k} mismatch — "
                f"original={o.get(k)!r} parsed={p.get(k)!r}"
            )


def main() -> int:
    files = sorted(FIXTURES.glob("*.json"))
    if not files:
        print(f"NO FIXTURES FOUND under {FIXTURES}", file=sys.stderr)
        return 2
    failures: list[str] = []
    for f in files:
        try:
            assert_roundtrip(f)
            print(f"  OK  {f.name}")
        except AssertionError as e:
            failures.append(str(e))
            print(f"  FAIL  {f.name}: {e}")
    if failures:
        print(f"\n{len(failures)} of {len(files)} fixtures failed")
        return 1
    print(f"\n{len(files)} fixtures round-tripped OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
