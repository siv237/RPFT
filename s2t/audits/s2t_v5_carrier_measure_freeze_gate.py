#!/usr/bin/env python3
"""Machine ledger for the Version V carrier parent-measure freeze gate."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUTPUT = RESULTS / "s2t_v5_carrier_measure_freeze_gate_results.json"


def load(name):
    with (RESULTS / name).open(encoding="utf-8") as handle:
        return json.load(handle)


one_kernel = load("s2t_v4_one_kernel_sign_trilemma_gate_results.json")
counterterms = load("s2t_v4_full_field_carrier_counterterm_gate_results.json")
bare = load("s2t_v4_gaussian_bare_spectral_topology_gate_results.json")
retrospective = load("s2t_v4_project_retrospective_entropy_measure_gate_results.json")

toe65_path = ROOT / "s2t/17705966/ТОЕ 6.5.pdf"
toe65_sha256 = hashlib.sha256(toe65_path.read_bytes()).hexdigest()
toe65_rows = [row for row in retrospective["pdfs"] if row["path"].endswith("ТОЕ 6.5.pdf")]
assert len(toe65_rows) == 1
toe65_metadata = toe65_rows[0]
assert toe65_metadata["pages"] == 6

assert one_kernel["verdict"] == "one trace and minus-log trace have opposite carrier minima"
assert one_kernel["scalar"]["bare_winner"] != one_kernel["scalar"]["Gibbs_winner"]
assert one_kernel["Dirac"]["bare_winner"] != one_kernel["Dirac"]["Gibbs_winner"]

reversal = counterterms["finite_counterterm_reversal_witnesses"]
assert all(row["both_signs_allowed_until_c_R_is_fixed"] if key == "Einstein" else True for key, row in reversal.items())
assert reversal["Weyl_squared"]["both_signs_allowed_until_c_W_is_fixed"]
assert reversal["Euler"]["both_signs_allowed_until_topology_weight_is_fixed"]
assert bare["verdict"].startswith("Gaussian_bare_spectral_action_fixes")

requirements = {
    "trace_class_logarithmic_generator": {
        "pass": True,
        "reason": "H_C=-tau^-1 log C is well defined on the support",
    },
    "normalized_state_at_fixed_carrier": {
        "pass": True,
        "reason": "Gibbs variation fixes rho=C/Tr C for fixed H_C",
    },
    "entropy_coefficient_source_derived": {
        "pass": False,
        "reason": "TOE 6.5 treats T_eff as a roadmap variable",
    },
    "carrier_prior_measure_defined": {
        "pass": False,
        "reason": "TOE 6.5 varies spectral density but gives no measure on metrics/topologies",
    },
    "unique_primary_semantics": {
        "pass": False,
        "reason": "outer-log Gibbs and positive bare trace have opposite carrier orderings",
    },
    "finite_curvature_topology_weights_derived": {
        "pass": False,
        "reason": "finite Einstein, Weyl-squared and Euler terms reverse cross-topology ordering",
    },
    "scalar_nonminimal_couplings_derived": {
        "pass": False,
        "reason": "not fixed by the source functional",
    },
    "field_ghost_BV_measure_frozen": {
        "pass": False,
        "reason": "the full scalar-vector-ghost-Dirac measure is absent",
    },
    "massive_vector_completion_derived": {
        "pass": False,
        "reason": "Proca/Stueckelberg/Higgs origin is external",
    },
    "joint_off_shell_hessian_defined": {
        "pass": False,
        "reason": "the functional and measure are not uniquely frozen",
    },
    "observed_inputs_used": {
        "pass": True,
        "reason": "no masses, couplings or mixing data enter this gate",
    },
}

parent_requirements = [
    key for key in requirements if key not in {"observed_inputs_used"}
]
passed_parent_requirements = [key for key in parent_requirements if requirements[key]["pass"]]
failed_parent_requirements = [key for key in parent_requirements if not requirements[key]["pass"]]

assert passed_parent_requirements == [
    "trace_class_logarithmic_generator",
    "normalized_state_at_fixed_carrier",
]
assert len(failed_parent_requirements) == 8

result = {
    "date": "2026-08-15",
    "gate": "version5_carrier_measure_freeze_gate",
    "primary_source": {
        "path": "s2t/17705966/ТОЕ 6.5.pdf",
        "sha256": toe65_sha256,
        "pages": toe65_metadata["pages"],
        "extracted_characters_in_retrospective_audit": toe65_metadata["extracted_characters"],
        "status": "proof_roadmap_not_frozen_parent_measure",
        "open_source_variables": [
            "T_eff",
            "cutoff function f",
            "regulator scale sigma",
            "mode-number constraint and multiplier mu",
            "positive spectral-density function space",
            "modified heat-kernel density",
            "parametric ansatz and background",
        ],
    },
    "exact_witnesses": {
        "one_kernel_time": one_kernel["time"],
        "scalar_bare_winner": one_kernel["scalar"]["bare_winner"],
        "scalar_gibbs_winner": one_kernel["scalar"]["Gibbs_winner"],
        "Dirac_bare_winner": one_kernel["Dirac"]["bare_winner"],
        "Dirac_gibbs_winner": one_kernel["Dirac"]["Gibbs_winner"],
        "delta_integral_R": counterterms["difference_S4_minus_S2xS2"]["integral_R"],
        "delta_integral_Weyl2": counterterms["difference_S4_minus_S2xS2"]["integral_Weyl2"],
        "delta_integral_Euler": counterterms["difference_S4_minus_S2xS2"]["integral_Euler_density"],
        "gaussian_crossing_time": bare["exact_heat_trace"]["crossing_time"],
        "gaussian_cutoff_warning": bare["correlation_cell_map"]["warning"],
    },
    "requirements": requirements,
    "summary_counts": {
        "parent_requirements": len(parent_requirements),
        "passed": len(passed_parent_requirements),
        "failed": len(failed_parent_requirements),
    },
    "verdict": {
        "state_normalization": "pass",
        "parent_measure": "fail",
        "current_carrier_first_architecture": "closed_before_spectral_sums_and_phenomenology",
        "mathematical_architecture_passes": 0,
        "physical_closures": 0,
    },
    "reopening_requires": [
        "an a priori measure on metrics and topologies",
        "derived T_eff, tau, Lambda and their relation",
        "full bare and renormalized curvature couplings",
        "field/BV measure and massive-vector origin",
        "one functional or a derived hierarchy with no free relative weight",
    ],
    "next_gate": "version5_boundary_parent_trace_freeze_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))