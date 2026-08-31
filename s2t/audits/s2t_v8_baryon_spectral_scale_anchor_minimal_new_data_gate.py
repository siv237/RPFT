#!/usr/bin/env python3
"""Exact minimal-data audit for anchoring a baryon spectral kernel."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_spectral_scale_anchor_minimal_new_data_gate_results.json"
PREVIOUS = ROOT / "s2t/results/s2t_v8_baryon_spectral_scale_anchor_candidate_audit_gate_results.json"

def main() -> None:
    previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    assert previous["passing_candidates"] == 0
    z, a, c, lam = sp.symbols("z a c lambda_3", positive=True)
    mass_sq = c * a
    shape = sp.cancel(mass_sq / (z + mass_sq))
    kernel_scalar = sp.cancel(lam * shape)
    assert shape.subs(z, 0) == 1
    assert kernel_scalar.subs(z, 0) == lam
    assert sp.diff(shape, z).subs(z, 0) == -1 / (a * c)
    assert shape.subs({z: a, c: 1}) == sp.Rational(1, 2)
    assert shape.subs({z: a, c: 2}) == sp.Rational(2, 3)
    assert shape.subs({z: 1, a: 1, c: 1}) == sp.Rational(1, 2)
    assert shape.subs({z: 1, a: 2, c: 1}) == sp.Rational(2, 3)
    normalized = sp.cancel(kernel_scalar / kernel_scalar.subs(z, 0))
    assert sp.cancel(normalized - shape) == 0
    exact = [mass_sq, shape, kernel_scalar, normalized]
    assert not any(atom.is_Float for obj in exact for atom in sp.preorder_traversal(obj))
    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_spectral_scale_anchor_minimal_new_data_gate",
        "field": "Q(z,a,c,lambda_3)",
        "input_sha256": hashlib.sha256(PREVIOUS.read_bytes()).hexdigest(),
        "kernel": {"mass_sq": "c*a", "shape": str(shape), "scalar": str(kernel_scalar), "static_value": "lambda_3", "slope": "-1/(a*c)"},
        "independence_witnesses": {
            "fixed_a_c_1_at_z_a": "1/2", "fixed_a_c_2_at_z_a": "2/3",
            "fixed_c_a_1_at_z_1": "1/2", "fixed_c_a_2_at_z_1": "2/3",
            "lambda_changes_amplitude_not_normalized_shape": True,
        },
        "minimal_new_data": {
            "shape": ["selected positive base scale a", "selected dimensionless typed map coefficient c"],
            "full_kernel_additionally_requires": "lambda_3",
            "independent_data_count_shape": 2,
            "independent_data_count_full_kernel": 3,
        },
        "verdict": {"minimal_contract_derived": True, "anchor_realized_by_current_parent": False, "physical_kernel_derived": False},
        "next_gate": "version8_baryon_base_scale_selector_architecture_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())

if __name__ == "__main__": main()