import json
from pathlib import Path

projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())
checklist = json.loads(Path("s2t_c6_l21_full_operator_checklist_results.json").read_text())

projected_trace = projection["projection"]["projected_gram_trace"]
projected_rank = projection["projection"]["projected_rank_numeric"]

results = {
    "status": "delta2_delta_gate_fixed_locality_or_finite_block_required",
    "inputs": [
        "s2t_c6_l21_n3_explicit_projection_results.json",
        "s2t_c6_l21_full_operator_checklist_results.json",
    ],
    "determinant_identity": {
        "second_variation": "delta^2 log det Delta = Tr(Delta^-1 delta^2 Delta) - Tr(Delta^-1 delta Delta Delta^-1 delta Delta)",
        "coexact_boson_prefactor": "Gamma_coex = 1/2 log det' Delta_1,coex, so the delta^2 Delta block enters with prefactor +1/2 before local subtraction choices",
        "warning": "The trace-square sign audit is conditional unless Tr(Delta^-1 delta^2 Delta) is proven local/subtracted/compensated or evaluated as a finite low-shell matrix block.",
    },
    "gate_definition": {
        "cannot_be_assumed": "delta^2 Delta cannot be dropped by naming it local after a nonzero n=1<->n=3 low-shell obstruction has been found.",
        "allowed_outcomes": [
            "local_heat_kernel_only: prove the P02/mixed low-shell projection vanishes and the remainder is a local counterterm fixed before fitting",
            "exact_compensation: show cancellation against ghost/exact/projector/Hilbert terms in the same determinant scheme",
            "finite_block: compute C_delta2[1,1], C_delta2[1,3], and any diagonal n=3 contribution in the quotient-normalized bases",
        ],
        "forbidden_outcomes": [
            "post-hoc finite subtraction of the trace-80 obstruction",
            "dropping delta^2 Delta while keeping the trace-square suppression as a theorem",
            "using a scheme-dependent counterterm whose coefficient is chosen after comparing with alpha",
        ],
    },
    "required_matrix_output": {
        "block_name": "C_delta2",
        "domain_basis": "six quotient-normalized n=1 Killing one-forms",
        "target_basis": "30-dimensional quotient-normalized n=3 coexact basis plus any diagonal same-shell blocks required by second variation",
        "must_report": [
            "whether Tr(Delta^-1 delta^2 Delta) has a nonlocal finite projection in P02",
            "the quotient-normalized low-shell matrix elements if the projection is nonzero",
            "the subtraction scheme and why it was fixed before using the observed alpha residual",
            "the combined sign after adding trace-square, connection, Ricci, projector, Hilbert, and delta2 blocks",
        ],
    },
    "current_obstruction_context": {
        "projected_trace_before_delta2_gate": projected_trace,
        "projected_rank_before_delta2_gate": projected_rank,
        "meaning": "The nonzero trace-square low-shell block makes the delta^2 Delta term a real gate, not an optional caveat.",
    },
    "pass_fail": [
        {
            "test": "determinant_identity_recorded",
            "status": "pass",
            "meaning": "The formal place and sign of Tr(Delta^-1 delta^2 Delta) are fixed.",
        },
        {
            "test": "locality_or_compensation_proven",
            "status": "not_yet",
            "meaning": "No proof currently removes the finite low-shell delta^2 Delta projection.",
        },
        {
            "test": "finite_matrix_evaluated",
            "status": "not_yet",
            "meaning": "C_delta2 has not been computed in the n=1/n=3 quotient-normalized bases.",
        },
    ],
    "plain_language": "The fifth extinguisher is the acceleration of the operator itself. It may be harmless local smoke, but after trace 80 it must either be proven smoke or measured as another flame.",
    "verdict": "The delta^2 Delta gate is now explicit. Mature C6 requires either a proof that Tr(Delta^-1 delta^2 Delta) is purely local/subtracted or exactly compensated in the same Maxwell--ghost scheme, or a finite quotient-normalized low-shell computation of C_delta2. Until one of these outcomes is delivered, the trace-square suppression remains conditional rather than a determinant theorem.",
}

Path("s2t_c6_l21_delta2_delta_gate_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "identity_recorded": True,
    "locality_or_compensation_proven": False,
    "finite_matrix_evaluated": False,
    "projected_trace_before_delta2_gate": projected_trace,
}, indent=2, ensure_ascii=False))