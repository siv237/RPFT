#!/usr/bin/env python3
"""Exact audit of the baryon electromagnetic magnetic-contact gate."""

from __future__ import annotations

import hashlib
import json
from itertools import permutations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_em_magnetic_hyperfine_origin_gate_results.json"


def kron3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.kronecker_product(left, middle, right)


def one_site(operator: sp.Matrix, slot: int, identity: sp.Matrix) -> sp.Matrix:
    factors = [identity, identity, identity]
    factors[slot] = operator
    return kron3(*factors)


def permutation_symmetrizer(local_dimension: int) -> sp.Matrix:
    size = local_dimension**3
    symmetrizer = sp.zeros(size, size)
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
        symmetrizer += matrix / 6
    return symmetrizer


def expectation(vector: sp.Matrix, operator: sp.Matrix) -> sp.Expr:
    return sp.factor((sp.conjugate(vector).T * operator * vector)[0])


def main() -> None:
    identity2 = sp.eye(2)
    pauli = (
        sp.Matrix([[0, 1], [1, 0]]),
        sp.Matrix([[0, -sp.I], [sp.I, 0]]),
        sp.diag(1, -1),
    )

    spin_pairs = {}
    for left, right in ((0, 1), (0, 2), (1, 2)):
        operator = sp.zeros(8, 8)
        for sigma in pauli:
            factors = [identity2, identity2, identity2]
            factors[left] = sigma
            factors[right] = sigma
            operator += kron3(*factors)
        spin_pairs[left, right] = operator

    total_spin = [
        sum((one_site(sigma / 2, slot, identity2) for slot in range(3)), sp.zeros(8, 8))
        for sigma in pauli
    ]
    total_spin_square = sum((generator**2 for generator in total_spin), sp.zeros(8, 8))

    singlet_pair = sp.zeros(8, 1)
    singlet_pair[2] = 1 / sp.sqrt(2)
    singlet_pair[4] = -1 / sp.sqrt(2)
    triplet_pair = sp.zeros(8, 1)
    triplet_pair[1] = sp.sqrt(sp.Rational(2, 3))
    triplet_pair[2] = -1 / sp.sqrt(6)
    triplet_pair[4] = -1 / sp.sqrt(6)

    up = sp.Rational(2, 3)
    down = -sp.Rational(1, 3)
    proton_charges = (up, up, down)
    neutron_charges = (up, down, down)

    coupling_results = {}
    for name, vector in (("pair_singlet", singlet_pair), ("pair_triplet", triplet_pair)):
        correlations = {
            f"{left + 1}{right + 1}": expectation(vector, operator)
            for (left, right), operator in spin_pairs.items()
        }
        proton_value = sp.factor(
            sum(
                proton_charges[left]
                * proton_charges[right]
                * correlations[f"{left + 1}{right + 1}"]
                for left, right in spin_pairs
            )
        )
        neutron_value = sp.factor(
            sum(
                neutron_charges[left]
                * neutron_charges[right]
                * correlations[f"{left + 1}{right + 1}"]
                for left, right in spin_pairs
            )
        )
        coupling_results[name] = {
            "norm": str(expectation(vector, sp.eye(8))),
            "total_spin_square": str(expectation(vector, total_spin_square)),
            "pair_correlations": {key: str(value) for key, value in correlations.items()},
            "proton_O": str(proton_value),
            "neutron_O": str(neutron_value),
            "neutron_minus_proton_O": str(sp.factor(neutron_value - proton_value)),
        }

    # Joint aroma-spin carrier: local basis (u up, u down, d up, d down).
    identity4 = sp.eye(4)
    aroma_generators = [sp.kronecker_product(sigma / 2, identity2) for sigma in pauli]
    spin_generators = [sp.kronecker_product(identity2, sigma / 2) for sigma in pauli]

    total_isospin = [
        sum((one_site(generator, slot, identity4) for slot in range(3)), sp.zeros(64, 64))
        for generator in aroma_generators
    ]
    joint_total_spin = [
        sum((one_site(generator, slot, identity4) for slot in range(3)), sp.zeros(64, 64))
        for generator in spin_generators
    ]
    isospin_square = sum((generator**2 for generator in total_isospin), sp.zeros(64, 64))
    joint_spin_square = sum((generator**2 for generator in joint_total_spin), sp.zeros(64, 64))
    symmetrizer = permutation_symmetrizer(4)

    magnetic_form = sp.zeros(64, 64)
    for left, right in ((0, 1), (0, 2), (1, 2)):
        for sigma in pauli:
            charge_spin = sp.kronecker_product(sp.diag(up, down), sigma)
            factors = [identity4, identity4, identity4]
            factors[left] = charge_spin
            factors[right] = charge_spin
            magnetic_form += kron3(*factors)

    symmetric_values = {}
    for label, isospin_z in (("proton", sp.Rational(1, 2)), ("neutron", -sp.Rational(1, 2))):
        selected_indices = [
            index
            for index in range(64)
            if total_isospin[2][index, index] == isospin_z
            and joint_total_spin[2][index, index] == sp.Rational(1, 2)
        ]
        coordinate_basis = sp.eye(64)[:, selected_indices]
        symmetric_columns = sp.Matrix.hstack(*(symmetrizer * coordinate_basis).columnspace())
        constraints = sp.Matrix.vstack(
            (isospin_square - sp.Rational(3, 4) * sp.eye(64)) * symmetric_columns,
            (joint_spin_square - sp.Rational(3, 4) * sp.eye(64)) * symmetric_columns,
        )
        nullspace = constraints.nullspace()
        assert len(nullspace) == 1
        vector = symmetric_columns * nullspace[0]
        vector /= sp.sqrt(expectation(vector, sp.eye(64)))
        symmetric_values[label] = {
            "weight_space_dimension": len(selected_indices),
            "symmetric_weight_space_dimension": symmetric_columns.shape[1],
            "joint_I_half_S_half_dimension": len(nullspace),
            "I_squared": str(expectation(vector, isospin_square)),
            "S_squared": str(expectation(vector, joint_spin_square)),
            "O": str(expectation(vector, magnetic_form)),
        }

    symmetric_difference = sp.factor(
        sp.sympify(symmetric_values["neutron"]["O"])
        - sp.sympify(symmetric_values["proton"]["O"])
    )
    opposite_signs = (
        sp.sympify(coupling_results["pair_singlet"]["neutron_minus_proton_O"]) > 0
        and sp.sympify(coupling_results["pair_triplet"]["neutron_minus_proton_O"]) < 0
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_em_magnetic_hyperfine_origin_gate",
        "field": "Q with exact radicals; no Float inputs",
        "spin_half_countermodels": coupling_results,
        "same_total_spin_opposite_difference_signs": bool(opposite_signs),
        "joint_permutation_symmetric_sector": {
            **symmetric_values,
            "neutron_minus_proton_O": str(symmetric_difference),
            "conditional_energy_difference": "-zeta*h/(3*T)",
        },
        "contact_dilation": {
            "dimension": "d",
            "law": "<delta^(d)(r_i-r_j)>_psi_s = s^d <delta^(d)(r_i-r_j)>_psi",
            "contact_scale_selected": False,
        },
        "project_boundary": {
            "weak_isospin_equals_physical_spin": False,
            "physical_spin_carrier_present_before_this_extension": False,
            "epsilon_color_projector_selects_spin_aroma_state": False,
            "s_wave_spatial_state_derived": False,
            "magnetic_moment_coefficient_derived": False,
            "conditional_algebraic_factor_derived": True,
            "physical_magnetic_splitting_derived": False,
        },
        "verdict": {
            "accept_conditional_symmetric_factor_minus_one_third": True,
            "reject_total_isospin_as_magnetic_hyperfine_operator": True,
            "next_gate": "version8_baryon_spin_flavor_permutation_carrier_gate",
        },
    }

    assert coupling_results["pair_singlet"]["total_spin_square"] == "3/4"
    assert coupling_results["pair_triplet"]["total_spin_square"] == "3/4"
    assert coupling_results["pair_singlet"]["neutron_minus_proton_O"] == "2"
    assert coupling_results["pair_triplet"]["neutron_minus_proton_O"] == "-4/3"
    assert symmetric_values["proton"]["O"] == "4/3"
    assert symmetric_values["neutron"]["O"] == "1"
    assert symmetric_difference == -sp.Rational(1, 3)
    assert not any(atom.is_Float for atom in sp.preorder_traversal(magnetic_form))

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()