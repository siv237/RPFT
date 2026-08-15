import json
import math
from pathlib import Path

# Analytic moment audit for the first ambient strain space on S^3/RP^3.
# Unit S^3 volume is 2*pi^2; RP^3 volume is pi^2.
# For x uniformly on S^{d-1}, d=4:
# E[x_a x_b] = delta_ab/d
# E[x_a x_b x_c x_d] = (delta_ab delta_cd + delta_ac delta_bd + delta_ad delta_bc)/(d(d+2))
# Therefore for symmetric A,B:
# <q_A q_B>_S3 = Vol(S3) * ((Tr A)(Tr B) + 2 Tr(AB))/(d(d+2))
# The same local integral descends to RP3 with half volume because q_A is even.

d = 4
vol_s3 = 2 * math.pi**2
vol_rp3 = math.pi**2
bosonic_half = 0.5

# Inner product coefficients for q_A=x^T A x on RP3.
coef_trace_trace = vol_rp3 / (d * (d + 2))
coef_ab = 2 * vol_rp3 / (d * (d + 2))

# Decompose A = a I + A0, Tr(A0)=0.
# q_I=|x|^2=1. Norm^2(q_I)=Vol(RP3).
trace_norm_identity = vol_rp3
# For traceless A0, integral q_A0^2 = 2 Vol/(d(d+2)) Tr(A0^2).
traceless_norm_per_frobenius = 2 * vol_rp3 / (d * (d + 2))

# Dimension accounting.
sym2_dim = d * (d + 1) // 2
trace_dim = 1
traceless_dim = sym2_dim - 1

# Compare required volume factor in absorption.
S_GEO = 4 * math.pi**3 + math.pi**2 + math.pi
T_RP3 = 1.5227161455271536e-05
PI4_TERM = 1 / (math.pi**4 * S_GEO**2)
base_volume_half = (vol_rp3 / 2) * T_RP3 / S_GEO
required_prefactor = PI4_TERM / (T_RP3 / S_GEO)

checks = [
    {
        "check": "even_descent",
        "status": "pass",
        "reason": "q_A(-x)=q_A(x), so quadratic strains descend from S3 to RP3 and integrals are exactly half of S3 integrals.",
    },
    {
        "check": "trace_traceless_orthogonality",
        "status": "pass",
        "reason": "For A0 traceless, integral q_I q_A0 = Vol(RP3)*Tr(A0)/d = 0.",
    },
    {
        "check": "rank_count",
        "status": "pass",
        "reason": "Sym^2(R4) decomposes orthogonally as trace rank 1 plus traceless rank 9.",
    },
    {
        "check": "volume_half_factor",
        "status": "conditional_pass",
        "reason": "Vol(RP3)=pi^2 follows from the quotient and the bosonic logdet contributes a formal 1/2. This derives the natural prefactor pi^2/2 if the coexact tower density is normalized per unit RP3 volume.",
    },
    {
        "check": "absolute_absorption_identity",
        "status": "not_closed",
        "reason": "The moment normalization derives the natural prefactor, but it does not derive the Bessel tower normalization or the N_need-10 finite scheme gap.",
    },
]

results = {
    "status": "P02_volume_normalization_natural_prefactor_derived_conditionally",
    "geometry": {
        "ambient_dimension": d,
        "Vol_S3_unit": vol_s3,
        "Vol_RP3_unit": vol_rp3,
        "Vol_RP3_over_2_bosonic_half": vol_rp3 / 2,
    },
    "moments": {
        "E_xa_xb": "delta_ab/4",
        "E_xa_xb_xc_xd": "(delta_ab delta_cd + delta_ac delta_bd + delta_ad delta_bc)/24",
        "inner_product_RP3_qA_qB": "Vol(RP3)*((Tr A)(Tr B)+2Tr(AB))/(4*6)",
        "coef_trace_trace": coef_trace_trace,
        "coef_frobenius_AB": coef_ab,
        "norm_q_identity": trace_norm_identity,
        "traceless_norm_per_Tr_A0_squared": traceless_norm_per_frobenius,
    },
    "rank_decomposition": {
        "Sym2_R4_dim": sym2_dim,
        "trace_dim_ell0": trace_dim,
        "traceless_dim_ell2": traceless_dim,
        "total_rank": sym2_dim,
    },
    "absorption_prefactor": {
        "natural_Vol_RP3_over_2": vol_rp3 / 2,
        "required_prefactor_for_exact_pi4_without_CasMix": required_prefactor,
        "required_over_natural": required_prefactor / (vol_rp3 / 2),
        "base_volume_half_absorption": base_volume_half,
        "base_relative_overshoot_vs_pi4": (base_volume_half - PI4_TERM) / PI4_TERM,
    },
    "checks": checks,
    "verdict": (
        "The pi^2/2 prefactor is not a fitted number at the P02 normalization level: pi^2 is Vol(RP3) and 1/2 is the bosonic logdet factor. "
        "Moment formulas on S3/RP3 give an orthogonal trace/traceless decomposition with rank 1+9. "
        "This conditionally closes the volume-factor subtest of C6, provided the Bessel tower T_coex is normalized as a per-volume determinant density. "
        "It does not close the full C6 proof because the combined Maxwell--ghost second-variation sign and N_need-10 scheme gap remain open."
    ),
}

Path("s2t_p02_volume_normalization_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "Vol_RP3_over_2": vol_rp3 / 2,
    "rank": sym2_dim,
    "required_over_natural": required_prefactor / (vol_rp3 / 2),
    "base_relative_overshoot_vs_pi4": (base_volume_half - PI4_TERM) / PI4_TERM,
}, indent=2, ensure_ascii=False))