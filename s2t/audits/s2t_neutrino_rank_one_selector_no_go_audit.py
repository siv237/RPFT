import json
import math
from pathlib import Path

import numpy as np


def projector(vector):
    vector = np.asarray(vector, dtype=float)
    vector = vector / np.linalg.norm(vector)
    return np.outer(vector, vector)


def matrix_rank(matrix, tolerance=1e-10):
    return int(np.linalg.matrix_rank(matrix, tol=tolerance))


identity4 = np.eye(4)
left_i = np.array(
    [
        [0, -1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, -1],
        [0, 0, 1, 0],
    ],
    dtype=float,
)
left_j = np.array(
    [
        [0, 0, -1, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0],
        [0, -1, 0, 0],
    ],
    dtype=float,
)
left_k = left_i @ left_j
quaternion_group = [
    identity4,
    -identity4,
    left_i,
    -left_i,
    left_j,
    -left_j,
    left_k,
    -left_k,
]

spin_seed_projector = projector([1, 0, 0, 0])
spin_reynolds_average = sum(
    group_element @ spin_seed_projector @ group_element.T
    for group_element in quaternion_group
) / len(quaternion_group)

generation_singlet = np.ones(3) / math.sqrt(3)
cycle_self_dual = np.ones(2) / math.sqrt(2)
p_generation = projector(generation_singlet)
p_cycle = projector(cycle_self_dual)
p_spin = identity4

canonical_joint_projector = np.kron(np.kron(p_generation, p_spin), p_cycle)
full_dimension = 3 * 4 * 2
canonical_rank = matrix_rank(canonical_joint_projector)


def rp3_dirac_multiplicity(k, spin_structure, sign):
    sphere_half_coefficient = math.comb(k + 2, 2)
    parity = (-1) ** k
    if spin_structure == "tau_plus":
        factor = 1 - parity if sign == "+" else 1 + parity
    else:
        factor = 1 + parity if sign == "+" else 1 - parity
    return sphere_half_coefficient * factor


rp3_low_shells = []
for spin_structure in ["tau_plus", "tau_minus"]:
    for k in range(4):
        rp3_low_shells.append(
            {
                "spin_structure": spin_structure,
                "k": k,
                "absolute_eigenvalue": k + 1.5,
                "positive_complex_multiplicity": rp3_dirac_multiplicity(k, spin_structure, "+"),
                "negative_complex_multiplicity": rp3_dirac_multiplicity(k, spin_structure, "-"),
            }
        )

lowest_real_rank = 2 * max(
    rp3_dirac_multiplicity(0, "tau_plus", "+"),
    rp3_dirac_multiplicity(0, "tau_plus", "-"),
)

commutator_errors = {
    "left_i": float(np.max(np.abs(left_i @ spin_reynolds_average - spin_reynolds_average @ left_i))),
    "left_j": float(np.max(np.abs(left_j @ spin_reynolds_average - spin_reynolds_average @ left_j))),
    "left_k": float(np.max(np.abs(left_k @ spin_reynolds_average - spin_reynolds_average @ left_k))),
}

results = {
    "status": "symmetry_protected_rank_one_selector_not_available_minimal_covariant_rank_is_four",
    "date": "2026-08-03",
    "module": {
        "factorization": "R3_generation tensor R4_lowest_RP3_spinor tensor R2_cycle",
        "full_real_dimension": full_dimension,
        "generation_singlet_rank": matrix_rank(p_generation),
        "lowest_RP3_spinor_real_rank": lowest_real_rank,
        "self_dual_cycle_rank": matrix_rank(p_cycle),
        "joint_canonical_rank": canonical_rank,
    },
    "spin_covariance_test": {
        "finite_exact_subgroup": "Q8 acting by left quaternion multiplication on R4",
        "reason": (
            "Q8 is sufficient for the obstruction: left multiplication by i squares to -I, "
            "so it has no invariant real line. A rank-one real projector cannot commute with it."
        ),
        "reynolds_average_of_rank_one_seed": spin_reynolds_average.tolist(),
        "expected_average": (identity4 / 4).tolist(),
        "average_error": float(np.max(np.abs(spin_reynolds_average - identity4 / 4))),
        "support_rank_after_symmetry_average": matrix_rank(spin_reynolds_average),
        "commutator_errors": commutator_errors,
    },
    "RP3_dirac_spectrum": {
        "generating_functions": {
            "tau_plus": {
                "F_plus": "(1-z)^(-3)-(1+z)^(-3)",
                "F_minus": "(1-z)^(-3)+(1+z)^(-3)",
            },
            "tau_minus": "positive and negative branches exchanged",
        },
        "low_shells": rp3_low_shells,
        "lowest_absolute_eigenvalue": 1.5,
        "lowest_nonzero_complex_multiplicity": 2,
        "lowest_nonzero_real_rank": lowest_real_rank,
        "consequence": (
            "Choosing a spin structure selects the sign of the lowest branch but not a single "
            "spinor polarization. The lowest covariant eigenspace remains four-dimensional over R."
        ),
    },
    "dimension_options": {
        "remove_full_generation_singlet_spinor_cycle_module": {
            "removed_rank": 8,
            "remaining_rank": 16,
        },
        "remove_generation_singlet_self_dual_lowest_spinor_module": {
            "removed_rank": canonical_rank,
            "remaining_rank": full_dimension - canonical_rank,
        },
        "remove_one_vector": {
            "removed_rank": 1,
            "remaining_rank": 23,
            "symmetry_status": "requires explicit spin-polarization breaking or extra structure",
        },
    },
    "no_go_statement": (
        "The declared exact data S3 generation symmetry, the RP3 Dirac operator and spin/isometry "
        "covariance, and cycle self-duality do not select a real line in R24. They select at best "
        "generation-singlet tensor lowest-spinor tensor self-dual-cycle, whose real rank is four. "
        "A rank-one projector therefore cannot be symmetry-protected without adding a new spinor "
        "polarization, boundary/defect datum, condensate, or explicit symmetry breaking."
    ),
    "theory_effect": {
        "rank_23_denominator": "no_go_under_current_exact_symmetries",
        "smallest_current_covariant_removed_block": 4,
        "conditional_remaining_rank_if_that_block_is_removed": 20,
        "Qcycle": "retained",
        "cycle_seesaw_contraction": "retained",
        "neutrino_mass_prediction": "open",
    },
    "next_steps": [
        "do not search for rank one inside the unchanged symmetric module",
        "either derive a physical defect or condensate that selects a spinor polarization",
        "or rebuild the denominator using a covariant removed block of rank four or eight",
        "treat any choice of a single Killing spinor as new symmetry-breaking input",
    ],
}

assert full_dimension == 24
assert canonical_rank == 4
assert lowest_real_rank == 4
assert np.max(np.abs(spin_reynolds_average - identity4 / 4)) < 1e-12
assert all(error < 1e-12 for error in commutator_errors.values())

Path("s2t_neutrino_rank_one_selector_no_go_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "full_dimension": full_dimension,
            "canonical_joint_rank": canonical_rank,
            "lowest_RP3_spinor_real_rank": lowest_real_rank,
            "rank_23_status": results["theory_effect"]["rank_23_denominator"],
        },
        indent=2,
        ensure_ascii=False,
    )
)