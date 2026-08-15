import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
FULL_DIMENSION = 24
BASE_MASS = 2.5

kernel_vector = np.zeros(FULL_DIMENSION)
kernel_vector[0] = 1.0
p_kernel = np.outer(kernel_vector, kernel_vector)
p_heavy = np.eye(FULL_DIMENSION) - p_kernel
heavy_rank = int(np.linalg.matrix_rank(p_heavy))

mass_rank_only = BASE_MASS * p_heavy
mass_rank_only_pinv = np.linalg.pinv(mass_rank_only)

democratic = np.zeros(FULL_DIMENSION)
democratic[1:] = 1.0
democratic_normalized = democratic / np.linalg.norm(democratic)


def seesaw_contraction(coupling, inverse_mass):
    return float(coupling @ inverse_mass @ coupling)


normalized_rank_only = seesaw_contraction(democratic_normalized, mass_rank_only_pinv)
unnormalized_rank_only = seesaw_contraction(democratic, mass_rank_only_pinv)

d_nu = heavy_rank + 1.0 / PI
mass_desired = BASE_MASS * d_nu * p_heavy
mass_desired_pinv = np.linalg.pinv(mass_desired)
normalized_desired = seesaw_contraction(democratic_normalized, mass_desired_pinv)

nonzero_eigenvalues = np.linalg.eigvalsh(mass_rank_only)
nonzero_eigenvalues = nonzero_eigenvalues[np.abs(nonzero_eigenvalues) > 1e-12]
log_pseudodeterminant = float(np.sum(np.log(nonzero_eigenvalues)))

rng = np.random.default_rng(20260803)
random_matrix = rng.normal(size=(heavy_rank, heavy_rank))
orthogonal_heavy, _ = np.linalg.qr(random_matrix)
orthogonal_full = np.eye(FULL_DIMENSION)
orthogonal_full[1:, 1:] = orthogonal_heavy

invariance_errors = {}
for scalar in [1.0, 2.0, float(heavy_rank), d_nu]:
    invariant_mass = scalar * p_heavy
    invariance_errors[str(scalar)] = float(
        np.max(np.abs(orthogonal_full @ invariant_mass @ orthogonal_full.T - invariant_mass))
    )

results = {
    "status": "global_defect_action_candidate_exists_rank23_does_not_fix_tree_level_denominator",
    "date": "2026-08-03",
    "global_tubular_action_candidate": {
        "tube": "N(gamma), the solid-torus tubular neighborhood of the systolic core",
        "quadratic_action": "S_tube=(1/2) integral_N(gamma) <Psi,B_Phi Psi>",
        "operator": "B_Phi=Dirac_Sroot + Phi_1 Gamma_1 + Phi_2 Gamma_2",
        "field_data": (
            "Psi is the Majorana/Nambu spinor with the square-root torsion transition; "
            "Phi is the charge-two pairing section with forced unit winding."
        ),
        "asymptotic_mass_input": (
            "The magnitude of Phi may be identified with the already declared heavy scale M_*; "
            "its topological profile adds no continuous fit parameter."
        ),
        "cycle_vertex": (
            "S_Y on gamma uses the normalized kernel restriction R_gamma and the existing row "
            "(m_e^2/m_mu) v^T Qcycle^(1/2)."
        ),
        "status": "well_defined_EFT_candidate_global_operator_coefficients_not_derived_from_S2T_spectral_action",
    },
    "finite_heavy_quotient": {
        "full_dimension": FULL_DIMENSION,
        "kernel_rank": int(np.linalg.matrix_rank(p_kernel)),
        "heavy_projector_rank": heavy_rank,
        "projector_idempotence_error": float(np.max(np.abs(p_heavy @ p_heavy - p_heavy))),
        "rank_only_mass_operator": "M0*P_heavy",
        "rank_only_mass_eigenvalues": np.linalg.eigvalsh(mass_rank_only).tolist(),
        "self_adjointness_error": float(np.max(np.abs(mass_rank_only.T - mass_rank_only))),
    },
    "tree_level_seesaw_test": {
        "normalized_democratic_coupling": normalized_rank_only,
        "expected_normalized": 1.0 / BASE_MASS,
        "unnormalized_democratic_coupling": unnormalized_rank_only,
        "expected_unnormalized": heavy_rank / BASE_MASS,
        "interpretation": (
            "With a canonically normalized light-to-heavy vector, the rank cancels. With equal "
            "unnormalized couplings, rank 23 appears in the numerator. Neither case produces a "
            "tree-level denominator 23."
        ),
    },
    "determinant_test": {
        "log_pseudodeterminant": log_pseudodeterminant,
        "expected": heavy_rank * math.log(BASE_MASS),
        "interpretation": (
            "The quotient rank enters the Gaussian determinant multiplicity as 23*log(M0), not as "
            "a mass eigenvalue 23*M0."
        ),
    },
    "symmetry_test": {
        "heavy_symmetry": "O(23) acting on im(P_heavy)",
        "invariance_errors_for_multiple_scalars": invariance_errors,
        "conclusion": (
            "O(23) covariance fixes the mass operator to m*P_heavy but leaves the scalar m arbitrary. "
            "Symmetry and rank alone cannot select m=23*M0."
        ),
    },
    "desired_denominator_operator": {
        "operator": "M0*(Tr(P_heavy)+pi^(-1))*P_heavy",
        "D_nu": d_nu,
        "normalized_seesaw_contraction": normalized_desired,
        "expected": 1.0 / (BASE_MASS * d_nu),
        "status": (
            "algebraically_works_but_the_trace_normalization_rule_is_an_additional_action_principle"
        ),
    },
    "action_level_gate": {
        "closed": [
            "global tubular EFT operator can be written",
            "square-root transition and odd pairing winding are compatible",
            "one real kernel and rank-23 heavy quotient are consistent",
            "Qcycle Yukawa row can be attached through the normalized restriction map",
        ],
        "open": [
            "derive why the heavy mass scalar equals Tr(P_heavy)+pi^(-1)",
            "show whether this scalar arises from a one-loop self-energy, spectral trace, or collective stiffness",
            "avoid defining the desired denominator directly in the mass operator",
        ],
    },
    "theory_effect": {
        "rank_one_defect": "retained",
        "rank_23_heavy_quotient": "retained",
        "D_nu_23_plus_inverse_pi": "not_yet_derived_at_action_level",
        "global_BdG_EFT": "constructed_conditionally",
        "next_target": "derive a trace-induced collective mass normalization in the same action",
    },
    "verdict": (
        "The global defect EFT can be written consistently and its heavy quotient has rank 23, but "
        "a tree-level quadratic action does not turn that rank into the mass denominator 23. "
        "Canonical coupling removes the rank; unnormalized democratic coupling puts it in the "
        "numerator; the Gaussian determinant contains 23 log(M0). Recovering D_nu requires a new "
        "derived collective normalization, such as a spectral or loop self-energy proportional to "
        "Tr(P_heavy), rather than the rank count alone."
    ),
}

assert heavy_rank == 23
assert abs(normalized_rank_only - 1.0 / BASE_MASS) < 1e-12
assert abs(unnormalized_rank_only - heavy_rank / BASE_MASS) < 1e-12
assert abs(log_pseudodeterminant - heavy_rank * math.log(BASE_MASS)) < 1e-12
assert all(error < 1e-12 for error in invariance_errors.values())
assert abs(normalized_desired - 1.0 / (BASE_MASS * d_nu)) < 1e-12

Path("s2t_neutrino_global_action_denominator_gate_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "heavy_rank": heavy_rank,
            "normalized_rank_only": normalized_rank_only,
            "unnormalized_rank_only": unnormalized_rank_only,
            "log_pseudodeterminant": log_pseudodeterminant,
            "D_nu_status": results["theory_effect"]["D_nu_23_plus_inverse_pi"],
        },
        indent=2,
        ensure_ascii=False,
    )
)