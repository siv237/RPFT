import itertools
import json
import math
from pathlib import Path

import numpy as np


ALPHA_INV = 137.035999177
RHO_S2T = 0.75 * (1.0 + (1.0 / ALPHA_INV) / 3.0)

scorecard = json.loads(Path("s2t_blind_prediction_scorecard_results.json").read_text())
rows = {row["observable"]: row for row in scorecard["rows"]}
fermi = json.loads(Path("s2t_blind_fermi_constant_results.json").read_text())

v_s2t = fermi["frozen_prediction"]["v_S2T_GeV"]
v_fermi = fermi["experimental_comparison"]["v_from_G_F_GeV"]

mw_prediction = rows["M_W_GeV"]["prediction"]
mz_prediction = rows["M_Z_GeV"]["prediction"]
mw_control = rows["M_W_GeV"]["control"]
mz_control = rows["M_Z_GeV"]["control"]

g2_prediction = 2.0 * mw_prediction / v_s2t
gz_prediction = 2.0 * mz_prediction / v_s2t
gy_prediction = math.sqrt(gz_prediction**2 - g2_prediction**2)

g2_required = 2.0 * mw_control / v_fermi
gz_required = 2.0 * mz_control / v_fermi
gy_required = math.sqrt(gz_required**2 - g2_required**2)

alpha_s_prediction = rows["alpha_s_MZ"]["prediction"]
alpha_s_required = rows["alpha_s_MZ"]["control"]
g3_prediction = math.sqrt(4.0 * math.pi * alpha_s_prediction)
g3_required = math.sqrt(4.0 * math.pi * alpha_s_required)


def inverse_alpha(gauge_coupling):
    return 4.0 * math.pi / gauge_coupling**2


required_signed_shifts = np.array(
    [
        inverse_alpha(gy_required) - inverse_alpha(gy_prediction),
        inverse_alpha(g2_required) - inverse_alpha(g2_prediction),
        inverse_alpha(g3_required) - inverse_alpha(g3_prediction),
    ]
)
required_magnitudes = -required_signed_shifts

beta_vectors = {
    "Q": np.array([2.0 / 9.0, 2.0, 4.0 / 3.0]),
    "U": np.array([16.0 / 9.0, 0.0, 2.0 / 3.0]),
    "D": np.array([4.0 / 9.0, 0.0, 2.0 / 3.0]),
    "L": np.array([2.0 / 3.0, 2.0 / 3.0, 0.0]),
    "E": np.array([4.0 / 3.0, 0.0, 0.0]),
    "H": np.array([1.0 / 6.0, 1.0 / 6.0, 0.0]),
    "Sigma3": np.array([0.0, 2.0 / 3.0, 0.0]),
    "Sigma8": np.array([0.0, 0.0, 1.0]),
}


def ray_fit(vector):
    scale = float(required_magnitudes @ vector / (vector @ vector))
    fitted = scale * vector
    relative_residual = (fitted - required_magnitudes) / required_magnitudes
    return {
        "common_amplitude": scale,
        "fitted_shift_magnitudes": fitted.tolist(),
        "relative_residuals": relative_residual.tolist(),
        "relative_residual_norm": float(np.linalg.norm(relative_residual)),
        "max_abs_relative_residual": float(np.max(np.abs(relative_residual))),
    }


frozen_candidate_rays = {
    "one_complete_generation": (
        beta_vectors["Q"]
        + beta_vectors["U"]
        + beta_vectors["D"]
        + beta_vectors["L"]
        + beta_vectors["E"]
    ),
    "three_generations_plus_one_Higgs": (
        3.0
        * (
            beta_vectors["Q"]
            + beta_vectors["U"]
            + beta_vectors["D"]
            + beta_vectors["L"]
            + beta_vectors["E"]
        )
        + beta_vectors["H"]
    ),
    "split_U_plus_2D_plus_H": (
        beta_vectors["U"] + 2.0 * beta_vectors["D"] + beta_vectors["H"]
    ),
}

ray_rows = {
    name: {
        "beta_vector_Y_2_3": vector.tolist(),
        **ray_fit(vector),
    }
    for name, vector in frozen_candidate_rays.items()
}


def integer_cone_search(names, maximum_count, maximum_total=None):
    candidates = []
    for counts in itertools.product(range(maximum_count + 1), repeat=len(names)):
        if sum(counts) == 0:
            continue
        if maximum_total is not None and sum(counts) > maximum_total:
            continue
        vector = sum(
            (count * beta_vectors[name] for count, name in zip(counts, names)),
            np.zeros(3),
        )
        fit = ray_fit(vector)
        candidates.append(
            {
                "counts": {name: count for name, count in zip(names, counts)},
                "total_count": sum(counts),
                "beta_vector_Y_2_3": vector.tolist(),
                **fit,
            }
        )
    candidates.sort(
        key=lambda row: (
            row["relative_residual_norm"],
            row["max_abs_relative_residual"],
            row["total_count"],
        )
    )
    return candidates


minimal_split_search = integer_cone_search(
    ["U", "D", "H"], maximum_count=6, maximum_total=4
)
larger_split_search = integer_cone_search(
    ["U", "D", "H"], maximum_count=6
)
extended_search = integer_cone_search(
    ["U", "D", "H", "Sigma3", "Sigma8"], maximum_count=6
)

geometric_single_level_amplitude = abs(math.log(RHO_S2T)) / (2.0 * math.pi)


def amplitude_diagnostic(candidate):
    return {
        "candidate_common_amplitude": candidate["common_amplitude"],
        "single_geometric_level_amplitude": geometric_single_level_amplitude,
        "effective_geometric_level_units": (
            candidate["common_amplitude"] / geometric_single_level_amplitude
        ),
    }


minimal_best = minimal_split_search[0]
larger_best = larger_split_search[0]
extended_best = extended_search[0]

results = {
    "status": "complete_multiplet_KK_rays_fail_split_singlet_direction_matches_but_tower_origin_open",
    "date": "2026-08-04",
    "required_low_energy_threshold_vector": {
        "scheme": (
            "tree-level physical proxy after fixing v from G_F; components are inverse-alpha shifts for gY,g2,g3"
        ),
        "signed_shifts_Y_2_3": required_signed_shifts.tolist(),
        "magnitudes_Y_2_3": required_magnitudes.tolist(),
        "normalized_to_SU2": (required_magnitudes / required_magnitudes[1]).tolist(),
    },
    "representation_conventions": {
        "vectors": {
            name: vector.tolist() for name, vector in beta_vectors.items()
        },
        "meaning": (
            "one-loop matter beta directions in the gY,g2,g3 normalization; only the direction is tested"
        ),
    },
    "frozen_candidate_rays": ray_rows,
    "inverse_diagnostic_search": {
        "warning": (
            "integer searches use the target and are diagnostics of missing representation content, not predictions"
        ),
        "best_total_count_at_most_4": minimal_best,
        "best_U_D_H_counts_0_to_6": larger_best,
        "best_extended_counts_0_to_6": extended_best,
    },
    "geometric_magnitude_gate": {
        "rho_S2T": RHO_S2T,
        "log_rho": math.log(RHO_S2T),
        "single_level_amplitude_abs_log_rho_over_2pi": geometric_single_level_amplitude,
        "minimal_split_candidate": amplitude_diagnostic(minimal_best),
        "larger_split_candidate": amplitude_diagnostic(larger_best),
        "extended_candidate": amplitude_diagnostic(extended_best),
        "finding": (
            "one geometric splitting unit is too small; a regulated tower equivalent to roughly 7-35 coherent units is required, depending on representation multiplicity"
        ),
    },
    "sector_diagnosis": {
        "complete_generation": (
            "fails directionally because it carries far too much SU2 relative to the required correction"
        ),
        "split_hint": (
            "the low-complexity U+2D+H ray has beta ratio 17:1:12 versus the required 16.91:1:11.01"
        ),
        "physical_interpretation": (
            "any viable KK sector must be strongly split by holonomy or boundary conditions, retaining hypercharged/color SU2 singlets while suppressing doublet partners"
        ),
        "remaining_obligation": (
            "derive this split from an anomaly-free parent representation and compute the regulated KK threshold sum before comparison"
        ),
    },
    "verdict": (
        "The first no-fit representation gate is negative for complete multiplet replicas: their threshold direction cannot repair the observed gauge residual vector. "
        "A simple split ray U+2D+H nearly matches the direction, which is a useful structural hint but not evidence because it was identified after the residual vector was known. "
        "Its magnitude also requires a multi-level coherent KK contribution. The next legitimate model must derive an anomaly-free holonomy projection that creates this split and then predict the finite tower sum without fitting."
    ),
}

assert ray_rows["one_complete_generation"]["max_abs_relative_residual"] > 7.0
assert ray_rows["split_U_plus_2D_plus_H"]["max_abs_relative_residual"] < 0.06
assert minimal_best["counts"] == {"U": 1, "D": 2, "H": 1}
assert extended_best["max_abs_relative_residual"] < 0.02

Path("s2t_kk_representation_cone_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "required_ratio_Y_2_3": results[
                "required_low_energy_threshold_vector"
            ]["normalized_to_SU2"],
            "complete_generation_max_residual": ray_rows[
                "one_complete_generation"
            ]["max_abs_relative_residual"],
            "split_U_2D_H_max_residual": ray_rows[
                "split_U_plus_2D_plus_H"
            ]["max_abs_relative_residual"],
            "minimal_split_effective_level_units": amplitude_diagnostic(minimal_best)[
                "effective_geometric_level_units"
            ],
        },
        indent=2,
        ensure_ascii=False,
    )
)