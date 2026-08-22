#!/usr/bin/env python3
"""Аудит глобальности нейтринной линии и её полиномиального родителя."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "s2t/results"
OUT = RESULTS / "s2t_v6_spectral_transition_neutrino_line_parent_gate_results.json"
EPS = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)


def random_su2(rng: np.random.Generator) -> np.ndarray:
    z = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    q = q @ np.diag(np.conjugate(phases))
    return q / np.sqrt(np.linalg.det(q))


def objects(h: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ht = EPS @ np.conjugate(h)
    w = np.outer(ht, np.conjugate(ht))
    pairing = np.outer(ht, ht)
    p = w / np.trace(w) if np.linalg.norm(h) > 0 else np.full((2, 2), np.nan)
    return p, w, pairing


def main() -> None:
    higgs = json.loads((RESULTS / "s2t_v6_spectral_transition_higgs_resolved_support_gate_results.json").read_text())
    old = json.loads((RESULTS / "s2t_v5_holonomy_projector_defect_multiplicity_gate_results.json").read_text())
    split = json.loads((RESULTS / "s2t_v5_h15_neutrino_degree_split_gate_results.json").read_text())

    pa, _, _ = objects(np.array([1.0, 0.0], dtype=complex))
    pb, _, _ = objects(np.array([0.0, 1.0], dtype=complex))
    directional_limit_distance = float(np.linalg.norm(pa - pb))

    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    constraints = []
    for s in (sx, sy, sz):
        constraints.append(np.kron(np.eye(2), s) - np.kron(s.T, np.eye(2)))
    singular_values = np.linalg.svd(np.vstack(constraints), compute_uv=False)
    commutant_dimension = int(np.sum(singular_values < 1e-10))

    rng = np.random.default_rng(260821)
    covariance = {"normalized_projector": 0.0, "quadratic_support": 0.0, "pairing_tensor": 0.0}
    rank_samples = []
    homogeneity_residual = 0.0
    zero_continuity = 0.0
    for _ in range(24):
        h = rng.normal(size=2) + 1j * rng.normal(size=2)
        u = random_su2(rng)
        p, w, b = objects(h)
        pu, wu, bu = objects(u @ h)
        covariance["normalized_projector"] = max(covariance["normalized_projector"], float(np.linalg.norm(pu - u @ p @ u.conj().T)))
        covariance["quadratic_support"] = max(covariance["quadratic_support"], float(np.linalg.norm(wu - u @ w @ u.conj().T)))
        covariance["pairing_tensor"] = max(covariance["pairing_tensor"], float(np.linalg.norm(bu - u @ b @ u.T)))
        rank_samples.append(int(np.linalg.matrix_rank(w, tol=1e-10)))
        scale = 0.17
        _, ws, _ = objects(scale * h)
        homogeneity_residual = max(homogeneity_residual, float(np.linalg.norm(ws - scale**2 * w)))
        _, wz, _ = objects(1e-8 * h)
        zero_continuity = max(zero_continuity, float(np.linalg.norm(wz)))

    c3 = np.roll(np.eye(3), 1, axis=1)
    p0 = (np.eye(3) + c3 + c3 @ c3) / 3
    h0 = np.array([0.3 + 0.2j, -0.7 + 0.5j])
    pnu, wnu, bnu = objects(h0)

    result = {
        "gate": "version6_spectral_transition_neutrino_line_parent_gate",
        "input_certificates": {
            "Higgs_resolved_split": higgs["verdict"]["split"],
            "H15_has_Dirac_neutrino_edge": split["verdict"]["H15_contains_Dirac_neutrino_edge"],
            "previous_Higgs_dressed_projector_status": old["verdict"]["Higgs_dressed_neutrino_projector"],
        },
        "global_projector_no_go": {
            "weak_doublet_SU2_commutant_dimension": commutant_dimension,
            "only_invariant_endomorphisms": "complex scalars times I2",
            "invariant_idempotent_ranks": [0, 2],
            "constant_gauge_invariant_rank_one_projector": False,
            "directional_limits_at_H_zero_distance": directional_limit_distance,
            "continuous_SU2_equivariant_rank_one_extension_through_H_zero": False,
            "reason": "H=0 is fixed by all SU2, so an equivariant value there would have to be an invariant rank-one projector; none exists",
        },
        "quadratic_parent": {
            "unnormalized_support": "W_nu(H)=tilde(H) tilde(H)^dagger",
            "pairing_tensor": "B_nu(H)=tilde(H) tilde(H)^T",
            "polynomial_degree_in_H": 2,
            "continuous_at_H_zero": True,
            "value_at_H_zero": "zero operator",
            "rank_for_nonzero_H_samples": sorted(set(rank_samples)),
            "normalized_projector_formula": "P_nu=W_nu/Tr(W_nu)",
            "normalized_projector_defined_at_H_zero": False,
            "covariance_residuals": covariance,
            "quadratic_homogeneity_residual": homogeneity_residual,
            "norm_near_zero_at_scale_1e-8": zero_continuity,
        },
        "family_and_degree_ledger": {
            "family_holonomy_projector_rank": int(np.linalg.matrix_rank(p0, tol=1e-10)),
            "P0_tensor_Pnu_rank_for_H_nonzero": int(np.linalg.matrix_rank(np.kron(p0, pnu), tol=1e-10)),
            "P0_tensor_Wnu_rank_for_H_nonzero": int(np.linalg.matrix_rank(np.kron(p0, wnu), tol=1e-10)),
            "P0_tensor_Wnu_rank_at_H_zero": 0,
            "pairing_tensor_rank_for_H_nonzero": int(np.linalg.matrix_rank(bnu, tol=1e-10)),
            "degree_one_neutrino_edge_on_H15": False,
            "lowest_existing_route": "degree-five Weinberg operator built from two lepton and two Higgs fields",
            "absolute_coefficient_or_scale_derived": False,
            "family_pairing_matrix_derived": False,
        },
        "interpretation_boundary": {
            "global_neutrino_projector_is_parent_primitive": False,
            "quadratic_covariant_support_is_parent_admissible": True,
            "neutrino_support_changes_rank_at_Higgs_zero": True,
            "spectral_transition_can_be_defined_without_normalizing_to_a_line": True,
            "observed_neutrino_mass_derived": False,
        },
        "verdict": {
            "normalized_neutrino_line_parent_closed": False,
            "polynomial_neutrino_transition_support_exists": True,
            "correct_primitive": "unnormalized Higgs-quadratic covariant, not a globally smooth rank-one projector",
            "physical_closure": False,
            "status": "the normalized line is necessarily singular at Higgs zeros, while its unnormalized quadratic support extends canonically by zero; the missing data are the Weinberg coefficient, family tensor and nonlinear parent",
        },
        "next_gate": "version6_spectral_transition_weinberg_pairing_parent_gate",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()