#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

t = sp.symbols("t", real=True)
first_trace = sp.Rational(1, 45)
second_trace = sp.Rational(1, 4725)
checks = []
for count in range(1, 7):
    couplings = list(range(1, count + 1))
    matrix = sp.Matrix([
        [sp.Integer(coupling) ** power for coupling in couplings]
        for power in range(2, count + 2)
    ])
    checks.append({
        "species_count": count,
        "determinant": str(sp.factor(matrix.det())),
        "full_rank": matrix.rank() == count,
    })
results = {
    "status": "finite_gaussian_BV_periodic_singlet_cannot_generate_an_exact_nonzero_linear_primitive",
    "date": "2026-08-12",
    "periodic_tower": {
        "first_trace": "2*zeta(4)/pi^4=1/45",
        "second_trace": "2*zeta(8)/pi^8=1/4725",
        "bosonic_series": str(first_trace*t-second_trace*t**2/2)+"+O(t^3)",
        "fermionic_series": str(-first_trace*t+second_trace*t**2/2)+"+O(t^3)",
        "target_up_to_constant": str(-t/45),
    },
    "finite_BV_moment_theorem": {
        "condition": "sum_j a_j lambda_j^k=0 for every k>=2",
        "vandermonde_checks": checks,
        "conclusion": "finite distinct nonzero couplings force all net weights and the linear moment to vanish",
    },
    "reopening": "Gamma_zeta=-t*pi^(-4)*Tr'(Delta_per^(-2))=-t/45",
}
assert all(row["full_rank"] for row in checks)
Path("s2t_v4_periodic_singlet_bv_embedding_gate_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2)+"\n", encoding="utf-8"
)
print(json.dumps(results, ensure_ascii=False, indent=2))