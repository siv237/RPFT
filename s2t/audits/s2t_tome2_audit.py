import json
import math
from pathlib import Path

ALPHA_INV = 137.035999177
M_E_MEV = 0.51099895069
M_MU_MEV = 105.6583755
M_TAU_REF_MEV = 1776.86


def rel_error(value, reference):
    return (value - reference) / reference


alpha = 1 / ALPHA_INV
s_geo = 4 * math.pi**3 + math.pi**2 + math.pi
s_vac = s_geo - 1 / (24 * s_geo) - 1 / (math.pi**4 * s_geo**2)
tau_factor = math.pi**2 + 2 * math.pi + 2 / 3 - alpha / 3
m_tau_mev = M_MU_MEV * tau_factor
m_tau_gev = m_tau_mev / 1000
v_s2t = m_tau_gev * s_vac * (1 + math.pi ** -4)
lambda_h = (1 / 8) * (1 + 1 / (3 * math.pi**2))
m_h = math.sqrt(2 * lambda_h) * v_s2t

results = {
    "inputs": {
        "alpha_inv": ALPHA_INV,
        "m_e_MeV": M_E_MEV,
        "m_mu_MeV": M_MU_MEV,
    },
    "closed_rows": {
        "S_geo": s_geo,
        "S_vac": s_vac,
        "tau_factor": tau_factor,
        "m_tau_MeV": m_tau_mev,
        "v_S2T_GeV": v_s2t,
        "lambda_H_S2T": lambda_h,
        "M_H_GeV": m_h,
    },
    "reference_checks": {
        "alpha_inv_reference": ALPHA_INV,
        "S_vac_minus_alpha_inv": s_vac - ALPHA_INV,
        "m_tau_reference_MeV": M_TAU_REF_MEV,
        "m_tau_relative_error": rel_error(m_tau_mev, M_TAU_REF_MEV),
    },
    "status": {
        "S_vac": "closed_train_anchor_reproduction",
        "m_tau": "strong_conditional_relation_seed_and_projection_normalization_open",
        "v_S2T": "conditional_higgs_scale_inherits_tau_and_Svac",
        "lambda_H_S2T": "closed_spectral_scalar_normalization",
        "M_H": "conditional_higgs_mass_bridge_inherits_absolute_scale",
        "parent_action": "minimal_unified_two_sector_normalization_gate_failed",
        "global_physical_status": "IIA_rejected_zero_closed_independent_empirical_predictions",
    },
}

Path("s2t_tome2_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)

for section, values in results.items():
    print(f"[{section}]")
    for key, value in values.items():
        if isinstance(value, float):
            print(f"{key}={value:.15g}")
        else:
            print(f"{key}={value}")