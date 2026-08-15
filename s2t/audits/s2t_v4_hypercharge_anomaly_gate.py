import json

import sympy as sp


q, u, d, ell, e, n, h = sp.symbols("q u d ell e n h")

yukawa_solution = {u: q + h, d: q - h, e: ell - h, n: ell + h}
anomalies = {
    "su3_squared_u1": 2 * q - u - d,
    "su2_squared_u1": 3 * q + ell,
    "gravity_squared_u1": 6 * q - 3 * u - 3 * d + 2 * ell - e - n,
    "u1_cubed": 6 * q**3 - 3 * u**3 - 3 * d**3 + 2 * ell**3 - e**3 - n**3,
}
reduced = {
    name: sp.factor(expr.subs(yukawa_solution).subs(ell, -3 * q))
    for name, expr in anomalies.items()
}
normalized_solution = {
    "Q_L": sp.Rational(1, 6),
    "u_R": sp.Rational(2, 3),
    "d_R": sp.Rational(-1, 3),
    "L_L": sp.Rational(-1, 2),
    "e_R": sp.Integer(-1),
    "nu_R": sp.Integer(0),
    "H": sp.Rational(1, 2),
}
target_substitution = dict(zip((q, u, d, ell, e, n, h), normalized_solution.values()))
target_anomalies = {
    name: sp.simplify(expr.subs(target_substitution))
    for name, expr in anomalies.items()
}
without_nu_gravity = sp.factor(
    (6 * q - 3 * u - 3 * d + 2 * ell - e)
    .subs({u: q + h, d: q - h, e: ell - h})
    .subs(ell, -3 * q)
)
without_nu_cubic = sp.factor(
    (6 * q**3 - 3 * u**3 - 3 * d**3 + 2 * ell**3 - e**3)
    .subs({u: q + h, d: q - h, e: ell - h})
    .subs(ell, -3 * q)
)

result = {
    "gate": "version4_hypercharge_anomaly",
    "anomalies_after_yukawa_and_su2": {key: str(value) for key, value in reduced.items()},
    "with_right_neutrino": {
        "continuous_freedom": "q and h remain free before generator normalization",
        "interpretation": "hypercharge can mix with anomaly-free B-L",
        "sterile_condition": "n=ell+h=0",
        "sterile_solution": "h=3*q",
    },
    "without_right_neutrino": {
        "gravity_anomaly": str(without_nu_gravity),
        "cubic_anomaly": str(without_nu_cubic),
        "forced_relation": "h=3*q",
    },
    "normalized_hypercharges": {key: str(value) for key, value in normalized_solution.items()},
    "target_anomalies": {key: str(value) for key, value in target_anomalies.items()},
    "pure_su3_anomaly": "2-1-1=0",
    "witten_su2_doublets": 4,
    "passes_local_anomalies": all(value == 0 for value in target_anomalies.values()),
    "passes_witten_su2": True,
    "status": "conditional derivation up to overall U(1) normalization",
}

with open("s2t_v4_hypercharge_anomaly_gate_results.json", "w", encoding="utf-8") as handle:
    json.dump(result, handle, ensure_ascii=False, indent=2)

print(json.dumps(result, ensure_ascii=False, indent=2))