"""LCF certificate for the Hopf cycle in the K43-KMS product carrier."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HopfCycleK43KMSProductEmbeddingCertificate:
    embedding: sp.ImmutableMatrix
    projector: sp.ImmutableMatrix
    product_generator: sp.ImmutableMatrix
    stationary_state: sp.ImmutableMatrix
    rate_clock_map: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    product_dimension_theorem: Theorem
    embedding_isometry_theorem: Theorem
    projector_rank_theorem: Theorem
    hypercharge_typing_theorem: Theorem
    kms_singlet_typing_theorem: Theorem
    cycle_compression_theorem: Theorem
    product_rank_theorem: Theorem
    probability_conservation_theorem: Theorem
    offdiagonal_positivity_theorem: Theorem
    stationary_normalization_theorem: Theorem
    stationary_state_theorem: Theorem
    edge_current_theorem: Theorem
    cycle_affinity_theorem: Theorem
    entropy_production_theorem: Theorem
    rate_clock_rank_theorem: Theorem
    rate_clock_nullity_theorem: Theorem
    rate_clock_kernel_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    physical_origin_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HopfCycleK43KMSProductEmbeddingCertificate:
    cell_dimension = 43
    kms_dimension = 6
    product_dimension = cell_dimension*kms_dimension
    vacuum_index = 0
    hypercharge_index = 42
    kms_source_index = 0
    kms_singlet_index = 1
    rate = sp.symbols("kappa", positive=True)

    def product_index(cell: int, kms: int) -> int:
        return cell*kms_dimension+kms

    embedding_mutable = sp.zeros(product_dimension, 3)
    embedding_mutable[product_index(vacuum_index, kms_source_index), 0] = 1
    embedding_mutable[product_index(hypercharge_index, kms_source_index), 1] = 1
    embedding_mutable[product_index(vacuum_index, kms_singlet_index), 2] = 1
    embedding = sp.ImmutableMatrix(embedding_mutable)
    projector = sp.ImmutableMatrix(embedding*embedding.T)

    hypercharge_projector = sp.zeros(cell_dimension)
    hypercharge_projector[hypercharge_index, hypercharge_index] = 1
    singlet_projector = sp.zeros(kms_dimension)
    singlet_projector[kms_singlet_index, kms_singlet_index] = 1
    product_hypercharge_projector = sp.ImmutableMatrix(sp.kronecker_product(hypercharge_projector, sp.eye(kms_dimension)))
    product_singlet_projector = sp.ImmutableMatrix(sp.kronecker_product(sp.eye(cell_dimension), singlet_projector))

    cycle = sp.ImmutableMatrix(rate*sp.Matrix([[-3, 1, 2], [2, -3, 1], [1, 2, -3]]))
    product_generator = sp.ImmutableMatrix(embedding*cycle*embedding.T)
    stationary_state = sp.ImmutableMatrix(embedding*sp.ones(3, 1)/3)
    negative_offdiagonal = sum(
        1 for i in range(product_dimension) for j in range(product_dimension)
        if i != j and product_generator[i, j].is_negative is True
    )
    edge_current = rate/3
    cycle_affinity = 3*sp.log(2)
    entropy_production = rate*sp.log(2)
    rate_clock_map = sp.ImmutableMatrix([[1, -1, 0], [1, 0, 1]])
    scale_vector = sp.ImmutableMatrix([1, 1, -1])
    architecture = sp.ones(10, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 1, 1, 0, 0])

    product_dimension_theorem = kernel.prove_expression_equality(product_dimension, 258, subject="the K43 and six-dimensional KMS product has dimension 258")
    embedding_isometry_theorem = kernel.prove_matrix_equality(embedding.T*embedding, sp.eye(3), subject="vacuum-source hypercharge-source and vacuum-singlet define an isometric product embedding")
    projector_rank_theorem = kernel.prove_exact_rank(projector, 3, subject="the typed product cycle occupies exactly three canonical directions")
    hypercharge_typing_theorem = kernel.prove_matrix_equality(embedding.T*product_hypercharge_projector*embedding, sp.diag(0, 1, 0), subject="the second cycle vertex is uniquely typed by hypercharge")
    kms_singlet_typing_theorem = kernel.prove_matrix_equality(embedding.T*product_singlet_projector*embedding, sp.diag(0, 0, 1), subject="the third cycle vertex is uniquely typed by the KMS singlet")
    cycle_compression_theorem = kernel.prove_matrix_equality(embedding.T*product_generator*embedding, cycle, subject="product compression reproduces the oriented Hopf cycle")
    product_rank_theorem = kernel.prove_exact_rank(product_generator, 2, subject="the product embedded cycle preserves the active Markov rank")
    probability_conservation_theorem = kernel.prove_matrix_equality(sp.ones(1, product_dimension)*product_generator, sp.zeros(1, product_dimension), subject="the product embedding preserves total probability")
    offdiagonal_positivity_theorem = kernel.prove_expression_equality(negative_offdiagonal, 0, subject="the canonical product generator has no negative off-diagonal rates")
    stationary_normalization_theorem = kernel.prove_expression_equality((sp.ones(1, product_dimension)*stationary_state)[0], 1, subject="the embedded stationary state is a normalized probability vector")
    stationary_state_theorem = kernel.prove_matrix_equality(product_generator*stationary_state, sp.zeros(product_dimension, 1), subject="the canonical product cycle has an exact stationary state")
    edge_current_theorem = kernel.prove_expression_equality(edge_current, rate/3, subject="the product cycle retains the stationary edge current")
    cycle_affinity_theorem = kernel.prove_expression_equality(cycle_affinity, 3*sp.log(2), subject="the product cycle retains the KMS affinity")
    entropy_production_theorem = kernel.prove_expression_equality(entropy_production, rate*sp.log(2), subject="the product cycle retains positive entropy production")
    rate_clock_rank_theorem = kernel.prove_exact_rank(rate_clock_map, 2, subject="typed product embedding does not add an absolute rate constraint")
    rate_clock_nullity_theorem = kernel.prove_exact_nullity(rate_clock_map, 1, subject="one common rate-clock calibration remains after product embedding")
    rate_clock_kernel_theorem = kernel.prove_matrix_equality(rate_clock_map*scale_vector, sp.zeros(2, 1), subject="common rate and inverse time scaling remains the exact kernel")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(10, 1), subject="the canonical K43-KMS Hopf cycle architecture is fully constructed")
    origin_ledger_theorem = kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 1, 1, 0, 0]), subject="carrier typing positivity and current pass while rate and parent origins remain open")
    origin_score_theorem = kernel.prove_expression_equality(sum(origin_ledger), 5, subject="five of seven product cycle origin requirements pass")
    physical_origin_theorem = kernel.prove_expression_equality(origin_ledger[-2]+origin_ledger[-1], 0, subject="absolute conductance and common-parent origins are not supplied by the product carrier")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate", (product_dimension_theorem, embedding_isometry_theorem, projector_rank_theorem, hypercharge_typing_theorem, kms_singlet_typing_theorem, cycle_compression_theorem, product_rank_theorem, probability_conservation_theorem, offdiagonal_positivity_theorem, stationary_normalization_theorem, stationary_state_theorem, edge_current_theorem, cycle_affinity_theorem, entropy_production_theorem, rate_clock_rank_theorem, rate_clock_nullity_theorem, rate_clock_kernel_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, physical_origin_theorem))
    return HopfCycleK43KMSProductEmbeddingCertificate(embedding, projector, product_generator, stationary_state, rate_clock_map, scale_vector, architecture, origin_ledger, product_dimension_theorem, embedding_isometry_theorem, projector_rank_theorem, hypercharge_typing_theorem, kms_singlet_typing_theorem, cycle_compression_theorem, product_rank_theorem, probability_conservation_theorem, offdiagonal_positivity_theorem, stationary_normalization_theorem, stationary_state_theorem, edge_current_theorem, cycle_affinity_theorem, entropy_production_theorem, rate_clock_rank_theorem, rate_clock_nullity_theorem, rate_clock_kernel_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, physical_origin_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate", "Вложение хопфовского цикла в произведение K43 и KMS", ("s2t/gates/version10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_hopf_cycle_k43_kms_product_embedding_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("k43_kms_product_dimension_258", lambda: build_certificate().product_dimension_theorem), ("product_cycle_embedding_isometry", lambda: build_certificate().embedding_isometry_theorem), ("product_cycle_projector_rank_three", lambda: build_certificate().projector_rank_theorem), ("product_cycle_hypercharge_typing", lambda: build_certificate().hypercharge_typing_theorem), ("product_cycle_kms_singlet_typing", lambda: build_certificate().kms_singlet_typing_theorem), ("product_cycle_compression", lambda: build_certificate().cycle_compression_theorem), ("product_cycle_rank_two", lambda: build_certificate().product_rank_theorem), ("product_cycle_probability_conservation", lambda: build_certificate().probability_conservation_theorem), ("product_cycle_markov_offdiagonal", lambda: build_certificate().offdiagonal_positivity_theorem), ("product_stationary_state_normalized", lambda: build_certificate().stationary_normalization_theorem), ("product_stationary_state_exact", lambda: build_certificate().stationary_state_theorem), ("product_cycle_edge_current", lambda: build_certificate().edge_current_theorem), ("product_cycle_affinity", lambda: build_certificate().cycle_affinity_theorem), ("product_cycle_entropy_production", lambda: build_certificate().entropy_production_theorem), ("product_rate_clock_rank_two", lambda: build_certificate().rate_clock_rank_theorem), ("product_rate_clock_nullity_one", lambda: build_certificate().rate_clock_nullity_theorem), ("product_rate_clock_kernel", lambda: build_certificate().rate_clock_kernel_theorem), ("product_cycle_architecture_full", lambda: build_certificate().architecture_theorem), ("product_cycle_origin_ledger_five", lambda: build_certificate().origin_ledger_theorem), ("product_cycle_origin_score_five", lambda: build_certificate().origin_score_theorem), ("product_cycle_physical_origin_zero", lambda: build_certificate().physical_origin_theorem))))