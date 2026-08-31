#!/usr/bin/env python3
"""Exact S3 class-sum audit of spatial ground-state selection."""

from __future__ import annotations

import hashlib
import json
from itertools import permutations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_spatial_ground_state_symmetry_origin_gate_results.json"


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(3))


def parity(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(3)
        for j in range(i + 1, 3)
    )
    return -1 if inversions % 2 else 1


def main() -> None:
    alpha, beta = sp.symbols("alpha beta", real=True)
    group = list(permutations(range(3)))
    index = {element: position for position, element in enumerate(group)}
    regular = {}
    for element in group:
        matrix = sp.zeros(6, 6)
        for column, basis in enumerate(group):
            matrix[index[compose(element, basis)], column] = 1
        regular[element] = matrix

    identity = (0, 1, 2)
    transpositions = [element for element in group if parity(element) == -1]
    three_cycles = [
        element
        for element in group
        if parity(element) == 1 and element != identity
    ]
    t2 = sum((regular[element] for element in transpositions), sp.zeros(6, 6))
    t3 = sum((regular[element] for element in three_cycles), sp.zeros(6, 6))
    hamiltonian = alpha * t2 + beta * t3

    commutes = all(
        sp.simplify(hamiltonian * matrix - matrix * hamiltonian) == sp.zeros(6, 6)
        for matrix in regular.values()
    )
    symbolic_eigenvalues = {
        "trivial": 3 * alpha + 2 * beta,
        "sign": -3 * alpha + 2 * beta,
        "standard": -beta,
    }
    characteristic_expected = sp.factor(
        (sp.Symbol("z") - symbolic_eigenvalues["trivial"])
        * (sp.Symbol("z") - symbolic_eigenvalues["sign"])
        * (sp.Symbol("z") - symbolic_eigenvalues["standard"]) ** 4
    )
    characteristic_actual = sp.factor(hamiltonian.charpoly(sp.Symbol("z")).as_expr())

    examples = {
        "symmetric_ground": {"alpha": -1, "beta": 0, "ground_type": "trivial"},
        "sign_ground": {"alpha": 1, "beta": 0, "ground_type": "sign"},
        "standard_ground": {"alpha": 0, "beta": 1, "ground_type": "standard"},
    }
    for item in examples.values():
        levels = {
            name: sp.factor(value.subs({alpha: item["alpha"], beta: item["beta"]}))
            for name, value in symbolic_eigenvalues.items()
        }
        minimum = min(levels.values())
        item["levels"] = {name: str(value) for name, value in levels.items()}
        item["ground_verified"] = levels[item["ground_type"]] == minimum

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_spatial_ground_state_symmetry_origin_gate",
        "field": "Q(alpha,beta), no Float inputs",
        "regular_representation": {
            "dimension": 6,
            "transposition_class_size": len(transpositions),
            "three_cycle_class_size": len(three_cycles),
            "central_hamiltonian_commutes_with_S3": commutes,
            "levels": {name: str(value) for name, value in symbolic_eigenvalues.items()},
            "characteristic_polynomial_exact": (
                sp.expand(characteristic_actual - characteristic_expected) == 0
            ),
        },
        "ground_branch_countermodels": examples,
        "sufficient_condition": {
            "positivity_improving_semigroup": True,
            "implies_unique_positive_ground_state": True,
            "permutation_invariance_then_implies_trivial_type": True,
            "condition_verified_for_project_spatial_parent": False,
        },
        "project_boundary": {
            "three_coordinate_spatial_hamiltonian_present": False,
            "permutation_invariance_alone_selects_ground_type": False,
            "symmetric_spin_aroma_branch_unconditional": False,
        },
        "verdict": {
            "reject_symmetry_alone_as_ground_state_selector": True,
            "accept_positivity_improving_condition_as_sufficient": True,
            "next_gate": "version8_baryon_electromagnetic_closure_redteam_gate",
        },
    }

    assert commutes
    assert sp.expand(characteristic_actual - characteristic_expected) == 0
    assert all(bool(item["ground_verified"]) for item in examples.values())
    assert not any(
        atom.is_Float
        for entry in hamiltonian
        for atom in sp.preorder_traversal(entry)
    )

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()