"""Joint autonomous-clock and repeated-interaction continuum limit."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_bounded_strength_autonomous_clock_thermodynamic_limit import (
    build_certificate as build_clock_limit,
)
from .version8_full_noise_physical_time_scale import (
    build_certificate as build_time_scale,
)
from .version8_full_noise_repeated_interaction import (
    build_certificate as build_repeated_interaction,
)


@dataclass(frozen=True, slots=True)
class LocalClockedQMSCertificate:
    error_theorem: Theorem
    joint_limit_theorem: Theorem
    reduced_limit_theorem: Theorem
    time_boundary_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> LocalClockedQMSCertificate:
    clock = build_clock_limit()
    time_scale = build_time_scale()
    collision = build_repeated_interaction().collision_limit_theorem

    error = kernel.prove_clocked_collision_error_decomposition(
        clock.local_limit_theorem,
        collision,
        subject="clock-controlled repeated-interaction error on reduced observables",
    )
    joint_limit = kernel.prove_joint_clock_collision_continuum_limit(
        error,
        subject="joint logarithmic-clock and weak-collision continuum limit",
    )
    reduced_limit = kernel.prove_clocked_reduced_observable_limit(
        joint_limit,
        subject="local observable QMS recovered from the autonomous conveyor",
    )
    time_boundary = kernel.prove_clocked_qms_common_time_scale_boundary(
        reduced_limit,
        time_scale.physical_time_no_go_theorem,
        subject="common scale orbit of the autonomous clock and dissipative rate",
    )
    gate = kernel.prove_gate(
        "local_observable_clocked_qms_limit_and_time_anchor",
        (error, joint_limit, reduced_limit, time_boundary),
    )
    return LocalClockedQMSCertificate(
        error,
        joint_limit,
        reduced_limit,
        time_boundary,
        gate,
    )