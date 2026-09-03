#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate",
        "gauge_pair": {"decomposition": "2_tensor_2=1_direct_sum_3", "singlet_projector_rank": 1, "triplet_projector_rank": 3, "antisymmetrizer_equals_singlet_projector": True},
        "gauge_invariance": {"total_generator_action": "0_12x1", "projector_commutator": "0_12x4", "singlet_Casimir": 0, "triplet_Casimir": 2},
        "conditional_binding_parent": {"operator": "I4-P_singlet", "spectrum": {"0": 1, "1": 3}, "unique_singlet_ground_state": True},
        "inherited_binding": {"two_body_parent": "0_4", "singlet_triplet_splitting": 0, "binding_kernel_present": False},
        "multiplicity": {"doublet_copies": 16, "gauge_singlet_pair_dimension": 256, "selected_flavor_line": False},
        "conditional_pole": {"mass_squared_cell": "exp(-64*pi^2/3)", "simple": True, "residue": 1},
        "status": {"conditional_architecture": "12/12", "gauge_singlet": "6/6", "inherited_binding": "0/2", "physical_origin": "0/3"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {
            "active_rank_one_gauge_singlet_exists_as_composite": True,
            "singlet_is_canonically_selected_by_gauge_antisymmetry": True,
            "flavor_pair_is_selected": False,
            "binding_interaction_is_inherited": False,
            "transmuted_mass_is_dynamically_generated": False,
            "physical_composite_pole_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()