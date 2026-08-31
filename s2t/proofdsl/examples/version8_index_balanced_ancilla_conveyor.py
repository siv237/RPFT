"""Index-balanced two-chain ancilla conveyor for Tome VIII."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_full_noise_toeplitz_ancilla_chain import build_certificate as build_chain
from .version8_vacuum_chain_parent_state_and_local_hamiltonian_origin import (
    build_certificate as build_origin,
)


@dataclass(frozen=True, slots=True)
class IndexBalancedAncillaConveyorCertificate:
    cell_dimension: int
    total_index: int
    counterflow_theorem: Theorem
    swap_circuit_theorem: Theorem
    local_hamiltonian_theorem: Theorem
    recovery_theorem: Theorem
    autonomy_boundary_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> IndexBalancedAncillaConveyorCertificate:
    chain = build_chain()
    origin = build_origin()
    counterflow = kernel.prove_index_balanced_ancilla_counterflow(
        origin.shift_index_theorem,
        subject="opposite information flow on two equal 43-state ancilla chains",
    )
    circuit = kernel.prove_two_layer_swap_counterflow_circuit(
        counterflow,
        subject="nearest-neighbour two-layer SWAP realization of the balanced conveyor",
    )
    hamiltonian = kernel.prove_swap_layers_have_local_hamiltonians(
        circuit,
        subject="piecewise local Hamiltonian generation of both SWAP layers",
    )
    recovery = kernel.prove_balanced_conveyor_reduced_iteration(
        chain.recovery_theorem,
        circuit,
        subject="full-noise channel iteration with a spectator inverse-flow chain",
    )
    boundary = kernel.prove_balanced_conveyor_autonomy_boundary(
        hamiltonian,
        recovery,
        subject="stationary-autonomy boundary after GNVW index cancellation",
    )
    gate = kernel.prove_gate(
        "index_balanced_ancilla_conveyor",
        (counterflow, circuit, hamiltonian, recovery, boundary),
    )
    return IndexBalancedAncillaConveyorCertificate(
        chain.cell_dimension,
        int(counterflow.proposition.data["total_multiplicative_index"]),
        counterflow,
        circuit,
        hamiltonian,
        recovery,
        boundary,
        gate,
    )


if __name__ == "__main__":
    print(build_certificate().autonomy_boundary_theorem.proposition)