import json
import math
from pathlib import Path

# Conditional derivation of why the mixed Maxwell--ghost perturbation B can couple
# to P_{0,2}: if the allowed geometric perturbations are first-order homogeneous
# ambient deformations of S^3 ⊂ R^4, then they are parametrized by symmetric A_ab.
# The induced radial/conformal strain on the unit sphere is q_A(x)=x^T A x.
# q_A is even under x -> -x and therefore descends to RP^3. Its trace part is
# constant (ell=0); its traceless part is a quadratic harmonic (ell=2). Thus the
# perturbation space has rank dim Sym^2(R^4)=10 and is precisely P_{0,2}.

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
BASE_TOWER = (math.pi**2 / 2) * T_RP3 / S_GEO
P02_RANK = 10
TERM_WITH_P02 = BASE_TOWER * (1 - P02_RANK / (24 * S_GEO))

ambient_dim = 4
sym2_basis = []
for a in range(ambient_dim):
    for b in range(a, ambient_dim):
        sym2_basis.append((a, b))

trace_basis = ["delta_ab x^a x^b = |x|^2 = 1 on S^3"]
traceless_rank = len(sym2_basis) - 1

derivation_steps = [
    {
        "step": "gauge_fixed_one_loop_combination",
        "formula": "Gamma_gauge^(1)=1/2 log det' Delta_{1,coex} - 1/2 log det' Delta_0 plus zero-mode/gauge-volume terms",
        "source": "local RPFT-main/rigorous/30_qed_one_loop_proof.md section 30.4",
    },
    {
        "step": "metric_variation_of_logdet",
        "formula": "delta log det Delta = Tr(Delta^{-1} delta_g Delta)",
        "implication": "The mixed operator B is delta_g Delta evaluated on the allowed metric/volume strain h.",
    },
    {
        "step": "ambient_linear_deformation",
        "formula": "x -> (I + eps A)x, A_ab=A_ba after removing rotations",
        "implication": "Antisymmetric A are SO(4) rotations/isometries and do not produce physical strain; symmetric A parametrize first shape/scale strain.",
    },
    {
        "step": "quadratic_strain",
        "formula": "q_A(x)=x^T A x",
        "implication": "q_A(-x)=q_A(x), so q_A descends to RP^3.",
    },
    {
        "step": "harmonic_decomposition",
        "formula": "Sym^2(R^4)=R delta_ab ⊕ Sym^2_0(R^4)",
        "implication": "trace gives ell=0; traceless quadratics give ell=2 with dimension 9.",
    },
]

conditions = [
    {
        "condition": "allowed_metric_strains_are_ambient_linear_deformations",
        "status": "assumption_to_promote_to_axiom_or_derive_from_minimal_carrier",
        "why_needed": "Without this restriction, generic metric variations contain higher harmonics and the full scalar tower can enter."
    },
    {
        "condition": "antisymmetric_part_is_gauge_or_isometry",
        "status": "standard_geometric_fact",
        "why_needed": "It reduces GL(4) first deformations to Sym^2(R^4), not all 16 linear maps."
    },
    {
        "condition": "radial_trace_part_matches_scalar_casimir_branch",
        "status": "conditional",
        "why_needed": "The ell=0 component must be the finite scalar/ghost branch already responsible for 1/24."
    },
    {
        "condition": "mixed_trace_uses_first_strain_only",
        "status": "not_proven_by_standard_maxwell_alone",
        "why_needed": "Second and higher ambient deformations would generate ell>=4 sectors."
    },
    {
        "condition": "determinant_sign_survives_sector_powers",
        "status": "partially_supported",
        "why_needed": "delta^2 log det gives a negative quadratic trace, but the Maxwell--ghost combination has sector prefactors."
    },
]

results = {
    "status": "conditional_derivation_of_B_coupling_to_P02_from_ambient_metric_strain",
    "numbers": {
        "ambient_dim": ambient_dim,
        "sym2_rank": len(sym2_basis),
        "trace_rank_ell0": 1,
        "traceless_rank_ell2": traceless_rank,
        "P02_rank": P02_RANK,
        "S_geo": S_GEO,
        "term_with_P02": TERM_WITH_P02,
        "pi4_term": PI4_TERM,
        "relative_error_vs_pi4": (TERM_WITH_P02 - PI4_TERM) / PI4_TERM,
    },
    "sym2_basis_indices": sym2_basis,
    "trace_basis": trace_basis,
    "derivation_steps": derivation_steps,
    "conditions": conditions,
    "verdict": (
        "The coupling B to P_{0,2} can be conditionally derived if the mixed Maxwell--ghost perturbation is the metric variation of the determinant under first ambient linear deformations of S^3/RP^3. The physical strain space is Sym^2(R^4): antisymmetric parts are rotations, trace is ell=0, and traceless symmetric parts are ell=2. This gives rank 10 and excludes ell>=4 as higher-than-linear ambient strains. The remaining nontrivial assumption is that S2T permits only this first-strain channel in the mixed pi^-4 term."
    ),
}

Path("s2t_metric_variation_p02_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(results["numbers"], indent=2, ensure_ascii=False))
print(results["verdict"])