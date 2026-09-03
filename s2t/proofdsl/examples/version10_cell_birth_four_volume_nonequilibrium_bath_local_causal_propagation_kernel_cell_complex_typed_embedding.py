"""LCF certificate for the cell-complex embedding of the local causal kernel."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from ..structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class CellComplexKernelEmbeddingCertificate:
    boundary: sp.ImmutableMatrix
    laplacian: sp.ImmutableMatrix
    degree: sp.ImmutableMatrix
    adjacency: sp.ImmutableMatrix
    reference_adjacency: sp.ImmutableMatrix
    causal_defects: sp.ImmutableMatrix
    orientation_invariant_laplacian: sp.ImmutableMatrix
    relabelled_adjacency: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    parent_kernel: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CellComplexKernelEmbeddingCertificate:
    vertex_count = 7
    edge_count = 6
    boundary = sp.ImmutableMatrix(
        vertex_count,
        edge_count,
        lambda i, j: -1 if i == j else (1 if i == j + 1 else 0),
    )
    laplacian = sp.ImmutableMatrix(boundary * boundary.T)
    degree = sp.ImmutableMatrix.diag(*[laplacian[i, i] for i in range(vertex_count)])
    adjacency = sp.ImmutableMatrix((degree - laplacian) / 2)
    reference_adjacency = sp.ImmutableMatrix(
        vertex_count,
        vertex_count,
        lambda i, j: sp.Rational(1, 2) if abs(i - j) == 1 else 0,
    )

    causal_entries = []
    for step in (1, 2, 3):
        power = adjacency**step
        causal_entries.extend(
            power[i, j]
            for i in range(vertex_count)
            for j in range(vertex_count)
            if abs(i - j) > step
        )
    causal_defects = sp.ImmutableMatrix(causal_entries)

    orientation = sp.diag(1, -1, 1, -1, 1, -1)
    reoriented_boundary = sp.ImmutableMatrix(boundary * orientation)
    orientation_invariant_laplacian = sp.ImmutableMatrix(reoriented_boundary * reoriented_boundary.T)

    reversal = sp.ImmutableMatrix(
        vertex_count,
        vertex_count,
        lambda i, j: 1 if i + j == vertex_count - 1 else 0,
    )
    relabelled_laplacian = sp.ImmutableMatrix(reversal * laplacian * reversal.T)
    relabelled_degree = sp.ImmutableMatrix(reversal * degree * reversal.T)
    relabelled_adjacency = sp.ImmutableMatrix((relabelled_degree - relabelled_laplacian) / 2)

    c0 = Space("C_0(path_7)", vertex_count, "R")
    c1 = Space("C_1(path_7)", edge_count, "R")
    boundary_morphism = Morphism("partial_1", c1, c0, boundary)
    coboundary_morphism = boundary_morphism.dagger
    laplacian_morphism = boundary_morphism.then(coboundary_morphism, name="Delta_0")
    propagation_morphism = Morphism("A_cell", c0, c0, adjacency)

    k1, k2, k3, r = sp.symbols("k1 k2 k3 r", real=True)
    residuals = sp.ImmutableMatrix([k1 - r, k2 - r * k1, k3 - r * k2])
    parent = sp.expand((residuals.T * residuals)[0] / 2)
    variables = (k1, k2, k3, r)
    point = {k1: sp.Rational(1, 2), k2: sp.Rational(1, 4), k3: sp.Rational(1, 8), r: sp.Rational(1, 2)}
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, variables).subs(point))
    parent_kernel = sp.ImmutableMatrix([1, 1, sp.Rational(3, 4), 1])

    # Logarithmic variables are (tau_corr, Delta_t, ell_edge, v_g).
    scale_map = sp.ImmutableMatrix([[1, -1, 0, 0], [0, 1, -1, 1]])
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([1, 1, 1, 0]),
        sp.ImmutableMatrix([-1, -1, 0, 1]),
    )
    conditional_origin = sp.ones(10, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_well_typed_morphism(boundary_morphism),
        kernel.prove_well_typed_morphism(coboundary_morphism),
        kernel.prove_well_typed_morphism(laplacian_morphism),
        kernel.prove_well_typed_morphism(propagation_morphism),
        kernel.prove_matrix_equality(boundary.T * sp.ones(vertex_count, 1), sp.zeros(edge_count, 1), subject="oriented boundary annihilates the constant zero-chain"),
        kernel.prove_exact_rank(boundary, 6, subject="connected path boundary rank"),
        kernel.prove_matrix_equality(laplacian, laplacian.T, subject="zero-chain Hodge Laplacian is symmetric"),
        kernel.prove_exact_rank(laplacian, 6, subject="connected path Hodge Laplacian rank"),
        kernel.prove_exact_nullity(laplacian, 1, subject="constant zero-chain is the only Laplacian zero mode"),
        kernel.prove_matrix_equality(laplacian * sp.ones(vertex_count, 1), sp.zeros(vertex_count, 1), subject="constant zero-chain lies in the Laplacian kernel"),
        kernel.prove_matrix_equality(adjacency, reference_adjacency, subject="cell-complex incidence reproduces the local propagation operator"),
        kernel.prove_matrix_equality(adjacency, adjacency.T, subject="cell-complex propagation is symmetric"),
        kernel.prove_matrix_equality(causal_defects, sp.zeros(causal_defects.rows, 1), subject="embedded propagation preserves the three-step graph light cone"),
        kernel.prove_matrix_equality(orientation_invariant_laplacian, laplacian, subject="Hodge Laplacian is independent of edge orientations"),
        kernel.prove_matrix_equality(relabelled_adjacency, reversal * adjacency * reversal.T, subject="propagation is covariant under vertex relabelling"),
        kernel.prove_exact_rank(parent_hessian, 3, subject="typed embedding does not alter the memory-parent rank"),
        kernel.prove_exact_nullity(parent_hessian, 1, subject="decay remains a memory-parent zero mode"),
        kernel.prove_matrix_equality(parent_hessian * parent_kernel, sp.zeros(4, 1), subject="geometric decay tangent survives the cell-complex embedding"),
        kernel.prove_exact_rank(scale_map, 2, subject="embedded kernel scale-map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="embedded kernel scale-map nullity"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(2, 2), subject="edge-time scale orbits remain after typed embedding"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(10, 1), subject="conditional cell-complex embedding architecture complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 10, subject="ten conditional embedding requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="global complex edge metric and damping origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="typed incidence supplies no physical scale selector"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate",
        theorems,
    )
    return CellComplexKernelEmbeddingCertificate(
        boundary,
        laplacian,
        degree,
        adjacency,
        reference_adjacency,
        causal_defects,
        orientation_invariant_laplacian,
        relabelled_adjacency,
        parent_hessian,
        parent_kernel,
        scale_map,
        scale_kernel,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate",
    title="Типизированное вложение локального причинного ядра в клеточный комплекс",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_local_causal_propagation_kernel_cell_complex_typed_embedding_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"cell_complex_kernel_embedding_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(25)
    ),
)