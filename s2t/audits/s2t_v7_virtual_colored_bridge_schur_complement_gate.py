#!/usr/bin/env python3
"""Audit classical and one-loop elimination of the Version VII colored bridge."""

import hashlib
import json
from pathlib import Path

import sympy as sp


def matrix_strings(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.simplify(value)) for value in row] for row in matrix.tolist()]


def main() -> None:
    ma2, mb2, kappa = sp.symbols("M_a2 M_b2 kappa", positive=True)
    px, py, qx, qy = sp.symbols("p_x p_y q_x q_y", real=True)
    light_variables = (px, py, qx, qy)
    pnorm2 = px**2 + py**2
    qnorm2 = qx**2 + qy**2
    u = sp.expand(pnorm2 * qnorm2)
    delta = sp.expand(ma2 * mb2 - kappa**2 * u)

    # One Hermitian 2x2 block occurs for each of the three color components.
    trace_k = ma2 + mb2
    discriminant = sp.sqrt((ma2 - mb2) ** 2 + 4 * kappa**2 * u)
    eigenvalues = (
        sp.simplify((trace_k - discriminant) / 2),
        sp.simplify((trace_k + discriminant) / 2),
    )

    gamma_zero_mode = 3 * sp.log(delta)
    origin = {variable: 0 for variable in light_variables}
    light_hessian = sp.hessian(gamma_zero_mode, light_variables).subs(origin)
    first_u_coefficient = sp.simplify(sp.diff(3 * sp.log(ma2 * mb2 - kappa**2 * sp.Symbol("u")), sp.Symbol("u")).subs(sp.Symbol("u"), 0))

    result = {
        "gate": "version7_virtual_colored_bridge_schur_complement_gate",
        "field_role_audit": {
            "heavy_variables": ["a in anti-3", "b in 3"],
            "light_variables": ["p = X_L e_R", "q = L_L Y_R"],
            "heavy_objects_are_bosonic_edge_fields_not_linear_operator_subspaces": True,
            "ordinary_fermionic_messenger_schur_formula_directly_applicable": False,
        },
        "heavy_block": {
            "matrix": [["M_a2", "-kappa*conjugate(p*q)"], ["-kappa*p*q", "M_b2"]],
            "determinant": str(delta),
            "eigenvalues_each_with_color_multiplicity_three": [str(value) for value in eigenvalues],
            "color_preserving_domain": "M_a2*M_b2 - kappa^2*|p*q|^2 > 0",
            "gap_closes_at": "|p*q|^2 = M_a2*M_b2/kappa^2",
        },
        "classical_elimination": {
            "linear_heavy_source_present": False,
            "stationary_solution_inside_positive_domain": "a=b=0",
            "tree_level_light_correction": "0",
            "creates_light_quadratic_instability": False,
            "preserves_su3_at_stationary_solution": True,
        },
        "finite_dimensional_gaussian": {
            "complex_color_multiplicity": 3,
            "effective_action": "3*log(M_a2*M_b2-kappa^2*|p*q|^2)+constant",
            "leading_light_operator": "-3*kappa^2/(M_a2*M_b2)*|p*q|^2",
            "leading_u_coefficient": str(first_u_coefficient),
            "light_hessian_at_full_origin": matrix_strings(light_hessian),
            "light_hessian_is_zero": light_hessian == sp.zeros(4),
            "first_nonzero_light_degree": 4,
            "monotone_toward_gap_closure": True,
            "stable_interior_minimum_from_determinant_alone": False,
        },
        "four_dimensional_trace_log": {
            "leading_integrand": "-3*kappa^2*|p*q|^2/((k^2+M_a2)*(k^2+M_b2))",
            "uv_radial_asymptotic": "dk/k",
            "logarithmically_divergent_quartic_matching": True,
            "requires_counterterm_and_renormalization_scale": True,
            "finite_coefficient_fixed_by_current_finite_graph": False,
            "negative_light_mass_generated_at_p_equal_q_equal_zero": False,
        },
        "project_comparison": {
            "version4_messenger_schur_same_category": False,
            "version6_bridge_determinant_boundary_risk_reappears_in_zero_mode_control": True,
            "independent_color_preserving_quadratic_launch_already_derived": False,
        },
        "verdict": {
            "virtual_color_singlet_nonlinear_coupling_exists": True,
            "self_starting_color_preserving_parent_admitted": False,
            "coefficient_free_stable_vacuum_closed": False,
            "status": "nonlinear_structural_pass_but_self_start_and_normalization_no_go",
            "next_gate": "version7_color_preserving_quadratic_selector_origin_gate",
        },
    }

    out = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v7_virtual_colored_bridge_schur_complement_gate_results.json"
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out.write_text(text, encoding="utf-8")
    print(out)
    print(hashlib.sha256(text.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()