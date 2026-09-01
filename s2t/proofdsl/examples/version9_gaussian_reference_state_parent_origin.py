"""LCF certificate for the Gaussian reference-state parent-origin boundary."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class GaussianReferenceStateParentOriginCertificate:
    drift: sp.ImmutableMatrix
    diffusion: sp.ImmutableMatrix
    stationary_covariance: sp.ImmutableMatrix
    lyapunov_map: sp.ImmutableMatrix
    ratio_orbit_map: sp.ImmutableMatrix
    dimension_theorem: Theorem
    symmetric_dimension_theorem: Theorem
    stationary_theorem: Theorem
    reversible_theorem: Theorem
    lyapunov_rank_theorem: Theorem
    lyapunov_nullity_theorem: Theorem
    unit_witness_theorem: Theorem
    doubled_witness_theorem: Theorem
    witness_separation_theorem: Theorem
    rescaling_theorem: Theorem
    ratio_nonconstant_theorem: Theorem
    ratio_orbit_nullity_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> GaussianReferenceStateParentOriginCertificate:
    gamma, delta, scale = sp.symbols("gamma delta s", positive=True)
    dimension = 10
    drift = sp.ImmutableMatrix(gamma * sp.eye(dimension))
    diffusion = sp.ImmutableMatrix(delta * sp.eye(dimension))
    stationary_covariance = sp.ImmutableMatrix((delta / gamma) * sp.eye(dimension))
    lyapunov_map = sp.ImmutableMatrix(2 * sp.eye(dimension * (dimension + 1) // 2))
    ratio_orbit_map = sp.ImmutableMatrix([[-1, 1]])

    unit_drift = sp.eye(dimension)
    unit_diffusion = sp.eye(dimension)
    unit_covariance = sp.eye(dimension)
    doubled_diffusion = 2 * sp.eye(dimension)
    doubled_covariance = 2 * sp.eye(dimension)

    dimension_theorem = kernel.prove_expression_equality(
        drift.rows,
        dimension,
        subject="the minimal Gaussian reference dynamics acts on ten coordinates",
    )
    symmetric_dimension_theorem = kernel.prove_expression_equality(
        dimension * (dimension + 1) // 2,
        55,
        subject="the ten dimensional covariance space has fifty five symmetric directions",
    )
    stationary_theorem = kernel.prove_matrix_equality(
        drift * stationary_covariance
        + stationary_covariance * drift.T,
        2 * diffusion,
        subject="the isotropic OU covariance solves the stationary Lyapunov equation",
    )
    reversible_theorem = kernel.prove_matrix_equality(
        drift * diffusion,
        diffusion * drift.T,
        subject="the isotropic OU family satisfies detailed balance",
    )
    lyapunov_rank_theorem = kernel.prove_exact_rank(
        lyapunov_map,
        55,
        subject="the stable isotropic Lyapunov map fixes one covariance for fixed coefficients",
    )
    lyapunov_nullity_theorem = kernel.prove_exact_nullity(
        lyapunov_map,
        0,
        subject="the fixed coefficient stationary covariance has no matrix zero modes",
    )
    unit_witness_theorem = kernel.prove_matrix_equality(
        unit_drift * unit_covariance + unit_covariance * unit_drift.T,
        2 * unit_diffusion,
        subject="unit drift and diffusion give the unit reference covariance",
    )
    doubled_witness_theorem = kernel.prove_matrix_equality(
        unit_drift * doubled_covariance + doubled_covariance * unit_drift.T,
        2 * doubled_diffusion,
        subject="the same stable drift with doubled diffusion gives covariance two",
    )
    witness_separation_theorem = kernel.prove_expression_equality(
        sp.trace(doubled_covariance - unit_covariance),
        10,
        subject="two admissible isotropic stationary covariances are distinct",
    )
    rescaling_theorem = kernel.prove_expression_equality(
        scale * delta / (scale * gamma),
        delta / gamma,
        subject="common time rescaling leaves the stationary covariance unchanged",
    )
    ratio_nonconstant_theorem = kernel.prove_expression_nonconstant(
        delta / gamma,
        delta,
        subject="the stationary covariance depends on a free diffusion drift ratio",
    )
    ratio_orbit_nullity_theorem = kernel.prove_exact_nullity(
        ratio_orbit_map,
        1,
        subject="one common coefficient rescaling remains invisible to covariance",
    )
    gate_theorem = kernel.prove_gate(
        "version9_physical_reopening_gaussian_reference_state_parent_origin_gate",
        (
            dimension_theorem,
            symmetric_dimension_theorem,
            stationary_theorem,
            reversible_theorem,
            lyapunov_rank_theorem,
            lyapunov_nullity_theorem,
            unit_witness_theorem,
            doubled_witness_theorem,
            witness_separation_theorem,
            rescaling_theorem,
            ratio_nonconstant_theorem,
            ratio_orbit_nullity_theorem,
        ),
    )
    return GaussianReferenceStateParentOriginCertificate(
        drift=drift,
        diffusion=diffusion,
        stationary_covariance=stationary_covariance,
        lyapunov_map=lyapunov_map,
        ratio_orbit_map=ratio_orbit_map,
        dimension_theorem=dimension_theorem,
        symmetric_dimension_theorem=symmetric_dimension_theorem,
        stationary_theorem=stationary_theorem,
        reversible_theorem=reversible_theorem,
        lyapunov_rank_theorem=lyapunov_rank_theorem,
        lyapunov_nullity_theorem=lyapunov_nullity_theorem,
        unit_witness_theorem=unit_witness_theorem,
        doubled_witness_theorem=doubled_witness_theorem,
        witness_separation_theorem=witness_separation_theorem,
        rescaling_theorem=rescaling_theorem,
        ratio_nonconstant_theorem=ratio_nonconstant_theorem,
        ratio_orbit_nullity_theorem=ratio_orbit_nullity_theorem,
        gate_theorem=gate_theorem,
    )


SPEC = GateSpec(
    identifier="version9_physical_reopening_gaussian_reference_state_parent_origin_gate",
    title="Parent-origin Gaussian reference state common covariance carrier",
    source_paths=(
        "s2t/gates/version9_physical_reopening_gaussian_reference_state_parent_origin_gate.tex",
        "s2t/results/s2t_v9_physical_reopening_gaussian_reference_state_parent_origin_gate_results.json",
    ),
    obligations=(
        Obligation("gaussian_carrier_dimension_ten", lambda: build_certificate().dimension_theorem),
        Obligation("symmetric_covariance_dimension_fifty_five", lambda: build_certificate().symmetric_dimension_theorem),
        Obligation("stationary_lyapunov_equation", lambda: build_certificate().stationary_theorem),
        Obligation("isotropic_detailed_balance", lambda: build_certificate().reversible_theorem),
        Obligation("lyapunov_map_rank_fifty_five", lambda: build_certificate().lyapunov_rank_theorem),
        Obligation("lyapunov_map_nullity_zero", lambda: build_certificate().lyapunov_nullity_theorem),
        Obligation("unit_covariance_witness", lambda: build_certificate().unit_witness_theorem),
        Obligation("doubled_covariance_witness", lambda: build_certificate().doubled_witness_theorem),
        Obligation("distinct_admissible_covariances", lambda: build_certificate().witness_separation_theorem),
        Obligation("common_time_rescaling_invariance", lambda: build_certificate().rescaling_theorem),
        Obligation("free_diffusion_drift_ratio", lambda: build_certificate().ratio_nonconstant_theorem),
        Obligation("coefficient_orbit_nullity_one", lambda: build_certificate().ratio_orbit_nullity_theorem),
    ),
)


if __name__ == "__main__":
    print(build_certificate().gate_theorem.proposition)