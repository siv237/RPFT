#!/usr/bin/env python3
"""Exact S3 audit for the baryon spin-aroma-space selector."""

from __future__ import annotations

import hashlib
import json
from itertools import permutations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_spin_flavor_permutation_carrier_gate_results.json"


def kron3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def one_site(operator: sp.Matrix, slot: int, identity: sp.Matrix) -> sp.Matrix:
    factors = [identity, identity, identity]
    factors[slot] = operator
    return kron3(*factors)


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(3)
        for right in range(left + 1, 3)
    )
    return -1 if inversions % 2 else 1


def permutation_matrices(local_dimension: int) -> list[tuple[tuple[int, ...], sp.Matrix]]:
    size = local_dimension**3
    result = []
    for permutation in permutations(range(3)):
        matrix = sp.zeros(size, size)
        for first in range(local_dimension):
            for second in range(local_dimension):
                for third in range(local_dimension):
                    old = (first, second, third)
                    new = tuple(old[permutation[index]] for index in range(3))
                    old_index = first * local_dimension**2 + second * local_dimension + third
                    new_index = new[0] * local_dimension**2 + new[1] * local_dimension + new[2]
                    matrix[new_index, old_index] = 1
        result.append((permutation, matrix))
    return result


def expectation_matrix(basis: sp.Matrix, operator: sp.Matrix) -> tuple[sp.Matrix, sp.Matrix]:
    gram = sp.simplify(sp.conjugate(basis).T * basis)
    restricted = sp.simplify(sp.conjugate(basis).T * operator * basis)
    return gram, restricted


def main() -> None:
    character_table = sp.Matrix([[1, 1, 1], [1, -1, 1], [2, 0, -1]])
    class_sizes = sp.diag(1, 3, 2)
    matching = sp.simplify(character_table * class_sizes * character_table.T / 6)

    identity2 = sp.eye(2)
    identity4 = sp.eye(4)
    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.diag(1, -1),
    )
    aroma_generators = [sp.kronecker_product(sigma / 2, identity2) for sigma in pauli]
    spin_generators = [sp.kronecker_product(identity2, sigma / 2) for sigma in pauli]
    total_isospin = [
        sum((one_site(generator, slot, identity4) for slot in range(3)), sp.zeros(64, 64))
        for generator in aroma_generators
    ]
    total_spin = [
        sum((one_site(generator, slot, identity4) for slot in range(3)), sp.zeros(64, 64))
        for generator in spin_generators
    ]
    isospin_square = sum((generator**2 for generator in total_isospin), sp.zeros(64, 64))
    spin_square = sum((generator**2 for generator in total_spin), sp.zeros(64, 64))

    permutation_data = permutation_matrices(4)
    projector_trivial = sum((matrix for _, matrix in permutation_data), sp.zeros(64, 64)) / 6
    projector_sign = sum(
        (permutation_sign(permutation) * matrix for permutation, matrix in permutation_data),
        sp.zeros(64, 64),
    ) / 6
    projector_standard = sp.eye(64) - projector_trivial - projector_sign
    projectors = {
        "trivial": projector_trivial,
        "sign": projector_sign,
        "standard": projector_standard,
    }

    up = sp.Rational(2, 3)
    down = -sp.Rational(1, 3)
    magnetic_form = sp.zeros(64, 64)
    for left, right in ((0, 1), (0, 2), (1, 2)):
        for sigma in pauli:
            charge_spin = sp.kronecker_product(sp.diag(up, down), sigma)
            factors = [identity4, identity4, identity4]
            factors[left] = charge_spin
            factors[right] = charge_spin
            magnetic_form += kron3(*factors)

    branch_values: dict[str, dict[str, str | int | bool]] = {
        name: {} for name in projectors
    }
    joint_dimensions = {}
    for particle, isospin_z in (
        ("proton", sp.Rational(1, 2)),
        ("neutron", -sp.Rational(1, 2)),
    ):
        selected_indices = [
            index
            for index in range(64)
            if total_isospin[2][index, index] == isospin_z
            and total_spin[2][index, index] == sp.Rational(1, 2)
        ]
        weight_basis = sp.eye(64)[:, selected_indices]
        constraints = sp.Matrix.vstack(
            (isospin_square - sp.Rational(3, 4) * sp.eye(64)) * weight_basis,
            (spin_square - sp.Rational(3, 4) * sp.eye(64)) * weight_basis,
        )
        joint_basis = sp.Matrix.hstack(
            *(weight_basis * vector for vector in constraints.nullspace())
        )
        joint_dimensions[particle] = joint_basis.shape[1]

        for name, projector in projectors.items():
            branch_basis = sp.Matrix.hstack(*(projector * joint_basis).columnspace())
            gram, restricted = expectation_matrix(branch_basis, magnetic_form)
            value = sp.factor(restricted[0, 0] / gram[0, 0])
            scalar_exact = sp.simplify(restricted - value * gram) == sp.zeros(
                branch_basis.shape[1], branch_basis.shape[1]
            )
            branch_values[name][f"{particle}_dimension"] = branch_basis.shape[1]
            branch_values[name][f"{particle}_O"] = str(value)
            branch_values[name][f"{particle}_scalar_exact"] = bool(scalar_exact)

    for values in branch_values.values():
        proton_value = sp.sympify(values["proton_O"])
        neutron_value = sp.sympify(values["neutron_O"])
        values["neutron_minus_proton_O"] = str(sp.factor(neutron_value - proton_value))

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_spin_flavor_permutation_carrier_gate",
        "field": "Q with exact S3 representation matrices",
        "S3_character_table": {
            "class_order": ["identity", "transposition", "three_cycle"],
            "class_sizes": [1, 3, 2],
            "irreducible_order": ["trivial", "sign", "standard"],
            "characters": [list(map(int, character_table.row(index))) for index in range(3)],
            "invariant_multiplicity_matrix": [
                [str(matching[row, column]) for column in range(3)]
                for row in range(3)
            ],
            "matching_matrix_is_identity": bool(matching == sp.eye(3)),
        },
        "fermionic_branch_rule": {
            "color_type": "sign",
            "required_space_tensor_spin_aroma_type": "contains trivial",
            "allowed_matched_pairs": [
                ["trivial", "trivial"],
                ["sign", "sign"],
                ["standard", "standard"],
            ],
            "unique_symmetric_branch_selected": False,
        },
        "joint_I_half_S_half_sector": {
            "proton_dimension": joint_dimensions["proton"],
            "neutron_dimension": joint_dimensions["neutron"],
            "decomposition": "trivial + sign + standard",
            "branch_values": branch_values,
        },
        "sufficient_extra_condition": {
            "spatial_ground_state_type": "trivial",
            "spatial_ground_state_dimension": "1",
            "then_spin_aroma_type": "trivial",
            "then_neutron_minus_proton_O": "-1/3",
            "spatial_parent_present": False,
        },
        "verdict": {
            "pauli_principle_selects_matching_types": True,
            "pauli_principle_selects_symmetric_spin_aroma_alone": False,
            "magnetic_branch_unique_in_current_project": False,
            "next_gate": "version8_baryon_spatial_ground_state_symmetry_origin_gate",
        },
    }

    assert matching == sp.eye(3)
    assert projector_trivial.rank() == 20
    assert projector_sign.rank() == 4
    assert projector_standard.rank() == 40
    assert joint_dimensions == {"proton": 4, "neutron": 4}
    assert branch_values["trivial"]["neutron_minus_proton_O"] == "-1/3"
    assert branch_values["sign"]["neutron_minus_proton_O"] == "1"
    assert branch_values["standard"]["neutron_minus_proton_O"] == "1/3"
    assert all(
        values[f"{particle}_scalar_exact"]
        for values in branch_values.values()
        for particle in ("proton", "neutron")
    )
    assert not any(atom.is_Float for atom in sp.preorder_traversal(magnetic_form))

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()