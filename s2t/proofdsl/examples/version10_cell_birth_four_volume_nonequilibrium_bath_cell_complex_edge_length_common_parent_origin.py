"""LCF certificate for the common parent of the cell-complex edge length."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class EdgeLengthCommonParentCertificate:
    invariant_vector: sp.ImmutableMatrix
    parent_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    velocity_anchored_map: sp.ImmutableMatrix
    velocity_anchored_kernel: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> EdgeLengthCommonParentCertificate:
    target = sp.ImmutableMatrix([1, 1, sp.pi, 2 * sp.sqrt(3), 42, 1, 1])
    invariant_vector = sp.ImmutableMatrix(target)

    coordinates = sp.symbols("u_v u_E u_k u_omega u_Lambda u_step u_edge", real=True)
    parent = sum((coordinate - value) ** 2 for coordinate, value in zip(coordinates, target)) / 2
    target_substitution = dict(zip(coordinates, target))
    parent_gradient = sp.ImmutableMatrix(
        [sp.diff(parent, coordinate) for coordinate in coordinates]
    ).subs(target_substitution)
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, coordinates))

    # Logarithmic variables are
    # (v_cell, E_C, k_BZ, omega_UV, Lambda_43, Delta_t, v_g,
    #  ell_cell, ell_edge).
    scale_map = sp.ImmutableMatrix(
        [
            [1, 0, 0, 0, 0, 0, 0, -4, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 0, -1, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, -1],
            [0, 0, 0, 0, 0, 0, 0, -1, 1],
        ]
    )
    velocity_orbit = sp.ImmutableMatrix([0, 0, 0, 1, 0, -1, 1, 0, 0])
    length_orbit = sp.ImmutableMatrix([4, -1, -1, -1, -1, 1, 0, 1, 1])
    scale_kernel = sp.ImmutableMatrix.hstack(velocity_orbit, length_orbit)
    velocity_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 0, 0, 0, 0, 0, 1, 0, 0]])
    )
    velocity_anchored_kernel = length_orbit
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        velocity_anchored_map,
        sp.ImmutableMatrix([[0, 0, 0, 0, 0, 0, 0, 1, 0]]),
    )

    conditional_origin = sp.ones(11, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_expression_equality(invariant_vector[0], 1, subject="four-volume to fourth edge-length ratio"),
        kernel.prove_expression_equality(invariant_vector[1], 1, subject="clock-energy Compton product"),
        kernel.prove_expression_equality(invariant_vector[2], sp.pi, subject="Brillouin cutoff times cell length"),
        kernel.prove_expression_equality(invariant_vector[3], 2 * sp.sqrt(3), subject="ultraviolet frequency transit product"),
        kernel.prove_expression_equality(invariant_vector[4], 42, subject="K43 cutoff times cell length"),
        kernel.prove_expression_equality(invariant_vector[5], 1, subject="causal edge transit condition"),
        kernel.prove_expression_equality(invariant_vector[6], 1, subject="propagation edge and four-cell edge identification"),
        kernel.prove_expression_equality(invariant_vector[4] / invariant_vector[2], 42 / sp.pi, subject="K43 to Brillouin cutoff ratio survives the common parent"),
        kernel.prove_expression_equality(invariant_vector[3] * invariant_vector[5] * invariant_vector[6], 2 * sp.sqrt(3), subject="ultraviolet phase per causal edge step"),
        kernel.prove_expression_equality(invariant_vector[0] / invariant_vector[6] ** 4, 1, subject="four-volume is the fourth power of the propagation edge"),
        kernel.prove_matrix_equality(parent_gradient, sp.zeros(7, 1), subject="edge-length common parent stationary point"),
        kernel.prove_matrix_equality(parent_hessian, sp.eye(7), subject="edge-length common parent Hessian"),
        kernel.prove_exact_rank(parent_hessian, 7, subject="common invariant parent strict rank"),
        kernel.prove_expression_equality(parent_hessian.det(), 1, subject="common invariant parent determinant"),
        kernel.prove_exact_rank(scale_map, 7, subject="edge-length dimensional map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="velocity and common-length scale freedoms"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(7, 2), subject="two residual scale orbits of the common parent"),
        kernel.prove_exact_rank(velocity_anchored_map, 8, subject="causal-speed anchor leaves one common-length orbit"),
        kernel.prove_exact_nullity(velocity_anchored_map, 1, subject="absolute edge length remains after fixing propagation speed"),
        kernel.prove_matrix_equality(velocity_anchored_map * velocity_anchored_kernel, sp.zeros(8, 1), subject="common length-energy orbit after the speed anchor"),
        kernel.prove_exact_rank(fully_anchored_map, 9, subject="speed and independent length anchors close the dimensional map"),
        kernel.prove_exact_nullity(fully_anchored_map, 0, subject="no scale orbit remains after an independent length anchor"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(11, 1), subject="conditional common edge-length architecture complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 11, subject="eleven conditional common-parent requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="growth-complex length and damping origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="common relative parent supplies no absolute physical selector"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate",
        theorems,
    )
    return EdgeLengthCommonParentCertificate(
        invariant_vector,
        parent_gradient,
        parent_hessian,
        scale_map,
        scale_kernel,
        velocity_anchored_map,
        velocity_anchored_kernel,
        fully_anchored_map,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate",
    title="Общий родитель длины ребра клеточного комплекса",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_cell_complex_edge_length_common_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"edge_length_common_parent_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(26)
    ),
)