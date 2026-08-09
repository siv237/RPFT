#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np

from s2t_shared_holonomy_two_sector_audit import (
    POINTS,
    affine_permutation,
    algebra_dimension,
    commutant_dimension,
    generated_group,
    permutation_matrix,
    restrict,
    spectral_ratio,
    triplet_basis,
)


def permutation_sign(permutation):
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(4)
        for right in range(left + 1, 4)
    )
    return -1 if inversions % 2 else 1


def cycle_type(permutation):
    seen = set()
    lengths = []
    for start in range(4):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return "+".join(map(str, sorted(lengths, reverse=True)))


def rotation_axis(rotation):
    eigenvalues, eigenvectors = np.linalg.eig(rotation)
    index = int(np.argmin(np.abs(eigenvalues - 1.0)))
    axis = np.real(eigenvectors[:, index])
    axis /= np.linalg.norm(axis)
    for value in axis:
        if abs(value) > 1e-10:
            if value < 0:
                axis = -axis
            break
    return axis


def axis_key(axis):
    return tuple(np.round(np.outer(axis, axis).reshape(-1), 10))


def rodrigues(axis, cosine, sine):
    nx, ny, nz = axis
    cross = np.array(
        [[0.0, -nz, ny], [nz, 0.0, -nx], [-ny, nx, 0.0]], dtype=float
    )
    return (
        cosine * np.eye(3)
        + (1.0 - cosine) * np.outer(axis, axis)
        + sine * cross
    )


def main():
    identity2 = np.eye(2, dtype=int)
    shear2 = np.array([[1, 0], [1, 1]], dtype=int)
    translation_x = affine_permutation(identity2, (1, 0))
    translation_y = affine_permutation(identity2, (0, 1))
    shear = affine_permutation(shear2, (0, 0))
    current_group = generated_group([translation_x, translation_y, shear])

    basis = triplet_basis()
    restricted_tx = restrict(permutation_matrix(translation_x), basis)
    restricted_ty = restrict(permutation_matrix(translation_y), basis)
    current_generators = [
        restricted_tx,
        restricted_ty,
        restrict(permutation_matrix(shear), basis),
    ]

    target_cosine = (26.0 - 9.0 * math.sqrt(15.0)) / 11.0
    target_angle = math.acos(target_cosine)
    target_phase = target_angle / (2.0 * math.pi)
    target_sine = math.sin(target_angle)

    def response(cosine):
        phase = math.acos(cosine) / (2.0 * math.pi)
        return spectral_ratio(0.0) + 2.0 * spectral_ratio(phase)

    response_at_target = response(target_cosine)
    response_derivative = 8.0 * (5.0 + target_cosine) / (
        3.0 * (1.0 - target_cosine) ** 3
    )
    gap_curvature = response_derivative
    cosine_sensitivity_to_bare_stiffness = 1.0 / response_derivative

    axis_sources = {}
    for permutation in itertools.permutations(range(4)):
        if permutation == tuple(range(4)):
            continue
        standard = restrict(permutation_matrix(permutation), basis)
        proper_rotation = permutation_sign(permutation) * standard
        axis = rotation_axis(proper_rotation)
        axis_sources.setdefault(axis_key(axis), {"axis": axis, "sources": []})[
            "sources"
        ].append(
            {
                "permutation": list(permutation),
                "cycle_type": cycle_type(permutation),
                "inside_current_D8": permutation in current_group,
            }
        )

    kernels = {
        "inverse_length": (1.0 / math.pi, 1.0 / (2.0 * math.pi)),
        "inverse_square": (1.0 / math.pi**2, 1.0 / (4.0 * math.pi**2)),
        "tunneling": (math.exp(-math.pi), math.exp(-2.0 * math.pi)),
    }
    factor_operators = {
        name: w3 * (np.eye(3) - restricted_tx)
        + w1 * (np.eye(3) - restricted_ty)
        for name, (w3, w1) in kernels.items()
    }

    rows = []
    for data in axis_sources.values():
        axis = data["axis"]
        wilson = rodrigues(axis, target_cosine, target_sine)
        incidence = 0.5 * (wilson + wilson.T)
        generators = current_generators + [incidence]
        outside_sources = [
            source for source in data["sources"] if not source["inside_current_D8"]
        ]
        rows.append(
            {
                "axis": axis.tolist(),
                "source_cycle_types": sorted(
                    {source["cycle_type"] for source in data["sources"]}
                ),
                "outside_D8_source_count": len(outside_sources),
                "family_algebra_dimension": algebra_dimension(generators),
                "family_commutant_dimension": commutant_dimension(generators),
                "full_M3": algebra_dimension(generators) == 9,
                "factor_costs": {
                    name: float(axis @ operator @ axis)
                    for name, operator in factor_operators.items()
                },
            }
        )

    joint_rows = [
        row
        for row in rows
        if row["full_M3"] and row["outside_D8_source_count"] > 0
    ]
    selector_summary = {}
    for kernel in kernels:
        minimum = min(row["factor_costs"][kernel] for row in joint_rows)
        minima = [
            row for row in joint_rows if abs(row["factor_costs"][kernel] - minimum) < 1e-10
        ]
        selector_summary[kernel] = {
            "minimum_cost": minimum,
            "degeneracy": len(minima),
            "selected_cycle_types": [row["source_cycle_types"] for row in minima],
            "selected_axes": [row["axis"] for row in minima],
        }

    results = {
        "status": "spectral_gap_action_has_a_stable_exact_Wilson_saddle_and_factor_geometry_reduces_axis_choice_but_does_not_complete_the_physical_derivation",
        "date": "2026-08-05",
        "continuous_two_sector_solution": {
            "cos_theta": "(26-9*sqrt(15))/11",
            "cos_theta_numeric": target_cosine,
            "phase": target_phase,
            "tensor_response_over_pi4": response_at_target,
            "canonical_axes": len(rows),
            "joint_full_M3_axes": len(joint_rows),
        },
        "gap_action": {
            "response": "R(c)=1/45+8(2+c)/(3(1-c)^2)",
            "potential": "V_gap(c)=(8/3)(3/(1-c)+log(1-c))-(44/45)c",
            "stationarity": "V_gap'(c)=R(c)-1=0",
            "stationary_polynomial": "11*c^2-52*c-49=0",
            "curvature_at_target": gap_curvature,
            "stable_local_minimum": gap_curvature > 0,
            "bare_stiffness": 1.0,
            "dc_dkappa_at_kappa_1": cosine_sensitivity_to_bare_stiffness,
            "interpretation": (
                "The exact angle is a stable saddle of a parameter-free spectral primitive if the tree-level stiffness is canonically one. The one is therefore the new normalization gate."
            ),
            "standard_determinant_status": (
                "The potential contains both a resolvent-like 1/(1-c) term and a log-determinant term. It is a valid primitive of the susceptibility but has not yet been derived from a local BV/BRST field content."
            ),
        },
        "finite_order_gate": {
            "polynomial_for_two_cos_theta": "11*x^2-104*x-196",
            "finite_order": False,
            "reason": "two_cos_theta_is_not_an_algebraic_integer",
        },
        "factor_axis_selector": {
            "kernels": {
                name: {"weight_rp3": weights[0], "weight_s1": weights[1]}
                for name, weights in kernels.items()
            },
            "summary": selector_summary,
            "finding": (
                "Each tested pre-existing factor kernel reduces the eight joint axes to a smaller minimum set. Whether this is a legitimate vacuum-selection energy requires deriving the coupling n^T L n from the same boundary action."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "The exact Wilson angle is not merely an isolated fitted point: it is a stable stationary point of an explicit zero-parameter spectral gap functional, and existing factor operators can reduce the axis degeneracy."
            ),
            "negative": (
                "Canonical unit stiffness, the resolvent-plus-determinant field origin, the axis coupling, BRST completion and source normalization are not yet derived from one local action."
            ),
            "next_gate": (
                "Construct a local auxiliary-field or boundary gauge action whose one-loop integration produces V_gap with unit tree stiffness and the factor-axis term, then recompute the complete determinant signs."
            ),
        },
        "axis_rows": rows,
    }

    Path("s2t_continuous_wilson_gap_action_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "joint_axes": len(joint_rows),
                "response": response_at_target,
                "gap_curvature": gap_curvature,
                "dc_dkappa": cosine_sensitivity_to_bare_stiffness,
                "axis_selector": selector_summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()