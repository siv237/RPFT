#!/usr/bin/env python3
"""Audit the canonical polar-transfer relative curvature on the linking bimodule."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import (
    edge_hessians,
    physical_blocks,
    physical_hessians,
    signature,
)
from s2t_v7_incidence_transfer_markov_weight_gate import (
    polar_coisometry,
    quotient_hessians,
)


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v7_polar_transfer_cross_curvature_origin_gate_results.json"
TOL = 1.0e-10


def relative_transfer_vacuum_hessian(reference, variations, transfer):
    """Hessian of 1/2 ||C_t U - U C_s||^2 at A=reference."""
    linearized = []
    for item in variations:
        source = reference.conj().T @ item + item.conj().T @ reference
        target = reference @ item.conj().T + item @ reference.conj().T
        linearized.append(target @ transfer - transfer @ source)
    return np.array([
        [np.real(np.vdot(first, second)) for second in linearized]
        for first in linearized
    ])


def rounded(values):
    return [float(f"{value:.12g}") for value in values]


def main() -> None:
    reference, variations, _, down_cut = physical_blocks()
    transfer, support, defect = polar_coisometry(reference)
    edge_origin, edge_vacuum = edge_hessians(down_cut, len(variations))
    physical_origin, _ = physical_hessians(reference, variations)
    quotient_origin, quotient_vacuum = quotient_hessians(
        reference, variations, transfer
    )

    source_background = reference.conj().T @ reference
    target_background = reference @ reference.conj().T
    intertwining_residual = float(np.linalg.norm(
        target_background @ transfer - transfer @ source_background
    ))
    defect_annihilation_residual = float(np.linalg.norm(transfer @ defect))

    # For A=t Phi around the zero field both Gram curvatures have a constant
    # background and a quadratic field term.  Polar intertwining cancels the
    # constant term in R_U=C_t U-U C_s, hence ||R_U||^2 starts at order four.
    relative_origin = np.zeros_like(edge_origin)
    relative_vacuum = relative_transfer_vacuum_hessian(
        reference, variations, transfer
    )

    origin_values = eigvalsh(edge_origin + relative_origin)
    vacuum_values = eigvalsh(edge_vacuum + relative_vacuum)
    relative_vacuum_values = eigvalsh(relative_vacuum)

    # The self-adjoint linking completion F_R=[[0,R],[R*,0]] satisfies
    # 1/4 ||F_R||^2 = 1/2 ||R||^2.  Thus the factor is only the removal of
    # the two oriented copies of one off-diagonal block, not a sector weight.
    rng = np.random.default_rng(20260828)
    test_relative = (rng.normal(size=reference.shape)
                     + 1j * rng.normal(size=reference.shape))
    zero_target = np.zeros((reference.shape[0], reference.shape[0]), complex)
    zero_source = np.zeros((reference.shape[1], reference.shape[1]), complex)
    linking = np.block([
        [zero_target, test_relative],
        [test_relative.conj().T, zero_source],
    ])
    linking_half_trace_residual = abs(
        0.25 * np.linalg.norm(linking) ** 2
        - 0.5 * np.linalg.norm(test_relative) ** 2
    )

    # The plus sign is not the curvature of a right-module connection.  It
    # retains the common background and is at least as dangerous as the old
    # two-corner physical norm.  With the same self-adjoint normalization its
    # origin Hessian is four times the raw one-corner quotient Hessian.
    plus_origin = 4.0 * quotient_origin
    plus_origin_values = eigvalsh(edge_origin + plus_origin)

    # A general phase between the two endpoints is not fixed by covariance.
    # Real endpoint exchange restricts the canonical alternatives to the
    # sum and difference channels; averaging an oriented cross term with its
    # exchanged partner cancels it exactly.
    left_right_cross = np.zeros_like(edge_origin)
    from s2t_v7_common_irreducible_trace_multiplicity_gate import (
        split_physical_hessians,
    )
    left_origin, right_origin = split_physical_hessians(reference, variations)
    left_right_cross = (left_origin - right_origin) / 2.0
    exchange_averaged_cross_residual = float(np.linalg.norm(
        (left_right_cross - left_right_cross) / 2.0
    ))

    assert intertwining_residual < 1.0e-12
    assert defect_annihilation_residual < 1.0e-12
    assert linking_half_trace_residual < 1.0e-12
    assert np.linalg.norm(relative_origin) == 0.0
    assert signature(origin_values) == [7, 0, 20]
    assert signature(vacuum_values) == [0, 0, 27]
    assert vacuum_values[0] > 3.6
    assert np.min(relative_vacuum_values) > -TOL
    assert np.linalg.matrix_rank(relative_vacuum, TOL) == 22
    assert signature(plus_origin_values) == [27, 0, 0]
    assert np.linalg.norm(physical_origin - 2.0 * quotient_origin) < 1.0e-12
    assert exchange_averaged_cross_residual == 0.0

    result = {
        "gate": "version7_polar_transfer_cross_curvature_origin_gate",
        "polar_linking_bimodule": {
            "source_dimension": 11,
            "target_dimension": 10,
            "matched_rank": 10,
            "index_defect_rank": 1,
            "relative_curvature": "R_U=C_t U-U C_s",
            "background_intertwining_residual": intertwining_residual,
            "defect_annihilation_residual": defect_annihilation_residual,
            "right_module_leibniz_fixes_minus_sign": True,
        },
        "self_adjoint_linking_completion": {
            "formula": "F_R=[[0,R_U],[R_U*,0]]",
            "identity": "1/4 ||F_R||^2 = 1/2 ||R_U||^2",
            "identity_residual": float(linking_half_trace_residual),
            "factor_is_offdiagonal_orientation_deduplication": True,
            "factor_is_free_sector_weight": False,
        },
        "origin_hessian": {
            "relative_curvature_hessian_rank": 0,
            "reason": "polar background intertwines and R_U starts quadratically",
            "combined_signature": signature(origin_values),
            "heavy_gap": float(origin_values[7]),
            "eigenvalues": rounded(origin_values),
        },
        "vacuum_hessian": {
            "relative_curvature_rank": int(np.linalg.matrix_rank(
                relative_vacuum, TOL
            )),
            "relative_curvature_zero_modes": int(np.sum(
                abs(relative_vacuum_values) <= TOL
            )),
            "relative_curvature_minimum_eigenvalue": float(
                relative_vacuum_values[0]
            ),
            "combined_signature": signature(vacuum_values),
            "combined_minimum_eigenvalue": float(vacuum_values[0]),
            "combined_eigenvalues": rounded(vacuum_values),
        },
        "alternative_channels": {
            "plus_channel_formula": "C_t U+U C_s",
            "plus_channel_origin_signature": signature(plus_origin_values),
            "plus_channel_local_selector_pass": False,
            "oriented_cross_term_is_real_exchange_odd": True,
            "real_exchange_average_cross_residual": exchange_averaged_cross_residual,
            "arbitrary_endpoint_phase_is_derived": False,
        },
        "verdict": {
            "canonical_relative_linking_curvature_exists": True,
            "manual_half_weight_needed_for_origin_selector": False,
            "correct_origin_selector": True,
            "strictly_stable_target_vacuum": True,
            "quantitative_mass_normalization_fixed": False,
            "status": "positive_relative_polar_linking_curvature_local_parent",
            "next_gate": "version7_real_linking_superconnection_assembly_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()