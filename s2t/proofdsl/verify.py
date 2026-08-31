"""CLI for deterministic verification of the curated proof-gate registry."""

from __future__ import annotations

import argparse
import json

from .gates import verify_gate
from .registry import registered_gates


def verify_all() -> dict[str, object]:
    verified = [verify_gate(spec) for spec in registered_gates()]
    return {
        "status": "lcf-checked",
        "gate_count": len(verified),
        "obligation_count": sum(len(item.obligations) for item in verified),
        "gates": [item.to_dict() for item in verified],
        "certificate_sha256": {item.spec.identifier: item.sha256 for item in verified},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    print(
        json.dumps(
            verify_all(),
            ensure_ascii=False,
            indent=2 if args.pretty else None,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()