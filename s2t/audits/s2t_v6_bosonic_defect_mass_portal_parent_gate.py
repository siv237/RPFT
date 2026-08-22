#!/usr/bin/env python3
"""Audit absolute scale and Higgs portal of the bosonic defect parent."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_mass_portal_parent_gate_results.json"


def stationary_radius(c_d: float, c_f: float, c_v: float) -> float:
    """Positive stationary radius of E=c_d R+c_f/R+c_v R^3."""
    roots = np.roots([3.0 * c_v, c_d, -c_f])
    positive = [root.real for root in roots if abs(root.imag) < 1e-12 and root.real > 0]
    return float(np.sqrt(positive[0]))


def energy(radius: float, c_d: float, c_f: float, c_v: float) -> float:
    return float(c_d * radius + c_f / radius + c_v * radius**3)


def uniaxial_state(shape: float) -> np.ndarray:
    return np.diag([1.0 / 3.0 + 2.0 * shape / 3.0,
                    1.0 / 3.0 - shape / 3.0,
                    1.0 / 3.0 - shape / 3.0])


def middle_hodge_block(trace_amplitude: float, shape: float, higgs_norm_squared: float) -> float:
    gram = trace_amplitude * uniaxial_state(shape)
    defect = gram - higgs_norm_squared * np.eye(3)
    return float(np.trace(defect @ defect))


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v6_gauged_projective_spin_cover_parent_gate_results.json")
        .read_text(encoding="utf-8")
    )
    finite = previous["finite_energy_test_unit_coefficients"]
    i_d = float(finite["integral_DQ_squared"])
    i_f = float(finite["integral_F_squared"])
    i_v = float(finite["integral_bulk_potential"])

    dimensionless_radius = stationary_radius(i_d, i_f, i_v)
    dimensionless_mass = energy(dimensionless_radius, i_d, i_f, i_v)

    # Two arbitrary choices of physical length and energy units leave every
    # dimensionless profile equation unchanged while changing mass and radius.
    scale_examples = []
    for length_unit, energy_unit in [(1.0, 1.0), (7.0, 11.0), (1.0e-3, 2.0e6)]:
        c_d = energy_unit / length_unit
        c_f = energy_unit * length_unit
        c_v = energy_unit / length_unit**3
        radius = stationary_radius(i_d * c_d, i_f * c_f, i_v * c_v)
        mass = energy(radius, i_d * c_d, i_f * c_f, i_v * c_v)
        scale_examples.append(
            {
                "length_unit": length_unit,
                "energy_unit": energy_unit,
                "physical_radius": radius,
                "predicted_radius": length_unit * dimensionless_radius,
                "physical_mass": mass,
                "predicted_mass": energy_unit * dimensionless_mass,
            }
        )

    # In the M300 Hodge block Tr(T R-h^2 I)^2 the Higgs field couples to T,
    # not to the traceless shape Q=R-I/3.  The mixed finite difference is the
    # coefficient test for Tr(Q^2) h^2.
    trace_amplitude = 1.37
    shape = 0.41
    higgs_norm_squared = 0.73
    portal_residual = (
        middle_hodge_block(trace_amplitude, shape, higgs_norm_squared)
        - middle_hodge_block(trace_amplitude, shape, 0.0)
        - middle_hodge_block(trace_amplitude, 0.0, higgs_norm_squared)
        + middle_hodge_block(trace_amplitude, 0.0, 0.0)
    )

    eps = 1.0e-6
    radial_higgs_mixed = (
        middle_hodge_block(trace_amplitude + eps, 0.0, higgs_norm_squared + eps)
        - middle_hodge_block(trace_amplitude + eps, 0.0, higgs_norm_squared - eps)
        - middle_hodge_block(trace_amplitude - eps, 0.0, higgs_norm_squared + eps)
        + middle_hodge_block(trace_amplitude - eps, 0.0, higgs_norm_squared - eps)
    ) / (4.0 * eps**2)

    result = {
        "gate": "version6_bosonic_defect_mass_portal_parent_gate",
        "dimensionless_profile": {
            "integral_DQ_squared": i_d,
            "integral_F_squared": i_f,
            "integral_bulk_potential": i_v,
            "unit_coefficient_stationary_radius": dimensionless_radius,
            "unit_coefficient_mass": dimensionless_mass,
        },
        "two_scale_degeneracy": {
            "parameterization": {
                "c_D": "E0/L0",
                "c_F": "E0*L0",
                "c_V": "E0/L0^3",
                "R_physical": "L0*r_dimensionless",
                "M_physical": "E0*m_dimensionless",
            },
            "examples": scale_examples,
            "absolute_length_scale_derived": False,
            "absolute_energy_scale_derived": False,
        },
        "lorentzian_completion": {
            "allowed_tensor_structure": "Tr(D_mu Q D^mu Q), Tr(F_mu_nu F^mu_nu), V(Q)",
            "static_signs_fix_minkowski_relative_signs_after_metric_convention": True,
            "common_normalization_from_current_parent": False,
            "time_kinetic_coefficient_derived": False,
        },
        "higgs_portal_test": {
            "m300_middle_block": "Tr(T R-|H|^2 I_3)^2",
            "expanded_form": "T^2 Tr(R^2)-2 T |H|^2+3|H|^4",
            "shape_variable": "Q=R-I_3/3",
            "mixed_shape_higgs_residual": portal_residual,
            "radial_higgs_mixed_derivative": radial_higgs_mixed,
            "Tr_Q2_H2_coefficient_in_minimal_M300_parent": 0.0,
            "radial_amplitude_H2_coupling_exists": True,
            "nonzero_bosonic_defect_higgs_portal_derived": False,
        },
        "verdict": {
            "dimensionless_profile_and_scaling_closed": True,
            "absolute_mass_and_radius_derived": False,
            "lorentz_covariant_form_admissible": True,
            "lorentz_covariant_parent_normalization_derived": False,
            "minimal_parent_predicts_nonzero_shape_higgs_portal": False,
            "current_bosonic_defect_is_observably_coupled": False,
            "status": "scale_and_portal_no_go_for_current_parent",
            "next_gate": "version6_bosonic_defect_full_euler_lagrange_stability_gate",
        },
    }

    for example in scale_examples:
        assert abs(example["physical_radius"] - example["predicted_radius"]) < 1e-8 * max(1.0, example["physical_radius"])
        assert abs(example["physical_mass"] - example["predicted_mass"]) < 1e-8 * max(1.0, example["physical_mass"])
    assert abs(portal_residual) < 1e-12
    assert abs(radial_higgs_mixed + 2.0) < 2e-4

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()