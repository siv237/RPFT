#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_final_conclusion_and_tome11_program import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_final_conclusion_and_tome11_program_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_mathai_quillen_shift_symmetry_parent_origin_gate_results.json").read_text())
    assert predecessor["next_gate"] == SPEC.identifier
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.operational_physical + c.operational_deficit == c.operational_conditional
    assert c.inherited_rg_physical + c.inherited_rg_deficit == sp.ones(6, 1)
    assert c.tome11_dependency.rank() == 6 and c.tome11_dependency.det() == 1
    result = {
        "date": "2026-09-03",
        "gate": SPEC.identifier,
        "predecessor": predecessor["gate"],
        "tome10_operational_contract": {
            "criteria": [
                "common_growth_spectral_field_carrier",
                "physical_origin_of_normalized_birth_measure",
                "nonzero_quantum_running_or_trace_anomaly",
                "physical_growth_curvature_coupling",
                "typed_geometric_to_local_energy_map",
                "unconditional_dimensionless_consequence",
            ],
            "conditional": list(map(int, c.operational_conditional)),
            "conditional_score": "6/6",
            "physical": list(map(int, c.operational_physical)),
            "physical_score": "4/6",
            "deficit": list(map(int, c.operational_deficit)),
            "deficit_rank": 2,
        },
        "tome9_inherited_quantum_rg_contract": {
            "criteria": [
                "common_quantum_field_RG_carrier",
                "nonzero_beta_or_trace_anomaly",
                "RG_invariant_transmutation_scale",
                "typed_scale_embedding_into_KMS_Gaussian_parent",
                "physical_measure_and_reference_state_for_logdet",
                "scheme_independent_blind_consequence",
            ],
            "physical": list(map(int, c.inherited_rg_physical)),
            "physical_score": "3/6",
            "deficit": list(map(int, c.inherited_rg_deficit)),
            "deficit_rank": 3,
        },
        "stable_achievements": [
            "geometric history zeta=log(N/N0)/3 and common typed carrier",
            "dimensionless reciprocal spectral running with exact trace witness",
            "normalized cell-birth and KMS throughflow architectures",
            "relative curvature, Newton-cell and entropy-growth identities",
            "RG-invariant discrete resolution not requiring absolute cell size",
            "typed particle-wrinkle chain ending in a strict Mathai-Quillen shift no-go",
        ],
        "unresolved_physical_packages": [
            "origin of birth weights and physical clock rate",
            "independent curvature-flow coupling and absolute cosmological scale",
            "RG-invariant absolute transmutation scale and inherited portal",
            "physical logdet/Berezin parent without new auxiliary fields",
        ],
        "reopening_packages": {
            "physical_passes": list(map(int, c.reopening_packages)),
            "score": "0/4",
        },
        "tome11_program": {
            "title": "Relational observables, perturbations, and falsifiable cross-sector consequences",
            "criteria": [
                "common_relational_observable_algebra",
                "explicit_quotient_by_the_scale_orbit",
                "linear_perturbation_and_response_theory",
                "particle_cosmology_cross_sector_morphisms",
                "scheme_and_gauge_independent_blind_relations",
                "frozen_external_falsification_protocol",
            ],
            "dependency_rank": c.tome11_dependency.rank(),
            "dependency_determinant": int(c.tome11_dependency.det()),
            "specification": list(map(int, c.tome11_specification)),
            "construction": list(map(int, c.tome11_construction)),
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "tome10_conditionally_closed": True,
            "tome10_physically_complete": False,
            "absolute_scale_derived": False,
            "particle_wrinkle_parent_derived": False,
            "tome10_frozen": True,
            "tome11_admitted_as_program_only": True,
        },
        "next_gate": "version11_relational_observable_common_carrier_admission_gate",
        "floating_point_values": 0,
    }
    output = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(output)
    print(OUT)
    print(hashlib.sha256(output.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()