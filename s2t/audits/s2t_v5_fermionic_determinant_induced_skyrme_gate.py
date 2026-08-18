#!/usr/bin/env python3
"""Audit whether the H15 fermion determinant fixes a Skyrme scale."""
from __future__ import annotations

import json
import math
from pathlib import Path


def gamma1(x: float) -> float:
    """Upper incomplete Gamma(1,x)."""
    return math.exp(-x)


def gamma2(x: float) -> float:
    """Upper incomplete Gamma(2,x)."""
    return math.exp(-x) * (1.0 + x)


def main() -> None:
    samples = []
    for x in (0.01, 0.25, 1.0, 4.0):
        g1 = gamma1(x)
        g2 = gamma2(x)
        samples.append(
            {
                "x=M^2/Lambda^2": x,
                "Gamma(1,x)": g1,
                "Gamma(2,x)": g2,
                "Gamma(2,x)/Gamma(1,x)": g2 / g1,
            }
        )

    result = {
        "gate": "version5_fermionic_determinant_induced_skyrme_gate",
        "literature_mechanism": {
            "normal_parity_expansion_through_four_derivatives": True,
            "two_derivative_term_possible": True,
            "four_derivative_terms_possible": True,
            "pure_positive_skyrme_term_guaranteed": False,
            "additional_four_derivative_invariants": True,
        },
        "proper_time_ratio_audit": {
            "identity": "Gamma(2,x)/Gamma(1,x)=1+x",
            "samples": samples,
            "relative_four_derivative_weights_universal": False,
        },
        "project_inputs": {
            "canonical_D_of_V15_on_H15": False,
            "fermion_gap_M_derived": False,
            "relative_Yukawa_amplitudes_derived": False,
            "renormalization_condition_derived": False,
            "common_trace_weight": "1/7",
            "common_weight_cancels_from_E4_over_E2": True,
        },
        "dimensional_conclusion": {
            "generic_radius": "M^-1 times R(M/Lambda,Y,scheme)",
            "finite_radius_from_current_parent": False,
        },
        "verdict": {
            "conditional_induction": True,
            "parameter_free_scale_closure": False,
            "physical_closure": False,
            "next_gate": "version5_eta_wzw_real_pair_phase_gate",
        },
    }

    for sample in samples:
        x = sample["x=M^2/Lambda^2"]
        assert abs(sample["Gamma(2,x)/Gamma(1,x)"] - (1.0 + x)) < 1e-14
    assert len({round(s["Gamma(2,x)/Gamma(1,x)"], 12) for s in samples}) == 4
    assert not result["project_inputs"]["fermion_gap_M_derived"]
    assert not result["verdict"]["parameter_free_scale_closure"]

    out = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "s2t_v5_fermionic_determinant_induced_skyrme_gate_results.json"
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()