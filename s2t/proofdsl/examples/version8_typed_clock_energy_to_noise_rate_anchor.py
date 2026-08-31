"""Typed dimensional bridge from clock energy to the full-noise rate."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_local_observable_clocked_qms_limit_and_time_anchor import (
    build_certificate as build_clocked_qms,
)


@dataclass(frozen=True, slots=True)
class TypedClockEnergyAnchorCertificate:
    rate_identity_theorem: Theorem
    relative_calibration_theorem: Theorem
    underdetermination_theorem: Theorem
    anchor_no_go_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> TypedClockEnergyAnchorCertificate:
    previous = build_clocked_qms()
    rate_identity = kernel.prove_typed_clock_collision_rate_identity(
        previous.time_boundary_theorem,
        subject="dimensional collision rate measured by an autonomous clock",
    )
    calibration = kernel.prove_clock_rate_relative_calibration(
        rate_identity,
        subject="relative calibration of the dissipative rate to the clock frequency",
    )
    underdetermination = kernel.prove_clock_interaction_scale_underdetermination(
        calibration,
        subject="independent dimensionless clock-interaction coupling",
    )
    no_go = kernel.prove_typed_clock_energy_anchor_no_go(
        underdetermination,
        subject="absence of a typed dimensional clock-energy anchor in the current parent",
    )
    gate = kernel.prove_gate(
        "typed_clock_energy_to_noise_rate_anchor",
        (rate_identity, calibration, underdetermination, no_go),
    )
    return TypedClockEnergyAnchorCertificate(
        rate_identity, calibration, underdetermination, no_go, gate
    )