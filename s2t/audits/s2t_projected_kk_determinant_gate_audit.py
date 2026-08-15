import json
import math
from pathlib import Path

import numpy as np


projection = json.loads(
    Path("s2t_anomaly_free_holonomy_projection_results.json").read_text()
)
cone = json.loads(Path("s2t_kk_representation_cone_results.json").read_text())

required = np.array(
    cone["required_low_energy_threshold_vector"]["magnitudes_Y_2_3"]
)
survivor_beta = np.array(
    projection["zero_mode_content"]["beta_vector_Y_2_3"]
)

component_beta = {
    row["name"]: np.array(row["beta"])
    for row in projection["phase_table"]
}

quarter_partner_beta = (
    component_beta["Q"]
    + 2.0 * component_beta["L"]
    + component_beta["T_H"]
)
half_partner_beta = component_beta["E"]


def stable_logdet_ratio(rho, beta):
    x = 2.0 * math.pi * rho
    q = math.exp(-x)
    cosine = math.cos(2.0 * math.pi * beta)
    numerator = 1.0 - 2.0 * cosine * q + q * q
    denominator = (1.0 - q) ** 2
    return math.log(numerator / denominator)


def normalized_to_su2(vector):
    return (vector / vector[1]).tolist()


rho_grid = [0.05, 0.1, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
shell_rows = []
for rho in rho_grid:
    quarter_weight = stable_logdet_ratio(rho, 0.25)
    half_weight = stable_logdet_ratio(rho, 0.5)
    partner_vector = (
        quarter_weight * quarter_partner_beta
        + half_weight * half_partner_beta
    )
    shell_rows.append(
        {
            "rho": rho,
            "quarter_logdet_ratio": quarter_weight,
            "half_logdet_ratio": half_weight,
            "half_over_quarter": half_weight / quarter_weight,
            "partner_threshold_direction_Y_2_3": partner_vector.tolist(),
            "normalized_to_SU2": normalized_to_su2(partner_vector),
            "relative_to_required_normalized": (
                partner_vector / partner_vector[1]
                - required / required[1]
            ).tolist(),
        }
    )

best_survivor_amplitude = float(required @ survivor_beta / (survivor_beta @ survivor_beta))
survivor_fitted = best_survivor_amplitude * survivor_beta
survivor_relative_residual = (survivor_fitted - required) / required
running_log_interval = 2.0 * math.pi * best_survivor_amplitude
t_ew = 29.919805079547
mz_gev = 91.1880
lambda_s2t_gev = mz_gev * math.exp(t_ew)
split_scale_gev = lambda_s2t_gev * math.exp(-running_log_interval)

partner_color_over_su2 = quarter_partner_beta[2] / quarter_partner_beta[1]
required_color_over_su2 = required[2] / required[1]

results = {
    "status": "projected_partner_holonomy_determinant_fails_direction_survivor_intermediate_running_remains_conditional",
    "date": "2026-08-04",
    "normalization": {
        "mode_function": (
            "L_beta(rho)=log[(cosh(2pi rho)-cos(2pi beta))/(cosh(2pi rho)-1)]"
        ),
        "local_terms": "cancel in each shifted-minus-periodic ratio",
        "overall_gauge_prefactor": (
            "irrelevant for the direction no-go; a standard 1/(2pi) factor is used only for the running-scale reconstruction"
        ),
    },
    "projected_partner_content": {
        "quarter_branches": "Q + 2 L + T_H",
        "quarter_beta_vector_Y_2_3": quarter_partner_beta.tolist(),
        "half_branch": "E",
        "half_beta_vector_Y_2_3": half_partner_beta.tolist(),
        "generic_common_shell": (
            "Delta_shell=A(rho)*(Q+2L+T_H)+B(rho)*E, with A,B>0"
        ),
        "fixed_color_over_SU2": partner_color_over_su2,
        "required_color_over_SU2": required_color_over_su2,
    },
    "shell_sweep": shell_rows,
    "analytic_direction_no_go": {
        "quarter_vector_exact": "(5/3,10/3,3/2)",
        "half_vector_exact": "(4/3,0,0)",
        "normalized_generic_vector": (
            "((5+4r)/10, 1, 9/20), r=B/A>0"
        ),
        "finding": (
            "the color/SU2 ratio is identically 9/20 for every common shell and every positive tower sum, while the required ratio is about 11.014"
        ),
        "verdict": (
            "the finite holonomy determinant of the projected partners cannot generate the required gauge correction direction under a common RP3 spectrum"
        ),
    },
    "survivor_running_reconstruction": {
        "survivor_content": "U+2D+H",
        "beta_vector_Y_2_3": survivor_beta.tolist(),
        "best_common_inverse_alpha_amplitude": best_survivor_amplitude,
        "fitted_shift_magnitudes": survivor_fitted.tolist(),
        "relative_residuals": survivor_relative_residual.tolist(),
        "max_abs_relative_residual": float(
            np.max(np.abs(survivor_relative_residual))
        ),
        "equivalent_log_running_interval": running_log_interval,
        "Lambda_S2T_GeV_from_existing_T_EW": lambda_s2t_gev,
        "reconstructed_split_scale_GeV": split_scale_gev,
        "interpretation": (
            "if the periodic split sector is active over this intermediate interval, its ordinary running has nearly the required direction; the scale is reconstructed from controls and is not yet predicted"
        ),
    },
    "theory_effect": {
        "finite_projected_partner_determinant": "closed_negatively_in_common_spectrum_model",
        "split_zero_sector_running": "directionally_viable_but_scale_not_derived",
        "required_new_input": (
            "a geometric or dynamical mass for the vectorlike U,D,H sector near the reconstructed intermediate scale, plus non-common spectra if partner determinants are retained"
        ),
        "stop_rule": (
            "do not use the reconstructed split scale as a prediction; derive it independently before rerunning the gauge scorecard"
        ),
    },
    "verdict": (
        "The requested determinant calculation is negative in the minimal common-spectrum realization. The quarter/half-shifted partners always produce color/SU2 ratio 9/20, far from the required 11.014, independent of normalization or the number of common KK shells. The only surviving mechanism is ordinary intermediate-scale running of the periodic U+2D+H sector. It would need a log interval about 10.065, corresponding to a reconstructed scale near 3.8e10 GeV for the existing S2T high scale, but that mass scale is not derived and therefore cannot yet repair the prediction."
    ),
}

assert abs(partner_color_over_su2 - 9.0 / 20.0) < 1.0e-12
assert required_color_over_su2 > 11.0
assert all(1.0 < row["half_over_quarter"] < 2.0 for row in shell_rows)
assert results["survivor_running_reconstruction"]["max_abs_relative_residual"] < 0.06

Path("s2t_projected_kk_determinant_gate_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "partner_color_over_SU2": partner_color_over_su2,
            "required_color_over_SU2": required_color_over_su2,
            "survivor_running_log_interval": running_log_interval,
            "reconstructed_split_scale_GeV": split_scale_gev,
            "survivor_max_residual": results[
                "survivor_running_reconstruction"
            ]["max_abs_relative_residual"],
        },
        indent=2,
        ensure_ascii=False,
    )
)