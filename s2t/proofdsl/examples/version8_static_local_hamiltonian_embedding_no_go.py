"""Static minimal-carrier Hamiltonian no-go for the balanced conveyor."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from ..kernel import Theorem, kernel
from .version8_index_balanced_ancilla_conveyor import build_certificate as build_balanced


@dataclass(frozen=True, slots=True)
class StaticLocalHamiltonianEmbeddingNoGoCertificate:
    active_winding: int
    spectator_winding: int
    determinant_winding: int
    winding_theorem: Theorem
    static_no_go_theorem: Theorem
    carrier_boundary_theorem: Theorem
    full_gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> StaticLocalHamiltonianEmbeddingNoGoCertificate:
    balanced = build_balanced()
    winding = kernel.prove_balanced_conveyor_bloch_winding(
        balanced.swap_circuit_theorem,
        subject="Bloch eigenchannel windings of the balanced 43-by-43 conveyor",
    )
    no_go = kernel.prove_static_periodic_two_band_logarithm_no_go(
        winding,
        subject="static finite-range number-preserving logarithm on the minimal two-chain carrier",
    )
    boundary = kernel.prove_static_conveyor_carrier_boundary(
        no_go,
        subject="scope boundary between the minimal Bloch no-go and enlarged clock carriers",
    )
    gate = kernel.prove_gate(
        "static_local_hamiltonian_embedding_or_no_go",
        (winding, no_go, boundary),
    )
    data = winding.proposition.data
    return StaticLocalHamiltonianEmbeddingNoGoCertificate(
        int(data["active_eigenvalue_winding"]),
        int(data["spectator_eigenvalue_winding"]),
        int(data["determinant_winding"]),
        winding,
        no_go,
        boundary,
        gate,
    )


if __name__ == "__main__":
    print(build_certificate().static_no_go_theorem.proposition)