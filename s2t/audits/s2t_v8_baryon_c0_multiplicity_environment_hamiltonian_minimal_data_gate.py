#!/usr/bin/env python3
"""Exact minimal-data audit for a Hamiltonian pure-state selector."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_pure_state_selector_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["unique_pure_state_selectors"] == 0
    assert previous["next_gate"] == "version8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate"

    h00, h01, h02, h11, h12, h22 = sp.symbols(
        "h00 h01 h02 h11 h12 h22", real=True
    )
    h_generic = sp.Matrix(
        [[h00, h01, h02], [h01, h11, h12], [h02, h12, h22]]
    )
    q = sp.symbols("q", real=True)
    assert q * sp.eye(3) * h_generic - h_generic * q * sp.eye(3) == sp.zeros(3)

    z = sp.Matrix([1, 2, 2]) / 3
    projector = sp.simplify(z * z.T)
    complement = sp.eye(3) - projector
    assert sp.simplify(z.dot(z)) == 1
    assert projector.rank() == 1
    assert complement.rank() == 2
    assert sp.simplify(projector * projector - projector) == sp.zeros(3)

    epsilon, delta = sp.symbols("epsilon delta", real=True, positive=True)
    h_axial = epsilon * sp.eye(3) + delta * complement
    assert sp.simplify((h_axial - epsilon * sp.eye(3)) * projector) == sp.zeros(3)
    assert sp.simplify((h_axial - epsilon * sp.eye(3)) * complement - delta * complement) == sp.zeros(3)

    a = sp.symbols("a", positive=True)
    b = sp.symbols("b", real=True)
    h_affine = a * h_axial + b * sp.eye(3)
    assert sp.simplify(h_affine * projector - (a * epsilon + b) * projector) == sp.zeros(3)

    x = sp.symbols("x", positive=True)
    rho = sp.simplify((projector + x * complement) / (1 + 2 * x))
    assert sp.simplify(sp.trace(rho) - 1) == 0
    assert sp.factor(rho.det()) == x**2 / (2 * x + 1) ** 3
    purity = sp.factor(sp.trace(rho * rho))
    assert purity == (2 * x**2 + 1) / (2 * x + 1) ** 2
    assert sp.factor(1 - purity) == 2 * x * (x + 2) / (2 * x + 1) ** 2
    assert sp.simplify(rho.subs(x, 0) - projector) == sp.zeros(3)
    assert sp.simplify(rho.subs(x, 1) - sp.eye(3) / 3) == sp.zeros(3)

    p0 = sp.diag(1, 0, 0)
    rho0 = (p0 + x * (sp.eye(3) - p0)) / (1 + 2 * x)
    trace_distance = sp.simplify(2 * x / (1 + 2 * x))
    assert trace_distance.subs(x, 0) == 0
    assert sp.simplify(rho0[1, 1] + rho0[2, 2] - trace_distance) == 0

    exact_objects = [h_generic, projector, complement, h_axial, h_affine, rho, purity, trace_distance]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate",
        "admissible_hamiltonians": {
            "class": "Sym_3(R)",
            "real_dimension": 6,
            "gauge_constraint_reduces_class": False,
        },
        "minimal_axial_representative": {
            "formula": "epsilon I3 + Delta(I3-P)",
            "projector_rank": 1,
            "complement_rank": 2,
            "spectrum_multiplicities": "1+2",
            "selector_space": "RP^2",
            "positive_affine_energy_transform_preserves_projector": True,
        },
        "finite_temperature_gibbs": {
            "x": "exp(-beta Delta)",
            "state": "(P+x(I3-P))/(1+2x)",
            "determinant": "x^2/(1+2x)^3",
            "rank_for_positive_x": 3,
            "purity": "(1+2x^2)/(1+2x)^2",
            "exactly_pure_for_finite_beta_delta": False,
            "zero_temperature_limit": "P",
            "trace_distance_to_P": "2x/(1+2x)",
        },
        "minimal_data_layers": {
            "direction": "P in RP^2",
            "exact_gibbs_purity": "beta Delta -> infinity or external pure preparation",
            "absolute_energy_time_scale": "Delta_phys>0",
            "derived_layers": 0,
            "required_layers": 3,
        },
        "circularity_witness": {
            "formula": "h=Delta(I3-rho_*)",
            "constructs_hamiltonian_from_desired_projector": True,
            "derives_projector": False,
        },
        "verdict": {
            "minimal_selector_classified": True,
            "finite_temperature_pure_state_no_go": True,
            "current_parent_selects_direction": False,
            "current_parent_supplies_cooling_limit": False,
            "current_parent_supplies_absolute_gap": False,
            "single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()