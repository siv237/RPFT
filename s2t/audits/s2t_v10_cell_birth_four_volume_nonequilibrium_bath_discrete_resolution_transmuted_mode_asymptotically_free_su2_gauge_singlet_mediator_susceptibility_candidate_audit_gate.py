#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_mediator_susceptibility_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    c = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_coefficient_parent_origin_gate",
        "normalization_orbit": {
            "g_squared_exponent": -2,
            "susceptibility_exponent": 2,
            "binding_product_exponent": int(c.binding_exponent),
            "invariant_observable": "g_squared*chi",
        },
        "massless_static_obstruction": {
            "kinetic_operator": [[1, -1], [-1, 1]],
            "spectrum": {"0": 1, "2": 1},
            "rank": int(c.massless_laplacian.rank()),
            "determinant": int(c.massless_laplacian.det()),
            "zero_mode": [1, 1],
        },
        "exact_internal_numbers": {
            "inverse_k43_cutoff": "1/42",
            "inverse_abs_af_beta": "1/2",
            "neither_is_a_typed_static_propagator": True,
        },
        "candidate_audit": {
            "candidate_count": c.candidate_matrix.rows,
            "criterion_count": c.candidate_matrix.cols,
            "rank": int(c.candidate_matrix.rank()),
            "scores": [int(x) for x in c.score_vector],
            "full_passes": int(sum(c.pass_vector)),
            "internal_origins": int(sum(c.internal_origin_vector)),
        },
        "status": {
            "candidate_coverage": "11/11",
            "full_candidate_passes": "0/11",
            "normalization_invariant_product": "1/1",
            "physical_origin": "0/3",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "susceptibility_alone_is_normalization_invariant": False,
            "binding_product_is_normalization_invariant": True,
            "massless_static_propagator_is_invertible": False,
            "finite_typed_normalized_static_kernel_is_inherited": False,
            "mediator_susceptibility_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_su2_mediator_static_propagator_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()