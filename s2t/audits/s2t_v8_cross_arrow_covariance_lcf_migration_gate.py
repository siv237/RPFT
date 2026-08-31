#!/usr/bin/env python3
"""Migrate the polar cross-arrow covariance gate to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_cross_arrow_covariance_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_cross_covariance import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def matrix_strings(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(value) for value in row] for row in matrix.tolist()]


def main() -> None:
    certificate = build_certificate()
    angle_degrees = sp.N(certificate.soft_axis_angle_radians * 180 / sp.pi, 16)
    eigenvalues = [sp.N(value, 16) for value in certificate.pair_eigenvalues]
    assert certificate.repetition_theorem.proposition.data["shape"] == [12, 12]
    assert certificate.decoupling_theorem.proposition.data["shape"] == [12, 15]
    assert certificate.positivity_theorem.proposition.data[
        "distinct_eigenvalues"
    ] is True
    assert abs(float(angle_degrees) - 55.45091552083214) < 1.0e-12

    old_path = ROOT / "s2t/results/s2t_v8_cross_arrow_covariance_origin_gate_results.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    old_pair = old["polar_linking_cross_structure"]
    for exact_row, old_row in zip(certificate.pair_matrix.tolist(), old_pair["linking_pair_matrix"]):
        for exact_value, old_value in zip(exact_row, old_row):
            assert abs(float(sp.N(exact_value)) - old_value) < 1.0e-11
    assert abs(float(angle_degrees) - old_pair["covariance_soft_axis_angle_degrees"]) < 1.0e-12

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"] == "version8_cross_arrow_covariance_origin_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 10

    result = {
        "date": "2026-08-29",
        "gate": "version8_cross_arrow_covariance_lcf_migration_gate",
        "exact_algebraic_carrier": {
            "field": "Q(sqrt(2), 2 cos(pi/7))",
            "field_degree": certificate.pair_formula_theorem.proposition.data[
                "field_degree"
            ],
            "polar_coisometry_residual": "zero",
            "physical_reference_shape": [10, 11],
        },
        "polar_cross_structure": {
            "exact_pair_matrix": matrix_strings(certificate.pair_matrix),
            "pair_eigenvalues_exact": [str(value) for value in certificate.pair_eigenvalues],
            "pair_eigenvalues_decimal": [str(value) for value in eigenvalues],
            "positive_definite": True,
            "distinct_eigenvalues": True,
            "number_of_identical_real_pairs": 6,
            "repetition_residual": "zero",
            "coupling_to_other_15_directions": "zero",
        },
        "common_axis": {
            "affine_pair": "(32/5) I_2 + 2 eta B",
            "eta_assumption": "eta > 0",
            "commutator_with_B": "zero",
            "soft_axis_angle_exact": str(certificate.soft_axis_angle_radians),
            "soft_axis_angle_degrees": str(angle_degrees),
            "axis_depends_on_eta": False,
            "normalized_anisotropy_depends_on_eta": True,
        },
        "measure_scale_no_go": {
            "classical_action_scale_nonconstant": True,
            "harmonic_kinetic_scale_nonconstant": True,
            "heat_correlation_time_nonconstant": True,
            "unique_covariance_shape_derived": False,
            "unique_covariance_scale_derived": False,
            "unique_kraus_rate_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_cross_arrow_covariance_origin_gate"
            ],
        },
        "verdict": {
            "polar_cross_axis_lcf_checked": True,
            "six_pair_structure_exact": True,
            "cross_other_decoupling_exact": True,
            "axis_exact_but_not_ckm_pmns": True,
            "shape_and_rate_still_open": True,
            "status": "lcf-checked-axis-positive-shape-rate-no-go",
            "next_gate": "version8_minimal_covariant_stinespring_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()