#!/usr/bin/env python3
import json
import math
from pathlib import Path


def main():
    pi = math.pi
    full_trace_per_component = pi**4 / 3.0

    # Gamma(q)=c Tr log(K+qI), K_n=(n+1/2)^2.
    # Gamma''(0)=-c Tr K^-2.
    determinant_blocks = [
        {
            "block": "real_bosonic_full_two_form",
            "rank": 6,
            "c_logdet": 0.5,
            "Hessian": -0.5 * 6 * full_trace_per_component,
            "statistics": "bosonic",
            "matches_positive_pi4": False,
        },
        {
            "block": "complex_bosonic_selfdual_two_form",
            "rank": 3,
            "c_logdet": 1.0,
            "Hessian": -1.0 * 3 * full_trace_per_component,
            "statistics": "bosonic",
            "matches_positive_pi4": False,
        },
        {
            "block": "real_Grassmann_full_two_form",
            "rank": 6,
            "c_logdet": -0.5,
            "Hessian": 0.5 * 6 * full_trace_per_component,
            "statistics": "Grassmann/Pfaffian",
            "matches_positive_pi4": True,
        },
        {
            "block": "complex_Grassmann_selfdual_two_form",
            "rank": 3,
            "c_logdet": -1.0,
            "Hessian": 1.0 * 3 * full_trace_per_component,
            "statistics": "complex Grassmann",
            "matches_positive_pi4": True,
        },
    ]

    bf_results = json.loads(
        Path("s2t_bf_nielsen_kallosh_results.json").read_text(encoding="utf-8")
    )
    isolated_ghost_test = next(
        row
        for row in bf_results["tests"]
        if row["test"] == "isolated_one_form_ghost"
    )
    nk_test = next(
        row
        for row in bf_results["tests"]
        if row["test"] == "nielsen_kallosh_identification"
    )

    collective_hessian = pi**4
    inverse_hessian = 1.0 / collective_hessian
    source_for_exact_elimination = math.sqrt(2.0)
    # Full determinant form:
    # Z_2 ~ det(Delta_2)^(-1/2) det(Delta_1)^(+1)
    # det(Delta_0)^(-3/2), so Gamma coefficients are (+1/2,-1,+3/2).
    # Transverse determinant form:
    # Z_2 ~ det(Delta_2^T)^(-1/2) det(Delta_1^T)^(+1/2)
    # det(Delta_0)^(-1/2), so Gamma coefficients are (+1/2,-1/2,+1/2).
    # The two representations must be paired with ranks (6,4,1) and (3,3,1)
    # respectively; both leave one physical scalar degree of freedom.
    brst_raw_effective_c = 0.5 * 6 - 1.0 * 4 + 1.5 * 1
    brst_transverse_effective_c = 0.5 * 3 - 0.5 * 3 + 0.5 * 1
    brst_raw_hessian = -brst_raw_effective_c * full_trace_per_component
    brst_transverse_hessian = (
        -brst_transverse_effective_c * full_trace_per_component
    )

    results = {
        "status": "positive_pi4_logdet_Hessian_exists_only_in_ghostlike_blocks_not_present_as_BRST_complete_current_sector",
        "date": "2026-08-05",
        "spectral_model": {
            "operator": "K_n=(n+1/2)^2",
            "deformation": "K(q)=K+q I",
            "effective_action": "Gamma(q)=c Tr log K(q)",
            "Hessian": "Gamma''(0)=-c Tr K^-2",
            "full_trace_per_component": full_trace_per_component,
            "identity": "sum_{n in Z}(n+1/2)^-4=pi^4/3",
        },
        "determinant_blocks": determinant_blocks,
        "exact_positive_candidates": [
            row["block"] for row in determinant_blocks if row["matches_positive_pi4"]
        ],
        "sign_gate": {
            "finding": (
                "Bosonic determinant blocks give negative curvature -pi^4 for the natural "
                "rank-six/rank-three choices. Positive stable curvature +pi^4 requires the "
                "opposite Grassmann determinant sign."
            ),
        },
        "BRST_completeness_gate": {
            "previous_isolated_ghost_result": isolated_ghost_test["result"],
            "previous_full_two_form_factor": isolated_ghost_test[
                "full_p2_oscillator_factor"
            ],
            "previous_NK_result": nk_test["result"],
            "finding": (
                "Neither a real Grassmann two-form nor an isolated complex selfdual tensor "
                "ghost is a mandatory member of the standard two-form BRST tower. Adding only "
                "the favorable determinant repeats the previously rejected isolated-ghost move."
            ),
            "common_spectrum_controls": {
                "raw_bundle_rank_effective_c": brst_raw_effective_c,
                "raw_bundle_rank_Hessian": brst_raw_hessian,
                "transverse_rank_effective_c": brst_transverse_effective_c,
                "transverse_rank_Hessian": brst_transverse_hessian,
                "interpretation": (
                    "The full-rank and transverse determinant representations agree when their "
                    "correct exponents are used. Both reduce the six components to one physical "
                    "scalar degree of freedom and give negative bosonic curvature -pi^4/6."
                ),
            },
        },
        "boundary_gate": {
            "required": "antiperiodic tensor-ghost modes along S1",
            "current": "periodic Maxwell/FP gauge complex",
            "finding": (
                "The half-shift must be supplied by a new Z2-twisted tensor bundle; it is not "
                "inherited from the existing periodic gauge symmetry."
            ),
        },
        "inverse_response": {
            "Hessian": collective_hessian,
            "inverse_Hessian": inverse_hessian,
            "target": 1.0 / pi**4,
            "auxiliary_action": "Gamma(q)=H q^2/2 + J q/S_geo",
            "on_shell_shift": "-J^2/(2 H S_geo^2)",
            "J_required_for_exact_formula": source_for_exact_elimination,
            "finding": (
                "Even after H=pi^4 is induced, Gaussian elimination gives the exact S2T "
                "coefficient only if the linear source is fixed to sqrt(2), or if an equivalent "
                "two-source/variance readout is derived."
            ),
        },
        "comparison_with_C6": {
            "not_same_object": (
                "This q-mass Hessian is a new global tensor-ghost susceptibility. It is not the "
                "ambient metric Hessian of the existing Maxwell coexact determinant audited in C6."
            ),
            "consequence": (
                "A success would define new II.B field content and requires recomputing the "
                "1/24 branch, local heat coefficients and ghost cancellations."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "There is an explicit determinant whose second derivative is exactly +pi^4 "
                "without a numerical multiplier: a half-shifted ghostlike rank-six/full or rank-three/selfdual block."
            ),
            "negative": (
                "The required block is not BRST-mandatory, has the wrong boundary condition for "
                "the current gauge complex, and still needs a fixed source map to produce -1/(pi^4 S^2)."
            ),
            "status": "explicit_new_model_seed_not_current_theory_rescue",
            "reopening_condition": (
                "Derive the twisted tensor ghost from a complete reducible gauge symmetry and "
                "show that the full BV determinant leaves H=pi^4 and fixes the source normalization."
            ),
        },
    }

    assert abs(full_trace_per_component - pi**4 / 3.0) < 1e-12
    assert all(
        abs(abs(row["Hessian"]) - pi**4) < 1e-12 for row in determinant_blocks
    )
    assert results["exact_positive_candidates"] == [
        "real_Grassmann_full_two_form",
        "complex_Grassmann_selfdual_two_form",
    ]
    assert abs(inverse_hessian - 1.0 / pi**4) < 1e-14

    Path("s2t_halfshift_tensor_ghost_hessian_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "full_trace_per_component": full_trace_per_component,
                "exact_positive_candidates": results["exact_positive_candidates"],
                "positive_Hessian": collective_hessian,
                "inverse_Hessian": inverse_hessian,
                "required_source": source_for_exact_elimination,
                "BRST_raw_control_Hessian": brst_raw_hessian,
                "BRST_transverse_control_Hessian": brst_transverse_hessian,
                "BRST_status": "not_mandatory_in_current_complex",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()