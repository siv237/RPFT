#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp
from s2t.proofdsl.examples.version10_cell_birth_four_volume_spectral_counting_measure_origin import SPEC, build_certificate
from s2t.proofdsl.gates import verify_gate

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v10_cell_birth_four_volume_spectral_counting_measure_origin_gate_results.json"


def main() -> None:
    predecessor = json.loads((ROOT / "s2t/results/s2t_v10_cell_birth_intrinsic_four_volume_parent_origin_gate_results.json").read_text())
    gate = "version10_cell_birth_four_volume_spectral_counting_measure_origin_gate"
    assert predecessor["next_gate"] == gate and SPEC.identifier == gate
    verified = verify_gate(SPEC)
    c = build_certificate()
    assert c.spectral_shape.shape == (43, 43)
    assert c.counting_projector.rank() == 43
    assert c.scale_hessian.rank() == 1
    assert c.scale_hessian.nullspace() == [sp.Matrix([-1, 1])]
    assert sum(c.architecture) == 8 and sum(c.origin_ledger) == 3
    result = {
        "date": "2026-09-01", "gate": gate, "predecessor": predecessor["gate"],
        "finite_cell_spectrum": {"dimension": 43, "levels": "0,1,...,42 divided by ell_cell", "full_count": 43, "top_threshold": "Lambda*ell_cell=42", "normalized_second_moment": 25585},
        "spectral_counting_parent": {"functional": "(log(Lambda)+log(ell_cell)-log(42))^2/2", "hessian": [[1,1],[1,1]], "rank": 1, "nullity": 1, "kernel": "(-1,1)", "spectrum": [0,2]},
        "scale_boundary": {"orbit": "(Lambda,ell_cell)->(Lambda/s,s*ell_cell)", "count_invariant": True, "cell_length_selected": False, "cell_four_volume_selected": False},
        "status": {"spectral_counting_architecture": "8/8", "origin_ledger": "3/5", "absolute_cell_volume": "0/1", "absolute_clock_energy": "0/1"},
        "proofdsl": {"status": "lcf-checked", "obligation_count": len(verified.obligations), "obligations": [n for n,_ in verified.obligations], "certificate_sha256": verified.sha256, "floating_point_values": 0},
        "verdict": {"finite_spectral_count_constructed": True, "spectral_count_selects_cutoff_length_product": True, "spectral_count_selects_absolute_volume": False},
        "next_gate": "version10_cell_birth_four_volume_topological_quantum_candidate_audit_gate", "floating_point_values": 0,
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest()); print(verified.sha256)


if __name__ == "__main__": main()