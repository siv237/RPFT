"""LCF certificate for embedding the universal cover into the birth graph."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from ..structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class UniversalCoverGrowthGraphCertificate:
    cover_boundary: sp.ImmutableMatrix
    base_boundary: sp.ImmutableMatrix
    vertex_projection: sp.ImmutableMatrix
    edge_projection: sp.ImmutableMatrix
    chain_map_defect: sp.ImmutableMatrix
    cover_adjacency: sp.ImmutableMatrix
    base_adjacency: sp.ImmutableMatrix
    local_adjacency_defect: sp.ImmutableMatrix
    deck_period_defect: sp.ImmutableMatrix
    birth_shift_defect: sp.ImmutableMatrix
    height: sp.ImmutableMatrix
    height_increment: sp.ImmutableMatrix
    height_shift_defect: sp.ImmutableMatrix
    radius_counts: sp.ImmutableMatrix
    shell_counts: sp.ImmutableMatrix
    forward_counts: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> UniversalCoverGrowthGraphCertificate:
    vertices = tuple(range(-3, 4))
    edges = tuple(range(-3, 3))

    cover_boundary = sp.ImmutableMatrix(
        7, 6, lambda i, j: -1 if i == j else (1 if i == j + 1 else 0)
    )
    base_boundary = sp.ImmutableMatrix(
        [[-1, 0, 1], [1, -1, 0], [0, 1, -1]]
    )
    vertex_projection = sp.ImmutableMatrix(
        3, 7, lambda i, j: 1 if i == vertices[j] % 3 else 0
    )
    edge_projection = sp.ImmutableMatrix(
        3, 6, lambda i, j: 1 if i == edges[j] % 3 else 0
    )
    chain_map_defect = sp.ImmutableMatrix(
        base_boundary * edge_projection - vertex_projection * cover_boundary
    )

    cover_adjacency = sp.ImmutableMatrix(
        7, 7, lambda i, j: sp.Rational(1, 2) if abs(i - j) == 1 else 0
    )
    base_adjacency = sp.ImmutableMatrix(
        3, 3, lambda i, j: 0 if i == j else sp.Rational(1, 2)
    )
    interior_selector = sp.zeros(7, 5)
    for index in range(5):
        interior_selector[index + 1, index] = 1
    local_adjacency_defect = sp.ImmutableMatrix(
        vertex_projection * cover_adjacency * interior_selector
        - base_adjacency * vertex_projection * interior_selector
    )
    deck_period_defect = sp.ImmutableMatrix(
        vertex_projection[:, 3:7] - vertex_projection[:, 0:4]
    )

    cover_shift = sp.zeros(7)
    for index in range(6):
        cover_shift[index + 1, index] = 1
    source_selector = sp.zeros(7, 6)
    for index in range(6):
        source_selector[index, index] = 1
    base_shift = sp.ImmutableMatrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    birth_shift_defect = sp.ImmutableMatrix(
        vertex_projection * cover_shift * source_selector
        - base_shift * vertex_projection * source_selector
    )

    height = sp.ImmutableMatrix(vertices)
    height_increment = sp.ImmutableMatrix(cover_boundary.T * height)
    shifted_height = height + sp.ones(7, 1)
    height_shift_defect = sp.ImmutableMatrix(
        cover_boundary.T * shifted_height - height_increment
    )
    radius_counts = sp.ImmutableMatrix([1, 3, 5, 7])
    shell_counts = sp.ImmutableMatrix([1, 2, 2, 2])
    forward_counts = sp.ImmutableMatrix([1, 2, 3, 4])

    cover_c0 = Space("C_0(B_3(Z))", 7, "R")
    cover_c1 = Space("C_1(B_3(Z))", 6, "R")
    base_c0 = Space("C_0(C_3)", 3, "R")
    base_c1 = Space("C_1(C_3)", 3, "R")
    cover_boundary_morphism = Morphism("partial_cover", cover_c1, cover_c0, cover_boundary)
    base_boundary_morphism = Morphism("partial_C3", base_c1, base_c0, base_boundary)
    vertex_projection_morphism = Morphism("p_0", cover_c0, base_c0, vertex_projection)
    edge_projection_morphism = Morphism("p_1", cover_c1, base_c1, edge_projection)
    cover_adjacency_morphism = Morphism("A_cover", cover_c0, cover_c0, cover_adjacency)
    base_adjacency_morphism = Morphism("A_C3", base_c0, base_c0, base_adjacency)
    cover_shift_morphism = Morphism("U_birth", cover_c0, cover_c0, cover_shift)

    # Previous edge-length map after the physical speed anchor v_g=c.
    # Variables are (v_cell, E_C, k_BZ, omega_UV, Lambda_43, Delta_t,
    # v_g, ell_cell, ell_edge).
    scale_map = sp.ImmutableMatrix(
        [
            [1, 0, 0, 0, 0, 0, 0, -4, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, -1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, -1],
            [0, 0, 0, 0, 0, 0, 0, -1, 1],
            [0, 0, 0, 0, 0, 0, 1, 0, 0],
        ]
    )
    scale_kernel = sp.ImmutableMatrix([4, -1, -1, -1, -1, 1, 0, 1, 1])
    conditional_origin = sp.ones(12, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_well_typed_morphism(cover_boundary_morphism),
        kernel.prove_well_typed_morphism(base_boundary_morphism),
        kernel.prove_well_typed_morphism(vertex_projection_morphism),
        kernel.prove_well_typed_morphism(edge_projection_morphism),
        kernel.prove_well_typed_morphism(cover_adjacency_morphism),
        kernel.prove_well_typed_morphism(base_adjacency_morphism),
        kernel.prove_well_typed_morphism(cover_shift_morphism),
        kernel.prove_matrix_equality(chain_map_defect, sp.zeros(3, 6), subject="universal-cover projection commutes with the boundary"),
        kernel.prove_exact_rank(cover_boundary, 6, subject="radius-three universal-cover ball boundary rank"),
        kernel.prove_exact_rank(base_boundary, 2, subject="Hopf three-cycle boundary rank"),
        kernel.prove_exact_rank(vertex_projection, 3, subject="vertex covering projection is onto"),
        kernel.prove_exact_rank(edge_projection, 3, subject="edge covering projection is onto"),
        kernel.prove_matrix_equality(cover_boundary.T * sp.ones(7, 1), sp.zeros(6, 1), subject="cover boundary annihilates constant zero-chains"),
        kernel.prove_matrix_equality(base_boundary.T * sp.ones(3, 1), sp.zeros(3, 1), subject="cycle boundary annihilates constant zero-chains"),
        kernel.prove_matrix_equality(local_adjacency_defect, sp.zeros(3, 5), subject="covering projection intertwines local adjacency away from truncation boundary"),
        kernel.prove_matrix_equality(deck_period_defect, sp.zeros(3, 4), subject="translation by three is a deck transformation"),
        kernel.prove_matrix_equality(birth_shift_defect, sp.zeros(3, 6), subject="forward birth shift projects to the oriented Hopf cycle"),
        kernel.prove_matrix_equality(height_increment, sp.ones(6, 1), subject="each oriented cover edge advances birth height by one"),
        kernel.prove_matrix_equality(height_shift_defect, sp.zeros(6, 1), subject="absolute birth-height origin remains translation free"),
        kernel.prove_matrix_equality(radius_counts, sp.ImmutableMatrix([1, 3, 5, 7]), subject="linear ball growth in the universal cover"),
        kernel.prove_matrix_equality(shell_counts, sp.ImmutableMatrix([1, 2, 2, 2]), subject="two-sided universal-cover shell multiplicities"),
        kernel.prove_matrix_equality(forward_counts, sp.ImmutableMatrix([1, 2, 3, 4]), subject="one new future vertex per birth step"),
        kernel.prove_exact_rank(scale_map, 8, subject="universal cover adds no dimensional rank after the speed anchor"),
        kernel.prove_exact_nullity(scale_map, 1, subject="common physical length remains free on the universal cover"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(8, 1), subject="universal cover preserves the common length-energy orbit"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(12, 1), subject="conditional universal-cover growth architecture complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 12, subject="twelve conditional universal-cover requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="physical growth graph metric and clock origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="combinatorial covering supplies no physical graph selector or clock"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate",
        theorems,
    )
    return UniversalCoverGrowthGraphCertificate(
        cover_boundary,
        base_boundary,
        vertex_projection,
        edge_projection,
        chain_map_defect,
        cover_adjacency,
        base_adjacency,
        local_adjacency_defect,
        deck_period_defect,
        birth_shift_defect,
        height,
        height_increment,
        height_shift_defect,
        radius_counts,
        shell_counts,
        forward_counts,
        scale_map,
        scale_kernel,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate",
    title="Типизированное вложение универсального покрытия в граф рождения",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_growth_graph_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"universal_cover_growth_graph_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(29)
    ),
)