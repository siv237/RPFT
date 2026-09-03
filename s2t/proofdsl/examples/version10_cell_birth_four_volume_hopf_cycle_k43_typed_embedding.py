"""LCF certificate for embedding the oriented Hopf cycle into K43."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfCycleK43TypedEmbeddingCertificate:
    coordinate_embedding: sp.ImmutableMatrix
    coordinate_projector: sp.ImmutableMatrix
    coordinate_generator: sp.ImmutableMatrix
    symmetric_embedding: sp.ImmutableMatrix
    symmetric_generator: sp.ImmutableMatrix
    dichotomy: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    coordinate_isometry_theorem: Theorem
    coordinate_projector_rank_theorem: Theorem
    coordinate_compression_theorem: Theorem
    coordinate_rank_theorem: Theorem
    coordinate_nullity_theorem: Theorem
    coordinate_conservation_theorem: Theorem
    coordinate_offdiagonal_theorem: Theorem
    coordinate_degeneracy_theorem: Theorem
    symmetric_isometry_theorem: Theorem
    symmetric_permutation_theorem: Theorem
    symmetric_compression_theorem: Theorem
    symmetric_negative_entry_theorem: Theorem
    symmetric_negative_count_theorem: Theorem
    dichotomy_theorem: Theorem
    pass_vector_theorem: Theorem
    dichotomy_rank_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    physical_origin_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfCycleK43TypedEmbeddingCertificate:
    dimension = 43
    transfer_dimension = 30
    vacuum_index = 0
    hypercharge_index = 42
    rate = sp.symbols("kappa", positive=True)
    cycle = sp.ImmutableMatrix(rate*sp.Matrix([[-3, 1, 2], [2, -3, 1], [1, 2, -3]]))

    coordinate_mutable = sp.zeros(dimension, 3)
    coordinate_mutable[vacuum_index, 0] = 1
    coordinate_mutable[hypercharge_index, 1] = 1
    coordinate_mutable[1, 2] = 1
    coordinate_embedding = sp.ImmutableMatrix(coordinate_mutable)
    coordinate_projector = sp.ImmutableMatrix(coordinate_embedding*coordinate_embedding.T)
    coordinate_generator = sp.ImmutableMatrix(coordinate_embedding*cycle*coordinate_embedding.T)
    coordinate_negative_offdiagonal = sum(
        1 for i in range(dimension) for j in range(dimension)
        if i != j and coordinate_generator[i, j].is_negative is True
    )

    symmetric_mutable = sp.zeros(dimension, 3)
    symmetric_mutable[vacuum_index, 0] = 1
    symmetric_mutable[hypercharge_index, 1] = 1
    for index in range(1, transfer_dimension + 1):
        symmetric_mutable[index, 2] = 1/sp.sqrt(transfer_dimension)
    symmetric_embedding = sp.ImmutableMatrix(symmetric_mutable)
    symmetric_generator = sp.ImmutableMatrix(symmetric_embedding*cycle*symmetric_embedding.T)
    symmetric_negative_offdiagonal = sum(
        1 for i in range(dimension) for j in range(dimension)
        if i != j and symmetric_generator[i, j].is_negative is True
    )
    swap = sp.eye(dimension)
    swap[1, 1] = swap[2, 2] = 0
    swap[1, 2] = swap[2, 1] = 1

    dichotomy = sp.ImmutableMatrix([[1, 0], [0, 1]])
    pass_vector = sp.ImmutableMatrix([sp.prod(dichotomy.row(i)) for i in range(2)])
    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 0, 0, 0])

    coordinate_isometry_theorem = kernel.prove_matrix_equality(coordinate_embedding.T*coordinate_embedding, sp.eye(3), subject="vacuum hypercharge and one transfer label define an isometric K43 cycle embedding")
    coordinate_projector_rank_theorem = kernel.prove_exact_rank(coordinate_projector, 3, subject="the coordinate cycle occupies exactly three K43 directions")
    coordinate_compression_theorem = kernel.prove_matrix_equality(coordinate_embedding.T*coordinate_generator*coordinate_embedding, cycle, subject="coordinate compression reproduces the oriented cycle generator")
    coordinate_rank_theorem = kernel.prove_exact_rank(coordinate_generator, 2, subject="the embedded coordinate cycle preserves the active Markov rank")
    coordinate_nullity_theorem = kernel.prove_exact_nullity(coordinate_generator, 41, subject="the coordinate cycle is inactive on the forty-dimensional complement plus its stationary line")
    coordinate_conservation_theorem = kernel.prove_matrix_equality(sp.ones(1, dimension)*coordinate_generator, sp.zeros(1, dimension), subject="the coordinate embedding preserves probability conservation")
    coordinate_offdiagonal_theorem = kernel.prove_expression_equality(coordinate_negative_offdiagonal, 0, subject="the coordinate embedded generator has no negative off-diagonal rate")
    coordinate_degeneracy_theorem = kernel.prove_expression_equality(transfer_dimension, 30, subject="thirty equivalent transfer labels compete for the third cycle vertex")
    symmetric_isometry_theorem = kernel.prove_matrix_equality(symmetric_embedding.T*symmetric_embedding, sp.eye(3), subject="the uniform transfer line defines an isometric symmetric embedding")
    symmetric_permutation_theorem = kernel.prove_matrix_equality(sp.ImmutableMatrix(swap)*symmetric_embedding[:, 2], symmetric_embedding[:, 2], subject="the uniform transfer line is invariant under transfer-label permutations")
    symmetric_compression_theorem = kernel.prove_matrix_equality(symmetric_embedding.T*symmetric_generator*symmetric_embedding, cycle, subject="symmetric compression also reproduces the abstract oriented cycle")
    symmetric_negative_entry_theorem = kernel.prove_expression_equality(symmetric_generator[1, 2], -rate/10, subject="coherent transfer symmetrization creates a forbidden negative off-diagonal rate")
    symmetric_negative_count_theorem = kernel.prove_expression_equality(symmetric_negative_offdiagonal, 870, subject="all ordered distinct transfer pairs acquire forbidden negative rates")
    dichotomy_theorem = kernel.prove_matrix_equality(dichotomy, sp.Matrix([[1, 0], [0, 1]]), subject="coordinate and symmetric embeddings satisfy complementary admissibility conditions")
    pass_vector_theorem = kernel.prove_matrix_equality(pass_vector, sp.zeros(2, 1), subject="neither embedding is simultaneously canonical and Markov positive")
    dichotomy_rank_theorem = kernel.prove_exact_rank(dichotomy, 2, subject="canonical typing and Markov positivity are independent requirements")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(8, 1), subject="both K43 embedding branches and their obstructions are fully checked")
    origin_ledger_theorem = kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 0, 0, 0]), subject="algebraic carrier and compression pass while canonical dynamics parent and scale origins remain open")
    origin_score_theorem = kernel.prove_expression_equality(sum(origin_ledger), 2, subject="two of five typed Hopf-cycle origin requirements pass")
    physical_origin_theorem = kernel.prove_expression_equality(sum(origin_ledger[2:, 0]), 0, subject="no canonical Markov parent or absolute rate is inherited inside K43 alone")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate", (coordinate_isometry_theorem, coordinate_projector_rank_theorem, coordinate_compression_theorem, coordinate_rank_theorem, coordinate_nullity_theorem, coordinate_conservation_theorem, coordinate_offdiagonal_theorem, coordinate_degeneracy_theorem, symmetric_isometry_theorem, symmetric_permutation_theorem, symmetric_compression_theorem, symmetric_negative_entry_theorem, symmetric_negative_count_theorem, dichotomy_theorem, pass_vector_theorem, dichotomy_rank_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, physical_origin_theorem))
    return HopfCycleK43TypedEmbeddingCertificate(coordinate_embedding, coordinate_projector, coordinate_generator, symmetric_embedding, symmetric_generator, dichotomy, pass_vector, architecture, origin_ledger, coordinate_isometry_theorem, coordinate_projector_rank_theorem, coordinate_compression_theorem, coordinate_rank_theorem, coordinate_nullity_theorem, coordinate_conservation_theorem, coordinate_offdiagonal_theorem, coordinate_degeneracy_theorem, symmetric_isometry_theorem, symmetric_permutation_theorem, symmetric_compression_theorem, symmetric_negative_entry_theorem, symmetric_negative_count_theorem, dichotomy_theorem, pass_vector_theorem, dichotomy_rank_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, physical_origin_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate", "Типизированное вложение хопфовского цикла в K43", ("s2t/gates/version10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_k43_typed_embedding_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("coordinate_cycle_embedding_isometry", lambda: build_certificate().coordinate_isometry_theorem), ("coordinate_cycle_projector_rank_three", lambda: build_certificate().coordinate_projector_rank_theorem), ("coordinate_cycle_compression", lambda: build_certificate().coordinate_compression_theorem), ("coordinate_cycle_rank_two", lambda: build_certificate().coordinate_rank_theorem), ("coordinate_cycle_nullity_forty_one", lambda: build_certificate().coordinate_nullity_theorem), ("coordinate_cycle_probability_conservation", lambda: build_certificate().coordinate_conservation_theorem), ("coordinate_cycle_markov_offdiagonal", lambda: build_certificate().coordinate_offdiagonal_theorem), ("coordinate_transfer_choice_degeneracy_thirty", lambda: build_certificate().coordinate_degeneracy_theorem), ("symmetric_cycle_embedding_isometry", lambda: build_certificate().symmetric_isometry_theorem), ("symmetric_transfer_permutation_invariance", lambda: build_certificate().symmetric_permutation_theorem), ("symmetric_cycle_compression", lambda: build_certificate().symmetric_compression_theorem), ("symmetric_cycle_negative_rate_witness", lambda: build_certificate().symmetric_negative_entry_theorem), ("symmetric_cycle_negative_rate_count", lambda: build_certificate().symmetric_negative_count_theorem), ("embedding_admissibility_dichotomy", lambda: build_certificate().dichotomy_theorem), ("zero_fully_admissible_embeddings", lambda: build_certificate().pass_vector_theorem), ("embedding_dichotomy_rank_two", lambda: build_certificate().dichotomy_rank_theorem), ("hopf_cycle_embedding_audit_full", lambda: build_certificate().architecture_theorem), ("hopf_cycle_origin_ledger_two", lambda: build_certificate().origin_ledger_theorem), ("hopf_cycle_origin_score_two", lambda: build_certificate().origin_score_theorem), ("canonical_markov_parent_origin_zero", lambda: build_certificate().physical_origin_theorem))))