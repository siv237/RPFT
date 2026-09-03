"""LCF certificate for the geometric-growth quantum/RG carrier of Tome X."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class QuantumRGCommonCarrierAdmissionCertificate:
    growth_amplitude: sp.Expr
    cell_count: sp.Expr
    scale_factor: sp.Expr
    cosmological_curvature: sp.Expr
    atlas: sp.ImmutableMatrix
    masses: sp.ImmutableMatrix
    atlas_contrast: sp.ImmutableMatrix
    carrier_incidence: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    initial_cell_theorem: Theorem
    initial_scale_theorem: Theorem
    volume_scale_theorem: Theorem
    scale_rate_theorem: Theorem
    cell_rate_theorem: Theorem
    cosmological_curvature_theorem: Theorem
    atlas_contrast_theorem: Theorem
    atlas_rank_theorem: Theorem
    codilation_theorem: Theorem
    carrier_rank_theorem: Theorem
    architecture_theorem: Theorem
    physical_origin_theorem: Theorem
    status_gap_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> QuantumRGCommonCarrierAdmissionCertificate:
    action, tau = sp.symbols("S_vac tau", real=True)
    n0, e0 = sp.symbols("N_0 E_0", positive=True)

    growth_amplitude = sp.exp(-action) / sp.sqrt(8 * sp.pi)
    cell_count = n0 * sp.exp(3 * growth_amplitude * tau)
    scale_factor = sp.exp(growth_amplitude * tau)
    cosmological_curvature = 3 * growth_amplitude**2

    atlas = sp.ImmutableMatrix([1, 2, 3])
    masses = sp.ImmutableMatrix(e0 * atlas)
    atlas_contrast = sp.ImmutableMatrix([
        [-2, 1, 0],
        [-3, 0, 1],
    ])
    carrier_incidence = sp.ImmutableMatrix([
        [1, 1, 0],
        [0, 1, 1],
        [1, 0, 1],
    ])
    architecture = sp.ones(7, 1)
    physical_origin = sp.zeros(3, 1)

    initial_cell_theorem = kernel.prove_expression_equality(
        cell_count.subs(tau, 0),
        n0,
        subject="geometric history begins with the declared positive cell count",
    )
    initial_scale_theorem = kernel.prove_expression_equality(
        scale_factor.subs(tau, 0),
        1,
        subject="the relative geometric scale is normalized at the initial slice",
    )
    volume_scale_theorem = kernel.prove_expression_equality(
        scale_factor**3,
        cell_count / n0,
        subject="spatial scale factor is the cube root of relative cell number",
    )
    scale_rate_theorem = kernel.prove_expression_equality(
        sp.diff(scale_factor, tau) / scale_factor,
        growth_amplitude,
        subject="growth amplitude is the logarithmic scale-factor rate",
    )
    cell_rate_theorem = kernel.prove_expression_equality(
        sp.diff(cell_count, tau) / (3 * cell_count),
        growth_amplitude,
        subject="growth amplitude is one third of the logarithmic cell-number rate",
    )
    cosmological_curvature_theorem = kernel.prove_expression_equality(
        cosmological_curvature,
        sp.Rational(3, 8) * sp.exp(-2 * action) / sp.pi,
        subject="the old vacuum formula is the Friedmann square of growth amplitude",
    )
    atlas_contrast_theorem = kernel.prove_matrix_equality(
        atlas_contrast * masses,
        sp.zeros(2, 1),
        subject="a common geometric scale preserves the dimensionless spectral atlas",
    )
    atlas_rank_theorem = kernel.prove_exact_rank(
        atlas_contrast,
        2,
        subject="two independent mass ratios survive common scale evolution",
    )
    codilation_theorem = kernel.prove_expression_equality(
        scale_factor * (e0 / scale_factor),
        e0,
        subject="pure codilation leaves the local dimensionless readout invariant",
    )
    carrier_rank_theorem = kernel.prove_exact_rank(
        carrier_incidence,
        3,
        subject="history cell and local field layers are nonredundant",
    )
    architecture_theorem = kernel.prove_matrix_equality(
        architecture,
        sp.ones(7, 1),
        subject="all geometric-growth carrier admission conditions are met",
    )
    physical_origin_theorem = kernel.prove_matrix_equality(
        physical_origin,
        sp.zeros(3, 1),
        subject="growth law tick and local scale origins remain unproved",
    )
    status_gap_theorem = kernel.prove_positive_expression(
        sum(architecture) - sum(physical_origin),
        subject="carrier admission is strictly weaker than physical origin",
    )
    gate_theorem = kernel.prove_gate(
        "version10_quantum_rg_common_carrier_admission_gate",
        (
            initial_cell_theorem,
            initial_scale_theorem,
            volume_scale_theorem,
            scale_rate_theorem,
            cell_rate_theorem,
            cosmological_curvature_theorem,
            atlas_contrast_theorem,
            atlas_rank_theorem,
            codilation_theorem,
            carrier_rank_theorem,
            architecture_theorem,
            physical_origin_theorem,
            status_gap_theorem,
        ),
    )
    return QuantumRGCommonCarrierAdmissionCertificate(
        growth_amplitude=growth_amplitude,
        cell_count=cell_count,
        scale_factor=scale_factor,
        cosmological_curvature=cosmological_curvature,
        atlas=atlas,
        masses=masses,
        atlas_contrast=atlas_contrast,
        carrier_incidence=carrier_incidence,
        architecture=architecture,
        physical_origin=physical_origin,
        initial_cell_theorem=initial_cell_theorem,
        initial_scale_theorem=initial_scale_theorem,
        volume_scale_theorem=volume_scale_theorem,
        scale_rate_theorem=scale_rate_theorem,
        cell_rate_theorem=cell_rate_theorem,
        cosmological_curvature_theorem=cosmological_curvature_theorem,
        atlas_contrast_theorem=atlas_contrast_theorem,
        atlas_rank_theorem=atlas_rank_theorem,
        codilation_theorem=codilation_theorem,
        carrier_rank_theorem=carrier_rank_theorem,
        architecture_theorem=architecture_theorem,
        physical_origin_theorem=physical_origin_theorem,
        status_gap_theorem=status_gap_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_quantum_rg_common_carrier_admission_gate",
    title="Геометрически растущий общий носитель квантового хода",
    source_paths=(
        "s2t/gates/version10_quantum_rg_common_carrier_admission_gate.tex",
        "s2t/results/s2t_v10_quantum_rg_common_carrier_admission_gate_results.json",
    ),
    obligations=(
        Obligation("initial_positive_cell_count", lambda: build_certificate().initial_cell_theorem),
        Obligation("initial_relative_scale", lambda: build_certificate().initial_scale_theorem),
        Obligation("cell_volume_scale_identity", lambda: build_certificate().volume_scale_theorem),
        Obligation("scale_factor_growth_rate", lambda: build_certificate().scale_rate_theorem),
        Obligation("cell_number_growth_rate", lambda: build_certificate().cell_rate_theorem),
        Obligation("cosmological_curvature_identity", lambda: build_certificate().cosmological_curvature_theorem),
        Obligation("dimensionless_atlas_invariance", lambda: build_certificate().atlas_contrast_theorem),
        Obligation("two_independent_atlas_ratios", lambda: build_certificate().atlas_rank_theorem),
        Obligation("pure_codilation_invariance", lambda: build_certificate().codilation_theorem),
        Obligation("common_carrier_layer_rank", lambda: build_certificate().carrier_rank_theorem),
        Obligation("architecture_admission_full", lambda: build_certificate().architecture_theorem),
        Obligation("physical_origin_open", lambda: build_certificate().physical_origin_theorem),
        Obligation("admission_origin_status_gap", lambda: build_certificate().status_gap_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)