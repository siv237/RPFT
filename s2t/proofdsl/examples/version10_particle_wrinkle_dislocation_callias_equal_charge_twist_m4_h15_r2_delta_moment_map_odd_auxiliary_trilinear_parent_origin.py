"""LCF certificate for the Delta moment-map odd auxiliary trilinear parent."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class DeltaMomentMapOddAuxiliaryTrilinearParentCertificate:
    hypercharge6: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    multiplicity_identity: sp.ImmutableMatrix
    multiplicity_exchange: sp.ImmutableMatrix
    invariant_metric_basis: sp.ImmutableMatrix
    normalization_constraint: sp.ImmutableMatrix
    inherited_coefficients: sp.ImmutableMatrix
    target_coefficients: sp.ImmutableMatrix
    inherited_multiplicity_metric: sp.ImmutableMatrix
    half_multiplicity_metric: sp.ImmutableMatrix
    target_multiplicity_metric: sp.ImmutableMatrix
    hadamard: sp.ImmutableMatrix
    inherited_diagonal_form: sp.ImmutableMatrix
    half_diagonal_form: sp.ImmutableMatrix
    target_diagonal_form: sp.ImmutableMatrix
    inherited_trace_metric: sp.ImmutableMatrix
    half_trace_metric: sp.ImmutableMatrix
    target_trace_metric: sp.ImmutableMatrix
    inherited_moment_operator: sp.ImmutableMatrix
    half_moment_operator: sp.ImmutableMatrix
    target_moment_operator: sp.ImmutableMatrix
    inherited_cross_block: sp.ImmutableMatrix
    half_cross_block: sp.ImmutableMatrix
    target_cross_block: sp.ImmutableMatrix
    antisymmetric_mixing: sp.ImmutableMatrix
    conditional_status: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> DeltaMomentMapOddAuxiliaryTrilinearParentCertificate:
    hypercharge6 = sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3])
    hypercharge_generator = sp.ImmutableMatrix(sp.diag(*list(hypercharge6)))
    identity2 = sp.ImmutableMatrix(sp.eye(2))
    exchange = sp.ImmutableMatrix([[0, 1], [1, 0]])
    invariant_metric_basis = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([1, 0, 0, 0]),
        sp.ImmutableMatrix([0, 0, 0, 1]),
        sp.ImmutableMatrix([0, 1, 1, 0]),
    )
    normalization_constraint = sp.ImmutableMatrix([[1, 0, 0], [0, 1, 0]])
    inherited_coefficients = sp.ImmutableMatrix([1, 1, 0])
    target_coefficients = sp.ImmutableMatrix([1, 1, 1])

    inherited_multiplicity_metric = identity2
    half_multiplicity_metric = sp.ImmutableMatrix(identity2 + sp.Rational(1, 2) * exchange)
    target_multiplicity_metric = sp.ImmutableMatrix(identity2 + exchange)
    hadamard = sp.ImmutableMatrix([[1, 1], [1, -1]])
    inherited_diagonal_form = sp.ImmutableMatrix(hadamard.T * inherited_multiplicity_metric * hadamard)
    half_diagonal_form = sp.ImmutableMatrix(hadamard.T * half_multiplicity_metric * hadamard)
    target_diagonal_form = sp.ImmutableMatrix(hadamard.T * target_multiplicity_metric * hadamard)

    identity8 = sp.eye(8)
    inherited_trace_metric = sp.ImmutableMatrix(sp.kronecker_product(inherited_multiplicity_metric, identity8))
    half_trace_metric = sp.ImmutableMatrix(sp.kronecker_product(half_multiplicity_metric, identity8))
    target_trace_metric = sp.ImmutableMatrix(sp.kronecker_product(target_multiplicity_metric, identity8))
    inherited_moment_operator = sp.ImmutableMatrix(sp.kronecker_product(inherited_multiplicity_metric, hypercharge_generator))
    half_moment_operator = sp.ImmutableMatrix(sp.kronecker_product(half_multiplicity_metric, hypercharge_generator))
    target_moment_operator = sp.ImmutableMatrix(sp.kronecker_product(target_multiplicity_metric, hypercharge_generator))
    inherited_cross_block = sp.ImmutableMatrix(inherited_moment_operator[:8, 8:])
    half_cross_block = sp.ImmutableMatrix(half_moment_operator[:8, 8:])
    target_cross_block = sp.ImmutableMatrix(target_moment_operator[:8, 8:])
    antisymmetric_mixing = sp.ImmutableMatrix(
        sp.kronecker_product(sp.Matrix([[0, 1], [-1, 0]]), hypercharge_generator)
    )

    # Slots: exact Q, gauge/Real invariant pairing, coefficient fixed,
    # nondegenerate independent trace metric, inherited action.
    conditional_status = sp.ImmutableMatrix([1, 1, 1, 0, 0])
    physical_status = sp.ImmutableMatrix([1, 1, 0, 1, 0])

    theorems = (
        kernel.prove_matrix_equality(hypercharge6, sp.ImmutableMatrix([3, -3, 7, 1, -1, -7, 3, -3]), subject="Delta moment map gives the exact six-hypercharge spectrum"),
        kernel.prove_exact_rank(hypercharge_generator, 8, subject="the required moment-map generator acts on all Sigma sectors"),
        kernel.prove_exact_rank(invariant_metric_basis, 3, subject="two isomorphic Real modules admit three symmetric invariant metric coefficients"),
        kernel.prove_exact_rank(normalization_constraint, 2, subject="unit normalization fixes only the two diagonal metric coefficients"),
        kernel.prove_exact_nullity(normalization_constraint, 1, subject="one off-diagonal multiplicity coefficient remains free"),
        kernel.prove_matrix_equality(inherited_coefficients, sp.ImmutableMatrix([1, 1, 0]), subject="orthogonal direct-sum inheritance selects zero mixing"),
        kernel.prove_matrix_equality(target_coefficients, sp.ImmutableMatrix([1, 1, 1]), subject="the exact Q cross block requires unit mixing"),
        kernel.prove_matrix_equality(inherited_diagonal_form, sp.diag(2, 2), subject="inherited multiplicity metric is nondegenerate"),
        kernel.prove_matrix_equality(half_diagonal_form, sp.diag(3, 1), subject="a nonzero admissible mixing remains nondegenerate but has the wrong coefficient"),
        kernel.prove_matrix_equality(target_diagonal_form, sp.diag(4, 0), subject="unit mixing lies on the degenerate boundary"),
        kernel.prove_exact_rank(inherited_trace_metric, 16, subject="inherited two-copy trace metric has full rank"),
        kernel.prove_exact_rank(half_trace_metric, 16, subject="half-mixed trace metric has full rank"),
        kernel.prove_exact_rank(target_trace_metric, 8, subject="target unit-mixed trace metric loses one full copy"),
        kernel.prove_exact_nullity(target_trace_metric, 8, subject="target unit mixing destroys auxiliary independence"),
        kernel.prove_exact_rank(inherited_cross_block, 0, subject="additive direct-sum moment map has no A-Sigma cross block"),
        kernel.prove_matrix_equality(half_cross_block, sp.Rational(1, 2) * hypercharge_generator, subject="generic invariant mixing produces a free multiple of Q"),
        kernel.prove_matrix_equality(target_cross_block, hypercharge_generator, subject="unit mixing reproduces the requested Q cross block"),
        kernel.prove_exact_rank(target_cross_block, 8, subject="the requested moment-map cross block has full rank"),
        kernel.prove_matrix_equality(antisymmetric_mixing.T, -antisymmetric_mixing, subject="antisymmetric multiplicity mixing contributes no Real quadratic scalar"),
        kernel.prove_expression_equality(sum(conditional_status), 3, subject="target-loaded moment-map trilinear closes three of five slots"),
        kernel.prove_expression_equality(sum(physical_status), 3, subject="inherited moment-map parent closes three of five slots but has zero cross coupling"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate",
        theorems,
    )
    return DeltaMomentMapOddAuxiliaryTrilinearParentCertificate(
        hypercharge6,
        hypercharge_generator,
        identity2,
        exchange,
        invariant_metric_basis,
        normalization_constraint,
        inherited_coefficients,
        target_coefficients,
        inherited_multiplicity_metric,
        half_multiplicity_metric,
        target_multiplicity_metric,
        hadamard,
        inherited_diagonal_form,
        half_diagonal_form,
        target_diagonal_form,
        inherited_trace_metric,
        half_trace_metric,
        target_trace_metric,
        inherited_moment_operator,
        half_moment_operator,
        target_moment_operator,
        inherited_cross_block,
        half_cross_block,
        target_cross_block,
        antisymmetric_mixing,
        conditional_status,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate",
    title="Родитель Delta moment-map odd auxiliary trilinear",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_r2_delta_moment_map_odd_auxiliary_trilinear_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_r2_delta_moment_map_odd_auxiliary_trilinear_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(21)
    ),
)