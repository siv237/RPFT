#!/usr/bin/env python3
import importlib.util
import json
import math
from pathlib import Path


OUTPUT = Path("s2t_v4_pati_salam_bv_multiplicity_fork_gate_results.json")


def load_bridge():
    path = Path("s2t_v4_spectral_pati_salam_bridge_gate.py")
    specification = importlib.util.spec_from_file_location("ps_bridge", path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def hessian(copy_number):
    return {
        "copy_number": copy_number,
        "lambda_relative": copy_number,
        "determinant_coefficient": 4 * copy_number,
        "radial_eigenvalue": 8.0 * math.sqrt(2.0),
        "gauge_zero_modes": 9,
        "transverse_eigenvalue": math.sqrt(2.0) * (4 * copy_number - 2),
        "transverse_multiplicity": 6,
    }


def main():
    bridge = load_bridge()
    gauge = json.loads(Path("s2t_v4_spectral_gauge_normalization_gate_results.json").read_text())
    inputs = {"MZ_GeV": gauge["inputs"]["MZ_GeV"], "couplings_at_MZ": gauge["couplings_at_MZ"]}
    fixed_scale = gauge["pairwise_crossings"]["g1_g2"]["scale_GeV"]
    scenarios = {
        "composite": {"R": 7.0 / 3.0, "L": 3.0, "4": 31.0 / 3.0},
        "composite_plus_1_1_15": {"R": 7.0 / 3.0, "L": 3.0, "4": 9.0},
        "fundamental": {"R": -26.0 / 3.0, "L": -2.0, "4": 2.0},
        "left_right_fundamental": {"R": -26.0 / 3.0, "L": -26.0 / 3.0, "4": -4.0 / 3.0},
    }
    shift = {"R": -2.0 / 3.0, "L": 0.0, "4": -4.0 / 3.0}
    base = {}
    vectorlike = {}
    for name, coefficients in scenarios.items():
        base[name] = bridge.best_unification_for_fixed_breaking(inputs, coefficients, fixed_scale)
        shifted = {key: coefficients[key] + shift[key] for key in ("R", "L", "4")}
        vectorlike[name] = bridge.best_unification_for_fixed_breaking(inputs, shifted, fixed_scale)
    output = {
        "gate": "version4_pati_salam_bv_multiplicity_fork",
        "existing_module": {"particle_dimension": 16, "KO6_dimension": 32, "contains_relative_chain": False},
        "relative_chain": {"path": "4bar -> 2_R -> 4", "particle_dimension": 10, "KO6_dimension": 20},
        "standard_BV_auxiliary": {
            "contractible_gauge_fixing_pairs": True,
            "changes_classical_vacuum": False,
            "can_supply_relative_weight": False,
        },
        "physical_vectorlike_branch": {
            "SU4_Dirac_fundamentals": 2,
            "SU2R_Dirac_doublets": 1,
            "anomaly_safe": True,
            "beta_shift_R_L_4": shift,
            "base_running": base,
            "running_with_chain": vectorlike,
            "passes_one_percent_gate": min(item["relative_spread"] for item in vectorlike.values()) < 0.01,
        },
        "classical_mapping_cone_branch": {
            "new_propagating_states": 0,
            "beta_shift_R_L_4": {"R": 0.0, "L": 0.0, "4": 0.0},
            "lambda_rule": "lambda_relative=k",
            "minimal_copy_number": 1,
            "minimal_choice_derived": False,
        },
        "copy_number_Hessian": [hessian(number) for number in range(1, 5)],
        "verdict": "standard BV no-go; physical vectorlike versus classical mapping-cone architecture fork",
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")
    for name in scenarios:
        print(name, f"{100*base[name]['relative_spread']:.3f}% -> {100*vectorlike[name]['relative_spread']:.3f}%")


if __name__ == "__main__":
    main()