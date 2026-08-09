import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
P02_RANK = 10
P02_TRACELESS_RANK = 9
P02_TRACE_RANK = 1

# Representation-level audit for the nonzero scalar residual in standard FP.
# On RP3 = S3/Z2, scalar harmonics descending from S3 have even ell.
# The first nonzero scalar shell is ell=2 with multiplicity (ell+1)^2 = 9.
# A traceless first ambient strain is an ell=2 tensor/scalar channel in Sym^2_0(R4).
# A scalar Laplacian variation contains the scalar stress-tensor insertion
#   delta_h Delta0 ~ -h^{ij} nabla_i nabla_j + lower derivative/divergence terms.
# Therefore its matrix elements follow the usual product/triangle selection rules:
#   ell' in ell \otimes 2, i.e. |ell-2| <= ell' <= ell+2 with parity preserved.
# This audit does not compute the full determinant coefficient; it checks whether
# zero-by-symmetry is available. It is not.

def dim_scalar_s3(ell: int) -> int:
    return (ell + 1) ** 2

def descends_to_rp3(ell: int) -> bool:
    return ell % 2 == 0

def ell2_coupling_allowed(ell_in: int, ell_out: int) -> bool:
    return abs(ell_in - 2) <= ell_out <= ell_in + 2 and (ell_in + ell_out + 2) % 2 == 0

shells = []
for ell in range(0, 12, 2):
    outgoing = [ell_out for ell_out in range(0, 12, 2) if ell2_coupling_allowed(ell, ell_out)]
    shells.append({
        "ell": ell,
        "rp3_allowed": descends_to_rp3(ell),
        "multiplicity": dim_scalar_s3(ell),
        "is_zero_shell": ell == 0,
        "ell2_P02_outgoing_shells": outgoing,
        "diagonal_ell2_coupling_allowed": ell2_coupling_allowed(ell, ell),
    })

nonzero_shells = [row for row in shells if row["ell"] > 0]
first_nonzero = nonzero_shells[0]

variation_terms = [
    {
        "term": "trace_volume_part",
        "rank": P02_TRACE_RANK,
        "selection_status": "allowed_but_volume_local_or_gauge_normalization",
        "meaning": "The trace direction rescales the metric/volume and must be handled by zero/gauge/Jacobian normalization or local counterterms.",
    },
    {
        "term": "traceless_ell2_part",
        "rank": P02_TRACELESS_RANK,
        "selection_status": "allowed_on_nonzero_scalar_tower",
        "meaning": "The ell=2 strain couples even RP3 scalar shells by ell -> ell, ell±2; the first nonzero shell ell=2 already admits diagonal and off-diagonal couplings.",
    },
    {
        "term": "constant_kappa_row",
        "rank": 0,
        "selection_status": "zero_for_traceless_spatial_laplacian_variation",
        "meaning": "The retained kappa_Cas row is constant on RP3, so gradient-based scalar Laplacian variation vanishes on that row.",
    },
]

outcomes = [
    {
        "candidate_verdict": "zero_by_symmetry",
        "status": "failed",
        "reason": "Even RP3 scalar harmonics and ell=2 strain satisfy triangle/parity selection rules; ell=2 nonzero scalar shell couples to ell=0,2,4.",
    },
    {
        "candidate_verdict": "nonzero_but_local_subtracted",
        "status": "not_proven",
        "reason": "Trace/heat-kernel pieces may be local, but the trace-square of the nonzero tower is not shown to be purely local by representation theory alone.",
    },
    {
        "candidate_verdict": "nonzero_finite_or_scheme_residual",
        "status": "blocking_risk",
        "reason": "Unless a later analytic determinant calculation proves locality/cancellation, standard FP has a nonzero scalar P02 leakage channel.",
    },
]

rank_flow = {
    "desired_coexact_rank": P02_RANK,
    "standard_FP_scalar_half_power": -0.5,
    "if_full_P02_scalar_channel_survives_effective_rank": P02_RANK / 2,
    "if_only_traceless_rank9_survives_effective_rank": P02_RANK - P02_TRACELESS_RANK / 2,
    "if_only_trace_rank1_survives_effective_rank": P02_RANK - P02_TRACE_RANK / 2,
}

results = {
    "status": "zero_by_symmetry_fails_for_nonzero_scalar_tower",
    "P02_decomposition": {
        "total_rank": P02_RANK,
        "trace_rank": P02_TRACE_RANK,
        "traceless_rank": P02_TRACELESS_RANK,
    },
    "scalar_shells_checked": shells,
    "first_nonzero_scalar_shell": first_nonzero,
    "variation_terms": variation_terms,
    "outcomes": outcomes,
    "rank_flow": rank_flow,
    "verdict": (
        "The nonzero scalar residual tower cannot be dismissed by a symmetry selection rule. On RP3 the scalar tower contains even ell shells; "
        "the first nonzero shell ell=2 has multiplicity 9 and an ell=2/P02 first-strain insertion is selection-rule allowed. "
        "Thus delta_h Delta0 has a nonzero P02 leakage channel on the nonzero scalar tower unless a stronger analytic result proves cancellation, locality, "
        "or physical-quotient removal. C6 is therefore not closed in standard covariant FP by symmetry alone."
    ),
}

Path("s2t_c6_scalar_variation_p02_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "first_nonzero_shell": first_nonzero,
    "zero_by_symmetry": "failed",
    "standard_FP_route": "blocked_without_cancellation_or_locality_proof",
}, indent=2, ensure_ascii=False))