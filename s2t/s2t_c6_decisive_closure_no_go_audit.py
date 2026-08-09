#!/usr/bin/env python3

import json
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


external_spectrum = load_json(
    "external_l21_spectrum_determinant_reproduction_results.json"
)
winding = load_json("external_rp3xs1_winding_determinant_results.json")
same_scheme = load_json("s2t_c6_same_scheme_final_verdict_results.json")
geometry = load_json(
    "s2t_c6_l21_delta2_principal_connection_ricci_C11_table_data.json"
)

spectrum_reproduced = all(
    row["match"] for row in external_spectrum["internal_coexact_comparison"]
)
scalar_half_residual = (
    external_spectrum["maxwell_bookkeeping"]["standard_FP_Gamma_nonzero_value_unit_RP3"]
    != 0.0
)
functional_bridge_fails = winding["controls"][
    "Bessel_and_logdet_are_not_same_object"
]
geometric_cancellation_fails = geometry["all_pairs_nonzero"] and not geometry[
    "zero_pairs"
]
mandatory_compensation_absent = (
    same_scheme["summary_counts"]["mandatory_compensation_found"] == 0
)

positive_closure = not any(
    [
        functional_bridge_fails,
        geometric_cancellation_fails,
        scalar_half_residual,
        mandatory_compensation_absent,
    ]
)
negative_closure = all(
    [
        spectrum_reproduced,
        functional_bridge_fails,
        geometric_cancellation_fails,
        scalar_half_residual,
        mandatory_compensation_absent,
    ]
)

if not negative_closure:
    raise RuntimeError("The declared C6 no-go inputs are not simultaneously satisfied")

results = {
    "status": "C6_closed_negatively_for_the_declared_Maxwell_FP_absorption_model",
    "date": "2026-08-03",
    "scope": (
        "The no-go applies to the current first-ambient-strain, Maxwell--ghost, "
        "rank-10 absorption construction. It does not prohibit a future theory with "
        "a newly derived mandatory sector or a different primary functional."
    ),
    "input_checks": {
        "external_L21_spectrum_reproduced": spectrum_reproduced,
        "casimir_kernel_is_not_logdet_winding": functional_bridge_fails,
        "principal_connection_Ricci_C11_all_pairs_nonzero": geometric_cancellation_fails,
        "standard_FP_scalar_half_residual_nonzero": scalar_half_residual,
        "mandatory_same_scheme_compensation_absent": mandatory_compensation_absent,
    },
    "numerical_witnesses": {
        "casimir_Bessel_sum_T": winding["numbers"]["internal_T_coex_RP3"],
        "bosonic_logdet_winding": winding["numbers"]["bosonic_Gamma_winding"],
        "absolute_logdet_to_T_ratio": winding["numbers"]["abs_Gamma_over_T"],
        "standard_FP_Gamma_nonzero_unit_RP3": external_spectrum[
            "maxwell_bookkeeping"
        ]["standard_FP_Gamma_nonzero_value_unit_RP3"],
        "geometric_zero_pair_count": len(geometry["zero_pairs"]),
        "geometric_rank_distribution": geometry["rank_distribution"],
    },
    "decision": {
        "positive_exact_pi4_determinant_closure": positive_closure,
        "negative_no_go_closure": negative_closure,
        "pi4_status": "strong_structural_compression_not_determinant_theorem",
        "S_vac_status": "conditional_not_closed_input",
        "maturity_effect": "C6_no_longer_an_open_calculation_inside_version_II_A",
    },
    "logic": [
        "The lens-space spectrum and standard FP determinant powers are independently reproduced.",
        "The positive Bessel kernel used by the absorption ansatz is a Casimir-energy object, whereas the Euclidean winding determinant is a logarithmic product; no identity equates them.",
        "The completed principal+connection+Ricci C11 block is nonzero for every symmetric strain pair.",
        "Projector and Hilbert transport are determinant-neutral, while standard FP retains a nonzero scalar half-determinant.",
        "No mandatory same-spectrum opposite-sign sector exists in the declared model.",
        "Therefore the exact pi^-4 absorption claim cannot be derived by completing another omitted block within the same construction.",
    ],
    "reopen_only_if": [
        "a new mandatory BRST, topological or EFT sector is derived before comparison with the target",
        "an exact spectral identity is proved between the relevant Casimir and log-determinant functionals",
        "a different primary physical functional is postulated and all previous pi^-4 numerics are recomputed within it",
    ],
    "verdict": (
        "C6 is closed negatively for Tome II.A. The external spectral gate confirms the "
        "lens-space spectrum but rejects the functional bridge from the Casimir Bessel "
        "kernel to the Euclidean Maxwell determinant. The same-scheme operator audit also "
        "leaves nonzero geometric and scalar residues with no mandatory compensation. "
        "Accordingly pi^-4 remains a strong structural compression, not a determinant theorem."
    ),
}

Path("s2t_c6_decisive_closure_no_go_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "positive_closure": positive_closure,
            "negative_closure": negative_closure,
            "functional_bridge_fails": functional_bridge_fails,
            "geometric_zero_pairs": len(geometry["zero_pairs"]),
            "scalar_half_residual": scalar_half_residual,
        },
        ensure_ascii=False,
        indent=2,
    )
)