import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
NATURAL = (math.pi**2 / 2) * T_RP3 / S_GEO
M = PI4_TERM / NATURAL
EPS = 1 - M
ABS_RESIDUAL = NATURAL - PI4_TERM

candidates = {
    "1/(24*S_geo)": 1 / (24 * S_GEO),
    "1/(2*pi*S_geo)": 1 / (2 * math.pi * S_GEO),
    "1/(3*pi*S_geo)": 1 / (3 * math.pi * S_GEO),
    "1/(4*pi*S_geo)": 1 / (4 * math.pi * S_GEO),
    "1/(pi*S_geo)": 1 / (math.pi * S_GEO),
    "alpha/pi_using_S_geo": 1 / (math.pi * S_GEO),
    "1/(pi^2*S_geo)": 1 / (math.pi**2 * S_GEO),
    "1/(2*pi^2*S_geo)": 1 / (2 * math.pi**2 * S_GEO),
    "1/(24*pi^2)": 1 / (24 * math.pi**2),
    "1/(32*pi^2)": 1 / (32 * math.pi**2),
    "1/(12*pi^2)": 1 / (12 * math.pi**2),
    "1/(8*pi^2)": 1 / (8 * math.pi**2),
    "1/(2*S_geo)": 1 / (2 * S_GEO),
    "1/(3*S_geo)": 1 / (3 * S_GEO),
    "1/(4*S_geo)": 1 / (4 * S_GEO),
    "1/S_geo": 1 / S_GEO,
}
comparisons = []
for name, value in candidates.items():
    comparisons.append({
        "candidate": name,
        "value": value,
        "eps_minus_candidate": EPS - value,
        "relative_error_to_eps": (value - EPS) / EPS,
        "M_candidate": 1 - value,
        "pi4_term_with_candidate": NATURAL * (1 - value),
        "absolute_error_vs_pi4": NATURAL * (1 - value) - PI4_TERM,
    })
comparisons.sort(key=lambda row: abs(row["relative_error_to_eps"]))

# Search low-complexity a/(b*pi*S), a/(b*S), a/(b*pi^2) families.
search = []
for family in ["a/(b*pi*S)", "a/(b*S)", "a/(b*pi^2)", "a/(b*pi^2*S)"]:
    for a in range(1, 13):
        for b in range(1, 97):
            if family == "a/(b*pi*S)":
                value = a / (b * math.pi * S_GEO)
            elif family == "a/(b*S)":
                value = a / (b * S_GEO)
            elif family == "a/(b*pi^2)":
                value = a / (b * math.pi**2)
            else:
                value = a / (b * math.pi**2 * S_GEO)
            if value < 0.02:
                search.append({
                    "expr": f"{a}/{b} in {family}",
                    "value": value,
                    "relative_error_to_eps": (value - EPS) / EPS,
                })
search.sort(key=lambda row: abs(row["relative_error_to_eps"]))

results = {
    "status": "residual_has_plausible_alpha_over_pi_like_scale_but_no_unique_derivation",
    "numbers": {
        "S_geo": S_GEO,
        "pi4_term": PI4_TERM,
        "natural_pi2_half_tower": NATURAL,
        "absolute_residual_natural_minus_pi4": ABS_RESIDUAL,
        "multiplier_needed": M,
        "epsilon_needed_1_minus_multiplier": EPS,
    },
    "best_named_candidates": comparisons[:12],
    "best_low_complexity_search": search[:20],
    "verdict": (
        "The correction needed to turn (pi^2/2)T/S into the exact pi^-4 term is "
        "epsilon=0.0030435883. This is close to alpha/pi = 1/(pi S_geo) = "
        "0.0023228, but not close enough for an identity. Low-complexity searches "
        "find rationalized variants, but they are numerology unless a determinant "
        "or torsion-sector derivation supplies the coefficient."
    ),
}
Path("s2t_pi4_residual_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps({
    "multiplier_needed": M,
    "epsilon_needed": EPS,
    "absolute_residual": ABS_RESIDUAL,
    "best_named": comparisons[:5],
    "best_search": search[:8],
}, indent=2, ensure_ascii=False))