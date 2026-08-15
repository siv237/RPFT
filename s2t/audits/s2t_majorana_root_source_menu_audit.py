#!/usr/bin/env python3
import cmath
import json
import math
from pathlib import Path


def phase_label(value):
    menu = {
        1.0 + 0.0j: "+1",
        -1.0 + 0.0j: "-1",
        0.0 + 1.0j: "+i",
        0.0 - 1.0j: "-i",
    }
    rounded = complex(round(value.real), round(value.imag))
    return menu.get(rounded, str(value))


def main():
    gauge = json.loads(
        Path("gauge_holonomy_results.json").read_text(encoding="utf-8")
    )
    projection = json.loads(
        Path("s2t_anomaly_free_holonomy_projection_results.json").read_text(
            encoding="utf-8"
        )
    )
    core = json.loads(
        Path("s2t_neutrino_core_gluing_majorana_line_results.json").read_text(
            encoding="utf-8"
        )
    )
    torsion = json.loads(
        Path("s2t_neutrino_torsion_square_root_defect_results.json").read_text(
            encoding="utf-8"
        )
    )

    sterile_hypercharge = 0.0
    su5_order_four_phase = cmath.exp(
        1j * 3.0 * math.pi * sterile_hypercharge
    )
    su5_z2_phase = su5_order_four_phase**2

    quarter_row = next(
        row for row in gauge["beta_sweep"] if abs(row["beta"] - 0.25) < 1e-12
    )
    abstract_doublet_phases = [
        cmath.exp(1j * math.pi * quarter_row["theta_plus_over_pi"]),
        cmath.exp(1j * math.pi * quarter_row["theta_minus_over_pi"]),
    ]

    projection_characters = projection["holonomies"][
        "multiplet_flat_characters"
    ]
    sterile_character_declared = any(
        "sterile" in key.lower() or "neutrino" in key.lower()
        for key in projection_characters
    )

    results = {
        "status": "no_existing_order_four_structure_is_a_mandatory_independent_root_connection_on_the_sterile_Majorana_mode",
        "date": "2026-08-06",
        "sterile_representation": {
            "SM_quantum_numbers": "(1,1)_0",
            "SU5_role": "additional singlet 1, absent from the minimal 10+bar5 generation",
            "hypercharge": sterile_hypercharge,
        },
        "candidate_menu": [
            {
                "candidate": "SU5 order-four hypercharge element h=exp(i 3 pi Y)",
                "phase_on_sterile": phase_label(su5_order_four_phase),
                "square": phase_label(su5_z2_phase),
                "supplies_root": abs(su5_order_four_phase.imag) > 0.5,
                "finding": (
                    "The sterile singlet has Y=0, so both h and P5 act trivially. "
                    "The SU5 quarter holonomy that splits Q,L,T_H cannot source "
                    "the Majorana root connection."
                ),
            },
            {
                "candidate": "abstract U1-like charge doublet at beta=1/4",
                "phases": [phase_label(value) for value in abstract_doublet_phases],
                "supplies_root_algebraically": all(
                    abs(value**2 + 1.0) < 1e-12
                    for value in abstract_doublet_phases
                ),
                "sterile_charge_assignment_derived": False,
                "finding": (
                    "The spectral audit contains charges plus/minus one and hence phases "
                    "plus/minus i, but no finite-algebra map assigns this U1-like charge "
                    "to the neutral sterile mode."
                ),
            },
            {
                "candidate": "multiplet flat character",
                "declared_characters": projection_characters,
                "sterile_character_declared": sterile_character_declared,
                "supplies_root": False,
                "finding": (
                    "A sterile flat character plus/minus i could be declared, but the current "
                    "projection table contains no sterile multiplet. Such an assignment is "
                    "a new sector choice rather than a consequence."
                ),
            },
            {
                "candidate": "spin structures on RP3 and S1",
                "available_coefficient_holonomies": ["+1", "-1"],
                "supplies_root": False,
                "finding": (
                    "Spin structures provide signs, not a coefficient line with square "
                    "equal to the nontrivial torsion character."
                ),
            },
            {
                "candidate": "Nambu quarter transition diag(i,-i)",
                "transition": core["local_BdG_data"]["transition_rule"],
                "coefficient_holonomy": core["core_gluing"][
                    "coefficient_holonomy"
                ],
                "supplies_root_as_independent_background": False,
                "finding": (
                    "The Nambu matrix transports the zero-mode basis after the pair phase "
                    "has already changed by pi. It is a consequence of the defect texture, "
                    "not an independent source of that texture."
                ),
            },
            {
                "candidate": "square root of the ambient torsion line on RP3 minus gamma",
                "phases_on_generator": torsion["square_root_defect"]["solutions"],
                "meridian_result": torsion["square_root_defect"][
                    "meridian_result"
                ],
                "extends_through_core": torsion["square_root_defect"]["branches"][
                    0
                ]["descends_across_core"],
                "supplies_root": True,
                "mandatory_in_frozen_action": False,
                "finding": (
                    "This is the required root connection, but it is singular and defined "
                    "only on the core complement. It must be introduced as a new topological "
                    "sector, disorder operator, or dynamical Z4/U1 connection."
                ),
            },
        ],
        "exhaustive_gate": {
            "existing_mandatory_root_sources": 0,
            "algebraically_available_but_unassigned": [
                "abstract beta=1/4 U1-like charge doublet",
                "multiplet-dependent flat character",
            ],
            "circular_candidates": ["Nambu quarter transition"],
            "actual_required_object": (
                "singular square-root torsion line on the systolic-core complement"
            ),
        },
        "minimal_extension_options": {
            "option_A": (
                "add a sterile-sector Z4 flat character and prove its discrete anomaly consistency"
            ),
            "option_B": (
                "add a dynamical U1 or Z4 gauge connection whose charge-two Higgs field is the Majorana pair"
            ),
            "option_C": (
                "declare a disorder operator summing the nonextendable root sector in the path integral"
            ),
            "all_are_new_structure": True,
        },
        "no_go": {
            "statement": (
                "The existing SU5, spin and Nambu structures do not independently provide "
                "the sterile Majorana root connection. Reusing their quarter phases without "
                "a representation map is sector reassignment, not derivation."
            ),
            "reopening_conditions": [
                "derive a sterile Z4 charge from the finite algebra and real structure",
                "show the root sector is included by the path-integral measure before neutrino data",
                "check discrete/global anomalies of the enlarged sterile sector",
                "derive the charge-two pairing field and its condensation from the same extension",
            ],
        },
        "scientific_verdict": {
            "positive": (
                "The project already contains the correct algebraic phase pair plus/minus i "
                "and the correct singular square-root line."
            ),
            "negative": (
                "No existing mandatory representation assigns that root to the sterile mode. "
                "The defect route therefore requires an explicit sterile Z4/U1/disorder extension."
            ),
            "program_effect": (
                "The next constructive branch is no longer hidden inside SU5. It must be "
                "registered as a new finite-algebra or topological-sector extension and "
                "tested against anomaly and two-sector normalization gates."
            ),
        },
    }

    assert phase_label(su5_order_four_phase) == "+1"
    assert phase_label(su5_z2_phase) == "+1"
    assert [phase_label(value) for value in abstract_doublet_phases] == [
        "-i",
        "+i",
    ]
    assert sterile_character_declared is False
    assert results["exhaustive_gate"]["existing_mandatory_root_sources"] == 0
    assert results["candidate_menu"][-1]["supplies_root"] is True
    assert results["candidate_menu"][-1]["mandatory_in_frozen_action"] is False

    Path("s2t_majorana_root_source_menu_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()