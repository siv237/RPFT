#!/usr/bin/env python3
import json
import math
from pathlib import Path


def branch_row(winding, circumference, lambda_pair, vacuum_scale_sq):
    gauge_integral = math.pi / 2.0
    pair_charge = -2
    covariant_momentum = (
        2.0 * math.pi * winding - pair_charge * gauge_integral
    ) / circumference
    momentum_sq = covariant_momentum**2
    amplitude_sq = max(
        0.0, vacuum_scale_sq - momentum_sq / lambda_pair
    )
    condensed = amplitude_sq > 0.0
    if condensed:
        energy_density = (
            momentum_sq * vacuum_scale_sq
            - momentum_sq**2 / (2.0 * lambda_pair)
        )
        radial_hessian = 4.0 * (
            lambda_pair * vacuum_scale_sq - momentum_sq
        )
    else:
        energy_density = 0.5 * lambda_pair * vacuum_scale_sq**2
        radial_hessian = 2.0 * (
            momentum_sq - lambda_pair * vacuum_scale_sq
        )
    normal_energy_density = 0.5 * lambda_pair * vacuum_scale_sq**2
    return {
        "winding": winding,
        "covariant_momentum": covariant_momentum,
        "covariant_momentum_squared": momentum_sq,
        "condensed": condensed,
        "amplitude_squared": amplitude_sq,
        "energy_density": energy_density,
        "normal_energy_density": normal_energy_density,
        "energy_gain": normal_energy_density - energy_density,
        "radial_hessian": radial_hessian,
    }


def main():
    trilemma = json.loads(
        Path("s2t_root_mass_condensate_trilemma_results.json").read_text(
            encoding="utf-8"
        )
    )
    defect = json.loads(
        Path("s2t_majorana_defect_parent_action_gate_results.json").read_text(
            encoding="utf-8"
        )
    )

    circumference = math.pi
    lambda_pair = 1.0
    geometry_momentum = math.pi / circumference
    critical_vacuum_scale_sq = geometry_momentum**2 / lambda_pair

    sample_control = []
    for ratio in [0.5, 1.0, 2.0, 10.0]:
        vacuum_scale_sq = ratio * critical_vacuum_scale_sq
        rows = [
            branch_row(winding, circumference, lambda_pair, vacuum_scale_sq)
            for winding in range(-3, 3)
        ]
        if ratio <= 1.0:
            minimum = branch_row(
                0, circumference, lambda_pair, vacuum_scale_sq
            )
            minimum["radial_hessian"] = 2.0 * (
                geometry_momentum**2
                - lambda_pair * vacuum_scale_sq
            )
            degenerate = []
            phase = "normal"
        else:
            minimum = min(rows, key=lambda row: row["energy_density"])
            degenerate = [
                row["winding"]
                for row in rows
                if row["condensed"]
                and abs(
                    row["energy_density"] - minimum["energy_density"]
                )
                < 1e-12
            ]
            phase = "condensed"
        sample_control.append(
            {
                "x=lambda*v^2/k_min^2": ratio,
                "phase": phase,
                "minimum_windings": degenerate,
                "minimum_condensed": minimum["condensed"],
                "minimum_amplitude_squared": minimum["amplitude_squared"],
                "minimum_energy_density": minimum["energy_density"],
                "minimum_radial_hessian": minimum["radial_hessian"],
            }
        )

    vacuum_scale_sq = 2.0 * critical_vacuum_scale_sq
    branch_zero = branch_row(
        0, circumference, lambda_pair, vacuum_scale_sq
    )
    branch_minus_one = branch_row(
        -1, circumference, lambda_pair, vacuum_scale_sq
    )

    results = {
        "status": "nonuniform_pairing_saddle_exists_only_above_a_dynamical_threshold_and_has_an_unselected_conjugate_winding_pair",
        "date": "2026-08-06",
        "functional": {
            "expression": (
                "F=integral_0^L [|D_y Phi|^2 + "
                "(lambda/2)(|Phi|^2-v^2)^2] dy"
            ),
            "periodic_scalar_winding": "arg Phi(y+L)-arg Phi(y)=2*pi*n",
            "root_connection_integral": "integral_y a=pi/2",
            "pair_charge": -2,
            "covariant_momenta": "k_n=(2*pi*n+pi)/L",
        },
        "geometry": {
            "circumference_L": circumference,
            "unit_RP3_systolic_value": "L=pi",
            "minimum_absolute_covariant_momentum": geometry_momentum,
            "degenerate_minimum_windings": [-1, 0],
        },
        "analytic_saddle": {
            "condensation_condition": "lambda*v^2 > k_min^2",
            "critical_v_squared": critical_vacuum_scale_sq,
            "condensed_amplitude_squared": "v^2-k_min^2/lambda",
            "condensed_energy_density": (
                "k_min^2*v^2-k_min^4/(2*lambda)"
            ),
            "energy_gain_over_Phi_zero": (
                "(lambda*v^2-k_min^2)^2/(2*lambda)"
            ),
            "radial_hessian": "4*(lambda*v^2-k_min^2)",
        },
        "explicit_stable_control_x_equals_2": {
            "winding_0": branch_zero,
            "winding_minus_1": branch_minus_one,
            "equal_energy": abs(
                branch_zero["energy_density"]
                - branch_minus_one["energy_density"]
            )
            < 1e-12,
            "opposite_covariant_momenta": abs(
                branch_zero["covariant_momentum"]
                + branch_minus_one["covariant_momentum"]
            )
            < 1e-12,
        },
        "threshold_scan": sample_control,
        "topological_and_dynamical_split": {
            "topology_fixes": [
                "half-shifted momentum lattice k_n=(2n+1)pi/L",
                "two conjugate lowest branches n=0 and n=-1",
                "unit transverse meridian winding if a condensate exists",
            ],
            "topology_does_not_fix": [
                "whether lambda*v^2 exceeds the geometric threshold",
                "the amplitude of the condensate",
                "which conjugate longitudinal branch is selected",
                "the B-L breaking scale and Yukawa normalization",
            ],
            "transverse_rank_one_index_retained_conditionally": defect[
                "topological_winding_gate"
            ]["mod_two_index"]
            == 1,
        },
        "revision_of_trilemma_branch": {
            "homogeneous_branch_closed": trilemma["logical_no_go"][
                "simultaneously_possible_with_scalar_Yukawa"
            ]
            is False,
            "nonuniform_branch_exists": True,
            "existence_is_unconditional": False,
            "reason": (
                "The nonuniform condensate appears only when the dynamical combination "
                "lambda*v^2 is larger than the geometry-fixed half-shift k_min^2."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The root holonomy produces a calculable half-shifted GL spectrum and "
                "a stable nonuniform condensate above threshold. The two lowest branches "
                "are exactly the conjugate windings n=0 and n=-1."
            ),
            "negative": (
                "Topology alone does not force condensation or choose an orientation. "
                "The branch still depends on the undetermined pairing stiffness, vacuum "
                "scale and an additional CP/orientation selector."
            ),
            "next_gate": (
                "Derive lambda*v^2 and the orientation-splitting term from the parent "
                "spectral action, then recompute the BdG kernel on the selected saddle."
            ),
        },
    }

    assert abs(geometry_momentum - 1.0) < 1e-12
    assert branch_zero["condensed"] is True
    assert branch_minus_one["condensed"] is True
    assert results["explicit_stable_control_x_equals_2"]["equal_energy"] is True
    assert results["explicit_stable_control_x_equals_2"][
        "opposite_covariant_momenta"
    ] is True
    assert sample_control[0]["minimum_condensed"] is False
    assert sample_control[1]["minimum_condensed"] is False
    assert sample_control[2]["minimum_condensed"] is True
    assert results["revision_of_trilemma_branch"][
        "existence_is_unconditional"
    ] is False

    Path("s2t_nonuniform_pairing_saddle_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()