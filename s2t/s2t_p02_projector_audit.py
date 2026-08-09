import json
import math
from pathlib import Path

# Ambient realization: S^3 is embedded in R^4 with coordinates x_a.
# Even quadratic functions x_a x_b descend to RP^3. Symmetric bilinears have
# dimension dim Sym^2(R^4)=4*5/2=10 and decompose into trace + traceless:
#   trace part: r^2=1 -> ell=0, dimension 1
#   traceless symmetric part -> ell=2 scalar harmonics, dimension 9.
# This gives a natural finite projector P_{0,2} if the mixed operator B is a
# first-order homogeneous quadratic strain/metric-volume perturbation.

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
BASE_TOWER = (math.pi**2 / 2) * T_RP3 / S_GEO
EPS_NEEDED = 1 - PI4_TERM / BASE_TOWER
N_NEED = 24 * S_GEO * EPS_NEEDED

ambient_dim = 4
sym2_dim = ambient_dim * (ambient_dim + 1) // 2
trace_dim = 1
traceless_sym2_dim = sym2_dim - trace_dim
rp3_even_scalar_l0 = 1
rp3_even_scalar_l2 = (2 + 1) ** 2

candidate = {
    "projector": "P_0_2 = projection onto restrictions of ambient quadratic even functions x_a x_b on S^3/RP^3",
    "ambient_dim": ambient_dim,
    "sym2_dim": sym2_dim,
    "trace_dim_ell0": trace_dim,
    "traceless_sym2_dim_ell2": traceless_sym2_dim,
    "rp3_even_scalar_l0": rp3_even_scalar_l0,
    "rp3_even_scalar_l2": rp3_even_scalar_l2,
    "rank": sym2_dim,
    "matches_scalar_shells": sym2_dim == rp3_even_scalar_l0 + rp3_even_scalar_l2,
    "matches_needed_integer": round(N_NEED) == sym2_dim,
}

term_with_projector = BASE_TOWER * (1 - sym2_dim / (24 * S_GEO))

conditions = [
    {
        "condition": "mixed_operator_is_quadratic_strain",
        "meaning": "The perturbation B in the mixed determinant trace must come from first-order ambient quadratic metric/volume strain h_ab x^a x^b, not from the full scalar determinant tower.",
        "status": "new_required_assumption_or_derivation"
    },
    {
        "condition": "projector_precedes_scalar_tower",
        "meaning": "P_0_2 must act before scalar/exact spectral summation; otherwise ordinary exact inheritance includes all ell>0 even shells.",
        "status": "required"
    },
    {
        "condition": "trace_part_counts_as_casimir_branch",
        "meaning": "The ell=0 trace component must be interpreted as the periodic scalar/ghost Casimir branch or gauge-volume finite part, not as a nonzero exact one-form.",
        "status": "required"
    },
    {
        "condition": "traceless_part_counts_as_first_shape_strain",
        "meaning": "The ell=2 dimension-9 sector is the traceless quadratic shape/strain sector on RP^3.",
        "status": "representation_theoretically_natural"
    },
    {
        "condition": "gauge_invariant_coupling",
        "meaning": "The Maxwell--ghost mixed trace must couple to this quadratic strain space in a gauge-invariant way with the determinant-expansion minus sign.",
        "status": "not_proven_here"
    }
]

controls = []
for ell_max in [0, 2, 4, 6, 8]:
    cumulative = sum((ell + 1) ** 2 for ell in range(0, ell_max + 1, 2))
    term = BASE_TOWER * (1 - cumulative / (24 * S_GEO))
    controls.append({
        "selection": f"ordinary_scalar_cumulative_through_ell_{ell_max}",
        "rank": cumulative,
        "relative_error_vs_pi4": (term - PI4_TERM) / PI4_TERM,
        "natural_as_quadratic_strain": ell_max == 2,
    })

results = {
    "status": "p02_projector_has_representation_theoretic_candidate_not_full_determinant_proof",
    "numbers": {
        "S_geo": S_GEO,
        "pi4_term": PI4_TERM,
        "base_tower": BASE_TOWER,
        "N_need": N_NEED,
        "projector_rank": sym2_dim,
        "term_with_P02": term_with_projector,
        "relative_error_vs_pi4": (term_with_projector - PI4_TERM) / PI4_TERM,
    },
    "candidate": candidate,
    "conditions": conditions,
    "controls": controls,
    "verdict": (
        "A natural finite-rank P_0,2 candidate exists if the mixed determinant perturbation is not the full scalar/exact tower, "
        "but the ambient quadratic strain sector Sym^2(R^4) restricted to S^3/RP^3. This space has dimension 10 and decomposes "
        "as ell=0 trace plus ell=2 traceless harmonics, i.e. 1+9. This explains why ell>=4 are excluded: they are higher-than-quadratic "
        "ambient deformations. However, the remaining proof obligation is to derive that the Maxwell--ghost mixed operator B is exactly this "
        "quadratic strain projector with the required determinant sign."
    )
}

Path("s2t_p02_projector_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(results["numbers"], indent=2, ensure_ascii=False))
print(results["verdict"])