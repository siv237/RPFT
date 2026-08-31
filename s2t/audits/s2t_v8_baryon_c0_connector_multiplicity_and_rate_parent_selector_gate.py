#!/usr/bin/env python3
"""Exact parent-selector audit for connector multiplicity and rate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_connector_multiplicity_and_rate_parent_selector_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_old_new_gauge_covariant_connector_classification_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["classification"]["complex_solution_dimension"] == 3
    assert previous["next_gate"] == "version8_baryon_c0_connector_multiplicity_and_rate_parent_selector_gate"
    assert not previous["selector_boundary"]["connector_direction_selected"]
    assert not previous["selector_boundary"]["positive_rate_selected"]

    basis = []
    for row, column in ((8, 0), (17, 1), (18, 1)):
        item = sp.zeros(21, 2)
        item[row, column] = 1
        basis.append(sp.ImmutableMatrix(item))
    trace_metric = sp.Matrix(
        [[sp.trace(left.H * right) for right in basis] for left in basis]
    )
    assert trace_metric == sp.eye(3)

    z0, z1, z2 = sp.symbols("z0 z1 z2", real=True)
    a = sp.symbols("a", real=True)
    b = sp.symbols("b", positive=True)
    z = sp.Matrix([z0, z1, z2])
    radius2 = (z.T * z)[0]
    potential = a * radius2 / 2 + b * radius2**2 / 4
    gradient = sp.Matrix([sp.diff(potential, variable) for variable in z])
    hessian = sp.hessian(potential, z)
    assert all(
        sp.simplify(left - right) == 0
        for left, right in zip(gradient, (a + b * radius2) * z)
    )

    r = sp.symbols("r", positive=True)
    vacuum_hessian = sp.simplify(hessian.subs({z0: r, z1: 0, z2: 0, a: -b * r**2}))
    assert vacuum_hessian == sp.diag(2 * b * r**2, 0, 0)
    assert vacuum_hessian.rank() == 1
    assert len(vacuum_hessian.nullspace()) == 2

    zero_extended_old_parent_hessian = sp.zeros(3)
    assert zero_extended_old_parent_hessian.rank() == 0

    mass2, temperature = sp.symbols("m2 T", positive=True)
    gaussian_covariance = sp.simplify(temperature * (mass2 * sp.eye(3)).inv())
    assert gaussian_covariance == temperature / mass2 * sp.eye(3)

    selector_a = sp.diag(-1, 1, 2)
    selector_b = sp.diag(2, -1, 1)
    assert selector_a.eigenvects()[0][0] == -1
    assert selector_b.eigenvects()[0][0] == -1
    assert selector_a * sp.eye(3)[:, 0] == -sp.eye(3)[:, 0]
    assert selector_b * sp.eye(3)[:, 1] == -sp.eye(3)[:, 1]

    gamma, scale = sp.symbols("gamma s", positive=True)
    assert sp.simplify((gamma / scale**2) * scale**2 - gamma) == 0

    rotations = (
        sp.eye(3),
        sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]]),
        sp.Matrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]]),
    )
    assert all((rotation * z).dot(rotation * z) == radius2 for rotation in rotations)

    exact_objects = [*trace_metric, potential, *gradient, *vacuum_hessian, *gaussian_covariance]
    assert not any(atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_connector_multiplicity_and_rate_parent_selector_gate",
        "multiplicity_geometry": {
            "real_dimension": 3,
            "common_trace_metric": "I3",
            "real_projective_direction_space": "RP^2",
            "current_parent_extended_hessian": "0_3",
        },
        "isotropic_parent": {
            "potential": "a||z||^2/2+b||z||^4/4",
            "broken_phase_condition": "a<0,b>0",
            "vacuum_radius_squared": "-a/b",
            "vacuum_moduli": "RP^2",
            "vacuum_hessian_rank": 1,
            "angular_zero_modes": 2,
            "connector_direction_selected": False,
        },
        "anisotropic_witness": {
            "allowed_by_endpoint_labels": True,
            "selector_A": "diag(-1,1,2)",
            "selector_B": "diag(2,-1,1)",
            "selected_branches_differ": True,
            "anisotropic_weights_derived": False,
        },
        "rate": {
            "gaussian_covariance": "(T/m^2) I3",
            "frame_rate_orbit": "V->sV, gamma->gamma/s^2",
            "trace_normalization_removes_frame_scale": True,
            "environment_intensity_selected": False,
            "absolute_gamma_selected": False,
        },
        "selector_ledger": {
            "required": 2,
            "derived": 0,
            "direction_RP2": False,
            "positive_rate_gamma": False,
        },
        "verdict": {
            "common_trace_selects_only_radial_norm": True,
            "current_parent_selects_connector": False,
            "current_parent_selects_rate": False,
            "new_bimodule_weights_and_environment_scale_required": True,
        },
        "next_gate": "version8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()