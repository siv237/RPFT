"""Exact scale-orbit certificate for the full 42-jump collision model."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_noise_repeated_interaction import build_certificate as build_star


@dataclass(frozen=True, slots=True)
class FullNoisePhysicalTimeScaleCertificate:
    coupling_scale: sp.Symbol
    physical_time: sp.Symbol
    energy_scale: sp.Symbol
    hbar: sp.Symbol
    rate_scale_theorem: Theorem
    orbit_invariance_theorem: Theorem
    coupling_freedom_theorem: Theorem
    energy_time_theorem: Theorem
    energy_anchor_theorem: Theorem
    physical_time_no_go_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FullNoisePhysicalTimeScaleCertificate:
    star = build_star()
    g = sp.Symbol("g", positive=True)
    t = sp.Symbol("t_phys", positive=True)
    energy = sp.Symbol("E_*", positive=True)
    hbar = sp.Symbol("hbar", positive=True)

    rate_scale = kernel.prove_expression_equality(
        (g * g),
        g**2,
        subject="quadratic scaling of the weak-collision GKSL tangent",
    )
    orbit = kernel.prove_expression_equality(
        g**2 * (t / g**2),
        t,
        subject="invariance of the dimensionless semigroup parameter",
    )
    coupling_freedom = kernel.prove_expression_nonconstant(
        g**2,
        g,
        subject="the full 42-jump decay rate depends on the free coupling scale",
    )
    energy_time = kernel.prove_expression_equality(
        energy * (hbar / energy),
        hbar,
        subject="energy-time calibration identity",
    )
    energy_anchor = kernel.prove_expression_nonconstant(
        hbar / energy,
        energy,
        subject="a physical time unit requires an independently fixed energy scale",
    )
    no_go = kernel.prove_collision_physical_time_scale_no_go(
        star.star_theorem,
        g,
        t,
        energy,
        hbar,
        subject="absolute physical time scale of the full 42-jump collision model",
        premises=(rate_scale, orbit, coupling_freedom, energy_time, energy_anchor),
    )
    gate = kernel.prove_gate(
        "full_noise_physical_time_scale_no_go",
        (rate_scale, orbit, coupling_freedom, energy_time, energy_anchor, no_go),
    )
    return FullNoisePhysicalTimeScaleCertificate(
        g,
        t,
        energy,
        hbar,
        rate_scale,
        orbit,
        coupling_freedom,
        energy_time,
        energy_anchor,
        no_go,
        gate,
    )


if __name__ == "__main__":
    print(build_certificate().physical_time_no_go_theorem.proposition)