import contextlib
import io
import itertools
import json
import runpy

import numpy as np
import sympy as sp
from scipy.optimize import differential_evolution, minimize_scalar


def chiral_matrix(theta, radius=1.0):
    connector = radius * np.exp(-1j * theta)
    return np.array(
        [
            [0, 0, 0, connector, 0, 0],
            [0, 0.5, -0.5, 0, connector, 0],
            [0, -0.5, 0.5, 0, 0, connector],
            [0, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1, 0],
            [0, 0, 1, 1, 0, 0],
        ],
        dtype=complex,
    )


def squared_spectrum(theta):
    matrix = chiral_matrix(theta)
    return np.linalg.eigvalsh(matrix @ matrix.conj().T)


z, c, y = sp.symbols("z c y", nonzero=True, real=True)
symbolic_chiral = sp.Matrix(
    [
        [0, 0, 0, 1 / z, 0, 0],
        [0, sp.Rational(1, 2), -sp.Rational(1, 2), 0, 1 / z, 0],
        [0, -sp.Rational(1, 2), sp.Rational(1, 2), 0, 0, 1 / z],
        [0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0],
        [0, 0, 1, 1, 0, 0],
    ]
)
symbolic_hamiltonian = sp.simplify(
    symbolic_chiral * symbolic_chiral.T.subs(z, 1 / z)
)


def laurent_to_cosine(expression):
    terms = {}
    for term in sp.Add.make_args(sp.expand(expression)):
        coefficient, power = term.as_coeff_exponent(z)
        terms[int(power)] = terms.get(int(power), 0) + coefficient
    result = terms.get(0, 0)
    for power in range(1, max(abs(index) for index in terms) + 1):
        positive = sp.simplify(terms.get(power, 0))
        negative = sp.simplify(terms.get(-power, 0))
        if sp.simplify(positive - negative) != 0:
            raise ValueError("non-real Laurent trace")
        result += 2 * positive * sp.chebyshevt(power, c)
    return sp.factor(result)


characteristic = symbolic_hamiltonian.charpoly(y).as_expr()
characteristic_cosine = 0
for (power,), coefficient in sp.Poly(characteristic, y).terms():
    characteristic_cosine += laurent_to_cosine(coefficient) * y**power
characteristic_cosine = sp.factor(characteristic_cosine)

moment_polynomials = {}
power_matrix = sp.eye(6)
for order in range(1, 9):
    power_matrix = sp.simplify(power_matrix * symbolic_hamiltonian)
    moment_polynomials[str(2 * order)] = str(
        laurent_to_cosine(2 * sp.trace(power_matrix))
    )


def spectral_value(profile, scale, theta):
    eigenvalues = squared_spectrum(theta)
    if profile == "heat":
        values = np.exp(-scale * eigenvalues)
    elif profile == "gaussian":
        values = np.exp(-scale * eigenvalues**2)
    elif profile == "heat2":
        values = (1 + scale * eigenvalues) * np.exp(-scale * eigenvalues)
    else:
        raise ValueError(profile)
    return float(2 * np.sum(values))


def local_even_coefficients(profile, scale):
    angles = np.linspace(0, 0.08, 33)
    values = np.array(
        [
            spectral_value(profile, scale, angle)
            - spectral_value(profile, scale, 0)
            for angle in angles
        ]
    )
    design = np.column_stack(
        [angles**2, angles**4, angles**6, angles**8]
    )
    return np.linalg.lstsq(design, values, rcond=None)[0]


profile_rows = {}
for profile in ("heat", "gaussian", "heat2"):
    scales = np.logspace(-3, 3, 121)
    interior_minimum_found = False
    endpoint_choices = set()
    for scale in scales:
        grid = np.linspace(0, np.pi, 2001)
        values = np.array(
            [spectral_value(profile, scale, angle) for angle in grid]
        )
        minimum_angle = float(grid[int(np.argmin(values))])
        if 1e-3 < minimum_angle < np.pi - 1e-3:
            interior_minimum_found = True
        endpoint_choices.add(
            "zero" if minimum_angle < np.pi / 2 else "pi"
        )
    profile_rows[profile] = {
        "unit_scale_even_coefficients": local_even_coefficients(
            profile, 1.0
        ).tolist(),
        "interior_minimum_found_on_scale_scan": interior_minimum_found,
        "endpoint_choices": sorted(endpoint_choices),
    }

critical_scales = {
    "gaussian": 0.13632819354805842,
    "heat2": 0.550813793906306,
}
critical_coefficients = {
    profile: local_even_coefficients(profile, scale).tolist()
    for profile, scale in critical_scales.items()
}


counterexample_weight = 1 / 12


def counterexample_profile(eigenvalues):
    return (
        np.exp(-eigenvalues**2 / 100)
        + counterexample_weight * np.exp(-10 * eigenvalues**2)
    ) / (1 + counterexample_weight)


def counterexample_value(theta):
    return float(2 * np.sum(counterexample_profile(squared_spectrum(theta))))


counterexample_fit = minimize_scalar(
    counterexample_value,
    bounds=(0, np.pi),
    method="bounded",
    options={"xatol": 1e-14},
)
counterexample_theta = float(counterexample_fit.x)
counterexample_amplitude = float(np.sin(counterexample_theta))


namespace_output = io.StringIO()
with contextlib.redirect_stdout(namespace_output):
    pfaffian_namespace = runpy.run_path(
        "s2t_v4_pfaffian_stiffness_gate.py"
    )

modular_roots = pfaffian_namespace["modular_roots"]
candidate_data = pfaffian_namespace["candidate_data"]
mass_objective = pfaffian_namespace["mass_objective"]
mass_targets = pfaffian_namespace["mass_targets"]
ckm_target = pfaffian_namespace["ckm_target"]
ckm_jarlskog_target = pfaffian_namespace["ckm_jarlskog_target"]

branch_rows = []
for orientation_sign in (-1, 1):
    roots = modular_roots(orientation_sign * counterexample_amplitude)
    for placement in ("left_gns", "right_gns", "kms_symmetric"):
        sign_rows = []
        for sign_bits in itertools.product((-1, 1), repeat=4):
            fit = differential_evolution(
                lambda value: mass_objective(
                    value[0], placement, sign_bits, roots
                ),
                [(-10, 15)],
                seed=1729,
                tol=1e-9,
                polish=True,
            )
            sign_rows.append(
                {
                    "sign_bits": list(sign_bits),
                    "messenger_ratio": float(1 + np.exp(fit.x[0])),
                    "mass_log_rms": float(fit.fun),
                }
            )
        sign_rows.sort(key=lambda row: row["mass_log_rms"])
        branch_rows.append(
            {
                "orientation_sign": orientation_sign,
                "placement": placement,
                **sign_rows[0],
            }
        )

branch_rows.sort(key=lambda row: row["mass_log_rms"])
best = branch_rows[0]
best_roots = modular_roots(
    best["orientation_sign"] * counterexample_amplitude
)
best_data = candidate_data(
    best["placement"],
    best["messenger_ratio"],
    best["sign_bits"],
    best_roots,
)
ckm = best_data["u"]["left_eigenvectors"].conj().T @ best_data["d"][
    "left_eigenvectors"
]
ckm_absolute = np.abs(ckm)
ckm_angles = np.array(
    [ckm_absolute[0, 1], ckm_absolute[1, 2], ckm_absolute[0, 2]]
)
jarlskog = np.imag(
    ckm[0, 0]
    * ckm[1, 1]
    * np.conj(ckm[0, 1])
    * np.conj(ckm[1, 0])
)
mass_errors = {}
for sector in ("u", "d"):
    ratios = best_data[sector]["normalized_masses"][:2] / mass_targets[sector][:2]
    mass_errors[sector] = np.maximum(ratios, 1 / ratios).tolist()

output = {
    "gate": "version4_full_spectral_profile_global",
    "characteristic_polynomial_d_squared": str(characteristic_cosine),
    "even_moment_polynomials": moment_polynomials,
    "general_theta_expansion": (
        "S_f(theta)=F_f(1)-F_f'(1) theta^2/2+"
        "(F_f'(1)/24+F_f''(1)/8) theta^4+O(theta^6)"
    ),
    "positive_f_alone_fixes_quartic_sign": False,
    "profile_rows": profile_rows,
    "critical_scales": critical_scales,
    "critical_even_coefficients": critical_coefficients,
    "positive_counterexample_profile": (
        "f(u)=[exp(-u^2/100)+(1/12)exp(-10u^2)]/(13/12)"
    ),
    "counterexample_unit_radial_slice": {
        "theta_minimum": counterexample_theta,
        "cp_conjugate_minima": [-counterexample_theta, counterexample_theta],
        "orientation_amplitude": counterexample_amplitude,
        "energy_gap_from_zero": float(
            counterexample_value(0) - counterexample_fit.fun
        ),
        "energy_gap_from_pi": float(
            counterexample_value(np.pi) - counterexample_fit.fun
        ),
    },
    "counterexample_is_profile_selector": False,
    "counterexample_branch_rows": branch_rows,
    "counterexample_mass_selected_best": best,
    "counterexample_normalized_masses": {
        sector: best_data[sector]["normalized_masses"].tolist()
        for sector in ("u", "d", "e", "nu")
    },
    "counterexample_mass_errors": mass_errors,
    "counterexample_ckm_absolute": ckm_absolute.tolist(),
    "counterexample_ckm_angles": ckm_angles.tolist(),
    "counterexample_ckm_angle_ratios": (ckm_angles / ckm_target).tolist(),
    "counterexample_jarlskog": float(jarlskog),
    "counterexample_jarlskog_ratio": abs(jarlskog) / ckm_jarlskog_target,
    "verdict": (
        "the structural CP no-go is false for an unspecified positive full "
        "spectral function: a smooth positive profile can create conjugate "
        "interior angular minima, but the profile is not selected by the "
        "current theory and therefore does not constitute a prediction"
    ),
}

with open(
    "s2t_v4_full_spectral_profile_global_gate_results.json",
    "w",
    encoding="utf-8",
) as handle:
    json.dump(output, handle, ensure_ascii=False, indent=2)

print(json.dumps(output, ensure_ascii=False, indent=2))