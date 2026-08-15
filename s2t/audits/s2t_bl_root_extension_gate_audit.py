#!/usr/bin/env python3
import cmath
import json
import math
from fractions import Fraction
from pathlib import Path


FIELDS = (
    {"name": "Q", "multiplicity": 6, "Y": Fraction(1, 6), "BL": Fraction(1, 3), "T3": Fraction(1), "T2": Fraction(3, 2)},
    {"name": "u_c", "multiplicity": 3, "Y": Fraction(-2, 3), "BL": Fraction(-1, 3), "T3": Fraction(1, 2), "T2": Fraction(0)},
    {"name": "d_c", "multiplicity": 3, "Y": Fraction(1, 3), "BL": Fraction(-1, 3), "T3": Fraction(1, 2), "T2": Fraction(0)},
    {"name": "L", "multiplicity": 2, "Y": Fraction(-1, 2), "BL": Fraction(-1), "T3": Fraction(0), "T2": Fraction(1, 2)},
    {"name": "e_c", "multiplicity": 1, "Y": Fraction(1), "BL": Fraction(1), "T3": Fraction(0), "T2": Fraction(0)},
    {"name": "N_c", "multiplicity": 1, "Y": Fraction(0), "BL": Fraction(1), "T3": Fraction(0), "T2": Fraction(0)},
)


def rational(value):
    return {"fraction": str(value), "float": float(value)}


def phase_label(value):
    rounded = complex(round(value.real), round(value.imag))
    return {
        1.0 + 0.0j: "+1",
        -1.0 + 0.0j: "-1",
        0.0 + 1.0j: "+i",
        0.0 - 1.0j: "-i",
    }.get(rounded, str(value))


def main():
    anomalies = {
        "gravity_squared_B_minus_L": sum(
            field["multiplicity"] * field["BL"] for field in FIELDS
        ),
        "B_minus_L_cubed": sum(
            field["multiplicity"] * field["BL"] ** 3 for field in FIELDS
        ),
        "SU3_squared_B_minus_L": sum(
            field["T3"] * field["BL"] for field in FIELDS
        ),
        "SU2_squared_B_minus_L": sum(
            field["T2"] * field["BL"] for field in FIELDS
        ),
        "Y_squared_B_minus_L": sum(
            field["multiplicity"] * field["Y"] ** 2 * field["BL"]
            for field in FIELDS
        ),
        "Y_B_minus_L_squared": sum(
            field["multiplicity"] * field["Y"] * field["BL"] ** 2
            for field in FIELDS
        ),
    }
    kinetic_mixing_trace = sum(
        field["multiplicity"] * field["Y"] * field["BL"]
        for field in FIELDS
    )

    generator_integral = math.pi / 2.0
    meridian_integral = 2.0 * generator_integral
    sterile_charge = 1
    pairing_charge = -2
    sterile_generator_phase = cmath.exp(
        1j * sterile_charge * generator_integral
    )
    sterile_meridian_phase = cmath.exp(
        1j * sterile_charge * meridian_integral
    )
    pairing_generator_phase = cmath.exp(
        1j * pairing_charge * generator_integral
    )
    forced_winding = -pairing_charge * meridian_integral / (2.0 * math.pi)

    results = {
        "status": "minimal_BL_extension_closes_root_representation_and_continuous_anomaly_gates_but_adds_unfixed_dynamics_and_kinetic_mixing",
        "date": "2026-08-06",
        "convention": "all fermions are left-handed Weyl fields",
        "one_generation_fields": [
            {
                "name": field["name"],
                "multiplicity": field["multiplicity"],
                "Y": str(field["Y"]),
                "B_minus_L": str(field["BL"]),
            }
            for field in FIELDS
        ],
        "continuous_anomalies_per_generation": {
            name: rational(value) for name, value in anomalies.items()
        },
        "continuous_anomaly_gate_passes": all(
            value == 0 for value in anomalies.values()
        ),
        "root_holonomy": {
            "generator_integral_over_pi": generator_integral / math.pi,
            "meridian_integral_over_pi": meridian_integral / math.pi,
            "sterile_charge": sterile_charge,
            "sterile_generator_phase": phase_label(sterile_generator_phase),
            "sterile_meridian_phase": phase_label(sterile_meridian_phase),
            "pairing_scalar_charge": pairing_charge,
            "pairing_generator_phase": phase_label(pairing_generator_phase),
            "Majorana_vertex_charge_sum": pairing_charge + 2 * sterile_charge,
            "forced_pairing_winding": forced_winding,
            "absolute_winding": abs(forced_winding),
        },
        "abelian_mixing": {
            "trace_Y_times_B_minus_L_per_generation": rational(
                kinetic_mixing_trace
            ),
            "radiatively_generated": kinetic_mixing_trace != 0,
            "consequence": (
                "The extension requires a kinetic-mixing boundary condition and running; "
                "it is a new normalization-sensitive gauge-sector datum."
            ),
        },
        "new_continuous_data": [
            "g_BL",
            "v_BL",
            "lambda_BL",
            "lambda_HPhi",
            "epsilon_YB",
            "Majorana Yukawa matrix y_N",
        ],
        "unification_status": {
            "inside_minimal_SU5": False,
            "reason": (
                "N_c is an external SU5 singlet, while B-L must act nontrivially on it."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "U(1) B-L with one N_c per generation and a charge-minus-two scalar "
                "is the first tested coherent extension that supplies the order-four "
                "sterile root, an invariant Majorana pairing field, and cancellation "
                "of all continuous local anomalies."
            ),
            "negative": (
                "The gauge factor, breaking scale, scalar potential, kinetic mixing and "
                "Yukawa matrix are not derived from the frozen S2T parent action."
            ),
            "program_effect": (
                "The root problem now has a concrete extension target, but adopting it "
                "creates a new model rather than closing II.A."
            ),
        },
    }

    assert results["continuous_anomaly_gate_passes"] is True
    assert phase_label(sterile_generator_phase) == "+i"
    assert phase_label(sterile_meridian_phase) == "-1"
    assert pairing_charge + 2 * sterile_charge == 0
    assert abs(abs(forced_winding) - 1.0) < 1e-12
    assert kinetic_mixing_trace == Fraction(8, 3)
    assert results["unification_status"]["inside_minimal_SU5"] is False

    Path("s2t_bl_root_extension_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()