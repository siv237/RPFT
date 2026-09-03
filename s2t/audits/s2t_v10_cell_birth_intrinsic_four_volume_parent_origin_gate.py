#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp

from s2t.proofdsl.examples.version10_cell_birth_intrinsic_four_volume_parent_origin import (
    SPEC,
    build_certificate,
)
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_intrinsic_four_volume_parent_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_cell_birth_clock_energy_geometric_anchor_candidate_audit_gate_results.json").read_text())
    gate = "version10_cell_birth_intrinsic_four_volume_parent_origin_gate"
    assert predecessor["next_gate"] == gate
    assert SPEC.identifier == gate
    verified = verify_gate(SPEC)
    certificate = build_certificate()
    assert certificate.cell_volume == sp.symbols("ell_cell", positive=True) ** 4
    assert certificate.normalized_shape == sp.eye(4)
    assert certificate.common_hessian.rank() == 3
    assert certificate.common_hessian.nullspace() == [sp.Matrix([0, 0, -1, 1])]
    assert sum(certificate.architecture) == 8
    assert sum(certificate.relative_origin) == 3
    assert sum(certificate.physical_ledger) == 0

    result = {
        "date": "2026-09-01",
        "gate": gate,
        "predecessor": predecessor["gate"],
        "intrinsic_cell_geometry": {
            "gram": "G_cell=ell_cell^2*I_4",
            "gram_determinant": "ell_cell^8",
            "four_volume": "v_cell=sqrt(det(G_cell))=ell_cell^4",
            "normalized_shape": "G_cell/sqrt(v_cell)=I_4",
            "normalized_shape_determinant": 1,
            "dilation": "ell_cell->s*ell_cell, v_cell->s^4*v_cell",
        },
        "birth_volume_law": {
            "total_volume": "V_N=N*v_cell",
            "single_birth_increment": "V_(N+1)-V_N=v_cell",
        },
        "volume_energy_invariant": {
            "invariant": "Y=E_C^4*v_cell/(hbar*c)^4",
            "unit_relation": "Y=1 iff E_C*ell_cell=hbar*c",
            "scale_orbit": "(E_C,ell_cell)->(E_C/s,s*ell_cell)",
            "invariant_under_orbit": True,
        },
        "common_parent": {
            "functional": "((u-k_X)^2+(rho-u)^2+(epsilon+lambda)^2)/2",
            "hessian": [[2,-1,0,0],[-1,1,0,0],[0,0,1,1],[0,0,1,1]],
            "rank": 3,
            "nullity": 1,
            "determinant": 0,
            "kernel": "(0,0,1,-1)",
            "spectrum": ["0", "2", "(3-sqrt(5))/2", "(3+sqrt(5))/2"],
        },
        "status": {
            "intrinsic_volume_architecture": "8/8",
            "relative_volume_origin": "3/3",
            "cell_volume_magnitude": "0/1",
            "absolute_clock_energy": "0/1",
            "absolute_scale": "0/1",
        },
        "proofdsl": {
            "status": "lcf-checked",
            "obligation_count": len(verified.obligations),
            "obligations": [name for name, _ in verified.obligations],
            "certificate_sha256": verified.sha256,
            "floating_point_values": 0,
        },
        "verdict": {
            "intrinsic_four_volume_carrier_constructed": True,
            "single_birth_volume_increment_derived": True,
            "volume_energy_product_selected": True,
            "cell_volume_magnitude_derived": False,
            "absolute_clock_energy_derived": False,
        },
        "next_gate": "version10_cell_birth_four_volume_spectral_counting_measure_origin_gate",
        "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text)
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())
    print(verified.sha256)


if __name__ == "__main__":
    main()