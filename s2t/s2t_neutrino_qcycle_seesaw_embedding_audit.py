import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
Q = np.diag([PI, 1.0 / PI])
E = np.diag([math.sqrt(PI), 1.0 / math.sqrt(PI)])
v = np.array([[1.0, 1.0]])
identity_cycle = np.eye(2)

y = 1.0
M0 = 1.0
mD_cycle = y * (v @ E)
seesaw_cycle = -mD_cycle @ np.linalg.inv(M0 * identity_cycle) @ mD_cycle.T
target = -(PI + 1.0 / PI)


rotation_checks = []
for angle in [0.0, 0.17, 0.51, 1.03, 1.57]:
    rotation = np.array(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]]
    )
    mD_rotated = mD_cycle @ rotation.T
    MR_rotated = rotation @ identity_cycle @ rotation.T
    value = -mD_rotated @ np.linalg.inv(MR_rotated) @ mD_rotated.T
    rotation_checks.append(
        {
            "angle": angle,
            "seesaw_value": float(value[0, 0]),
            "error": float(value[0, 0] - target),
        }
    )


ME_MEV = 0.51099895069
MMU_MEV = 105.6583755
D_NU = 23 + 1.0 / PI
y_physical_eV = ME_MEV**2 / MMU_MEV * 1e6
M0_physical_eV = D_NU * MMU_MEV * 1e6
mu_from_matrix = (
    y_physical_eV**2
    / M0_physical_eV
    * float((v @ Q @ v.T)[0, 0])
)


results = {
    "status": "minimal_Qcycle_seesaw_contraction_constructed_internal_spinor_embedding_open",
    "date": "2026-08-03",
    "cycle_data": {
        "Qcycle": Q.tolist(),
        "cycle_vielbein": E.tolist(),
        "primitive_self_dual_vector": v.flatten().tolist(),
        "cycle_metric_determinant": float(np.linalg.det(Q)),
    },
    "minimal_embedding": {
        "Dirac_row": "mD_cycle=y*v^T*Qcycle^(1/2)",
        "Dirac_row_numeric_at_y1": mD_cycle.flatten().tolist(),
        "heavy_cycle_block": "MR_cycle=M0*I2",
        "seesaw_contraction": "-mD_cycle*MR_cycle^-1*mD_cycle^T",
        "result_at_y1_M01": float(seesaw_cycle[0, 0]),
        "expected": target,
        "error": float(seesaw_cycle[0, 0] - target),
    },
    "derivation": {
        "identity": (
            "v^T Qcycle^(1/2) I2 Qcycle^(1/2) v = v^T Qcycle v = pi+pi^-1"
        ),
        "no_cross_term": "the primal and dual cycle channels are orthogonal in the Hodge Gram basis",
        "no_continuous_overlap_coefficient": (
            "v=(1,1) is the primitive self-dual integral vector and Qcycle is fixed by the systolic length"
        ),
        "no_new_mass_scale": "det Qcycle=1 and the only heavy scale remains M0=D_nu*m_mu",
    },
    "basis_invariance": {
        "rule": "mD maps as mD O^T and MR as O MR O^T",
        "rotation_checks": rotation_checks,
        "max_abs_error": max(abs(row["error"]) for row in rotation_checks),
    },
    "physical_scale": {
        "y=m_e^2/m_mu_eV": y_physical_eV,
        "M0=D_nu*m_mu_eV": M0_physical_eV,
        "mu_nu_from_matrix_eV": mu_from_matrix,
        "dm21_eV2": mu_from_matrix**2,
    },
    "normalization_guardrail": {
        "statement": (
            "The integral vector v is a primitive coupling/charge vector in the cycle lattice, not a wavefunction "
            "to be divided by its Q norm. Canonically normalizing v would erase the predicted factor and would "
            "change the model definition."
        ),
        "required_EFT_statement": (
            "The cycle doublet must have canonical kinetic term in the orthonormal channel basis, while its Yukawa "
            "components are the lattice vector transported by the vielbein Qcycle^(1/2)."
        ),
    },
    "generation_structure": {
        "factorization": (
            "mD_total=mD_generation tensor mD_cycle and MR_total=MR_generation tensor I2"
        ),
        "effect": (
            "the Qcycle contraction multiplies the full light-neutrino matrix by one scalar and therefore leaves "
            "the dimensionless eigenvalue ratio R_nu unchanged"
        ),
        "state_count_warning": (
            "The cycle doublet must be embedded as two orthogonal channels inside the already counted real Majorana "
            "module, not added as two new sterile generations."
        ),
    },
    "remaining_obligations": [
        "construct an isometric embedding of the cycle doublet into the existing eight-real-dimensional Majorana module",
        "derive the defect/restriction Yukawa vertex from the ambient Dirac action",
        "prove that charge conjugation or another exact symmetry selects the primitive self-dual vector v=(1,1)",
        "show that no additional cycle-channel mass matrix replaces the minimal identity block",
    ],
    "theory_effect": {
        "pi_plus_inverse_factor": "derived_inside_minimal_cycle_channel_seesaw_contraction",
        "absolute_neutrino_scale": "substantially_strengthened_but_not_full_theorem",
        "dimensionless_ratio_Rnu": "unchanged",
        "new_primary_gap": "representation_and_vertex_embedding_not_scalar_numerology",
    },
    "verdict": (
        "A minimal matrix embedding exists. In the orthonormal cycle-channel basis, take the Dirac row to be "
        "y v^T Qcycle^(1/2) with primitive self-dual v=(1,1), and take the heavy cycle block to be M0 I2. "
        "The seesaw contraction is then exactly -(y^2/M0)(pi+pi^-1), is invariant under orthogonal channel-basis "
        "changes, introduces no new mass scale, and leaves R_nu unchanged. The remaining theorem gap is to embed "
        "these two channels and their self-dual Yukawa vector inside the already declared ambient Majorana/Dirac module."
    ),
}


assert abs(results["minimal_embedding"]["error"]) < 1e-14
assert results["basis_invariance"]["max_abs_error"] < 1e-14
assert abs(results["physical_scale"]["mu_nu_from_matrix_eV"] - 0.008576992731264175) < 1e-15

Path("s2t_neutrino_qcycle_seesaw_embedding_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps({
    "status": results["status"],
    "Dirac_row": results["minimal_embedding"]["Dirac_row_numeric_at_y1"],
    "seesaw_factor": results["minimal_embedding"]["result_at_y1_M01"],
    "basis_max_error": results["basis_invariance"]["max_abs_error"],
    "mu_nu_eV": results["physical_scale"]["mu_nu_from_matrix_eV"],
}, indent=2, ensure_ascii=False))