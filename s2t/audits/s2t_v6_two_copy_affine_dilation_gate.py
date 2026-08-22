#!/usr/bin/env python3
"""Audit the two-copy realization boundary of normalized state squaring."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def swap_operator(dimension: int) -> np.ndarray:
    swap = np.zeros((dimension**2, dimension**2))
    for i in range(dimension):
        for j in range(dimension):
            swap[j * dimension + i, i * dimension + j] = 1.0
    return swap


def random_state(rng: np.random.Generator) -> np.ndarray:
    matrix = rng.normal(size=(3, 3))
    gram = matrix @ matrix.T
    return gram / np.trace(gram)


def square_map(state: np.ndarray) -> np.ndarray:
    square = state @ state
    return square / np.trace(square)


def diagonal_family(parameter: float) -> np.ndarray:
    return np.diag([parameter, 0.5 * (1.0 - parameter), 0.5 * (1.0 - parameter)])


def main() -> None:
    rng = np.random.default_rng(20260819)
    swap = swap_operator(3)
    identity = np.eye(3)
    virtual_residuals = []
    for _ in range(100):
        state = random_state(rng)
        observable = rng.normal(size=(3, 3))
        observable = 0.5 * (observable + observable.T)
        numerator = np.trace(np.kron(observable, identity) @ swap @ np.kron(state, state))
        denominator = np.trace(swap @ np.kron(state, state))
        virtual = numerator / denominator
        direct = np.trace(observable @ square_map(state))
        virtual_residuals.append(abs(float(virtual - direct)))

    sample_parameters = np.linspace(0.05, 0.95, 181)
    target_axis = np.array(
        [square_map(diagonal_family(parameter))[0, 0] for parameter in sample_parameters]
    )
    design = np.column_stack(
        [np.ones_like(sample_parameters), sample_parameters, sample_parameters**2]
    )
    coefficients, *_ = np.linalg.lstsq(design, target_axis, rcond=None)
    quadratic_fit = design @ coefficients
    quadratic_residual = float(np.max(np.abs(target_axis - quadratic_fit)))

    mixture_one = diagonal_family(0.2)
    mixture_two = diagonal_family(0.8)
    midpoint = 0.5 * (mixture_one + mixture_two)
    affine_defect = float(
        np.linalg.norm(
            square_map(midpoint)
            - 0.5 * (square_map(mixture_one) + square_map(mixture_two))
        )
    )

    result = {
        "gate": "version6_two_copy_affine_dilation_gate",
        "two_copy_virtual_identity": {
            "numerator": "Tr[(O tensor I) SWAP (R tensor R)]=Tr(O R^2)",
            "denominator": "Tr[SWAP (R tensor R)]=Tr(R^2)",
            "maximum_numeric_residual": max(virtual_residuals),
            "normalized_square_observables_available": True,
            "normalized_square_state_physically_prepared": False,
        },
        "deterministic_channel_obstruction": {
            "input_curve": "R(t) tensor R(t) is polynomial of degree two in t",
            "fixed_linear_channel_output_curve": "polynomial of degree at most two in t",
            "target_axis_curve": "t^2/[t^2+(1-t)^2/2]",
            "best_quadratic_uniform_grid_residual": quadratic_residual,
            "convex_affinity_defect": affine_defect,
            "exact_fixed_trace_preserving_realization": False,
        },
        "project_interpretation": {
            "tensor_square_carrier_exists": True,
            "swap_and_exterior_contractions_exist": True,
            "virtual_feedback_observable_is_representable": True,
            "virtual_feedback_term_is_parent_derived": False,
            "autonomous_state_update_requires_extra_instrument": True,
            "allowed_extra_structures": [
                "postselection with a derived success branch",
                "measurement and feedback",
                "a larger unitary dilation with discarded record",
                "or a controlled mean-field limit",
            ],
        },
        "verdict": {
            "two_copy_route_is_mathematically_real": True,
            "two_copy_route_is_only_virtual_at_current_parent_level": True,
            "nonlinear_update_is_autonomous_dynamics": False,
            "effective_free_energy_remains_valid": True,
            "matter_field_expansion_may_proceed": True,
            "matter_birth_fully_derived": False,
            "next_gate": "version6_projective_order_parameter_field_spectrum_gate",
        },
    }

    assert result["two_copy_virtual_identity"]["maximum_numeric_residual"] < 2e-13
    assert quadratic_residual > 1e-2
    assert affine_defect > 1e-2

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v6_two_copy_affine_dilation_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()