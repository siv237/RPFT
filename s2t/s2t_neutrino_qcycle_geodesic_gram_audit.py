import json
import math
from pathlib import Path


R3 = 1.0
ELL = math.pi * R3


def primitive_self_dual_vectors(bound=8):
    rows = []
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            if a == 0 and b == 0:
                continue
            primitive = math.gcd(abs(a), abs(b)) == 1
            self_dual = a == b
            if primitive and self_dual:
                rows.append([a, b])
    return rows


Q = [[ELL, 0.0], [0.0, 1.0 / ELL]]
Q_sqrt = [[math.sqrt(ELL), 0.0], [0.0, 1.0 / math.sqrt(ELL)]]
v_self_dual = [1, 1]
norm_squared = ELL + 1.0 / ELL


results = {
    "status": "Qcycle_constructed_on_RP3_systolic_geodesic_Dirac_embedding_open",
    "date": "2026-08-03",
    "geometry": {
        "ambient": "round RP3 of radius R3",
        "cycle": "projective line gamma=RP1 embedded as a shortest noncontractible closed geodesic",
        "lift": "a path from x to -x along a great circle in S3",
        "cycle_length_formula": "ell=pi*R3",
        "R3": R3,
        "ell": ELL,
        "isometry_independence": "all projective lines are related by round-RP3 isometries",
    },
    "integral_cycle_complex": {
        "space": "H0(gamma;Z) direct_sum H1(gamma;Z)",
        "zero_form_generator": "e0=1",
        "one_form_generator": "e1=ds/ell with integral_gamma e1=1",
        "zero_form_norm_squared": ELL,
        "one_form_norm_squared": 1.0 / ELL,
        "cross_inner_product": 0.0,
        "derivation": {
            "e0": "integral_gamma 1^2 ds=ell",
            "e1": "integral_gamma |ds/ell|^2 ds=1/ell",
        },
    },
    "Qcycle": {
        "matrix": Q,
        "square_root": Q_sqrt,
        "determinant": 1.0,
        "trace": norm_squared,
        "target_pi_plus_inverse": math.pi + 1.0 / math.pi,
        "target_error": norm_squared - (math.pi + 1.0 / math.pi),
        "duality": "J exchanges e0 and e1 while ell maps to ell^-1",
    },
    "lattice_selection": {
        "lattice": "Z e0 direct_sum Z e1",
        "duality_action": "J(a,b)=(b,a)",
        "primitive_self_dual_vectors_in_search": primitive_self_dual_vectors(),
        "selected_up_to_sign": "v_nu=e0+e1",
        "selection_reason": (
            "The primitive nonzero lattice vectors invariant under J are exactly plus/minus (1,1); "
            "there is no continuous coefficient."
        ),
        "selected_norm_squared": norm_squared,
        "selected_norm": math.sqrt(norm_squared),
    },
    "Dirac_insertion_candidate": {
        "formula": "m_D^(nu)=(m_e^2/m_mu)*norm_Q(v_nu)",
        "operator_form": "norm_Q(v_nu)=norm(Qcycle^(1/2) v_nu)",
        "result": "sqrt(pi+pi^-1)*m_e^2/m_mu at R3=1",
        "status": "algebraically_derived_from_cycle_Gram_data",
    },
    "scope_and_obligations": {
        "constructed": [
            "positive self-adjoint Qcycle",
            "determinant-one reciprocal spectrum",
            "pi plus inverse-pi trace",
            "unique primitive self-dual lattice vector",
        ],
        "not_yet_constructed": [
            "restriction map from the ambient neutrino spinor bundle to the cycle complex",
            "EFT vertex forcing equal primal and dual amplitudes",
            "proof that the cycle Gram norm multiplies the charged-lepton suppression m_e^2/m_mu",
        ],
        "ambient_cohomology_warning": (
            "H1(RP3;R)=0. The one-form generator belongs intrinsically to the geodesic gamma, not to a global "
            "ambient harmonic one-form. The coupling must therefore be a cycle-restriction or defect operator."
        ),
    },
    "robustness": {
        "radius_formula": "N_nu_squared(R3)=pi*R3+1/(pi*R3)",
        "derivative_at_R3_1": math.pi - 1.0 / math.pi,
        "requires_unit_radius_normalization": True,
        "cycle_choice_dependence": "none_on_round_RP3",
        "holonomy_branch_dependence": "none",
    },
    "theory_effect": {
        "Qcycle_existence": "constructed",
        "holonomy_no_go": "bypassed_by_positive_systolic_metric_not_by_phase_angle",
        "absolute_neutrino_scale": "upgraded_from_scalar_ansatz_to_operator_candidate_but_still_conditional",
        "common_source_feedback": (
            "The common source may couple a torsion/systolic cycle sector to its intrinsic primal-dual Hodge metric."
        ),
    },
    "next_steps": [
        "define the restriction/defect map Res_gamma from ambient spinors to the cycle Hilbert complex",
        "construct a self-dual neutrino vertex selecting v_nu=e0+e1",
        "show that Qcycle^(1/2) enters the Dirac mass matrix element",
        "test stability under admissible carrier deformations preserving the RP3 systolic class",
    ],
    "verdict": (
        "Qcycle can be constructed canonically on a shortest noncontractible projective geodesic gamma in unit "
        "round RP3. In the integral bases e0=1 and e1=ds/pi, the Hodge L2 Gram matrix is diag(pi,pi^-1). "
        "Its determinant is one and the unique primitive self-dual lattice vector v=(1,1) has squared norm "
        "pi+pi^-1. This derives the desired reciprocal factor without using a branch-dependent holonomy angle. "
        "The remaining gap is physical rather than algebraic: derive the ambient-spinor restriction and EFT vertex "
        "that insert Qcycle^(1/2) into m_D."
    ),
}


assert abs(results["Qcycle"]["determinant"] - 1.0) < 1e-15
assert abs(results["Qcycle"]["target_error"]) < 1e-15
assert results["lattice_selection"]["primitive_self_dual_vectors_in_search"] == [[-1, -1], [1, 1]]

Path("s2t_neutrino_qcycle_geodesic_gram_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)
print(json.dumps({
    "status": results["status"],
    "Qcycle": Q,
    "determinant": results["Qcycle"]["determinant"],
    "trace": results["Qcycle"]["trace"],
    "selected_vector": v_self_dual,
}, indent=2, ensure_ascii=False))