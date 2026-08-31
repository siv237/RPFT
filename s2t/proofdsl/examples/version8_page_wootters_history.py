"""Finite Page--Wootters/Stinespring history for the exact cross channel."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..history import KrausHistory
from ..kernel import Theorem, kernel
from .version8_noise_clock import build_certificate as build_noise_clock_certificate
from .version8_stinespring import benchmark_channel, build_certificate as build_stinespring_certificate


@dataclass(frozen=True, slots=True)
class PageWoottersHistoryCertificate:
    steps: int
    clock_dimension: int
    system_dimension: int
    environment_dimension_per_tick: int
    branch_count_bounds: tuple[int, ...]
    padded_data_dimension: int
    full_history_dimension: int
    recovery_theorem: Theorem
    history_parent_theorem: Theorem
    extension_freedom_theorem: Theorem
    collision_limit_theorem: Theorem
    physical_clock_no_go_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> PageWoottersHistoryCertificate:
    channel = benchmark_channel()
    steps = 2
    initial = sp.zeros(21)
    initial[0, 0] = 1
    history = KrausHistory("two_tick_cross_history", channel, initial, steps)

    recovery = kernel.prove_kraus_history_recovery(
        history,
        subject="conditional clock slices recover Phi^n for n=0,1,2",
    )
    parent = kernel.prove_isometric_history_parent(
        history,
        recovery,
        subject="frustration-free finite Stinespring history parent",
    )
    freedom = kernel.prove_stinespring_unitary_extension_freedom(
        channel.space.dimension,
        len(channel.kraus),
        subject="nonuniqueness of a full autonomous unitary clock step",
    )

    noise_clock = build_noise_clock_certificate()
    collision = noise_clock.collision_limit_theorem
    stinespring = build_stinespring_certificate()
    no_go = kernel.prove_gate(
        "page_wootters_physical_clock_boundary",
        (
            stinespring.semigroup_no_go_theorem,
            freedom,
            noise_clock.rate_scaling_theorem,
        ),
    )

    environment_dimension = len(channel.kraus)
    padded_data_dimension = channel.space.dimension * environment_dimension**steps
    full_history_dimension = history.clock_dimension * padded_data_dimension
    return PageWoottersHistoryCertificate(
        steps=steps,
        clock_dimension=history.clock_dimension,
        system_dimension=channel.space.dimension,
        environment_dimension_per_tick=environment_dimension,
        branch_count_bounds=tuple(history.branch_count(step) for step in range(steps + 1)),
        padded_data_dimension=padded_data_dimension,
        full_history_dimension=full_history_dimension,
        recovery_theorem=recovery,
        history_parent_theorem=parent,
        extension_freedom_theorem=freedom,
        collision_limit_theorem=collision,
        physical_clock_no_go_theorem=no_go,
    )


if __name__ == "__main__":
    print(build_certificate())