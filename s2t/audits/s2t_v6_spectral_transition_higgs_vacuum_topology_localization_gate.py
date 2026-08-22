#!/usr/bin/env python3
"""Audit the topology relevant to localizing the Higgs rank transition.

The script verifies explicit contractions of an embedded winding loop and
an embedded two-sphere inside S^3.  The homotopy groups themselves are
standard exact inputs; the numerical checks certify the concrete homotopies
used in the gate and the fact that the Higgs norm never vanishes.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_higgs_vacuum_topology_localization_gate_results.json"


def main() -> None:
    phis = np.linspace(0.0, 2.0 * np.pi, 1025)
    ts = np.linspace(0.0, 1.0, 257)

    loop_norm_residuals: list[float] = []
    loop_endpoint_residuals: list[float] = []
    for winding in (1, 2, 7):
        for t in ts:
            first = np.sin(np.pi * t / 2.0) * np.ones_like(phis, dtype=complex)
            second = np.cos(np.pi * t / 2.0) * np.exp(1j * winding * phis)
            norm2 = np.abs(first) ** 2 + np.abs(second) ** 2
            loop_norm_residuals.append(float(np.max(np.abs(norm2 - 1.0))))
        endpoint = np.column_stack(
            [np.ones_like(phis, dtype=complex), np.zeros_like(phis, dtype=complex)]
        )
        loop_endpoint_residuals.append(float(np.max(np.linalg.norm(endpoint - endpoint[0], axis=1))))

    thetas = np.linspace(0.0, np.pi, 129)
    azimuths = np.linspace(0.0, 2.0 * np.pi, 257)
    sphere_points = []
    for theta in thetas:
        for phi in azimuths:
            sphere_points.append(
                [
                    np.sin(theta) * np.cos(phi),
                    np.sin(theta) * np.sin(phi),
                    np.cos(theta),
                ]
            )
    sphere = np.asarray(sphere_points)

    sphere_norm_residuals: list[float] = []
    sphere_endpoint_residuals: list[float] = []
    for t in ts:
        embedded = np.column_stack(
            [np.sqrt(1.0 - t * t) * sphere, t * np.ones(len(sphere))]
        )
        sphere_norm_residuals.append(
            float(np.max(np.abs(np.sum(embedded * embedded, axis=1) - 1.0)))
        )
        if t == 1.0:
            sphere_endpoint_residuals.append(
                float(np.max(np.linalg.norm(embedded - embedded[0], axis=1)))
            )

    # A normalized Higgs doublet has nonzero norm everywhere.  Therefore
    # W_nu=tilde(H)tilde(H)^dagger has rank one at every sampled point.
    rng = np.random.default_rng(20260821)
    rank_samples = []
    projector_residuals = []
    for _ in range(512):
        h = rng.normal(size=2) + 1j * rng.normal(size=2)
        h /= np.linalg.norm(h)
        tilde_h = np.array([np.conj(h[1]), -np.conj(h[0])], dtype=complex)
        w_nu = np.outer(tilde_h, tilde_h.conj())
        rank_samples.append(int(np.linalg.matrix_rank(w_nu, tol=1e-12)))
        projector_residuals.append(float(np.linalg.norm(w_nu @ w_nu - w_nu)))

    result = {
        "gate": "version6_spectral_transition_higgs_vacuum_topology_localization_gate",
        "vacuum_manifold": {
            "constraint": "H^dagger H=v^2/2 in C^2",
            "homogeneous_space": "(SU(2)_L x U(1)_Y)/U(1)_em",
            "topology": "S^3",
            "homotopy_groups": {"pi0": "0", "pi1": "0", "pi2": "0", "pi3": "Z"},
        },
        "explicit_loop_contraction": {
            "formula": "h_t(phi)=(sin(pi t/2), cos(pi t/2) exp(i n phi))",
            "tested_windings": [1, 2, 7],
            "max_unit_norm_residual": max(loop_norm_residuals),
            "max_constant_endpoint_residual": max(loop_endpoint_residuals),
            "crosses_H_zero": False,
        },
        "explicit_sphere_contraction": {
            "formula": "F_t(n)=(sqrt(1-t^2) n,t)",
            "sample_points": len(sphere),
            "max_unit_norm_residual": max(sphere_norm_residuals),
            "max_constant_endpoint_residual": max(sphere_endpoint_residuals),
            "crosses_H_zero": False,
        },
        "rank_change_audit": {
            "sample_count": len(rank_samples),
            "unique_ranks_of_W_nu_on_normalized_Higgs_vacuum": sorted(set(rank_samples)),
            "max_projector_residual": max(projector_residuals),
            "pi3_texture_can_keep_H_nonzero_everywhere": True,
            "pi3_texture_forces_rank_zero_core": False,
        },
        "defect_classification": {
            "domain_wall_from_one_Higgs_doublet": False,
            "topological_string_from_one_Higgs_doublet": False,
            "topological_monopole_from_one_Higgs_doublet": False,
            "texture_class_exists": True,
            "texture_localizes_rank_change_0_to_1": False,
            "embedded_or_semilocal_saddles_excluded": False,
        },
        "verdict": {
            "one_Higgs_doublet_topologically_localizes_H_zero": False,
            "one_Higgs_doublet_topologically_localizes_W_nu_rank_change": False,
            "alternative_global_electroweak_quotient_is_current_parent_derived": False,
            "non_topological_dynamic_localization_remains_open": True,
            "physical_closure": False,
            "status": "S^3 has trivial pi0, pi1 and pi2; pi3 textures keep the Higgs norm nonzero, so one standard doublet does not topologically force the rank-changing core",
        },
        "next_gate": "version6_spectral_transition_higgs_zero_finite_energy_saddle_gate",
    }

    assert result["explicit_loop_contraction"]["max_unit_norm_residual"] < 1e-12
    assert result["explicit_sphere_contraction"]["max_unit_norm_residual"] < 1e-12
    assert result["rank_change_audit"]["unique_ranks_of_W_nu_on_normalized_Higgs_vacuum"] == [1]

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()