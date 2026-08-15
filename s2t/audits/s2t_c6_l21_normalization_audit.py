import json
import math
from pathlib import Path

cover_degree = 2
vol_s3_unit = 2 * math.pi ** 2
vol_l21_unit = vol_s3_unit / cover_degree

normalization_rules = [
    {
        "object": "descended_one_form",
        "s3_norm_assumption": "Integral_S3 |alpha|^2 dvol = 1 for an antipodal-invariant form.",
        "l21_raw_norm_squared": 1 / cover_degree,
        "l21_orthonormal_multiplier": math.sqrt(cover_degree),
        "meaning": "A quotient-orthonormal form is sqrt(2) times the descended S3-normalized invariant form.",
    },
    {
        "object": "bilinear_matrix_element_with_strain",
        "formula": "<alpha_i, V_q alpha_j>_L21 = Integral_S3 alpha_i V_q alpha_j dvol_S3 when alpha_i, alpha_j are S3-normalized invariant lifts and the L21 forms are renormalized by sqrt(2).",
        "net_cover_factor": 1.0,
        "meaning": "The two sqrt(2) factors from the external one-forms cancel the 1/2 quotient integral.",
    },
    {
        "object": "trace_square",
        "formula": "Sum_ij lambda_i^-1 M_ij lambda_j^-1 M_ji uses quotient-orthonormal states; no extra factor 1/2 or 2 may be inserted after the matrix elements are normalized.",
        "net_cover_factor": 1.0,
        "meaning": "The L(2,1) projection changes the allowed states, not the already normalized bilinear trace by a global volume multiplier.",
    },
]

failure_modes = [
    {
        "mistake": "use_s3_normalized_forms_directly_on_l21",
        "effect": "All L21 norms are smaller by 1/2; matrix elements are off by a factor 1/2.",
        "status": "forbidden",
    },
    {
        "mistake": "multiply_final_trace_by_cover_degree_after_orthonormalization",
        "effect": "Double-counts the quotient normalization already present in the matrix elements.",
        "status": "forbidden",
    },
    {
        "mistake": "keep_even_shells_because_s3_integrals_are_used",
        "effect": "Confuses the lift used for integration with the quotient state space; even shells remain projected out.",
        "status": "forbidden",
    },
]

checks = {
    "volume_ratio_s3_to_l21": vol_s3_unit / vol_l21_unit,
    "raw_descended_norm_squared": 1 / cover_degree,
    "renormalized_norm_squared": cover_degree * (1 / cover_degree),
    "bilinear_net_factor": (math.sqrt(cover_degree) ** 2) / cover_degree,
}

results = {
    "status": "L21_normalization_fixed_no_global_cover_factor_in_trace",
    "cover_degree": cover_degree,
    "volumes_unit_radius": {
        "S3": vol_s3_unit,
        "L21_RP3": vol_l21_unit,
    },
    "normalization_rules": normalization_rules,
    "checks": checks,
    "failure_modes": failure_modes,
    "verdict": (
        "For antipodal-invariant coexact one-forms lifted to S3, quotient orthonormalization multiplies each state by sqrt(2). "
        "In a bilinear variation matrix element this cancels the 1/2 quotient integral, so the practical integral may be computed on S3 over invariant lifts with no extra global cover factor. "
        "The cover only decides the allowed parity sector and the state normalization; it does not turn the final mixed trace into twice or half the S3-normalized answer."
    ),
}

Path("s2t_c6_l21_normalization_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": results["status"], "checks": checks}, indent=2, ensure_ascii=False))