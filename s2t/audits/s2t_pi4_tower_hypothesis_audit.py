import json
import math
from pathlib import Path

ALPHA_INV = 137.035999177
S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
T_OVER_S = T_RP3 / S_GEO
HALF_T_OVER_S = T_RP3 / (2 * S_GEO)

c_direct = PI4_TERM / T_OVER_S
c_halfdet = PI4_TERM / HALF_T_OVER_S
natural_candidates = {
    "1": 1.0,
    "1/2": 0.5,
    "pi": math.pi,
    "pi^2/2": math.pi**2 / 2,
    "pi^2": math.pi**2,
    "5": 5.0,
    "sqrt(24)": math.sqrt(24),
    "Vol(RP3)=pi^2": math.pi**2,
    "Vol(RP3)/2=pi^2/2": math.pi**2 / 2,
}
comparisons = {}
for name, value in natural_candidates.items():
    direct = value * T_OVER_S
    halfdet = value * HALF_T_OVER_S
    comparisons[name] = {
        "value": value,
        "as_direct_prefactor_term": direct,
        "direct_relative_to_pi4": direct / PI4_TERM,
        "direct_residual_vs_pi4": direct - PI4_TERM,
        "as_halfdet_prefactor_term": halfdet,
        "halfdet_relative_to_pi4": halfdet / PI4_TERM,
        "halfdet_residual_vs_pi4": halfdet - PI4_TERM,
    }

# If the pi^-4 term already equals a volume-weighted half determinant tower,
# the predicted coefficient is C_tower = pi^2 in Delta = -(pi^2/2) T/S.
pi2_half_tower = (math.pi**2 / 2) * T_OVER_S
residual = pi2_half_tower - PI4_TERM
results = {
    "status": "pi4_tower_hypothesis_promising_not_proven",
    "inputs": {
        "S_geo": S_GEO,
        "T_coex_RP3": T_RP3,
        "pi4_term": PI4_TERM,
        "T_over_S_geo": T_OVER_S,
        "half_T_over_S_geo": HALF_T_OVER_S,
    },
    "required_prefactors": {
        "direct_C_for_pi4_equals_C_T_over_S": c_direct,
        "halfdet_C_for_pi4_equals_C_T_over_2S": c_halfdet,
        "halfdet_C_over_pi2": c_halfdet / math.pi**2,
        "direct_C_over_pi2_over_2": c_direct / (math.pi**2 / 2),
    },
    "best_natural_candidate": {
        "hypothesis": "pi4 term ~= (Vol(RP3)/2) * T_coex_RP3 / S_geo",
        "value": pi2_half_tower,
        "target_pi4_term": PI4_TERM,
        "absolute_residual": residual,
        "relative_residual": residual / PI4_TERM,
        "alpha_inverse_shift_if_used_instead_of_pi4": residual,
    },
    "candidate_comparisons": comparisons,
    "verdict": (
        "The strongest natural relation is pi4_term ≈ (pi^2/2) T_RP3/S_geo, "
        "equivalently pi4_term ≈ pi^2 * T_RP3/(2 S_geo). The mismatch is about "
        f"{residual / PI4_TERM:.6%}. This is close enough to be a serious lead, "
        "but not an identity at the current exact-tower normalization; it requires "
        "a determinant derivation of the volume factor and an explanation of the residual."
    ),
}
Path("s2t_pi4_tower_hypothesis_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps({
    "pi4_term": PI4_TERM,
    "T_over_S": T_OVER_S,
    "required_direct_C": c_direct,
    "required_halfdet_C": c_halfdet,
    "pi2": math.pi**2,
    "pi2_half_candidate": pi2_half_tower,
    "relative_residual": residual / PI4_TERM,
}, indent=2))