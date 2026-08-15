#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

vx, vc = sp.pi**2, 2 * sp.pi
vk = sp.simplify(vx * vc)
nx, nc = sp.simplify(vk / vc), sp.simplify(vk / vx)
target = sp.simplify(nx + nc)
double_readout = sp.simplify(4 * target)

results = {
    "date": "2026-08-09",
    "status": "conditional_measure_pass_module_multiplicity_open",
    "factor_norms": [str(nx), str(nc)],
    "direct_sum_norm": str(target),
    "single_field_double_readout": str(double_readout),
    "factor_weights_free": False,
    "module_origin_derived": False,
    "next_gate": "finite algebra or superconnection",
}
assert nx == sp.pi**2
assert nc == 2 * sp.pi
Path("s2t_v3_conditional_expectation_results.json").write_text(
    json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)