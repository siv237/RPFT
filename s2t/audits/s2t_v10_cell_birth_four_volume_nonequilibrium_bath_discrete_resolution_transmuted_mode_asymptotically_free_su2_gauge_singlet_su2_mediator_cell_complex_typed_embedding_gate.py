#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_cell_complex_typed_embedding_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate",
        "cell_adjoint_carrier": {
            "edge_dimension": 3,
            "vertex_dimension": 6,
            "boundary_rank": int(c.adjoint_boundary.rank()),
            "laplacian_rank": int(c.adjoint_laplacian.rank()),
            "laplacian_nullity": 6 - int(c.adjoint_laplacian.rank()),
        },
        "relative_current": {
            "intertwiner_shape": list(c.relative_current_intertwiner.shape),
            "rank": int(c.relative_current_intertwiner.rank()),
            "gram": "I3",
            "image_projector": "P_triplet",
            "adjoint_covariance": True,
        },
        "combined_current": {
            "shape": list(c.combined_current_map.shape),
            "rank": int(c.combined_current_map.rank()),
            "pair_support": "P_triplet",
            "cell_support": "P_conserved_adjoint",
        },
        "conditional_response": {
            "susceptibility_matrix": "I3/2",
            "coupling_squared": "3/8",
            "binding_coefficient": "3/16",
        },
        "status": {
            "conditional_architecture": "14/14",
            "typed_embedding": "10/10",
            "inherited_ingredients": "2/2",
            "physical_origin": "0/2",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "adjoint_cell_field_is_typed": True,
            "relative_pair_current_is_adjoint_covariant": True,
            "conserved_current_map_is_constructed": True,
            "susceptibility_is_component_independent": True,
            "flavor_pair_is_selected": False,
            "gap_to_pole_map_is_derived": False,
            "physical_composite_pole_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_pair_selector_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()