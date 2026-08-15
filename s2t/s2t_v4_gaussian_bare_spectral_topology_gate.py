import json
import math

import numpy as np
from scipy.optimize import brentq
from scipy.special import logsumexp


PI = math.pi
RADIUS_S4 = (3.0 / (8.0 * PI**2)) ** 0.25
RADIUS_S2 = (1.0 / (16.0 * PI**2)) ** 0.25
S4_CORRELATION_RADIUS_RATIO = 1.35139219568654


def log_dirac_heat_s4(time):
    cutoff = max(100, math.ceil(math.sqrt(100.0 * RADIUS_S4**2 / time)))
    level = np.arange(cutoff + 1, dtype=float)
    degeneracy_d_squared = 8.0 * (level + 1.0) * (level + 2.0) * (level + 3.0) / 6.0
    eigenvalue_d_squared = (level + 2.0) ** 2 / RADIUS_S4**2
    return float(logsumexp(np.log(degeneracy_d_squared) - time * eigenvalue_d_squared))


def log_dirac_heat_s2xs2(time):
    cutoff = max(100, math.ceil(math.sqrt(100.0 * RADIUS_S2**2 / time)))
    level = np.arange(cutoff + 1, dtype=float)
    degeneracy_d_squared_s2 = 4.0 * (level + 1.0)
    eigenvalue_d_squared_s2 = (level + 1.0) ** 2 / RADIUS_S2**2
    log_factor_trace = float(
        logsumexp(np.log(degeneracy_d_squared_s2) - time * eigenvalue_d_squared_s2)
    )
    return 2.0 * log_factor_trace


def traces(time):
    s4 = math.exp(log_dirac_heat_s4(time))
    s22 = math.exp(log_dirac_heat_s2xs2(time))
    return s4, s22


def difference(time):
    s4, s22 = traces(time)
    return s4 - s22


crossing = brentq(difference, 0.1, 0.2, xtol=1.0e-14)
correlation_time_unit_volume = (RADIUS_S4 / S4_CORRELATION_RADIUS_RATIO) ** 2

sample_times = [
    0.01,
    0.05,
    0.1,
    correlation_time_unit_volume,
    crossing,
    0.15,
    0.2,
    0.5,
]
samples = []
for time in sample_times:
    s4, s22 = traces(time)
    samples.append(
        {
            "time": time,
            "trace_S4": s4,
            "trace_S2xS2": s22,
            "difference_S4_minus_S2xS2": s4 - s22,
            "winner_for_positive_spectral_action": "S4" if s4 < s22 else "S2xS2",
        }
    )


result = {
    "gate": "version4_gaussian_bare_spectral_topology",
    "date": "2026-08-11",
    "normalization": "unit_four_volume",
    "spectra": {
        "S4": {
            "D_eigenvalues": "+/-(ell+2)/a",
            "D2_total_degeneracy": "8*binomial(ell+3,3)",
        },
        "S2": {
            "D_eigenvalues": "+/-(ell+1)/b",
            "D2_total_degeneracy": "4*(ell+1)",
        },
        "S2xS2": "D_product_squared=D1_squared+D2_squared and heat trace factorizes",
    },
    "gaussian_profile": {
        "f": "exp(-u)",
        "f0_a4_moment": 1.0,
        "f2_a2_moment": 1.0,
        "interpretation": "fundamental_bare_Wilsonian_spectral_action_at_the_cutoff",
    },
    "almost_commutative_factorization": {
        "operator": "D=D_M tensor 1 + gamma5 tensor D_F",
        "vacuum_condition": "D_F_constant_and_background_gauge_curvature_zero",
        "square": "D_squared=D_M_squared tensor 1 + 1 tensor D_F_squared",
        "heat_trace": "Tr exp(-t D_squared)=Tr exp(-t D_M_squared)*Tr exp(-t D_F_squared)",
        "consequence": "the_positive_finite_factor_does_not_change_the_carrier_ordering",
    },
    "quantum_supertrace_non_cancellation": {
        "bosonic_degrees": "3_scalars_plus_3_massive_vector_polarizations=6",
        "fermionic_degrees": "2_Dirac_pairs_times_4=8",
        "Str_1": -2,
        "Str_M2_over_chi2": 13,
        "Str_M4_over_chi4": 67,
        "verdict": "no_supersymmetric_cancellation_of_local_quantum_terms",
    },
    "local_a4_check_per_spinor_copy": {
        "formula": "a4=(1/(360*(4*pi)^2))*integral(11*E4-18*W2)",
        "difference_S4_minus_S2xS2": 13.0 / 90.0,
        "meaning": "the_scale_independent_a4_piece_alone_prefers_S2xS2",
    },
    "exact_heat_trace": {
        "crossing_time": crossing,
        "ordering": {
            "time_below_crossing": "S4_has_lower_positive_Gaussian_Dirac_spectral_action",
            "time_above_crossing": "S2xS2_has_lower_positive_Gaussian_Dirac_spectral_action",
        },
        "samples": samples,
    },
    "correlation_cell_map": {
        "S4_radius_unit_volume": RADIUS_S4,
        "S4_radius_over_sigma": S4_CORRELATION_RADIUS_RATIO,
        "sigma_squared_in_unit_volume_coordinates": correlation_time_unit_volume,
        "lies_below_Dirac_crossing": correlation_time_unit_volume < crossing,
        "winner_at_that_time": "S4" if difference(correlation_time_unit_volume) < 0.0 else "S2xS2",
        "warning": "this_is_a_compatibility_test_not_an_independent_scale_derivation",
    },
    "verdict": "Gaussian_bare_spectral_action_fixes_the_local_topology_weights_but_carrier_ordering_still_depends_on_the_cutoff_time",
    "reopening": "the_existing_correlation_cell_ratio_places_the_model_in_the_S4_Dirac_compatibility_window_conditionally",
}

with open("s2t_v4_gaussian_bare_spectral_topology_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps({
    "crossing_time": crossing,
    "correlation_time": correlation_time_unit_volume,
    "winner_at_correlation_time": result["correlation_cell_map"]["winner_at_that_time"],
    "difference_at_correlation_time": difference(correlation_time_unit_volume),
}, ensure_ascii=False, indent=2))