#!/usr/bin/env python3
"""Exact intertwiner audit for the coherence even corner and family triplet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate_results.json"

PAIRS = ((0, 1), (0, 2), (1, 2))


def wedge_representation(generator: sp.Matrix) -> sp.Matrix:
    result = sp.zeros(3)
    for column, (i, j) in enumerate(PAIRS):
        for a in range(3):
            coefficient = generator[a, i]
            if coefficient and a != j:
                pair = tuple(sorted((a, j)))
                result[PAIRS.index(pair), column] += (1 if a < j else -1) * coefficient
        for a in range(3):
            coefficient = generator[a, j]
            if coefficient and i != a:
                pair = tuple(sorted((i, a)))
                result[PAIRS.index(pair), column] += (1 if i < a else -1) * coefficient
    return result


def system_rank(generators: list[tuple[sp.Matrix, sp.Matrix]]) -> tuple[int, int]:
    variables = sp.symbols("z0:9")
    z = sp.Matrix(3, 3, variables)
    equations = []
    for target, source in generators:
        equations.extend(list(target * z - z * source))
    matrix, _ = sp.linear_eq_to_matrix(equations, variables)
    return matrix.rank(), 9 - matrix.rank()


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_edge_coherence_radius_portal_parent_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate"

    l12 = sp.Matrix([[0, 1, 0], [-1, 0, 0], [0, 0, 0]])
    l13 = sp.Matrix([[0, 0, 1], [0, 0, 0], [-1, 0, 0]])
    l23 = sp.Matrix([[0, 0, 0], [0, 0, 1], [0, -1, 0]])
    so3 = [l12, l13, l23]

    # Currently the coherence corner has no declared family action.
    current_family_rank, current_family_nullity = system_rank(
        [(generator, sp.zeros(3)) for generator in so3]
    )
    assert (current_family_rank, current_family_nullity) == (9, 0)

    # The A4 residual also has no invariant vector in its standard triplet.
    cycle = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    half_turn = sp.diag(1, -1, -1)
    a4_rank, a4_nullity = system_rank(
        [(cycle - sp.eye(3), sp.zeros(3)), (half_turn - sp.eye(3), sp.zeros(3))]
    )
    assert (a4_rank, a4_nullity) == (9, 0)

    # Conversely, the family target is trivial under the physical channel group,
    # while Lambda^2(C2+C1)=C1+C2 has no invariant quotient of the required type.
    channel_generators = []
    for i, j in ((0, 0), (0, 1), (1, 0), (1, 1), (2, 2)):
        unit = sp.zeros(3)
        unit[i, j] = 1
        channel_generators.append(wedge_representation(unit))
    channel_rank, channel_nullity = system_rank(
        [(sp.zeros(3), generator) for generator in channel_generators]
    )
    assert (channel_rank, channel_nullity) == (9, 0)

    # Conditional diagonal SO(3): promote W to an oriented standard triplet.
    wedge_so3 = [wedge_representation(generator) for generator in so3]
    promoted_rank, promoted_nullity = system_rank(list(zip(so3, wedge_so3)))
    assert (promoted_rank, promoted_nullity) == (8, 1)
    hodge_star = sp.Matrix([[0, 0, 1], [0, -1, 0], [1, 0, 0]])
    for target, source in zip(so3, wedge_so3):
        assert target * hodge_star - hodge_star * source == sp.zeros(3)
    assert hodge_star.T * hodge_star == sp.eye(3)
    assert hodge_star.det() == 1

    scale = sp.symbols("c", real=True)
    scaled = scale * hodge_star
    assert scaled.T * scaled == scale**2 * sp.eye(3)
    normalized_scales = sp.solve(sp.Eq(scale**2, 1), scale)
    assert normalized_scales == [-1, 1]

    exact_objects = so3 + wedge_so3 + channel_generators + [hodge_star, scaled]
    assert not any(item.atoms(sp.Float) for item in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_coherence_even_corner_family_triplet_intertwiner_gate",
        "current_representations": {
            "coherence_corner": "Lambda^2(C2+C1)=C1+C2 under U(2)_{eX} x U(1)_Y; family action trivial",
            "family_target": "standard irreducible 3 of SO(3)_fam; channel action trivial",
            "product_group": "(U(2)_{eX} x U(1)_Y) x SO(3)_fam",
        },
        "current_intertwiner_systems": {
            "family_SO3_rank": current_family_rank,
            "family_SO3_nullity": current_family_nullity,
            "family_A4_rank": a4_rank,
            "family_A4_nullity": a4_nullity,
            "channel_rank": channel_rank,
            "channel_nullity": channel_nullity,
            "full_product_group_Hom_dimension": 0,
        },
        "conditional_promotion": {
            "new_channel_type": "oriented standard R3 of a diagonal SO(3)",
            "source": "Lambda^2 R3",
            "target": "R3",
            "intertwiner_system_rank": promoted_rank,
            "Hom_dimension": promoted_nullity,
            "canonical_shape": "Hodge star from the oriented metric",
            "matrix": [[0, 0, 1], [0, -1, 0], [1, 0, 0]],
            "isometry": True,
            "determinant": 1,
            "normalized_maps": ["-*", "+*"],
        },
        "typing_cost": {
            "mixes_W_e_W_X_W_Y": True,
            "current_W_bimodule_types_equal": False,
            "accidental_U3_promoted_to_physical": True,
            "diagonal_family_channel_lock_required": True,
            "orientation_sign_requires_origin": True,
        },
        "ledgers": {
            "current_intertwiner_satisfied": 0,
            "current_intertwiner_tested": 4,
            "conditional_shape_satisfied": 4,
            "conditional_shape_tested": 4,
            "new_parent_inputs": ["unified channel bimodule", "diagonal SO(3) lock", "oriented metric/sign"],
        },
        "verdict": {
            "current_nonzero_intertwiner_exists": False,
            "A4_residual_repairs_intertwiner": False,
            "conditional_Hodge_intertwiner_exists": True,
            "conditional_intertwiner_unique_up_to_scale": True,
            "conditional_intertwiner_is_currently_typed": False,
            "portal_parent_origin_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_coherence_channel_triplet_promotion_bimodule_compatibility_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()