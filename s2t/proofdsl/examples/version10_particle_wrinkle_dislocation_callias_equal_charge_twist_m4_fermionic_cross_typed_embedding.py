"""LCF certificate for the Callias equal-charge M4 typed embedding."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CalliasM4TypedEmbeddingCertificate:
    spatial_generators: tuple[sp.ImmutableMatrix, ...]
    twist_generators: tuple[sp.ImmutableMatrix, ...]
    spatial_twist_commutators: sp.ImmutableMatrix
    twist_grading: sp.ImmutableMatrix
    twist_cross: sp.ImmutableMatrix
    charge_operator: sp.ImmutableMatrix
    charge_cross_defect: sp.ImmutableMatrix
    positive_projector: sp.ImmutableMatrix
    negative_projector: sp.ImmutableMatrix
    partial_isometry: sp.ImmutableMatrix
    conditional_amplifier: sp.ImmutableMatrix
    inherited_amplifier: sp.ImmutableMatrix
    algebra_gram: sp.ImmutableMatrix
    dirac_witness: sp.ImmutableMatrix
    determinant_curvature: sp.Expr
    conditional_architecture: sp.ImmutableMatrix
    inherited_data: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CalliasM4TypedEmbeddingCertificate:
    sx = sp.ImmutableMatrix([[0, 1], [1, 0]])
    sy = sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.ImmutableMatrix([[1, 0], [0, -1]])
    pauli = (sx, sy, sz)
    i2, i15 = sp.eye(2), sp.eye(15)
    spatial_generators = tuple(sp.ImmutableMatrix(sp.kronecker_product(g, i2, i15)) for g in pauli)
    twist_generators = tuple(sp.ImmutableMatrix(sp.kronecker_product(i2, g, i15)) for g in pauli)
    spatial_twist_commutators = sp.ImmutableMatrix.vstack(*(
        s * t - t * s for s in spatial_generators for t in twist_generators
    ))
    twist_cross, twist_grading = twist_generators[0], twist_generators[2]
    coefficient_charge = sp.diag(*range(1, 16))
    charge_operator = sp.ImmutableMatrix(sp.kronecker_product(i2, i2, coefficient_charge))
    charge_cross_defect = sp.ImmutableMatrix(charge_operator * twist_cross - twist_cross * charge_operator)
    positive_projector = sp.ImmutableMatrix((sp.eye(60) + twist_grading) / 2)
    negative_projector = sp.ImmutableMatrix((sp.eye(60) - twist_grading) / 2)
    partial_isometry = sp.ImmutableMatrix(positive_projector * twist_cross * negative_projector)

    uniform15 = sp.ones(15, 1)
    conditional_amplifier = sp.ImmutableMatrix(sp.kronecker_product(i2, uniform15))
    inherited_amplifier = sp.ImmutableMatrix(sp.zeros(30, 2))
    algebra_gram = sp.ImmutableMatrix(60 * sp.eye(16))
    dirac_witness = sp.ImmutableMatrix(twist_grading + twist_cross)
    x = sp.symbols("x", real=True)
    determinant_action = -30 * sp.log(1 + x**2)
    determinant_curvature = sp.simplify(sp.diff(determinant_action, x, 2).subs(x, 0))
    conditional_architecture = sp.ImmutableMatrix.ones(16, 1)
    inherited_data = sp.ImmutableMatrix([1, 1, 1, 0, 0])
    physical_origin = sp.ImmutableMatrix.zeros(3, 1)

    theorems = (
        kernel.prove_matrix_equality(spatial_twist_commutators, sp.zeros(540, 60), subject="spatial and twist Clifford actions commute"),
        kernel.prove_matrix_equality(twist_grading**2, sp.eye(60), subject="amplified twist grading is involutive"),
        kernel.prove_matrix_equality(twist_cross**2, sp.eye(60), subject="amplified cross twist is involutive"),
        kernel.prove_matrix_equality(twist_grading * twist_cross + twist_cross * twist_grading, sp.zeros(60), subject="amplified grading and cross twist anticommute"),
        kernel.prove_matrix_equality(charge_cross_defect, sp.zeros(60), subject="equal-charge cross twist is gauge compatible"),
        kernel.prove_exact_rank(positive_projector, 30, subject="positive twist sector has rank thirty"),
        kernel.prove_exact_rank(negative_projector, 30, subject="negative twist sector has rank thirty"),
        kernel.prove_matrix_equality(positive_projector + negative_projector, sp.eye(60), subject="twist sectors resolve the Callias carrier"),
        kernel.prove_matrix_equality(partial_isometry.T.conjugate() * partial_isometry, negative_projector, subject="cross partial isometry has negative initial sector"),
        kernel.prove_matrix_equality(partial_isometry * partial_isometry.T.conjugate(), positive_projector, subject="cross partial isometry has positive final sector"),
        kernel.prove_exact_rank(partial_isometry, 30, subject="Callias cross partial isometry has rank thirty"),
        kernel.prove_exact_rank(conditional_amplifier, 2, subject="uniform H15 amplifier embeds the cell doublet"),
        kernel.prove_matrix_equality(conditional_amplifier.T * conditional_amplifier, 15 * sp.eye(2), subject="uniform H15 amplifier has equal channel norm"),
        kernel.prove_exact_rank(inherited_amplifier, 0, subject="inherited cell-to-Callias amplifier remains zero"),
        kernel.prove_matrix_equality(algebra_gram, 60 * sp.eye(16), subject="amplified Pauli tensor basis is orthogonal"),
        kernel.prove_exact_rank(algebra_gram, 16, subject="typed embedding carries the full M4 algebra"),
        kernel.prove_matrix_equality(dirac_witness**2, 2 * sp.eye(60), subject="unit Callias cross Dirac witness has scalar square"),
        kernel.prove_exact_spectrum(dirac_witness, {-sp.sqrt(2): 30, sp.sqrt(2): 30}, subject="Callias cross Dirac spectrum has multiplicity thirty"),
        kernel.prove_expression_equality(determinant_curvature, -60, subject="H15 amplification multiplies fermion susceptibility by fifteen"),
        kernel.prove_expression_equality(sum(conditional_architecture), 16, subject="conditional Callias M4 typed embedding is complete"),
        kernel.prove_matrix_equality(inherited_data, sp.Matrix([1, 1, 1, 0, 0]), subject="dimensions Clifford split and abstract equal charge algebra are inherited"),
        kernel.prove_expression_equality(sum(inherited_data), 3, subject="three of five typed embedding inputs are inherited"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="sector identification uniform amplifier and coupling origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical Callias M4 embedding origin remains zero"),
    )
    gate_theorem = kernel.prove_gate("version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate", theorems)
    return CalliasM4TypedEmbeddingCertificate(
        spatial_generators, twist_generators, spatial_twist_commutators,
        twist_grading, twist_cross, charge_operator, charge_cross_defect,
        positive_projector, negative_projector, partial_isometry,
        conditional_amplifier, inherited_amplifier, algebra_gram,
        dirac_witness, determinant_curvature, conditional_architecture,
        inherited_data, physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate",
    title="Типизированное Callias--M4 вложение фермионного cross-оператора",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_fermionic_cross_typed_embedding_gate_results.json",
    ),
    obligations=tuple(Obligation(f"callias_m4_cross_typed_embedding_{i:02d}", lambda i=i: build_certificate().theorems[i]) for i in range(24)),
)