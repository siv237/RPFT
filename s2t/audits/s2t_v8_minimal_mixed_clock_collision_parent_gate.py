#!/usr/bin/env python3
"""Exact audit of the minimal energy-conserving clock--collision parent."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_minimal_mixed_clock_collision_parent_gate_results.json"


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def main() -> None:
    # A two-direction exact representative suffices for the algebraic identity;
    # the proof is termwise and therefore extends to all 42 Hermitian jumps.
    identity_s = sp.eye(2)
    identity_e = sp.eye(3)
    identity_c = sp.eye(2)
    sigma_x = sp.Matrix([[0, 1], [1, 0]])
    sigma_z = sp.Matrix([[1, 0], [0, -1]])
    jumps = (sigma_x, sigma_z)

    h_environment = sp.diag(0, 1, 1)
    h_clock = sp.diag(0, 1)
    h_free = sp.kronecker_product(identity_s, h_environment, identity_c)
    h_free += sp.kronecker_product(identity_s, identity_e, h_clock)

    ket_e0 = sp.Matrix([1, 0, 0])
    ket_c1 = sp.Matrix([0, 1])
    bath_input = sp.kronecker_product(ket_e0, ket_c1)

    interaction = sp.zeros(12)
    extracted_jumps: list[sp.Matrix] = []
    for index, jump in enumerate(jumps, start=1):
        ket_ea = sp.eye(3)[:, index]
        ket_c0 = sp.Matrix([1, 0])
        raise_environment = ket_ea * ket_e0.T
        lower_clock = ket_c0 * ket_c1.T
        transfer = sp.kronecker_product(raise_environment, lower_clock)
        interaction += sp.kronecker_product(jump, transfer + transfer.T)

        bath_output = sp.kronecker_product(ket_ea, ket_c0)
        left = sp.kronecker_product(identity_s, bath_output.T)
        right = sp.kronecker_product(identity_s, bath_input)
        extracted_jumps.append(sp.simplify(left * interaction * right))

    commutator = sp.simplify(h_free * interaction - interaction * h_free)
    energy_conservation_exact = matrix_is_zero(commutator)
    jump_extraction_exact = all(
        matrix_is_zero(extracted - expected)
        for extracted, expected in zip(extracted_jumps, jumps)
    )

    left_input = sp.kronecker_product(identity_s, bath_input.T)
    right_input = sp.kronecker_product(identity_s, bath_input)
    vacuum_first_moment = sp.simplify(left_input * interaction * right_input)
    vacuum_second_moment = sp.simplify(
        left_input * interaction**2 * right_input
    )
    expected_second_moment = sum((jump**2 for jump in jumps), sp.zeros(2))

    e_c, chi, lam = sp.symbols("E_C chi lambda", positive=True)
    h_total = e_c * (h_free + chi * interaction)
    scaled_h_total = (lam * e_c) * (h_free + chi * interaction)
    scale_identity = sp.simplify(scaled_h_total - lam * h_total)

    p1 = sp.ones(4) / 4
    p3 = sp.eye(4) - p1
    affine_rank = p3.rank()
    full_noise_rank = 42
    intertwiner_parameter_count = affine_rank * full_noise_rank

    result = {
        "date": "2026-08-30",
        "gate": "version8_minimal_mixed_clock_collision_parent_gate",
        "representative": {
            "system_dimension": 2,
            "environment_dimension": 3,
            "clock_dimension": 2,
            "jump_count": 2,
            "extension_to_full_frame": "termwise_for_42_Hermitian_jumps",
        },
        "parent": {
            "free_energy": "E_C(P_exc_environment+N_clock)",
            "interaction_energy": "chi E_C sum_a F_a tensor (|a,0><0,1|+h.c.)",
            "total_hamiltonian": "E_C(H_0+chi G)",
        },
        "exact_checks": {
            "energy_conservation_commutator_zero": energy_conservation_exact,
            "jump_extraction_exact": jump_extraction_exact,
            "vacuum_first_moment_zero": matrix_is_zero(vacuum_first_moment),
            "vacuum_second_moment_exact": matrix_is_zero(
                vacuum_second_moment - expected_second_moment
            ),
            "common_energy_scale_identity": matrix_is_zero(scale_identity),
        },
        "affine_multiplicity": {
            "rank_P3": affine_rank,
            "full_noise_rank": full_noise_rank,
            "direct_unitary_identification_possible": affine_rank == full_noise_rank,
            "linear_map_parameter_count_P3_to_noise": intertwiner_parameter_count,
            "canonical_map_to_full_noise_frame_supplied": False,
            "role": "resonant_degeneracy_only_not_rate_or_energy_selector",
        },
        "scale_and_rate": {
            "tick_duration": "tau_C=hbar/E_C",
            "rate": "Gamma=chi^2 E_C/hbar",
            "relative_rate": "Gamma/Omega=chi^2",
            "scale_orbit": "(E_C,t)->(lambda E_C,t/lambda)",
            "chi_values_preserving_energy_conservation": "all_positive_chi",
            "E_C_selected": False,
            "chi_selected": False,
        },
        "verdict": {
            "energy_conserving_full_noise_parent_exists": True,
            "typed_rate_bridge_strengthened": True,
            "prepared_excited_clock_chain_required": True,
            "affine_rank_three_needed_for_full_noise_parent": False,
            "absolute_time_anchor_derived": False,
            "time_sprint_closed_on_current_parent": True,
            "next_program": "exact_baryon_sector_certificates",
        },
    }

    assert all(result["exact_checks"].values())
    assert affine_rank == 3
    assert intertwiner_parameter_count == 126
    assert not result["scale_and_rate"]["E_C_selected"]
    assert not result["scale_and_rate"]["chi_selected"]

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()