#!/usr/bin/env python3
"""Exact admission and non-uniqueness audit for a nonlocal six-point kernel."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_nonlocal_six_point_kernel_admission_gate_results.json"
PREVIOUS = ROOT / "s2t/results/s2t_v8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate_results.json"


def main() -> None:
    previous = json.loads(PREVIOUS.read_text(encoding="utf-8"))
    assert previous["verdict"]["derivative_branch_status"] == "STOP"
    assert previous["comparison"]["static_W3_nonzero"] is True

    z, t = sp.symbols("z t", real=True, nonnegative=True)
    f_one = sp.cancel(1 / (z + 1))
    f_two = sp.cancel(sp.Rational(1, 2) / (z + 1) + 2 / (z + 4))
    difference = sp.factor(f_two - f_one)
    family = sp.factor((1 - t) * f_one + t * f_two)

    assert f_one.subs(z, 0) == 1
    assert f_two.subs(z, 0) == 1
    assert f_one.subs(z, 1) == sp.Rational(1, 2)
    assert f_two.subs(z, 1) == sp.Rational(13, 20)
    expected_difference = 3 * z / (2 * (z + 1) * (z + 4))
    assert sp.cancel(difference - expected_difference) == 0
    assert sp.diff(f_one, z).subs(z, 0) == -1
    assert sp.diff(f_two, z).subs(z, 0) == -sp.Rational(5, 8)
    assert family.subs(z, 0) == 1
    assert sp.factor(family.subs(t, 0) - f_one) == 0
    assert sp.factor(family.subs(t, 1) - f_two) == 0

    # Positive Stieltjes/Yukawa decompositions.  Residues are coupling
    # squares, masses are pole locations in the Euclidean variable z=k^2.
    one_pole_data = ((sp.Integer(1), sp.Integer(1)),)
    two_pole_data = (
        (sp.Rational(1, 2), sp.Integer(1)),
        (sp.Integer(2), sp.Integer(4)),
    )
    reconstructed_one = sum(residue / (z + mass_sq) for residue, mass_sq in one_pole_data)
    reconstructed_two = sum(residue / (z + mass_sq) for residue, mass_sq in two_pole_data)
    assert sp.cancel(reconstructed_one - f_one) == 0
    assert sp.cancel(reconstructed_two - f_two) == 0
    assert all(residue > 0 and mass_sq > 0 for residue, mass_sq in one_pole_data + two_pole_data)

    denominator_one = sp.denom(sp.cancel(f_one))
    denominator_two = sp.denom(sp.cancel(f_two))
    assert sp.degree(denominator_one, z) == 1
    assert sp.degree(denominator_two, z) == 2
    assert sp.expand(denominator_two - 2 * (z + 1) * (z + 4)) == 0

    exact_objects = [
        f_one,
        f_two,
        difference,
        family,
        denominator_one,
        denominator_two,
        *[item for pair in one_pole_data + two_pole_data for item in pair],
    ]
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    previous_hash = hashlib.sha256(PREVIOUS.read_bytes()).hexdigest()
    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_nonlocal_six_point_kernel_admission_gate",
        "field": "Q(z,t)",
        "input_certificate": {
            "path": str(PREVIOUS.relative_to(ROOT)),
            "sha256": previous_hash,
            "static_W3_nonzero": True,
            "local_derivative_branch": "STOP",
        },
        "form_factors": {
            "one_pole": str(f_one),
            "two_pole": str(f_two),
            "common_static_value": "1",
            "one_pole_at_z_1": "1/2",
            "two_pole_at_z_1": "13/20",
            "difference": str(difference),
            "slope_at_zero": {"one_pole": "-1", "two_pole": "-5/8"},
            "convex_family": str(family),
        },
        "positive_spectral_data": {
            "one_pole_residue_mass_squared": [["1", "1"]],
            "two_pole_residue_mass_squared": [["1/2", "1"], ["2", "4"]],
            "all_residues_positive": True,
            "all_mass_squares_positive": True,
        },
        "locality_test": {
            "one_pole_denominator_degree": 1,
            "two_pole_denominator_degree": 2,
            "finite_order_local_polynomial_symbol": False,
            "interpretation": "inverse kinetic form factors are nonlocal effective kernels",
        },
        "inherited_operator_properties": {
            "self_adjoint": True,
            "gauge_invariant": True,
            "permutation_invariant": True,
            "connected_partial_traces_zero": True,
            "reason": "real scalar form factor multiplies the previously certified W3",
        },
        "verdict": {
            "nonlocal_six_point_kernel_class_admitted": True,
            "static_nonzero_W3_projection_admitted": True,
            "kernel_shape_unique_from_current_constraints": False,
            "spectral_masses_and_residues_derived_from_current_parent": False,
            "physical_baryon_bound_state_derived": False,
        },
        "next_gate": "version8_baryon_nonlocal_kernel_spectral_measure_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()