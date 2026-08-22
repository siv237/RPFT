#!/usr/bin/env python3
"""Audit whether existing parents canonically couple family R to compacton radiation."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_radiative_cooling_common_carrier_attribution_gate_results.json"


def load(name: str) -> dict[str, object]:
    return json.loads((RESULTS / name).read_text(encoding="utf-8"))


def random_density(rng: np.random.Generator, dimension: int) -> np.ndarray:
    matrix = rng.normal(size=(dimension, dimension)) + 1.0j * rng.normal(size=(dimension, dimension))
    density = matrix @ matrix.conj().T
    return density / np.trace(density)


def random_unitary(rng: np.random.Generator, dimension: int) -> np.ndarray:
    matrix = rng.normal(size=(dimension, dimension)) + 1.0j * rng.normal(size=(dimension, dimension))
    q, r = np.linalg.qr(matrix)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0.0, phases / np.abs(phases), 1.0)
    return q @ np.diag(np.conj(phases))


def partial_trace_walk(density: np.ndarray, family_dimension: int, walk_dimension: int) -> np.ndarray:
    tensor = density.reshape(family_dimension, walk_dimension, family_dimension, walk_dimension)
    return np.einsum("aibi->ab", tensor)


def full_matrix_commutant_nullity(dimension: int) -> tuple[int, np.ndarray]:
    identity = np.eye(dimension, dtype=complex)
    constraints = []
    for row in range(dimension):
        for column in range(dimension):
            matrix_unit = np.zeros((dimension, dimension), dtype=complex)
            matrix_unit[row, column] = 1.0
            constraints.append(np.kron(matrix_unit.T, identity) - np.kron(identity, matrix_unit))
    operator = np.vstack(constraints)
    singular_values = np.linalg.svd(operator, compute_uv=False)
    tolerance = 1.0e-12
    rank = int(np.count_nonzero(singular_values > tolerance))
    return dimension * dimension - rank, singular_values


def main() -> None:
    nonlinear = load("s2t_v6_spectral_transition_discrete_nonlinear_parent_reopening_gate_results.json")
    selector = load("s2t_v6_spectral_transition_discrete_equivariant_coin_selector_gate_results.json")
    chiral = load("s2t_v6_spectral_transition_discrete_chiral_coin_closure_gate_results.json")
    affine = load("s2t_v6_existing_multiplicity_resonant_sink_gate_results.json")
    radiation = load("s2t_v6_spectral_transition_real_pair_radiative_cooling_parent_gate_results.json")

    assert nonlinear["analytic_structure"]["full_internal_bimodule_dimension"] == 300
    assert nonlinear["analytic_structure"]["full_bimodule_commutant"] == "C_times_identity"
    assert nonlinear["verdict"]["internal_multiplicity_reduced"] is False
    assert selector["physical_observed_carrier"]["dimension"] == 15
    assert selector["physical_observed_carrier"]["commutant_complex_dimension"] == 5
    assert selector["verdict"]["unique_physical_selector_derived"] is False
    assert chiral["verdict"]["endogenous_composite_higgs_coin_constructed"] is True
    assert chiral["verdict"]["unique_chiral_endpoint_selected"] is False
    assert affine["affine_triplet_certificate"]["V_maps_P3_to_family_triplet"] is True
    assert affine["canonical_affine_coupling_test"]["acts_as_scalar_on_family_triplet"] is True
    assert affine["canonical_affine_coupling_test"]["creates_uniaxial_split"] is False
    assert radiation["verdict"]["Real_pair_positive_radiation_current_nonzero"] is True
    assert radiation["verdict"]["route_passes_parent_gate"] is False

    commutant_nullity, singular_values = full_matrix_commutant_nullity(3)
    assert commutant_nullity == 1

    rng = np.random.default_rng(20260822)
    family_dimension = 3
    walk_dimension = 6
    lift = np.kron(np.eye(family_dimension), random_unitary(rng, walk_dimension))
    maximum_reduced_state_residual = 0.0
    maximum_trace_residual = 0.0
    trials = 24
    for _ in range(trials):
        joint = random_density(rng, family_dimension * walk_dimension)
        before = partial_trace_walk(joint, family_dimension, walk_dimension)
        after_joint = lift @ joint @ lift.conj().T
        after = partial_trace_walk(after_joint, family_dimension, walk_dimension)
        maximum_reduced_state_residual = max(maximum_reduced_state_residual, float(np.linalg.norm(after - before)))
        maximum_trace_residual = max(maximum_trace_residual, float(abs(np.trace(after_joint) - 1.0)))

    candidates = {
        "full_M20_M15_bimodule": {
            "already_exists": True,
            "contains_compacton_internal_carrier": True,
            "contains_family_selective_intertwiner": False,
            "obstruction": "the full bimodule commutant is C times the identity",
        },
        "physical_H15_reduction": {
            "already_exists": True,
            "contains_chiral_compacton_sector": True,
            "contains_family_R_sector": False,
            "obstruction": "its five central blocks distinguish Standard Model species within one family line, not the SO(3) family triplet",
        },
        "affine_P3_coisometry": {
            "already_exists": True,
            "contains_family_R_sector": True,
            "contains_outgoing_spatial_chiral_modes": False,
            "obstruction": "the canonical rho V coupling is isotropic and preserves R=I3/3",
        },
        "declared_tensor_product_C3_family_tensor_walk": {
            "already_exists_as_named_parent": False,
            "kinematically_well_defined": True,
            "canonical_factorized_lift_changes_R": False,
            "obstruction": "I3 tensor U_walk leaves the family reduced state invariant; a nontrivial coupling requires new Q- or P-dependent data",
        },
    }

    required_items = {
        "one_existing_declared_carrier_contains_family_chiral_and_spatial_factors": False,
        "canonical_intertwiner_is_non_scalar_on_family_triplet": False,
        "intertwiner_changes_family_spectrum_without_assuming_axis_P": False,
        "same_trace_normalization_covers_projective_energy_and_walk_flux": False,
        "derived_partial_trace_identifies_outgoing_modes_as_family_environment": False,
        "no_new_coupling_or_scale_is_required": False,
    }
    assert not any(required_items.values())
    assert maximum_reduced_state_residual < 1.0e-13
    assert maximum_trace_residual < 1.0e-13

    result = {
        "gate": "version6_spectral_transition_radiative_cooling_common_carrier_attribution_gate",
        "existing_carrier_attribution": {
            "full_internal_bimodule_dimension": nonlinear["analytic_structure"]["full_internal_bimodule_dimension"],
            "full_bimodule_commutant": nonlinear["analytic_structure"]["full_bimodule_commutant"],
            "physical_one_family_carrier_dimension": selector["physical_observed_carrier"]["dimension"],
            "physical_species_commutant_dimension": selector["physical_observed_carrier"]["commutant_complex_dimension"],
            "family_triplet_dimension": 3,
            "family_full_matrix_action_commutant_dimension": commutant_nullity,
            "smallest_nonzero_commutant_constraint_singular_value": float(min(x for x in singular_values if x > 1.0e-12)),
        },
        "factorized_lift_no_go": {
            "family_dimension": family_dimension,
            "walk_dimension": walk_dimension,
            "random_entangled_joint_state_trials": trials,
            "maximum_family_reduced_state_residual_after_I3_tensor_Uwalk": maximum_reduced_state_residual,
            "maximum_joint_trace_residual": maximum_trace_residual,
            "exact_statement": "for every joint state Omega, Tr_walk[(I3 tensor U) Omega (I3 tensor U*)]=Tr_walk(Omega)",
        },
        "candidate_ledger": candidates,
        "required_parent_items": required_items,
        "passed_parent_item_count": sum(required_items.values()),
        "retained_exact_data": {
            "Real_pair_positive_radiation_flux": radiation["Real_pair_radiation_test"]["physical_half_trace_flux"],
            "expected_4pi2": radiation["Real_pair_radiation_test"]["expected_4pi2"],
            "radiation_flux_is_dynamically_attributed_to_R": False,
        },
        "verdict": {
            "common_ambient_tensor_product_can_be_declared": True,
            "common_carrier_is_already_derived_as_one_parent": False,
            "canonical_existing_intertwiner_changes_R": False,
            "radiative_cooling_route_closed_at_existing_parent_level": True,
            "status": "the family triplet and compacton walk can be placed in a common tensor product, but this is a new kinematic declaration rather than an existing attributed parent. The full M20-M15 commutant is scalar, the physical H15 projectors distinguish species rather than families, and the affine P3 link is isotropic. The only coefficient-free factorized lift is identity on the family factor and exactly preserves the reduced state R, including for entangled joint states. A cooling interaction would therefore require a new Q- or P-dependent intertwiner, normalization and subsystem split. The exact 4pi^2 radiation coefficient remains valid but dynamically disconnected from projective ordering.",
            "next_gate": "version6_spectral_transition_post_radiative_bridge_final_dynamic_status_gate",
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()