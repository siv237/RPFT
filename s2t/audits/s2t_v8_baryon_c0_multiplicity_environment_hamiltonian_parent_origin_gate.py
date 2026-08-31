#!/usr/bin/env python3
"""Exact parent-origin audit for the multiplicity-environment Hamiltonian."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate_results.json"


def main() -> None:
    previous = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_multiplicity_environment_hamiltonian_minimal_data_gate_results.json").read_text(encoding="utf-8")
    )
    endpoint = json.loads(
        (ROOT / "s2t/results/s2t_v8_baryon_c0_extended_endpoint_bimodule_weight_origin_gate_results.json").read_text(encoding="utf-8")
    )
    assert previous["minimal_data_layers"]["derived_layers"] == 0
    assert previous["next_gate"] == "version8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate"
    assert endpoint["full_hom_closure"]["connector_metric"] == "(2/5) I3"

    old_hessian = sp.zeros(3)
    m5_trace = sp.Rational(2, 5) * sp.eye(3)
    kossakowski = sp.eye(3)
    assert old_hessian.rank() == 0
    assert m5_trace.rank() == kossakowski.rank() == 3

    witness_a = tuple(map(sp.Rational, ("1/10", "1/5", "1/2", "1/10")))
    witness_b = tuple(map(sp.Rational, ("1/2", "1/10", "1/5", "1/10")))

    def local_hamiltonian(weights: tuple[sp.Rational, ...]) -> sp.Matrix:
        p0, p1, p2, q = weights
        assert p0 + p1 + p2 + 2 * q == 1
        return sp.diag(p0 + q, p1 + q, p2 + q)

    h_a = local_hamiltonian(witness_a)
    h_b = local_hamiltonian(witness_b)
    assert h_a.diagonal()[0] < h_a.diagonal()[1] < h_a.diagonal()[2]
    assert h_b.diagonal()[1] < h_b.diagonal()[2] < h_b.diagonal()[0]

    r4 = sp.Matrix(
        [
            [sp.Rational(27, 2), -2, sp.Rational(3, 2)],
            [-2, sp.Rational(35, 2), sp.Rational(-5, 2)],
            [sp.Rational(3, 2), sp.Rational(-5, 2), 17],
        ]
    )
    lam = sp.symbols("lambda")
    characteristic = sp.factor(r4.charpoly(lam).as_expr())
    discriminant = sp.factor(sp.discriminant(characteristic, lam))
    expected_characteristic = sp.Rational(1, 4) * (
        4 * lam**3 - 192 * lam**2 + 3003 * lam - 15358
    )
    assert sp.simplify(characteristic - expected_characteristic) == 0
    assert discriminant == sp.Rational(164241, 16) > 0

    projectors = tuple(sp.diag(*[1 if i == j else 0 for i in range(3)]) for j in range(3))
    commutators = tuple(r4 * projector - projector * r4 for projector in projectors)
    commutator_norm = sp.simplify(sum(sp.trace(item.T * item) for item in commutators))
    assert commutator_norm == 50
    assert all(item != sp.zeros(3) for item in commutators)

    t_entries = sp.symbols("t0:9", real=True)
    transport = sp.Matrix(3, 3, t_entries)
    transported_hamiltonian = transport * r4 * transport.T
    assert len(t_entries) == 9
    assert sp.simplify(transported_hamiltonian - transported_hamiltonian.T) == sp.zeros(3)

    candidates = {
        "old_parent_restriction": {"anisotropic": False, "selected": False},
        "M5_unique_trace": {"anisotropic": False, "selected": False},
        "full_kossakowski_covariance": {"anisotropic": False, "selected": False},
        "local_trace_simplex": {"anisotropic": True, "selected": False},
        "family_R4_plus": {
            "anisotropic": True,
            "selected": False,
            "typed_carrier_map_present": False,
            "endpoint_diagonal": False,
        },
    }
    assert sum(item["selected"] for item in candidates.values()) == 0

    exact_objects = [old_hessian, m5_trace, kossakowski, h_a, h_b, r4, characteristic, discriminant, commutator_norm, transported_hamiltonian]
    assert not any(obj.atoms(sp.Float) for obj in exact_objects)

    result = {
        "date": "2026-08-30",
        "gate": "version8_baryon_c0_multiplicity_environment_hamiltonian_parent_origin_gate",
        "intrinsic_sources": {
            "old_parent_hessian": "0_3",
            "M5_trace_metric": "(2/5) I3",
            "full_kossakowski_covariance": "I3",
            "intrinsic_anisotropic_source_found": False,
        },
        "local_trace_family": {
            "dimension_after_normalization": 3,
            "witness_A_hamiltonian": [[str(x) for x in h_a.diagonal()]],
            "witness_B_hamiltonian": [[str(x) for x in h_b.diagonal()]],
            "different_ground_coordinates": True,
            "weights_selected": False,
        },
        "family_R4_near_miss": {
            "matrix": [[str(item) for item in row] for row in r4.tolist()],
            "characteristic_polynomial": "(4 lambda^3-192 lambda^2+3003 lambda-15358)/4",
            "discriminant": "164241/16",
            "simple_spectrum": True,
            "endpoint_projector_commutator_norm_squared_sum": "50",
            "direct_endpoint_compatible": False,
            "typed_family_to_environment_map_present": False,
        },
        "transport_map": {
            "formal_equivariant_hom": "M3(R)",
            "real_dimension": 9,
            "isometric_subfamily": "O(3)",
            "canonical_element_selected": False,
            "transported_hamiltonian": "T R4_plus T^T",
            "absolute_energy_scale_supplied": False,
        },
        "candidate_ledger": candidates,
        "verdict": {
            "candidate_count": 5,
            "derived_parent_origins": 0,
            "anisotropic_hamiltonian_derived": False,
            "direction_projector_derived": False,
            "absolute_gap_derived": False,
            "single_c0_map_derived": False,
        },
        "next_gate": "version8_baryon_c0_family_to_multiplicity_intertwiner_admission_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()