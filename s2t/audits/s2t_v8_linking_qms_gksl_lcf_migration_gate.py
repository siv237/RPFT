#!/usr/bin/env python3
"""Migrate the linking quantum Markov semigroup to the exact LCF eDSL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_linking_qms_gksl_lcf_migration_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl.examples.version8_linking_qms import build_certificate  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402


def main() -> None:
    certificate = build_certificate()
    assert certificate.incidence_rank == 10
    assert certificate.linking_fixed_dimension == 41
    assert certificate.gksl_theorem.proposition.kind == "gksl_well_formed"
    assert certificate.trace_theorem.proposition.data["checked_matrix_units"] == 441
    assert certificate.corner_invariance_theorem.proposition.data[
        "checked_matrix_units"
    ] == 221
    assert certificate.corner_formula_theorem.proposition.data["basis_size"] == 221
    assert certificate.fixed_dimension_theorem.proposition.data == {
        "rank": 180,
        "nullity": 41,
        "shape": [220, 221],
    }

    old_path = ROOT / "s2t/results/s2t_v8_linking_dirichlet_quantum_markov_semigroup_gate_results.json"
    old = json.loads(old_path.read_text(encoding="utf-8"))
    old_fixed_dimension = old["fixed_algebra"]["dimension"]
    assert old_fixed_dimension == certificate.linking_fixed_dimension

    registry = verify_all()
    registered = next(
        gate
        for gate in registry["gates"]
        if gate["identifier"]
        == "version8_linking_dirichlet_quantum_markov_semigroup_gate"
    )
    assert registered["status"] == "lcf-checked"
    assert len(registered["obligations"]) == 6

    result = {
        "date": "2026-08-29",
        "gate": "version8_linking_qms_gksl_lcf_migration_gate",
        "exact_carrier": {
            "endpoint_dimension": 21,
            "source_corner_dimension": 11,
            "target_corner_dimension": 10,
            "incidence_rank": certificate.incidence_rank,
            "incidence_entries": "integers zero and one",
        },
        "gksl_certificate": {
            "jump_operator": "D_A = [[0,A^*],[A,0]]",
            "jump_self_adjoint": True,
            "hamiltonian": "zero",
            "rate": "1",
            "trusted_kernel_rule": "finite_dimensional_gksl_constructor",
            "complete_positivity_status": "derived inside the trusted GKSL rule",
            "independent_choi_semigroup_certificate": False,
        },
        "exact_matrix_unit_checks": {
            "trace_preservation_full_matrix_units": 441,
            "unital_identity_residual": "zero",
            "corner_invariance_matrix_units": 221,
            "corner_formula_matrix_units": 221,
        },
        "fixed_algebra": {
            "commutant_system_shape": [220, 221],
            "commutant_system_rank": 180,
            "exact_nullity": certificate.linking_fixed_dimension,
            "old_numerical_dimension": old_fixed_dimension,
        },
        "proofdsl_registry": {
            "status": registered["status"],
            "obligation_count": len(registered["obligations"]),
            "certificate_sha256": registry["certificate_sha256"][
                "version8_linking_dirichlet_quantum_markov_semigroup_gate"
            ],
        },
        "verdict": {
            "gksl_structure_lcf_checked": True,
            "trace_preservation_exact": True,
            "unitality_exact": True,
            "endpoint_corner_invariance_exact": True,
            "explicit_corner_formula_exact": True,
            "fixed_dimension_41_exact": True,
            "independent_cp_proof_object_obtained": False,
            "status": "lcf-checked-with-trusted-gksl-rule",
            "next_gate": "version8_gauge_twirl_kraus_lcf_migration_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()