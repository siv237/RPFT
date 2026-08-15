import json
import math
from fractions import Fraction


inputs = {
    "alpha_em_inverse_MZ": 127.955,
    "sin2_thetaW_MSbar_MZ": 0.23122,
    "alpha_s_MSbar_MZ": 0.1180,
    "MZ_GeV": 91.1876,
}

beta_sm = {
    "1": Fraction(41, 10),
    "2": Fraction(-19, 6),
    "3": Fraction(-7, 1),
}

indices = {
    "Q": {"1": Fraction(1, 10), "2": Fraction(3, 2), "3": Fraction(1, 1)},
    "u_c": {"1": Fraction(4, 5), "2": Fraction(0, 1), "3": Fraction(1, 2)},
    "e_c": {"1": Fraction(3, 5), "2": Fraction(0, 1), "3": Fraction(0, 1)},
    "d_c": {"1": Fraction(1, 5), "2": Fraction(0, 1), "3": Fraction(1, 2)},
    "L": {"1": Fraction(3, 10), "2": Fraction(1, 2), "3": Fraction(0, 1)},
    "nu_c": {"1": Fraction(0, 1), "2": Fraction(0, 1), "3": Fraction(0, 1)},
}

charges = {
    "Y": {
        "Q": Fraction(1, 6),
        "u_c": Fraction(-2, 3),
        "e_c": Fraction(1, 1),
        "d_c": Fraction(1, 3),
        "L": Fraction(-1, 2),
        "nu_c": Fraction(0, 1),
    },
    "B-L": {
        "Q": Fraction(1, 3),
        "u_c": Fraction(-1, 3),
        "e_c": Fraction(1, 1),
        "d_c": Fraction(-1, 3),
        "L": Fraction(-1, 1),
        "nu_c": Fraction(1, 1),
    },
    "T3R": {
        "Q": Fraction(0, 1),
        "u_c": Fraction(-1, 2),
        "e_c": Fraction(1, 2),
        "d_c": Fraction(1, 2),
        "L": Fraction(0, 1),
        "nu_c": Fraction(-1, 2),
    },
}


def alpha_inverse_values():
    alpha = 1 / inputs["alpha_em_inverse_MZ"]
    sin2_theta = inputs["sin2_thetaW_MSbar_MZ"]
    return {
        "1": Fraction(3, 5) * (1 - sin2_theta) / alpha,
        "2": sin2_theta / alpha,
        "3": 1 / inputs["alpha_s_MSbar_MZ"],
    }


def threshold_direction(weights, copies):
    component_beta = {
        field: {
            group: Fraction(4 * copies, 3) * value
            for group, value in group_indices.items()
        }
        for field, group_indices in indices.items()
    }
    return {
        pair: sum(
            (component_beta[field][pair[0]] - component_beta[field][pair[1]])
            * weights[field]
            for field in indices
        )
        for pair in ("12", "13")
    }


def solve_quadratic_direction(generator, copies, alpha_inverse):
    weights = {field: charge**2 for field, charge in charges[generator].items()}
    direction = threshold_direction(weights, copies)
    b12 = float(beta_sm["1"] - beta_sm["2"])
    b13 = float(beta_sm["1"] - beta_sm["3"])
    s12 = float(direction["12"])
    s13 = float(direction["13"])
    rhs12 = 2 * math.pi * (alpha_inverse["1"] - alpha_inverse["2"])
    rhs13 = 2 * math.pi * (alpha_inverse["1"] - alpha_inverse["3"])
    determinant = b13 * s12 - b12 * s13
    log_mu = (rhs13 * s12 - rhs12 * s13) / determinant
    eta = (b12 * rhs13 - b13 * rhs12) / determinant
    weight_values = [float(value) for value in weights.values()]
    log_spread = abs(eta) * (max(weight_values) - min(weight_values))
    return {
        "copies": copies,
        "direction_S12": str(direction["12"]),
        "direction_S13": str(direction["13"]),
        "log_mu_over_MZ": log_mu,
        "unification_scale_GeV": inputs["MZ_GeV"] * math.exp(log_mu),
        "fitted_eta": eta,
        "minimum_mass_spread": math.exp(log_spread),
    }


alpha_inverse = alpha_inverse_values()
linear_directions = {
    generator: {
        pair: str(value)
        for pair, value in threshold_direction(generator_charges, copies=1).items()
    }
    for generator, generator_charges in charges.items()
}
quadratic_solutions = {
    generator: {
        str(copies): solve_quadratic_direction(generator, copies, alpha_inverse)
        for copies in (1, 2)
    }
    for generator in charges
}

result = {
    "gate": "version4_boundary_threshold_splitting",
    "mass_ansatz": "log(M_a/M0)=eta*q_a or eta*q_a^2",
    "linear_generator_directions": linear_directions,
    "all_linear_directions_vanish": all(
        value == "0"
        for direction in linear_directions.values()
        for value in direction.values()
    ),
    "linear_cancellation_origin": "mixed gauge-gauge-generator anomaly cancellation in a complete SO10 spinor",
    "quadratic_generator_solutions": quadratic_solutions,
    "two_pair_mass_spreads": {
        generator: solution["2"]["minimum_mass_spread"]
        for generator, solution in quadratic_solutions.items()
    },
    "status": "linear single-generator splitting is invisible to one-loop coupling differences; quadratic repair is fitted and requires large component hierarchies",
}

with open("s2t_v4_boundary_threshold_splitting_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))