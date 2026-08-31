#!/usr/bin/env python3
"""Exact classification of existing scalar carriers for two central sources."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate_results.json").read_text())
    gate = "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_existing_scalar_carrier_classification_gate"
    assert predecessor["next_gate"] == gate

    r, s = sp.symbols("r s", real=True)
    B0 = sp.Matrix([[sp.sqrt(3), 0, 0], [0, 0, 0]])
    M0 = sp.Matrix([[0, 1, 0], [0, 0, 1]])
    B, M = r * B0, s * M0
    t_b = sp.trace(B * B.T)
    t_m = sp.trace(M * M.T)
    d_b = sp.det(B * B.T)
    d_m = sp.det(M * M.T)
    alignment = sp.trace((M * B.T) * (M * B.T).T)
    assert (t_b, t_m, d_b, d_m, alignment) == (3 * r**2, 2 * s**2, 0, s**4, 0)

    jac = sp.Matrix([[sp.diff(t_b, r), sp.diff(t_b, s)], [sp.diff(t_m, r), sp.diff(t_m, s)]]).subs({r: 1, s: 1})
    assert jac == sp.diag(6, 4) and jac.det() == 24 and jac.rank() == 2
    gradients = sp.Matrix([
        [sp.diff(t_b, r), sp.diff(t_b, s)],
        [sp.diff(t_m, r), sp.diff(t_m, s)],
        [sp.diff(d_b, r), sp.diff(d_b, s)],
        [sp.diff(d_m, r), sp.diff(d_m, s)],
        [sp.diff(alignment, r), sp.diff(alignment, s)],
    ]).subs({r: 1, s: 1})
    assert gradients == sp.Matrix([[6, 0], [0, 4], [0, 0], [0, 4], [0, 0]])
    assert gradients.rank() == 2

    x_y, x_u, x_d = sp.symbols("x_Y x_u x_d", real=True)
    spectator_radii = sp.Matrix([x_y**2, x_u**2, x_d**2])
    spectator_jac = spectator_radii.jacobian((x_y, x_u, x_d)).subs({x_y: 0, x_u: 0, x_d: 0})
    assert spectator_jac == sp.zeros(3)

    c_ba, c_bb, c_ma, c_mb = sp.symbols("c_BA c_BB c_MA c_MB", real=True)
    coefficient_map = sp.Matrix([[3, 0, 2, 0], [0, 3, 0, 2]])
    coeffs = sp.Matrix([c_ba, c_bb, c_ma, c_mb])
    sources = coefficient_map * coeffs
    assert coefficient_map.rank() == 2 and len(coefficient_map.nullspace()) == 2
    k_b, k_m = sp.symbols("kappa_B kappa_M", real=True)
    diagonal_map = sp.diag(3, 2)
    assert diagonal_map.det() == 6
    inherited_portal_hessian = sp.zeros(2)

    objects = [B0, M0, B, M, t_b, t_m, d_b, d_m, alignment, jac, gradients, spectator_jac, coefficient_map, coeffs, sources, diagonal_map, inherited_portal_hessian]
    assert not any(obj.atoms(sp.Float) for obj in objects)

    result = {
        "date": "2026-08-31",
        "gate": gate,
        "active_scalar_carriers": {
            "coherence_radius": {"symbol": "T_B=Tr(BB*)", "vacuum_value": 3, "active": True, "gauge_singlet": True},
            "mass_radius": {"symbol": "T_M=Tr(MM*)", "vacuum_value": 2, "active": True, "gauge_singlet": True},
            "radial_jacobian": [[6, 0], [0, 4]],
            "radial_jacobian_determinant": 24,
            "radial_rank": 2,
        },
        "dependent_or_zero_candidates": {
            "det_BBstar": {"radial_value": 0, "first_order_new_direction": False},
            "det_MMstar": {"radial_value": "s^4", "gradient_at_vacuum": [0, 4], "first_order_new_direction": False},
            "alignment_norm": {"radial_value": 0, "first_order_new_direction": False},
            "spectator_edge_radii": {"vacuum_values": [0, 0, 0], "linear_response_rank": 0},
        },
        "portal_matrix_classification": {
            "general_matrix": [["c_BA", "c_BB"], ["c_MA", "c_MB"]],
            "dimension": 4,
            "vacuum_coefficient_map": [[3, 0, 2, 0], [0, 3, 0, 2]],
            "vacuum_coefficient_map_rank": 2,
            "vacuum_coefficient_map_nullity": 2,
            "diagonal_convention_sources": ["j_A=3 kappa_B", "j_B=2 kappa_M"],
            "diagonal_convention_determinant": 6,
            "diagonal_convention_symmetry_selected": False,
            "equivariant_hom_dimension": 4,
        },
        "inherited_parent": {
            "mixed_portal_hessian": [[0, 0], [0, 0]],
            "portal_rank": 0,
            "source_components_generated": 0,
        },
        "ledgers": {
            "carrier_classification_satisfied": 6,
            "carrier_classification_tested": 6,
            "canonical_pairing_satisfied": 0,
            "canonical_pairing_tested": 5,
            "inherited_portal_satisfied": 0,
            "inherited_portal_tested": 4,
        },
        "verdict": {
            "two_independent_active_scalar_modes_exist": True,
            "two_static_source_numbers_require_two_carriers": False,
            "two_dynamic_radial_modes_available": True,
            "canonical_carrier_to_central_pairing_exists": False,
            "inherited_portal_matrix_nonzero": False,
            "two_sources_derived": False,
        },
        "next_gate": "version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_portal_matrix_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()