#!/usr/bin/env python3
import json
import math
from pathlib import Path


def quartic_vacuum(mass_squared, quartic):
    if quartic <= 0:
        return {
            "stable": False,
            "condensed": None,
            "vacuum_amplitude_squared": None,
        }
    if mass_squared >= 0:
        return {
            "stable": True,
            "condensed": False,
            "vacuum_amplitude_squared": 0.0,
        }
    return {
        "stable": True,
        "condensed": True,
        "vacuum_amplitude_squared": -mass_squared / (2.0 * quartic),
    }


def main():
    torsion = json.loads(
        Path("s2t_neutrino_torsion_square_root_defect_results.json").read_text(
            encoding="utf-8"
        )
    )
    core = json.loads(
        Path("s2t_neutrino_core_gluing_majorana_line_results.json").read_text(
            encoding="utf-8"
        )
    )
    global_action = json.loads(
        Path("s2t_neutrino_global_action_denominator_gate_results.json").read_text(
            encoding="utf-8"
        )
    )
    parent = json.loads(
        Path("s2t_neutrino_parent_superconnection_embedding_results.json").read_text(
            encoding="utf-8"
        )
    )

    meridian_flux = math.pi
    pair_charge = 2
    forced_phase_change = pair_charge * meridian_flux
    forced_winding = forced_phase_change / (2.0 * math.pi)

    potential_controls = {
        "positive_mass_squared": quartic_vacuum(1.0, 1.0),
        "zero_mass_squared": quartic_vacuum(0.0, 1.0),
        "negative_mass_squared": quartic_vacuum(-1.0, 1.0),
        "unstable_quartic": quartic_vacuum(-1.0, -1.0),
    }

    results = {
        "status": "square_root_flux_forces_odd_winding_conditionally_but_the_existing_S2T_action_does_not_force_pairing_condensation",
        "date": "2026-08-06",
        "minimal_tubular_action": {
            "bosonic_sector": (
                "S_B=int_Ngamma [Z_Phi |(d-2 i a)Phi|^2 + "
                "m_Phi^2 |Phi|^2 + lambda_Phi |Phi|^4 + "
                "(1/4 e_root^2)|f_a|^2]"
            ),
            "fermionic_sector": (
                "S_F=(1/2) int_Ngamma Psi^T C [D_a + "
                "Re(Phi) Gamma1 + Im(Phi) Gamma2] Psi"
            ),
            "topological_boundary_sector": "integral_meridian a = pi mod 2pi",
            "continuous_coefficients": [
                "Z_Phi",
                "m_Phi_squared",
                "lambda_Phi",
                "e_root",
                "Majorana_Yukawa_normalization",
            ],
        },
        "topological_winding_gate": {
            "meridian_flux": meridian_flux,
            "pair_charge": pair_charge,
            "finite_energy_condition": "integral(d arg Phi - 2 a)=0",
            "forced_pair_phase_change": forced_phase_change,
            "forced_winding": forced_winding,
            "mod_two_index": int(round(forced_winding)) % 2,
            "matches_existing_torsion_audit": int(round(forced_winding))
            == torsion["forced_majorana_vortex"]["vortex_winding"],
            "finding": (
                "Once a nonzero charge-two pairing field and the square-root pi flux "
                "are present, finite energy forces unit winding without a fitted integer."
            ),
        },
        "condensation_gate": {
            "potential": "V=m_Phi^2 |Phi|^2 + lambda_Phi |Phi|^4",
            "controls": potential_controls,
            "finding": (
                "Topology fixes the winding class but not whether |Phi| is nonzero. "
                "For nonnegative m_Phi^2 the vacuum is Phi=0 and no gapped class-D "
                "defect exists. Condensation requires a negative quadratic term or an "
                "independently derived attractive gap equation."
            ),
            "sign_derived_in_existing_S2T_action": False,
            "vacuum_amplitude_derived": False,
        },
        "square_root_connection_gate": {
            "smooth_ambient_Z2_meridian_holonomy": torsion[
                "smooth_ambient_torsion_line"
            ]["character_on_mu_core"],
            "root_meridian_holonomy": torsion["square_root_defect"]["branches"][
                0
            ]["holonomy_on_core_meridian"],
            "extends_across_core": torsion["square_root_defect"]["branches"][0][
                "descends_across_core"
            ],
            "finding": (
                "The smooth ambient Z2 line is locally trivial on the meridian. "
                "Its square root has holonomy -1 and cannot extend through the core. "
                "A local parent theory must therefore contain a new dynamical Z4/U1 "
                "connection or an explicit disorder/defect sector."
            ),
            "existing_quarter_branch_match": torsion[
                "existing_gauge_holonomy_match"
            ]["match"],
            "sector_identification_derived": False,
        },
        "rank_one_saddle_gate": {
            "local_core_gluing_rank": core["rank_one_result"][
                "combined_real_rank"
            ],
            "complement_rank": core["rank_one_result"][
                "complement_rank_in_R24"
            ],
            "global_tubular_EFT_status": global_action[
                "theory_effect"
            ]["global_BdG_EFT"],
            "parent_restriction_status": parent["theory_effect"][
                "parent_tubular_restriction"
            ],
            "finding": (
                "If the square-root flux and condensed pairing saddle are admitted, "
                "the local zero mode, core gluing, R24 embedding and tubular restriction "
                "are mutually consistent. The obstruction is dynamical existence, not "
                "the index calculation."
            ),
        },
        "parent_action_gate": {
            "topology_alone_forces_defect": False,
            "conditional_statement": (
                "pi flux plus nonzero charge-two pairing implies odd vortex and rank one"
            ),
            "missing_derivations": [
                "why the square-root connection is a dynamical or summed sector of S2T",
                "why the pairing quadratic coefficient is negative or the gap equation condenses",
                "why the quarter-holonomy gauge branch couples to the Majorana pair field",
                "why the resulting heavy scale and Yukawa normalization equal the frozen neutrino inputs",
            ],
            "new_model_if_added_by_hand": True,
        },
        "no_go": {
            "statement": (
                "The ambient Z2 topology does not by itself create the class-D defect. "
                "It fixes an odd winding only after adding a singular square-root flux "
                "sector and a nonzero charge-two pairing condensate. Without a parent "
                "gap equation these are structural additions, not consequences of II.A."
            ),
            "reopening_conditions": [
                "derive a Z4/U1 root connection or disorder sector from the existing finite algebra",
                "derive a negative pairing Hessian or attractive four-fermion gap equation",
                "show the selected saddle is energetically preferred over Phi=0",
                "retain the mod-two kernel and rank-23 complement under the full fluctuation complex",
            ],
        },
        "scientific_verdict": {
            "positive": (
                "The topological part is strong: the square-root pi flux forces winding one, "
                "and the resulting rank-one Majorana kernel is internally consistent."
            ),
            "negative": (
                "The current action does not force the root flux sector or the pairing condensate. "
                "Therefore the defect is a well-defined conditional submodel, not yet a derived saddle."
            ),
            "next_target": (
                "Search the existing finite algebra/superconnection for a mandatory Z4 root "
                "connection and compute the pairing Hessian before introducing any new coupling."
            ),
        },
    }

    assert abs(forced_winding - 1.0) < 1e-12
    assert potential_controls["positive_mass_squared"]["condensed"] is False
    assert potential_controls["negative_mass_squared"]["condensed"] is True
    assert results["square_root_connection_gate"]["extends_across_core"] is False
    assert results["rank_one_saddle_gate"]["local_core_gluing_rank"] == 1
    assert results["rank_one_saddle_gate"]["complement_rank"] == 23

    Path("s2t_majorana_defect_parent_action_gate_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()