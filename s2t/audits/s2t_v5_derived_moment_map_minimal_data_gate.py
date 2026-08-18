#!/usr/bin/env python3
"""Audit the minimal preprojective/derived origin of the family moment map."""

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_derived_moment_map_minimal_data_gate_results.json"

# Fixed nonsingular integer witnesses. Real matrices are sufficient for the
# physical SO(3) branch and make transpose equal to Hilbert adjoint.
X = np.array([[1.0, 2.0, 0.0], [0.0, 1.0, 1.0], [2.0, 0.0, 1.0]])
Y = np.array([[1.0, 0.0, 1.0], [1.0, 2.0, 0.0], [0.0, 1.0, 2.0]])
I3 = np.eye(3)
Z3 = np.zeros((3, 3))


def block_matrix(rows):
    return np.block(rows)


# Oriented differential on V_0 -> V_G -> V_2.
d = block_matrix([[Z3, Z3, Z3], [X, Z3, Z3], [Z3, Y, Z3]])
d_star = d.T
hodge_commutator = d @ d_star - d_star @ d

mu_0 = -(X.T @ X)
mu_g = X @ X.T - Y.T @ Y
mu_2 = Y @ Y.T
expected = block_matrix([[mu_0, Z3, Z3], [Z3, mu_g, Z3], [Z3, Z3, mu_2]])

hodge_residual = float(np.linalg.norm(hodge_commutator - expected))
trace_balance = float(abs(np.trace(mu_0) + np.trace(mu_g) + np.trace(mu_2)))
assert hodge_residual == 0.0
assert trace_balance == 0.0

# The middle vertex idempotent gives the desired normalized local norm.
P_g = block_matrix([[Z3, Z3, Z3], [Z3, I3, Z3], [Z3, Z3, Z3]])
middle_norm = float(np.trace(mu_g @ mu_g) / 3.0)
projected_norm = float(np.trace(P_g @ hodge_commutator @ hodge_commutator) / 3.0)
full_norm = float(np.trace(hodge_commutator @ hodge_commutator) / 3.0)
normalization_residual = abs(middle_norm - projected_norm)
assert normalization_residual == 0.0
assert full_norm > middle_norm

# Reverse the first edge. The algebraic orientation-change isomorphism uses
# b=x* and b*=-x. It preserves the relation but not b*=b^dagger.
b = X.T
b_formal_reverse = -X
formal_middle_x = -(b_formal_reverse @ b)
formal_orientation_residual_x = float(np.linalg.norm(formal_middle_x - X @ X.T))
formal_star_defect_x = float(np.linalg.norm(b_formal_reverse - b.T))
assert formal_orientation_residual_x == 0.0
assert formal_star_defect_x > 0.0

# A star-preserving reversal has b*=b^dagger=x and flips the local sign.
b_positive_reverse = b.T
positive_middle_x = -(b_positive_reverse @ b)
positive_orientation_residual_x = float(np.linalg.norm(positive_middle_x - X @ X.T))
assert positive_orientation_residual_x > 0.0

# The same obstruction occurs when the second edge is reversed.
c = Y.T
c_formal_reverse = -Y
formal_middle_y = c @ c_formal_reverse
formal_orientation_residual_y = float(np.linalg.norm(formal_middle_y + Y.T @ Y))
formal_star_defect_y = float(np.linalg.norm(c_formal_reverse - c.T))
assert formal_orientation_residual_y == 0.0
assert formal_star_defect_y > 0.0

c_positive_reverse = c.T
positive_middle_y = c @ c_positive_reverse
positive_orientation_residual_y = float(np.linalg.norm(positive_middle_y + Y.T @ Y))
assert positive_orientation_residual_y > 0.0

# Global reversal changes mu_g to -mu_g, while a single reversal changes the
# norm in general and recreates the chain-versus-sink ambiguity.
mu_global_reverse = -X @ X.T + Y.T @ Y
global_reverse_norm_residual = abs(
    np.trace(mu_global_reverse @ mu_global_reverse) / 3.0 - middle_norm
)
mu_first_only_reverse = -X @ X.T - Y.T @ Y
single_reverse_norm_shift = abs(
    np.trace(mu_first_only_reverse @ mu_first_only_reverse) / 3.0 - middle_norm
)
assert global_reverse_norm_residual == 0.0
assert single_reverse_norm_shift > 0.0

# The real target is symmetric and pairs trivially with so(3).
so3_basis = []
for i, j in [(0, 1), (0, 2), (1, 2)]:
    generator = np.zeros((3, 3))
    generator[i, j] = 1.0
    generator[j, i] = -1.0
    so3_basis.append(generator)
so3_pairings = [float(np.trace(mu_g @ generator)) for generator in so3_basis]
so3_pairing_norm = float(np.linalg.norm(so3_pairings))
assert so3_pairing_norm == 0.0

# A full Hermitian/GL(3) dual detects mu_g, but has dimension nine rather
# than the physical three-dimensional SO(3) algebra.
full_matrix_pairing_norm = float(np.linalg.norm(mu_g))
assert full_matrix_pairing_norm > 0.0

result = {
    "date": "2026-08-16",
    "gate": "version5_derived_moment_map_minimal_data_gate",
    "preprojective_identity": {
        "middle_relation": "X X^T - Y^T Y",
        "hodge_block_residual": hodge_residual,
        "total_trace_balance": trace_balance,
        "exact_target": True,
    },
    "orientation_change": {
        "formal_isomorphism": "b=x_star, b_star=-x",
        "general_phase_relation_preservation": "alpha*beta=-1",
        "positive_star_phase_condition": "beta=conjugate(alpha)",
        "phase_conditions_compatible": False,
        "formal_relation_residual_first_edge": formal_orientation_residual_x,
        "formal_relation_residual_second_edge": formal_orientation_residual_y,
        "formal_star_defect_first_edge": formal_star_defect_x,
        "formal_star_defect_second_edge": formal_star_defect_y,
        "positive_star_residual_first_edge": positive_orientation_residual_x,
        "positive_star_residual_second_edge": positive_orientation_residual_y,
        "global_reversal_norm_residual": global_reverse_norm_residual,
        "single_edge_reversal_norm_shift": single_reverse_norm_shift,
        "formal_orientation_independence": True,
        "positive_star_orientation_independence": False,
    },
    "real_form": {
        "mu_is_symmetric": bool(np.allclose(mu_g, mu_g.T)),
        "so3_pairings": so3_pairings,
        "so3_pairing_norm": so3_pairing_norm,
        "strict_SO3_moment_map_nonzero": False,
        "full_matrix_pairing_norm": full_matrix_pairing_norm,
        "U3_or_GL3_detects_relation": True,
        "SO3_dimension": 3,
        "U3_or_GL3_dimension": 9,
        "additional_generators_if_enlarged": 6,
    },
    "derived_complex": {
        "minimal_rule": "d(theta_i)=r_i, d(arrows)=0",
        "d_squared_zero": True,
        "moment_relation_is_input": True,
        "moment_relation_derived_from_KO6": False,
    },
    "normalization": {
        "middle_vertex_normalized_norm": middle_norm,
        "projected_full_trace_norm": projected_norm,
        "normalization_residual": normalization_residual,
        "unprojected_full_norm": full_norm,
        "middle_vertex_idempotent_required": True,
        "gauged_versus_framed_vertex_split_required": True,
    },
    "verdict": {
        "exact_preprojective_target": "pass",
        "formal_orientation_independence": "pass",
        "positive_star_canonicity": "fail",
        "physical_SO3_moment_map": "fail",
        "derived_nilpotence": "conditional_pass",
        "parent_derivation_from_current_KO6": "fail",
        "minimal_preprojective_route": "closed_as_parent_origin",
        "new_complex_symplectic_parent": "open_only_as_new_architecture",
        "physical_closure": False,
    },
    "next_gate": "version5_parent_architecture_status_freeze_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))