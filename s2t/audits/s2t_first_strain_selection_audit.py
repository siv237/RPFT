import json
from pathlib import Path

# S2T selection audit: which metric-perturbation class is admissible for the pi^-4 mixed term?
# The criterion is not numerical fit but S2T minimality:
# 1. no new continuous moduli after fixing K and radii,
# 2. preserve the constant-curvature carrier class at first order,
# 3. be representation-theoretically canonical under the S^3 cover / SO(4),
# 4. produce a finite trace rank before scalar-tower summation,
# 5. not introduce an arbitrary cutoff or selected ell by hand.

candidates = [
    {
        "name": "arbitrary_internal_metric_perturbation",
        "description": "Generic symmetric 2-tensor h_ij(y) on RP^3.",
        "finite_rank": False,
        "canonical_under_so4": False,
        "preserves_minimal_carrier_class": False,
        "introduces_continuous_moduli": True,
        "selects_ell_0_2_without_cutoff": False,
        "rank": "infinite/full tensor tower",
        "verdict": "forbidden_for_IIA_mixed_residue"
    },
    {
        "name": "ordinary_scalar_exact_tower",
        "description": "Use scalar/exact inheritance directly after Hodge decomposition.",
        "finite_rank": False,
        "canonical_under_so4": True,
        "preserves_minimal_carrier_class": True,
        "introduces_continuous_moduli": False,
        "selects_ell_0_2_without_cutoff": False,
        "rank": "full even scalar tower",
        "verdict": "fails_shell_selection"
    },
    {
        "name": "manual_ell_0_2_cutoff",
        "description": "Select ell=0,2 by hand from scalar tower.",
        "finite_rank": True,
        "canonical_under_so4": False,
        "preserves_minimal_carrier_class": None,
        "introduces_continuous_moduli": False,
        "selects_ell_0_2_without_cutoff": False,
        "rank": 10,
        "verdict": "forbidden_hidden_discrete_cutoff"
    },
    {
        "name": "first_ambient_linear_strain",
        "description": "Allowed first strain of S^3 subset R^4: x -> (I+eps A)x, quotient by rotations; symmetric A gives q_A=x^T A x.",
        "finite_rank": True,
        "canonical_under_so4": True,
        "preserves_minimal_carrier_class": True,
        "introduces_continuous_moduli": False,
        "selects_ell_0_2_without_cutoff": True,
        "rank": 10,
        "verdict": "unique_minimal_admissible_candidate"
    },
    {
        "name": "higher_ambient_polynomial_strain_degree_4",
        "description": "Allow quartic ambient deformations generating ell=0,2,4 sectors.",
        "finite_rank": True,
        "canonical_under_so4": True,
        "preserves_minimal_carrier_class": False,
        "introduces_continuous_moduli": True,
        "selects_ell_0_2_without_cutoff": False,
        "rank": "larger than 10",
        "verdict": "forbidden_until_new_sector_derived"
    }
]

criteria = [
    "K=RP3xS1 and radii are fixed before blind comparison",
    "b1(RP3)=0 excludes continuous U(1) moduli; analogous metric moduli are not allowed in II.A unless derived",
    "constant positive curvature carrier means arbitrary h_ij is outside the minimal carrier class",
    "a mixed determinant residue may use a tangent/strain channel, but S2T minimality permits only the first canonical tangent channel",
    "first ambient linear strain is canonical for S3 cover and descends to RP3 because q_A(-x)=q_A(x)",
    "higher polynomial strains constitute new sectors and would introduce extra discrete/continuous choices"
]

winner = [c for c in candidates if c["verdict"] == "unique_minimal_admissible_candidate"][0]

results = {
    "status": "first_ambient_strain_selected_by_S2T_minimality",
    "criteria": criteria,
    "candidates": candidates,
    "selected": winner,
    "derived_rule": "For the II.A pi^-4 mixed determinant residue, admissible metric perturbations are restricted to the first canonical ambient strain channel Sym^2(R^4), unless a new sector is explicitly derived and audited.",
    "remaining_risk": "This is an S2T selection theorem, not a full microscopic QED theorem. A future broader model may include higher metric strains, but then pi^-4 must be recomputed rather than using the II.A closure row.",
}

Path("s2t_first_strain_selection_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({"status": results["status"], "selected": winner["name"], "rank": winner["rank"]}, indent=2, ensure_ascii=False))