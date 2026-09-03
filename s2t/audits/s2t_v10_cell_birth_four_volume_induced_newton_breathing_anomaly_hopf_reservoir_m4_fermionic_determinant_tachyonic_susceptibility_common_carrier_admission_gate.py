#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_tachyonic_susceptibility_common_carrier_admission_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_cell_incidence_tachyonic_sign_parent_origin_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.dirac_square == (1 + sp.symbols("x", real=True) ** 2) * sp.eye(4)
    assert certificate.determinant_polynomial == (1 + sp.symbols("x", real=True) ** 2) ** 2
    assert certificate.fermion_curvature == -4
    assert certificate.total_curvature == -2
    assert certificate.stationary_curvatures == sp.Matrix([2, -2, 2])
    assert certificate.block_diagonal_cross_projection == sp.zeros(4)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "minimal_conditional_carrier": {
            "complex_dimension": 4,
            "decomposition": "C2_reservoir direct_sum C2_path",
            "reservoir_projector_rank": 2,
            "path_projector_rank": 2,
            "sector_grading_squared": "I4",
            "cross_involution_squared": "I4",
            "grading_cross_anticommutator": "zero",
        },
        "fermionic_determinant": {
            "dirac_square": "(1+x^2) I4",
            "determinant": "(1+x^2)^2",
            "logdet_curvature_at_zero": -4,
            "unit_incidence_plus_logdet_curvature_at_zero": -2,
            "stationary_points": [-1, 0, 1],
            "stationary_curvatures": [2, -2, 2],
            "minimum_value": "1-log(4)",
            "berezin_pairing_rank": 8,
            "berezin_pairing_determinant": 16,
        },
        "inheritance": {
            "common_C4_carrier": True,
            "sector_grading": True,
            "cross_bilinear": False,
            "odd_statistics": False,
            "coupling_normalization": False,
            "Berezin_measure": False,
            "block_diagonal_cross_projection_rank": 0,
        },
        "status": {
            "conditional_architecture": "14/14",
            "inherited_ingredients": "2/6",
            "strict_common_carrier_admission": "0/1",
            "physical_origin": "0/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "conditional_M4_fermionic_carrier_is_sufficient": True,
            "fermion_logdet_conditionally_seeds_stable_nonzero_cross_mode": True,
            "cross_generator_is_inherited_from_block_diagonal_parent": False,
            "fermionic_statistics_and_measure_are_inherited": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_fermionic_determinant_cross_bilinear_odd_statistics_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()