#!/usr/bin/env python3
import cmath
import json
import math
from pathlib import Path


def phase(angle):
    return cmath.exp(1j * angle)


def phase_label(value):
    rounded = complex(round(value.real), round(value.imag))
    return {
        1.0 + 0.0j: "+1",
        -1.0 + 0.0j: "-1",
        0.0 + 1.0j: "+i",
        0.0 - 1.0j: "-i",
    }.get(rounded, str(value))


def main():
    torsion = json.loads(
        Path("s2t_neutrino_torsion_square_root_defect_results.json").read_text(
            encoding="utf-8"
        )
    )
    extension = json.loads(
        Path("s2t_bl_root_extension_gate_results.json").read_text(
            encoding="utf-8"
        )
    )

    root_angle_y = math.pi / 2.0
    meridian_multiple = 2
    root_angle_mu = meridian_multiple * root_angle_y
    sterile_charge = 1
    pairing_charge = -2

    sterile_y = phase(sterile_charge * root_angle_y)
    pairing_gauge_y = phase(pairing_charge * root_angle_y)
    pairing_gauge_mu = phase(pairing_charge * root_angle_mu)
    ambient_torsion_y = -1.0 + 0.0j
    ambient_torsion_mu = ambient_torsion_y**meridian_multiple
    twisted_pairing_y = pairing_gauge_y * ambient_torsion_y
    twisted_pairing_mu = pairing_gauge_mu * ambient_torsion_mu

    residual_order_ordinary = abs(pairing_charge)
    order_four_element_preserves_ordinary_vev = (
        abs(pairing_gauge_y - 1.0) < 1e-12
    )

    charge_four_phase_y = phase(-4 * root_angle_y)
    charge_four_majorana_vertex_sum = -4 + 2 * sterile_charge

    results = {
        "status": "intermediate_condensate_holonomy_rescue_superseded_by_root_mass_condensate_trilemma",
        "date": "2026-08-06",
        "supersession": {
            "superseded": True,
            "superseded_by": "s2t_root_mass_condensate_trilemma_results.json",
            "retained_result": (
                "The ambient torsion twist cancels the pairing-field holonomy "
                "obstruction, but it does not close the full Yukawa vertex."
            ),
        },
        "topology": {
            "core_complement": torsion["topology"]["core_complement"],
            "filling_relation": torsion["topology"]["filling_relation"],
            "generator": "y",
            "meridian": "mu=2y",
        },
        "ordinary_charge_two_scalar": {
            "root_holonomy_on_y": phase_label(sterile_y),
            "pairing_gauge_holonomy_on_y": phase_label(pairing_gauge_y),
            "pairing_gauge_holonomy_on_meridian": phase_label(pairing_gauge_mu),
            "nonzero_parallel_section_on_y": abs(pairing_gauge_y - 1.0) < 1e-12,
            "nonzero_parallel_section_on_meridian": abs(pairing_gauge_mu - 1.0)
            < 1e-12,
            "unbroken_subgroup_after_charge_two_vev": f"Z{residual_order_ordinary}",
            "order_four_element_preserves_vev": order_four_element_preserves_ordinary_vev,
            "finding": (
                "The charge-minus-two scalar sees holonomy -1 on the closed complement "
                "generator y. An ordinary nowhere-zero covariantly constant condensate "
                "therefore cannot coexist with the sterile +i root holonomy."
            ),
        },
        "charge_four_alternative": {
            "holonomy_on_y": phase_label(charge_four_phase_y),
            "leaves_Z4": abs(charge_four_phase_y - 1.0) < 1e-12,
            "Majorana_vertex_charge_sum": charge_four_majorana_vertex_sum,
            "allows_linear_Phi_NN_vertex": charge_four_majorana_vertex_sum == 0,
            "finding": (
                "A charge-four condensate preserves the order-four element but cannot "
                "generate the linear Majorana vertex Phi N_c N_c."
            ),
        },
        "torsion_twisted_pairing_scalar": {
            "bundle": "ambient Z2 torsion line tensor U(1)_(B-L) charge-minus-two line",
            "ambient_torsion_holonomy_on_y": phase_label(ambient_torsion_y),
            "ambient_torsion_holonomy_on_meridian": phase_label(
                ambient_torsion_mu
            ),
            "total_holonomy_on_y": phase_label(twisted_pairing_y),
            "total_holonomy_on_meridian": phase_label(twisted_pairing_mu),
            "nonzero_parallel_section_on_complement": (
                abs(twisted_pairing_y - 1.0) < 1e-12
                and abs(twisted_pairing_mu - 1.0) < 1e-12
            ),
            "Majorana_bilinear_holonomy_on_y": phase_label(sterile_y**2),
            "finding": (
                "The existing ambient torsion sign cancels the charge-two gauge sign. "
                "A twisted pairing section can therefore condense consistently and pair "
                "the N_c N_c bilinear, whose root holonomy also squares to -1."
            ),
        },
        "revision_of_previous_gate": {
            "continuous_anomaly_result_retained": extension[
                "continuous_anomaly_gate_passes"
            ],
            "kinetic_mixing_result_retained": extension["abelian_mixing"][
                "trace_Y_times_B_minus_L_per_generation"
            ],
            "ordinary_scalar_claim_retained": False,
            "revised_candidate": (
                "U(1)_(B-L) root connection plus an ambient-torsion-twisted "
                "charge-minus-two pairing section"
            ),
        },
        "scientific_verdict": {
            "negative": (
                "Minimal B-L with an ordinary charge-two Higgs does not by itself realize "
                "the desired order-four root and a nonzero pairing condensate on the full "
                "core complement."
            ),
            "conditional_rescue": (
                "The pairing-field holonomy obstruction cancels if the field is twisted "
                "by the ambient Z2 torsion line. The later trilemma proves that the "
                "remaining sign is transferred to the Yukawa map."
            ),
            "next_gate": (
                "Derive this twisted bundle assignment and its potential from the finite "
                "algebra or spectral action before treating the B-L branch as coherent."
            ),
        },
    }

    assert phase_label(sterile_y) == "+i"
    assert phase_label(pairing_gauge_y) == "-1"
    assert phase_label(pairing_gauge_mu) == "+1"
    assert residual_order_ordinary == 2
    assert order_four_element_preserves_ordinary_vev is False
    assert phase_label(charge_four_phase_y) == "+1"
    assert charge_four_majorana_vertex_sum != 0
    assert phase_label(twisted_pairing_y) == "+1"
    assert phase_label(twisted_pairing_mu) == "+1"
    assert results["torsion_twisted_pairing_scalar"][
        "nonzero_parallel_section_on_complement"
    ] is True

    Path("s2t_bl_root_condensate_consistency_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()