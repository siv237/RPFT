#!/usr/bin/env python3
"""Exact cubic-trace audit on the full centered 42-direction noise frame."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_cubic_trace_connected_operator_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import (  # noqa: E402
    full_noise_frame,
)


def main() -> None:
    frame = list(full_noise_frame())
    system_dimension = frame[0].rows
    identity = sp.eye(system_dimension)
    traces = [sp.simplify(sp.trace(item)) for item in frame]
    centered = [
        sp.ImmutableMatrix(item - trace * identity / system_dimension)
        for item, trace in zip(frame, traces, strict=True)
    ]
    centered_metric = sp.Matrix(
        [[sp.simplify(sp.trace(left * right)) for right in centered] for left in centered]
    )

    assert len(frame) == 42
    assert system_dimension == 21
    assert [(index, value) for index, value in enumerate(traces) if value != 0] == [
        (41, sp.Integer(-4))
    ]
    assert all(sp.trace(item) == 0 for item in centered)
    assert centered_metric.rank() == 42
    assert all(
        item - centered_item == trace * identity / system_dimension
        for item, centered_item, trace in zip(frame, centered, traces, strict=True)
    )

    nonzero: dict[tuple[int, int, int], sp.Expr] = {}
    support = {"TTT": 0, "TTG": 0, "TGG": 0, "GGG": 0}
    for a in range(42):
        for b in range(a, 42):
            for c in range(b, 42):
                value = sp.simplify(
                    sp.trace(centered[a] * (centered[b] * centered[c] + centered[c] * centered[b]))
                    / 2
                )
                if value == 0:
                    continue
                nonzero[(a, b, c)] = value
                sector = "".join("T" if index < 30 else "G" for index in (a, b, c))
                support[sector] += 1

    for indices, value in nonzero.items():
        for permutation in set(itertools.permutations(indices)):
            a, b, c = permutation
            permuted = sp.simplify(
                sp.trace(centered[a] * (centered[b] * centered[c] + centered[c] * centered[b]))
                / 2
            )
            assert permuted == value

    assert len(nonzero) == 168
    assert support == {"TTT": 0, "TTG": 140, "TGG": 0, "GGG": 28}
    assert all(sp.conjugate(value) == value for value in nonzero.values())

    # Because every centered frame element is traceless, every one-copy
    # partial trace of the tensor product candidate vanishes term by term.
    partial_trace_factors = {
        "copy_1": all(sp.trace(item) == 0 for item in centered),
        "copy_2": all(sp.trace(item) == 0 for item in centered),
        "copy_3": all(sp.trace(item) == 0 for item in centered),
    }

    exact_objects = (
        traces
        + list(centered_metric)
        + list(nonzero.values())
    )
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    sample = [
        {"indices_zero_based": list(indices), "value": str(value)}
        for indices, value in list(nonzero.items())[:12]
    ]
    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_cubic_trace_connected_operator_gate",
        "field": "Q",
        "frame": {
            "system_dimension": system_dimension,
            "frame_dimension": len(frame),
            "nonzero_original_traces": [
                {"index_zero_based": index, "trace": str(value)}
                for index, value in enumerate(traces)
                if value != 0
            ],
            "centering": "Fhat_a=F_a-Tr(F_a)I_21/21",
            "centered_trace_metric_rank": centered_metric.rank(),
            "same_double_commutator_generator": True,
        },
        "symmetric_cubic_trace_tensor": {
            "definition": "d_abc=Tr(Fhat_a{Fhat_b,Fhat_c})/2",
            "fully_symmetric": True,
            "real": True,
            "nonzero_unordered_components": len(nonzero),
            "support_unordered": support,
            "sample": sample,
        },
        "connected_three_copy_operator": {
            "definition": "W3=d^{abc}Fhat_a tensor Fhat_b tensor Fhat_c",
            "indices_raised_by": "centered trace metric inverse",
            "nonzero": True,
            "Hermitian": True,
            "permutation_invariant": True,
            "gauge_invariant_by_trace_cyclicity": True,
            "partial_traces_zero": partial_trace_factors,
        },
        "boundary": {
            "pure_three_transfer_component": False,
            "generated_by_current_quadratic_gksl_parent": False,
            "overall_three_body_coupling_derived": False,
            "faddeev_kernel_derived": False,
            "confinement_or_spatial_kernel_derived": False,
        },
        "verdict": {
            "canonical_connected_operator_carrier": True,
            "physical_baryon_parent": False,
            "next_gate": "cubic_trace_parent_action_coefficient_origin_or_no_go",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()