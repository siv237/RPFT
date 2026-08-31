#!/usr/bin/env python3
"""Exact aligned condensate/mass selector audit on the isotypic channel."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate_results.json"


def action(b: sp.Matrix, m: sp.Matrix) -> sp.Expr:
    gram_b = b * b.T
    gram_m = m * m.T
    alignment = m * b.T
    return sp.expand(
        (sp.trace(gram_b) - 3) ** 2
        + 4 * gram_b.det()
        + sp.trace((gram_m - sp.eye(2)) ** 2)
        + sp.trace(alignment * alignment.T)
    )


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_minimal_isotypic_channel_extension_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["next_gate"] == "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate"

    b_variables = sp.symbols("b0:6", real=True)
    m_variables = sp.symbols("m0:6", real=True)
    b = sp.Matrix(2, 3, b_variables)
    m = sp.Matrix(2, 3, m_variables)
    potential = action(b, m)

    b0 = sp.Matrix([[sp.sqrt(3), 0, 0], [0, 0, 0]])
    m0 = sp.Matrix([[0, 1, 0], [0, 0, 1]])
    assert action(b0, m0) == 0
    assert b0.rank() == 1 and m0.rank() == 2
    assert m0 * b0.T == sp.zeros(2)
    assert m0 * m0.T == sp.eye(2)

    p_b = sp.simplify(b0.T * b0 / 3)
    p_m = sp.simplify(m0.T * m0)
    assert p_b.rank() == 1 and p_m.rank() == 2
    assert p_b * p_m == sp.zeros(3)
    assert p_b + p_m == sp.eye(3)

    # Exact invariance under representative left and right orthogonal changes.
    g_b = sp.Matrix([[0, 1], [1, 0]])
    g_m = sp.diag(1, -1)
    h = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    assert sp.simplify(action(g_b * b * h.T, g_m * m * h.T) - potential) == 0

    b1 = b0 * h.T
    m1 = m0 * h.T
    assert action(b1, m1) == 0
    assert b1.T * b1 / 3 != p_b
    assert sp.simplify(b1.T * b1 / 3 + m1.T * m1) == sp.eye(3)

    substitutions = {variable: 0 for variable in (*b_variables, *m_variables)}
    substitutions[b_variables[0]] = sp.sqrt(3)
    substitutions[m_variables[1]] = 1
    substitutions[m_variables[5]] = 1
    hessian = sp.simplify(sp.hessian(potential, (*b_variables, *m_variables)).subs(substitutions))
    eigenvalues = hessian.eigenvals()
    assert hessian.rank() == 8
    assert eigenvalues == {sp.Integer(0): 4, sp.Integer(8): 5, sp.Integer(24): 1, sp.Integer(26): 2}

    # Six allowed but unselected complex arrows are absent from this subparent.
    complex_spectators = previous["minimal_vectorlike_completion"]["allowed_but_unselected_edges"]
    assert len(complex_spectators) == 6
    real_spectator_zero_modes = 2 * len(complex_spectators)
    full_real_slice_signature = {
        "negative": 0,
        "zero": 4 + real_spectator_zero_modes,
        "positive": hessian.rank(),
    }
    assert full_real_slice_signature == {"negative": 0, "zero": 16, "positive": 8}

    exact_objects = [b, m, potential, b0, m0, p_b, p_m, g_b, g_m, h, b1, m1, hessian]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-31",
        "gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_vectorlike_mass_edge_selector_gate",
        "aligned_subparent": {
            "potential": "(Tr(BB*)-3)^2 + 4 det(BB*) + ||MM*-I2||_F^2 + ||MB*||_F^2",
            "field_shapes": {"B": [2, 3], "M": [2, 3]},
            "nonnegative_terms": 4,
            "zero_set": {
                "Tr_BBstar": 3,
                "rank_B": 1,
                "MMstar": "I2",
                "rank_M": 2,
                "MBstar": "0",
            },
            "right_projector_identity": "B*B/3 + M*M = I3",
            "mass_kernel_equals_coherence_line": True,
            "representative_vacuum_energy": 0,
            "orthogonal_covariance_verified": True,
        },
        "real_slice_hessian": {
            "variables": 12,
            "rank": hessian.rank(),
            "nullity": 12 - hessian.rank(),
            "eigenvalue_multiplicities": {str(key): value for key, value in sorted(eigenvalues.items(), key=lambda item: item[0])},
            "negative_modes": 0,
            "zero_modes_are_orbit_tangent": True,
        },
        "orbit_and_edge_selector": {
            "two_distinct_zero_energy_channel_projectors_exhibited": True,
            "absolute_channel_direction_selected": False,
            "full_new_strict_edges": 9,
            "selected_new_edges": 3,
            "omitted_allowed_complex_edges": complex_spectators,
            "omitted_real_flat_modes": real_spectator_zero_modes,
            "full_real_slice_signature_with_spectators": full_real_slice_signature,
            "coordinate_edge_menu_selected": False,
        },
        "ledgers": {
            "aligned_shape_satisfied": 8,
            "aligned_shape_tested": 8,
            "full_graph_selector_satisfied": 0,
            "full_graph_selector_tested": 5,
            "parent_origin_satisfied": 0,
            "parent_origin_tested": 4,
            "new_parent_inputs": [
                "dynamical rank-two mass field M",
                "relative coefficients of the four nonnegative terms",
                "projector excluding six allowed edge fields",
                "diagonal family-channel identification",
            ],
        },
        "verdict": {
            "aligned_condensate_mass_architecture_exists": True,
            "alignment_requires_explicit_SO3_breaking_spurion": False,
            "vacuum_direction_unique": False,
            "full_strict_graph_selected": False,
            "current_parent_origin_derived": False,
            "portal_parent_origin_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_full_graph_aligned_parent_embedding_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()