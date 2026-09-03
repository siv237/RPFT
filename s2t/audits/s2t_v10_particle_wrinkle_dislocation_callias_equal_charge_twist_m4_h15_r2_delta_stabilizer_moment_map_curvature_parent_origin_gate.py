#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_stabilizer_moment_map_curvature_parent_origin_gate_results.json"


def main():
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_sigma_mixed_curvature_candidate_audit_gate_results.json").read_text()
    )
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.moment_norms == sp.ImmutableMatrix([sp.Rational(1, 2), sp.Rational(3, 4)])
    assert c.hypercharge6 == sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3])
    assert c.positive_moment_hessian.rank() == 8
    assert c.full_parent_hessian.rank() == 14
    assert len(c.full_parent_hessian.nullspace()) == 2
    assert c.schur_complement == c.target_gap
    assert c.inherited_auxiliary_coupling.rank() == 0

    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "moment_map": {
            "mu_R": [["1/2", 0], [0, "-1/2"]],
            "mu_4": [["-1/4", 0, 0, 0], [0, "-1/4", 0, 0], [0, 0, "-1/4", 0], [0, 0, 0, "3/4"]],
            "trace_norms": ["1/2", "3/4"],
            "normalized_combination": "Q=6Y=6*mu_R-4*ad(mu_4)",
            "Sigma_spectrum": list(map(int, c.hypercharge6)),
            "normalization_locked": True,
        },
        "positive_norm_diagnosis": {
            "Hessian": "Q^2",
            "diagonal": list(map(int, c.positive_moment_hessian.diagonal())),
            "rank": 8,
            "R2_mass": 49,
            "verdict": "wrong ordering: R2 is maximally heavy",
        },
        "shared_auxiliary_parent": {
            "full_block": "[[49I,Q],[Q,I]]",
            "congruence_diagonal": "diag(49I-Q^2,I)",
            "full_rank": 14,
            "full_nullity": 2,
            "full_inertia_negative_zero_positive": [0, 2, 14],
            "Schur_complement": "49I-Q^2",
            "Schur_diagonal": list(map(int, c.schur_complement.diagonal())),
            "Schur_rank": 6,
            "Schur_nullity": 2,
            "conditional_parent_valid": True,
        },
        "inheritance": {
            "typed_auxiliary_Q_coupling_rank": 0,
            "inherited_cross_block_rank": 0,
            "inherited_Schur_complement": "49I",
            "fixed_point_auxiliary_subspace_embedding": "open",
        },
        "status": {
            "conditional_Schur_parent": "3/4",
            "physical_origin": "2/4",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "moment_map_normalization_derived": True,
            "positive_moment_map_norm_gives_target_gap": False,
            "shared_auxiliary_Schur_parent_gives_target_gap": True,
            "shared_auxiliary_channel_inherited": False,
            "physical_parent_found": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_shared_fixed_point_auxiliary_channel_typed_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()