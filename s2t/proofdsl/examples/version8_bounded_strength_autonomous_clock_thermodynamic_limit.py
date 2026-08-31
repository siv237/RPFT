"""Resource boundary for bounded-strength autonomous clocks."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_clock_augmented_static_hamiltonian_conveyor import (
    build_certificate as build_clock_augmented,
)


@dataclass(frozen=True, slots=True)
class BoundedStrengthClockCertificate:
    finite_volume_theorem: Theorem
    resource_schedule_theorem: Theorem
    global_boundary_theorem: Theorem
    local_limit_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> BoundedStrengthClockCertificate:
    previous = build_clock_augmented()
    finite_volume = kernel.prove_quasi_ideal_clock_finite_volume_error(
        previous.boundary_theorem,
        subject="finite-volume autonomous approximation by a quasi-ideal clock",
    )
    resource_schedule = kernel.prove_logarithmic_clock_resource_schedule(
        finite_volume,
        subject="clock dimension and energy sufficient for a target global error",
    )
    global_boundary = kernel.prove_fixed_clock_global_uniformity_boundary(
        resource_schedule,
        subject="global channel-norm thermodynamic boundary at fixed clock size",
    )
    local_limit = kernel.prove_local_observable_clock_limit_admission(
        global_boundary,
        subject="finite-support observable limit inside a bounded causal cone",
    )
    gate = kernel.prove_gate(
        "bounded_strength_autonomous_clock_thermodynamic_limit",
        (finite_volume, resource_schedule, global_boundary, local_limit),
    )
    return BoundedStrengthClockCertificate(
        finite_volume,
        resource_schedule,
        global_boundary,
        local_limit,
        gate,
    )