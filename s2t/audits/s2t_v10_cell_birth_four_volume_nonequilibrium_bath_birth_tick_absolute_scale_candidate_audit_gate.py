#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_absolute_scale_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    names = [
        "clock_energy_inverse",
        "causal_edge_transit",
        "ultraviolet_phase_tick",
        "K43_spectral_transit",
        "bath_correlation_time",
        "Hopf_conductance_tick",
        "dimensional_transmutation_frequency",
        "Planck_time",
        "curvature_time",
        "observed_growth_time",
        "dimensionless_vacuum_action",
        "external_atomic_clock_period",
    ]
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate",
        "criteria": [
            "time_dimension",
            "internal_availability",
            "selected_by_current_parent",
            "independent_scale_orbit_breaking",
            "non_circularity",
            "unique_typed_map_to_birth_tick",
        ],
        "candidates": [
            {
                "name": name,
                "score": int(certificate.score_vector[index]),
                "pass": bool(certificate.pass_vector[index]),
            }
            for index, name in enumerate(names)
        ],
        "audit": {
            "matrix_shape": "12x6",
            "criterion_rank": 6,
            "complete_passes": 0,
            "maximum_score": 5,
            "internal_orbit_breakers": 0,
        },
        "relative_collapse": {
            "equivalent_formulas": [
                "hbar/E_C",
                "ell_edge/c",
                "2 sqrt(3)/omega_UV",
                "42/(c Lambda_43)",
                "1/(22 kappa)",
            ],
            "all_equal_tau_birth": True,
            "exponential_correlation_over_tau_birth": "1/(2 sqrt(3))",
            "Gaussian_correlation_over_tau_birth": "sqrt(pi)/(4 sqrt(3))",
        },
        "scale_audit": {
            "after_c_anchor_rank_nullity": "3/1",
            "kernel": [int(value) for value in certificate.scale_kernel],
            "after_external_tick_anchor": "4/0",
        },
        "status": {
            "candidate_coverage": "12/12",
            "criterion_coverage": "6/6",
            "complete_candidates": "0/12",
            "absolute_birth_tick_origin": "0/1",
            "physical_clock_origin": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "current_internal_tick_formulas_are_independent_anchors": False,
            "bath_correlation_time_uniquely_selects_birth_tick": False,
            "dimensional_transmutation_breaks_scale_orbit": False,
            "external_clocks_can_break_the_orbit": True,
            "an_internal_absolute_birth_tick_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_birth_tick_dimensional_transmutation_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()