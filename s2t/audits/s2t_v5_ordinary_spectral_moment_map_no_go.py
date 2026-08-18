#!/usr/bin/env python3
"""Exact audit of spectral blindness to an oriented Gram decomposition."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_ordinary_spectral_moment_map_no_go_results.json"

t, s = sp.symbols("t s", real=True, positive=True)
lam = sp.Symbol("lambda")
x = sp.sqrt(t * s)
y = sp.sqrt((1 - t) * s)
D = sp.Matrix([[0, x, 0], [x, 0, y], [0, y, 0]])

characteristic_polynomial = sp.factor(D.charpoly(lam).as_expr())
assert sp.simplify(characteristic_polynomial - lam * (lam**2 - s)) == 0

moments = {}
supermoments = {}
grading = sp.diag(1, -1, 1)
for power in range(1, 7):
    moment = sp.simplify(sp.trace(D ** (2 * power)))
    supermoment = sp.simplify(sp.trace(grading * D ** (2 * power)))
    assert sp.simplify(moment - 2 * s**power) == 0
    assert supermoment == 0
    moments[str(2 * power)] = str(moment)
    supermoments[str(2 * power)] = str(supermoment)

moment_map_norm = sp.expand((t * s - (1 - t) * s) ** 2)
assert sp.simplify(moment_map_norm - (2 * t - 1) ** 2 * s**2) == 0

S = sp.diag(1, 2)
matrix_family = []
for value in (sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4)):
    A = value * S
    B = (1 - value) * S
    spectral_moments = [sp.trace((A + B) ** k) for k in range(1, 5)]
    mu_norm = sp.trace((A - B) ** 2)
    matrix_family.append(
        {
            "t": str(value),
            "spectral_moments": [str(item) for item in spectral_moments],
            "moment_map_norm": str(mu_norm),
        }
    )

assert len({tuple(item["spectral_moments"]) for item in matrix_family}) == 1
assert len({item["moment_map_norm"] for item in matrix_family}) == 2

result = {
    "date": "2026-08-15",
    "gate": "version5_ordinary_spectral_moment_map_no_go",
    "scalar_family": {
        "Dirac_characteristic_polynomial": str(characteristic_polynomial),
        "even_moments": moments,
        "supermoments": supermoments,
        "all_spectral_data_independent_of_t": True,
        "moment_map_norm": str(moment_map_norm),
        "moment_map_depends_on_t": True,
    },
    "matrix_family": matrix_family,
    "general_identity": {
        "middle_gram": "A+B",
        "moment_map": "A-B",
        "trace_D4": "2 Tr(A+B)^2",
        "moment_map_square": "Tr(A-B)^2",
        "ordinary_spectral_function_recovers_difference": False,
    },
    "supertrace": {
        "positive_even_powers_zero": True,
        "general_role": "index times f(0)",
        "moment_map_potential": False,
    },
    "scope": {
        "closed": [
            "ordinary Tr f(D^2)",
            "functions of ordinary spectral moments",
            "singular-value determinant functionals",
            "unprojected graded supertrace",
        ],
        "not_closed": [
            "relative or conditionally projected curvature",
            "auxiliary moment-map fields",
            "twisted or derived calculi",
            "BV-BFV structures",
            "relative modular functionals",
            "nonlocal boundary actions",
        ],
    },
    "verdict": {
        "spectral_blindness_theorem": True,
        "quartic_cross_sign_no_go": True,
        "supertrace_rescue": False,
        "ordinary_one_trace_moment_map_origin": "closed",
        "nonordinary_architectures": "undecided",
        "physical_closure": False,
    },
    "next_gate": "version5_nonordinary_architecture_fork_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))