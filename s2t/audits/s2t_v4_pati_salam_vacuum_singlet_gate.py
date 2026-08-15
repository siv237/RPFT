#!/usr/bin/env python3
import json
import math
from pathlib import Path


BRIDGE_PATH = Path("s2t_v4_spectral_pati_salam_bridge_gate_results.json")
PORTAL_PATH = Path("s2t_v3_portal_menu_results.json")
TRANSMUTATION_PATH = Path("s2t_v3_dilaton_radion_transmutation_results.json")
OUTPUT_PATH = Path("s2t_v4_pati_salam_vacuum_singlet_gate_results.json")


def main():
    bridge = json.loads(BRIDGE_PATH.read_text())
    portal = json.loads(PORTAL_PATH.read_text())
    transmutation = json.loads(TRANSMUTATION_PATH.read_text())

    muon_mass_gev = 0.1056583755
    neutrino_denominator = 23.0 + 1.0 / math.pi
    project_majorana_scale_gev = neutrino_denominator * muon_mass_gev

    optimized_scales = {
        name: item["breaking_scale_GeV"]
        for name, item in bridge["freely_optimized_breaking_scale_results"].items()
    }
    ratios = {
        name: scale / project_majorana_scale_gev
        for name, scale in optimized_scales.items()
    }
    decade_gaps = {name: math.log10(ratio) for name, ratio in ratios.items()}

    universal_shift_test = {
        "initial_required_goldstone_mass_squared": 0.0,
        "initial_unwanted_pseudogoldstone_mass_squared": 0.0,
        "universal_singlet_shift": "delta",
        "required_goldstone_after_shift": "delta",
        "unwanted_mode_after_shift": "delta",
        "goldstone_condition": "delta=0",
        "unwanted_mode_then_massless": True,
        "universal_singlet_rescues_goldstone_count": False,
    }

    output = {
        "gate": "version4_pati_salam_vacuum_singlet",
        "date": "2026-08-13",
        "literature_inputs": {
            "canonical_spectral_pati_salam_vacuum_suitable": False,
            "obstruction": (
                "the desired color-triplet Goldstone and an unwanted scalar remain "
                "mass-degenerate; the published stationary point is not a suitable minimum"
            ),
            "source": "arXiv:1905.04533",
        },
        "project_scale_comparison": {
            "neutrino_denominator": neutrino_denominator,
            "muon_mass_GeV": muon_mass_gev,
            "project_MR0_GeV": project_majorana_scale_gev,
            "pati_salam_optimized_scales_GeV": optimized_scales,
            "scale_ratios": ratios,
            "decade_gaps": decade_gaps,
            "current_MR0_can_be_identified_with_pati_salam_scale": False,
        },
        "existing_singlet_route": {
            "coleman_weinberg_architecture_exists": transmutation["verdict"][
                "quantum_transmutation_architecture_exists"
            ],
            "coleman_weinberg_scale_gate_passed": transmutation["verdict"][
                "quantum_scale_gate_passed"
            ],
            "direct_sum_scalar_portal": portal["portal_menu"]["scalar"][
                "minimal_spectral_value"
            ],
            "nonzero_portal_requires_new_representation": portal["verdict"][
                "nonzero_portal_requires_new_representation"
            ],
        },
        "universal_singlet_mass_shift_test": universal_shift_test,
        "verdict": {
            "canonical_pati_salam_bridge_passed_vacuum_gate": False,
            "existing_project_singlet_rescues_it": False,
            "pure_universal_shift_rescues_it": False,
            "connected_diagonal_real_singlet_extension_closed": False,
            "reason": (
                "the project singlet is decoupled in the minimal spectral sum, and even a "
                "universal portal cannot split the required Goldstone from the unwanted "
                "mass-degenerate mode"
            ),
            "minimal_model_improvement": (
                "an explicit common Pati-Salam finite geometry containing the conditional "
                "composite adjoint and/or a connected diagonal real singlet whose full mixed "
                "invariants are fixed by the spectral action"
            ),
            "next_gate": (
                "construct the project Pati-Salam finite Dirac block and test the composite "
                "adjoint and connected diagonal singlet potentials separately"
            ),
        },
    }
    OUTPUT_PATH.write_text(json.dumps(output, indent=2) + "\n")

    print(f"project M_R^(0) = {project_majorana_scale_gev:.12g} GeV")
    for name in optimized_scales:
        print(
            f"{name}: m_R/M_R^(0)={ratios[name]:.6e}, "
            f"gap={decade_gaps[name]:.3f} decades"
        )
    print("universal singlet rescue:", universal_shift_test["universal_singlet_rescues_goldstone_count"])


if __name__ == "__main__":
    main()