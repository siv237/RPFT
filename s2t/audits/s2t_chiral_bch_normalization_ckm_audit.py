#!/usr/bin/env python3
import itertools
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


def mixing_angles(unitary):
    sin_theta_13 = abs(unitary[0, 2])
    cos_theta_13 = math.sqrt(max(0.0, 1.0 - sin_theta_13**2))
    if cos_theta_13 == 0.0:
        return np.ones(3)
    return np.array(
        [
            abs(unitary[0, 1]) / cos_theta_13,
            abs(unitary[1, 2]) / cos_theta_13,
            sin_theta_13,
        ]
    )


def control_matrix(control):
    sin12, sin23, sin13 = (
        control["sin_theta_12"],
        control["sin_theta_23"],
        control["sin_theta_13"],
    )
    cos12, cos23, cos13 = (
        math.sqrt(1.0 - sin12**2),
        math.sqrt(1.0 - sin23**2),
        math.sqrt(1.0 - sin13**2),
    )
    phase = np.exp(1j * control["delta_radians"])
    return np.array(
        [
            [cos12 * cos13, sin12 * cos13, sin13 / phase],
            [
                -sin12 * cos23 - cos12 * sin23 * sin13 * phase,
                cos12 * cos23 - sin12 * sin23 * sin13 * phase,
                sin23 * cos13,
            ],
            [
                sin12 * sin23 - cos12 * cos23 * sin13 * phase,
                -cos12 * sin23 - sin12 * cos23 * sin13 * phase,
                cos23 * cos13,
            ],
        ]
    )


def compact(row):
    return {
        key: value
        for key, value in row.items()
        if key not in {"overlap", "fixed_order_angles"}
    }


def main():
    wilson = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
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
    normalization_menu = {
        "raw": 1.0,
        "chiral_projector": 1.0 / 2.0,
        "family_normalized_trace": 1.0 / 3.0,
        "four_state_normalized_trace": 1.0 / 4.0,
        "chiral_family_trace": 1.0 / 6.0,
        "doubled_four_state_trace": 1.0 / 8.0,
        "incidence_channel_average": 1.0 / 12.0,
        "S4_orbit_average": 1.0 / 24.0,
        "signed_chiral_S4_average": 1.0 / 48.0,
    }

    candidates = []
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
                    for normalization, coefficient in normalization_menu.items():
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
                            vectors_up = np.linalg.eigh(corrected_up)[1]
                            vectors_down = np.linalg.eigh(corrected_down)[1]
                            candidates.append(
                                {
                                    "mode": mode,
                                    "kernel": kernel_name,
                                    "orientation_up": orientation_up,
                                    "orientation_down": orientation_down,
                                    "normalization": normalization,
                                    "coefficient": coefficient,
                                    "side": side,
                                    "overlap": vectors_up.conjugate().T
                                    @ vectors_down,
                                }
                            )

    control = json.loads(
        Path("s2t_two_layer_physical_ckm_redteam_results.json").read_text(
            encoding="utf-8"
        )
    )["post_blind_PDG_2024_control"]
    target_angles = np.array(
        [
            control["sin_theta_12"],
            control["sin_theta_23"],
            control["sin_theta_13"],
        ]
    )
    target_matrix = control_matrix(control)
    permutations = list(itertools.permutations(range(3)))
    scored = []
    for candidate in candidates:
        overlap = candidate["overlap"]
        absolute_jarlskog = abs(jarlskog(overlap))
        best = None
        for row_order in permutations:
            for column_order in permutations:
                permuted = overlap[np.ix_(row_order, column_order)]
                angles = mixing_angles(permuted)
                trial = {
                    "matrix_score": float(
                        np.linalg.norm(
                            np.abs(permuted) - np.abs(target_matrix)
                        )
                    ),
                    "angle_log_rms": float(
                        np.sqrt(
                            np.mean(
                                np.log(
                                    np.maximum(angles, 1e-15)
                                    / target_angles
                                )
                                ** 2
                            )
                        )
                    ),
                    "row_permutation": row_order,
                    "column_permutation": column_order,
                    "angles": angles.tolist(),
                }
                if best is None or (
                    trial["matrix_score"],
                    trial["angle_log_rms"],
                ) < (best["matrix_score"], best["angle_log_rms"]):
                    best = trial
        scored.append(
            {
                **candidate,
                "absolute_Jarlskog": absolute_jarlskog,
                "Jarlskog_ratio_to_control": (
                    absolute_jarlskog / control["Jarlskog"]
                ),
                "fixed_order_angles": mixing_angles(overlap).tolist(),
                "best_permutation": best,
            }
        )

    factor_two = [
        row
        for row in scored
        if 0.5 <= row["Jarlskog_ratio_to_control"] <= 2.0
    ]
    angle_successes = [
        row
        for row in factor_two
        if all(
            0.5 <= value / target <= 2.0
            for value, target in zip(
                row["best_permutation"]["angles"], target_angles
            )
        )
    ]
    closest_j = sorted(
        scored,
        key=lambda row: abs(math.log(row["Jarlskog_ratio_to_control"])),
    )
    best_full = sorted(
        factor_two,
        key=lambda row: row["best_permutation"]["matrix_score"],
    )
    aggregates = {}
    for name, coefficient in normalization_menu.items():
        rows = [row for row in scored if row["normalization"] == name]
        closest = min(
            rows,
            key=lambda row: abs(math.log(row["Jarlskog_ratio_to_control"])),
        )
        aggregates[name] = {
            "coefficient": coefficient,
            "minimum_absolute_J": min(
                row["absolute_Jarlskog"] for row in rows
            ),
            "maximum_absolute_J": max(
                row["absolute_Jarlskog"] for row in rows
            ),
            "closest_J_ratio": closest["Jarlskog_ratio_to_control"],
            "best_permuted_matrix_score": min(
                row["best_permutation"]["matrix_score"] for row in rows
            ),
        }

    results = {
        "status": "natural_finite_algebra_normalizations_can_match_J_alone_but_no_candidate_reproduces_the_full_CKM_hierarchy_and_masses_remain_centrally_unidentified",
        "date": "2026-08-06",
        "blind_protocol": {
            "normalization_menu_frozen_before_CKM": True,
            "candidate_matrices_generated_before_control": True,
            "menu_origin": (
                "inverse dimensions from chiral doubling, normalized traces, "
                "incidence channels and S4 orbit averages"
            ),
            "CKM_use": "post-blind scoring only",
        },
        "scan": {
            "normalization_menu": normalization_menu,
            "candidate_count": len(scored),
            "permutation_controls_per_candidate": 36,
            "aggregate_by_normalization": aggregates,
        },
        "post_blind_CKM_gate": {
            "control": control,
            "J_within_factor_two_count": len(factor_two),
            "all_three_angles_within_factor_two_count": len(angle_successes),
            "closest_J_candidates": [
                compact(row) for row in closest_j[:12]
            ],
            "best_full_matrix_candidates_among_J_factor_two": [
                compact(row) for row in best_full[:12]
            ],
            "best_angle_log_rms_among_J_factor_two": min(
                row["best_permutation"]["angle_log_rms"]
                for row in factor_two
            ),
            "best_matrix_score_among_J_factor_two": min(
                row["best_permutation"]["matrix_score"]
                for row in factor_two
            ),
            "finding": (
                "Dimension-derived coefficients can reproduce J at percent "
                "level, but after all generation permutations no candidate "
                "reproduces the hierarchical three-angle CKM pattern."
            ),
        },
        "mass_hierarchy_gate": {
            "theorem": (
                "H_u to H_u+c_u I and H_d to H_d+c_d I leave eigenvectors, "
                "mixing and J unchanged while continuously changing every "
                "eigenvalue ratio."
            ),
            "consequence": (
                "Mass hierarchies are not identified until a parent action "
                "fixes central offsets and a positive Yukawa readout."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "Finite-algebra dimensions naturally reach the suppression "
                "scale of the observed Jarlskog invariant."
            ),
            "negative": (
                "Matching J alone fails the full CKM gate, and masses remain "
                "nonidentifiable under central shifts."
            ),
            "next_gate": (
                "Derive unequal family-edge metrics or a noncentral Yukawa "
                "readout that fixes central offsets and all three mixing angles."
            ),
        },
    }
    assert len(scored) == 432
    assert len(factor_two) == 52
    assert not angle_successes
    assert abs(closest_j[0]["Jarlskog_ratio_to_control"] - 1.0) < 0.02
    assert results["post_blind_CKM_gate"][
        "best_angle_log_rms_among_J_factor_two"
    ] > 1.0
    assert results["post_blind_CKM_gate"][
        "best_matrix_score_among_J_factor_two"
    ] > 0.8

    Path("s2t_chiral_bch_normalization_ckm_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "candidate_count": len(scored),
                "J_within_factor_two": len(factor_two),
                "all_angles_within_factor_two": len(angle_successes),
                "closest_J_ratio": closest_j[0][
                    "Jarlskog_ratio_to_control"
                ],
                "best_angle_log_rms": results["post_blind_CKM_gate"][
                    "best_angle_log_rms_among_J_factor_two"
                ],
                "best_matrix_score": results["post_blind_CKM_gate"][
                    "best_matrix_score_among_J_factor_two"
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()