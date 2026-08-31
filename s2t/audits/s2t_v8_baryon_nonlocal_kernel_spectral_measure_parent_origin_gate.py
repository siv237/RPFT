#!/usr/bin/env python3
"""Exact Schur and scale-orbit audit for a nonlocal baryon kernel parent."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate_results.json"
NONLOCAL_INPUT = ROOT / "s2t/results/s2t_v8_baryon_nonlocal_six_point_kernel_admission_gate_results.json"
BASE_SCALE_INPUT = ROOT / "s2t/results/s2t_v8_full_field_a4_dirac_lift_origin_gate_results.json"


def main() -> None:
    nonlocal_input = json.loads(NONLOCAL_INPUT.read_text(encoding="utf-8"))
    base_scale_input = json.loads(BASE_SCALE_INPUT.read_text(encoding="utf-8"))
    assert nonlocal_input["verdict"]["nonlocal_six_point_kernel_class_admitted"] is True
    assert nonlocal_input["verdict"]["kernel_shape_unique_from_current_constraints"] is False
    assert base_scale_input["verdict"]["external_metric_scale_selected"] is False

    z, q, mass_sq, coupling_sq, lambda_3, source = sp.symbols(
        "z q mass_sq coupling_sq lambda_3 source", positive=True
    )
    auxiliary = sp.symbols("auxiliary", real=True)

    action = sp.expand(
        sp.Rational(1, 2) * (z + mass_sq) * auxiliary**2
        - sp.sqrt(coupling_sq) * auxiliary * source
    )
    stationary_auxiliary = sp.sqrt(coupling_sq) * source / (z + mass_sq)
    effective = sp.factor(action.subs(auxiliary, stationary_auxiliary))
    expected_effective = -coupling_sq * source**2 / (2 * (z + mass_sq))
    assert sp.cancel(effective - expected_effective) == 0

    matched_coupling_sq = lambda_3 * mass_sq
    normalized_form = mass_sq / (z + mass_sq)
    scaled_mass_sq = q * mass_sq
    scaled_coupling_sq = q * matched_coupling_sq
    scaled_form = scaled_mass_sq / (z + scaled_mass_sq)

    assert sp.cancel(matched_coupling_sq / mass_sq - lambda_3) == 0
    assert sp.cancel(scaled_coupling_sq / scaled_mass_sq - lambda_3) == 0
    assert normalized_form.subs(z, 0) == 1
    assert scaled_form.subs(z, 0) == 1
    assert sp.diff(scaled_form, z).subs(z, 0) == -1 / (q * mass_sq)
    assert normalized_form.subs(z, mass_sq) == sp.Rational(1, 2)
    assert scaled_form.subs({z: mass_sq, q: 2}) == sp.Rational(2, 3)
    assert sp.cancel(scaled_form.subs(q, 1) - normalized_form) == 0
    assert sp.cancel(scaled_form.subs(q, 2) - normalized_form) != 0

    exact_objects = [
        action,
        stationary_auxiliary,
        effective,
        matched_coupling_sq,
        normalized_form,
        scaled_mass_sq,
        scaled_coupling_sq,
        scaled_form,
    ]
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate",
        "field": "Q(z,q,mass_sq,lambda_3) with algebraic sqrt(coupling_sq)",
        "input_certificates": {
            "nonlocal_admission": {
                "path": str(NONLOCAL_INPUT.relative_to(ROOT)),
                "sha256": hashlib.sha256(NONLOCAL_INPUT.read_bytes()).hexdigest(),
            },
            "base_scale_no_go": {
                "path": str(BASE_SCALE_INPUT.relative_to(ROOT)),
                "sha256": hashlib.sha256(BASE_SCALE_INPUT.read_bytes()).hexdigest(),
            },
        },
        "single_auxiliary_parent": {
            "action": "(z+mass_sq)*auxiliary^2/2-sqrt(coupling_sq)*auxiliary*source",
            "stationary_auxiliary": str(stationary_auxiliary),
            "effective_schur_term": str(effective),
            "positive_auxiliary_hessian_for_nonnegative_z": True,
        },
        "static_matching": {
            "condition": "coupling_sq=lambda_3*mass_sq",
            "normalized_form_factor": str(normalized_form),
            "static_value": "1",
        },
        "scale_orbit": {
            "transformation": "mass_sq -> q*mass_sq, coupling_sq -> q*coupling_sq",
            "static_coefficient_preserved": True,
            "scaled_form_factor": str(scaled_form),
            "slope_at_zero": "-1/(q*mass_sq)",
            "witness_at_z_equal_mass_sq": {"q=1": "1/2", "q=2": "2/3"},
            "base_dirac_scale_selected_by_finite_parent": False,
        },
        "verdict": {
            "single_auxiliary_parent_realizes_one_pole_kernel": True,
            "static_matching_selects_spectral_mass": False,
            "current_finite_parent_selects_spectral_measure": False,
            "spectral_scale_orbit_dimension_at_least": 1,
            "nonlocal_kernel_parent_origin": "NO-GO without an independent base-scale selector",
        },
        "next_gate": "version8_baryon_spectral_scale_anchor_candidate_audit_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()