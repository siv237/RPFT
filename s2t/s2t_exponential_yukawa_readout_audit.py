#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np

from s2t_relative_modular_cocycle_bch_audit import cross_matrix, jarlskog
from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def mass_pattern(eigenvalues, beta):
    ordered = np.sort(np.real(eigenvalues))
    weights = np.exp(-beta * (ordered - ordered[0]))
    return np.sort(weights / weights.max())


def hierarchy_score(prediction, target):
    return float(
        np.sqrt(np.mean(np.log(prediction[:-1] / target[:-1]) ** 2))
    )


def mixing_angles(unitary):
    sin13 = abs(unitary[0, 2])
    cos13 = math.sqrt(max(0.0, 1.0 - sin13**2))
    return np.array(
        [abs(unitary[0, 1]) / cos13, abs(unitary[1, 2]) / cos13, sin13]
    )


def main():
    wilson = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    hierarchy = json.loads(
        Path("s2t_family_factor_operator_results.json").read_text(
            encoding="utf-8"
        )
    )["hierarchy_comparison"]
    target_up = np.array(
        hierarchy["up_quarks_at_declared_scales"]["target"]
    )
    target_down = np.array(
        hierarchy["down_quarks_at_declared_scales"]["target"]
    )
    cosine = wilson["continuous_two_sector_solution"]["cos_theta_numeric"]
    angle = math.acos(cosine)
    axes = [
        np.array(axis)
        for axis in wilson["factor_axis_selector"]["summary"][
            "inverse_length"
        ]["selected_axes"]
    ]
    basis = triplet_basis()
    identity2 = np.eye(2, dtype=int)
    translate_rp3 = restrict(
        permutation_matrix(affine_permutation(identity2, (1, 0))), basis
    )
    translate_s1 = restrict(
        permutation_matrix(affine_permutation(identity2, (0, 1))), basis
    )
    kernels = {
        "inverse_length": (1.0 / math.pi, 1.0 / (2.0 * math.pi)),
        "inverse_square": (1.0 / math.pi**2, 1.0 / (4.0 * math.pi**2)),
        "tunneling": (math.exp(-math.pi), math.exp(-2.0 * math.pi)),
    }
    normalizations = {
        "raw": 1.0,
        "chiral_projector": 1.0 / 2.0,
        "family_trace": 1.0 / 3.0,
        "four_state_trace": 1.0 / 4.0,
        "chiral_family_trace": 1.0 / 6.0,
        "doubled_four_state_trace": 1.0 / 8.0,
        "incidence_channel_average": 1.0 / 12.0,
        "S4_orbit_average": 1.0 / 24.0,
        "signed_chiral_S4_average": 1.0 / 48.0,
    }
    beta_menu = {
        "unit": 1.0,
        "RP3_length": math.pi,
        "S1_length": 2.0 * math.pi,
    }

    rows = []
    for mode in ["modular_generator", "full_Wilson_Hermitian_part"]:
        for kernel_name, (weight_rp3, weight_s1) in kernels.items():
            factor_operator = (
                weight_rp3 * (np.eye(3) - translate_rp3)
                + weight_s1 * (np.eye(3) - translate_s1)
            )
            for orientation_up in [1, -1]:
                for orientation_down in [1, -1]:
                    hamiltonians = []
                    for axis, orientation in zip(
                        axes, [orientation_up, orientation_down]
                    ):
                        generator = 1j * cross_matrix(axis)
                        incidence = cosine * np.eye(3) + (
                            1.0 - cosine
                        ) * np.outer(axis, axis)
                        if mode == "modular_generator":
                            hamiltonian = (
                                factor_operator
                                + orientation * angle * generator
                            )
                        else:
                            hamiltonian = (
                                factor_operator
                                + incidence
                                + orientation
                                * math.sin(angle)
                                * generator
                            )
                        hamiltonians.append(hamiltonian)
                    hamiltonian_up, hamiltonian_down = hamiltonians
                    relative_operator = 0.5j * (
                        hamiltonian_up @ hamiltonian_down
                        - hamiltonian_down @ hamiltonian_up
                    )
                    for normalization, coefficient in normalizations.items():
                        for side in ["up_only", "down_only"]:
                            corrected_up = (
                                hamiltonian_up + coefficient * relative_operator
                                if side == "up_only"
                                else hamiltonian_up
                            )
                            corrected_down = (
                                hamiltonian_down - coefficient * relative_operator
                                if side == "down_only"
                                else hamiltonian_down
                            )
                            eigenvalues_up, vectors_up = np.linalg.eigh(
                                corrected_up
                            )
                            eigenvalues_down, vectors_down = np.linalg.eigh(
                                corrected_down
                            )
                            overlap = (
                                vectors_up[:, ::-1].conjugate().T
                                @ vectors_down[:, ::-1]
                            )
                            for beta_up_name, beta_up in beta_menu.items():
                                for beta_down_name, beta_down in beta_menu.items():
                                    pattern_up = mass_pattern(
                                        eigenvalues_up, beta_up
                                    )
                                    pattern_down = mass_pattern(
                                        eigenvalues_down, beta_down
                                    )
                                    score_up = hierarchy_score(
                                        pattern_up, target_up
                                    )
                                    score_down = hierarchy_score(
                                        pattern_down, target_down
                                    )
                                    rows.append(
                                        {
                                            "mode": mode,
                                            "kernel": kernel_name,
                                            "orientation_up": orientation_up,
                                            "orientation_down": orientation_down,
                                            "normalization": normalization,
                                            "coefficient": coefficient,
                                            "side": side,
                                            "beta_up": beta_up_name,
                                            "beta_down": beta_down_name,
                                            "up_pattern": pattern_up.tolist(),
                                            "down_pattern": pattern_down.tolist(),
                                            "up_log_RMS": score_up,
                                            "down_log_RMS": score_down,
                                            "combined_log_RMS": math.sqrt(
                                                (score_up**2 + score_down**2)
                                                / 2.0
                                            ),
                                            "overlap": overlap,
                                            "corrected_up": corrected_up,
                                            "corrected_down": corrected_down,
                                        }
                                    )

    ordered = sorted(rows, key=lambda row: row["combined_log_RMS"])
    selected = ordered[0]
    shift_up = selected["corrected_up"] + 7.3 * np.eye(3)
    shift_down = selected["corrected_down"] - 4.1 * np.eye(3)
    shifted_up, shifted_vectors_up = np.linalg.eigh(shift_up)
    shifted_down, shifted_vectors_down = np.linalg.eigh(shift_down)
    shifted_overlap = (
        shifted_vectors_up[:, ::-1].conjugate().T
        @ shifted_vectors_down[:, ::-1]
    )
    selected_shift_pattern_up = mass_pattern(
        shifted_up, beta_menu[selected["beta_up"]]
    )
    selected_shift_pattern_down = mass_pattern(
        shifted_down, beta_menu[selected["beta_down"]]
    )

    ckm_control = json.loads(
        Path("s2t_two_layer_physical_ckm_redteam_results.json").read_text(
            encoding="utf-8"
        )
    )["post_blind_PDG_2024_control"]
    selected_angles = mixing_angles(selected["overlap"])
    selected_jarlskog = abs(jarlskog(selected["overlap"]))
    target_angles = np.array(
        [
            ckm_control["sin_theta_12"],
            ckm_control["sin_theta_23"],
            ckm_control["sin_theta_13"],
        ]
    )
    light_ratio_errors = [
        value / target
        for value, target in zip(
            selected["up_pattern"][:-1] + selected["down_pattern"][:-1],
            target_up[:-1].tolist() + target_down[:-1].tolist(),
        )
    ]
    within_factor = {
        str(factor): sum(
            all(
                1.0 / factor <= prediction / target <= factor
                for prediction, target in zip(
                    row["up_pattern"][:-1] + row["down_pattern"][:-1],
                    target_up[:-1].tolist() + target_down[:-1].tolist(),
                )
            )
            for row in rows
        )
        for factor in [2, 3, 5, 10]
    }

    def compact(row):
        return {
            key: value
            for key, value in row.items()
            if key not in {"overlap", "corrected_up", "corrected_down"}
        }

    results = {
        "status": "central_shift_invariant_exponential_readout_improves_mass_hierarchy_but_mass_selected_candidate_fails_blind_CKM_and_no_single_functional_calculus_closes_both",
        "date": "2026-08-06",
        "protocol": {
            "train_data": "up- and down-quark hierarchy ratios at the already declared scales",
            "blind_data": "all CKM angles and Jarlskog invariant",
            "readout": "m_i proportional to exp[-beta(E_i-E_min)]",
            "beta_menu": beta_menu,
            "beta_assignments": "all nine discrete up/down pairs",
            "continuous_fit": False,
        },
        "scan": {
            "candidate_count": len(rows),
            "within_factor_all_four_light_ratios": within_factor,
            "best_rows": [compact(row) for row in ordered[:12]],
        },
        "mass_selected_candidate": {
            **compact(selected),
            "light_ratio_multiplicative_errors": light_ratio_errors,
            "finding": (
                "The mass-only optimum selects beta_u=beta_d=pi. It captures "
                "the two middle ratios and the down first-generation ratio at "
                "order unity, but misses the lightest up ratio by factor 10.24."
            ),
        },
        "central_shift_gate": {
            "up_pattern_error": float(
                np.max(
                    np.abs(
                        selected_shift_pattern_up
                        - np.array(selected["up_pattern"])
                    )
                )
            ),
            "down_pattern_error": float(
                np.max(
                    np.abs(
                        selected_shift_pattern_down
                        - np.array(selected["down_pattern"])
                    )
                )
            ),
            "absolute_overlap_error": float(
                np.max(
                    np.abs(np.abs(shifted_overlap) - np.abs(selected["overlap"]))
                )
            ),
            "theorem": (
                "Normalized exponential functional calculus removes central "
                "offsets exactly because only eigenvalue differences enter."
            ),
        },
        "blind_CKM_gate": {
            "angles": selected_angles.tolist(),
            "control_angles": target_angles.tolist(),
            "angle_ratios": (selected_angles / target_angles).tolist(),
            "absolute_Jarlskog": selected_jarlskog,
            "control_Jarlskog": ckm_control["Jarlskog"],
            "Jarlskog_ratio": selected_jarlskog
            / ckm_control["Jarlskog"],
            "finding": (
                "The mass-selected readout predicts order-one mixing and a "
                "Jarlskog invariant hundreds of times too large."
            ),
        },
        "functional_calculus_no_go": {
            "statement": (
                "For every scalar function f, f(H) has the same spectral "
                "projectors as H. Functional calculus can reshape masses and "
                "remove central offsets but cannot repair a wrong mixing basis."
            ),
            "next_gate": (
                "Introduce a source-derived noncommuting Yukawa insertion or "
                "unequal edge metric that changes eigenvectors, not only "
                "eigenvalues."
            ),
        },
    }

    assert len(rows) == 3888
    assert selected["beta_up"] == "RP3_length"
    assert selected["beta_down"] == "RP3_length"
    assert within_factor["10"] == 0
    assert abs(light_ratio_errors[0] - 10.24208915425299) < 1e-10
    assert results["central_shift_gate"]["up_pattern_error"] < 1e-12
    assert results["central_shift_gate"]["down_pattern_error"] < 1e-12
    assert results["central_shift_gate"]["absolute_overlap_error"] < 1e-12
    assert results["blind_CKM_gate"]["Jarlskog_ratio"] > 300

    Path("s2t_exponential_yukawa_readout_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "candidate_count": len(rows),
                "best_mass_score": selected["combined_log_RMS"],
                "best_betas": [selected["beta_up"], selected["beta_down"]],
                "light_ratio_errors": light_ratio_errors,
                "Jarlskog_ratio": results["blind_CKM_gate"][
                    "Jarlskog_ratio"
                ],
                "angle_ratios": results["blind_CKM_gate"]["angle_ratios"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()