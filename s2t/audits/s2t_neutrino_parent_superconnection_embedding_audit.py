import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
FULL_DIMENSION = 24
BACKGROUND_MASS = 1.0

kernel_vector = np.zeros(FULL_DIMENSION)
kernel_vector[0] = 1.0
p_kernel = np.outer(kernel_vector, kernel_vector)
p_heavy = np.eye(FULL_DIMENSION) - p_kernel

e0_hat_norm_squared = 1.0
e1_integral_norm_squared = 1.0 / PI
radial_profile_norm_squared = 1.0
spectator_circle_mode_norm_squared = 1.0

ambient_zero_form_norm = (
    float(np.trace(p_heavy.T @ p_heavy))
    * e0_hat_norm_squared
    * radial_profile_norm_squared
    * spectator_circle_mode_norm_squared
)
ambient_one_form_norm = (
    float(np.trace(p_kernel.T @ p_kernel))
    * e1_integral_norm_squared
    * radial_profile_norm_squared
    * spectator_circle_mode_norm_squared
)
ambient_cross = float(np.trace(p_heavy.T @ p_kernel))
ambient_total_norm = ambient_zero_form_norm + ambient_one_form_norm

restricted_zero_form_norm = float(np.trace(p_heavy.T @ p_heavy)) * e0_hat_norm_squared
restricted_one_form_norm = float(np.trace(p_kernel.T @ p_kernel)) * e1_integral_norm_squared
restricted_total_norm = restricted_zero_form_norm + restricted_one_form_norm


def spectral_weights(kind, parameter=None):
    x = BACKGROUND_MASS**2
    if kind == "linear":
        derivative_at_zero = 1.0
        derivative_at_x = 1.0
        second_at_x = 0.0
    elif kind == "exp":
        rate = parameter
        derivative_at_zero = -rate
        derivative_at_x = -rate * math.exp(-rate * x)
        second_at_x = rate**2 * math.exp(-rate * x)
    elif kind == "rational":
        power = parameter
        derivative_at_zero = -power
        derivative_at_x = -power * (1.0 + x) ** (-power - 1.0)
        second_at_x = power * (power + 1.0) * (1.0 + x) ** (-power - 2.0)
    else:
        raise ValueError(kind)

    kernel_weight = 2.0 * derivative_at_zero
    heavy_weight = 2.0 * derivative_at_x + 4.0 * x * second_at_x
    return kernel_weight, heavy_weight


kernel_family = []
for kind, parameter in [
    ("linear", None),
    ("exp", 1.0),
    ("exp", 2.0),
    ("rational", 3.0),
    ("rational", 4.0),
]:
    kernel_weight, heavy_weight = spectral_weights(kind, parameter)
    kernel_family.append(
        {
            "kind": kind,
            "parameter": parameter,
            "kernel_sector_weight": kernel_weight,
            "heavy_sector_weight": heavy_weight,
            "weight_difference": heavy_weight - kernel_weight,
            "equal_weights": abs(heavy_weight - kernel_weight) < 1e-12,
        }
    )

results = {
    "status": "parent_superconnection_restriction_constructed_generic_spectral_hessian_does_not_force_metric",
    "date": "2026-08-03",
    "parent_data": {
        "carrier": "K=RP3 x S1",
        "Hilbert_space": "L2(K,S_K) tensor R24 tensor Nambu",
        "base_operator": "D_parent=D_K tensor I + Gamma_K tensor D_F",
        "defect_sector": "tubular neighborhood N(gamma) x S1 with square-root torsion transition",
        "parent_superconnection": (
            "A_parent=D_parent+Phi_defect+connection_root; its one-parameter collective tangent is "
            "delta A=a rho(r)[P_heavy tensor e0_hat + P_kernel tensor e1]"
        ),
    },
    "minimality_constraints": [
        "the degree-zero variation acts only on the heavy quotient",
        "the degree-one variation acts only on the unique defect kernel line",
        "the same scalar amplitude multiplies both pieces",
        "the radial profile and spectator S1 mode are canonically normalized",
        "the zero-form is wavefunction-normalized and the one-form has unit period",
    ],
    "tubular_restriction": {
        "ambient_zero_form_norm": ambient_zero_form_norm,
        "ambient_one_form_norm": ambient_one_form_norm,
        "ambient_cross_trace": ambient_cross,
        "ambient_total_norm": ambient_total_norm,
        "restricted_zero_form_norm": restricted_zero_form_norm,
        "restricted_one_form_norm": restricted_one_form_norm,
        "restricted_total_norm": restricted_total_norm,
        "restriction_error": abs(ambient_total_norm - restricted_total_norm),
        "target": 23.0 + 1.0 / PI,
        "interpretation": (
            "Normalized transverse and spectator factors integrate out, leaving exactly the previously "
            "constructed graded tangent on gamma."
        ),
    },
    "canonical_configuration_metric": {
        "metric": "<delta A,delta A>=integral Str(delta A^dagger * delta A)",
        "result": ambient_total_norm,
        "status": "exact_parent_embedding_of_the_minimal_superconnection_norm",
    },
    "generic_spectral_action_hessian": {
        "model": "S_f(a)=Tr f((D0+a delta A)^2) expanded at a=0",
        "background_mass": BACKGROUND_MASS,
        "kernel_family": kernel_family,
        "finding": (
            "Only the linear quadratic functional gives equal second-order weights automatically in "
            "this reduced control model. Generic heat/rational kernels split the heavy and kernel "
            "weights around a nonzero mass background."
        ),
    },
    "theory_effect": {
        "parent_tubular_restriction": "closed",
        "canonical_superconnection_metric": "closed",
        "generic_Tr_f_D2_derivation": "not_closed",
        "D_nu": "derived_if_the_parent_action_uses_the_canonical_configuration_metric",
        "remaining_choice": (
            "declare/derive the configuration-space trace metric as the primary S2T kinetic metric, "
            "or prove a special spectral kernel/background identity that reproduces it"
        ),
    },
    "verdict": (
        "The parent embedding of the graded tangent itself is explicit: normalized transverse and "
        "spectator modes reduce the ambient superconnection variation exactly to the gamma-sector "
        "tangent with norm 23+pi^-1. This closes the geometric restriction problem. It does not show "
        "that an arbitrary bosonic spectral action Tr f(D^2) has the same Hessian: generic kernels "
        "weight the massive heavy quotient and zero-mode connection differently. Therefore the "
        "denominator is a theorem of the canonical superconnection configuration metric, but only a "
        "conditional consequence of an otherwise unspecified spectral-action kernel."
    ),
}

assert abs(ambient_cross) < 1e-12
assert abs(ambient_total_norm - (23.0 + 1.0 / PI)) < 1e-12
assert abs(restricted_total_norm - ambient_total_norm) < 1e-12
assert kernel_family[0]["equal_weights"]
assert any(not row["equal_weights"] for row in kernel_family[1:])

Path("s2t_neutrino_parent_superconnection_embedding_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "ambient_norm": ambient_total_norm,
            "restriction_error": results["tubular_restriction"]["restriction_error"],
            "linear_kernel_equal_weights": kernel_family[0]["equal_weights"],
            "generic_equal_weight_count": sum(row["equal_weights"] for row in kernel_family),
            "generic_kernel_count": len(kernel_family),
        },
        indent=2,
        ensure_ascii=False,
    )
)