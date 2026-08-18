#!/usr/bin/env python3
"""Проверка масштаба локализации голономной нулевой моды."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_holonomy_zero_mode_localization_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


boundary = load_result("s2t_v5_massless_holonomy_defect_index_gate_results.json")
projector = load_result("s2t_v4_family_defect_projector_supercurvature_gate_results.json")
locking = load_result("s2t_v4_family_defect_gauge_family_locking_gate_results.json")
majorana = load_result("s2t_majorana_defect_parent_action_gate_results.json")

assert boundary["twisted_circle_spectrum"]["zero_level_count_single_chiral"] == 1
assert not boundary["localization_audit"]["localized_at_defect_core"]
assert projector["supercurvature_factorization"]["native_hessian_eigenvalues"] == [8 / 3] * 3
assert locking["status"]["pairing_condensate"] == "not_selected_by_symmetry"

# Радиальная энергия комплексного поля спаривания становится безразмерной
# при r=xi*rho, но физическая ширина xi остаётся свободной.
Z, lam, v = sp.symbols("Z lambda v", positive=True, real=True)
xi = sp.sqrt(Z / (lam * v**2))
gradient_coefficient = sp.simplify(Z * v**2)
potential_coefficient = sp.simplify(lam * v**4 * xi**2 / 2)
assert sp.simplify(potential_coefficient - gradient_coefficient / 2) == 0

scale_examples = []
for name, z_value, lambda_value, v_value in (
    ("unit_width", 1, 1, 1),
    ("double_width", 4, 1, 1),
):
    width = sp.simplify(xi.subs({Z: z_value, lam: lambda_value, v: v_value}))
    scale_examples.append(
        {
            "name": name,
            "Z_Phi": z_value,
            "lambda_Phi": lambda_value,
            "v": v_value,
            "xi": str(width),
            "same_winding_boundary_conditions": True,
        }
    )
assert scale_examples[0]["xi"] == "1"
assert scale_examples[1]["xi"] == "2"

# Условный поперечный оператор Дирака с ручным профилем
# m(x)=M tanh(x/xi) имеет нулевую моду cosh(x/xi)^(-M xi).
M, xi_symbol = sp.symbols("M xi", positive=True, real=True)
profile_exponent = sp.simplify(M * xi_symbol)
ipr = sp.simplify(1 / (3 * xi_symbol))
rms_width = sp.simplify(sp.pi * xi_symbol / sp.sqrt(12))

localization_examples = []
for name, width_value in (("unit_width", 1), ("double_width", 2)):
    localization_examples.append(
        {
            "name": name,
            "xi": width_value,
            "M_chosen_for_M_xi_equal_one": 1 / width_value,
            "inverse_participation_ratio": float(ipr.subs(xi_symbol, width_value)),
            "rms_width": float(rms_width.subs(xi_symbol, width_value)),
            "normalizable": True,
            "mod_two_parity": 1,
        }
    )
assert localization_examples[1]["rms_width"] == 2 * localization_examples[0]["rms_width"]
assert localization_examples[0]["inverse_participation_ratio"] == 2 * localization_examples[1]["inverse_participation_ratio"]

free_coefficients = majorana["minimal_tubular_action"]["continuous_coefficients"]
for required in ("Z_Phi", "m_Phi_squared", "lambda_Phi", "Majorana_Yukawa_normalization"):
    assert required in free_coefficients

result = {
    "gate": "version5_holonomy_zero_mode_localization_gate",
    "input_certificates": {
        "boundary_C3_zero_level_count": 1,
        "boundary_mode_localized": False,
        "projector_supercurvature_hessian": ["8/3", "8/3", "8/3"],
        "pairing_condensate_selected_by_existing_locking_symmetry": False,
    },
    "field_type_audit": {
        "H": {
            "type": "neutral traceless self-adjoint family endomorphism",
            "vacuum_data": "four rank-one tetrahedral projectors",
            "native_curvature": "Q(H)=H^2-H/sqrt(3)-I/4",
        },
        "Phi": {
            "type": "complex charge-two Majorana pairing section",
            "required_defect_data": "nonzero vacuum amplitude, meridional phase winding and a core zero",
            "native_action_data": free_coefficients,
        },
        "canonical_equivariant_identification_H_to_Phi_in_project": False,
        "reason": "H is a neutral family-axis endomorphism, whereas Phi is a charged complex pairing section; the gauge-family locking gate treats them as distinct fields.",
    },
    "radial_scaling_audit": {
        "energy": "2*pi int r dr [Z_Phi(|d_r Phi|^2+|Phi|^2/r^2)+(lambda_Phi/2)(|Phi|^2-v^2)^2]",
        "substitution": "Phi=v F(r/xi), xi=sqrt(Z_Phi/(lambda_Phi v^2))",
        "dimensionless_common_factor": str(gradient_coefficient),
        "dimensionless_potential_coefficient": str(potential_coefficient),
        "dimensionless_profile_can_be_universal": True,
        "physical_width_fixed": False,
        "scale_examples": scale_examples,
    },
    "conditional_dirac_localization": {
        "assumed_mass_profile": "m(x)=M tanh(x/xi)",
        "zero_mode": "psi(x) proportional to cosh(x/xi)^(-M xi)",
        "profile_exponent": str(profile_exponent),
        "special_normalized_wavefunction": "sech(x/xi)/sqrt(2*xi) for M*xi=1",
        "special_inverse_participation_ratio": str(ipr),
        "special_rms_width": str(rms_width),
        "examples": localization_examples,
        "finding": "Normalizability follows conditionally after a sign-changing mass profile is supplied, but the localization length changes continuously while the winding and mod-two parity stay unchanged.",
    },
    "projector_hessian_test": {
        "native_H_hessian": "8/3",
        "can_be_used_as_lambda_Phi_v_squared_without_new_map": False,
        "even_after_manual_identification_remaining_free_data": [
            "Z_Phi or an equivalent transverse metric normalization",
            "Majorana Yukawa normalization g_Phi controlling the fermionic decay length",
            "existence and orientation of the nonzero pairing vacuum",
        ],
    },
    "verdict": {
        "boundary_zero_level": "retained",
        "conditional_bulk_zero_mode": "retained_if_a_charged_pairing_vortex_is_supplied",
        "parameter_free_radial_profile": "fail",
        "parameter_free_localization_width": "fail",
        "QH_to_pairing_identification": "not_derived",
        "localized_neutrino_or_Majorana_defect": "not_obtained",
        "physical_closure": False,
        "status": "The C3 boundary zero cannot be promoted to a localized bulk defect by the existing projector supercurvature. H and Phi have different field types, and radial rescaling leaves an unfixed physical width xi together with an independent fermionic decay normalization.",
    },
    "next_gate": (
        "Freeze the boundary-to-core bridge under the present field content. "
        "Reopen it only if a parent construction supplies a charged pairing section Phi, "
        "its covariant kinetic norm and its nonzero vacuum in the same trace before comparison with observables."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))