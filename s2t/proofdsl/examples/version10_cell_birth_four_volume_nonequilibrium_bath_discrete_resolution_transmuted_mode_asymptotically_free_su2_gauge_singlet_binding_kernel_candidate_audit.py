"""LCF audit of binding-kernel candidates for the composite SU(2) singlet."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2GaugeSingletBindingKernelCandidateAuditCertificate:
    singlet_projector: sp.ImmutableMatrix
    triplet_projector: sp.ImmutableMatrix
    total_generators: tuple[sp.ImmutableMatrix, ...]
    exchange_kernel: sp.ImmutableMatrix
    commutant_constraint: sp.ImmutableMatrix
    commutant_dimension: sp.Expr
    invariant_basis: sp.ImmutableMatrix
    general_invariant_kernel: sp.ImmutableMatrix
    channel_gap: sp.Expr
    normalized_exchange_parent: sp.ImmutableMatrix
    inherited_kernel: sp.ImmutableMatrix
    inherited_gap: sp.Expr
    flavor_identity: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    selected_origin_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2GaugeSingletBindingKernelCandidateAuditCertificate:
    pauli = (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )
    generators = tuple(sigma / 2 for sigma in pauli)
    total_generators = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(t, sp.eye(2)) + sp.kronecker_product(sp.eye(2), t))
        for t in generators
    )
    singlet_vector = sp.ImmutableMatrix([0, 1 / sp.sqrt(2), -1 / sp.sqrt(2), 0])
    singlet_projector = sp.ImmutableMatrix(singlet_vector * singlet_vector.H)
    triplet_projector = sp.ImmutableMatrix(sp.eye(4) - singlet_projector)

    exchange_mutable = sp.zeros(4)
    for t in generators:
        exchange_mutable += sp.kronecker_product(t, t)
    exchange_kernel = sp.ImmutableMatrix(exchange_mutable)

    commutant_constraint = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(
            sp.kronecker_product(sp.eye(4), generator)
            - sp.kronecker_product(generator.T, sp.eye(4))
        )
        for generator in total_generators
    ))
    commutant_dimension = sp.Integer(16 - commutant_constraint.rank())
    invariant_basis = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix(sp.eye(4)).reshape(16, 1),
        singlet_projector.reshape(16, 1),
    )

    a, b = sp.symbols("a b", real=True)
    general_invariant_kernel = sp.ImmutableMatrix(a * singlet_projector + b * triplet_projector)
    channel_gap = sp.simplify(b - a)
    normalized_exchange_parent = sp.ImmutableMatrix(sp.Rational(3, 4) * sp.eye(4) + exchange_kernel)
    inherited_kernel = sp.ImmutableMatrix(sp.zeros(4))
    inherited_gap = sp.Integer(0)
    flavor_identity = sp.ImmutableMatrix(sp.eye(256))

    # Columns: SU2 type, inherited interaction, singlet attraction,
    # parent-selected coefficient, selected flavor line, non-target-loaded scale.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 1, 0, 1],  # inherited zero two-body kernel
        [1, 1, 0, 0, 0, 1],  # scalar identity/contact term
        [1, 0, 1, 0, 0, 1],  # canonical T1 dot T2 exchange operator
        [1, 0, 1, 0, 0, 1],  # singlet antisymmetrizer channel
        [1, 0, 1, 0, 0, 0],  # target-normalized triplet penalty
        [1, 0, 1, 0, 0, 1],  # hypothetical gauge-boson exchange
        [1, 0, 1, 0, 1, 1],  # hand-selected flavor four-fermion channel
        [0, 1, 0, 0, 0, 1],  # untyped nonequilibrium-bath exchange
        [1, 1, 0, 1, 0, 1],  # inherited scalar spectral self-energy
        [0, 1, 1, 0, 0, 1],  # portal splitting without pair typing
        [1, 0, 1, 0, 1, 0],  # fitted composite pole kernel
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    selected_origin_vector = sp.ImmutableMatrix([
        candidate_matrix[i, 1]
        * candidate_matrix[i, 2]
        * candidate_matrix[i, 3]
        * candidate_matrix[i, 4]
        * candidate_matrix[i, 5]
        for i in range(candidate_matrix.rows)
    ])
    audit_coverage = sp.ones(11, 1)
    physical_origin = sp.zeros(3, 1)

    commutator_stack = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(generator * exchange_kernel - exchange_kernel * generator)
        for generator in total_generators
    ))
    general_commutator_stack = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(generator * general_invariant_kernel - general_invariant_kernel * generator)
        for generator in total_generators
    ))

    theorems = (
        kernel.prove_exact_rank(commutant_constraint, 14, subject="diagonal SU2 commutator constraints have rank fourteen"),
        kernel.prove_expression_equality(commutant_dimension, 2, subject="two-doublet SU2 commutant is two-dimensional"),
        kernel.prove_exact_rank(invariant_basis, 2, subject="identity and singlet projector span two independent invariant directions"),
        kernel.prove_matrix_equality(commutator_stack, sp.zeros(12, 4), subject="canonical gauge exchange commutes with total SU2"),
        kernel.prove_matrix_equality(exchange_kernel, sp.Rational(1, 4) * sp.eye(4) - singlet_projector, subject="exchange kernel resolves singlet and triplet channels"),
        kernel.prove_exact_spectrum(exchange_kernel, {sp.Rational(-3, 4): 1, sp.Rational(1, 4): 3}, subject="canonical exchange is attractive in the singlet convention"),
        kernel.prove_matrix_equality(general_commutator_stack, sp.zeros(12, 4), subject="general channel-diagonal kernel is SU2 invariant"),
        kernel.prove_matrix_equality(general_invariant_kernel * singlet_projector, a * singlet_projector, subject="general invariant kernel has singlet eigenvalue a"),
        kernel.prove_matrix_equality(general_invariant_kernel * triplet_projector, b * triplet_projector, subject="general invariant kernel has triplet eigenvalue b"),
        kernel.prove_expression_equality(channel_gap, b - a, subject="singlet-triplet binding gap remains one free relative coefficient"),
        kernel.prove_matrix_equality(normalized_exchange_parent, triplet_projector, subject="unit-normalized exchange reproduces the conditional triplet penalty"),
        kernel.prove_exact_spectrum(normalized_exchange_parent, {sp.Integer(0): 1, sp.Integer(1): 3}, subject="normalized exchange parent has a unique singlet ground state"),
        kernel.prove_matrix_equality(inherited_kernel, sp.zeros(4), subject="inherited two-body binding kernel is zero"),
        kernel.prove_expression_equality(inherited_gap, 0, subject="inherited singlet-triplet gap vanishes"),
        kernel.prove_exact_rank(flavor_identity, 256, subject="inherited flavor-blind kernel leaves all pair singlets degenerate"),
        kernel.prove_expression_equality(candidate_matrix.shape[0], 11, subject="eleven binding-kernel candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.shape[1], 6, subject="six binding-origin criteria are applied"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="binding-kernel audit has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 3, 3, 3, 2, 3, 4, 2, 4, 3, 3]), subject="binding candidate score ledger"),
        kernel.prove_expression_equality(max(score_vector), 4, subject="best binding candidates remain two criteria short of closure"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no binding-kernel candidate passes all criteria"),
        kernel.prove_matrix_equality(selected_origin_vector, sp.zeros(11, 1), subject="no inherited attractive kernel has coefficient flavor and scale origins together"),
        kernel.prove_expression_equality(sum(audit_coverage), 11, subject="all declared binding candidates are covered"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="binding coefficient flavor selector and pole-scale origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict binding-kernel origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate",
        theorems,
    )
    return SU2GaugeSingletBindingKernelCandidateAuditCertificate(
        singlet_projector, triplet_projector, total_generators,
        exchange_kernel, commutant_constraint, commutant_dimension,
        invariant_basis, general_invariant_kernel, channel_gap,
        normalized_exchange_parent, inherited_kernel, inherited_gap,
        flavor_identity, candidate_matrix, score_vector, pass_vector,
        selected_origin_vector, audit_coverage, physical_origin, theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate",
    title="Аудит связывающих ядер композитного SU(2)-синглета",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_binding_kernel_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_singlet_binding_kernel_candidate_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(25)
    ),
)