"""LCF audit of flavor-pair selectors for the composite SU(2) singlet."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class FlavorPairSelectorAuditCertificate:
    identity: sp.ImmutableMatrix
    democratic_projector: sp.ImmutableMatrix
    basis_projector: sp.ImmutableMatrix
    cyclic_shift: sp.ImmutableMatrix
    basis_symmetry_defect: sp.ImmutableMatrix
    pair_multiplicity: sp.Expr
    diagonal_pair_rank: sp.Expr
    symmetric_pair_rank: sp.Expr
    antisymmetric_pair_rank: sp.Expr
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    origin_vector: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> FlavorPairSelectorAuditCertificate:
    identity = sp.ImmutableMatrix(sp.eye(16))
    democratic_vector = sp.ImmutableMatrix(sp.ones(16, 1) / 4)
    democratic_projector = sp.ImmutableMatrix(democratic_vector * democratic_vector.H)
    e0 = sp.ImmutableMatrix([1] + [0] * 15)
    basis_projector = sp.ImmutableMatrix(e0 * e0.H)
    shift_mutable = sp.zeros(16)
    for i in range(16):
        shift_mutable[(i + 1) % 16, i] = 1
    cyclic_shift = sp.ImmutableMatrix(shift_mutable)
    basis_symmetry_defect = sp.ImmutableMatrix(cyclic_shift * basis_projector - basis_projector * cyclic_shift)
    pair_multiplicity = sp.Integer(16**2)
    diagonal_pair_rank = sp.Integer(16)
    symmetric_pair_rank = sp.Integer(16 * 17 // 2)
    antisymmetric_pair_rank = sp.Integer(16 * 15 // 2)
    # rank one, internal, residual-symmetry invariant, selected parent,
    # fermionic compatibility, non-target-loaded.
    candidate_matrix = sp.ImmutableMatrix([
        [0,1,1,1,1,1], [0,1,1,0,1,1], [0,1,1,0,1,1],
        [0,1,1,0,1,1], [1,1,0,0,1,1], [1,1,1,0,1,1],
        [1,1,1,0,1,1], [1,0,0,0,0,1], [1,0,0,0,1,1],
        [1,1,0,1,1,0],
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(10)])
    pass_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(10)])
    origin_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(10)])
    physical_origin = sp.zeros(2, 1)
    theorems = (
        kernel.prove_exact_rank(identity,16,subject="flavor identity leaves all one-particle copies degenerate"),
        kernel.prove_expression_equality(pair_multiplicity,256,subject="two flavor slots contain two hundred fifty-six pairs"),
        kernel.prove_expression_equality(diagonal_pair_rank,16,subject="same-flavor diagonal has rank sixteen"),
        kernel.prove_expression_equality(symmetric_pair_rank,136,subject="symmetric flavor-pair sector rank"),
        kernel.prove_expression_equality(antisymmetric_pair_rank,120,subject="antisymmetric flavor-pair sector rank"),
        kernel.prove_matrix_equality(democratic_projector*democratic_projector,democratic_projector,subject="democratic flavor selector is a projector"),
        kernel.prove_exact_rank(democratic_projector,1,subject="democratic flavor selector has rank one"),
        kernel.prove_matrix_equality(cyclic_shift*democratic_projector-democratic_projector*cyclic_shift,sp.zeros(16),subject="democratic selector preserves cyclic flavor symmetry"),
        kernel.prove_exact_rank(basis_projector,1,subject="basis flavor line is rank one"),
        kernel.prove_exact_rank(basis_symmetry_defect,2,subject="basis selector breaks cyclic flavor symmetry"),
        kernel.prove_expression_equality(candidate_matrix.shape[0],10,subject="ten flavor selectors are audited"),
        kernel.prove_expression_equality(candidate_matrix.shape[1],6,subject="six selector criteria are applied"),
        kernel.prove_exact_rank(candidate_matrix,6,subject="flavor selector audit has full criterion rank"),
        kernel.prove_matrix_equality(score_vector,sp.Matrix([5,4,4,4,4,5,5,2,3,4]),subject="flavor selector score ledger"),
        kernel.prove_expression_equality(max(score_vector),5,subject="best selector remains below closure"),
        kernel.prove_matrix_equality(pass_vector,sp.zeros(10,1),subject="no flavor selector passes all criteria"),
        kernel.prove_matrix_equality(origin_vector,sp.zeros(10,1),subject="no rank-one selector has complete physical origin"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(2,1),subject="selector parent and pole map remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict flavor origin score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_pair_selector_candidate_audit_gate",theorems)
    return FlavorPairSelectorAuditCertificate(identity,democratic_projector,basis_projector,cyclic_shift,basis_symmetry_defect,pair_multiplicity,diagonal_pair_rank,symmetric_pair_rank,antisymmetric_pair_rank,candidate_matrix,score_vector,pass_vector,origin_vector,physical_origin,theorems,gate_theorem)

SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_pair_selector_candidate_audit_gate",title="Аудит селектора flavor-пары композитного SU(2)-синглета",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_pair_selector_candidate_audit_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_pair_selector_candidate_audit_gate_results.json"),obligations=tuple(Obligation(f"su2_singlet_flavor_selector_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(19)))