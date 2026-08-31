"""Clock-augmented static history Hamiltonian for the balanced conveyor."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_static_local_hamiltonian_embedding_no_go import build_certificate as build_static


@dataclass(frozen=True, slots=True)
class ClockAugmentedConveyorCertificate:
    transfer_theorem: Theorem
    execution_theorem: Theorem
    locality_theorem: Theorem
    boundary_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> ClockAugmentedConveyorCertificate:
    static = build_static()
    transfer = kernel.prove_three_site_history_clock_transfer(
        static.carrier_boundary_theorem,
        subject="three-state perfect-transfer clock for the two-layer conveyor word",
    )
    execution = kernel.prove_dressed_history_word_execution(
        transfer,
        subject="one-shot static execution of W1 W0 on a finite history carrier",
    )
    locality = kernel.prove_history_clock_uniform_locality_boundary(
        execution,
        subject="local serialisation and bounded-strength scaling on a ring of length L",
    )
    boundary = kernel.prove_clock_augmented_conveyor_boundary(
        locality,
        subject="finite-history success versus thermodynamic autonomous-conveyor closure",
    )
    gate = kernel.prove_gate(
        "clock_augmented_static_hamiltonian_conveyor",
        (transfer, execution, locality, boundary),
    )
    return ClockAugmentedConveyorCertificate(transfer, execution, locality, boundary, gate)