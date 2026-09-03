#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate",
        "static_carrier": {
            "laplacian": [[1, -1], [-1, 1]],
            "decomposition": "L=2*P_physical",
            "gauge_projector_rank": int(c.gauge_projector.rank()),
            "physical_projector_rank": int(c.physical_projector.rank()),
        },
        "gauge_fixed_propagator": {
            "kinetic_operator": "2*P_physical+xi*P_gauge",
            "green_operator": "P_physical/2+P_gauge/xi",
            "two_sided_inverse": True,
            "projected_green": "P_physical/2",
        },
        "conserved_source": {
            "vector": ["1/sqrt(2)", "-1/sqrt(2)"],
            "gauge_projection": [0, 0],
            "susceptibility": "1/2",
            "gauge_parameter_derivative": 0,
        },
        "conditional_binding": {
            "coupling_squared": "3/8",
            "binding_coefficient": "3/16",
        },
        "status": {
            "conditional_architecture": "12/12",
            "gauge_independence": "5/5",
            "inherited_geometric_laplacian": "1/1",
            "typed_su2_embedding": "0/2",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "conserved_source_removes_zero_mode": True,
            "finite_gauge_independent_susceptibility_exists": True,
            "conditional_binding_coefficient_is_three_sixteenths": True,
            "cell_laplacian_is_inherited": True,
            "su2_gauge_field_embedding_is_inherited": False,
            "composite_current_map_is_inherited": False,
            "physical_static_mediator_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()