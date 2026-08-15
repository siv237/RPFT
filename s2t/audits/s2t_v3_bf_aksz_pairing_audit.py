#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

level, polarization = sp.symbols("level polarization", positive=True)
omega = level * sp.Matrix([[0, 1], [-1, 0]])
J = sp.Matrix([[0, -1 / polarization], [polarization, 0]])
metric = sp.simplify(omega * J)
v = sp.Matrix(sp.symbols("v0:2", real=True))

results = {
    "date": "2026-08-09",
    "status": "pure_bf_aksz_pairing_no_go",
    "self_pairing": str((v.T * omega * v)[0]),
    "J_squared": str(sp.simplify(J**2)),
    "metric": str(metric),
    "polarization_fixed_by_level": False,
    "K_closed": True,
    "next_gate": "conditional expectations",
}
assert sp.simplify((v.T * omega * v)[0]) == 0
assert metric == level * sp.diag(polarization, 1 / polarization)
Path("s2t_v3_bf_aksz_pairing_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)