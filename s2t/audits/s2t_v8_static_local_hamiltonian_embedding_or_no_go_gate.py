#!/usr/bin/env python3
"""Audit the static minimal-carrier Bloch-logarithm obstruction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_static_local_hamiltonian_embedding_or_no_go_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_static_local_hamiltonian_embedding_no_go import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert (
        certificate.active_winding,
        certificate.spectator_winding,
        certificate.determinant_winding,
    ) == (-1, 1, 0)
    no_go = certificate.static_no_go_theorem.proposition.data
    assert no_go["contradiction"] is True
    assert no_go["exact_static_hamiltonian_exists"] is False
    boundary = certificate.carrier_boundary_theorem.proposition.data
    assert boundary["interacting_static_hamiltonian_excluded"] is False
    assert boundary["clock_augmented_static_hamiltonian_excluded"] is False

    registry = verify_all()
    gate = next(
        item
        for item in registry["gates"]
        if item["identifier"]
        == "version8_static_local_hamiltonian_embedding_or_no_go_gate"
    )
    assert len(gate["obligations"]) == 3
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "target": {
            "bloch_unitary": "diag(exp(-ik),exp(+ik))",
            "active_winding": -1,
            "spectator_winding": 1,
            "determinant_winding": 0,
            "gnvw_index": 1,
        },
        "assumed_static_class": {
            "translation_invariant": True,
            "finite_range": True,
            "number_preserving": True,
            "carrier": "minimal active-plus-spectator two-chain single-excitation sector",
            "bloch_hamiltonian": "continuous periodic Hermitian trigonometric polynomial",
        },
        "no_go": {
            "periodic_scalar_log_winding": 0,
            "target_eigenchannel_windings": [-1, 1],
            "continuous_periodic_static_logarithm": False,
            "exact_static_hamiltonian_in_assumed_class": False,
            "residual": "winding mismatch",
        },
        "scope_boundary": {
            "piecewise_local_floquet_remains_valid": True,
            "general_interacting_static_hamiltonian_excluded": False,
            "clock_augmented_static_hamiltonian_excluded": False,
            "next_gate": "version8_clock_augmented_static_hamiltonian_conveyor_gate",
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()