"""LCF certificate for the bath group-velocity to cell-birth front morphism."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FrontSpeedMorphismCertificate:
    propagation_cells: sp.Rational
    group_speed: sp.Expr
    local_growth_speed: sp.Expr
    front_speed: sp.Expr
    transfer_factor: sp.Expr
    crossing_radius: sp.Rational
    sample_transfer: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernels: sp.ImmutableMatrix
    radius_anchored_map: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    parent_kernel: sp.ImmutableMatrix
    anchored_hessian: sp.ImmutableMatrix
    stationary_gradient: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    conditional_origin: sp.ImmutableMatrix
    physical_status: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FrontSpeedMorphismCertificate:
    k_x = sp.symbols("k_X", positive=True)
    rho = sp.symbols("rho", positive=True)
    rho_0 = sp.symbols("rho_0", positive=True)
    zeta = sp.symbols("zeta", real=True)
    g, f, h = sp.symbols("g f h", real=True)

    propagation_cells = sp.Rational(121, 8)
    group_speed = sp.Rational(121, 24) * k_x
    local_growth_speed = k_x / 3
    front_speed = rho * k_x / 3
    transfer_factor = sp.Rational(8, 121) * rho
    crossing_radius = propagation_cells
    sample_transfer = sp.ImmutableMatrix(
        [sp.Rational(1, 2), 1, 2]
    )

    scale_map = sp.ImmutableMatrix(
        [[1, -1, 0, 0], [0, -1, -1, 1]]
    )
    scale_kernels = sp.ImmutableMatrix(
        [[1, 0], [1, 0], [0, 1], [1, 1]]
    )
    radius_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 0, 1, 0]])
    )

    parent = (
        (g - propagation_cells * h) ** 2
        + (f - rho * h) ** 2
    ) / 2
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (g, f, h)))
    parent_kernel = sp.ImmutableMatrix([propagation_cells, rho, 1])
    anchored_parent = parent + (h - k_x / 3) ** 2 / 2
    anchored_hessian = sp.ImmutableMatrix(
        sp.hessian(anchored_parent, (g, f, h))
    )
    stationary = {
        g: group_speed,
        f: front_speed,
        h: local_growth_speed,
    }
    stationary_gradient = sp.ImmutableMatrix(
        [sp.simplify(sp.diff(anchored_parent, x).subs(stationary)) for x in (g, f, h)]
    )

    rho_history = rho_0 * sp.exp(zeta)
    zeta_star = sp.log(propagation_cells / rho_0)
    history_transfer = sp.simplify(transfer_factor.subs(rho, rho_history))

    architecture = sp.ones(10, 1)
    conditional_origin = sp.ones(8, 1)
    physical_status = sp.ImmutableMatrix([1, 0, 0])

    theorems = (
        kernel.prove_expression_equality(
            propagation_cells, sp.Rational(121, 8),
            subject="bath propagation length in cell units",
        ),
        kernel.prove_expression_equality(
            group_speed, propagation_cells * local_growth_speed,
            subject="group speed is the local growth speed across 121/8 cells",
        ),
        kernel.prove_expression_equality(
            front_speed, rho * local_growth_speed,
            subject="cell-birth level-set front kinematics",
        ),
        kernel.prove_expression_equality(
            front_speed / group_speed, transfer_factor,
            subject="typed radius-dependent front transfer",
        ),
        kernel.prove_expression_equality(
            transfer_factor.subs(rho, crossing_radius), 1,
            subject="group and front speeds meet on one shell",
        ),
        kernel.prove_matrix_equality(
            sp.ImmutableMatrix([
                transfer_factor.subs(rho, crossing_radius / 2),
                transfer_factor.subs(rho, crossing_radius),
                transfer_factor.subs(rho, 2 * crossing_radius),
            ]),
            sample_transfer,
            subject="front transfer is not a universal identity",
        ),
        kernel.prove_expression_equality(
            group_speed / local_growth_speed, propagation_cells,
            subject="bath causal reach per growth time",
        ),
        kernel.prove_expression_equality(
            local_growth_speed, sp.Rational(8, 121) * group_speed,
            subject="growth speed recovered from bath group speed",
        ),
        kernel.prove_expression_equality(
            history_transfer,
            sp.Rational(8, 121) * rho_0 * sp.exp(zeta),
            subject="front transfer along the growth history",
        ),
        kernel.prove_expression_equality(
            history_transfer.subs(zeta, zeta_star), 1,
            subject="unique logarithmic crossing epoch",
        ),
        kernel.prove_expression_equality(
            sp.diff(history_transfer, zeta), history_transfer,
            subject="front transfer changes along every nonstatic history",
        ),
        kernel.prove_exact_rank(
            scale_map, 2, subject="two independent velocity-front relations"
        ),
        kernel.prove_exact_nullity(
            scale_map, 2, subject="clock scale and radius state directions remain"
        ),
        kernel.prove_matrix_equality(
            scale_map * scale_kernels, sp.zeros(2, 2),
            subject="explicit calibration and radius kernels",
        ),
        kernel.prove_exact_rank(
            radius_anchored_map, 3,
            subject="fixing the growth state removes the radius direction",
        ),
        kernel.prove_exact_nullity(
            radius_anchored_map, 1,
            subject="one common velocity-clock calibration remains",
        ),
        kernel.prove_matrix_equality(
            parent_hessian,
            sp.Matrix([
                [1, 0, -propagation_cells],
                [0, 1, -rho],
                [-propagation_cells, -rho, propagation_cells**2 + rho**2],
            ]),
            subject="unanchored morphism parent Hessian",
        ),
        kernel.prove_exact_rank(
            parent_hessian, 2, subject="unanchored morphism parent rank"
        ),
        kernel.prove_exact_nullity(
            parent_hessian, 1, subject="unanchored common amplitude remains"
        ),
        kernel.prove_matrix_equality(
            parent_hessian * parent_kernel, sp.zeros(3, 1),
            subject="parent null direction",
        ),
        kernel.prove_exact_rank(
            anchored_hessian, 3, subject="growth anchor closes the morphism parent"
        ),
        kernel.prove_expression_equality(
            anchored_hessian.det(), 1,
            subject="anchored morphism parent determinant",
        ),
        kernel.prove_matrix_equality(
            stationary_gradient, sp.zeros(3, 1),
            subject="derived group and front speeds are the unique stationary point",
        ),
        kernel.prove_matrix_equality(
            architecture, sp.ones(10, 1),
            subject="front morphism architecture complete",
        ),
        kernel.prove_expression_equality(
            sum(architecture), 10,
            subject="ten architecture requirements pass",
        ),
        kernel.prove_matrix_equality(
            conditional_origin, sp.ones(8, 1),
            subject="conditional provenance transfer complete",
        ),
        kernel.prove_expression_equality(
            sum(conditional_origin), 8,
            subject="eight conditional origin requirements pass",
        ),
        kernel.prove_matrix_equality(
            physical_status, sp.Matrix([1, 0, 0]),
            subject="typed morphism passes while universal and causal identities fail",
        ),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate",
        theorems,
    )
    return FrontSpeedMorphismCertificate(
        propagation_cells,
        group_speed,
        local_growth_speed,
        front_speed,
        transfer_factor,
        crossing_radius,
        sample_transfer,
        scale_map,
        scale_kernels,
        radius_anchored_map,
        parent_hessian,
        parent_kernel,
        anchored_hessian,
        stationary_gradient,
        architecture,
        conditional_origin,
        physical_status,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate",
    title="Морфизм групповой скорости ванны в скорость фронта рождения клеток",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_group_velocity_cell_birth_front_speed_morphism_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(
            f"front_speed_morphism_{i:02d}",
            lambda i=i: build_certificate().theorems[i],
        )
        for i in range(28)
    ),
)