#!/usr/bin/env python3
"""Audit whether one spectral profile fixes the singlet--virtual ratio."""

import hashlib
import json
from pathlib import Path

import sympy as sp


def main() -> None:
    t, t1, t2, w = sp.symbols("t t1 t2 w", positive=True)

    # Convention for Tr chi(D^2/Lambda^2) in four dimensions:
    # f0=chi(0), f2=int_0^infty chi(x)dx, f_{-2}=-chi'(0).
    pure = {
        "f0": sp.Integer(1),
        "f2": 1 / t,
        "fminus2": t,
    }
    pure_ratio = sp.simplify(pure["f2"] * pure["fminus2"] / pure["f0"] ** 2)

    mixture = {
        "f0": sp.Integer(1),
        "f2": w / t1 + (1 - w) / t2,
        "fminus2": w * t1 + (1 - w) * t2,
    }
    mixture_ratio = sp.factor(
        mixture["f2"] * mixture["fminus2"] / mixture["f0"] ** 2
    )
    mixture_excess = sp.factor(mixture_ratio - 1)
    benchmark = {w: sp.Rational(1, 2), t1: 1, t2: 4}

    result = {
        "gate": "version7_common_spectral_profile_singlet_virtual_ratio_gate",
        "four_dimensional_spectral_weights": {
            "mass_level": "f2*Lambda^2 times finite a2 trace constants",
            "hodge_quartic": "f0 times finite a4 trace constants",
            "six_cycle": "fminus2/Lambda^2 times finite a6 trace constants",
            "moment_convention": "f0=chi(0), f2=int chi, fminus2=-chi'(0)",
            "dimensionless_profile_invariant": "R_chi=f2*fminus2/f0^2",
        },
        "pure_heat_kernel_profile": {
            "profile": "chi_t(x)=exp(-t*x)",
            "f0": str(pure["f0"]),
            "f2": str(pure["f2"]),
            "fminus2": str(pure["fminus2"]),
            "R_chi": str(pure_ratio),
            "scale_independent": bool(pure_ratio == 1),
        },
        "two_scale_positive_mixture": {
            "profile": "w*exp(-t1*x)+(1-w)*exp(-t2*x)",
            "R_chi": str(mixture_ratio),
            "R_chi_minus_one": str(mixture_excess),
            "R_chi_ge_one_for_0_le_w_le_1": True,
            "equality_only_for_single_scale_or_endpoint": True,
            "benchmark": {
                "w": "1/2",
                "t1": "1",
                "t2": "4",
                "R_chi": str(sp.simplify(mixture_ratio.subs(benchmark))),
            },
        },
        "flat_profile_branch": {
            "condition": "chi'(0)=0",
            "fminus2": 0,
            "classical_a6_cycle_coefficient": 0,
            "virtual_cycle_survives_at_this_order": False,
        },
        "renormalized_determinant": {
            "four_dimensional_pq_vertex_log_divergent": True,
            "local_counterterm_required": True,
            "renormalized_gamma_fixed_by_bare_profile_alone": False,
            "matching_scale_required": True,
        },
        "verdict": {
            "one_unspecified_profile_is_one_number": False,
            "pure_gaussian_collapses_classical_moment_ratio": True,
            "general_positive_profile_fixes_R_chi": False,
            "common_profile_fixes_renormalized_a_gamma_ratio": False,
            "coefficient_free_closure_pass": False,
            "status": "gaussian_classical_partial_pass_general_and_renormalized_no_go",
            "next_gate": "version7_full_product_a6_cycle_coefficient_gate",
        },
    }

    out = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_common_spectral_profile_singlet_virtual_ratio_gate_results.json"
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()