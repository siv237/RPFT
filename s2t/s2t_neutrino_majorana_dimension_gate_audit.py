import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
ME_MEV = 0.51099895069
MMU_MEV = 105.6583755
N2 = PI + 1.0 / PI


def generation_projectors():
    u = np.ones((3, 1)) / math.sqrt(3)
    p_singlet = u @ u.T
    p_traceless = np.eye(3) - p_singlet
    return p_singlet, p_traceless


def prediction(integer_part):
    denominator = integer_part + 1.0 / PI
    ratio = denominator + PI**2 + 2.0 / 3.0
    mu_eV = N2 * ME_MEV**4 / (MMU_MEV**3 * denominator) * 1e6
    return {
        "integer_part": integer_part,
        "D_nu": denominator,
        "R_nu": ratio,
        "mu_nu_eV": mu_eV,
        "dm21_eV2": mu_eV**2,
        "dm31_eV2": ratio * mu_eV**2,
    }


p_singlet, p_traceless = generation_projectors()

module_cases = []
for label, internal_real_dimension in [
    ("physical_4D_Majorana", 4),
    ("Euclidean_Dirac_realification_or_symplectic_Majorana", 8),
]:
    full_dimension = 3 * internal_real_dimension
    singlet_projector = np.kron(p_singlet, np.eye(internal_real_dimension))
    traceless_projector = np.kron(p_traceless, np.eye(internal_real_dimension))
    module_cases.append(
        {
            "case": label,
            "internal_real_dimension_per_generation": internal_real_dimension,
            "full_real_dimension": full_dimension,
            "rank_generation_singlet_submodule": int(np.linalg.matrix_rank(singlet_projector)),
            "rank_generation_traceless_submodule": int(np.linalg.matrix_rank(traceless_projector)),
            "naive_full_minus_one": full_dimension - 1,
            "generation_covariant_result": 2 * internal_real_dimension,
            "projector_idempotence_error": float(
                np.max(np.abs(traceless_projector @ traceless_projector - traceless_projector))
            ),
        }
    )


DM21_NUFIT = 7.49e-5
DM31_NUFIT = 2.513e-3
ratio_nufit = DM31_NUFIT / DM21_NUFIT
integer_part_required_by_ratio = ratio_nufit - PI**2 - 2.0 / 3.0 - 1.0 / PI


results = {
    "status": "neutrino_23_count_not_derived_generation_singlet_removes_full_internal_module",
    "date": "2026-08-03",
    "dimension_statement": {
        "physical_Majorana_4D": (
            "A four-dimensional Minkowski Majorana spinor has four real off-shell components."
        ),
        "Euclidean_internal_spinor": (
            "A complex four-component Euclidean Dirac spinor has eight real components, but this is a "
            "realification rather than an ordinary four-dimensional Majorana condition. An eight-real "
            "symplectic-Majorana interpretation requires an explicit doublet/reality structure."
        ),
    },
    "generation_projector": {
        "P_singlet": p_singlet.tolist(),
        "P_traceless": p_traceless.tolist(),
        "rule": "P0_total=P_traceless tensor I_internal",
        "consequence": (
            "Removing the generation-singlet field removes one full copy of the internal spinor module, not one "
            "real component."
        ),
    },
    "module_cases": module_cases,
    "rank_one_route_for_23": {
        "required_projector": "P_rank1=|u><u| on the full R24 module",
        "resulting_rank": 23,
        "status": "mathematically_possible_but_not_generation_singlet_and_not_yet_canonical",
        "obligations": [
            "derive a distinguished normalized vector u in generation tensor internal-spinor space",
            "show that u is selected by the declared Dirac/Qcycle operator rather than by data",
            "show that removing only u is compatible with spin and generation symmetries",
            "replace the current N_tr generation-field formula by the actual rank-one projector",
        ],
    },
    "prediction_scenarios": [
        prediction(23),
        prediction(20),
        prediction(16),
        prediction(11),
        prediction(8),
    ],
    "phenomenology_diagnostic": {
        "nufit6_ratio_benchmark": ratio_nufit,
        "integer_part_required_by_ratio_central_value": integer_part_required_by_ratio,
        "distance_to_23": integer_part_required_by_ratio - 23,
        "interpretation": (
            "The oscillation ratio numerically favors an integer part near 23, so the dimension argument must be "
            "derived independently to avoid reverse-engineering the observed ratio."
        ),
    },
    "Qcycle_relation": {
        "positive_result": (
            "Qcycle can naturally supply a two-channel metric and may fit inside an eight-real symplectic-Majorana "
            "module."
        ),
        "limitation": (
            "Qcycle does not by itself produce a unique rank-one vector in the remaining spinor and generation "
            "factors, so it does not derive 24-1=23."
        ),
    },
    "theory_effect": {
        "Qcycle_factor": "retained_as_constructed_operator",
        "minimal_cycle_seesaw_contraction": "retained_conditionally",
        "D_nu_23_plus_inverse_pi": "downgraded_to_rank_one_projector_hypothesis",
        "absolute_neutrino_scale": "not_closed",
        "dimensionless_ratio_R_nu": "not_structurally_closed_because_it_contains_23",
    },
    "next_steps": [
        "decide whether the internal module is physical Majorana, Euclidean Dirac realification, or symplectic Majorana",
        "construct the full generation tensor spinor tensor cycle representation",
        "search for a symmetry-protected rank-one kernel vector u",
        "if no rank-one selector exists, replace 23 by the generation-covariant rank and re-evaluate the neutrino model",
    ],
    "verdict": (
        "The written proof of 23 as 3*8-1 is not representation-consistent. If N_tr is the generation-singlet "
        "spinor field, its removal subtracts an entire internal module: eight real dimensions in the declared "
        "eight-real case, leaving 16, not 23. A rank-23 subspace can be obtained only by removing one specified "
        "vector from the full R24 module, but no such canonical vector is currently derived. Qcycle remains a valid "
        "positive reciprocal operator and its seesaw contraction remains algebraically correct, yet the heavy "
        "denominator and therefore R_nu return to conditional status."
    ),
}


assert module_cases[1]["rank_generation_singlet_submodule"] == 8
assert module_cases[1]["rank_generation_traceless_submodule"] == 16
assert module_cases[0]["rank_generation_singlet_submodule"] == 4
assert module_cases[0]["rank_generation_traceless_submodule"] == 8

Path("s2t_neutrino_majorana_dimension_gate_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps({
    "status": results["status"],
    "module_cases": module_cases,
    "integer_part_required_by_ratio": integer_part_required_by_ratio,
}, indent=2, ensure_ascii=False))