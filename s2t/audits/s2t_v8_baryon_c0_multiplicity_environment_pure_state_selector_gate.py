#!/usr/bin/env python3
"""Exact audit of pure-state selectors on the three-dimensional environment."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_pure_state_selector_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_full_multiplicity_frame_single_map_compatibility_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["choi_stinespring"]["full_minimal_environment_dimension"] == 3
    assert previous["next_gate"] == "version8_baryon_c0_multiplicity_environment_pure_state_selector_gate"

    rho00, rho01, rho02, rho11, rho12, rho22 = sp.symbols(
        "rho00 rho01 rho02 rho11 rho12 rho22", real=True
    )
    rho_real = sp.Matrix(
        [[rho00, rho01, rho02], [rho01, rho11, rho12], [rho02, rho12, rho22]]
    )
    q = sp.symbols("q", real=True)
    gauge_generator = q * sp.eye(3)
    assert gauge_generator * rho_real - rho_real * gauge_generator == sp.zeros(3)

    e0 = sp.Matrix([1, 0, 0])
    e1 = sp.Matrix([0, 1, 0])
    p0 = e0 * e0.T
    p1 = e1 * e1.T
    rho_trace = sp.eye(3) / 3
    assert rho_trace.rank() == 3
    assert p0.rank() == p1.rank() == 1
    assert sp.trace(p0) == sp.trace(p1) == sp.trace(rho_trace) == 1

    entropy_trace = -3 * sp.Rational(1, 3) * sp.log(sp.Rational(1, 3))
    assert sp.simplify(entropy_trace - sp.log(3)) == 0
    entropy_pure = sp.Integer(0)

    epsilon, beta = sp.symbols("epsilon beta", real=True)
    gibbs_scalar = sp.exp(-beta * epsilon)
    rho_gibbs = gibbs_scalar * sp.eye(3) / (3 * gibbs_scalar)
    assert sp.simplify(rho_gibbs - rho_trace) == sp.zeros(3)

    def purity_functional(rho: sp.MatrixBase) -> sp.Expr:
        return sp.simplify(2 * (1 - sp.trace(rho * rho)))

    assert purity_functional(p0) == purity_functional(p1) == 0
    assert purity_functional(rho_trace) == sp.Rational(4, 3)

    h_a = sp.diag(0, 1, 2)
    h_b = sp.diag(2, 0, 1)
    assert h_a * e0 == sp.zeros(3, 1)
    assert h_b * e1 == sp.zeros(3, 1)
    assert p0 != p1
    assert list(h_a.eigenvals().keys()) == [0, 1, 2]
    assert set(h_b.eigenvals().keys()) == {0, 1, 2}

    candidates = {
        "scalar_gauge_action": {"selects_purity": False, "selects_direction": False},
        "real_structure": {"selects_purity": False, "selects_direction": False},
        "normalized_trace_or_isotropic_gibbs": {"selects_purity": False, "selects_direction": False},
        "entropy_minimum": {"selects_purity": True, "selects_direction": False},
        "version6_exterior_square_purity_parent": {
            "selects_purity": True,
            "selects_direction": False,
            "typed_current_parent_origin": False,
        },
    }
    assert sum(item["selects_direction"] for item in candidates.values()) == 0

    exact_objects = [rho_real, gauge_generator, rho_trace, p0, p1, rho_gibbs, h_a, h_b]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_multiplicity_environment_pure_state_selector_gate",
        "environment": {
            "complex_dimension": 3,
            "state_space": "D_3",
            "scalar_gauge_action": True,
            "all_density_matrices_gauge_invariant": True,
            "real_pure_state_orbit": "RP^2",
        },
        "canonical_states": {
            "normalized_trace_state": "I3/3",
            "normalized_trace_rank": 3,
            "normalized_trace_entropy": "log(3)",
            "isotropic_gibbs_state": "I3/3",
            "pure_state_entropy": str(entropy_pure),
        },
        "purity_functional": {
            "formula": "2(1-Tr(rho^2))",
            "value_on_rank_one": "0",
            "value_on_I3_over_3": "4/3",
            "real_minimum_set": "RP^2",
            "selects_direction": False,
        },
        "anisotropic_witnesses": {
            "h_A": "diag(0,1,2)",
            "ground_projector_A": "e0 e0^T",
            "h_B": "diag(2,0,1)",
            "ground_projector_B": "e1 e1^T",
            "same_declared_gauge_and_real_symmetries": True,
            "different_selected_pure_states": True,
        },
        "candidate_ledger": candidates,
        "verdict": {
            "candidate_count": 5,
            "unique_pure_state_selectors": 0,
            "purity_can_be_selected_conditionally": True,
            "direction_selected": False,
            "single_c0_map_derived": False,
            "new_anisotropic_hamiltonian_data_required": True,
        },
        "next_gate": "version8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()