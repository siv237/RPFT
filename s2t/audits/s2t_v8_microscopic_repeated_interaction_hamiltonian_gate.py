#!/usr/bin/env python3
"""LCF audit of the microscopic repeated-interaction Hamiltonian gate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v8_microscopic_repeated_interaction_hamiltonian_gate_results.json"
)
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_microscopic_interaction_hamiltonian import (  # noqa: E402
    build_certificate,
)
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.system_dimension == 21
    assert certificate.environment_dimension == 13
    assert certificate.ambient_dimension == 273
    assert certificate.jump_dimension == 12
    assert certificate.full_commutant_dimension == 8
    assert certificate.symmetric_rate_metric_dimension == 4
    assert certificate.finite_step_witness == (0, 0)
    assert certificate.typed_theorem.proposition.data["shape"] == [273, 273]
    assert certificate.tangent_theorem.proposition.data["jump_count"] == 12
    assert certificate.covariance_theorem.proposition.data["gauge_invariant"]
    assert certificate.coupling_commutant_theorem.proposition.data[
        "full_commutant_dimension"
    ] == 8
    assert certificate.coupling_commutant_theorem.proposition.data[
        "symmetric_commutant_dimension"
    ] == 4
    assert certificate.finite_step_no_go_theorem.proposition.kind == (
        "matrix_inequality"
    )

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"]
        == "version8_microscopic_repeated_interaction_hamiltonian_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 9

    result = {
        "date": "2026-08-29",
        "gate": "version8_microscopic_repeated_interaction_hamiltonian_gate",
        "carrier": {
            "system_dimension": 21,
            "environment_dimension": 13,
            "jump_dimension": 12,
            "ambient_dimension": 273,
            "environment_decomposition": "C|0> direct_sum E_cross_C",
        },
        "interaction": {
            "formula": "H_int=sum_a D_a tensor (|a><0|+|0><a|)",
            "self_adjoint": True,
            "well_typed": True,
            "vacuum_second_moment": "sum_a D_a^2=G",
            "gauge_covariant": True,
            "orthogonal_frame_basis_independent": True,
        },
        "weak_collision_limit": {
            "unitary": "U_h=exp(-i sqrt(h) H_int)",
            "K0_tangent": "I-hG/2+O(h^2)",
            "Ka_tangent": "-i sqrt(h) D_a+O(h^(3/2))",
            "gksl_tangent_exact": True,
            "fresh_ancilla_scaling": "h=u/n",
            "continuous_limit": "exp(u L_cross)",
        },
        "coupling_selector": {
            "full_real_gauge_commutant_dimension": 8,
            "real_self_adjoint_interaction_coupling_dimension": 8,
            "symmetric_rate_metric_dimension": 4,
            "representation_interpretation": "two equivalent real cross copies; commutant M2(C)",
            "diagonal_two_rate_family_is_complete": False,
            "gauge_symmetry_selects_identity_coupling": False,
            "cross_family_mixing_allowed": True,
            "lindblad_generator_depends_on": "C^T C",
        },
        "finite_step_boundary": {
            "same_first_derivative_as_exact_kraus_channel": True,
            "same_second_order_coefficient": False,
            "matrix_unit_witness": [0, 0],
            "exact_finite_channel_reconstructed": False,
        },
        "physical_boundary": {
            "overall_coupling_scale_selected": False,
            "physical_tick_duration_selected": False,
            "fresh_ancilla_supply_derived": False,
            "autonomous_nonequilibrium_clock_derived": False,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "gate_count": registry["gate_count"],
            "total_obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][
                "version8_microscopic_repeated_interaction_hamiltonian_gate"
            ],
        },
        "verdict": {
            "microscopic_unitary_realization_exists": True,
            "unique_interaction_hamiltonian_derived": False,
            "dimensionless_cross_semigroup_microscopically_realized": True,
            "physical_time_closed": False,
            "status": "lcf_checked_microscopic_collision_realization_with_four_parameter_coupling_no_go",
            "next_gate": "geometric_cross_family_coupling_matrix_selector_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()