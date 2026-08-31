"""No-go certificate for a canonical autonomous unitary clock extension."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_page_wootters_history import build_certificate as build_history_certificate
from .version8_stinespring import benchmark_channel, build_certificate as build_stinespring_certificate


@dataclass(frozen=True, slots=True)
class AutonomousClockUnitaryCertificate:
    system_dimension: int
    environment_dimension: int
    complement_dimension: int
    extension_parameter_dimension: int
    real_even_extension_count_lower_bound: int
    minimal_environment_theorem: Theorem
    covariance_theorem: Theorem
    ambiguity_theorem: Theorem
    autonomous_clock_no_go_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> AutonomousClockUnitaryCertificate:
    channel = benchmark_channel()
    stinespring = build_stinespring_certificate()
    history = build_history_certificate()
    ambiguity = kernel.prove_covariant_stinespring_extension_ambiguity(
        channel,
        stinespring.covariance_theorem,
        subject="gauge-covariant complement phases preserve the same clock channel",
    )
    no_go = kernel.prove_gate(
        "canonical_autonomous_clock_unitary_no_go",
        (
            history.history_parent_theorem,
            ambiguity,
            history.physical_clock_no_go_theorem,
        ),
    )
    return AutonomousClockUnitaryCertificate(
        system_dimension=channel.space.dimension,
        environment_dimension=len(channel.kraus),
        complement_dimension=252,
        extension_parameter_dimension=252**2,
        real_even_extension_count_lower_bound=2,
        minimal_environment_theorem=stinespring.minimal_environment_theorem,
        covariance_theorem=stinespring.covariance_theorem,
        ambiguity_theorem=ambiguity,
        autonomous_clock_no_go_theorem=no_go,
    )


if __name__ == "__main__":
    print(build_certificate())