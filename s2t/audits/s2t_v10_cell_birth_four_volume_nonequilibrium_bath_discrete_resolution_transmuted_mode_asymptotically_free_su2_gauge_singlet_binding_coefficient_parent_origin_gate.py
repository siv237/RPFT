#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate",
        "inherited_data": {
            "exchange_operator": "sum_a T_a tensor T_a=I4/4-P_singlet",
            "coupling_squared": "3/8",
            "binding_coefficient": 0,
            "susceptibility_mixed_block": 0,
            "pole_map": "0_1x1",
        },
        "conditional_parent": {
            "functional": "((kappa-g2*chi)^2+(chi-chi0)^2)/2",
            "stationary_point": ["3*chi0/8", "chi0"],
            "hessian": [["1", "-3/8"], ["-3/8", "73/64"]],
            "rank": int(c.conditional_hessian.rank()),
            "determinant": str(c.conditional_hessian.det()),
            "leading_minors": [str(x) for x in c.leading_minors],
        },
        "inherited_parent": {
            "hessian": [[1, 0], [0, 0]],
            "rank": int(c.inherited_hessian.rank()),
            "nullity": 2 - int(c.inherited_hessian.rank()),
            "flat_direction": [0, 1],
        },
        "status": {
            "conditional_architecture": "10/10",
            "inherited_kinematic_ingredients": "2/2",
            "inherited_dynamic_mixed_block": "0/1",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "strict_conditional_parent_exists": True,
            "exchange_operator_is_inherited": True,
            "coupling_value_is_inherited": True,
            "mediator_susceptibility_is_inherited": False,
            "binding_coefficient_is_dynamically_derived": False,
            "composite_pole_mass_map_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()