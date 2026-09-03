#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_m4_cross_generator_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_common_carrier_admission_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.conditional_gradient == sp.zeros(4, 1)
    assert certificate.conditional_hessian.rank() == 4
    assert certificate.conditional_hessian.det() == 32
    assert certificate.sign_minimum_values == sp.zeros(4, 1)
    assert certificate.phase_potential == 0
    assert certificate.inherited_cross_hessian == sp.zeros(4)

    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "conditional_parent": {
            "potential": "Tr((V*V-I)^2)/4+Tr((ZV-VZ)*(ZV-VZ))/4",
            "stationary_point": "V=I2",
            "hessian_rank": 4,
            "hessian_determinant": 32,
            "hessian_spectrum": {"2": 3, "4": 1},
            "real_sign_minima": 4,
            "complex_phase_moduli": "U(1)^2",
        },
        "inherited_parent": {
            "cross_hessian_rank_nullity": "0/4",
            "linear_cross_source": [0, 0, 0, 0],
            "bifundamental_cross_variable_present": False,
        },
        "status": {
            "conditional_architecture": "10/10",
            "conditional_origin": "8/8",
            "cross_variable_origin": "0/1",
            "condensate_norm_origin": "0/1",
            "intertwiner_phase_origin": "0/1",
            "coefficient_origin": "0/3",
            "physical_temperature_origin": "0/1",
            "strict_physical_origin": "0/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "positive_parent_can_conditionally_condense_cross_generator": True,
            "conditional_parent_selects_unique_phase": False,
            "existing_parent_contains_cross_order_parameter": False,
            "M4_cross_generator_has_physical_origin": False,
        },
        "next_gate": "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_m4_bifundamental_condensate_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()