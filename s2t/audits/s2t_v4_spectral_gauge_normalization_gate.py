import itertools
import json
import math
from fractions import Fraction


trace_contributions = {
    "Q_L": {"Y2": Fraction(1, 6), "SU2": Fraction(3, 2), "SU3": Fraction(1, 1)},
    "u_R": {"Y2": Fraction(4, 3), "SU2": Fraction(0, 1), "SU3": Fraction(1, 2)},
    "d_R": {"Y2": Fraction(1, 3), "SU2": Fraction(0, 1), "SU3": Fraction(1, 2)},
    "L_L": {"Y2": Fraction(1, 2), "SU2": Fraction(1, 2), "SU3": Fraction(0, 1)},
    "e_R": {"Y2": Fraction(1, 1), "SU2": Fraction(0, 1), "SU3": Fraction(0, 1)},
    "nu_R": {"Y2": Fraction(0, 1), "SU2": Fraction(0, 1), "SU3": Fraction(0, 1)},
}

C_Y = sum(item["Y2"] for item in trace_contributions.values())
C_2 = sum(item["SU2"] for item in trace_contributions.values())
C_3 = sum(item["SU3"] for item in trace_contributions.values())
C_1 = Fraction(3, 5) * C_Y

inputs = {
    "alpha_em_inverse_MZ": 127.955,
    "alpha_em_inverse_uncertainty": 0.010,
    "sin2_thetaW_MSbar_MZ": 0.23122,
    "sin2_thetaW_uncertainty": 0.00006,
    "alpha_s_MSbar_MZ": 0.1180,
    "alpha_s_uncertainty": 0.0009,
    "MZ_GeV": 91.1876,
}

beta = {"g1": 41 / 10, "g2": -19 / 6, "g3": -7}


def low_energy_couplings(alpha_inverse, sin2_theta, alpha_s):
    alpha = 1 / alpha_inverse
    electric_charge = math.sqrt(4 * math.pi * alpha)
    g_y = electric_charge / math.sqrt(1 - sin2_theta)
    g_2 = electric_charge / math.sqrt(sin2_theta)
    g_1 = math.sqrt(5 / 3) * g_y
    g_3 = math.sqrt(4 * math.pi * alpha_s)
    return {"gY": g_y, "g1": g_1, "g2": g_2, "g3": g_3, "e": electric_charge}


def crossing(first, second, couplings):
    logarithm = (
        8
        * math.pi**2
        * (1 / couplings[first] ** 2 - 1 / couplings[second] ** 2)
        / (beta[first] - beta[second])
    )
    scale = inputs["MZ_GeV"] * math.exp(logarithm)
    running = {
        name: 1
        / math.sqrt(
            1 / couplings[name] ** 2
            - beta[name] * logarithm / (8 * math.pi**2)
        )
        for name in ("g1", "g2", "g3")
    }
    return logarithm, scale, running


central = low_energy_couplings(
    inputs["alpha_em_inverse_MZ"],
    inputs["sin2_thetaW_MSbar_MZ"],
    inputs["alpha_s_MSbar_MZ"],
)

pairwise = {}
for first, second in (("g1", "g2"), ("g2", "g3"), ("g1", "g3")):
    logarithm, scale, running = crossing(first, second, central)
    pairwise[f"{first}_{second}"] = {
        "log_mu_over_MZ": logarithm,
        "scale_GeV": scale,
        "running_couplings": running,
        "relative_spread": max(running.values()) / min(running.values()) - 1,
    }

corner_mismatch = []
for alpha_inverse, sin2_theta, alpha_s in itertools.product(
    (
        inputs["alpha_em_inverse_MZ"] - inputs["alpha_em_inverse_uncertainty"],
        inputs["alpha_em_inverse_MZ"] + inputs["alpha_em_inverse_uncertainty"],
    ),
    (
        inputs["sin2_thetaW_MSbar_MZ"] - inputs["sin2_thetaW_uncertainty"],
        inputs["sin2_thetaW_MSbar_MZ"] + inputs["sin2_thetaW_uncertainty"],
    ),
    (
        inputs["alpha_s_MSbar_MZ"] - inputs["alpha_s_uncertainty"],
        inputs["alpha_s_MSbar_MZ"] + inputs["alpha_s_uncertainty"],
    ),
):
    couplings = low_energy_couplings(alpha_inverse, sin2_theta, alpha_s)
    _, _, running = crossing("g1", "g3", couplings)
    common = (running["g1"] + running["g3"]) / 2
    corner_mismatch.append(abs(running["g2"] / common - 1))

result = {
    "gate": "version4_spectral_gauge_normalization",
    "trace_contributions": {
        field: {name: str(value) for name, value in values.items()}
        for field, values in trace_contributions.items()
    },
    "trace_totals": {"C_Y": str(C_Y), "C_1_GUT": str(C_1), "C_2": str(C_2), "C_3": str(C_3)},
    "spectral_relation": "g1=g2=g3, equivalently gY^2=(3/5) g2^2 and g2=g3",
    "spectral_sin2_thetaW": "3/8",
    "generation_and_reality_doubling_cancel_in_ratios": True,
    "inputs": inputs,
    "couplings_at_MZ": central,
    "one_loop_beta_coefficients": beta,
    "pairwise_crossings": pairwise,
    "common_triple_crossing_exists": False,
    "g1_g3_crossing_g2_relative_mismatch": abs(
        pairwise["g1_g3"]["running_couplings"]["g2"]
        / pairwise["g1_g3"]["running_couplings"]["g1"]
        - 1
    ),
    "g1_g3_crossing_mismatch_corner_range": [min(corner_mismatch), max(corner_mismatch)],
    "status": "exact spectral trace ratio; minimal no-threshold one-loop SM running fails exact triple matching",
}

with open("s2t_v4_spectral_gauge_normalization_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))