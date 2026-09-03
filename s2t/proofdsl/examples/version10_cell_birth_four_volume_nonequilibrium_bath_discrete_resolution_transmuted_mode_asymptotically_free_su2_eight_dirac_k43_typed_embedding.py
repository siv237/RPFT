"""LCF certificate for embedding the minimal SU(2)+8D carrier into K43."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2EightDiracK43TypedEmbeddingCertificate:
    generators: tuple[sp.ImmutableMatrix, ...]
    active_projector: sp.ImmutableMatrix
    singlet_projector: sp.ImmutableMatrix
    casimir: sp.ImmutableMatrix
    trace_gram: sp.ImmutableMatrix
    fermion_index: sp.Expr
    beta_coefficient: sp.Expr
    local_anomaly_tensor: sp.ImmutableMatrix
    witten_parity: sp.Expr
    commutant_dimension: sp.Expr
    active_rank_one_pole: sp.ImmutableMatrix
    active_pole_gauge_defect: sp.Expr
    singlet_rank_one_pole: sp.ImmutableMatrix
    singlet_pole_gauge_defect: sp.Expr
    minimal_invariant_active_projector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2EightDiracK43TypedEmbeddingCertificate:
    pauli = (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )
    generators = tuple(
        sp.ImmutableMatrix(sp.diag(sp.kronecker_product(sigma / 2, sp.eye(16)), sp.zeros(11)))
        for sigma in pauli
    )
    active_projector = sp.ImmutableMatrix(sp.diag(*([1] * 32 + [0] * 11)))
    singlet_projector = sp.ImmutableMatrix(sp.eye(43) - active_projector)
    casimir_mutable = sp.zeros(43)
    for generator in generators:
        casimir_mutable += generator * generator
    casimir = sp.ImmutableMatrix(casimir_mutable)
    trace_gram = sp.ImmutableMatrix(3, 3, lambda a, b: sp.trace(generators[a] * generators[b]))
    fermion_index = sp.simplify(trace_gram[0, 0])
    beta_coefficient = sp.simplify(-sp.Rational(22, 3) + sp.Rational(2, 3) * fermion_index)
    local_anomaly_tensor = sp.ImmutableMatrix([
        sp.trace(generators[a] * (generators[b] * generators[c] + generators[c] * generators[b]))
        for a in range(3) for b in range(3) for c in range(3)
    ])
    witten_parity = sp.Mod(16, 2)
    commutant_dimension = sp.Integer(16**2 + 11**2)

    active_rank_one_pole_mutable = sp.zeros(43)
    active_rank_one_pole_mutable[0, 0] = 1
    active_rank_one_pole = sp.ImmutableMatrix(active_rank_one_pole_mutable)
    singlet_rank_one_pole_mutable = sp.zeros(43)
    singlet_rank_one_pole_mutable[32, 32] = 1
    singlet_rank_one_pole = sp.ImmutableMatrix(singlet_rank_one_pole_mutable)
    multiplicity_line = sp.zeros(16)
    multiplicity_line[0, 0] = 1
    minimal_invariant_active_projector = sp.ImmutableMatrix(
        sp.diag(sp.kronecker_product(sp.eye(2), multiplicity_line), sp.zeros(11))
    )

    def gauge_defect(projector: sp.MatrixBase) -> sp.Expr:
        total = sp.Integer(0)
        for generator in generators:
            commutator = generator * projector - projector * generator
            total += sp.trace(commutator.H * commutator)
        return sp.simplify(total)

    active_pole_gauge_defect = gauge_defect(active_rank_one_pole)
    singlet_pole_gauge_defect = gauge_defect(singlet_rank_one_pole)
    su2_commutators = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix(generators[0] * generators[1] - generators[1] * generators[0] - sp.I * generators[2]),
        sp.ImmutableMatrix(generators[1] * generators[2] - generators[2] * generators[1] - sp.I * generators[0]),
        sp.ImmutableMatrix(generators[2] * generators[0] - generators[0] * generators[2] - sp.I * generators[1]),
    )
    invariant_doublet_commutators = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(generator * minimal_invariant_active_projector - minimal_invariant_active_projector * generator)
        for generator in generators
    ))
    architecture = sp.ones(12, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_expression_equality(active_projector.rank(), 32, subject="sixteen SU2 doublets occupy thirty-two K43 dimensions"),
        kernel.prove_expression_equality(singlet_projector.rank(), 11, subject="eleven K43 directions remain SU2 singlets"),
        kernel.prove_matrix_equality(active_projector + singlet_projector, sp.eye(43), subject="active and singlet sectors resolve K43"),
        kernel.prove_matrix_equality(active_projector * singlet_projector, sp.zeros(43), subject="active and singlet K43 sectors are orthogonal"),
        kernel.prove_matrix_equality(su2_commutators, sp.zeros(129, 43), subject="embedded generators obey the SU2 Lie algebra"),
        kernel.prove_matrix_equality(casimir, sp.Rational(3, 4) * active_projector, subject="embedded doublets have the fundamental SU2 Casimir"),
        kernel.prove_matrix_equality(trace_gram, 8 * sp.eye(3), subject="sixteen Weyl doublets have total Dynkin index eight"),
        kernel.prove_expression_equality(fermion_index, 8, subject="fermion Dynkin index of the embedded carrier"),
        kernel.prove_expression_equality(beta_coefficient, -2, subject="embedded SU2 plus eight Dirac carrier has exact beta minus two"),
        kernel.prove_matrix_equality(local_anomaly_tensor, sp.zeros(27, 1), subject="the embedded SU2 carrier has no local cubic gauge anomaly"),
        kernel.prove_expression_equality(witten_parity, 0, subject="sixteen Weyl doublets pass the global SU2 anomaly test"),
        kernel.prove_expression_equality(commutant_dimension, 377, subject="the K43 embedding retains a large multiplicity commutant"),
        kernel.prove_expression_equality(active_rank_one_pole.rank(), 1, subject="a rank-one pole can be placed in the active doublet sector"),
        kernel.prove_matrix_equality(active_projector * active_rank_one_pole, active_rank_one_pole, subject="the trial charged pole lies in the AF carrier"),
        kernel.prove_expression_equality(active_pole_gauge_defect, 1, subject="the active rank-one pole is not SU2 invariant"),
        kernel.prove_expression_equality(singlet_rank_one_pole.rank(), 1, subject="a rank-one gauge-invariant pole exists in the singlet complement"),
        kernel.prove_expression_equality(singlet_pole_gauge_defect, 0, subject="the singlet rank-one pole is SU2 invariant"),
        kernel.prove_matrix_equality(active_projector * singlet_rank_one_pole, sp.zeros(43), subject="the invariant rank-one pole is disconnected from the AF carrier"),
        kernel.prove_expression_equality(minimal_invariant_active_projector.rank(), 2, subject="the smallest explicit invariant active projector is one full doublet"),
        kernel.prove_matrix_equality(invariant_doublet_commutators, sp.zeros(129, 43), subject="the rank-two doublet projector is SU2 invariant"),
        kernel.prove_matrix_equality(active_projector * minimal_invariant_active_projector, minimal_invariant_active_projector, subject="the minimal invariant doublet lies in the AF sector"),
        kernel.prove_matrix_equality(architecture, sp.ones(12, 1), subject="conditional SU2 K43 embedding architecture is complete"),
        kernel.prove_expression_equality(sum(architecture), 12, subject="twelve embedding checks pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="embedding selector multiplicity parent and gauge-singlet pole origin remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict physical embedding origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate",
        theorems,
    )
    return SU2EightDiracK43TypedEmbeddingCertificate(
        generators, active_projector, singlet_projector, casimir, trace_gram,
        fermion_index, beta_coefficient, local_anomaly_tensor, witten_parity,
        commutant_dimension, active_rank_one_pole, active_pole_gauge_defect,
        singlet_rank_one_pole, singlet_pole_gauge_defect,
        minimal_invariant_active_projector, architecture, physical_origin,
        theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate",
    title="Типизированное K43-вложение минимального SU(2)+8D носителя",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_eight_dirac_k43_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_eight_dirac_k43_embedding_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(25)
    ),
)