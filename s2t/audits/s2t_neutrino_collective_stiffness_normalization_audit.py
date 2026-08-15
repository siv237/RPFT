import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
ME_MEV = 0.51099895069
MMU_MEV = 105.6583755

full_dimension = 24
kernel_vector = np.zeros(full_dimension)
kernel_vector[0] = 1.0
p_kernel = np.outer(kernel_vector, kernel_vector)
p_heavy = np.eye(full_dimension) - p_kernel

heavy_rank = int(np.linalg.matrix_rank(p_heavy))
hilbert_schmidt_norm_squared = float(np.trace(p_heavy.T @ p_heavy))
dual_cycle_norm_squared = 1.0 / PI
collective_norm_squared = hilbert_schmidt_norm_squared + dual_cycle_norm_squared

qcycle_factor = PI + 1.0 / PI
base_dirac_scale_mev = ME_MEV**2 / MMU_MEV
heavy_base_scale_mev = MMU_MEV

normalized_collective_overlap = 1.0 / math.sqrt(collective_norm_squared)
effective_inverse_stiffness = normalized_collective_overlap**2 / heavy_base_scale_mev
mu_mev = qcycle_factor * base_dirac_scale_mev**2 * effective_inverse_stiffness
mu_ev = mu_mev * 1e6


def integrate_auxiliary(stiffness, coupling, source=1.0):
    stationary_amplitude = -coupling * source / stiffness
    effective_action = -0.5 * coupling**2 * source**2 / stiffness
    return stationary_amplitude, effective_action


auxiliary_stiffness = heavy_base_scale_mev * collective_norm_squared
auxiliary_coupling = math.sqrt(qcycle_factor) * base_dirac_scale_mev
stationary_amplitude, effective_action = integrate_auxiliary(
    auxiliary_stiffness,
    auxiliary_coupling,
)

rescaling_checks = []
for scale in [0.25, 0.5, 2.0, 4.0]:
    rescaled_stiffness = auxiliary_stiffness / scale**2
    rescaled_coupling = auxiliary_coupling / scale
    _, rescaled_effective_action = integrate_auxiliary(
        rescaled_stiffness,
        rescaled_coupling,
    )
    rescaling_checks.append(
        {
            "field_rescaling": scale,
            "effective_action": rescaled_effective_action,
            "difference": rescaled_effective_action - effective_action,
        }
    )

weight_scenarios = []
for heavy_weight, cycle_weight in [
    (1.0, 1.0),
    (2.0, 1.0),
    (1.0, 2.0),
    (0.5, 1.0),
    (1.0, 0.5),
]:
    weighted_norm = (
        heavy_weight * hilbert_schmidt_norm_squared
        + cycle_weight * dual_cycle_norm_squared
    )
    weighted_mu_ev = (
        qcycle_factor
        * base_dirac_scale_mev**2
        / (heavy_base_scale_mev * weighted_norm)
        * 1e6
    )
    weight_scenarios.append(
        {
            "heavy_weight": heavy_weight,
            "cycle_weight": cycle_weight,
            "D_effective": weighted_norm,
            "mu_nu_eV": weighted_mu_ev,
        }
    )

results = {
    "status": "collective_stiffness_recovers_Dnu_with_common_unweighted_metric_relative_weight_derivation_open",
    "date": "2026-08-03",
    "collective_tangent": {
        "definition": "Xi=(P_heavy,e1_dual) in End(R24) direct_sum Omega1(gamma)",
        "heavy_projector_rank": heavy_rank,
        "Hilbert_Schmidt_norm_squared": hilbert_schmidt_norm_squared,
        "dual_cycle_Hodge_norm_squared": dual_cycle_norm_squared,
        "common_product_norm_squared": collective_norm_squared,
        "target": 23.0 + 1.0 / PI,
        "error": abs(collective_norm_squared - (23.0 + 1.0 / PI)),
    },
    "auxiliary_collective_action": {
        "action": "S[a]=(M_*/2)||Xi||^2 a^2 + y_cycle a J_nu",
        "interpretation": (
            "a is the non-propagating collective amplitude of the Majorana pairing deformation, "
            "not an additional fitted particle."
        ),
        "stiffness_MeV": auxiliary_stiffness,
        "coupling_MeV": auxiliary_coupling,
        "stationary_amplitude": stationary_amplitude,
        "effective_action_coefficient": effective_action,
        "integrated_out_rule": "Delta S_eff=-(y_cycle^2/(2 M_* ||Xi||^2)) J_nu^2",
    },
    "normalization_mechanism": {
        "normalized_collective_overlap": normalized_collective_overlap,
        "two_vertex_factor": normalized_collective_overlap**2,
        "effective_inverse_stiffness_per_MeV": effective_inverse_stiffness,
        "consequence": (
            "The rank enters through canonical normalization of one collective deformation. It is "
            "neither a heavy mass eigenvalue nor an unnormalized sum over 23 propagators."
        ),
    },
    "neutrino_scale": {
        "Qcycle_factor": qcycle_factor,
        "base_Dirac_scale_MeV": base_dirac_scale_mev,
        "heavy_base_scale_MeV": heavy_base_scale_mev,
        "D_nu": collective_norm_squared,
        "mu_nu_eV": mu_ev,
        "dm21_eV2": mu_ev**2,
        "R_nu": collective_norm_squared + PI**2 + 2.0 / 3.0,
        "dm31_eV2": (collective_norm_squared + PI**2 + 2.0 / 3.0) * mu_ev**2,
    },
    "field_rescaling_test": {
        "reference_effective_action": effective_action,
        "checks": rescaling_checks,
        "max_error": max(abs(row["difference"]) for row in rescaling_checks),
        "interpretation": (
            "Rescaling the auxiliary coordinate changes stiffness and coupling together but leaves "
            "the induced operator invariant. The denominator is not a coordinate-normalization artifact."
        ),
    },
    "relative_metric_weight_gate": {
        "scenarios": weight_scenarios,
        "canonical_choice": "heavy_weight=cycle_weight=1",
        "open_issue": (
            "A general product metric alpha*Tr(delta M^2)+beta*||delta A||^2 contains a relative "
            "weight alpha/beta. Exact D_nu follows only if the same spectral trace fixes alpha=beta."
        ),
        "no_fit_requirement": (
            "derive the common unweighted metric from a single superconnection/spectral-action trace; "
            "do not select equal weights from the neutrino data"
        ),
    },
    "comparison_with_previous_gate": {
        "previous_no_go": (
            "rank 23 does not become a tree-level mass eigenvalue and does not belong directly in M_H"
        ),
        "resolution": (
            "use the Hilbert-Schmidt plus Hodge norm of the collective pairing deformation, so two "
            "normalized vertices supply 1/(23+pi^-1)"
        ),
        "compatibility": "the previous no-go is retained rather than contradicted",
    },
    "theory_effect": {
        "D_nu": "recovered_conditionally_as_collective_stiffness_norm",
        "rank23": "used_as_Hilbert_Schmidt_norm_of_P_heavy",
        "inverse_pi": "used_as_Hodge_norm_of_the_dual_cycle_generator",
        "continuous_fit_parameter_added": False,
        "remaining_gate": "derive equal relative weights from one S2T superconnection trace",
    },
    "verdict": (
        "A non-tautological action-level route to D_nu exists. The canonical collective deformation "
        "Xi=(P_heavy,e1_dual) has squared product norm Tr(P_heavy^2)+||e1||^2=23+pi^-1. "
        "Integrating out its auxiliary amplitude, or equivalently normalizing its single collective "
        "mode, gives the desired inverse denominator while respecting the earlier tree-level no-go. "
        "The remaining structural obligation is to derive the equal Hilbert-Schmidt/Hodge weighting "
        "from a single spectral or superconnection action rather than assume it."
    ),
}

assert heavy_rank == 23
assert abs(hilbert_schmidt_norm_squared - 23.0) < 1e-12
assert abs(collective_norm_squared - (23.0 + 1.0 / PI)) < 1e-12
assert abs(mu_ev - 0.008576992731264175) < 1e-12
assert max(abs(row["difference"]) for row in rescaling_checks) < 1e-18

Path("s2t_neutrino_collective_stiffness_normalization_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "HS_norm_squared": hilbert_schmidt_norm_squared,
            "cycle_norm_squared": dual_cycle_norm_squared,
            "D_nu": collective_norm_squared,
            "mu_nu_eV": mu_ev,
            "rescaling_max_error": results["field_rescaling_test"]["max_error"],
            "remaining_gate": results["theory_effect"]["remaining_gate"],
        },
        indent=2,
        ensure_ascii=False,
    )
)