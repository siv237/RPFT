import json
import math
from pathlib import Path

S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
P02_TOTAL_RANK = 10
P02_TRACE_RANK = 1
P02_TRACELESS_RANK = 9

# The audit separates two questions that were previously conflated:
# 1. Does the retained constant RP3 scalar KK row (kappa_Cas=1/24) carry P02 leakage?
# 2. If standard FP leaves a nonzero scalar half-determinant, can that nonzero scalar tower carry P02?
#
# For a product metric where the first ambient strain acts only on RP3, a scalar mode constant on RP3 has
# grad_RP3 phi = 0. Hence the first variation of the spatial scalar Laplacian on that row is zero.
# Nonzero S1 momentum m != 0 is unaffected by an RP3 metric strain. The traceless ell=2 part therefore has
# no direct operator insertion on the kappa_Cas row. The trace/volume direction is a normalization/gauge-volume
# issue, not a finite P02 trace-square unless separately derived.

projection_blocks = [
    {
        "block": "constant_RP3_scalar_KK_row",
        "role": "kappa_Cas_1_over_24",
        "rp3_gradient": 0,
        "s1_eigenvalue_depends_on_rp3_metric": False,
        "P02_traceless_rank9_projection": 0,
        "P02_trace_rank1_projection": "volume_normalization_only_open",
        "classification": "safe_for_traceless_P02_not_full_C6_closure",
        "reason": "A scalar constant on RP3 has no RP3 gradient, so first ambient RP3 strain cannot produce an ell=2/traceless scalar operator insertion on the retained kappa_Cas row.",
    },
    {
        "block": "nonzero_scalar_residual_tower_from_standard_FP",
        "role": "minus_half_logdet_Delta0_if_not_cancelled",
        "rp3_gradient": "nonzero",
        "s1_eigenvalue_depends_on_rp3_metric": False,
        "P02_traceless_rank9_projection": "not_excluded",
        "P02_trace_rank1_projection": "not_excluded_or_local_volume",
        "classification": "dangerous_open_block",
        "reason": "Nonconstant scalar eigenmodes have nonzero RP3 gradients. A first ambient strain can couple through the scalar stress tensor, so P02 trace-square leakage is not excluded by the constant-row argument.",
    },
    {
        "block": "physical_transverse_quotient",
        "role": "definition_removes_scalar_tower_before_C6",
        "rp3_gradient": "not_applicable",
        "s1_eigenvalue_depends_on_rp3_metric": "not_applicable",
        "P02_traceless_rank9_projection": 0,
        "P02_trace_rank1_projection": 0,
        "classification": "viable_if_adopted_as_defining_scheme",
        "reason": "If the determinant is defined directly on the coexact quotient, the standard-FP scalar residual is not part of the finite C6 trace.",
    },
]

rank_consequences = [
    {
        "case": "only_kappa_Cas_constant_row_retained",
        "scalar_P02_leak_rank": 0,
        "coexact_effective_rank_remains": 10,
        "status": "does_not_spoil_rank10_for_traceless_P02",
    },
    {
        "case": "standard_FP_nonzero_scalar_half_residual_not_cancelled",
        "scalar_P02_leak_rank": "up_to_P02_rank_with_half_power",
        "coexact_effective_rank_remains": 5,
        "status": "rank10_not_derived",
    },
    {
        "case": "trace_volume_mode_only",
        "scalar_P02_leak_rank": P02_TRACE_RANK,
        "coexact_effective_rank_remains": 9.5,
        "status": "small_but_still_requires_volume_normalization_proof",
    },
]

obligations = [
    {
        "obligation": "constant_branch_isolation",
        "status": "conditional_pass_for_traceless_P02",
        "claim": "The kappa_Cas constant RP3 row has no direct ell=2/traceless P02 operator insertion under RP3-only first ambient strain.",
    },
    {
        "obligation": "trace_volume_direction",
        "status": "open",
        "claim": "The rank-1 trace part must be assigned to volume/gauge normalization or explicitly included.",
    },
    {
        "obligation": "nonzero_scalar_half_residual",
        "status": "open_blocking",
        "claim": "If standard FP leaves -1/2 log det' Delta0 over nonzero scalar modes, P02 leakage is not excluded and rank 10 is not derived.",
    },
]

results = {
    "status": "constant_kappa_branch_safe_but_nonzero_scalar_residual_open",
    "P02_decomposition": {
        "total_rank": P02_TOTAL_RANK,
        "trace_rank": P02_TRACE_RANK,
        "traceless_rank": P02_TRACELESS_RANK,
    },
    "projection_blocks": projection_blocks,
    "rank_consequences": rank_consequences,
    "obligations": obligations,
    "verdict": (
        "The retained kappa_Cas=1/24 row can be isolated from traceless P02 leakage: it is constant on RP3, so an RP3 first-strain "
        "does not act through the scalar Laplacian on that row. This supports the statement that the 1/24 branch is not itself a ghost P02 trace-square. "
        "However, this does not close standard covariant FP, because a nonzero scalar half-determinant remains unless cancelled by zero/gauge/Jacobian factors. "
        "Nonconstant scalar modes can couple to first ambient strain through their gradients, so P02 leakage from the residual nonzero scalar tower remains the blocking gap."
    ),
}

Path("s2t_c6_scalar_p02_projection_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "constant_branch_traceless_P02_projection": 0,
    "trace_direction_status": "open_volume_normalization",
    "nonzero_scalar_residual_status": "open_blocking",
}, indent=2, ensure_ascii=False))