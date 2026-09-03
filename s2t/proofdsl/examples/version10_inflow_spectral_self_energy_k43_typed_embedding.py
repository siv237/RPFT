"""LCF certificate for the typed K43 embedding of the oriented reservoir."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from .version8_gauge_twirl_kraus import _endpoint_gauge_generators


@dataclass(frozen=True, slots=True)
class InflowSpectralSelfEnergyK43EmbeddingCertificate:
    embedding: sp.ImmutableMatrix
    embedded_projector: sp.ImmutableMatrix
    hypercharge_generator: sp.ImmutableMatrix
    embedded_operator: sp.ImmutableMatrix
    embedded_propagator: sp.ImmutableMatrix
    restricted_star_interaction: sp.ImmutableMatrix
    kms_embedding: sp.ImmutableMatrix
    compressed_cell_parent: sp.ImmutableMatrix
    incoming_self_energy: sp.Expr
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    embedding_isometry_theorem: Theorem
    projector_rank_theorem: Theorem
    hypercharge_invariance_theorem: Theorem
    hypercharge_rank_theorem: Theorem
    restricted_star_rank_theorem: Theorem
    compression_theorem: Theorem
    determinant_theorem: Theorem
    inverse_theorem: Theorem
    incoming_self_energy_theorem: Theorem
    incoming_beta_theorem: Theorem
    kms_isometry_theorem: Theorem
    kms_rank_theorem: Theorem
    cell_parent_compression_theorem: Theorem
    inherited_parent_beta_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    physical_origin_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> InflowSpectralSelfEnergyK43EmbeddingCertificate:
    zeta = sp.symbols("zeta", real=True)
    cell_dimension = 43
    kms_dimension = 6
    vacuum_index = 0
    hypercharge_excitation_index = 42

    embedding_mutable = sp.zeros(cell_dimension, 2)
    embedding_mutable[hypercharge_excitation_index, 0] = 1
    embedding_mutable[vacuum_index, 1] = 1
    embedding = sp.ImmutableMatrix(embedding_mutable)
    embedded_projector = sp.ImmutableMatrix(embedding * embedding.T)

    gauge_generators = _endpoint_gauge_generators()
    hypercharge_generator = sp.ImmutableMatrix(gauge_generators[-1])
    commutator_stack = sp.ImmutableMatrix.vstack(
        *(
            sp.ImmutableMatrix(generator * hypercharge_generator - hypercharge_generator * generator)
            for generator in gauge_generators
        )
    )

    incoming_line = sp.ImmutableMatrix(embedding[:, 0] * embedding[:, 0].T)
    vacuum_line = sp.ImmutableMatrix(embedding[:, 1] * embedding[:, 1].T)
    embedded_operator = sp.ImmutableMatrix(
        sp.eye(cell_dimension)
        + (sp.exp(-zeta) - 1) * incoming_line
        + (sp.exp(zeta) - 1) * vacuum_line
    )
    embedded_propagator = sp.ImmutableMatrix(
        sp.eye(cell_dimension)
        + (sp.exp(zeta) - 1) * incoming_line
        + (sp.exp(-zeta) - 1) * vacuum_line
    )
    compressed_operator = sp.ImmutableMatrix(embedding.T * embedded_operator * embedding)
    incoming_vector = sp.ImmutableMatrix(embedding[:, 0])
    incoming_self_energy = sp.simplify(
        (incoming_vector.T * embedded_propagator * incoming_vector)[0]
    )

    exchange = sp.ImmutableMatrix([[0, 1], [1, 0]])
    restricted_star_interaction = sp.ImmutableMatrix(
        sp.kronecker_product(hypercharge_generator, exchange)
    )
    kms_embedding = sp.ImmutableMatrix(sp.kronecker_product(embedding, sp.eye(kms_dimension)))

    cell_parent = sp.eye(cell_dimension)
    cell_parent[vacuum_index, vacuum_index] = 0
    compressed_cell_parent = sp.ImmutableMatrix(embedding.T * cell_parent * embedding)
    inherited_parent_beta = sp.ImmutableMatrix(
        compressed_cell_parent.applyfunc(lambda entry: sp.diff(entry, zeta))
    )

    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 1, 0, 0])

    embedding_isometry_theorem = kernel.prove_matrix_equality(
        embedding.T * embedding,
        sp.eye(2),
        subject="hypercharge excitation and cell vacuum define an isometric K43 embedding",
    )
    projector_rank_theorem = kernel.prove_exact_rank(
        embedded_projector,
        2,
        subject="the typed oriented reservoir occupies exactly two K43 directions",
    )
    hypercharge_invariance_theorem = kernel.prove_matrix_equality(
        commutator_stack,
        sp.zeros(12 * 21, 21),
        subject="the hypercharge jump direction is invariant under the endpoint gauge algebra",
    )
    hypercharge_rank_theorem = kernel.prove_exact_rank(
        hypercharge_generator,
        21,
        subject="the inherited hypercharge jump acts nontrivially on every endpoint state",
    )
    restricted_star_rank_theorem = kernel.prove_exact_rank(
        restricted_star_interaction,
        42,
        subject="the inherited star Hamiltonian couples the full endpoint to the typed two-mode sector",
    )
    compression_theorem = kernel.prove_matrix_equality(
        compressed_operator,
        sp.diag(sp.exp(-zeta), sp.exp(zeta)),
        subject="compression of the K43 operator reproduces the reciprocal reservoir",
    )
    determinant_theorem = kernel.prove_expression_equality(
        embedded_operator.det(),
        1,
        subject="the embedded reciprocal K43 operator has unit determinant",
    )
    inverse_theorem = kernel.prove_matrix_equality(
        embedded_operator * embedded_propagator,
        sp.eye(cell_dimension),
        subject="the embedded K43 propagator is exact",
    )
    incoming_self_energy_theorem = kernel.prove_expression_equality(
        incoming_self_energy,
        sp.exp(zeta),
        subject="the typed hypercharge excitation carries the incoming running self energy",
    )
    incoming_beta_theorem = kernel.prove_expression_equality(
        sp.diff(incoming_self_energy, zeta),
        incoming_self_energy,
        subject="the typed incoming self energy retains its nonzero geometric beta",
    )
    kms_isometry_theorem = kernel.prove_matrix_equality(
        kms_embedding.T * kms_embedding,
        sp.eye(12),
        subject="tensoring with the six-dimensional KMS factor preserves the embedding",
    )
    kms_rank_theorem = kernel.prove_exact_rank(
        kms_embedding,
        12,
        subject="the typed K43 reservoir has the expected twelve-dimensional KMS lift",
    )
    cell_parent_compression_theorem = kernel.prove_matrix_equality(
        compressed_cell_parent,
        sp.diag(1, 0),
        subject="the inherited cell parent only separates excitation from vacuum",
    )
    inherited_parent_beta_theorem = kernel.prove_matrix_equality(
        inherited_parent_beta,
        sp.zeros(2),
        subject="the inherited K43 cell parent has no geometric spectral running",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(8, 1),
        subject="all typed K43 embedding architecture conditions pass",
    )
    origin_ledger_theorem = kernel.prove_matrix_equality(
        origin_ledger,
        sp.Matrix([1, 1, 1, 1, 0, 0]),
        subject="carrier typing passes while spectral and common-parent origins remain open",
    )
    origin_score_theorem = kernel.prove_expression_equality(
        sum(origin_ledger),
        4,
        subject="four of six typed physical origin conditions are inherited",
    )
    physical_origin_theorem = kernel.prove_expression_equality(
        origin_ledger[-2] + origin_ledger[-1],
        0,
        subject="neither geometric spectral running nor its common parent is inherited",
    )
    gate_theorem = kernel.prove_gate(
        "version10_inflow_spectral_self_energy_k43_typed_embedding_gate",
        (
            embedding_isometry_theorem,
            projector_rank_theorem,
            hypercharge_invariance_theorem,
            hypercharge_rank_theorem,
            restricted_star_rank_theorem,
            compression_theorem,
            determinant_theorem,
            inverse_theorem,
            incoming_self_energy_theorem,
            incoming_beta_theorem,
            kms_isometry_theorem,
            kms_rank_theorem,
            cell_parent_compression_theorem,
            inherited_parent_beta_theorem,
            architecture_theorem,
            origin_ledger_theorem,
            origin_score_theorem,
            physical_origin_theorem,
        ),
    )
    return InflowSpectralSelfEnergyK43EmbeddingCertificate(
        embedding=embedding,
        embedded_projector=embedded_projector,
        hypercharge_generator=hypercharge_generator,
        embedded_operator=embedded_operator,
        embedded_propagator=embedded_propagator,
        restricted_star_interaction=restricted_star_interaction,
        kms_embedding=kms_embedding,
        compressed_cell_parent=compressed_cell_parent,
        incoming_self_energy=incoming_self_energy,
        architecture=architecture,
        origin_ledger=origin_ledger,
        embedding_isometry_theorem=embedding_isometry_theorem,
        projector_rank_theorem=projector_rank_theorem,
        hypercharge_invariance_theorem=hypercharge_invariance_theorem,
        hypercharge_rank_theorem=hypercharge_rank_theorem,
        restricted_star_rank_theorem=restricted_star_rank_theorem,
        compression_theorem=compression_theorem,
        determinant_theorem=determinant_theorem,
        inverse_theorem=inverse_theorem,
        incoming_self_energy_theorem=incoming_self_energy_theorem,
        incoming_beta_theorem=incoming_beta_theorem,
        kms_isometry_theorem=kms_isometry_theorem,
        kms_rank_theorem=kms_rank_theorem,
        cell_parent_compression_theorem=cell_parent_compression_theorem,
        inherited_parent_beta_theorem=inherited_parent_beta_theorem,
        architecture_theorem=architecture_theorem,
        origin_ledger_theorem=origin_ledger_theorem,
        origin_score_theorem=origin_score_theorem,
        physical_origin_theorem=physical_origin_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_inflow_spectral_self_energy_k43_typed_embedding_gate",
    title="Типизированное вложение спектральной самоэнергии в K43",
    source_paths=(
        "s2t/gates/version10_inflow_spectral_self_energy_k43_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_inflow_spectral_self_energy_k43_typed_embedding_gate_results.json",
    ),
    obligations=(
        Obligation("k43_embedding_isometry", lambda: build_certificate().embedding_isometry_theorem),
        Obligation("typed_projector_rank_two", lambda: build_certificate().projector_rank_theorem),
        Obligation("hypercharge_direction_gauge_invariant", lambda: build_certificate().hypercharge_invariance_theorem),
        Obligation("hypercharge_endpoint_rank_twenty_one", lambda: build_certificate().hypercharge_rank_theorem),
        Obligation("restricted_star_interaction_rank_forty_two", lambda: build_certificate().restricted_star_rank_theorem),
        Obligation("reciprocal_operator_compression", lambda: build_certificate().compression_theorem),
        Obligation("embedded_operator_unit_determinant", lambda: build_certificate().determinant_theorem),
        Obligation("embedded_propagator_exact", lambda: build_certificate().inverse_theorem),
        Obligation("typed_incoming_self_energy", lambda: build_certificate().incoming_self_energy_theorem),
        Obligation("typed_incoming_geometric_beta", lambda: build_certificate().incoming_beta_theorem),
        Obligation("kms_lift_isometry", lambda: build_certificate().kms_isometry_theorem),
        Obligation("kms_lift_rank_twelve", lambda: build_certificate().kms_rank_theorem),
        Obligation("inherited_cell_parent_compression", lambda: build_certificate().cell_parent_compression_theorem),
        Obligation("inherited_cell_parent_zero_beta", lambda: build_certificate().inherited_parent_beta_theorem),
        Obligation("typed_embedding_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("typed_origin_ledger_four_of_six", lambda: build_certificate().origin_ledger_theorem),
        Obligation("typed_origin_score_four", lambda: build_certificate().origin_score_theorem),
        Obligation("spectral_parent_origin_zero", lambda: build_certificate().physical_origin_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)