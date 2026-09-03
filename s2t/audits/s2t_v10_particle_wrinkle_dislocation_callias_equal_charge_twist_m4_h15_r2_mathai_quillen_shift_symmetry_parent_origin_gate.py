#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_odd_pair_statistics_candidate_audit_gate_results.json").read_text())
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.effective_hessian.rank() == 6
    assert c.difference_map * c.diagonal_shift == sp.zeros(8)
    assert c.stueckelberg_hessian * c.diagonal_shift == sp.zeros(16, 8)
    assert c.physical_inclusion.T * c.stueckelberg_hessian * c.physical_inclusion == c.effective_hessian
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "inherited_parent": {
            "effective_Sigma_hessian_diagonal": list(map(int, c.effective_hessian.diagonal())),
            "hessian_rank_nullity": [c.effective_hessian.rank(), 8 - c.effective_hessian.rank()],
            "required_full_shift_rank": c.required_shift.rank(),
            "translation_breaking_rank": (c.effective_hessian * c.required_shift).rank(),
            "maximum_quadratic_flat_shift_rank": c.inherited_flat_basis.rank(),
            "quadratic_shift_rank_deficit": c.required_shift.rank() - c.inherited_flat_basis.rank(),
            "ordinary_gauge_translational_rank_at_Sigma_zero": c.ordinary_gauge_tangent_at_origin.rank(),
        },
        "conditional_stueckelberg_completion": {
            "doubled_real_dimension": 16,
            "difference_map_rank": c.difference_map.rank(),
            "diagonal_shift_rank": c.diagonal_shift.rank(),
            "difference_annihilates_shift": True,
            "parent_hessian_rank_nullity": [c.stueckelberg_hessian.rank(), 16 - c.stueckelberg_hessian.rank()],
            "full_shift_invariant": True,
            "unitary_gauge_recovers_original_hessian": True,
            "Q_gauge_fixing_rank": c.gauge_fixing_operator.rank(),
            "FP_determinant": int(c.gauge_fixing_operator.det()),
            "inherited_copy_injection_rank": c.inherited_stueckelberg_injection.rank(),
            "target_loaded_new_copy": True,
        },
        "status": {
            "criteria": ["typed_copy", "rank8_shift", "shift_invariant_parent", "quotient_recovery", "Q_FP_operator", "acyclic_BRST", "inherited_origin"],
            "conditional": list(map(int, c.conditional_status)),
            "conditional_score": "6/7",
            "inherited": list(map(int, c.inherited_status)),
            "inherited_score": "3/7",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "current_Sigma_parent_has_rank8_shift_symmetry": False,
            "conditional_stueckelberg_shift_parent_exists": True,
            "conditional_completion_is_inherited": False,
            "physical_Mathai_Quillen_parent_found": False,
            "particle_wrinkle_branch_ready_for_final_no_go": True,
        },
        "next_gate": "version10_final_conclusion_and_tome11_program_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()