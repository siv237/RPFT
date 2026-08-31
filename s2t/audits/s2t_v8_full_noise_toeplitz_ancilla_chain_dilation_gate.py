#!/usr/bin/env python3
"""Audit the Toeplitz-shift chain supplying full-noise ancillas."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_full_noise_toeplitz_ancilla_chain_dilation_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_full_noise_toeplitz_ancilla_chain import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    chain = certificate.chain_theorem.proposition.data
    assert chain["cell_dimension"] == 43
    assert chain["used_cell_revisited"] is False
    registry = verify_all()
    gate = next(
        item for item in registry["gates"]
        if item["identifier"] == "version8_full_noise_toeplitz_ancilla_chain_dilation_gate"
    )
    assert len(gate["obligations"]) == 7
    result = {
        "date": "2026-08-30",
        "gate": gate["identifier"],
        "carrier": {
            "system_dimension": certificate.system_dimension,
            "jump_dimension": certificate.jump_dimension,
            "cell_dimension": certificate.cell_dimension,
            "chain": "infinite bilateral tensor chain relative to |0>^tensor Z",
            "counter": "N e_n=n e_n",
            "shift": "U e_n=e_(n+1)",
            "commutator": "[N,U^k]=k U^k",
        },
        "global_step": {
            "formula": "V=(I_system tensor S_chain) U_collision^(0)",
            "unitary": True,
            "same_step_repeated": True,
            "external_reset_each_step": False,
            "used_cell_revisited": False,
            "cellwise_gauge_covariant": True,
        },
        "recovery": {
            "formula": "Tr_chain Ad(V)^n(rho_0 tensor omega_vac)=Phi_h^n(rho_0)",
            "domain": "all finite n >= 0",
            "proof": "finite-cylinder induction",
            "residual": "0",
        },
        "boundary": {
            "preloaded_product_vacuum_required": True,
            "vacuum_chain_parent_derived": False,
            "time_independent_local_hamiltonian_derived": False,
            "absolute_tick_duration_derived": False,
            "autonomy_status": "exact discrete Floquet autonomy, conditional reservoir preparation",
        },
        "registry": {
            "gate_count": registry["gate_count"],
            "obligation_count": registry["obligation_count"],
            "certificate_sha256": registry["certificate_sha256"][gate["identifier"]],
        },
        "next_gate": "vacuum_chain_parent_state_and_local_hamiltonian_origin_gate",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()