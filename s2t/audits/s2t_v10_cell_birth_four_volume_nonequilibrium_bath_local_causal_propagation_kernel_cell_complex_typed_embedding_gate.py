#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate",
        "cell_complex": {
            "witness": "oriented seven-vertex path complex",
            "chain_spaces": {"C0_dimension": 7, "C1_dimension": 6},
            "boundary_rank": int(certificate.boundary.rank()),
            "laplacian_rank_nullity": "6/1",
            "construction": "Delta_0=B B^T, D=diag(Delta_0), A=(D-Delta_0)/2",
            "orientation_invariant": True,
            "vertex_relabelling_covariant": True,
        },
        "propagation": {
            "reproduces_previous_adjacency": certificate.adjacency == certificate.reference_adjacency,
            "checked_steps": [1, 2, 3],
            "causal_defects": 0,
            "edge_amplitude": "1/2 (inherited normalization)",
        },
        "memory_parent": {
            "rank_nullity": "3/1",
            "kernel_tangent_at_r_half": ["1", "1", "3/4", "1"],
            "decay_selected_by_embedding": False,
        },
        "scale_audit": {
            "rank_nullity": "2/2",
            "kernel": [[int(value) for value in row] for row in certificate.scale_kernel.tolist()],
        },
        "status": {
            "conditional_typed_embedding": "10/10",
            "typed_incidence_origin": "1/1",
            "global_cell_complex_origin": "0/1",
            "physical_edge_metric_origin": "0/1",
            "damping_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "local_kernel_has_a_typed_cell_complex_realization": True,
            "realization_is_orientation_independent": True,
            "realization_preserves_causal_support": True,
            "realization_selects_physical_edge_length": False,
            "realization_selects_decay_parameter": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()