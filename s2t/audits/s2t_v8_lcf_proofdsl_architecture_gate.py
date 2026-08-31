#!/usr/bin/env python3
"""Audit the LCF proof eDSL architecture and its first migrated gates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_lcf_proofdsl_architecture_gate_results.json"
sys.path.insert(0, str(ROOT))

from s2t.proofdsl import LindbladGenerator, Morphism, Proposition, Space, Theorem  # noqa: E402
from s2t.proofdsl.kernel import ProofError  # noqa: E402
from s2t.proofdsl.verify import verify_all  # noqa: E402
from s2t.proofdsl.z3_backend import available as z3_available  # noqa: E402


def rejection_controls() -> dict[str, bool]:
    space = Space("control", 1)
    zero = Morphism("zero", space, space, sp.zeros(1))
    controls = {
        "direct_theorem_construction_rejected": False,
        "wrong_morphism_shape_rejected": False,
        "incompatible_composition_rejected": False,
        "floating_lindblad_rate_rejected": False,
        "negative_lindblad_rate_rejected": False,
    }
    try:
        Theorem(Proposition.make("fake", "fake"), "outside_kernel")
    except PermissionError:
        controls["direct_theorem_construction_rejected"] = True
    try:
        Morphism("wrong", Space("A", 1), Space("B", 2), sp.eye(1))
    except ValueError:
        controls["wrong_morphism_shape_rejected"] = True
    try:
        Morphism("f", Space("A", 1), Space("B", 1), sp.eye(1)).then(
            Morphism("g", Space("C", 1), Space("A", 1), sp.eye(1))
        )
    except TypeError:
        controls["incompatible_composition_rejected"] = True
    for key, rate in (
        ("floating_lindblad_rate_rejected", 0.5),
        ("negative_lindblad_rate_rejected", -1),
    ):
        try:
            LindbladGenerator.make("bad", zero, [zero], [rate])
        except ProofError:
            controls[key] = True
    assert all(controls.values())
    return controls


def main() -> None:
    registry = verify_all()
    assert registry["status"] == "lcf-checked"
    assert registry["gate_count"] == 26
    assert registry["obligation_count"] == 165
    identifiers = [item["identifier"] for item in registry["gates"]]
    assert identifiers == [
        "version8_bimodule_common_curvature_relative_weight_gate",
        "spinodal_threshold",
        "version8_markov_fixed_algebra_selector_gate",
        "version8_linking_dirichlet_quantum_markov_semigroup_gate",
        "version8_gauge_twirl_cross_sector_kraus_bridge_gate",
        "version8_kraus_bridge_parent_action_hessian_gate",
        "version8_cross_arrow_covariance_origin_gate",
        "version8_minimal_covariant_stinespring_carrier_gate",
        "version8_intrinsic_noise_clock_dilation_gate",
        "version8_full_primitive_markov_generator_assembly_gate",
        "version8_kms_nontracial_relative_rate_selector_gate",
        "version8_modular_bohr_parent_origin_gate",
        "version8_page_wootters_stinespring_history_gate",
        "version8_canonical_autonomous_clock_unitary_extension_no_go_gate",
        "version8_microscopic_repeated_interaction_hamiltonian_gate",
        "version8_trace_dual_cross_interaction_selector_gate",
        "version8_metric_dual_environment_parent_action_origin_gate",
        "version8_full_noise_cotangent_carrier_admission_gate",
        "version8_full_noise_trace_frame_metric_gate",
        "version8_full_noise_42_jump_gksl_fixed_algebra_gate",
        "version8_full_noise_repeated_interaction_hamiltonian_gate",
        "version8_full_noise_physical_time_scale_no_go_gate",
        "version8_full_noise_toeplitz_ancilla_chain_dilation_gate",
        "version8_vacuum_chain_parent_state_and_local_hamiltonian_origin_gate",
        "version8_index_balanced_ancilla_conveyor_gate",
        "version8_static_local_hamiltonian_embedding_or_no_go_gate",
    ]
    for gate in registry["gates"]:
        for path in gate["source_paths"]:
            assert (ROOT / path).exists()

    controls = rejection_controls()
    result = {
        "date": "2026-08-30",
        "gate": "version8_lcf_proofdsl_architecture_gate",
        "architecture": {
            "language": "pure Python",
            "trusted_theorem_issuer": "s2t/proofdsl/kernel.py",
            "exact_backend": "SymPy",
            "floating_point_admitted": False,
            "z3_optional_backend_available": z3_available(),
            "z3_can_issue_theorems": False,
            "status_ladder": [
                "gate/result",
                "candidate",
                "spec-frozen",
                "lcf-checked",
                "lean-draft",
                "lean-verified",
            ],
        },
        "registry": registry,
        "illegal_state_rejection_controls": controls,
        "migration_queue": [
            "version8_clock_augmented_static_hamiltonian_conveyor_gate",
            "version7_common_higgs_degree_two_cross_edge_gate",
            "version7_common_chain_number_hodge_relative_trace_gate",
        ],
        "verdict": {
            "base_gate_template_operational": True,
            "deterministic_gate_certificates_operational": True,
            "real_project_no_go_migrated": True,
            "independent_exact_calculus_result_migrated": True,
            "all_project_audits_formalized": False,
            "python_kernel_formally_verified": False,
            "next_gate": "version8_clock_augmented_static_hamiltonian_conveyor_gate",
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(text, encoding="utf-8")
    print(OUTPUT)
    print(hashlib.sha256(text.encode()).hexdigest())


if __name__ == "__main__":
    main()