#!/usr/bin/env python3
"""Exact audit of inherited dimensional-transmutation inputs."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_dimensional_transmutation_input_origin_gate_results.json"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def main() -> None:
    finite = load("s2t/results/s2t_v3_product_heat_kernel_kappa_results.json")
    gauge = load("s2t/results/s2t_v3_a4_gauge_coupling_results.json")
    rg = load("s2t/results/s2t_v3_rg_anomaly_scale_setting_results.json")
    previous = load("s2t/results/s2t_v8_baryon_base_scale_selector_architecture_gate_results.json")

    assert finite["finite_supertrace"]["numerator"] == 40
    assert finite["finite_supertrace"]["B0"] == "5/(8*pi**2)"
    assert gauge["mass_and_supertrace"]["completed_zero_mode_numerator"] == "67"
    assert gauge["mass_and_supertrace"]["B_zero"] == "67/(64*pi**2)"
    assert rg["charge_ledger"]["one_loop_b"] == "2"
    assert previous["next_gate"] == "version8_baryon_dimensional_transmutation_input_origin_gate"

    c_sigma, delta_kk, s, mu, lam = sp.symbols(
        "c_sigma delta_kk s mu Lambda", real=True
    )
    numerator = 67 + c_sigma**2 + delta_kk
    positive_witness = numerator.subs({c_sigma: 0, delta_kk: 0})
    negative_witness = numerator.subs({c_sigma: 0, delta_kk: -68})
    assert positive_witness == 67
    assert negative_witness == -1

    b = sp.Rational(2, 3) * 2 + sp.Rational(1, 3) * 2
    landau_log_ratio = sp.simplify(8 * sp.pi**2 / (b * sp.Rational(3, 8)))
    assert b == 2
    assert landau_log_ratio == sp.Rational(32, 3) * sp.pi**2
    assert sp.simplify((s * lam) / (s * mu) - lam / mu) == 0

    requirements = {
        "full_B_computed_and_positive": False,
        "absolute_DT_scale_selected": False,
        "internal_c0_map_derived": False,
    }
    assert sum(requirements.values()) == 0
    exact_objects = [numerator, positive_witness, negative_witness, b, landau_log_ratio]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_dimensional_transmutation_input_origin_gate",
        "inherited_exact_blocks": {
            "finite_numerator": 40,
            "B_finite": "5/(8*pi**2)",
            "gauge_BV_numerator": 27,
            "zero_mode_numerator": 67,
            "B_zero": "67/(64*pi**2)",
            "B_zero_positive": True,
            "one_loop_b": 2,
            "landau_log_ratio": "32*pi**2/3",
        },
        "full_B_boundary": {
            "numerator": "67+c_sigma**2+delta_kk",
            "positive_unspecified_completion_witness": 67,
            "negative_unspecified_completion_witness": -1,
            "sign_fixed_without_full_lift": False,
        },
        "rg_boundary": {
            "spectral_matching_g_squared": "3/8",
            "dimensionless_ratio_fixed": True,
            "scale_orbit": "(mu,Lambda_DT)->(s*mu,s*Lambda_DT)",
            "absolute_scale_fixed": False,
        },
        "c0_boundary": {
            "typed_hidden_to_baryon_map_found": False,
            "moment_map_level_may_be_renamed_c0": False,
        },
        "full_input_requirements": requirements,
        "completed_full_inputs": 0,
        "total_full_inputs": 3,
        "verdict": {
            "early_level_work_reused": True,
            "two_dimensionless_subblocks_closed": True,
            "dimensional_transmutation_selector_closed": False,
        },
        "next_gate": "version8_baryon_c0_typed_internal_map_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()