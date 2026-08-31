#!/usr/bin/env python3
"""Exact audit of the baryon electromagnetic spatial-kernel gate."""

from __future__ import annotations

import hashlib
import json
from itertools import permutations
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_em_spatial_kernel_origin_gate_results.json"


def energy(charges: tuple[sp.Rational, ...], mu: sp.Symbol, pairs: dict[tuple[int, int], sp.Symbol]) -> sp.Expr:
    self_part = mu * sum(charge**2 for charge in charges)
    pair_part = 2 * sum(pairs[i, j] * charges[i] * charges[j] for i, j in pairs)
    return sp.factor(self_part + pair_part)


def distinct_permutations(charges: tuple[sp.Rational, ...]) -> list[tuple[sp.Rational, ...]]:
    return sorted(set(permutations(charges)), key=str)


def main() -> None:
    mu, g12, g13, g23, s, g0 = sp.symbols("mu g12 g13 g23 s g0", positive=True)
    up = sp.Rational(2, 3)
    down = -sp.Rational(1, 3)
    pairs = {(0, 1): g12, (0, 2): g13, (1, 2): g23}

    proton = (up, up, down)
    neutron = (up, down, down)
    ep = energy(proton, mu, pairs)
    en = energy(neutron, mu, pairs)
    labelled_difference = sp.factor(en - ep)
    labelled_expected = sp.factor(-mu / 3 + sp.Rational(2, 3) * (g23 - 2 * g12))

    positive_counterexample = sp.factor(
        labelled_difference.subs({mu: 1, g12: 1, g13: 1, g23: 3})
    )

    proton_orbit = distinct_permutations(proton)
    neutron_orbit = distinct_permutations(neutron)
    ep_average = sp.factor(sum(energy(state, mu, pairs) for state in proton_orbit) / 3)
    en_average = sp.factor(sum(energy(state, mu, pairs) for state in neutron_orbit) / 3)
    averaged_difference = sp.factor(en_average - ep_average)
    gbar = sp.factor((g12 + g13 + g23) / 3)
    averaged_expected = sp.factor(-(mu + 2 * gbar) / 3)

    pair_averages = {}
    for name, orbit in (("proton", proton_orbit), ("neutron", neutron_orbit)):
        pair_averages[name] = {
            f"{i + 1}{j + 1}": str(sp.factor(sum(state[i] * state[j] for state in orbit) / 3))
            for i, j in pairs
        }

    coulomb_before = g0
    coulomb_after_dilation = sp.factor(s * g0)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_em_spatial_kernel_origin_gate",
        "field": "Q(mu,g12,g13,g23,s,g0)",
        "labelled_three_copy_model": {
            "proton_energy_times_T": str(ep),
            "neutron_energy_times_T": str(en),
            "neutron_minus_proton_times_T": str(labelled_difference),
            "closed_form_identity_exact": sp.simplify(labelled_difference - labelled_expected) == 0,
            "positive_kernel_counterexample": {
                "mu": "1",
                "g12": "1",
                "g13": "1",
                "g23": "3",
                "difference_times_T": str(positive_counterexample),
                "sign_flipped_positive": bool(positive_counterexample > 0),
            },
        },
        "permutation_averaged_model": {
            "proton_orbit_size": len(proton_orbit),
            "neutron_orbit_size": len(neutron_orbit),
            "pair_charge_averages": pair_averages,
            "proton_energy_times_T": str(ep_average),
            "neutron_energy_times_T": str(en_average),
            "g_bar": str(gbar),
            "neutron_minus_proton_times_T": str(averaged_difference),
            "closed_form_identity_exact": sp.simplify(averaged_difference - averaged_expected) == 0,
            "negative_for_positive_mu_and_g_bar": True,
        },
        "coulomb_dilation": {
            "kernel_expectation_before": str(coulomb_before),
            "kernel_expectation_after_coordinate_dilation": str(coulomb_after_dilation),
            "homogeneity_degree": "1",
            "scale_selected_by_charge_algebra": False,
        },
        "project_boundary": {
            "charge_algebra_selects_pair_kernel": False,
            "epsilon_singlet_selects_radial_scale": False,
            "three_copy_coordinate_carrier_present": False,
            "positive_sign_protected_without_permutation_average": False,
            "negative_electrostatic_sign_after_permutation_average": True,
            "physical_splitting_magnitude_derived": False,
        },
        "verdict": {
            "accept_conditional_symmetrized_sign": True,
            "reject_spatial_kernel_as_derived_from_charge_identity": True,
            "next_gate": "version8_baryon_em_magnetic_hyperfine_origin_gate",
        },
    }

    assert sp.simplify(labelled_difference - labelled_expected) == 0
    assert positive_counterexample == sp.Rational(1, 3)
    assert pair_averages["proton"] == {"12": "0", "13": "0", "23": "0"}
    assert pair_averages["neutron"] == {"12": "-1/9", "13": "-1/9", "23": "-1/9"}
    assert sp.simplify(averaged_difference - averaged_expected) == 0
    assert not any(atom.is_Float for atom in sp.preorder_traversal(labelled_difference))
    assert not any(atom.is_Float for atom in sp.preorder_traversal(averaged_difference))

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()