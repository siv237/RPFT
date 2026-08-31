#!/usr/bin/env python3
"""Exact minimal neutral endpoint and 45-frame extension audit."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_minimal_neutral_endpoint_extension_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import (  # noqa: E402
    build_certificate as frame_certificate,
    full_noise_frame,
)
from s2t.proofdsl.examples.version8_gauge_twirl_kraus import _endpoint_gauge_generators  # noqa: E402


def extend(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    result = sp.zeros(23)
    result[:21, :21] = matrix
    return sp.ImmutableMatrix(result)


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["new_neutral_endpoint_state_required"]
    assert previous["next_gate"] == "version8_baryon_c0_minimal_neutral_endpoint_extension_gate"

    ps = sp.zeros(23); ps[21, 21] = 1
    pa = sp.zeros(23); pa[22, 22] = 1
    e = sp.zeros(23); e[21, 22] = 1
    ps, pa, e = map(sp.ImmutableMatrix, (ps, pa, e))
    x = sp.ImmutableMatrix(e + e.H)
    y = sp.ImmutableMatrix(-sp.I * (e - e.H))
    h = sp.ImmutableMatrix(ps - pa)
    assert e * e.H == ps and e.H * e == pa

    gamma21 = sp.diag(*([-1] * 11 + [1] * 10))
    gamma23 = sp.ImmutableMatrix(sp.diag(gamma21, 1, -1))
    assert gamma23 * x + x * gamma23 == sp.zeros(23)
    assert gamma23 * y + y * gamma23 == sp.zeros(23)

    generators = tuple(extend(item) for item in _endpoint_gauge_generators())
    assert all(g * x - x * g == sp.zeros(23) for g in generators)
    assert all(g * y - y * g == sp.zeros(23) for g in generators)
    assert sp.conjugate(x) == x
    assert sp.conjugate(y) == -y

    assert x * y - y * x == 2 * sp.I * h
    assert h * x - x * h == 2 * sp.I * y
    assert h * y - y * h == -2 * sp.I * x

    old = tuple(extend(item) for item in full_noise_frame())
    extended_frame = old + (x, y, h)
    flattened = sp.Matrix.hstack(*[sp.Matrix(list(item)) for item in extended_frame])
    assert flattened.rank() == 45

    old_metric = sp.Matrix(frame_certificate().trace_metric)
    new_metric = sp.Matrix(
        [[sp.simplify(sp.trace(left.H * right)) for right in extended_frame] for left in extended_frame]
    )
    assert new_metric[:42, :42] == old_metric
    assert new_metric[:42, 42:] == sp.zeros(42, 3)
    assert new_metric[42:, :42] == sp.zeros(3, 42)
    assert new_metric[42:, 42:] == 2 * sp.eye(3)
    assert new_metric.rank() == 45

    exact_objects = [*gamma23, *x, *y, *h, *flattened, *new_metric]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_minimal_neutral_endpoint_extension_gate",
        "endpoint_extension": {
            "old_dimension": 21,
            "new_neutral_complex_states": 2,
            "new_dimension": 23,
            "minimal_by_two_orthogonal_rank_one_corners": True,
        },
        "bridge": {
            "E": "|s0><a0|",
            "Hermitian_directions": ["X=E+E*", "Y=-i(E-E*)", "H=P_s-P_a"],
            "odd_XY": True,
            "gauge_neutral_XY": True,
            "real_span_closed": True,
            "imprimitivity": True,
        },
        "lie_closure": {
            "relations": ["[X,Y]=2iH", "[H,X]=2iY", "[H,Y]=-2iX"],
            "new_real_dimension": 3,
        },
        "extended_frame": {
            "old_rank": 42,
            "new_rank": 45,
            "trace_metric": "K45=K42 direct_sum 2I3",
            "trace_metric_rank": 45,
        },
        "conditional_selector": {
            "kappa": 1,
            "r_star": 4,
            "c0": 4,
            "physical_origin_of_new_states": False,
        },
        "verdict": {
            "minimal_neutral_endpoint_extension_admitted": True,
            "minimal_state_increment": 2,
            "minimal_gauge_closed_frame_increment": 3,
            "physical_extended_parent_derived": False,
        },
        "next_gate": "version8_baryon_c0_extended_45_frame_fixed_algebra_and_dynamics_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()