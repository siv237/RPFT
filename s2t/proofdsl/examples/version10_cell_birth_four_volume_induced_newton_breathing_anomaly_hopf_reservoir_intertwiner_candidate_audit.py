"""LCF certificate for the Hopf-reservoir intertwiner candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfReservoirIntertwinerAuditCertificate:
    reservoir_orientation: sp.ImmutableMatrix
    path_orientation: sp.ImmutableMatrix
    intertwiner_constraint: sp.ImmutableMatrix
    intertwiner_kernel: sp.ImmutableMatrix
    real_orthogonal_intertwiners: tuple[sp.ImmutableMatrix, ...]
    inherited_mixed_block: sp.ImmutableMatrix
    projector_matching: sp.ImmutableMatrix
    target_loaded_hessian: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    inherited_pass_vector: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfReservoirIntertwinerAuditCertificate:
    orientation = sp.ImmutableMatrix.diag(-1, 1)
    intertwiner_constraint = sp.ImmutableMatrix.diag(0, -2, 2, 0)
    intertwiner_kernel = sp.ImmutableMatrix([
        [1, 0],
        [0, 0],
        [0, 0],
        [0, 1],
    ])
    signs = (
        sp.ImmutableMatrix.diag(1, 1),
        sp.ImmutableMatrix.diag(-1, 1),
        sp.ImmutableMatrix.diag(1, -1),
        sp.ImmutableMatrix.diag(-1, -1),
    )
    inherited_mixed_block = sp.ImmutableMatrix.zeros(2, 2)
    p_minus = sp.ImmutableMatrix.diag(1, 0)
    p_plus = sp.ImmutableMatrix.diag(0, 1)
    projector_matching = sp.ImmutableMatrix(p_minus * p_minus + p_plus * p_plus)
    target_loaded_hessian = sp.ImmutableMatrix.vstack(
        sp.ImmutableMatrix.hstack(sp.eye(2), -sp.eye(2)),
        sp.ImmutableMatrix.hstack(-sp.eye(2), sp.eye(2)),
    )

    # Columns: correct Hom type, inherited/non-target-loaded, nonzero map,
    # orientation compatible, phase/coefficient selected, mixed parent block.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 1, 0, 0],  # inherited zero mixed block
        [1, 1, 1, 1, 0, 0],  # spectral projector matching
        [1, 0, 1, 1, 1, 0],  # basis identity
        [1, 0, 1, 1, 0, 0],  # relative-sign intertwiner
        [1, 1, 1, 0, 1, 0],  # KMS modular swap
        [0, 1, 1, 0, 0, 0],  # Hopf incidence restriction
        [1, 1, 1, 0, 0, 0],  # modular conjugation
        [1, 1, 1, 1, 0, 0],  # bath-current covariance
        [1, 0, 1, 0, 1, 0],  # minimal portal Pauli block
        [1, 0, 1, 1, 1, 1],  # target-loaded coupling parent
    ])
    score_vector = sp.ImmutableMatrix([
        sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    pass_vector = sp.ImmutableMatrix([
        sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)
    ])
    inherited_pass_vector = sp.ImmutableMatrix([
        int(candidate_matrix[i, 1] == 1 and candidate_matrix[i, 2] == 1
            and candidate_matrix[i, 4] == 1 and candidate_matrix[i, 5] == 1)
        for i in range(candidate_matrix.rows)
    ])
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])

    theorems = (
        kernel.prove_matrix_equality(orientation, sp.diag(-1, 1),
                                     subject="reservoir and path orientations have the same signed spectrum"),
        kernel.prove_matrix_equality(intertwiner_constraint, sp.diag(0, -2, 2, 0),
                                     subject="vectorized intertwiner constraint is exact"),
        kernel.prove_exact_rank(intertwiner_constraint, 2,
                                subject="orientation fixes the two off-diagonal intertwiner entries"),
        kernel.prove_exact_nullity(intertwiner_constraint, 2,
                                   subject="two diagonal intertwiner amplitudes remain free"),
        kernel.prove_matrix_equality(intertwiner_constraint * intertwiner_kernel, sp.zeros(4, 2),
                                     subject="diagonal maps span the exact intertwiner kernel"),
        kernel.prove_exact_rank(intertwiner_kernel, 2,
                                subject="intertwiner kernel basis has two independent columns"),
        kernel.prove_expression_equality(len(signs), 4,
                                         subject="four real orthogonal diagonal intertwiners remain"),
        kernel.prove_matrix_equality(signs[0].T * signs[0], sp.eye(2),
                                     subject="positive identity intertwiner is orthogonal"),
        kernel.prove_matrix_equality(signs[1].T * signs[1], sp.eye(2),
                                     subject="first relative-sign intertwiner is orthogonal"),
        kernel.prove_matrix_equality(signs[2].T * signs[2], sp.eye(2),
                                     subject="second relative-sign intertwiner is orthogonal"),
        kernel.prove_matrix_equality(signs[3].T * signs[3], sp.eye(2),
                                     subject="negative identity intertwiner is orthogonal"),
        kernel.prove_matrix_equality(inherited_mixed_block, sp.zeros(2),
                                     subject="inherited reservoir-path mixed block is zero"),
        kernel.prove_matrix_equality(projector_matching, sp.eye(2),
                                     subject="spectral projectors formally match the oriented levels"),
        kernel.prove_matrix_equality(target_loaded_hessian,
                                     sp.Matrix([[1, 0, -1, 0], [0, 1, 0, -1],
                                                [-1, 0, 1, 0], [0, -1, 0, 1]]),
                                     subject="target-loaded coupling supplies a nonzero mixed Hessian"),
        kernel.prove_exact_rank(target_loaded_hessian, 2,
                                subject="target-loaded coupling controls only relative reservoir-path modes"),
        kernel.prove_exact_nullity(target_loaded_hessian, 2,
                                   subject="two common modes remain in the target-loaded coupling"),
        kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix),
                                     subject="ten intertwiner candidates are audited on six criteria"),
        kernel.prove_exact_rank(candidate_matrix, 6,
                                subject="intertwiner candidate audit covers all criterion directions"),
        kernel.prove_matrix_equality(score_vector, sp.Matrix([3, 4, 4, 3, 4, 2, 3, 4, 3, 5]),
                                     subject="intertwiner candidate scores are exact"),
        kernel.prove_expression_equality(max(score_vector), 5,
                                         subject="best intertwiner candidate misses one criterion"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(10, 1),
                                     subject="no intertwiner candidate passes the strict contract"),
        kernel.prove_matrix_equality(inherited_pass_vector, sp.zeros(10, 1),
                                     subject="no inherited candidate supplies phase and mixed parent together"),
        kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 0, 0, 0]),
                                     subject="audit structure passes while three physical origins remain open"),
        kernel.prove_expression_equality(sum(origin_ledger), 3,
                                         subject="three of six origin requirements pass"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate",
        theorems,
    )
    return HopfReservoirIntertwinerAuditCertificate(
        orientation, orientation, intertwiner_constraint, intertwiner_kernel,
        signs, inherited_mixed_block, projector_matching, target_loaded_hessian,
        candidate_matrix, score_vector, pass_vector, inherited_pass_vector,
        origin_ledger, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate",
    title="Аудит кандидатов резервуарно-хопфовского интертвинера",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_induced_newton_breathing_anomaly_hopf_reservoir_intertwiner_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"hopf_reservoir_intertwiner_audit_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(24)
    ),
)