import json
from pathlib import Path

path_gate = json.loads(Path("s2t_c6_l21_delta2_path_choice_gate_results.json").read_text())
metric_strain = json.loads(Path("s2t_c6_l21_metric_strain_tensor_results.json").read_text())
finite_spec = json.loads(Path("s2t_c6_l21_delta2_finite_block_spec_results.json").read_text())

results = {
    "status": "delta2_ambient_linear_path_formula_fixed_operator_delta2_missing",
    "inputs": [
        "s2t_c6_l21_delta2_path_choice_gate_results.json",
        "s2t_c6_l21_metric_strain_tensor_results.json",
        "s2t_c6_l21_delta2_finite_block_spec_results.json",
    ],
    "selected_path": {
        "path_id": "ambient_linear_embedding_strain",
        "map": "F_eps(x)=(I+eps A)x, A=A^T, x in S3 subset R4, descended to L(2,1)",
        "metric": "g_eps = F_eps^* <.,.>_R4 on the fixed S3/RP3 parameter manifold",
        "reason": "This is the same first ambient strain route that supplies P02=Sym^2(R4)=1+9 in earlier audits.",
        "selection_status": "fixed_for_theorem_route_before_C_delta2_numbers",
    },
    "metric_derivatives": {
        "first_derivative_same_A": "g'_A(u,v)=2 <u,A v>",
        "second_derivative_same_A": "g''_A(u,v)=2 <A u,A v>",
        "mixed_second_derivative_A_B": "partial_A partial_B g(u,v)=<A u,B v>+<B u,A v>",
        "expansion_same_A": "g_eps(u,v)=g(u,v)+eps*2<u,A v>+eps^2<Au,Av>",
        "tangent_vectors": "u,v in T_x S3 with <u,x>=<v,x>=0",
    },
    "relation_to_first_strain_split": {
        "first_strain_from_existing_audit": metric_strain["metric_strain_formulas"][0]["formula"],
        "mod_diffeomorphism_split": metric_strain["metric_strain_formulas"][3]["formula"],
        "warning": "The first-order conformal representative h=2q_A g may be used as a diagnostic slice, but the theorem-route delta2 path is the raw ambient pullback path unless a slice theorem is supplied.",
    },
    "what_this_fixes": [
        "the g''(0) ambiguity for the preferred finite C_delta2 theorem route",
        "the bilinear mixed second derivative for the 55 symmetric deformation pairs",
        "the rule that C_delta2 numbers must be computed in the same quotient-normalized convention as the trace-square audits",
    ],
    "what_remains_open": [
        "derive delta2 Delta_1,coex from g'_A and g''_{A,B}",
        "include connection, Ricci, projector, and Hilbert/basis effects consistently at second order",
        "evaluate diagonal C_delta2[1,1] and C_delta2[3,3] traces from the finite spec",
        "prove or reject cancellation with the trace-square obstruction in the same scheme",
    ],
    "finite_block_context": finite_spec["counts"],
    "pass_fail": [
        {
            "test": "preferred_path_selected_before_numbers",
            "status": "pass",
            "meaning": "The theorem-route second-variation path is now fixed before any finite C_delta2 matrix entries are computed.",
        },
        {
            "test": "operator_delta2_formula_derived",
            "status": "not_yet",
            "meaning": "The metric path is fixed, but the actual second variation of the coexact one-form Laplacian is still missing.",
        },
        {
            "test": "finite_C_delta2_evaluated",
            "status": "not_yet",
            "meaning": "No diagonal low-shell traces have been computed yet.",
        },
    ],
    "plain_language": "We have now nailed the rails to the floor: the path is the raw ambient pullback metric. The train still has not run; C_delta2 is not computed yet.",
    "verdict": "The preferred delta2 theorem path is now fixed at metric-derivative level. For F_eps=(I+eps A)x, g'_A(u,v)=2<u,Av>, g''_A(u,v)=2<Au,Av>, and the mixed A,B derivative is <Au,Bv>+<Bu,Av>. This removes the path-choice ambiguity for the preferred route, but it does not close C6: the actual delta2 Delta_1,coex operator and the finite diagonal low-shell traces remain unevaluated.",
}

Path("s2t_c6_l21_delta2_ambient_path_formula_results.json").write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n")
print(json.dumps({
    "status": results["status"],
    "path_id": results["selected_path"]["path_id"],
    "preferred_path_selected_before_numbers": True,
    "operator_delta2_formula_derived": False,
    "finite_C_delta2_evaluated": False,
}, indent=2, ensure_ascii=False))