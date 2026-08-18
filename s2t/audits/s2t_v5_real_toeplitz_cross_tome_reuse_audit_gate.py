#!/usr/bin/env python3
"""Retrospective inventory for the Real Toeplitz KO6 continuation."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    evidence = {
        "version3_real_bimodule_square": {
            "proved": "KO6 requires two conjugate copies with opposite grading",
            "reusable": "exchange J and grading skeleton",
            "does_not_prove": "Fredholm or Clifford index",
        },
        "version3_orbit_measure_pfaffian": {
            "proved": "bosonic full trace and fermionic Pfaffian half-count differ",
            "reusable": "trace cancellation is not a K-class test",
            "does_not_prove": "integer Real index",
        },
        "version4_pfaffian_eta_orientation": {
            "proved": "oriented reduced signs cancel in the full J-paired Pfaffian",
            "reusable": "separate functional-measure phase from KO class",
            "does_not_prove": "triviality of exchange Real class",
        },
        "version5_oriented_height_hodge": {
            "proved": "KO6 exchange does not select an orientation sign",
            "reusable": "sign must come from Hopf/Toeplitz orientation data",
            "does_not_prove": "failure after an orientation is already fixed",
        },
        "version5_affine_ko6_reference_corner": {
            "proved": "explicit J d J^-1=d* exchange completion exists",
            "reusable": "finite algebraic model of the same exchange pattern",
            "does_not_prove": "nonzero index in finite dimension",
        },
        "strict_rpft_spectral_flow": {
            "proved": "the archived theta:0-to-pi family has spectral flow zero",
            "reusable": "negative control against importing the old pi argument",
            "does_not_prove": "the coefficient Toeplitz boundary index",
        },
    }

    reusable = [
        "J exchanges conjugate copies",
        "the conjugate copy has opposite grading",
        "J d J^-1=d* is already an exact project pattern",
        "full trace or Pfaffian cancellation is not a KO-class computation",
        "orientation must be supplied by the Hopf/Toeplitz symbol, not by J alone",
    ]
    missing = [
        "graded Clifford convention for degree six",
        "explicit real-to-complex comparison map",
        "proof that the KO6 generator maps to the oriented pair (-1,+1)",
        "coefficient multiplication by rank(q0)=15 inside the real boundary map",
    ]

    result = {
        "gate": "version5_real_toeplitz_cross_tome_reuse_audit_gate",
        "scope": {
            "tomes_and_live_gates": ["III", "IV", "V"],
            "strict_rpft_archive_checked": True,
            "explicit_Cl06_index_cycle_found": False,
        },
        "evidence_matrix": evidence,
        "reusable_lemmas": reusable,
        "missing_lemmas": missing,
        "architectural_consequence": {
            "new_physical_particle_antiparticle_sector_needed": False,
            "new_finite_KO6_doubling_needed": False,
            "analytic_relative_KKO_cycle_needed": True,
            "old_rpft_zero_spectral_flow_can_supply_index": False,
            "candidate_weight": 15 / 105,
        },
        "verdict": {
            "retrospective_review_changes_next_step": True,
            "exchange_skeleton_already_proved": True,
            "integer_class_already_proved": False,
            "next_gate": "version5_real_toeplitz_bott_comparison_map_gate",
            "stop_test": "comparison image must be anti-diagonal oriented pair, not diagonal cancellation",
        },
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_real_toeplitz_cross_tome_reuse_audit_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert len(evidence) == 6
    assert result["architectural_consequence"]["candidate_weight"] == 1 / 7
    assert not result["scope"]["explicit_Cl06_index_cycle_found"]
    print(output)


if __name__ == "__main__":
    main()