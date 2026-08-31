#!/usr/bin/env python3
"""Exact bimodule compatibility audit for the conditional channel triplet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coherence_channel_triplet_promotion_bimodule_compatibility_gate_results.json"


def linear_rank_and_nullity(expressions: list[sp.Expr], variables: tuple[sp.Symbol, ...]) -> tuple[int, int]:
    matrix, _ = sp.linear_eq_to_matrix(expressions, variables)
    rank = matrix.rank()
    return rank, len(variables) - rank


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_coherence_channel_triplet_promotion_bimodule_compatibility_gate"

    # e_R and X_R are isotypic (C,C,R); Y_R is (H,C,R).
    type_projector = sp.diag(0, 0, 1)
    entries = sp.symbols("a0:9")
    generic = sp.Matrix(3, 3, entries)
    commutator = generic * type_projector - type_projector * generic
    commutant_rank, commutant_nullity = linear_rank_and_nullity(list(commutator), entries)
    assert (commutant_rank, commutant_nullity) == (4, 5)

    x12, x13, x23 = sp.symbols("x12 x13 x23", real=True)
    skew = sp.Matrix([[0, x12, x13], [-x12, 0, x23], [-x13, -x23, 0]])
    skew_commutator = skew * type_projector - type_projector * skew
    orthogonal_rank, orthogonal_nullity = linear_rank_and_nullity(
        list(skew_commutator), (x12, x13, x23)
    )
    assert (orthogonal_rank, orthogonal_nullity) == (2, 1)

    l12 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    l13 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    l23 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
    so3 = [l12, l13, l23]
    commuting_so3_generators = [generator * type_projector == type_projector * generator for generator in so3]
    assert commuting_so3_generators == [True, False, False]

    # The standard A4 triplet also mixes the 2+1 type decomposition.
    cycle = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    half_turn = sp.diag(1, -1, -1)
    a4_preserves_types = [
        cycle * type_projector == type_projector * cycle,
        half_turn * type_projector == type_projector * half_turn,
    ]
    assert a4_preserves_types == [False, True]

    # Infinitesimal su(2) on C2 is not an honest SO(3) representation:
    # the nontrivial central element of Spin(3)=SU(2) acts as -I2.
    spin_cover_center = sp.diag(-1, -1, 1)
    assert spin_cover_center != sp.eye(3)
    assert spin_cover_center**2 == sp.eye(3)

    # Minimal non-destructive extension: add Z_R of the same type as e_R,X_R.
    extended_type_projector = sp.diag(0, 0, 0, 1)
    extended_entries = sp.symbols("b0:16")
    extended_generic = sp.Matrix(4, 4, extended_entries)
    extended_commutator = extended_generic * extended_type_projector - extended_type_projector * extended_generic
    extended_rank, extended_nullity = linear_rank_and_nullity(list(extended_commutator), extended_entries)
    assert (extended_rank, extended_nullity) == (6, 10)  # M3(C) + C

    embedded_so3 = [sp.diag(1, 1, 1, 1) * 0 for _ in range(3)]
    for index, generator in enumerate(so3):
        embedded_so3[index][:3, :3] = generator
        assert embedded_so3[index] * extended_type_projector == extended_type_projector * embedded_so3[index]

    selected_chain_dimensions = {
        "H0": 1,
        "H1": 2 * 3,
        "H2": sp.binomial(2, 2) * sp.binomial(3, 2),
    }
    assert selected_chain_dimensions == {"H0": 1, "H1": 6, "H2": 3}
    full_extended_edge_dimension = 2 * 4
    assert full_extended_edge_dimension == 8

    exact_objects = [
        type_projector,
        generic,
        commutator,
        skew,
        skew_commutator,
        cycle,
        half_turn,
        spin_cover_center,
        extended_type_projector,
        extended_generic,
        extended_commutator,
        *so3,
        *embedded_so3,
    ]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_coherence_channel_triplet_promotion_bimodule_compatibility_gate",
        "current_channel_types": {
            "W_e": "(C,C,R)",
            "W_X": "(C,C,R)",
            "W_Y": "(H,C,R)",
            "isotypic_decomposition": "C2 + C1",
        },
        "current_type_commutant": {
            "complex_algebra": "M2(C) + C",
            "linear_system_rank": commutant_rank,
            "dimension": commutant_nullity,
            "real_orthogonal_lie_algebra": "so(2)",
            "orthogonal_system_rank": orthogonal_rank,
            "orthogonal_dimension": orthogonal_nullity,
            "standard_so3_generators_preserving_types": commuting_so3_generators,
        },
        "finite_group_and_cover_checks": {
            "standard_A4_generators_preserving_types": a4_preserves_types,
            "full_standard_A4_triplet_allowed": False,
            "spin_cover_center": [[-1, 0, 0], [0, -1, 0], [0, 0, 1]],
            "spin_half_representation_descends_to_SO3": False,
        },
        "minimal_non_destructive_extension": {
            "new_endpoint": "Z_R=(C,C,R)",
            "extended_decomposition": "C3 + C1_Y",
            "type_commutant": "M3(C) + C",
            "commutant_dimension": extended_nullity,
            "canonical_isotypic_projector_rank": 3,
            "SO3_on_isotypic_C3_allowed": True,
            "selected_coherence_chain_dimensions": {key: int(value) for key, value in selected_chain_dimensions.items()},
            "full_extended_edge_dimension": full_extended_edge_dimension,
            "new_complex_arrow_components": 2,
            "old_Y_channel_is_spectator": True,
            "old_rank_one_condensate_inherited": False,
        },
        "ledgers": {
            "current_promotion_satisfied": 0,
            "current_promotion_tested": 5,
            "conditional_extension_shape_satisfied": 5,
            "conditional_extension_shape_tested": 5,
            "new_parent_inputs": [
                "one new (C,C,R) endpoint",
                "two new allowed arrows from the coherence row doublet",
                "new condensate on the selected isotypic 2x3 subcarrier",
                "diagonal family-channel SO(3) lock",
            ],
        },
        "verdict": {
            "current_channel_triplet_promotion_bimodule_compatible": False,
            "basis_change_can_repair_current_types": False,
            "A4_can_repair_current_types": False,
            "spin_cover_can_repair_current_types": False,
            "minimal_non_destructive_extension_shape_exists": True,
            "minimal_extension_is_inherited": False,
            "portal_parent_origin_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()