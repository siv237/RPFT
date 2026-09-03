#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_inflow_spectral_self_energy_k43_typed_embedding import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / (
    "s2t/results/"
    "s2t_v10_inflow_spectral_self_energy_k43_typed_embedding_gate_results.json"
)


def main() -> None:
    predecessor_path = ROOT / (
        "s2t/results/"
        "s2t_v10_inflow_spectral_self_energy_running_parent_origin_gate_results.json"
    )
    predecessor = json.loads(predecessor_path.read_text())
    gate = "version10_inflow_spectral_self_energy_k43_typed_embedding_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    zeta = sp.symbols("zeta", real=True)
    assert certificate.embedding.shape == (43, 2)
    assert certificate.embedding.T * certificate.embedding == sp.eye(2)
    assert certificate.embedded_projector.rank() == 2
    assert certificate.hypercharge_generator.rank() == 21
    assert certificate.restricted_star_interaction.rank() == 42
    assert certificate.kms_embedding.shape == (258, 12)
    assert certificate.kms_embedding.rank() == 12
    assert certificate.embedded_operator.det() == 1
    assert certificate.compressed_cell_parent == sp.ImmutableMatrix(sp.diag(1, 0))
    assert sp.diff(certificate.incoming_self_energy, zeta) == certificate.incoming_self_energy
    assert sum(certificate.architecture) == 8
    assert sum(certificate.origin_ledger) == 4

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "typed_subcarrier": {
            "ambient_cell": "K43=C|0> direct_sum C^42_jump",
            "subcarrier": "W_Y=span{|Y>,|0>}",
            "embedding_shape": [43, 2],
            "embedding_isometry": True,
            "projector_rank": 2,
            "hypercharge_commutator_checks": "12/12",
            "hypercharge_endpoint_rank": 21,
        },
        "inherited_interaction": {
            "restriction": "Y tensor (|Y><0|+|0><Y|)",
            "restricted_rank": 42,
            "non_spectator": True,
        },
        "kms_typing": {
            "lift": "E_Y tensor I_6",
            "shape": [258, 12],
            "rank": 12,
            "isometry": True,
            "detailed_balance_for_new_operator_derived": False,
        },
        "embedded_spectral_operator": {
            "operator": "I43+(exp(-zeta)-1)P_Y+(exp(zeta)-1)P_0",
            "compressed_operator": "diag(exp(-zeta),exp(zeta))",
            "determinant": "1",
            "incoming_self_energy": "exp(zeta)",
            "incoming_beta": "Sigma_Y",
        },
        "inherited_parent_boundary": {
            "cell_parent": "I43-|0><0|",
            "compression": "diag(1,0)",
            "geometric_beta": "0",
            "reciprocal_spectrum_derived": False,
            "common_growth_parent_derived": False,
        },
        "status": {
            "typed_embedding_architecture": "8/8",
            "origin_ledger": "4/6",
            "typed_k43_embedding": "1/1",
            "reciprocal_spectral_operator_origin": "0/1",
            "common_spectral_growth_parent": "0/1",
            "absolute_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "typed_reservoir_exists_inside_k43": True,
            "gauge_invariant_hypercharge_line_exists": True,
            "inherited_star_coupling_nonzero": True,
            "spectral_running_inherited_from_old_parent": False,
            "absolute_scale_derived": False,
        },
        "next_gate": "version10_k43_reciprocal_spectral_operator_growth_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()