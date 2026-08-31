"""Exact cycle-space audit for the heavy-arrow horizontal-phase proposal."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class HorizontalPhaseHeavyArrowCycleAdmissionCertificate:
    boundary_matrix: sp.ImmutableMatrix
    incidence_boundary_matrix: sp.ImmutableMatrix
    cycle_basis: sp.ImmutableMatrix
    heavy_cycle_projection: sp.ImmutableMatrix
    target_phase_weights: sp.ImmutableMatrix
    graph_rank: int
    cycle_rank: int
    incidence_cycle_rank: int
    heavy_cycle_rank: int
    graph_rank_theorem: Theorem
    cycle_rank_theorem: Theorem
    incidence_forest_theorem: Theorem
    cycle_basis_theorem: Theorem
    cycle_basis_rank_theorem: Theorem
    heavy_cycle_rank_theorem: Theorem
    up_edge_leaf_theorem: Theorem
    cycle_phase_charge_theorem: Theorem
    heavy_cycle_phase_no_go_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> HorizontalPhaseHeavyArrowCycleAdmissionCertificate:
    # Vertices: QL, LL, XL, YL | uR, dR, eR, XR, YR.
    # Edges 0..6 are incidence edges; 7..10 are heavy edges.
    edges = (
        (0, 4),  # QL-uR
        (0, 5),  # QL-dR
        (1, 6),  # LL-eR
        (2, 6),  # XL-eR
        (2, 7),  # XL-XR
        (1, 8),  # LL-YR
        (3, 8),  # YL-YR
        (2, 5),  # XL-dR, heavy
        (3, 6),  # YL-eR, heavy
        (1, 7),  # LL-XR, heavy
        (0, 8),  # QL-YR, heavy
    )
    boundary = sp.zeros(9, 11)
    for column, (source, target) in enumerate(edges):
        boundary[source, column] = -1
        boundary[target, column] = 1
    boundary = sp.ImmutableMatrix(boundary)
    incidence_boundary = sp.ImmutableMatrix(boundary[:, :7])

    cycle_basis = sp.ImmutableMatrix(
        [
            [0, 0, 0],
            [0, 0, -1],
            [-1, -1, 1],
            [0, 1, -1],
            [0, -1, 0],
            [1, 0, -1],
            [-1, 0, 0],
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
    )
    heavy_projection = sp.ImmutableMatrix(cycle_basis[7:11, :])
    target_phase_weights = sp.ImmutableMatrix(
        [[4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]
    )

    graph_rank = boundary.rank()
    cycle_rank = 11 - graph_rank
    incidence_cycle_rank = 7 - incidence_boundary.rank()
    heavy_cycle_rank = heavy_projection.rank()

    graph_rank_theorem = kernel.prove_expression_equality(
        graph_rank,
        8,
        subject="rank of the connected nine-vertex full bimodule support graph",
    )
    cycle_rank_theorem = kernel.prove_expression_equality(
        cycle_rank,
        3,
        subject="first Betti number of the eleven-edge full support graph",
    )
    incidence_forest_theorem = kernel.prove_expression_equality(
        incidence_cycle_rank,
        0,
        subject="the seven-edge incidence support is a forest",
    )
    cycle_basis_theorem = kernel.prove_matrix_equality(
        boundary * cycle_basis,
        sp.zeros(9, 3),
        subject="three explicit heavy-arrow circulations are closed graph cycles",
    )
    cycle_basis_rank_theorem = kernel.prove_expression_equality(
        cycle_basis.rank(),
        3,
        subject="the explicit circulations form a basis of the cycle space",
    )
    heavy_cycle_rank_theorem = kernel.prove_expression_equality(
        heavy_cycle_rank,
        3,
        subject="heavy arrows generate every independent cycle direction",
    )
    up_edge_leaf_theorem = kernel.prove_matrix_equality(
        cycle_basis[0, :],
        sp.zeros(1, 3),
        subject="the unique QL-uR edge is absent from every graph cycle",
    )
    cycle_phase_charge_theorem = kernel.prove_matrix_equality(
        target_phase_weights * cycle_basis,
        sp.zeros(1, 3),
        subject="all heavy-arrow cycles have zero horizontal phase charge",
    )
    heavy_cycle_phase_no_go = kernel.prove_gate(
        "heavy_arrow_cycles_cannot_lift_the_horizontal_phase",
        (
            incidence_forest_theorem,
            cycle_basis_theorem,
            cycle_basis_rank_theorem,
            heavy_cycle_rank_theorem,
            up_edge_leaf_theorem,
            cycle_phase_charge_theorem,
        ),
    )
    gate = kernel.prove_gate(
        "horizontal_phase_heavy_arrow_cycle_admission",
        (
            graph_rank_theorem,
            cycle_rank_theorem,
            incidence_forest_theorem,
            cycle_basis_theorem,
            cycle_basis_rank_theorem,
            heavy_cycle_rank_theorem,
            up_edge_leaf_theorem,
            cycle_phase_charge_theorem,
            heavy_cycle_phase_no_go,
        ),
    )
    return HorizontalPhaseHeavyArrowCycleAdmissionCertificate(
        boundary_matrix=boundary,
        incidence_boundary_matrix=incidence_boundary,
        cycle_basis=cycle_basis,
        heavy_cycle_projection=heavy_projection,
        target_phase_weights=target_phase_weights,
        graph_rank=graph_rank,
        cycle_rank=cycle_rank,
        incidence_cycle_rank=incidence_cycle_rank,
        heavy_cycle_rank=heavy_cycle_rank,
        graph_rank_theorem=graph_rank_theorem,
        cycle_rank_theorem=cycle_rank_theorem,
        incidence_forest_theorem=incidence_forest_theorem,
        cycle_basis_theorem=cycle_basis_theorem,
        cycle_basis_rank_theorem=cycle_basis_rank_theorem,
        heavy_cycle_rank_theorem=heavy_cycle_rank_theorem,
        up_edge_leaf_theorem=up_edge_leaf_theorem,
        cycle_phase_charge_theorem=cycle_phase_charge_theorem,
        heavy_cycle_phase_no_go_theorem=heavy_cycle_phase_no_go,
        gate_theorem=gate,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(certificate.cycle_basis)
    print(certificate.target_phase_weights * certificate.cycle_basis)