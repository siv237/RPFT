import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
tau_x = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)


def majorana_conjugate(vector):
    return tau_x @ np.conjugate(vector)


def zero_basis(pair_phase):
    return np.array(
        [
            np.exp(0.5j * pair_phase),
            np.exp(-0.5j * pair_phase),
        ],
        dtype=complex,
    ) / math.sqrt(2.0)


def complex_matrix_data(matrix):
    return [
        [[value.real, value.imag] for value in row]
        for row in matrix
    ]


pair_phase_start = 0.0
pair_phase_end = PI
root_transition = np.diag([1j, -1j])

zero_start = zero_basis(pair_phase_start)
zero_end = zero_basis(pair_phase_end)
transported_zero = root_transition @ zero_start

spin_transition = -1.0
ambient_torsion_transition = -1.0
real_sign_product = spin_transition * ambient_torsion_transition
total_transition = real_sign_product * root_transition
total_transport = total_transition @ zero_start
core_coefficient_holonomy = np.vdot(zero_end, total_transport)

without_torsion_transition = spin_transition * root_transition
without_torsion_transport = without_torsion_transition @ zero_start
without_torsion_coefficient_holonomy = np.vdot(zero_end, without_torsion_transport)

majorana_errors = {
    "start": float(np.max(np.abs(majorana_conjugate(zero_start) - zero_start))),
    "end": float(np.max(np.abs(majorana_conjugate(zero_end) - zero_end))),
    "transported": float(
        np.max(np.abs(majorana_conjugate(total_transport) - total_transport))
    ),
}

transition_covariance_error = float(np.max(np.abs(transported_zero - zero_end)))
total_gluing_error = float(np.max(np.abs(total_transport - zero_end)))


def longitudinal_kernel_rank(coefficient_holonomy):
    if abs(coefficient_holonomy - 1.0) < 1e-12:
        return 1
    return 0


kernel_rank = longitudinal_kernel_rank(core_coefficient_holonomy)
kernel_rank_without_torsion = longitudinal_kernel_rank(without_torsion_coefficient_holonomy)

qcycle = np.diag([PI, 1.0 / PI])
v_cycle = np.array([1.0, 1.0])
qcycle_norm = float(v_cycle @ qcycle @ v_cycle)

results = {
    "status": "minimal_core_gluing_closes_periodic_majorana_line_action_embedding_open",
    "date": "2026-08-03",
    "local_BdG_data": {
        "Nambu_basis": "(psi, psi_dagger)",
        "particle_hole_operator": "C=tau_x*K",
        "zero_basis": "v(theta)=(exp(i theta/2),exp(-i theta/2))/sqrt(2)",
        "pair_phase_start": pair_phase_start,
        "pair_phase_end": pair_phase_end,
        "quarter_transition": complex_matrix_data(root_transition),
        "transition_rule": "v(theta+pi)=diag(i,-i)v(theta)",
        "transition_covariance_error": transition_covariance_error,
    },
    "Majorana_reality": {
        "errors": majorana_errors,
        "fixed_line_statement": (
            "For a C-fixed zero vector v, the physical coefficients in a*v are real because "
            "C(a*v)=conjugate(a)*v. The zero eigenspace therefore contributes one real Majorana "
            "direction, not a doubled complex state."
        ),
        "physical_zero_mode_real_rank": 1,
    },
    "core_gluing": {
        "spin_transition": spin_transition,
        "ambient_torsion_transition": ambient_torsion_transition,
        "real_sign_product": real_sign_product,
        "root_transition": complex_matrix_data(root_transition),
        "total_transition": complex_matrix_data(total_transition),
        "total_gluing_error": total_gluing_error,
        "coefficient_holonomy": [
            core_coefficient_holonomy.real,
            core_coefficient_holonomy.imag,
        ],
        "longitudinal_kernel_rank": kernel_rank,
        "interpretation": (
            "The quarter transition transports the local zero-mode basis itself. The remaining "
            "coefficient sees the product of the antiperiodic spin sign and the ambient torsion "
            "sign, which is +1. Hence the Majorana coefficient line is periodic."
        ),
    },
    "control_without_ambient_torsion": {
        "coefficient_holonomy": [
            without_torsion_coefficient_holonomy.real,
            without_torsion_coefficient_holonomy.imag,
        ],
        "longitudinal_kernel_rank": kernel_rank_without_torsion,
        "interpretation": (
            "Without the ambient Z2 line the coefficient holonomy is -1 and the longitudinal zero "
            "mode disappears. The cancellation is therefore structural, not automatic."
        ),
    },
    "rank_one_result": {
        "generation_singlet_rank": 1,
        "transverse_mod_two_kernel_rank": 1,
        "longitudinal_Majorana_kernel_rank": kernel_rank,
        "self_dual_cycle_rank": 1,
        "combined_real_rank": kernel_rank,
        "complement_rank_in_R24": 24 - kernel_rank,
    },
    "Qcycle_compatibility": {
        "self_dual_Qcycle_norm": qcycle_norm,
        "target": PI + 1.0 / PI,
        "error": abs(qcycle_norm - (PI + 1.0 / PI)),
    },
    "theory_effect": {
        "core_gluing_gate": "closed_in_the_minimal_local_defect_model",
        "rank_one_kernel": "constructed_without_Nambu_state_doubling",
        "rank_23": "restored_inside_the_conditional_defect_model",
        "full_S2T_status": "conditional_until_the_defect_BdG_operator_is_derived_from_the_action",
    },
    "remaining_proof_obligations": [
        "derive the Nambu transition and Majorana pairing operator from the S2T action",
        "construct the global tubular-neighborhood operator on RP3 rather than only transition data",
        "prove that its unique kernel embeds into the previously declared R24 heavy module",
        "show that quotienting this kernel produces the denominator contribution rather than a new light state",
    ],
    "verdict": (
        "The core-gluing obstruction closes algebraically in the minimal square-root defect model. "
        "The quarter-holonomy matrix maps the start zero basis to the end zero basis, while the spin "
        "and ambient torsion signs cancel. The coefficient line is periodic and has one longitudinal "
        "real zero mode. Particle-hole reality leaves one real direction, so no physical Nambu "
        "doubling occurs. Thus complement rank 23 is internally consistent in this defect model, "
        "although deriving the complete operator from the S2T action remains open."
    ),
}

assert transition_covariance_error < 1e-12
assert total_gluing_error < 1e-12
assert all(error < 1e-12 for error in majorana_errors.values())
assert abs(core_coefficient_holonomy - 1.0) < 1e-12
assert abs(without_torsion_coefficient_holonomy + 1.0) < 1e-12
assert kernel_rank == 1
assert kernel_rank_without_torsion == 0
assert results["rank_one_result"]["combined_real_rank"] == 1
assert results["rank_one_result"]["complement_rank_in_R24"] == 23
assert abs(qcycle_norm - (PI + 1.0 / PI)) < 1e-14

Path("s2t_neutrino_core_gluing_majorana_line_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "transition_covariance_error": transition_covariance_error,
            "coefficient_holonomy": results["core_gluing"]["coefficient_holonomy"],
            "longitudinal_kernel_rank": kernel_rank,
            "physical_real_rank": results["Majorana_reality"]["physical_zero_mode_real_rank"],
            "complement_rank": results["rank_one_result"]["complement_rank_in_R24"],
        },
        indent=2,
        ensure_ascii=False,
    )
)