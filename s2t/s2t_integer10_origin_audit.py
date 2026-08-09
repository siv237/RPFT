import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
NATURAL = (math.pi**2 / 2) * T_RP3 / S_GEO
EPS_NEEDED = 1 - PI4_TERM / NATURAL


def scalar_rp3_modes(l_max=8):
    rows = []
    for ell in range(0, l_max + 1, 2):
        rows.append({
            "ell": ell,
            "lambda": ell * (ell + 2),
            "degeneracy_s3": (ell + 1) ** 2,
            "rp3_parity": 1,
            "descends_to_rp3": True,
        })
    return rows

scalar_rows = scalar_rp3_modes()
zero_plus_first_even = scalar_rows[0]["degeneracy_s3"] + scalar_rows[1]["degeneracy_s3"]
casmix_epsilon = zero_plus_first_even / (24 * S_GEO)
casmix_term = NATURAL * (1 - casmix_epsilon)

alternative_integer_sources = {
    "scalar_even_shell_ell0_plus_ell2": zero_plus_first_even,
    "coexact_first_level_n1": 2 * 1 * (1 + 2),
    "scalar_first_nonzero_even_ell2_only": scalar_rows[1]["degeneracy_s3"],
    "internal_metric_symmetric_components_dim4": 4 * 5 // 2,
    "so4_isometry_dimension": 6,
    "rp3_volume_shell_candidate_pi2_not_integer": math.pi**2,
}

results = {
    "status": "integer10_has_plausible_scalar_ghost_shell_origin_not_final_proof",
    "core_claim": "On RP^3, scalar harmonics descending from S^3 are even ell. The zero shell ell=0 has degeneracy 1 and the first nonzero even shell ell=2 has degeneracy 9; together they give 10.",
    "numbers": {
        "S_geo": S_GEO,
        "pi4_term": PI4_TERM,
        "natural_pi2_half_tower": NATURAL,
        "epsilon_needed": EPS_NEEDED,
        "integer10_over_24S": casmix_epsilon,
        "epsilon_relative_error": (casmix_epsilon - EPS_NEEDED) / EPS_NEEDED,
        "casmix_term_with_integer10": casmix_term,
        "casmix_term_minus_pi4": casmix_term - PI4_TERM,
        "casmix_relative_error_vs_pi4": (casmix_term - PI4_TERM) / PI4_TERM,
    },
    "scalar_rp3_even_modes": scalar_rows,
    "alternative_integer_sources": alternative_integer_sources,
    "verdict": (
        "The integer 10 can be non-arbitrarily associated with the scalar/ghost "
        "RP3 even sector: 1 constant mode plus 9 first nonzero even scalar modes. "
        "This is structurally relevant because the 1/24 branch lives in the scalar "
        "periodic Maxwell--ghost determinant, and exact one-form modes inherit the "
        "scalar spectrum. It is not yet a proof of the second-order cross-term sign "
        "or coefficient, but it upgrades 10 from a naked fit to a concrete spectral "
        "candidate."
    ),
}

Path("s2t_integer10_origin_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps(results["numbers"], indent=2, ensure_ascii=False))
print("integer10", zero_plus_first_even)