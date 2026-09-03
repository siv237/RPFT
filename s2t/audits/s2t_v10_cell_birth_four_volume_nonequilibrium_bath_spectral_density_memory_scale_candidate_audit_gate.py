#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

from s2t.proofdsl.examples.version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate_results.json"


def main() -> None:
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    candidates = [
        "Drude_exponential_correlation",
        "Gaussian_correlation",
        "Ohmic_exponential_cutoff",
        "hard_Brillouin_band",
        "damped_oscillatory_profile",
        "finite_K43_spectral_comb",
        "two_KMS_on_shell_completion",
        "maximum_entropy_hard_band",
        "reciprocal_clock_cutoff_time",
        "observed_relaxation_time",
    ]
    result = {
        "date": "2026-09-02",
        "gate": SPEC.identifier,
        "predecessor": "version10_cell_birth_four_volume_nonequilibrium_bath_correlation_time_parent_origin_gate",
        "candidates": candidates,
        "criteria": [
            "nonnegative_spectral_density",
            "normalized_full_profile",
            "finite_absolute_memory",
            "exact_KMS_on_shell_compatibility",
            "selected_by_existing_parent",
            "independent_absolute_scale_orbit_breaker",
        ],
        "candidate_matrix": [[int(value) for value in certificate.candidate_matrix.row(i)] for i in range(10)],
        "candidate_scores": [int(value) for value in certificate.score_vector],
        "candidate_matrix_rank": 6,
        "passing_candidates": 0,
        "maximum_score": "5/6",
        "component_audit": {
            "shape_candidates": 8,
            "scale_candidates": 2,
            "component_dependency_rank": 2,
            "complete_component_origins": "0/2",
        },
        "exact_profile_witnesses": {
            "exponential_tau_times_omega": "1",
            "Gaussian_tau_times_omega": "sqrt(pi)/2",
            "damped_cosine_tau_times_omega": "1/2",
            "compact_triangle_tau_times_omega": "1/2",
        },
        "scale_audit": {
            "rank_nullity": "2/2",
            "kernel": [[int(value) for value in row] for row in certificate.scale_kernel.tolist()],
            "after_velocity_anchor": "3/1",
            "after_velocity_and_length_anchors": "4/0",
        },
        "status": {
            "candidate_coverage": "10/10",
            "criterion_rank": "6/6",
            "passing_candidates": "0/10",
            "spectral_shape_origin": "0/1",
            "absolute_memory_scale_origin": "0/1",
            "origin_ledger": "3/6",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "standard_profiles_are_mathematically_available": True,
            "existing_parent_selects_a_unique_profile": False,
            "observed_relaxation_is_noncircular": False,
            "absolute_bath_memory_is_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    print(OUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()