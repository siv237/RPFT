#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_particle_wrinkle_dislocation_mixed_bridge_candidate_audit_gate",
        "minimal_conditional_carrier": {
            "factorization": "C2_spin tensor C2_twist tensor H15",
            "complex_dimension": 60,
            "positive_mass_rank": 30,
            "negative_mass_rank": 30,
            "coefficient_index_multiplicity": 15,
            "spatial_twist_commutator": "zero",
        },
        "inherited_carriers": {
            "C2_spin_tensor_H15_dimension": 30,
            "K43_dimension": 43,
            "KO_pair_charge_flip_commutator_rank": int(certificate.ko_charge_defect.rank()),
            "cell_edge_pauli_algebra": True,
            "cell_to_flavor_twist_embedding_rank": int(certificate.cell_to_flavor_twist_map.rank()),
        },
        "status": {
            "conditional_architecture": "10/10",
            "separate_inherited_ingredients": "5/5",
            "equal_charge_twist_origin": "0/3",
            "strict_common_carrier_admission": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "minimal_callias_carrier_is_algebraically_consistent": True,
            "KO_particle_conjugate_pair_can_be_the_twist_doublet": False,
            "K43_cell_edge_can_supply_an_abstract_twist_algebra": True,
            "K43_cell_edge_is_embedded_uniformly_over_H15": False,
            "strict_callias_carrier_is_inherited": False,
        },
        "next_gate": "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()