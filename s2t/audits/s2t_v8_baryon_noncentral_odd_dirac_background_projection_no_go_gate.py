#!/usr/bin/env python3
"""Exact parity no-go for odd finite-Dirac cubic projections."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_noncentral_odd_dirac_background_projection_no_go_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_fixed_algebra import physical_incidence  # noqa: E402
from s2t.proofdsl.examples.version8_full_noise_trace_frame import (  # noqa: E402
    full_noise_frame,
)
from s2t.proofdsl.examples.version8_gauge_twirl_kraus import _dirac_jump  # noqa: E402


def symmetric_trace_with_background(
    background: sp.ImmutableMatrix,
    frame: list[sp.ImmutableMatrix],
    indices: tuple[int, int, int],
) -> sp.Expr:
    permutations = set(itertools.permutations(indices))
    return sp.simplify(
        sum(
            sp.trace(background * frame[a] * frame[b] * frame[c])
            for a, b, c in permutations
        )
        / len(permutations)
    )


def main() -> None:
    frame = list(full_noise_frame())
    identity = sp.eye(21)
    grading = sp.diag(*([1] * 11 + [-1] * 10))
    centered = [
        sp.ImmutableMatrix(item - sp.trace(item) * identity / 21) for item in frame
    ]
    parities = [1] * 30 + [0] * 12

    for item, parity in zip(centered, parities, strict=True):
        assert grading * item * grading == (-1) ** parity * item

    background = sp.ImmutableMatrix(_dirac_jump(physical_incidence()))
    assert grading * background * grading == -background
    assert sp.trace(background) == 0

    trace_support = {"TTT": 0, "TTG": 0, "TGG": 0, "GGG": 0}
    odd_background_support = {"TTT": 0, "TTG": 0, "TGG": 0, "GGG": 0}
    samples: list[dict[str, object]] = []

    for a in range(42):
        for b in range(a, 42):
            for c in range(b, 42):
                indices = (a, b, c)
                sector = "".join("T" if index < 30 else "G" for index in indices)
                trace_value = sp.simplify(
                    sp.trace(
                        centered[a]
                        * (centered[b] * centered[c] + centered[c] * centered[b])
                    )
                    / 2
                )
                background_value = symmetric_trace_with_background(
                    background, centered, indices
                )
                if trace_value != 0:
                    trace_support[sector] += 1
                if background_value != 0:
                    odd_background_support[sector] += 1
                    if len(samples) < 12:
                        samples.append(
                            {
                                "indices_zero_based": list(indices),
                                "value": str(background_value),
                            }
                        )

                transfer_parity = sum(index < 30 for index in indices) % 2
                if transfer_parity == 0:
                    # An odd background paired with an even finite product has
                    # an odd product and therefore zero ordinary trace.
                    assert background_value == 0

    assert trace_support == {"TTT": 0, "TTG": 140, "TGG": 0, "GGG": 28}
    assert odd_background_support == {"TTT": 130, "TTG": 0, "TGG": 35, "GGG": 0}

    exact_objects = [*background]
    assert not any(
        atom.is_Float
        for obj in exact_objects
        for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_noncentral_odd_dirac_background_projection_no_go_gate",
        "field": "Q",
        "finite_grading": {
            "definition": "Gamma=I_11 direct_sum (-I_10)",
            "transfer_directions_odd": 30,
            "gauge_directions_even": 12,
            "physical_incidence_background_odd": True,
        },
        "canonical_trace_tensor": {
            "support_unordered": trace_support,
            "finite_parity_of_nonzero_support": "even",
        },
        "odd_background_tensor": {
            "definition": "c_D(a,b,c)=Sym Tr(D Fhat_a Fhat_b Fhat_c)",
            "physical_incidence_support_unordered": odd_background_support,
            "finite_parity_of_nonzero_support": "odd",
            "sample": samples,
        },
        "general_parity_no_go": {
            "identity": "Tr(D_odd S_even)=0",
            "odd_background_can_reproduce_nonzero_d_abc": False,
            "supports_disjoint": True,
            "independent_of_background_entries": True,
        },
        "spacetime_supercurvature_boundary": {
            "total_odd_connection": "d+A_even^(1)+Phi_odd^(0)",
            "curvature": "F_A+D_A Phi+Phi^2",
            "TTG_and_GGG_cubic_vertices_require_derivatives": True,
            "constant_zero_momentum_cubic_vertex": 0,
            "equal_to_static_lambda_3_W3": False,
        },
        "verdict": {
            "central_even_shift_rejected": True,
            "noncentral_odd_background_rescue_rejected": True,
            "standard_local_supercurvature_generates_static_W3": False,
            "physical_six_point_kernel_derived": False,
            "next_gate": "derivative_cubic_vertex_to_six_point_kernel_or_stop",
        },
    }

    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()