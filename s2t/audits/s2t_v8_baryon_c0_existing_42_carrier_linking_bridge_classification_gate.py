#!/usr/bin/env python3
"""Exact classification of a c0 linking bridge inside the current 42-frame."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_trace_frame import full_noise_frame  # noqa: E402
from s2t.proofdsl.examples.version8_gauge_twirl_kraus import _endpoint_gauge_generators  # noqa: E402


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_linking_algebra_offdiagonal_bridge_admission_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["verdict"]["minimal_linking_architecture_admitted"]
    assert previous["next_gate"] == "version8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate"

    frame = tuple(full_noise_frame())
    generators = tuple(_endpoint_gauge_generators())
    hypercharge = generators[-1]
    assert len(frame) == 42
    assert all(item.shape == (21, 21) for item in frame)
    assert hypercharge.rank() == 21
    assert len(hypercharge.nullspace()) == 0

    p_aux = sp.zeros(22)
    p_aux[21, 21] = 1
    embedded = []
    for item in frame:
        extended = sp.zeros(22)
        extended[:21, :21] = item
        extended = sp.ImmutableMatrix(extended)
        embedded.append(extended)
        assert extended * p_aux == sp.zeros(22)
        assert p_aux * extended == sp.zeros(22)
        assert p_aux * extended.H * extended * p_aux == sp.zeros(22)

    diagonal_y = [sp.simplify(hypercharge[i, i]) for i in range(21)]
    charged_minus_one = [i for i, value in enumerate(diagonal_y) if value == -1]
    assert len(charged_minus_one) == 3
    for index in charged_minus_one:
        vector = sp.eye(21)[:, index]
        assert all(generator * vector == sp.zeros(21, 1) for generator in generators[:-1])
        assert hypercharge * vector == -vector

    exact_objects = list(hypercharge) + [entry for item in embedded for entry in item]
    assert not any(
        atom.is_Float for obj in exact_objects for atom in sp.preorder_traversal(obj)
    )

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_existing_42_carrier_linking_bridge_classification_gate",
        "current_endpoint": {
            "dimension": 21,
            "neutral_trivial_irrep_multiplicity": 0,
            "hypercharge_rank": 21,
            "hypercharge_nullity": 0,
        },
        "current_frame": {
            "real_dimension": 42,
            "ambient_algebra": "End(H21)",
            "zero_extended_to_H22": True,
            "all_basis_elements_annihilate_auxiliary_projector": True,
            "imprimitivity_bridge_count_in_span": 0,
        },
        "nearest_wrong_type_channels": {
            "charged_singlet_minus_one_multiplicity": 3,
            "charged_singlet_unique": False,
            "old_real_selected_channel_rank": 3,
            "old_real_selected_channel_type": "colored u_R triplet",
        },
        "verdict": {
            "required_neutral_linking_bridge_in_existing_42_carrier": False,
            "linear_or_algebraic_closure_can_create_external_endpoint": False,
            "new_neutral_endpoint_state_required": True,
            "new_off_diagonal_arrow_required": True,
        },
        "next_gate": "version8_baryon_c0_minimal_neutral_endpoint_extension_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()