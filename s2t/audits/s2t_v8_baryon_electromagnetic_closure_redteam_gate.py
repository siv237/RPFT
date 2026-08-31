#!/usr/bin/env python3
"""Exact closure audit for the baryon electromagnetic branch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_electromagnetic_closure_redteam_gate_results.json"


def main() -> None:
    a, z = sp.symbols("A_el z", positive=True)
    # z must be allowed to have either sign; replace its positive assumption.
    z = sp.symbols("z", real=True)
    branches = {
        "trivial": -a - z,
        "sign": -a + 3 * z,
        "standard": -a + z,
    }
    sign_conditions = {
        "trivial": "z > -A_el",
        "sign": "z < A_el/3",
        "standard": "z < A_el",
    }
    countermodels = {
        "trivial": {"z": -2 * a, "value": sp.factor(branches["trivial"].subs(z, -2 * a))},
        "sign": {"z": a, "value": sp.factor(branches["sign"].subs(z, a))},
        "standard": {"z": 2 * a, "value": sp.factor(branches["standard"].subs(z, 2 * a))},
    }

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_electromagnetic_closure_redteam_gate",
        "field": "Q(A_el,z), A_el>0",
        "total_three_branch_splitting_times_3T": {
            name: str(value) for name, value in branches.items()
        },
        "negative_sign_conditions": sign_conditions,
        "common_negative_strip": "-A_el < z < A_el/3",
        "positive_countermodels": {
            name: {"z": str(item["z"]), "value": str(item["value"])}
            for name, item in countermodels.items()
        },
        "closed_exactly": {
            "charge_identity": True,
            "charge_pattern": ["4", "1", "0", "1"],
            "conditional_permutation_averaged_electrostatic_sign": True,
            "magnetic_S3_branch_classification": True,
            "coulomb_and_contact_scaling_orbits": True,
        },
        "not_derived": {
            "coordinate_hamiltonian": True,
            "radial_state": True,
            "physical_spin_parent": True,
            "magnetic_coefficient_z": True,
            "permutation_branch": True,
            "absolute_energy_scale": True,
            "physical_mass_difference": True,
        },
        "verdict": {
            "parameter_free_electromagnetic_prediction": False,
            "branch_closed_negative": True,
            "resume_condition": "coordinate_spin_parent",
        },
    }

    assert countermodels["trivial"]["value"] == a
    assert countermodels["sign"]["value"] == 2 * a
    assert countermodels["standard"]["value"] == a
    assert all(sp.factor(value.subs(z, 0)) == -a for value in branches.values())
    assert not any(
        atom.is_Float for value in branches.values() for atom in sp.preorder_traversal(value)
    )

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()