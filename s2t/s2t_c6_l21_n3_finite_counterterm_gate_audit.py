import json
from pathlib import Path

projection = json.loads(Path("s2t_c6_l21_n3_explicit_projection_results.json").read_text())
parity = json.loads(Path("s2t_c6_l21_n3_parity_descent_results.json").read_text())
full_gate = json.loads(Path("s2t_c6_l21_full_operator_rescue_gate_results.json").read_text())

projected_trace = projection["projection"]["projected_gram_trace"]
projected_rank = projection["projection"]["projected_rank_numeric"]
projected_eigs = projection["projection"]["projected_eigenvalues"]
descends = parity["antipodal_rule"]["descends_to_L21"]

results = {
    "status": "n3_finite_low_shell_trace_not_rescuable_by_local_counterterm",
    "inputs": [
        "s2t_c6_l21_n3_explicit_projection_results.json",
        "s2t_c6_l21_n3_parity_descent_results.json",
        "s2t_c6_l21_full_operator_rescue_gate_results.json",
        "s2t_c6_l21_coexact_locality_gate_results.json",
    ],
    "low_shell_data": {
        "channel": "n=1 <-> n=3",
        "projected_trace": projected_trace,
        "projected_rank": projected_rank,
        "projected_eigenvalues": projected_eigs,
        "descends_to_L21": descends,
        "spectral_position": "finite low shell, not large-n asymptotic",
    },
    "locality_tests": [
        {
            "test": "is_this_a_UV_heat_kernel_asymptotic_piece",
            "verdict": "no",
            "reason": "The data comes from the finite 1<->3 low-shell block, not from the large-eigenvalue heat-kernel expansion.",
        },
        {
            "test": "can_a_predetermined_local_counterterm_remove_it_by_sector",
            "verdict": "no_as_stated",
            "reason": "A local counterterm can subtract prescribed local invariants, but this trace is global spectral matrix data in a specific off-diagonal shell channel.",
        },
        {
            "test": "can_a_finite_counterterm_be_chosen_after_the_fact",
            "verdict": "forbidden",
            "reason": "Choosing a finite subtraction to erase trace 80 after seeing the alpha target violates the no-hidden-parameter rule.",
        },
        {
            "test": "can_full_operator_terms_still_cancel_it",
            "verdict": "yes_open",
            "reason": "Connection, Ricci, coexact-projector, Hilbert-metric, and delta2-Delta terms are same-order operator data and remain the legitimate rescue gate.",
        },
    ],
    "allowed_rescues_remaining": full_gate["remaining_rescue_terms"],
    "plain_language": (
        "The n=3 signal is a real low note, not UV hiss. Local counterterms clean up the high-frequency hiss; they do not let us erase this specific low note after hearing it. "
        "Only a real full-operator cancellation or a no-fit absorption identity can still save the clean C6 theorem."
    ),
    "verdict": (
        "The nonzero n=1<->n=3 projected trace is finite low-shell spectral data on L(2,1). It is not a UV heat-kernel asymptotic term and cannot be discarded by a local counterterm without introducing a forbidden finite scheme choice. "
        "C6 therefore remains at the full-operator rescue gate: the remaining legitimate options are explicit cancellation by the missing one-form terms or a derived no-fit absorption identity."
    ),
}

Path("s2t_c6_l21_n3_finite_counterterm_gate_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "projected_trace": projected_trace,
    "projected_rank": projected_rank,
    "descends_to_L21": descends,
    "local_counterterm_rescue": "failed_for_finite_low_shell_trace",
}, indent=2, ensure_ascii=False))