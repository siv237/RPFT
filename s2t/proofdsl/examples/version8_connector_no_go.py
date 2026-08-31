"""Exact LCF certificate for the Tome VIII endpoint/transfer rank no-go."""

from __future__ import annotations

from dataclasses import dataclass

from ..kernel import Theorem, kernel
from ..structures import (
    Irrep,
    IsotypicBlock,
    SemisimpleRepresentation,
    Space,
    intertwiner_profile,
)


GROUP = "SU(3)xSU(2)xU(1)"


@dataclass(frozen=True, slots=True)
class Version8ConnectorCertificate:
    endpoint: SemisimpleRepresentation
    transfer: SemisimpleRepresentation
    hom_dimension: int
    maximum_rank: int
    theorem: Theorem


def build_certificate() -> Version8ConnectorCertificate:
    ql = Irrep(GROUP, "(3,2)_{1/6}", 6)
    triplet_two_thirds = Irrep(GROUP, "(3,1)_{2/3}", 3)
    triplet_minus_third = Irrep(GROUP, "(3,1)_{-1/3}", 3)
    doublet_minus_half = Irrep(GROUP, "(1,2)_{-1/2}", 2)
    singlet_minus_one = Irrep(GROUP, "(1,1)_{-1}", 1)
    doublet_plus_half = Irrep(GROUP, "(1,2)_{1/2}", 2)
    anti_triplet_minus_two_thirds = Irrep(GROUP, "(bar3,1)_{-2/3}", 3)
    singlet_zero = Irrep(GROUP, "(1,1)_0", 1)

    endpoint_space = Space("E_t+E_s", 21)
    transfer_space = Space("T_bimod", 20)
    endpoint = SemisimpleRepresentation(
        "endpoint_representation",
        endpoint_space,
        (
            IsotypicBlock(ql),
            IsotypicBlock(triplet_two_thirds),
            IsotypicBlock(triplet_minus_third),
            IsotypicBlock(doublet_minus_half, 3),
            IsotypicBlock(singlet_minus_one, 3),
        ),
    )
    transfer = SemisimpleRepresentation(
        "transfer_representation",
        transfer_space,
        (
            IsotypicBlock(doublet_plus_half),
            IsotypicBlock(doublet_minus_half, 4),
            IsotypicBlock(triplet_two_thirds),
            IsotypicBlock(anti_triplet_minus_two_thirds),
            IsotypicBlock(singlet_zero, 4),
        ),
    )
    profile = intertwiner_profile(endpoint, transfer)
    theorem = kernel.prove_intertwiner_rank_no_go(
        profile,
        requested_rank=20,
        subject="no full-rank covariant connector E_t+E_s -> T_bimod",
    )
    return Version8ConnectorCertificate(
        endpoint,
        transfer,
        profile.hom_dimension,
        profile.maximum_rank,
        theorem,
    )


if __name__ == "__main__":
    certificate = build_certificate()
    print(f"Hom_G dimension: {certificate.hom_dimension}")
    print(f"maximum rank: {certificate.maximum_rank}")
    print(certificate.theorem.proposition)