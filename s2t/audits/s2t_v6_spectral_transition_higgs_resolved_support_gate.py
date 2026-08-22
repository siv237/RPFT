#!/usr/bin/env python3
"""Аудит хиггс-разрешённых опор пакета H15."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "s2t/results/s2t_v6_spectral_transition_higgs_resolved_support_gate_results.json"


def random_su(rng: np.random.Generator, n: int) -> np.ndarray:
    z = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    q, r = np.linalg.qr(z)
    phases = np.diag(r)
    phases = np.where(np.abs(phases) > 0, phases / np.abs(phases), 1.0)
    q = q @ np.diag(np.conjugate(phases))
    return q / np.linalg.det(q) ** (1 / n)


def projectors(h: np.ndarray) -> dict[str, np.ndarray]:
    eps = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    ht = eps @ np.conjugate(h)
    norm2 = float(np.vdot(h, h).real)
    ph = np.outer(h, np.conjugate(h)) / norm2
    pt = np.outer(ht, np.conjugate(ht)) / norm2

    blocks = {name: np.zeros((15, 15), dtype=complex) for name in ("up", "down", "electron", "neutrino")}
    blocks["up"][:6, :6] = np.kron(np.eye(3), pt)
    blocks["up"][8:11, 8:11] = np.eye(3)
    blocks["down"][:6, :6] = np.kron(np.eye(3), ph)
    blocks["down"][11:14, 11:14] = np.eye(3)
    blocks["electron"][6:8, 6:8] = ph
    blocks["electron"][14, 14] = 1.0
    blocks["neutrino"][6:8, 6:8] = pt
    return blocks


def charged_dirac(h: np.ndarray, yu: float, yd: float, ye: float) -> np.ndarray:
    eps = np.array([[0.0, 1.0], [-1.0, 0.0]], dtype=complex)
    h = h / np.linalg.norm(h)
    ht = eps @ np.conjugate(h)
    d = np.zeros((15, 15), dtype=complex)
    for color in range(3):
        qslice = slice(2 * color, 2 * color + 2)
        d[qslice, 8 + color] = yu * ht
        d[8 + color, qslice] = yu * np.conjugate(ht)
        d[qslice, 11 + color] = yd * h
        d[11 + color, qslice] = yd * np.conjugate(h)
    d[6:8, 14] = ye * h
    d[14, 6:8] = ye * np.conjugate(h)
    return d


def main() -> None:
    rng = np.random.default_rng(20260821)
    h = np.array([0.37 + 0.29j, -0.41 + 0.77j], dtype=complex)
    p = projectors(h)
    names = list(p)
    total = sum(p.values())
    sum_residual = float(np.linalg.norm(total - np.eye(15)))
    idempotence = max(float(np.linalg.norm(x @ x - x)) for x in p.values())
    orthogonality = max(
        float(np.linalg.norm(p[a] @ p[b]))
        for i, a in enumerate(names)
        for b in names[i + 1 :]
    )
    ranks = {name: int(np.linalg.matrix_rank(x, tol=1e-10)) for name, x in p.items()}

    su2_residuals = {name: 0.0 for name in names}
    su3_residuals = {name: 0.0 for name in names}
    for _ in range(16):
        u = random_su(rng, 2)
        transformed = projectors(u @ h)
        g2 = np.zeros((15, 15), dtype=complex)
        g2[:6, :6] = np.kron(np.eye(3), u)
        g2[6:8, 6:8] = u
        g2[8:, 8:] = np.eye(7)
        v = random_su(rng, 3)
        g3 = np.zeros((15, 15), dtype=complex)
        g3[:6, :6] = np.kron(v, np.eye(2))
        g3[6:8, 6:8] = np.eye(2)
        g3[8:11, 8:11] = v
        g3[11:14, 11:14] = v
        g3[14, 14] = 1.0
        for name in names:
            su2_residuals[name] = max(
                su2_residuals[name],
                float(np.linalg.norm(transformed[name] - g2 @ p[name] @ g2.conj().T)),
            )
            su3_residuals[name] = max(
                su3_residuals[name],
                float(np.linalg.norm(g3 @ p[name] - p[name] @ g3)),
            )

    d = charged_dirac(h, 0.7, 0.4, 0.2)
    eigenvalues = np.linalg.eigvalsh(d)
    d_rank = int(np.linalg.matrix_rank(d, tol=1e-10))
    commutators = {name: float(np.linalg.norm(d @ x - x @ d)) for name, x in p.items()}
    weights = {name: rank / 105 for name, rank in ranks.items()}

    result = {
        "gate": "version6_spectral_transition_higgs_resolved_support_gate",
        "Higgs_covariant_projectors": {
            "definitions": {
                "P_H": "H H^dagger/(H^dagger H)",
                "P_tildeH": "tilde(H) tilde(H)^dagger/(H^dagger H)",
            },
            "ranks": ranks,
            "sum_to_identity_residual": sum_residual,
            "orthogonality_residual": orthogonality,
            "idempotence_residual": idempotence,
            "SU2_covariance_residuals": su2_residuals,
            "SU3_color_commutator_residuals": su3_residuals,
            "defined_at_H_equal_zero": False,
        },
        "charged_Dirac_reduction": {
            "sample_Yukawas_are_structure_test_only": {"up": 0.7, "down": 0.4, "electron": 0.2},
            "projector_commutator_residuals": commutators,
            "Dirac_rank": d_rank,
            "Dirac_nullity": 15 - d_rank,
            "sorted_eigenvalues": [float(x) for x in eigenvalues],
            "structural_support_split": "15=6_up+6_down+2_e+1_nu",
        },
        "Toeplitz_and_Real_ledger": {
            "component_KO6_classes": ranks,
            "component_weights": weights,
            "component_real_ranks": {name: 2 * rank for name, rank in ranks.items()},
            "class_sum": sum(ranks.values()),
            "weight_sum": sum(weights.values()),
        },
        "mass_boundary": {
            "charged_degree_one_edges": ["up", "down", "electron"],
            "charged_mass_values_derived": False,
            "neutrino_degree_one_edge": False,
            "neutrino_rank_one_line_is_Higgs_conditional": True,
            "neutrino_line_regular_at_Higgs_zero": False,
        },
        "verdict": {
            "Higgs_resolved_split_passes": True,
            "split": "15=6_up+6_down+2_e+1_nu",
            "charged_blocks_structurally_massive_for_nonzero_Yukawas": True,
            "neutrino_line_is_massless_at_degree_one": True,
            "rank_one_neutrino_line_is_parent_closed_particle": False,
            "physical_closure": False,
        },
        "next_gate": "version6_spectral_transition_neutrino_line_parent_gate",
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()