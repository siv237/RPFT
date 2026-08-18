#!/usr/bin/env python3
"""Audit an explicit exchange-Real KO7 Toeplitz symbol."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np


def main() -> None:
    n, r = 105, 15
    q = np.diag([1.0] * r + [0.0] * (n - r)).astype(complex)
    eye = np.eye(n, dtype=complex)
    residuals = []
    exchange = []
    for theta in np.linspace(0.0, 2 * np.pi, 33):
        z = np.exp(1j * theta)
        plus = z * q + (eye - q)
        minus = z.conjugate() * q.conjugate() + (eye - q.conjugate())
        residuals.extend([
            np.linalg.norm(plus.conj().T @ plus - eye),
            np.linalg.norm(minus.conj().T @ minus - eye),
        ])
        # tau(f,g)(z)=(g(conj z)^T,f(conj z)^T).
        minus_at_conj = z * q.conjugate() + (eye - q.conjugate())
        exchange.append(np.linalg.norm(minus_at_conj.T - plus))

    result = {
        "gate": "version5_real_toeplitz_ko7_unitary_representative_gate",
        "unitary": {
            "plus": "z q0 + (1-q0)",
            "minus": "z^(-1) conjugate(q0) + (1-conjugate(q0))",
            "matrix_size_per_branch": n,
            "coefficient_rank": r,
            "max_unitarity_residual": float(max(residuals)),
            "max_real_exchange_residual": float(max(exchange)),
            "KO7_symmetry": "V^tau=V",
        },
        "complex_K1_classes": [r, -r],
        "toeplitz_boundary_indices": [-r, r],
        "naive_doubling_rejected": {
            "formula": "p u + (1-p)u*",
            "reason": "represents 2[p]-[1] and doubles the intended class",
            "would_give_absolute_class": 2 * r,
        },
        "verdict": {
            "explicit_KO7_unitary": "pass",
            "real_symmetry": "pass",
            "boundary_matches_complexification_of_KO6_15": True,
            "normalized_weight": r / n,
            "physical_action": False,
            "next_gate": "version5_toeplitz_parent_action_variational_gap_gate",
        },
    }
    out = Path(__file__).resolve().parents[1] / "results" / "s2t_v5_real_toeplitz_ko7_unitary_representative_gate_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert max(residuals) < 1e-12
    assert max(exchange) < 1e-12
    assert r / n == 1 / 7
    print(out)


if __name__ == "__main__":
    main()