#!/usr/bin/env python3
"""Audit eta/WZW and Pfaffian phases of the Real exchange pair."""
from __future__ import annotations

import cmath
import json
from pathlib import Path


def main() -> None:
    winding_plus = 15
    winding_minus = -15
    integer_level = 1

    complex_phase_plus = cmath.exp(2j * cmath.pi * integer_level * winding_plus)
    complex_phase_minus = cmath.exp(2j * cmath.pi * integer_level * winding_minus)
    reduced_pfaffian_plus = (-1) ** winding_plus
    reduced_pfaffian_minus = (-1) ** abs(winding_minus)

    result = {
        "gate": "version5_eta_wzw_real_pair_phase_gate",
        "degree_audit": {
            "loop_domain": "S1",
            "cubic_WZW_form_on_S1": 0,
            "native_loop_invariant": "first odd Chern character / winding",
            "spatial_Bott_domain": "S3",
        },
        "oriented_charges": {
            "winding": [winding_plus, winding_minus],
            "Bott_three_charge": [winding_plus, winding_minus],
            "total_oriented_charge": winding_plus + winding_minus,
        },
        "complex_determinant_phase": {
            "integer_level": integer_level,
            "plus_phase": [complex_phase_plus.real, complex_phase_plus.imag],
            "minus_phase": [complex_phase_minus.real, complex_phase_minus.imag],
            "pair_phase": [
                (complex_phase_plus * complex_phase_minus).real,
                (complex_phase_plus * complex_phase_minus).imag,
            ],
            "sector_15_distinguished_from_zero": False,
            "fractional_level_derived": False,
        },
        "pfaffian_parity": {
            "conditional_reduced_plus": reduced_pfaffian_plus,
            "conditional_reduced_minus": reduced_pfaffian_minus,
            "full_real_pair": reduced_pfaffian_plus * reduced_pfaffian_minus,
            "real_skew_adjoint_family_constructed": False,
            "pfaffian_line_orientation_derived": False,
            "single_reality_orbit_measure_derived": False,
        },
        "project_cross_audit": {
            "version3_pfaffian_half_count_reused": True,
            "version4_full_KO6_phase_cancellation_reused": True,
            "version4_determinant_line_inflow_no_go_reused": True,
            "topological_closure_defect_preserved": True,
        },
        "verdict": {
            "eta_WZW_selects_nonzero_sector": False,
            "conditional_oriented_parity_witness": True,
            "full_real_measure_phase": "+1",
            "physical_closure": False,
            "next_gate": "version5_global_carrier_forced_nontrivial_sector_gate",
        },
    }

    tol = 1e-12
    assert abs(complex_phase_plus - 1) < tol
    assert abs(complex_phase_minus - 1) < tol
    assert winding_plus + winding_minus == 0
    assert reduced_pfaffian_plus == -1
    assert reduced_pfaffian_minus == -1
    assert reduced_pfaffian_plus * reduced_pfaffian_minus == 1
    assert not result["verdict"]["eta_WZW_selects_nonzero_sector"]

    out = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "s2t_v5_eta_wzw_real_pair_phase_gate_results.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()