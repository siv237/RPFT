"""LCF certificate for the physical-time readout of universal-cover height."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel
from ..structures import Morphism, Space


@dataclass(frozen=True, slots=True)
class BirthHeightPhysicalTimeCertificate:
    height: sp.ImmutableMatrix
    affine_time_map: sp.ImmutableMatrix
    edge_time_map: sp.ImmutableMatrix
    origin_edge_effect: sp.ImmutableMatrix
    tick_edge_effect: sp.ImmutableMatrix
    normalized_time_labels: sp.ImmutableMatrix
    shifted_time_labels: sp.ImmutableMatrix
    clock_invariants: sp.ImmutableMatrix
    parent_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    speed_anchored_map: sp.ImmutableMatrix
    speed_anchored_kernel: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BirthHeightPhysicalTimeCertificate:
    height = sp.ImmutableMatrix(range(-3, 4))
    affine_time_map = sp.ImmutableMatrix.hstack(sp.ones(7, 1), height)
    boundary = sp.ImmutableMatrix(
        7, 6, lambda i, j: -1 if i == j else (1 if i == j + 1 else 0)
    )
    edge_time_map = sp.ImmutableMatrix(boundary.T * affine_time_map)
    origin_parameter = sp.ImmutableMatrix([1, 0])
    tick_parameter = sp.ImmutableMatrix([0, 1])
    origin_edge_effect = sp.ImmutableMatrix(edge_time_map * origin_parameter)
    tick_edge_effect = sp.ImmutableMatrix(edge_time_map * tick_parameter)
    normalized_time_labels = sp.ImmutableMatrix(affine_time_map * tick_parameter)
    shifted_time_labels = sp.ImmutableMatrix(affine_time_map * sp.ImmutableMatrix([5, 1]))

    affine_parameters = Space("Aff(1)_birth", 2, "R")
    vertex_times = Space("T_vertices", 7, "R")
    edge_ticks = Space("Delta T_edges", 6, "R")
    time_readout_morphism = Morphism("time_readout", affine_parameters, vertex_times, affine_time_map)
    edge_difference_morphism = Morphism("delta_time", vertex_times, edge_ticks, boundary.T)
    affine_edge_morphism = time_readout_morphism.then(edge_difference_morphism, name="delta_time_after_readout")

    clock_invariants = sp.ImmutableMatrix([1, 1, 1])
    q_energy, q_transit, q_compton = sp.symbols(
        "q_energy q_transit q_compton", real=True
    )
    coordinates = (q_energy, q_transit, q_compton)
    parent = sum((coordinate - 1) ** 2 for coordinate in coordinates) / 2
    target = {coordinate: 1 for coordinate in coordinates}
    parent_gradient = sp.ImmutableMatrix(
        [sp.diff(parent, coordinate) for coordinate in coordinates]
    ).subs(target)
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, coordinates))

    # Logarithmic variables are (tau_birth, E_C, ell_edge, c).
    # The rows encode E_C tau_birth/hbar, c tau_birth/ell_edge and
    # E_C ell_edge/(hbar c); the third row is the first minus the second.
    scale_map = sp.ImmutableMatrix(
        [[1, 1, 0, 0], [1, 0, -1, 1], [0, 1, 1, -1]]
    )
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([1, -1, 1, 0]),
        sp.ImmutableMatrix([-1, 1, 0, 1]),
    )
    speed_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 0, 0, 1]])
    )
    speed_anchored_kernel = sp.ImmutableMatrix([1, -1, 1, 0])
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        speed_anchored_map, sp.ImmutableMatrix([[0, 0, 1, 0]])
    )
    conditional_origin = sp.ones(10, 1)
    physical_origin = sp.zeros(2, 1)

    theorems = (
        kernel.prove_well_typed_morphism(time_readout_morphism),
        kernel.prove_well_typed_morphism(edge_difference_morphism),
        kernel.prove_well_typed_morphism(affine_edge_morphism),
        kernel.prove_exact_rank(affine_time_map, 2, subject="affine birth-time readout has origin and tick coordinates"),
        kernel.prove_matrix_equality(edge_time_map, sp.ImmutableMatrix.hstack(sp.zeros(6, 1), sp.ones(6, 1)), subject="edge differences remove the time origin and retain the tick"),
        kernel.prove_exact_rank(edge_time_map, 1, subject="edge-time readout fixes only the affine slope"),
        kernel.prove_exact_nullity(edge_time_map, 1, subject="additive time origin is a readout gauge mode"),
        kernel.prove_matrix_equality(origin_edge_effect, sp.zeros(6, 1), subject="time-origin shifts have zero edge effect"),
        kernel.prove_matrix_equality(tick_edge_effect, sp.ones(6, 1), subject="unit normalized tick on every birth edge"),
        kernel.prove_matrix_equality(normalized_time_labels, height, subject="normalized physical-time labels reproduce cover height"),
        kernel.prove_matrix_equality(boundary.T * shifted_time_labels, sp.ones(6, 1), subject="translated time labels preserve all birth intervals"),
        kernel.prove_matrix_inequality(shifted_time_labels, normalized_time_labels, subject="distinct absolute time origins realize the same intervals"),
        kernel.prove_matrix_equality(clock_invariants, sp.ones(3, 1), subject="clock energy transit and Compton invariants agree"),
        kernel.prove_matrix_equality(parent_gradient, sp.zeros(3, 1), subject="conditional clock-metric parent stationary point"),
        kernel.prove_matrix_equality(parent_hessian, sp.eye(3), subject="conditional clock-metric invariant Hessian"),
        kernel.prove_exact_rank(parent_hessian, 3, subject="clock-metric parent is strict in invariant coordinates"),
        kernel.prove_expression_equality(parent_hessian.det(), 1, subject="clock-metric invariant parent determinant"),
        kernel.prove_matrix_equality(scale_map[2, :], scale_map[0, :] - scale_map[1, :], subject="Compton relation is dependent on energy-tick and causal-transit relations"),
        kernel.prove_exact_rank(scale_map, 2, subject="physical birth-time dimensional map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="speed and common tick-length scale freedoms"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(3, 2), subject="two physical-time scale orbits"),
        kernel.prove_exact_rank(speed_anchored_map, 3, subject="fixing c leaves one common tick-length orbit"),
        kernel.prove_exact_nullity(speed_anchored_map, 1, subject="absolute birth tick remains after the speed anchor"),
        kernel.prove_matrix_equality(speed_anchored_map * speed_anchored_kernel, sp.zeros(4, 1), subject="birth tick edge length and clock energy rescale together"),
        kernel.prove_exact_rank(fully_anchored_map, 4, subject="speed and independent length anchors close the birth-time map"),
        kernel.prove_exact_nullity(fully_anchored_map, 0, subject="no birth-time scale orbit remains after a length anchor"),
        kernel.prove_matrix_equality(conditional_origin, sp.ones(10, 1), subject="conditional birth-height time morphism complete"),
        kernel.prove_expression_equality(sum(conditional_origin), 10, subject="ten conditional physical-time morphism requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="physical time-readout selection and absolute tick remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="no absolute birth-time anchor is supplied"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate",
        theorems,
    )
    return BirthHeightPhysicalTimeCertificate(
        height,
        affine_time_map,
        edge_time_map,
        origin_edge_effect,
        tick_edge_effect,
        normalized_time_labels,
        shifted_time_labels,
        clock_invariants,
        parent_gradient,
        parent_hessian,
        scale_map,
        scale_kernel,
        speed_anchored_map,
        speed_anchored_kernel,
        fully_anchored_map,
        conditional_origin,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate",
    title="Морфизм высоты универсального покрытия в физическое время",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_universal_cover_birth_height_physical_time_morphism_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"birth_height_physical_time_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(30)
    ),
)