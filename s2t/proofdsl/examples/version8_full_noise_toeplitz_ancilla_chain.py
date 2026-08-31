"""Toeplitz-shift ancilla chain for the full 42-jump collision model."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..kernel import Theorem, kernel
from .version8_full_noise_repeated_interaction import build_certificate as build_star


@dataclass(frozen=True, slots=True)
class FullNoiseToeplitzAncillaChainCertificate:
    system_dimension: int
    jump_dimension: int
    cell_dimension: int
    counter_theorem: Theorem
    cell_dimension_theorem: Theorem
    chain_theorem: Theorem
    recovery_theorem: Theorem
    gauge_theorem: Theorem
    collision_limit_theorem: Theorem
    resource_boundary_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FullNoiseToeplitzAncillaChainCertificate:
    star = build_star()
    n = sp.Symbol("n", integer=True)
    k = sp.Symbol("k", integer=True)
    counter = kernel.prove_bilateral_shift_counter(
        n,
        k,
        subject="Toeplitz number operator counts absolute ancilla-chain shifts",
    )
    cell_dimension = kernel.prove_expression_equality(
        star.environment_dimension,
        1 + star.jump_dimension,
        subject="one vacuum plus 42 full-noise labels gives a 43-dimensional cell",
    )
    chain = kernel.prove_toeplitz_ancilla_chain_dilation(
        star.star_theorem,
        counter,
        star.closure_theorem,
        subject="bilateral Toeplitz conveyor of full-noise vacuum ancillas",
    )
    recovery = kernel.prove_ancilla_chain_reduced_iteration(
        chain,
        subject="the autonomous chain recovers every finite iterate Phi_h^n",
    )
    boundary = kernel.prove_ancilla_chain_resource_boundary(
        chain,
        subject="preloaded-vacuum and continuous-Hamiltonian boundary of chain autonomy",
    )
    gate = kernel.prove_gate(
        "full_noise_toeplitz_ancilla_chain_dilation",
        (
            counter,
            cell_dimension,
            chain,
            recovery,
            star.closure_theorem,
            star.collision_limit_theorem,
            boundary,
        ),
    )
    return FullNoiseToeplitzAncillaChainCertificate(
        star.system_dimension,
        star.jump_dimension,
        star.environment_dimension,
        counter,
        cell_dimension,
        chain,
        recovery,
        star.closure_theorem,
        star.collision_limit_theorem,
        boundary,
        gate,
    )


if __name__ == "__main__":
    print(build_certificate().chain_theorem.proposition)