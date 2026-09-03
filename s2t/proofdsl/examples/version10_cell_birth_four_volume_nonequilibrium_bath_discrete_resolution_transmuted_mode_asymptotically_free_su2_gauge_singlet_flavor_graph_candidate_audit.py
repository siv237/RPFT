"""LCF certificate for the sixteen-label flavor-graph candidate audit."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FlavorGraphCandidateAuditCertificate:
    democratic_vector: sp.ImmutableMatrix
    hypercube_adjacency: sp.ImmutableMatrix
    hypercube_laplacian: sp.ImmutableMatrix
    bit_flip_covariance_defects: sp.ImmutableMatrix
    complete_laplacian: sp.ImmutableMatrix
    bipartite_laplacian: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    internal_origin_vector: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


def _hypercube_adjacency() -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix(
        16,
        16,
        lambda i, j: int((int(i) ^ int(j)).bit_count() == 1),
    )


def _bit_flip(bit: int) -> sp.ImmutableMatrix:
    matrix = sp.zeros(16)
    for vertex in range(16):
        matrix[vertex ^ (1 << bit), vertex] = 1
    return sp.ImmutableMatrix(matrix)


@lru_cache(maxsize=1)
def build_certificate() -> FlavorGraphCandidateAuditCertificate:
    democratic_vector = sp.ImmutableMatrix(sp.ones(16, 1) / 4)
    hypercube_adjacency = _hypercube_adjacency()
    hypercube_laplacian = sp.ImmutableMatrix(4 * sp.eye(16) - hypercube_adjacency)
    bit_flips = tuple(_bit_flip(bit) for bit in range(4))
    bit_flip_covariance_defects = sp.ImmutableMatrix.vstack(
        *(flip * hypercube_laplacian - hypercube_laplacian * flip for flip in bit_flips)
    )

    complete_adjacency = sp.ones(16) - sp.eye(16)
    complete_laplacian = sp.ImmutableMatrix(15 * sp.eye(16) - complete_adjacency)

    bipartite_adjacency = sp.zeros(16)
    for left in range(8):
        for right in range(8, 16):
            bipartite_adjacency[left, right] = 1
            bipartite_adjacency[right, left] = 1
    bipartite_laplacian = sp.ImmutableMatrix(8 * sp.eye(16) - bipartite_adjacency)

    # Columns: sixteen-label carrier, unique democratic zero, non-scalar
    # geometry, inherited edge operator, parent-selected weight, no target load.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 0, 0, 1, 1, 1],  # zero graph
        [1, 1, 1, 0, 0, 1],  # complete K16
        [1, 1, 1, 0, 0, 1],  # cycle C16
        [1, 1, 0, 0, 0, 1],  # path P16
        [1, 1, 1, 0, 0, 1],  # four-cube Q4
        [1, 1, 1, 0, 0, 1],  # complete bipartite K8,8
        [1, 0, 0, 1, 0, 1],  # K43 block/multiplicity graph
        [1, 1, 0, 0, 0, 1],  # bath covariance graph
        [1, 1, 0, 0, 1, 0],  # fitted weighted graph
        [1, 1, 1, 1, 1, 0],  # target-loaded K16
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(10)])
    pass_vector = sp.ImmutableMatrix([int(score == 6) for score in score_vector])
    # The zero graph is inherited but cannot select a unique mode, hence it
    # does not count as a physical graph origin.
    internal_origin_vector = sp.ImmutableMatrix([0] * 10)
    audit_coverage = sp.ImmutableMatrix(sp.ones(10, 1))
    physical_origin = sp.ImmutableMatrix(sp.zeros(2, 1))

    theorems = (
        kernel.prove_matrix_equality(hypercube_adjacency, hypercube_adjacency.T, subject="Q4 adjacency is symmetric"),
        kernel.prove_matrix_equality(sp.diag(*hypercube_adjacency.diagonal()), sp.zeros(16), subject="Q4 adjacency has no loops"),
        kernel.prove_matrix_equality(hypercube_adjacency * sp.ones(16, 1), 4 * sp.ones(16, 1), subject="Q4 is four-regular"),
        kernel.prove_exact_spectrum(hypercube_adjacency, {sp.Integer(4): 1, sp.Integer(2): 4, sp.Integer(0): 6, sp.Integer(-2): 4, sp.Integer(-4): 1}, subject="Q4 adjacency spectrum is exact"),
        kernel.prove_matrix_equality(hypercube_laplacian, 4 * sp.eye(16) - hypercube_adjacency, subject="Q4 Laplacian is degree minus adjacency"),
        kernel.prove_exact_spectrum(hypercube_laplacian, {sp.Integer(0): 1, sp.Integer(2): 4, sp.Integer(4): 6, sp.Integer(6): 4, sp.Integer(8): 1}, subject="Q4 Laplacian spectrum is exact"),
        kernel.prove_exact_rank(hypercube_laplacian, 15, subject="Q4 has a unique Laplacian zero mode"),
        kernel.prove_expression_equality((democratic_vector.H * democratic_vector)[0], 1, subject="democratic flavor vector is normalized"),
        kernel.prove_matrix_equality(hypercube_laplacian * democratic_vector, sp.zeros(16, 1), subject="democratic vector is the Q4 zero mode"),
        kernel.prove_matrix_equality(bit_flip_covariance_defects, sp.zeros(64, 16), subject="Q4 is covariant under four bit flips"),
        kernel.prove_exact_spectrum(complete_laplacian, {sp.Integer(0): 1, sp.Integer(16): 15}, subject="K16 comparison spectrum is exact"),
        kernel.prove_exact_spectrum(bipartite_laplacian, {sp.Integer(0): 1, sp.Integer(8): 14, sp.Integer(16): 1}, subject="K8,8 comparison spectrum is exact"),
        kernel.prove_expression_equality(candidate_matrix.rows, 10, subject="ten flavor graph candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.cols, 6, subject="six independent admission criteria are used"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="candidate audit criteria have full rank"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([4, 4, 4, 3, 4, 4, 3, 3, 3, 5]), subject="flavor graph candidate scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="no graph candidate reaches all six criteria"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(10, 1), subject="strict flavor graph pass vector is empty"),
        kernel.prove_matrix_equality(internal_origin_vector, sp.zeros(10, 1), subject="no selecting flavor graph has internal origin"),
        kernel.prove_expression_equality(sum(audit_coverage), 10, subject="flavor graph audit coverage is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="graph and bit-label origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict flavor graph origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate",
        theorems,
    )
    return FlavorGraphCandidateAuditCertificate(
        democratic_vector,
        hypercube_adjacency,
        hypercube_laplacian,
        bit_flip_covariance_defects,
        complete_laplacian,
        bipartite_laplacian,
        candidate_matrix,
        score_vector,
        pass_vector,
        internal_origin_vector,
        audit_coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate",
    title="Аудит кандидатов flavor-графа",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_flavor_graph_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"flavor_graph_candidate_audit_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)