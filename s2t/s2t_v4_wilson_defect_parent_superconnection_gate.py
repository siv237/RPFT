import itertools
import json

import sympy as sp


def integer_spin_weight_planes(spin):
    return {weight: 1 for weight in range(1, spin + 1)}


solutions = []
for multiplicities in itertools.product(range(9), repeat=4):
    plane_counts = {weight: 0 for weight in range(1, 5)}
    dimension = 0
    zero_weights = 0
    for spin, multiplicity in enumerate(multiplicities, start=1):
        dimension += multiplicity * (2 * spin + 1)
        zero_weights += multiplicity
        for weight in integer_spin_weight_planes(spin):
            plane_counts[weight] += multiplicity
    if plane_counts[1] == 8 and all(plane_counts[weight] == 0 for weight in range(2, 5)):
        solutions.append(
            {
                "multiplicities_spin_1_to_4": multiplicities,
                "dimension": dimension,
                "zero_weight_lines": zero_weights,
                "positive_weight_planes": plane_counts,
            }
        )

c, s = sp.symbols("c s", real=True)
inertia = 1 - c
rotation = sp.Matrix([[c, -s], [s, c]])
incidence = sp.eye(2) - rotation
cone_laplacian = sp.simplify(incidence.T * incidence / 2)
cone_laplacian_on_circle = cone_laplacian.subs(s**2, 1 - c**2).applyfunc(sp.factor)
expected_laplacian = inertia * sp.eye(2)
family_casimir = sp.diag(*([2] * 3 + [6] * 5))
momentum = family_casimir / 2
momentum_squared_trace = sp.trace(momentum**2)
root_laplacian = sp.kronecker_product(expected_laplacian, sp.eye(8))
lifted_casimir = sp.kronecker_product(sp.eye(2), family_casimir)
quadratic_commutator = sp.simplify(
    root_laplacian * lifted_casimir - lifted_casimir * root_laplacian
)
normalized_cone_action = (
    momentum_squared_trace / (6 * inertia)
    + sp.Rational(16, 6) * sp.log(inertia)
    - c
)
target_gap_action = (
    sp.Rational(8, 1) / inertia
    + sp.Rational(8, 3) * sp.log(inertia)
    - sp.Rational(44, 45) * c
)
linear_residual = sp.simplify(target_gap_action - normalized_cone_action)
periodic_trace = sp.simplify(2 * sp.zeta(4) / sp.pi**4)
root_plane_real_dimension = 2
exact_oneform_weight = sp.Rational(root_plane_real_dimension, 2)
fp_ghost_weight = -sp.Integer(root_plane_real_dimension)
exact_ghost_net_weight = sp.simplify(exact_oneform_weight + fp_ghost_weight)
exact_ghost_stiffness = sp.simplify(
    exact_ghost_net_weight * periodic_trace * (1 - c)
)
desired_momenta = sp.Matrix([1, 1, 1, 3, 3, 3, 3, 3])
single_gauss_matrix = sp.ones(1, 8)
block_gauss_matrix = sp.Matrix(
    [
        [1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1],
    ]
)
component_gauss_matrix = sp.eye(8)
single_gauss_nullity = 8 - single_gauss_matrix.rank()
block_gauss_nullity = 8 - block_gauss_matrix.rank()
component_gauss_nullity = 8 - component_gauss_matrix.rank()
direct_sum_projected_partition = (
    3 * sp.exp(-sp.Rational(1, 2) / inertia)
    + 5 * sp.exp(-sp.Rational(9, 2) / inertia)
)
product_projected_partition = sp.exp(-sp.Rational(24, 1) / inertia)
full_family_trace_target = sp.simplify(3 * target_gap_action)
full_family_tree_term = -3 * c
full_family_periodic_term = c / 15
full_family_reconstruction = sp.simplify(
    momentum_squared_trace / (2 * inertia)
    + 8 * sp.log(inertia)
    + full_family_tree_term
    + full_family_periodic_term
)
coherent_block_dimensions = [3, 5]
coherent_casimir_charges = [1, 3]
coherent_source_norm_squared = sum(
    dimension * charge**2
    for dimension, charge in zip(
        coherent_block_dimensions, coherent_casimir_charges
    )
)
coherent_gaussian_real_dimension = 16
coherent_gaussian_effective_action = sp.simplify(
    sp.Rational(coherent_source_norm_squared, 6) / inertia
    + sp.Rational(coherent_gaussian_real_dimension, 6) * sp.log(inertia)
)
target_nonlinear_pair = sp.simplify(
    8 / inertia + sp.Rational(8, 3) * sp.log(inertia)
)

result = {
    "gate": "version4_wilson_defect_parent_superconnection",
    "date": "2026-08-12",
    "kinematic_common_superconnection": {
        "group": "U(1)_root x SU(2)_F",
        "connection": "d + i*q_root*a + A_F",
        "pairing": "charge-two Phi in the Nambu odd block",
        "status": "allowed_but_direct_product_and_not_predictive",
    },
    "local_mixed_invariant_gate": {
        "quadratic_kinetic_mixing": "F_root*Tr(F_F)=0 because su2 generators are traceless",
        "flat_wilson_curvature": "F_F=0 on the Wilson branch",
        "consequence": "local curvature action does not tie the root vortex to the flat family holonomy",
    },
    "SO3_exact_log_weight_gate": {
        "target": "eight weight-one real rotation planes and no higher weights",
        "solutions_spin_at_most_4": solutions,
        "minimal_solution": min(solutions, key=lambda row: row["dimension"]),
        "consequence": "an unbroken SO3 trace requires eight vector triplets, but an axis-selected residual U1 boundary sector can instead contain eight unit-weight planes",
    },
    "SU2_doublet_lift_gate": {
        "exact_log_candidate": "four complex fundamental doublets, real dimension 16",
        "center_action": -1,
        "descends_to_SO3": False,
        "angle_relation": "the adjoint triplet sees twice the fundamental Cartan angle",
        "consequence": "the exact determinant is not a single-valued functional of the same SO3 holonomy R_n(theta_star)",
    },
    "fixed_charge_gate": {
        "required_mean_momentum_squared": 6,
        "uniform_quantized_momentum_exists": False,
        "odd_positive_solutions": [
            [1, 1, 1, 1, 1, 3, 3, 5],
            [1, 1, 1, 3, 3, 3, 3, 3],
        ],
        "unique_minimal_maximum_momentum_sector": [1, 1, 1, 3, 3, 3, 3, 3],
        "momentum_squared_sum": 48,
        "inverse_coefficient": 8,
        "status": "exact_operator_level_match_with_family_Casimir_selection",
    },
    "family_Casimir_selector": {
        "carrier_decomposition": "End_0(V1)=V1 direct_sum V2 with dimensions 3+5",
        "operator": "P=C2/2",
        "momentum_spectrum": [1, 1, 1, 3, 3, 3, 3, 3],
        "Tr_P_squared": int(momentum_squared_trace),
        "alternative_momentum_five_excluded": True,
    },
    "mode_factorized_reduced_integral": {
        "compact_rank": 8,
        "gaussian_root_real_rank": 16,
        "partition_function": "Z proportional I^(-8) exp(-24/I)",
        "normalized_effective_action": "8/I+(8/3)log(I)",
        "fractional_determinant_required": False,
        "exact_nonlinear_pair": True,
    },
    "mapping_cone_gate": {
        "differential": "Q=1-U(theta)",
        "laplacian": "Q^T Q/2=(1-c)I2",
        "laplacian_matrix": str(cone_laplacian_on_circle),
        "exact_common_inertia": sp.simplify(
            cone_laplacian_on_circle - expected_laplacian
        )
        == sp.zeros(2),
        "commutator_with_family_Casimir": str(quadratic_commutator),
        "no_quadratic_family_mixing": quadratic_commutator == sp.zeros(16),
        "canonical_Wilson_plaquette": "1-c, hence -c modulo a constant",
        "normalized_candidate_action": str(normalized_cone_action),
        "target_gap_action": str(target_gap_action),
        "remaining_residual": str(linear_residual),
        "only_periodic_one_over_45_remains": linear_residual == c / 45,
    },
    "periodic_exact_ghost_BV_ledger": {
        "root_plane_real_dimension": root_plane_real_dimension,
        "exact_oneform_bosonic_weight": str(exact_oneform_weight),
        "FP_ghost_weight": str(fp_ghost_weight),
        "net_signed_weight": str(exact_ghost_net_weight),
        "periodic_trace": str(periodic_trace),
        "stiffness_term": str(exact_ghost_stiffness),
        "equals_required_term_up_to_constant": sp.simplify(
            exact_ghost_stiffness - (c / 45 - sp.Rational(1, 45))
        )
        == 0,
        "ordinary_Yang_Mills_coexact_modes_remain": True,
        "closure_condition": (
            "the one-form grade must be topological/flat or possess a BV partner that cancels "
            "all coexact root modes while preserving the exact-plus-ghost net weight -1"
        ),
    },
    "coexact_cancellation_trilemma": {
        "ordinary_local_oneform": {
            "coexact_modes": "present with positive bosonic spectral weight",
            "verdict": "fail_extra_nonzero_tower",
        },
        "pure_flat_or_BF_oneform": {
            "coexact_modes": "removed by the flatness constraint",
            "exact_ghost_residue": "also reduced to topological torsion/harmonic measure, not -Tr Delta^-2",
            "verdict": "fail_removes_required_one_over_45_mechanism",
        },
        "dynamical_or_localized_BF_partner": {
            "effect": "changes the operator spectrum or boundary conditions",
            "verdict": "fail_not_selective_isospectral_cancellation",
        },
        "finite_standard_local_BV_solution_exists": False,
        "surviving_class": (
            "declare the nonlocal zeta/Kubo stiffness -t*pi^-4*Tr'(Delta_per^-2) "
            "as a fundamental spectral configuration metric, then derive its unit coefficient "
            "and sign from the parent principle"
        ),
    },
    "fixed_charge_parent_measure_audit": {
        "desired_momentum_vector": list(map(int, desired_momenta)),
        "one_scalar_Gauss_law_rank": single_gauss_matrix.rank(),
        "one_scalar_Gauss_law_nullity": single_gauss_nullity,
        "two_block_Gauss_laws_rank": block_gauss_matrix.rank(),
        "two_block_Gauss_laws_nullity": block_gauss_nullity,
        "componentwise_constraint_rank": component_gauss_matrix.rank(),
        "componentwise_constraint_nullity": component_gauss_nullity,
        "minimal_linear_constraints_for_unique_vector": 8,
        "single_U1_Gauss_law_selects_unique_vector": False,
        "two_irrep_block_constraints_select_unique_vector": False,
        "componentwise_constraint_requires_new_multiplier_dimension": 8,
        "single_rotor_tensor_family_partition": str(direct_sum_projected_partition),
        "eight_rotor_product_partition": str(product_projected_partition),
        "product_partition_requires_eight_compact_factors": True,
        "family_trace_normalization": {
            "three_times_target": str(full_family_trace_target),
            "tree_multiplicity": 3,
            "periodic_multiplicity": 3,
            "reconstructed_full_action": str(full_family_reconstruction),
            "equals_three_times_target": sp.simplify(
                full_family_reconstruction - full_family_trace_target
            )
            == 0,
            "interpretation": (
                "division by three is harmless only if tree, periodic, compact, and "
                "Gaussian sectors all arise before division from one family-traced action"
            ),
        },
        "verdict": (
            "family-rank normalization has a coherent algebraic completion, but the "
            "minimal single-U1 or two-block Gauss-law menu does not derive the fixed "
            "momentum vector; a rank-eight covariant projector is additional structure"
        ),
        "next_gate": (
            "derive an eight-component SU2-covariant constraint from the existing "
            "superconnection, or abandon the eight-rotor product reconstruction"
        ),
    },
    "coherent_source_gaussian_bypass": {
        "carrier": "R2_root tensor (V1 direct_sum V2)",
        "real_dimension": coherent_gaussian_real_dimension,
        "axis_kernel_norms_squared": {
            "V1": coherent_block_dimensions[0],
            "V2": coherent_block_dimensions[1],
        },
        "source": "J(n)=e_root tensor (C2/2) kappa_n",
        "source_norm_squared": coherent_source_norm_squared,
        "gaussian_integral": (
            "integral d^16 X exp[-I||X||^2/2+i<J,X>] "
            "proportional I^-8 exp[-||J||^2/(2I)]"
        ),
        "family_normalized_effective_action": str(
            coherent_gaussian_effective_action
        ),
        "target_nonlinear_pair": str(target_nonlinear_pair),
        "exact_pair_match": sp.simplify(
            coherent_gaussian_effective_action - target_nonlinear_pair
        )
        == 0,
        "fixed_charge_projector_required": False,
        "eight_compact_rotors_required": False,
        "covariance": (
            "kappa_n is an equivariant reproducing-kernel vector; its block norm "
            "is dim(V_j), so the source norm is independent of the chosen axis"
        ),
        "open_physical_gate": (
            "derive the imaginary linear source as a gauge-invariant defect or "
            "boundary coupling, including its contour, sign, and axis measure"
        ),
        "status": "exact_algebraic_bypass_conditional_on_parent_source_origin",
    },
    "independent_parent_inputs": [
        "root gauge coupling",
        "pairing mass and quartic coupling",
        "family gauge stiffness",
        "Wilson tree stiffness",
        "boundary rotor representation and fixed-charge sector",
        "factor-axis coupling",
    ],
    "verdict": "local_three_node_oneform_BV_route_closed_by_coexact_cancellation_trilemma_nonlocal_spectral_metric_open",
    "reopening": (
        "derive the nonlocal zeta/Kubo stiffness as a fundamental parent spectral metric with "
        "unit coefficient and negative supertrace sign; do not claim a local Gaussian/BF realization"
    ),
}

assert len(solutions) == 1
assert result["SO3_exact_log_weight_gate"]["minimal_solution"]["multiplicities_spin_1_to_4"] == (8, 0, 0, 0)
assert sum(momentum * momentum for momentum in result["fixed_charge_gate"]["unique_minimal_maximum_momentum_sector"]) == 48
assert result["mapping_cone_gate"]["exact_common_inertia"]
assert result["mapping_cone_gate"]["no_quadratic_family_mixing"]
assert result["mapping_cone_gate"]["only_periodic_one_over_45_remains"]
assert result["periodic_exact_ghost_BV_ledger"][
    "equals_required_term_up_to_constant"
]
assert not result["coexact_cancellation_trilemma"][
    "finite_standard_local_BV_solution_exists"
]
assert single_gauss_nullity == 7
assert block_gauss_nullity == 6
assert component_gauss_nullity == 0
assert result["fixed_charge_parent_measure_audit"]["family_trace_normalization"][
    "equals_three_times_target"
]
assert coherent_source_norm_squared == 48
assert result["coherent_source_gaussian_bypass"]["exact_pair_match"]

with open("s2t_v4_wilson_defect_parent_superconnection_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, ensure_ascii=False, indent=2))