#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate_results.json"


def main() -> None:
    predecessor = json.loads(
        (ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_conductance_common_parent_origin_gate_results.json").read_text()
    )
    gate = "version10_cell_birth_four_volume_cosmological_constant_conductance_anchor_candidate_audit_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate

    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.candidate_matrix.shape == (7, 6)
    assert certificate.candidate_matrix.rank() == 5
    assert certificate.pass_vector == sp.zeros(7, 1)
    assert certificate.internal_break_vector == sp.zeros(7, 1)
    assert certificate.relative_scale_map.rank() == 4
    assert len(certificate.relative_scale_map.nullspace()) == 1
    assert certificate.independently_anchored_map.rank() == 5

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "candidates": [
            "growth_cosmological_constant",
            "intrinsic_cell_curvature",
            "spectral_cutoff_curvature",
            "throughflow_induced_curvature",
            "observed_cosmological_constant",
            "planck_vacuum_density_curvature",
            "topological_density_curvature",
        ],
        "criteria": [
            "correct_curvature_dimension",
            "internally_available",
            "independent_of_rate_scale",
            "typed_map_to_conductance",
            "breaks_rate_orbit",
            "common_parent_provenance",
        ],
        "candidate_matrix": [list(map(int, certificate.candidate_matrix.row(i))) for i in range(7)],
        "candidate_matrix_rank": 5,
        "candidate_scores": [int(sum(certificate.candidate_matrix.row(i))) for i in range(7)],
        "passing_candidates": 0,
        "maximum_score": "4/6",
        "internal_orbit_breakers": 0,
        "growth_cosmological_relation": {
            "growth_rate": "H_B=kappa/3",
            "cosmological_constant": "Lambda_growth=kappa^2/(3*c^2)",
            "attempted_conductance_recovery": "c*sqrt(3*Lambda_growth)=kappa",
            "curvature_radius_product": "kappa*ell_Lambda=3*c",
            "independent_anchor": False,
        },
        "scale_audit": {
            "variables": ["kappa", "Gamma_B", "Omega", "H_B", "Lambda"],
            "relative_map_rank": 4,
            "relative_map_nullity": 1,
            "scale_vector": [1, 1, 1, 1, 2],
            "rank_with_independently_fixed_Lambda": 5,
        },
        "status": {
            "candidate_audit_coverage": "7/7",
            "candidate_origin": "0/7",
            "conditional_external_Lambda_anchor": "1/1",
            "physical_cosmological_origin": "0/1",
            "absolute_conductance": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "growth_Lambda_is_compatible_with_conductance": True,
            "growth_Lambda_independently_selects_conductance": False,
            "independently_derived_Lambda_would_select_conductance": True,
            "current_project_derives_independent_physical_Lambda": False,
        },
        "next_gate": "version10_cell_birth_four_volume_cosmological_constant_throughflow_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()