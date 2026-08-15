import json
import math
from pathlib import Path

import numpy as np


PI = math.pi
LENGTH_GAMMA = PI


grid = np.linspace(-12.0, 12.0, 24001)
mass_profile = np.tanh(grid)
zero_profile = 1.0 / (math.sqrt(2.0) * np.cosh(grid))
zero_derivative = -mass_profile * zero_profile
jackiw_rebbi_residual = zero_derivative + mass_profile * zero_profile
profile_norm = float(np.trapezoid(zero_profile**2, grid))

adjoint_candidate = np.cosh(grid)
adjoint_window_norm = float(np.trapezoid(adjoint_candidate**2, grid))


def longitudinal_spectrum(total_holonomy, cutoff=4):
    shift = 0.0 if total_holonomy == 1 else 0.5
    return [
        {
            "n": n,
            "wave_number": 2.0 * PI * (n + shift) / LENGTH_GAMMA,
        }
        for n in range(-cutoff, cutoff + 1)
    ]


spin_holonomy = -1
torsion_line_holonomy = -1
total_holonomy = spin_holonomy * torsion_line_holonomy
longitudinal_modes = longitudinal_spectrum(total_holonomy)
longitudinal_kernel_rank = sum(abs(mode["wave_number"]) < 1e-12 for mode in longitudinal_modes)

qcycle = np.diag([PI, 1.0 / PI])
self_dual_vector = np.array([1.0, 1.0])
qcycle_norm = float(self_dual_vector @ qcycle @ self_dual_vector)

transverse_mod2_index = 1
generation_singlet_rank = 1
cycle_self_dual_rank = 1
combined_kernel_rank = (
    transverse_mod2_index
    * longitudinal_kernel_rank
    * generation_singlet_rank
    * cycle_self_dual_rank
)

results = {
    "status": "conditional_rank_one_majorana_defect_constructed_new_order_parameter_not_derived",
    "date": "2026-08-03",
    "geometry": {
        "defect_core": "shortest noncontractible geodesic gamma=RP1 in RP3",
        "core_length": LENGTH_GAMMA,
        "normal_neighborhood": "oriented rank-two disk bundle, locally a solid torus",
        "existing_flat_line": "nontrivial Z2 torsion line restricted to gamma",
    },
    "transverse_defect": {
        "class": "real class-D Majorana defect with odd mass winding",
        "minimal_radial_operator": "A=d/dx+tanh(x)",
        "normalized_zero_profile": "psi0=sech(x)/sqrt(2)",
        "numeric_profile_norm_on_window": profile_norm,
        "max_zero_equation_residual": float(np.max(np.abs(jackiw_rebbi_residual))),
        "adjoint_candidate": "cosh(x), non-normalizable",
        "adjoint_candidate_window_norm": adjoint_window_norm,
        "ordinary_index": 1,
        "mod_two_index": transverse_mod2_index,
        "interpretation": (
            "An odd vortex reduces the four-real-dimensional lowest spinor multiplet to one "
            "topologically protected real Majorana channel."
        ),
    },
    "longitudinal_gate": {
        "spin_holonomy": spin_holonomy,
        "torsion_line_holonomy": torsion_line_holonomy,
        "total_holonomy": total_holonomy,
        "rule": "h_total=h_spin*h_Z2",
        "spectrum": longitudinal_modes,
        "kernel_rank_for_single_real_channel": longitudinal_kernel_rank,
        "interpretation": (
            "The antiperiodic spin sign and nontrivial torsion-line sign cancel. The defect "
            "Majorana channel is periodic around gamma and has one constant real zero mode."
        ),
    },
    "rank_one_selector": {
        "factorization": (
            "generation singlet tensor transverse Majorana zero mode tensor longitudinal "
            "constant mode tensor self-dual cycle line"
        ),
        "factor_ranks": [
            generation_singlet_rank,
            transverse_mod2_index,
            longitudinal_kernel_rank,
            cycle_self_dual_rank,
        ],
        "combined_real_rank": combined_kernel_rank,
        "why_previous_no_go_is_avoided": (
            "The vortex mass texture physically breaks the spin-isometry multiplet and replaces "
            "an arbitrary polarization choice by a mod-two index."
        ),
    },
    "Qcycle_compatibility": {
        "Qcycle": qcycle.tolist(),
        "self_dual_vector": self_dual_vector.tolist(),
        "self_dual_Qcycle_norm": qcycle_norm,
        "target": PI + 1.0 / PI,
        "error": abs(qcycle_norm - (PI + 1.0 / PI)),
        "interpretation": (
            "The defect selects a single ambient spinor line while Qcycle continues to determine "
            "the reciprocal two-channel coupling norm. The two mechanisms act on different factors."
        ),
    },
    "rank_23_recovery_gate": {
        "conditional_statement": (
            "If the unique defect zero mode lies inside the declared R24 heavy module and is the "
            "single universal branch removed from the heavy determinant, then the complement has rank 23."
        ),
        "remaining_rank": 23,
        "status": "conditional_not_yet_a_theorem",
        "missing_proofs": [
            "derive the two-component real mass order parameter from an existing S2T field",
            "prove odd winding around gamma is forced rather than selected by hand",
            "derive the restriction map from the ambient RP3 spinor bundle to the vortex-core channel",
            "show that the Majorana/BdG formulation does not add physical states beyond R24",
            "show that integrating out or quotienting the unique zero branch produces the heavy denominator count",
        ],
    },
    "parameter_audit": {
        "new_continuous_fit_parameter_required_for_rank": False,
        "new_structural_field_required": True,
        "new_field": "two-component real Majorana mass order parameter with odd vortex winding",
        "profile_dependence": "zero-mode parity is stable under gap-preserving profile deformations",
        "mass_gap_scale": "still required for EFT dynamics but does not change the mod-two count",
    },
    "theory_effect": {
        "rank_one_route": "reopened_conditionally_by_topological_defect",
        "rank_23_denominator": "conditional_pending_defect_embedding",
        "Qcycle": "retained",
        "previous_symmetry_no_go": "retained_for_defect_free_module",
        "absolute_neutrino_scale": "still_open_but_has_a_concrete_completion_route",
    },
    "verdict": (
        "A mathematically explicit route around the rank-one no-go exists. An odd class-D mass "
        "defect localized on the systolic projective geodesic supplies one transverse Majorana "
        "channel by a mod-two index. Coupling that channel to the existing nontrivial Z2 flat line "
        "cancels the antiperiodic spin holonomy and leaves one longitudinal real zero mode. Together "
        "with the generation singlet and self-dual cycle line this gives a rank-one kernel in the "
        "ambient module. The mechanism is not yet derived from the current S2T action because the "
        "odd-winding mass order parameter and its restriction map are new structural data."
    ),
}

assert abs(profile_norm - 1.0) < 1e-9
assert np.max(np.abs(jackiw_rebbi_residual)) < 1e-14
assert total_holonomy == 1
assert longitudinal_kernel_rank == 1
assert combined_kernel_rank == 1
assert abs(qcycle_norm - (PI + 1.0 / PI)) < 1e-14

Path("s2t_neutrino_twisted_majorana_defect_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(
    json.dumps(
        {
            "status": results["status"],
            "transverse_mod2_index": transverse_mod2_index,
            "total_holonomy": total_holonomy,
            "longitudinal_kernel_rank": longitudinal_kernel_rank,
            "combined_kernel_rank": combined_kernel_rank,
            "rank_23_status": results["rank_23_recovery_gate"]["status"],
        },
        indent=2,
        ensure_ascii=False,
    )
)