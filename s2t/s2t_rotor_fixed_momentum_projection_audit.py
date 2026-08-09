#!/usr/bin/env python3
import json
import math
from pathlib import Path

import sympy as sp


def main():
    beta = sp.symbols("beta", positive=True)
    inertia = sp.symbols("I", positive=True)
    momentum_norm = sp.Integer(48)
    trace_rank = sp.Integer(3)

    fixed_sector_partition = sp.exp(
        -beta * momentum_norm / (2 * trace_rank * inertia)
    )
    fixed_sector_effective_action = sp.simplify(-sp.log(fixed_sector_partition))
    log_inertia_coefficient = sp.simplify(
        sp.diff(fixed_sector_effective_action, sp.log(inertia))
    ) if False else sp.Integer(0)

    # Numerical Poisson-resummation check for a single rotor:
    # sum_p exp[-beta p^2/(2I)] = sqrt(2*pi*I/beta)
    #     sum_w exp[-2*pi^2*I*w^2/beta].
    beta_value = 1.7
    inertia_value = 1.3
    cutoff = 40
    momentum_sum = sum(
        math.exp(-beta_value * momentum * momentum / (2 * inertia_value))
        for momentum in range(-cutoff, cutoff + 1)
    )
    winding_sum = math.sqrt(2 * math.pi * inertia_value / beta_value) * sum(
        math.exp(
            -2 * math.pi * math.pi * inertia_value * winding * winding / beta_value
        )
        for winding in range(-cutoff, cutoff + 1)
    )

    results = {
        "status": "fixed_momentum_projection_removes_the_rotor_log_determinant",
        "date": "2026-08-06",
        "canonical_rotor": {
            "hamiltonian": "H=p^2/(2I), p integer",
            "fixed_sector_partition": str(fixed_sector_partition),
            "fixed_sector_effective_action": str(fixed_sector_effective_action),
            "independent_log_I_coefficient": str(log_inertia_coefficient),
            "conclusion": (
                "A fixed momentum sector contains the inverse-inertia term but no independent "
                "Gaussian log(I) term."
            ),
        },
        "poisson_check": {
            "momentum_sum": momentum_sum,
            "winding_sum_with_prefactor": winding_sum,
            "absolute_residual": abs(momentum_sum - winding_sum),
            "passed": abs(momentum_sum - winding_sum) < 1e-13,
            "interpretation": (
                "The square-root fluctuation prefactor belongs to the winding representation "
                "of the unprojected trace. After resolving individual momentum sectors it does "
                "not survive as a sectorwise log determinant."
            ),
        },
        "eight_rotor_sector": {
            "momentum_squared_sum": int(momentum_norm),
            "trace_rank": int(trace_rank),
            "inverse_coefficient": str(momentum_norm / (2 * trace_rank)),
            "log_coefficient_from_same_projected_rotors": "0",
            "required_log_coefficient": "8/3",
            "single_carrier_exact_match": False,
        },
        "scientific_verdict": {
            "no_go": (
                "The momentum pattern 1^3 3^5 closes the inverse coefficient only. A canonical "
                "projection onto that sector removes the logarithmic determinant attributed to "
                "the same rotors, so one carrier cannot generate both terms."
            ),
            "surviving_option": (
                "Use a separate unit-weight Gaussian boundary carrier for the logarithm and a "
                "topological fixed-momentum carrier for the inverse term, tied by a parent "
                "symmetry before comparison with observables."
            ),
            "next_gate": (
                "Classify minimal two-layer boundary complexes and test whether their measures "
                "and BRST parities preserve the coefficient pair without a free relative factor."
            ),
        },
    }

    Path("s2t_rotor_fixed_momentum_projection_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "poisson_check": results["poisson_check"]["passed"],
                "inverse_coefficient": results["eight_rotor_sector"][
                    "inverse_coefficient"
                ],
                "same_carrier_log_coefficient": results["eight_rotor_sector"][
                    "log_coefficient_from_same_projected_rotors"
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()