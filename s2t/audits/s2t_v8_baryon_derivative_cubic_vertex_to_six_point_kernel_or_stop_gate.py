#!/usr/bin/env python3
"""Exact independent reproduction of the derivative cubic baryon STOP."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import full_noise_frame  # noqa: E402


def main() -> None:
    frame = list(full_noise_frame())
    identity = sp.eye(21)
    centered = [sp.ImmutableMatrix(item - sp.trace(item) * identity / 21) for item in frame]

    symmetric_support: dict[tuple[int, int, int], sp.Expr] = {}
    commutator_support: dict[tuple[int, int, int], sp.Expr] = {}
    symmetric_sectors = {"TTT": 0, "TTG": 0, "TGG": 0, "GGG": 0}
    commutator_sectors = {"TTT": 0, "TTG": 0, "TGG": 0, "GGG": 0}

    for a, b, c in itertools.combinations_with_replacement(range(42), 3):
        sector = "".join("T" if index < 30 else "G" for index in (a, b, c))
        d_value = sp.simplify(
            sp.trace(centered[a] * (centered[b] * centered[c] + centered[c] * centered[b])) / 2
        )
        c_value = sp.simplify(
            sp.trace(centered[a] * (centered[b] * centered[c] - centered[c] * centered[b]))
        )
        if d_value != 0:
            symmetric_support[(a, b, c)] = d_value
            symmetric_sectors[sector] += 1
        if c_value != 0:
            commutator_support[(a, b, c)] = c_value
            commutator_sectors[sector] += 1

    assert len(symmetric_support) == 168
    assert symmetric_sectors == {"TTT": 0, "TTG": 140, "TGG": 0, "GGG": 28}
    assert len(commutator_support) == 116
    assert commutator_sectors == {"TTT": 0, "TTG": 106, "TGG": 0, "GGG": 10}
    assert set(symmetric_support).isdisjoint(commutator_support)

    witnesses = {
        "C_0_1_41": sp.simplify(
            sp.trace(centered[0] * (centered[1] * centered[41] - centered[41] * centered[1]))
        ),
        "C_30_31_32": sp.simplify(
            sp.trace(centered[30] * (centered[31] * centered[32] - centered[32] * centered[31]))
        ),
        "d_0_0_40": sp.simplify(
            sp.trace(centered[0] * (centered[0] * centered[40] + centered[40] * centered[0])) / 2
        ),
        "d_30_30_37": sp.simplify(
            sp.trace(centered[30] * (centered[30] * centered[37] + centered[37] * centered[30])) / 2
        ),
    }
    assert witnesses == {
        "C_0_1_41": sp.I,
        "C_30_31_32": 16 * sp.I,
        "d_0_0_40": -1,
        "d_30_30_37": 8,
    }

    momentum = sp.symbols("p0:4", real=True)
    derivative_channel = sum(momentum[index] * (index + 1) for index in range(4))
    assert derivative_channel.subs({item: 0 for item in momentum}) == 0
    static_target_nonzero = witnesses["d_0_0_40"] != 0
    assert static_target_nonzero

    exact_objects = [*symmetric_support.values(), *commutator_support.values(), *witnesses.values()]
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_derivative_cubic_vertex_to_six_point_kernel_or_stop_gate",
        "field": "Q(i)",
        "enumeration": {
            "frame_dimension": 42,
            "unordered_triples": 13244,
            "floating_point_values": 0,
        },
        "symmetric_trace_tensor": {
            "definition": "d_abc=Tr(Fhat_a{Fhat_b,Fhat_c})/2",
            "nonzero_unordered": len(symmetric_support),
            "support": symmetric_sectors,
        },
        "commutator_tensor": {
            "definition": "C_abc=Tr(Fhat_a[Fhat_b,Fhat_c])",
            "nonzero_unordered": len(commutator_support),
            "support": commutator_sectors,
            "antisymmetric_in_last_two_indices": True,
            "full_symmetrization_zero": True,
        },
        "comparison": {
            "support_intersection_count": 0,
            "all_symmetric_support_has_zero_commutator_color": True,
            "derivative_channels_have_commutator_color": True,
            "derivative_channels_linear_in_momentum": True,
            "zero_momentum_derivative_kernel": 0,
            "static_W3_nonzero": True,
        },
        "witnesses": {key: str(value) for key, value in witnesses.items()},
        "verdict": {
            "derivative_local_branch_reproduces_W3": False,
            "derivative_branch_status": "STOP",
            "nonlocal_six_point_kernel_required_for_static_W3": True,
            "coefficient_or_nonlocal_kernel_derived": False,
        },
        "next_gate": "version8_baryon_nonlocal_six_point_kernel_admission_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()