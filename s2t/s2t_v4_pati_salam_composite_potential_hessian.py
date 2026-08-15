#!/usr/bin/env python3
import json
from pathlib import Path

import numpy as np
import sympy as sp

from s2t_v4_pati_salam_first_order_kernel import dirac_from_channels


OUTPUT_PATH = Path("s2t_v4_pati_salam_composite_potential_hessian_results.json")
RANDOM_SEED = 20260813
RANDOM_TESTS = 100
TOLERANCE = 1.0e-9


def crossed_majorana(delta):
    majorana = np.zeros((8, 8), dtype=complex)
    for right_first in range(2):
        for color_first in range(4):
            row = 4 * right_first + color_first
            for right_second in range(2):
                for color_second in range(4):
                    column = 4 * right_second + color_second
                    majorana[row, column] = (
                        delta[right_first, color_second]
                        * delta[right_second, color_first]
                    )
    return majorana


def trace_invariants(delta):
    majorana = crossed_majorana(delta)
    finite_dirac = dirac_from_channels(None, majorana, None)
    half_trace_two = 0.5 * np.trace(finite_dirac @ finite_dirac).real
    half_trace_four = 0.5 * np.trace(
        finite_dirac @ finite_dirac @ finite_dirac @ finite_dirac
    ).real
    gram = delta.conj().T @ delta
    rho = np.trace(gram).real
    tau = np.trace(gram @ gram).real
    return half_trace_two, half_trace_four, rho**2, tau**2


def symbolic_potential():
    coordinates = sp.symbols("x0:16", real=True)
    delta = sp.zeros(2, 4)
    for right_index in range(2):
        for color in range(4):
            coordinate = 2 * (4 * right_index + color)
            delta[right_index, color] = (
                coordinates[coordinate] + sp.I * coordinates[coordinate + 1]
            )
    gram = delta.conjugate().T * delta
    rho = sp.trace(gram)
    tau = sp.trace(gram * gram)
    potential = -rho**2 + tau**2
    return coordinates, rho, tau, potential


def stationary_audit(coordinates, potential, nonzero_entries):
    vacuum_value = 2 ** (-sp.Rational(1, 4))
    substitution = {coordinate: 0 for coordinate in coordinates}
    for coordinate_index in nonzero_entries:
        substitution[coordinates[coordinate_index]] = vacuum_value
    gradient = [sp.simplify(sp.diff(potential, coordinate).subs(substitution)) for coordinate in coordinates]
    hessian = sp.hessian(potential, coordinates).subs(substitution)
    eigenvalues = hessian.eigenvals()
    classified = {"positive": 0, "zero": 0, "negative": 0}
    exact_eigenvalues = {}
    for eigenvalue, multiplicity in eigenvalues.items():
        value = float(sp.N(eigenvalue))
        if value > TOLERANCE:
            classified["positive"] += int(multiplicity)
        elif value < -TOLERANCE:
            classified["negative"] += int(multiplicity)
        else:
            classified["zero"] += int(multiplicity)
        exact_eigenvalues[str(eigenvalue)] = int(multiplicity)
    return {
        "nonzero_real_coordinate_indices": nonzero_entries,
        "vacuum_entry": str(vacuum_value),
        "potential_value": str(sp.simplify(potential.subs(substitution))),
        "maximum_gradient_norm": float(
            max(abs(complex(sp.N(component))) for component in gradient)
        ),
        "exact_hessian_eigenvalues": exact_eigenvalues,
        "hessian_signature": classified,
    }


def main():
    rng = np.random.default_rng(RANDOM_SEED)
    maximum_trace_two_error = 0.0
    maximum_trace_four_error = 0.0
    for _ in range(RANDOM_TESTS):
        delta = rng.normal(size=(2, 4)) + 1j * rng.normal(size=(2, 4))
        half_two, half_four, rho_square, tau_square = trace_invariants(delta)
        maximum_trace_two_error = max(
            maximum_trace_two_error, abs(half_two - rho_square)
        )
        maximum_trace_four_error = max(
            maximum_trace_four_error, abs(half_four - tau_square)
        )

    coordinates, rho, tau, potential = symbolic_potential()
    rank_one = stationary_audit(coordinates, potential, [0])
    rank_two = stationary_audit(coordinates, potential, [0, 10])
    results = {
        "random_seed": RANDOM_SEED,
        "random_trace_tests": RANDOM_TESTS,
        "physical_half_trace_identities": {
            "half_Tr_D2": "(Tr Delta^dagger Delta)^2",
            "half_Tr_D4": "(Tr (Delta^dagger Delta)^2)^2",
            "maximum_D2_identity_error": maximum_trace_two_error,
            "maximum_D4_identity_error": maximum_trace_four_error,
        },
        "normalized_potential": "V=-rho^2+tau^2",
        "definitions": {
            "rho": str(rho),
            "tau": str(tau),
        },
        "rank_one_standard_model_candidate": rank_one,
        "rank_two_preferred_stationary_point": rank_two,
        "energy_difference_rank_two_minus_rank_one": str(
            sp.simplify(
                sp.sympify(rank_two["potential_value"])
                - sp.sympify(rank_one["potential_value"])
            )
        ),
        "universal_radial_extension_no_go": {
            "potential": "f(rho)+b tau^2, b>0",
            "rank_one_radial_stationarity": "f'(p)+4 b p^3=0",
            "orthogonal_rank_growth_coefficient": "f'(p)=-4 b p^3<0",
            "conclusion": "a norm-only singlet cannot stabilize rank one",
        },
        "required_repair": (
            "derive a representation-sensitive rank selector, for example an independent "
            "det(Delta Delta^dagger) invariant or a connected adjoint coupling"
        ),
    }
    OUTPUT_PATH.write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()