import json
import math

import numpy as np


PI = math.pi
RADIUS_S4 = (3.0 / (8.0 * PI**2)) ** 0.25
TAU = 0.1


def raw_cutoff_partial_sum(shell_cutoff):
    ell = np.arange(shell_cutoff + 1, dtype=float)
    degeneracy = (ell + 1.0) * (ell + 2.0) * (2.0 * ell + 3.0) / 6.0
    laplace_eigenvalue = ell * (ell + 3.0) / RADIUS_S4**2
    correlation_eigenvalue = np.exp(-TAU * laplace_eigenvalue)
    return float(np.sum(degeneracy * np.exp(-correlation_eigenvalue)))


shell_cutoffs = [10, 20, 40, 80]
raw_partial_sums = [
    {"shell_cutoff": cutoff, "raw_trace": raw_cutoff_partial_sum(cutoff)}
    for cutoff in shell_cutoffs
]

partition_a = 2.0
partition_b = 3.0
free_energy_direct_sum = -math.log(partition_a + partition_b)
sum_of_free_energies = -math.log(partition_a) - math.log(partition_b)

result = {
    "gate": "version4_spectral_gibbs_equivalence",
    "date": "2026-08-11",
    "raw_postulate": "Tr f(C/Lambda^2)",
    "trace_class_obstruction": "if_C_has_infinite_rank_and_f(0)_is_nonzero_then_f(C/Lambda^2)_is_not_trace_class",
    "example_cutoff": "f(u)=exp(-u)",
    "raw_partial_sums": raw_partial_sums,
    "corrected_unbounded_generator": "H_C=-tau_inverse_log(C)=Delta",
    "corrected_spectral_action": "Tr f(H_C/Lambda^2)",
    "direct_sum_test": {
        "Z_A": partition_a,
        "Z_B": partition_b,
        "F_A_direct_sum_B": free_energy_direct_sum,
        "F_A_plus_F_B": sum_of_free_energies,
        "difference": free_energy_direct_sum - sum_of_free_energies,
    },
    "equivalence_verdict": "no_scalar_trace_function_can_equal_Gibbs_free_energy_on_all_direct_sums",
    "exact_outer_transform": "F=-tau_inverse_log(Tr C)",
    "architecture": {
        "local_EFT": "Tr f((-log C)/(tau Lambda^2))",
        "global_carrier_selection": "-tau_inverse_log Tr C",
    },
}

with open("s2t_v4_spectral_gibbs_equivalence_gate_results.json", "w", encoding="utf-8") as output:
    json.dump(result, output, ensure_ascii=False, indent=2)
    output.write("\n")

print(json.dumps(result, indent=2))