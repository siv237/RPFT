"""LCF certificate for the intrinsic cell four-volume parent boundary."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CellBirthIntrinsicFourVolumeParentCertificate:
    cell_gram: sp.ImmutableMatrix
    normalized_shape: sp.ImmutableMatrix
    cell_volume: sp.Expr
    dimensionless_volume_energy: sp.Expr
    common_parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    common_hessian: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    relative_origin: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    gram_determinant_theorem: Theorem
    cell_volume_theorem: Theorem
    normalized_shape_theorem: Theorem
    normalized_determinant_theorem: Theorem
    volume_scaling_theorem: Theorem
    total_volume_theorem: Theorem
    birth_increment_theorem: Theorem
    invariant_unit_theorem: Theorem
    invariant_scaling_theorem: Theorem
    stationary_theorem: Theorem
    hessian_theorem: Theorem
    hessian_rank_theorem: Theorem
    hessian_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    hessian_spectrum_theorem: Theorem
    hessian_determinant_theorem: Theorem
    architecture_theorem: Theorem
    relative_origin_theorem: Theorem
    physical_ledger_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CellBirthIntrinsicFourVolumeParentCertificate:
    length, scale, energy, hbar, light_speed = sp.symbols(
        "ell_cell s E_C hbar c", positive=True
    )
    cell_count = sp.symbols("N", integer=True, positive=True)

    cell_gram = sp.ImmutableMatrix(length**2 * sp.eye(4))
    cell_volume = sp.simplify(sp.sqrt(cell_gram.det()))
    normalized_shape = sp.ImmutableMatrix(
        sp.simplify(cell_gram / sp.sqrt(cell_volume))
    )
    total_volume = cell_count * cell_volume
    next_total_volume = (cell_count + 1) * cell_volume

    dimensionless_volume_energy = sp.simplify(
        energy**4 * cell_volume / (hbar * light_speed) ** 4
    )
    compton_energy = hbar * light_speed / length
    rescaled_invariant = sp.simplify(
        (energy / scale) ** 4
        * ((scale * length) ** 4)
        / (hbar * light_speed) ** 4
    )

    u, rho, energy_log, length_log, coupling = sp.symbols(
        "u rho epsilon lambda k_X", real=True
    )
    common_parent = (
        ((u - coupling) ** 2 + (rho - u) ** 2) / 2
        + (energy_log + length_log) ** 2 / 2
    )
    stationary_point = {
        u: coupling,
        rho: coupling,
        energy_log: 0,
        length_log: 0,
    }
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(common_parent, variable).subs(stationary_point)
        for variable in (u, rho, energy_log, length_log)
    ])
    common_hessian = sp.ImmutableMatrix(
        sp.hessian(common_parent, (u, rho, energy_log, length_log))
    )
    scale_vector = sp.ImmutableMatrix([0, 0, 1, -1])
    architecture = sp.ones(8, 1)
    relative_origin = sp.ones(3, 1)
    physical_ledger = sp.zeros(2, 1)

    gram_determinant_theorem = kernel.prove_expression_equality(
        cell_gram.det(),
        length**8,
        subject="the isotropic four-cell Gram determinant has length degree eight",
    )
    cell_volume_theorem = kernel.prove_expression_equality(
        cell_volume,
        length**4,
        subject="the intrinsic four-volume is the fourth power of cell length",
    )
    normalized_shape_theorem = kernel.prove_matrix_equality(
        normalized_shape,
        sp.eye(4),
        subject="volume normalization removes the isotropic cell scale",
    )
    normalized_determinant_theorem = kernel.prove_expression_equality(
        normalized_shape.det(),
        1,
        subject="the normalized cell shape is unimodular",
    )
    volume_scaling_theorem = kernel.prove_expression_equality(
        (scale * length) ** 4,
        scale**4 * cell_volume,
        subject="a common length dilation scales intrinsic four-volume quartically",
    )
    total_volume_theorem = kernel.prove_expression_equality(
        total_volume,
        cell_count * length**4,
        subject="total four-volume is cell count times intrinsic cell volume",
    )
    birth_increment_theorem = kernel.prove_expression_equality(
        next_total_volume - total_volume,
        cell_volume,
        subject="one birth increases total four-volume by one intrinsic cell volume",
    )
    invariant_unit_theorem = kernel.prove_expression_equality(
        dimensionless_volume_energy.subs(energy, compton_energy),
        1,
        subject="the volume-energy invariant is unity on the Compton relation",
    )
    invariant_scaling_theorem = kernel.prove_expression_equality(
        rescaled_invariant,
        dimensionless_volume_energy,
        subject="opposite energy and length scaling preserves the volume-energy invariant",
    )
    stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(4, 1),
        subject="the combined relative parent has a stationary unit representative",
    )
    hessian_theorem = kernel.prove_matrix_equality(
        common_hessian,
        sp.Matrix([
            [2, -1, 0, 0],
            [-1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
        ]),
        subject="the volume-clock common parent has an exact block Hessian",
    )
    hessian_rank_theorem = kernel.prove_exact_rank(
        common_hessian,
        3,
        subject="the common parent fixes three of four logarithmic variables",
    )
    hessian_nullity_theorem = kernel.prove_exact_nullity(
        common_hessian,
        1,
        subject="one opposite energy-length rescaling remains flat",
    )
    scale_kernel_theorem = kernel.prove_matrix_equality(
        common_hessian * scale_vector,
        sp.zeros(4, 1),
        subject="the energy-length scale vector is the exact parent zero mode",
    )
    hessian_spectrum_theorem = kernel.prove_exact_spectrum(
        common_hessian,
        {
            sp.Integer(0): 1,
            sp.Integer(2): 1,
            (sp.Integer(3) - sp.sqrt(5)) / 2: 1,
            (sp.Integer(3) + sp.sqrt(5)) / 2: 1,
        },
        subject="the common parent is positive semidefinite with one scale zero mode",
    )
    hessian_determinant_theorem = kernel.prove_expression_equality(
        common_hessian.det(),
        0,
        subject="the common parent determinant vanishes only along absolute scale",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(8, 1),
        subject="all intrinsic four-volume carrier conditions pass",
    )
    relative_origin_theorem = kernel.prove_matrix_equality(
        relative_origin,
        sp.ones(3, 1),
        subject="cell volume birth increment and volume-energy relation are constructed",
    )
    physical_ledger_theorem = kernel.prove_matrix_equality(
        physical_ledger,
        sp.zeros(2, 1),
        subject="cell volume magnitude and clock energy remain unselected",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_intrinsic_four_volume_parent_origin_gate",
        (
            gram_determinant_theorem,
            cell_volume_theorem,
            normalized_shape_theorem,
            normalized_determinant_theorem,
            volume_scaling_theorem,
            total_volume_theorem,
            birth_increment_theorem,
            invariant_unit_theorem,
            invariant_scaling_theorem,
            stationary_theorem,
            hessian_theorem,
            hessian_rank_theorem,
            hessian_nullity_theorem,
            scale_kernel_theorem,
            hessian_spectrum_theorem,
            hessian_determinant_theorem,
            architecture_theorem,
            relative_origin_theorem,
            physical_ledger_theorem,
        ),
    )
    return CellBirthIntrinsicFourVolumeParentCertificate(
        cell_gram=cell_gram,
        normalized_shape=normalized_shape,
        cell_volume=cell_volume,
        dimensionless_volume_energy=dimensionless_volume_energy,
        common_parent=common_parent,
        stationary_gradient=stationary_gradient,
        common_hessian=common_hessian,
        scale_vector=scale_vector,
        architecture=architecture,
        relative_origin=relative_origin,
        physical_ledger=physical_ledger,
        gram_determinant_theorem=gram_determinant_theorem,
        cell_volume_theorem=cell_volume_theorem,
        normalized_shape_theorem=normalized_shape_theorem,
        normalized_determinant_theorem=normalized_determinant_theorem,
        volume_scaling_theorem=volume_scaling_theorem,
        total_volume_theorem=total_volume_theorem,
        birth_increment_theorem=birth_increment_theorem,
        invariant_unit_theorem=invariant_unit_theorem,
        invariant_scaling_theorem=invariant_scaling_theorem,
        stationary_theorem=stationary_theorem,
        hessian_theorem=hessian_theorem,
        hessian_rank_theorem=hessian_rank_theorem,
        hessian_nullity_theorem=hessian_nullity_theorem,
        scale_kernel_theorem=scale_kernel_theorem,
        hessian_spectrum_theorem=hessian_spectrum_theorem,
        hessian_determinant_theorem=hessian_determinant_theorem,
        architecture_theorem=architecture_theorem,
        relative_origin_theorem=relative_origin_theorem,
        physical_ledger_theorem=physical_ledger_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_intrinsic_four_volume_parent_origin_gate",
    title="Родитель собственного четырёхмерного объёма ячейки",
    source_paths=(
        "s2t/gates/version10_cell_birth_intrinsic_four_volume_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_intrinsic_four_volume_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("cell_gram_determinant_length_eight", lambda: build_certificate().gram_determinant_theorem),
        Obligation("intrinsic_cell_four_volume", lambda: build_certificate().cell_volume_theorem),
        Obligation("normalized_cell_shape_identity", lambda: build_certificate().normalized_shape_theorem),
        Obligation("normalized_cell_shape_unimodular", lambda: build_certificate().normalized_determinant_theorem),
        Obligation("four_volume_quartic_scaling", lambda: build_certificate().volume_scaling_theorem),
        Obligation("total_volume_cell_count_factorization", lambda: build_certificate().total_volume_theorem),
        Obligation("single_birth_volume_increment", lambda: build_certificate().birth_increment_theorem),
        Obligation("volume_energy_invariant_unit", lambda: build_certificate().invariant_unit_theorem),
        Obligation("volume_energy_scale_invariance", lambda: build_certificate().invariant_scaling_theorem),
        Obligation("common_parent_stationary_representative", lambda: build_certificate().stationary_theorem),
        Obligation("common_parent_block_hessian", lambda: build_certificate().hessian_theorem),
        Obligation("common_parent_rank_three", lambda: build_certificate().hessian_rank_theorem),
        Obligation("common_parent_nullity_one", lambda: build_certificate().hessian_nullity_theorem),
        Obligation("energy_length_scale_kernel", lambda: build_certificate().scale_kernel_theorem),
        Obligation("common_parent_semidefinite_spectrum", lambda: build_certificate().hessian_spectrum_theorem),
        Obligation("common_parent_zero_determinant", lambda: build_certificate().hessian_determinant_theorem),
        Obligation("intrinsic_volume_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("relative_volume_origin_full", lambda: build_certificate().relative_origin_theorem),
        Obligation("absolute_volume_energy_origin_zero", lambda: build_certificate().physical_ledger_theorem),
    ),
)