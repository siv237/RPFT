#!/usr/bin/env python3
"""Migrate the gauge-twirled cross-sector Kraus bridge to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_gauge_twirl_kraus_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_gauge_twirl_kraus import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def matrix_strings(matrix: sp.MatrixBase) -> list[list[str]]:
    return [[str(sp.simplify(value)) for value in row] for row in matrix.tolist()]


def main() -> None:
    certificate = build_certificate()
    expected_cross = sp.ImmutableMatrix(
        [[1, -2 / sp.sqrt(3)], [-2 / sp.sqrt(3), sp.Rational(4, 3)]]
    )
    assert certificate.cross_real_dimension == 12
    assert certificate.internal_control_dimension == 8
    assert certificate.cross_central_matrix == expected_cross
    assert certificate.internal_central_matrix == sp.zeros(2)
    assert certificate.gauge_covariance_theorem.proposition.data == {
        "frame_dimension": 12,
        "symmetry_generator_count": 12,
        "invariant_linear_dimension": 0,
    }
    assert certificate.cross_kernel_theorem.proposition.data["nullity"] == 1
    assert certificate.positive_rate_kernel_theorem.proposition.data["nullity"] == 1

    old_path = ROOT / "s2t/results/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate_results.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    old_cross = old["basis_independent_kraus_sum"]["central_tests"][
        "both_cross_multiplets"
    ]
    assert old_cross["kernel_dimension_inside_C2"] == 1
    for exact_row, old_row in zip(expected_cross.tolist(), old_cross["matrix"]):
        for exact_value, old_value in zip(exact_row, old_row):
            assert abs(float(sp.N(exact_value)) - old_value) < 1.0e-12

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"]
        == "version8_gauge_twirl_cross_sector_kraus_bridge_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 10

    result = {
        "date": "2026-08-29",
        "gate": "version8_gauge_twirl_kraus_lcf_migration_gate",
        "typed_kraus_carrier": {
            "endpoint_dimension": 21,
            "QLYR_real_directions": 6,
            "XLdR_real_directions": 6,
            "cross_real_dimension": certificate.cross_real_dimension,
            "internal_control_real_dimension": certificate.internal_control_dimension,
            "matrix_entries": "exact integers, I, and sqrt(2) normalization",
        },
        "gksl_and_basis_certificate": {
            "gksl_status": certificate.gksl_theorem.proposition.kind,
            "unital_identity_residual": certificate.unital_theorem.certificate[
                "identity_residual"
            ],
            "basis_invariance_rule": certificate.basis_invariance_theorem.rule,
            "basis_invariance_quantifier": certificate.basis_invariance_theorem.certificate[
                "quantifier"
            ],
        },
        "exact_gauge_covariance": {
            "symmetry": "SU(3) x SU(2) x U(1)",
            "hermitian_generators_checked": 12,
            "jump_frame_dimension": 12,
            "frame_gram": certificate.gauge_covariance_theorem.certificate[
                "frame_gram"
            ],
            "closure_residual": certificate.gauge_covariance_theorem.certificate[
                "closure_residual"
            ],
            "skew_action_residual": certificate.gauge_covariance_theorem.certificate[
                "action_transpose_residual"
            ],
            "linear_gauge_singlet_dimension": 0,
            "connected_group_covariance_exact": True,
        },
        "central_dirichlet_restrictions": {
            "QLYR": matrix_strings(certificate.qlyr_central_matrix),
            "XLdR": matrix_strings(certificate.xldr_central_matrix),
            "both_cross_multiplets": matrix_strings(certificate.cross_central_matrix),
            "both_cross_characteristic_polynomial": "lambda*(lambda - 7/3)",
            "both_cross_kernel_dimension": 1,
            "internal_lepton_control": matrix_strings(
                certificate.internal_central_matrix
            ),
            "old_numerical_kernel_dimension": old_cross[
                "kernel_dimension_inside_C2"
            ],
        },
        "positive_rate_robustness": {
            "symbolic_rates": ["gamma_QLYR > 0", "gamma_XLdR > 0"],
            "restriction": "(gamma_QLYR + gamma_XLdR) times the one-family matrix",
            "exact_kernel_dimension": 1,
            "finite_random_scan_needed": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_gauge_twirl_cross_sector_kraus_bridge_gate"
            ],
        },
        "verdict": {
            "gksl_structure_lcf_checked": True,
            "orthogonal_basis_independence_exact": True,
            "gauge_covariance_exact_at_lie_algebra_level": True,
            "linear_gauge_singlet_absent_exact": True,
            "C2_reduced_to_scalar_line_exact": True,
            "positive_rate_robustness_exact": True,
            "common_parent_action_hessian_checked": False,
            "status": "lcf-checked-parent-action-still-open",
            "next_gate": "version8_kraus_bridge_parent_action_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()