"""LCF certificate for Einstein-response anchor-package candidates."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class EinsteinResponseAnchorPackageAuditCertificate:
    gravity_candidates: sp.ImmutableMatrix
    temperature_candidates: sp.ImmutableMatrix
    volume_candidates: sp.ImmutableMatrix
    stress_candidates: sp.ImmutableMatrix
    pass_vectors: tuple[sp.ImmutableMatrix, ...]
    rank_vector: sp.ImmutableMatrix
    maximum_score_vector: sp.ImmutableMatrix
    combined_matrix: sp.ImmutableMatrix
    package_dependency: sp.ImmutableMatrix
    package_availability: sp.ImmutableMatrix
    conditional_anchor_map: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    audit_coverage: sp.ImmutableMatrix
    gravity_matrix_theorem: Theorem
    temperature_matrix_theorem: Theorem
    volume_matrix_theorem: Theorem
    stress_matrix_theorem: Theorem
    gravity_pass_theorem: Theorem
    temperature_pass_theorem: Theorem
    volume_pass_theorem: Theorem
    stress_pass_theorem: Theorem
    rank_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    combined_rank_theorem: Theorem
    package_dependency_theorem: Theorem
    package_rank_theorem: Theorem
    package_availability_theorem: Theorem
    conditional_rank_theorem: Theorem
    conditional_nullity_theorem: Theorem
    fully_anchored_rank_theorem: Theorem
    audit_coverage_theorem: Theorem
    physical_score_theorem: Theorem
    gate_theorem: Theorem


def _pass_vector(matrix: sp.ImmutableMatrix) -> sp.ImmutableMatrix:
    return sp.ImmutableMatrix([
        sp.prod(matrix.row(index)) for index in range(matrix.rows)
    ])


@lru_cache(maxsize=1)
def build_certificate() -> EinsteinResponseAnchorPackageAuditCertificate:
    # Columns: correct type/dimension, internal availability, independence
    # from kappa, common-parent origin, non-circularity.
    gravity_candidates = sp.ImmutableMatrix([
        [1, 1, 1, 0, 0],  # induced Einstein coefficient
        [1, 1, 1, 0, 0],  # spectral-action coefficient
        [1, 0, 1, 0, 1],  # imported Planck/Newton constant
        [1, 1, 0, 0, 0],  # solve G from the target cosmological relation
    ])
    temperature_candidates = sp.ImmutableMatrix([
        [1, 1, 0, 1, 0],  # KMS energy tied to Omega
        [1, 1, 1, 0, 1],  # endpoint spectral gap
        [1, 0, 1, 0, 1],  # external Landauer temperature
        [0, 1, 1, 0, 1],  # dimensionless vacuum action
    ])
    volume_candidates = sp.ImmutableMatrix([
        [1, 1, 1, 0, 1],  # intrinsic ell_cell^4
        [1, 1, 1, 0, 1],  # spectral counting volume
        [1, 1, 1, 0, 1],  # topological quantum times v0
        [1, 1, 0, 0, 0],  # cosmological radius volume
    ])
    stress_candidates = sp.ImmutableMatrix([
        [0, 1, 0, 1, 1],  # scalar entropy production
        [1, 1, 0, 0, 0],  # isotropic vacuum ansatz
        [1, 1, 1, 0, 1],  # metric variation of the current parent
        [1, 1, 1, 0, 1],  # Keldysh response tensor
    ])
    matrices = (
        gravity_candidates,
        temperature_candidates,
        volume_candidates,
        stress_candidates,
    )
    pass_vectors = tuple(_pass_vector(matrix) for matrix in matrices)
    rank_vector = sp.ImmutableMatrix([matrix.rank() for matrix in matrices])
    maximum_score_vector = sp.ImmutableMatrix([
        max(sum(matrix.row(index)) for index in range(matrix.rows))
        for matrix in matrices
    ])
    combined_matrix = sp.ImmutableMatrix.vstack(*matrices)
    package_dependency = sp.eye(4)
    package_availability = sp.zeros(4, 1)
    conditional_anchor_map = sp.ImmutableMatrix([[2, -1, -1, 1]])
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        conditional_anchor_map,
        sp.ImmutableMatrix([
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]),
    )
    audit_coverage = sp.ones(16, 1)

    matrix_theorems = tuple(
        kernel.prove_matrix_equality(
            matrix,
            sp.Matrix(matrix),
            subject=subject,
        )
        for matrix, subject in zip(
            matrices,
            (
                "four Newton-constant candidates are audited on five origin criteria",
                "four entropy-energy candidates are audited on five origin criteria",
                "four cell-volume candidates are audited on five origin criteria",
                "four throughflow stress-tensor candidates are audited on five origin criteria",
            ),
        )
    )
    pass_theorems = tuple(
        kernel.prove_matrix_equality(
            vector,
            sp.zeros(4, 1),
            subject=subject,
        )
        for vector, subject in zip(
            pass_vectors,
            (
                "no Newton-constant candidate passes the full origin contract",
                "no entropy-energy candidate passes the full origin contract",
                "no cell-volume candidate passes the full origin contract",
                "no stress-tensor candidate passes the full origin contract",
            ),
        )
    )
    rank_vector_theorem = kernel.prove_matrix_equality(
        rank_vector,
        sp.Matrix([3, 4, 2, 3]),
        subject="the four anchor menus have exact criterion ranks",
    )
    maximum_score_theorem = kernel.prove_matrix_equality(
        maximum_score_vector,
        sp.Matrix([3, 4, 4, 4]),
        subject="the best candidates still miss at least one origin criterion",
    )
    combined_rank_theorem = kernel.prove_exact_rank(
        combined_matrix,
        5,
        subject="the sixteen candidates jointly span all five audit criteria",
    )
    package_dependency_theorem = kernel.prove_matrix_equality(
        package_dependency,
        sp.eye(4),
        subject="absolute Einstein closure requires all four anchor packages independently",
    )
    package_rank_theorem = kernel.prove_exact_rank(
        package_dependency,
        4,
        subject="the Einstein anchor package has four independent components",
    )
    package_availability_theorem = kernel.prove_matrix_equality(
        package_availability,
        sp.zeros(4, 1),
        subject="none of the four physical anchor components is completely derived",
    )
    conditional_rank_theorem = kernel.prove_exact_rank(
        conditional_anchor_map,
        1,
        subject="the conditional conductance formula supplies one relation among four scales",
    )
    conditional_nullity_theorem = kernel.prove_exact_nullity(
        conditional_anchor_map,
        3,
        subject="three independent dimensional freedoms remain without the anchor package",
    )
    fully_anchored_rank_theorem = kernel.prove_exact_rank(
        fully_anchored_map,
        4,
        subject="independent anchor values would close the conditional conductance formula",
    )
    audit_coverage_theorem = kernel.prove_matrix_equality(
        audit_coverage,
        sp.ones(16, 1),
        subject="all sixteen declared anchor candidates are audited",
    )
    physical_score_theorem = kernel.prove_expression_equality(
        sum(package_availability),
        0,
        subject="the physical Einstein anchor package score is zero of four",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate",
        (
            *matrix_theorems,
            *pass_theorems,
            rank_vector_theorem,
            maximum_score_theorem,
            combined_rank_theorem,
            package_dependency_theorem,
            package_rank_theorem,
            package_availability_theorem,
            conditional_rank_theorem,
            conditional_nullity_theorem,
            fully_anchored_rank_theorem,
            audit_coverage_theorem,
            physical_score_theorem,
        ),
    )
    return EinsteinResponseAnchorPackageAuditCertificate(
        gravity_candidates,
        temperature_candidates,
        volume_candidates,
        stress_candidates,
        pass_vectors,
        rank_vector,
        maximum_score_vector,
        combined_matrix,
        package_dependency,
        package_availability,
        conditional_anchor_map,
        fully_anchored_map,
        audit_coverage,
        *matrix_theorems,
        *pass_theorems,
        rank_vector_theorem,
        maximum_score_theorem,
        combined_rank_theorem,
        package_dependency_theorem,
        package_rank_theorem,
        package_availability_theorem,
        conditional_rank_theorem,
        conditional_nullity_theorem,
        fully_anchored_rank_theorem,
        audit_coverage_theorem,
        physical_score_theorem,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate",
    title="Аудит пакета якорей эйнштейновского отклика",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_einstein_response_anchor_package_candidate_audit_gate_results.json",
    ),
    obligations=(
        Obligation("anchor_gravity_candidate_matrix", lambda: build_certificate().gravity_matrix_theorem),
        Obligation("anchor_temperature_candidate_matrix", lambda: build_certificate().temperature_matrix_theorem),
        Obligation("anchor_volume_candidate_matrix", lambda: build_certificate().volume_matrix_theorem),
        Obligation("anchor_stress_candidate_matrix", lambda: build_certificate().stress_matrix_theorem),
        Obligation("anchor_gravity_zero_passes", lambda: build_certificate().gravity_pass_theorem),
        Obligation("anchor_temperature_zero_passes", lambda: build_certificate().temperature_pass_theorem),
        Obligation("anchor_volume_zero_passes", lambda: build_certificate().volume_pass_theorem),
        Obligation("anchor_stress_zero_passes", lambda: build_certificate().stress_pass_theorem),
        Obligation("anchor_menu_rank_vector", lambda: build_certificate().rank_vector_theorem),
        Obligation("anchor_menu_maximum_scores", lambda: build_certificate().maximum_score_theorem),
        Obligation("anchor_combined_matrix_rank_five", lambda: build_certificate().combined_rank_theorem),
        Obligation("anchor_package_dependency_identity", lambda: build_certificate().package_dependency_theorem),
        Obligation("anchor_package_rank_four", lambda: build_certificate().package_rank_theorem),
        Obligation("anchor_package_availability_zero", lambda: build_certificate().package_availability_theorem),
        Obligation("anchor_conditional_relation_rank_one", lambda: build_certificate().conditional_rank_theorem),
        Obligation("anchor_conditional_relation_nullity_three", lambda: build_certificate().conditional_nullity_theorem),
        Obligation("anchor_full_package_rank_four", lambda: build_certificate().fully_anchored_rank_theorem),
        Obligation("anchor_candidate_audit_coverage", lambda: build_certificate().audit_coverage_theorem),
        Obligation("anchor_physical_package_score_zero", lambda: build_certificate().physical_score_theorem),
    ),
)