#!/usr/bin/env python3
import json
import math
from pathlib import Path

import numpy as np

from s2t_shared_holonomy_two_sector_audit import (
    affine_permutation,
    permutation_matrix,
    restrict,
    triplet_basis,
)


def cross_matrix(axis):
    x_value, y_value, z_value = axis
    return np.array(
        [
            [0.0, -z_value, y_value],
            [z_value, 0.0, -x_value],
            [-y_value, x_value, 0.0],
        ]
    )


def jarlskog(unitary):
    return float(
        np.imag(
            unitary[0, 0]
            * unitary[1, 1]
            * np.conjugate(unitary[0, 1])
            * np.conjugate(unitary[1, 0])
        )
    )


def main():
    wilson = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    cosine = wilson["continuous_two_sector_solution"]["cos_theta_numeric"]
    phase = wilson["continuous_two_sector_solution"]["phase"]
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

    base_rows = []
    direct_cocycle_rows = []
    bch_rows = []
    modular_times = [0.5, 1.0, phase]
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
                    eigenvalues_up, eigenvectors_up = np.linalg.eigh(
                        hamiltonian_up
                    )
                    eigenvalues_down, eigenvectors_down = np.linalg.eigh(
                        hamiltonian_down
                    )
                    base_overlap = (
                        eigenvectors_up.conjugate().T @ eigenvectors_down
                    )
                    base_jarlskog = jarlskog(base_overlap)
                    base_rows.append(
                        {
                            "mode": mode,
                            "kernel": kernel_name,
                            "orientation_up": orientation_up,
                            "orientation_down": orientation_down,
                            "Jarlskog": base_jarlskog,
                        }
                    )

                    for modular_time in modular_times:
                        row_phases = np.diag(
                            np.exp(-1j * modular_time * eigenvalues_up)
                        )
                        column_phases = np.diag(
                            np.exp(1j * modular_time * eigenvalues_down)
                        )
                        cocycle_overlap = (
                            row_phases @ base_overlap @ column_phases
                        )
                        direct_cocycle_rows.append(
                            {
                                "mode": mode,
                                "kernel": kernel_name,
                                "orientation_up": orientation_up,
                                "orientation_down": orientation_down,
                                "modular_time": modular_time,
                                "base_Jarlskog": base_jarlskog,
                                "cocycle_Jarlskog": jarlskog(
                                    cocycle_overlap
                                ),
                                "difference": abs(
                                    jarlskog(cocycle_overlap)
                                    - base_jarlskog
                                ),
                            }
                        )

                    commutator_correction = 0.5j * (
                        hamiltonian_up @ hamiltonian_down
                        - hamiltonian_down @ hamiltonian_up
                    )
                    for scheme in [
                        "antisymmetric_two_sided",
                        "up_only",
                        "down_only",
                    ]:
                        if scheme == "antisymmetric_two_sided":
                            corrected_up = (
                                hamiltonian_up + commutator_correction
                            )
                            corrected_down = (
                                hamiltonian_down - commutator_correction
                            )
                        elif scheme == "up_only":
                            corrected_up = (
                                hamiltonian_up + commutator_correction
                            )
                            corrected_down = hamiltonian_down
                        else:
                            corrected_up = hamiltonian_up
                            corrected_down = (
                                hamiltonian_down - commutator_correction
                            )

                        _, corrected_vectors_up = np.linalg.eigh(corrected_up)
                        _, corrected_vectors_down = np.linalg.eigh(
                            corrected_down
                        )
                        corrected_overlap = (
                            corrected_vectors_up.conjugate().T
                            @ corrected_vectors_down
                        )
                        bch_rows.append(
                            {
                                "mode": mode,
                                "kernel": kernel_name,
                                "orientation_up": orientation_up,
                                "orientation_down": orientation_down,
                                "scheme": scheme,
                                "commutator_norm": float(
                                    np.linalg.norm(commutator_correction)
                                ),
                                "minimum_absolute_overlap": float(
                                    np.min(np.abs(corrected_overlap))
                                ),
                                "Jarlskog": jarlskog(corrected_overlap),
                            }
                        )

    symmetric_rows = [
        row
        for row in bch_rows
        if row["scheme"] == "antisymmetric_two_sided"
    ]
    one_sided_rows = [
        row for row in bch_rows if row["scheme"] != "antisymmetric_two_sided"
    ]
    physical_control = 3.12e-5
    nonzero_one_sided = [
        abs(row["Jarlskog"])
        for row in one_sided_rows
        if abs(row["Jarlskog"]) > 1e-12
    ]
    results = {
        "status": "direct_relative_cocycle_is_a_rephasing_no_go_while_one_sided_BCH_backreaction_creates_CP_but_overshoots_and_requires_a_new_sector_asymmetry",
        "date": "2026-08-06",
        "blind_protocol": {
            "CKM_loaded_during_construction": False,
            "input_hamiltonians": (
                "the two oriented Wilson classes, three frozen factor kernels "
                "and four relative orientation pairs"
            ),
            "BCH_coefficient": "canonical one-half commutator coefficient",
            "post_blind_control": physical_control,
        },
        "base_gate": {
            "sector_pairs": len(base_rows),
            "all_base_CP_conserving": all(
                abs(row["Jarlskog"]) < 1e-12 for row in base_rows
            ),
        },
        "direct_cocycle_gate": {
            "formula": (
                "V(t)=diag(exp(-it h_u)) V "
                "diag(exp(+it h_d)) in the two eigenbases"
            ),
            "tested_times": modular_times,
            "tests": len(direct_cocycle_rows),
            "maximum_Jarlskog_change": max(
                row["difference"] for row in direct_cocycle_rows
            ),
            "theorem": (
                "The direct finite-dimensional Connes cocycle acts as row and "
                "column rephasing on the mixing matrix, so every rephasing "
                "invariant including J is unchanged."
            ),
            "finding": (
                "A direct relative modular cocycle cannot turn a CP-conserving "
                "overlap into CKM CP violation."
            ),
        },
        "BCH_commutator_gate": {
            "relative_operator": "Q=(i/2)[H_u,H_d]",
            "rows": bch_rows,
            "symmetric_two_sided": {
                "tests": len(symmetric_rows),
                "nonzero_CP": sum(
                    abs(row["Jarlskog"]) > 1e-12
                    for row in symmetric_rows
                ),
                "maximum_absolute_J": max(
                    abs(row["Jarlskog"]) for row in symmetric_rows
                ),
                "finding": (
                    "Adding +Q to one sector and -Q to the other preserves a "
                    "CP-conserving relation."
                ),
            },
            "one_sided": {
                "tests": len(one_sided_rows),
                "nonzero_CP": len(nonzero_one_sided),
                "minimum_absolute_J": min(nonzero_one_sided),
                "maximum_absolute_J": max(nonzero_one_sided),
                "control_J": physical_control,
                "minimum_overshoot_factor": min(nonzero_one_sided)
                / physical_control,
                "sign_pairing": (
                    "up-only and down-only corrections produce opposite J signs"
                ),
                "finding": (
                    "The first canonical commutator can create CP only through "
                    "an asymmetric sector backreaction. With coefficient one-half "
                    "all candidates overshoot the observed J scale."
                ),
            },
        },
        "scientific_verdict": {
            "positive": (
                "The relative modular commutator is the first coefficient-free "
                "operator in this chain that produces nonzero three-family CP."
            ),
            "negative": (
                "The direct cocycle is pure rephasing; symmetric backreaction "
                "still gives zero CP; one-sided backreaction is not yet derived "
                "and its canonical magnitude is at least about forty times too large."
            ),
            "next_gate": (
                "Derive a chiral or charge-asymmetric coupling of Q from the "
                "finite algebra and parent action. Its coefficient must be fixed "
                "before data and simultaneously pass a mass-hierarchy observable."
            ),
        },
    }

    assert len(base_rows) == 24
    assert len(direct_cocycle_rows) == 72
    assert results["base_gate"]["all_base_CP_conserving"]
    assert results["direct_cocycle_gate"]["maximum_Jarlskog_change"] < 1e-12
    assert len(symmetric_rows) == 24
    assert results["BCH_commutator_gate"]["symmetric_two_sided"][
        "nonzero_CP"
    ] == 0
    assert len(one_sided_rows) == 48
    assert len(nonzero_one_sided) == 48
    assert (
        results["BCH_commutator_gate"]["one_sided"][
            "minimum_overshoot_factor"
        ]
        > 30
    )

    Path("s2t_relative_modular_cocycle_bch_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "direct_cocycle_tests": len(direct_cocycle_rows),
                "direct_cocycle_max_delta_J": results[
                    "direct_cocycle_gate"
                ]["maximum_Jarlskog_change"],
                "symmetric_BCH_nonzero_CP": 0,
                "one_sided_BCH_nonzero_CP": len(nonzero_one_sided),
                "one_sided_min_J": min(nonzero_one_sided),
                "one_sided_min_overshoot": results[
                    "BCH_commutator_gate"
                ]["one_sided"]["minimum_overshoot_factor"],
                "next_gate": results["scientific_verdict"]["next_gate"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()