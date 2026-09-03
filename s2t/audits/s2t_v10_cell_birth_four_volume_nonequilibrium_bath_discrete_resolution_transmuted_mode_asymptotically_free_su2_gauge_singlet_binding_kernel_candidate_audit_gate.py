#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate",
        "invariant_operator_space": {
            "commutator_constraint_rank": int(c.commutant_constraint.rank()),
            "commutant_dimension": int(c.commutant_dimension),
            "basis": ["I4", "P_singlet"],
            "general_kernel": "a*P_singlet+b*P_triplet",
            "free_gap": "b-a",
        },
        "canonical_exchange": {
            "operator": "sum_a T_a tensor T_a",
            "identity": "I4/4-P_singlet",
            "spectrum": {"-3/4": 1, "1/4": 3},
            "normalized_parent": "3*I4/4+exchange=P_triplet",
        },
        "inherited_binding": {
            "kernel": "0_4",
            "singlet_triplet_gap": 0,
            "flavor_pair_degeneracy": 256,
        },
        "candidate_audit": {
            "candidate_count": c.candidate_matrix.rows,
            "criterion_count": c.candidate_matrix.cols,
            "rank": int(c.candidate_matrix.rank()),
            "scores": [int(x) for x in c.score_vector],
            "full_passes": int(sum(c.pass_vector)),
            "selected_internal_origins": int(sum(c.selected_origin_vector)),
        },
        "status": {
            "canonical_operator_architecture": "6/6",
            "candidate_coverage": "11/11",
            "full_candidate_passes": "0/11",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "su2_symmetry_fixes_two_channel_form": True,
            "canonical_exchange_selects_singlet_relative_to_triplet": True,
            "overall_binding_coefficient_is_derived": False,
            "flavor_pair_is_selected": False,
            "composite_pole_scale_is_derived": False,
            "physical_binding_kernel_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()