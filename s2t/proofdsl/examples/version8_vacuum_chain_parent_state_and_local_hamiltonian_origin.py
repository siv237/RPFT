"""Vacuum-chain parent and local-Hamiltonian origin test for Tome VIII."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_full_noise_toeplitz_ancilla_chain import (
    build_certificate as build_chain,
)


@dataclass(frozen=True, slots=True)
class VacuumChainParentAndHamiltonianOriginCertificate:
    cell_dimension: int
    excitation_dimension: int
    parent_theorem: Theorem
    shift_index_theorem: Theorem
    global_index_theorem: Theorem
    local_hamiltonian_no_go_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> VacuumChainParentAndHamiltonianOriginCertificate:
    chain = build_chain()
    parent = kernel.prove_product_vacuum_parent_hamiltonian(
        chain.chain_theorem,
        subject="commuting-projector parent of the 43-state ancilla vacuum chain",
    )
    shift_index = kernel.prove_ancilla_shift_gnvw_index(
        chain.chain_theorem,
        subject="GNVW information-flow index of the one-cell ancilla translation",
    )
    global_index = kernel.prove_finite_collision_preserves_chain_index(
        chain.chain_theorem,
        shift_index,
        subject="the local collision does not cancel the conveyor index",
    )
    no_go = kernel.prove_local_hamiltonian_ancilla_shift_no_go(
        parent,
        global_index,
        subject="local-Hamiltonian origin of the exact Toeplitz ancilla conveyor",
    )
    gate = kernel.prove_gate(
        "vacuum_chain_parent_state_and_local_hamiltonian_origin",
        (parent, shift_index, global_index, no_go),
    )
    return VacuumChainParentAndHamiltonianOriginCertificate(
        chain.cell_dimension,
        chain.cell_dimension - 1,
        parent,
        shift_index,
        global_index,
        no_go,
        gate,
    )


if __name__ == "__main__":
    print(build_certificate().local_hamiltonian_no_go_theorem.proposition)