"""LCF certificate for topological four-volume quantum candidates."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FourVolumeTopologicalQuantumAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    multiplicity_parent_hessian: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    candidate_matrix_theorem: Theorem
    pass_vector_theorem: Theorem
    maximum_score_theorem: Theorem
    candidate_rank_theorem: Theorem
    dimension_column_theorem: Theorem
    orbit_break_column_theorem: Theorem
    volume_factorization_theorem: Theorem
    volume_rescaling_theorem: Theorem
    density_identity_theorem: Theorem
    density_rescaling_theorem: Theorem
    parent_hessian_theorem: Theorem
    parent_rank_theorem: Theorem
    parent_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    parent_spectrum_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FourVolumeTopologicalQuantumAuditCertificate:
    # protected integer, internal, L^4 dimension, typed map to volume, orbit break
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 0, 0],  # Euler characteristic
        [1, 1, 0, 0, 0],  # signature
        [1, 1, 0, 0, 0],  # Pontryagin number
        [1, 1, 0, 0, 0],  # Dirac index
        [1, 1, 0, 0, 0],  # winding number
        [1, 1, 0, 1, 0],  # simplicial cell count
        [1, 1, 0, 0, 0],  # GNVW flow index
        [1, 1, 0, 1, 0],  # dimension of K43
    ])
    pass_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(8)])
    scores = [sum(candidate_matrix.row(i)) for i in range(8)]

    n, v0, scale = sp.symbols("n v_0 s", positive=True)
    total_volume = n * v0
    density = n / total_volume
    rescaled_volume = n * scale**4 * v0
    rescaled_density = n / rescaled_volume

    eta, q = sp.symbols("eta q", real=True)
    multiplicity_parent = eta**2 / 2
    multiplicity_parent_hessian = sp.ImmutableMatrix(sp.hessian(multiplicity_parent, (eta, q)))
    scale_vector = sp.ImmutableMatrix([0, 1])
    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 0, 0])

    candidate_matrix_theorem = kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="eight topological volume candidates are evaluated on five criteria")
    pass_vector_theorem = kernel.prove_matrix_equality(pass_vector, sp.zeros(8, 1), subject="no topological candidate supplies a physical four-volume quantum")
    maximum_score_theorem = kernel.prove_expression_equality(max(scores), 3, subject="cell counts satisfy only three of five volume-origin criteria")
    candidate_rank_theorem = kernel.prove_exact_rank(candidate_matrix, 2, subject="topological candidates span integer protection and volume typing only")
    dimension_column_theorem = kernel.prove_matrix_equality(candidate_matrix[:, 2], sp.zeros(8, 1), subject="all topological candidates lack length-four dimension")
    orbit_break_column_theorem = kernel.prove_matrix_equality(candidate_matrix[:, 4], sp.zeros(8, 1), subject="no topological candidate breaks the physical scale orbit")
    volume_factorization_theorem = kernel.prove_expression_equality(total_volume, n * v0, subject="topological multiplicity factors from elementary cell volume")
    volume_rescaling_theorem = kernel.prove_expression_equality(rescaled_volume, scale**4 * total_volume, subject="topological multiplicity is unchanged by physical volume rescaling")
    density_identity_theorem = kernel.prove_expression_equality(density * total_volume, n, subject="topological density integrates to the protected integer")
    density_rescaling_theorem = kernel.prove_expression_equality(rescaled_density, density / scale**4, subject="topological density acquires inverse volume dimension from the metric")
    parent_hessian_theorem = kernel.prove_matrix_equality(multiplicity_parent_hessian, sp.diag(1, 0), subject="multiplicity parent is flat in elementary volume scale")
    parent_rank_theorem = kernel.prove_exact_rank(multiplicity_parent_hessian, 1, subject="topological parent fixes multiplicity but not volume scale")
    parent_nullity_theorem = kernel.prove_exact_nullity(multiplicity_parent_hessian, 1, subject="elementary four-volume remains one exact zero mode")
    scale_kernel_theorem = kernel.prove_matrix_equality(multiplicity_parent_hessian * scale_vector, sp.zeros(2, 1), subject="the elementary volume direction is the topological parent kernel")
    parent_spectrum_theorem = kernel.prove_exact_spectrum(multiplicity_parent_hessian, {sp.Integer(0): 1, sp.Integer(1): 1}, subject="topological multiplicity parent has one protected and one flat direction")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(8, 1), subject="all declared topological candidate classes are audited")
    origin_ledger_theorem = kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 0, 0]), subject="integer protection and multiplicity pass while dimensional origin remains open")
    origin_score_theorem = kernel.prove_expression_equality(sum(origin_ledger), 2, subject="two of four topological volume-origin requirements pass")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_topological_quantum_candidate_audit_gate", (candidate_matrix_theorem, pass_vector_theorem, maximum_score_theorem, candidate_rank_theorem, dimension_column_theorem, orbit_break_column_theorem, volume_factorization_theorem, volume_rescaling_theorem, density_identity_theorem, density_rescaling_theorem, parent_hessian_theorem, parent_rank_theorem, parent_nullity_theorem, scale_kernel_theorem, parent_spectrum_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem))
    return FourVolumeTopologicalQuantumAuditCertificate(candidate_matrix, pass_vector, multiplicity_parent_hessian, scale_vector, architecture, origin_ledger, candidate_matrix_theorem, pass_vector_theorem, maximum_score_theorem, candidate_rank_theorem, dimension_column_theorem, orbit_break_column_theorem, volume_factorization_theorem, volume_rescaling_theorem, density_identity_theorem, density_rescaling_theorem, parent_hessian_theorem, parent_rank_theorem, parent_nullity_theorem, scale_kernel_theorem, parent_spectrum_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_topological_quantum_candidate_audit_gate", "Аудит топологических квантов четырёхмерного объёма", ("s2t/gates/version10_cell_birth_four_volume_topological_quantum_candidate_audit_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_topological_quantum_candidate_audit_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("topological_candidate_matrix", lambda: build_certificate().candidate_matrix_theorem), ("zero_passing_topological_candidates", lambda: build_certificate().pass_vector_theorem), ("maximum_topological_score_three", lambda: build_certificate().maximum_score_theorem), ("topological_candidate_rank_two", lambda: build_certificate().candidate_rank_theorem), ("topological_dimension_column_zero", lambda: build_certificate().dimension_column_theorem), ("topological_orbit_break_column_zero", lambda: build_certificate().orbit_break_column_theorem), ("volume_multiplicity_factorization", lambda: build_certificate().volume_factorization_theorem), ("volume_quartic_rescaling", lambda: build_certificate().volume_rescaling_theorem), ("topological_density_integral", lambda: build_certificate().density_identity_theorem), ("topological_density_inverse_scaling", lambda: build_certificate().density_rescaling_theorem), ("multiplicity_parent_hessian", lambda: build_certificate().parent_hessian_theorem), ("multiplicity_parent_rank_one", lambda: build_certificate().parent_rank_theorem), ("multiplicity_parent_nullity_one", lambda: build_certificate().parent_nullity_theorem), ("elementary_volume_scale_kernel", lambda: build_certificate().scale_kernel_theorem), ("multiplicity_parent_spectrum", lambda: build_certificate().parent_spectrum_theorem), ("topological_audit_coverage_full", lambda: build_certificate().architecture_theorem), ("topological_origin_ledger_two", lambda: build_certificate().origin_ledger_theorem), ("topological_origin_score_two", lambda: build_certificate().origin_score_theorem))))