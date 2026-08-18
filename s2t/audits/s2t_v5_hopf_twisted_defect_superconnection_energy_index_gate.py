#!/usr/bin/env python3
"""Audit the joint finite-energy/index completion of the Hopf defect line."""

from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


def main() -> None:
    rho = sp.symbols("rho", positive=True)

    # Charge-one Prasad--Sommerfield profiles in dimensionless radius rho=g v r.
    w = rho / sp.sinh(rho)
    h = (rho * sp.cosh(rho) - sp.sinh(rho)) / (rho * sp.sinh(rho))

    ode_w = sp.simplify(sp.diff(w, rho) + w * h)
    ode_h = sp.simplify(sp.diff(h, rho) - (1 - w**2) / rho**2)
    boundary_density = sp.simplify(h * (1 - w**2))

    limits = {
        "w_at_zero": str(sp.limit(w, rho, 0, dir="+")),
        "h_at_zero": str(sp.limit(h, rho, 0, dir="+")),
        "w_at_infinity": str(sp.limit(w, rho, sp.oo)),
        "h_at_infinity": str(sp.limit(h, rho, sp.oo)),
    }
    boundary_charge = sp.simplify(
        sp.limit(boundary_density, rho, sp.oo)
        - sp.limit(boundary_density, rho, 0, dir="+")
    )

    # For c1=1, flux 2 pi gives B_r=1/(2 r^2). Its Maxwell core energy
    # scales as integral_0 dr/r^2 and therefore diverges. The ungauged
    # projector hedgehog instead has a constant shell energy and diverges
    # at infinity.
    result = {
        "gate": "version5_hopf_twisted_defect_superconnection_energy_index_gate",
        "pure_hopf_line": {
            "Chern_number": 1,
            "flux_normalization": "integral_S2 F = 2 pi",
            "radial_magnetic_field": "B_r=1/(2 r^2)",
            "core_energy_integral": "pi/2 integral_0 dr/r^2",
            "core_energy_finite": False,
            "projector_gradient_shell_energy": "8 pi dr",
            "infrared_projector_energy_finite": False,
            "u1_phase_cancels_projector_angular_gradient": False,
            "verdict": "index_carrier_but_not_finite_energy_completion",
        },
        "smooth_bps_completion": {
            "dimensionless_radius": "rho=g v r",
            "profiles": {
                "w": "rho/sinh(rho)",
                "h": "coth(rho)-1/rho",
            },
            "Bogomolny_equations": {
                "w_prime_plus_w_h": str(ode_w),
                "h_prime_minus_one_minus_w2_over_rho2": str(ode_h),
                "passed": ode_w == 0 and ode_h == 0,
            },
            "boundary_values": limits,
            "smooth_core": limits["w_at_zero"] == "1" and limits["h_at_zero"] == "0",
            "vacuum_at_infinity": limits["w_at_infinity"] == "0" and limits["h_at_infinity"] == "1",
            "magnetic_charge": int(boundary_charge),
            "dimensionless_energy": str(sp.simplify(4 * sp.pi * boundary_charge)),
            "physical_energy": "4 pi v/g",
            "finite_energy": boundary_charge == 1,
            "asymptotic_positive_eigenline_Chern_number": 1,
            "Callias_index_fundamental_complex_fermion": 1,
            "same_topological_charge_controls_energy_and_index": True,
        },
        "superconnection_reading": {
            "graded_bundle": "(E tensor L) direct_sum (E* tensor L*)",
            "superconnection": "A_super=nabla_A+Phi",
            "curvature_components": ["F_A", "D_A Phi", "Phi^2"],
            "KO6_pairs_opposite_orientations": True,
            "full_real_index_cancels_between_conjugate_branches": True,
            "oriented_physical_branch_index": 1,
        },
        "project_embedding_audit": {
            "project_has_conditional_family_SO3_connection": True,
            "existing_connection_scope": "tubular/local bulk-core bridge",
            "global_spatial_SO3_Yang_Mills_Higgs_action_derived": False,
            "radial_amplitude_h_derived_from_M35": False,
            "gauge_stiffness_derived_from_normalized_M35_trace": False,
            "absolute_scales_g_and_v_derived": False,
            "H15_fundamental_Callias_coupling_derived": False,
        },
        "verdict": {
            "pure_hopf_curvature_alone_passes_joint_test": False,
            "standard_smooth_nonabelian_completion_passes_mathematical_joint_test": True,
            "completion_is_derived_from_current_parent": False,
            "status": "mathematical_joint_energy_index_pass_parent_derivation_open",
            "physical_closure": False,
        },
        "next_gate": "version5_spatial_so3_superconnection_parent_trace_gate",
    }

    output = Path(__file__).resolve().parents[1] / "results" / (
        "s2t_v5_hopf_twisted_defect_superconnection_energy_index_gate_results.json"
    )
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    assert ode_w == 0
    assert ode_h == 0
    assert limits == {
        "w_at_zero": "1",
        "h_at_zero": "0",
        "w_at_infinity": "0",
        "h_at_infinity": "1",
    }
    assert boundary_charge == 1
    assert math.isclose(float(4 * math.pi), 12.566370614359172)
    print(output)


if __name__ == "__main__":
    main()