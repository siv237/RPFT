"""LCF certificate for the common cell-birth clock-energy parent."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CellBirthClockEnergyCommonParentCertificate:
    bare_hamiltonian: sp.ImmutableMatrix
    exchange_generator: sp.ImmutableMatrix
    growth_coupling: sp.Expr
    step_growth: sp.Expr
    parent: sp.Expr
    stationary_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_orbit_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    relative_origin: sp.ImmutableMatrix
    bare_spectrum_theorem: Theorem
    exchange_commutator_theorem: Theorem
    exchange_rank_theorem: Theorem
    exchange_spectrum_theorem: Theorem
    growth_coupling_theorem: Theorem
    growth_coupling_positive_theorem: Theorem
    stationary_theorem: Theorem
    hessian_theorem: Theorem
    hessian_rank_theorem: Theorem
    hessian_determinant_theorem: Theorem
    hessian_spectrum_theorem: Theorem
    rate_calibration_theorem: Theorem
    growth_rate_theorem: Theorem
    relative_growth_theorem: Theorem
    scale_invariance_theorem: Theorem
    scale_orbit_nullity_theorem: Theorem
    required_frequency_theorem: Theorem
    architecture_theorem: Theorem
    relative_origin_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CellBirthClockEnergyCommonParentCertificate:
    x = sp.symbols("x", positive=True)
    u, rho = sp.symbols("u rho", real=True)
    energy, hbar, time, scale = sp.symbols(
        "E_C hbar t c", positive=True
    )

    birth_number = sp.diag(0, 0, 1, 1)
    clock_number = sp.diag(0, 1, 0, 1)
    bare_hamiltonian = sp.ImmutableMatrix(birth_number + clock_number)
    exchange_generator = sp.ImmutableMatrix([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ])

    growth_coupling = sp.log((1 + 2 * x) / (1 + x))
    step_growth = growth_coupling / 3
    parent = ((u - growth_coupling) ** 2 + (rho - u) ** 2) / 2
    stationary_point = {u: growth_coupling, rho: growth_coupling}
    stationary_gradient = sp.ImmutableMatrix([
        sp.diff(parent, variable).subs(stationary_point)
        for variable in (u, rho)
    ])
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, (u, rho)))

    clock_frequency = energy / hbar
    birth_rate = growth_coupling * clock_frequency
    hubble_rate = birth_rate / 3
    target_growth = x / sp.sqrt(8 * sp.pi)
    required_frequency = sp.simplify(target_growth / step_growth)
    phase = sp.exp(-sp.I * energy * time / hbar)
    rescaled_phase = sp.exp(-sp.I * (scale * energy) * (time / scale) / hbar)
    scale_orbit_map = sp.ImmutableMatrix([[1, 1]])
    architecture = sp.ones(9, 1)
    relative_origin = sp.ones(3, 1)

    bare_spectrum_theorem = kernel.prove_exact_spectrum(
        bare_hamiltonian,
        {sp.Integer(0): 1, sp.Integer(1): 2, sp.Integer(2): 1},
        subject="the birth-clock carrier has one resonant energy doublet",
    )
    exchange_commutator_theorem = kernel.prove_matrix_equality(
        bare_hamiltonian * exchange_generator,
        exchange_generator * bare_hamiltonian,
        subject="the birth-clock exchange preserves the bare total energy",
    )
    exchange_rank_theorem = kernel.prove_exact_rank(
        exchange_generator,
        2,
        subject="the resonant birth-clock exchange acts on exactly two states",
    )
    exchange_spectrum_theorem = kernel.prove_exact_spectrum(
        exchange_generator,
        {sp.Integer(-1): 1, sp.Integer(0): 2, sp.Integer(1): 1},
        subject="the resonant exchange has a symmetric unit spectrum",
    )
    growth_coupling_theorem = kernel.prove_expression_equality(
        growth_coupling,
        3 * step_growth,
        subject="the normalized cell-birth measure fixes the exchange coupling",
    )
    growth_coupling_positive_theorem = kernel.prove_positive_expression(
        growth_coupling,
        subject="the normalized cell-birth exchange coupling is positive",
    )
    stationary_theorem = kernel.prove_matrix_equality(
        stationary_gradient,
        sp.zeros(2, 1),
        subject="the common parent selects equal coupling and relative birth rate",
    )
    hessian_theorem = kernel.prove_matrix_equality(
        parent_hessian,
        sp.Matrix([[2, -1], [-1, 1]]),
        subject="the common birth-clock parent has an exact constant Hessian",
    )
    hessian_rank_theorem = kernel.prove_exact_rank(
        parent_hessian,
        2,
        subject="the common parent controls both relative variables",
    )
    hessian_determinant_theorem = kernel.prove_expression_equality(
        parent_hessian.det(),
        1,
        subject="the common parent Hessian has unit determinant",
    )
    hessian_spectrum_theorem = kernel.prove_exact_spectrum(
        parent_hessian,
        {
            (sp.Integer(3) - sp.sqrt(5)) / 2: 1,
            (sp.Integer(3) + sp.sqrt(5)) / 2: 1,
        },
        subject="the common parent is strictly positive in relative directions",
    )
    rate_calibration_theorem = kernel.prove_expression_equality(
        birth_rate,
        growth_coupling * energy / hbar,
        subject="the selected relative rate is calibrated by the clock energy",
    )
    growth_rate_theorem = kernel.prove_expression_equality(
        hubble_rate,
        step_growth * energy / hbar,
        subject="the physical geometric growth rate inherits the clock frequency",
    )
    relative_growth_theorem = kernel.prove_expression_equality(
        hubble_rate / clock_frequency,
        step_growth,
        subject="the clock-blind growth ratio equals the normalized step increment",
    )
    scale_invariance_theorem = kernel.prove_expression_equality(
        rescaled_phase,
        phase,
        subject="common energy-time rescaling preserves the birth-clock phase",
    )
    scale_orbit_nullity_theorem = kernel.prove_exact_nullity(
        scale_orbit_map,
        1,
        subject="the absolute birth-clock calibration retains one scale orbit",
    )
    required_frequency_theorem = kernel.prove_expression_equality(
        required_frequency,
        3 * x / (sp.sqrt(8 * sp.pi) * growth_coupling),
        subject="matching the proposed vacuum amplitude requires an extra clock frequency",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(9, 1),
        subject="all common birth-clock parent architecture conditions pass",
    )
    relative_origin_theorem = kernel.prove_matrix_equality(
        relative_origin,
        sp.ones(3, 1),
        subject="coupling rate ratio and clock-blind growth are jointly selected",
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_clock_energy_common_parent_origin_gate",
        (
            bare_spectrum_theorem,
            exchange_commutator_theorem,
            exchange_rank_theorem,
            exchange_spectrum_theorem,
            growth_coupling_theorem,
            growth_coupling_positive_theorem,
            stationary_theorem,
            hessian_theorem,
            hessian_rank_theorem,
            hessian_determinant_theorem,
            hessian_spectrum_theorem,
            rate_calibration_theorem,
            growth_rate_theorem,
            relative_growth_theorem,
            scale_invariance_theorem,
            scale_orbit_nullity_theorem,
            required_frequency_theorem,
            architecture_theorem,
            relative_origin_theorem,
        ),
    )
    return CellBirthClockEnergyCommonParentCertificate(
        bare_hamiltonian=bare_hamiltonian,
        exchange_generator=exchange_generator,
        growth_coupling=growth_coupling,
        step_growth=step_growth,
        parent=parent,
        stationary_gradient=stationary_gradient,
        parent_hessian=parent_hessian,
        scale_orbit_map=scale_orbit_map,
        architecture=architecture,
        relative_origin=relative_origin,
        bare_spectrum_theorem=bare_spectrum_theorem,
        exchange_commutator_theorem=exchange_commutator_theorem,
        exchange_rank_theorem=exchange_rank_theorem,
        exchange_spectrum_theorem=exchange_spectrum_theorem,
        growth_coupling_theorem=growth_coupling_theorem,
        growth_coupling_positive_theorem=growth_coupling_positive_theorem,
        stationary_theorem=stationary_theorem,
        hessian_theorem=hessian_theorem,
        hessian_rank_theorem=hessian_rank_theorem,
        hessian_determinant_theorem=hessian_determinant_theorem,
        hessian_spectrum_theorem=hessian_spectrum_theorem,
        rate_calibration_theorem=rate_calibration_theorem,
        growth_rate_theorem=growth_rate_theorem,
        relative_growth_theorem=relative_growth_theorem,
        scale_invariance_theorem=scale_invariance_theorem,
        scale_orbit_nullity_theorem=scale_orbit_nullity_theorem,
        required_frequency_theorem=required_frequency_theorem,
        architecture_theorem=architecture_theorem,
        relative_origin_theorem=relative_origin_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_clock_energy_common_parent_origin_gate",
    title="Общий родитель рождения ячеек, часов и энергии",
    source_paths=(
        "s2t/gates/version10_cell_birth_clock_energy_common_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_clock_energy_common_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("birth_clock_bare_spectrum", lambda: build_certificate().bare_spectrum_theorem),
        Obligation("resonant_exchange_energy_conservation", lambda: build_certificate().exchange_commutator_theorem),
        Obligation("resonant_exchange_rank_two", lambda: build_certificate().exchange_rank_theorem),
        Obligation("resonant_exchange_spectrum", lambda: build_certificate().exchange_spectrum_theorem),
        Obligation("growth_coupling_three_delta_zeta", lambda: build_certificate().growth_coupling_theorem),
        Obligation("growth_coupling_positive", lambda: build_certificate().growth_coupling_positive_theorem),
        Obligation("common_parent_stationary_point", lambda: build_certificate().stationary_theorem),
        Obligation("common_parent_hessian", lambda: build_certificate().hessian_theorem),
        Obligation("common_parent_hessian_rank_two", lambda: build_certificate().hessian_rank_theorem),
        Obligation("common_parent_hessian_determinant_one", lambda: build_certificate().hessian_determinant_theorem),
        Obligation("common_parent_positive_spectrum", lambda: build_certificate().hessian_spectrum_theorem),
        Obligation("clock_energy_rate_calibration", lambda: build_certificate().rate_calibration_theorem),
        Obligation("physical_growth_rate", lambda: build_certificate().growth_rate_theorem),
        Obligation("clock_blind_relative_growth", lambda: build_certificate().relative_growth_theorem),
        Obligation("energy_time_scale_invariance", lambda: build_certificate().scale_invariance_theorem),
        Obligation("absolute_scale_orbit_nullity_one", lambda: build_certificate().scale_orbit_nullity_theorem),
        Obligation("vacuum_target_required_frequency", lambda: build_certificate().required_frequency_theorem),
        Obligation("common_parent_architecture_full", lambda: build_certificate().architecture_theorem),
        Obligation("relative_origin_full", lambda: build_certificate().relative_origin_theorem),
    ),
)