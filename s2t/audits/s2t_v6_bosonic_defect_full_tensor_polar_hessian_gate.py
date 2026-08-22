#!/usr/bin/env python3
"""Глобальная область определения полного полярного гессиана Q+T+B.

Проверяется скрученное разложение по характерам остаточной Z3.  Это
предшествует численному спектру: общий целочисленный ряд Фурье в
сопутствующем базисе не задаёт однозначных полей вокруг Z6-вихря.
"""

from __future__ import annotations

import json
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
from scipy.linalg import expm


ROOT = Path(__file__).resolve().parents[2]
COUPLED_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_q_tetrahedral_coupled_vacuum_gate.py"
T_AUDIT = ROOT / "s2t/audits/s2t_v6_bosonic_defect_tetrahedral_gauge_mass_parent_gate.py"
Q_AUDIT = ROOT / "s2t/audits/s2t_v6_projective_order_parameter_field_spectrum_gate.py"
THERMAL_RESULT = ROOT / "s2t/results/s2t_v6_tensor_square_relative_carrier_normalization_gate_results.json"
OUT = ROOT / "s2t/results/s2t_v6_bosonic_defect_full_tensor_polar_hessian_gate_results.json"


def residue(weight: int) -> int:
    value = weight % 3
    return -1 if value == 2 else value


def main() -> None:
    coupled = runpy.run_path(str(COUPLED_AUDIT))
    t_module = runpy.run_path(str(T_AUDIT))
    q_module = runpy.run_path(str(Q_AUDIT))
    thermal = json.loads(THERMAL_RESULT.read_text(encoding="utf-8"))["thermal_reopening"]

    q_basis = coupled["symmetric_traceless_basis"]()
    t_basis, _ = t_module["symmetrized_traceless_rank_three_basis"]()
    axes = coupled["tetrahedral_axes"]()
    director = axes[0]
    identity = np.eye(3)

    # Ориентированный ортонормированный кадр с нулевой осью вдоль вихря.
    transverse_one = np.array([1.0, -1.0, 0.0]) / np.sqrt(2.0)
    transverse_two = np.cross(director, transverse_one)
    frame = np.array([director, transverse_one, transverse_two])

    def cross_generator(vector: np.ndarray) -> np.ndarray:
        x, y, z = vector
        return np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])

    # h_a=J_a/3: именно exp(2 pi h_0) является остаточным элементом Z3.
    h = np.array([cross_generator(vector) / 3.0 for vector in frame])

    def q_action(generator: np.ndarray, value: np.ndarray) -> np.ndarray:
        return generator @ value - value @ generator

    def representation_matrix(generator: np.ndarray) -> np.ndarray:
        q_part = np.array([
            [np.sum(left * q_action(generator, right)) for right in q_basis]
            for left in q_basis
        ])
        t_part = np.array([
            [np.sum(left * t_module["act_on_rank_three"](generator, right)) for right in t_basis]
            for left in t_basis
        ])
        result = np.zeros((12, 12))
        result[:5, :5] = q_part
        result[5:, 5:] = t_part
        return result

    representation = np.array([representation_matrix(generator) for generator in h])
    adjoint = np.zeros((3, 3, 3))
    gram = np.einsum("aij,bij->ab", h, h)
    for a in range(3):
        for b in range(3):
            bracket = h[a] @ h[b] - h[b] @ h[a]
            adjoint[a, :, b] = np.linalg.solve(gram, np.einsum("cij,ij->c", h, bracket))

    matter_weights = np.rint(3.0 * np.linalg.eigvalsh(-1j * representation[0])).astype(int)
    gauge_weights = np.rint(3.0 * np.linalg.eigvalsh(-1j * adjoint[0])).astype(int)
    q_weights = np.rint(3.0 * np.linalg.eigvalsh(-1j * representation[0, :5, :5])).astype(int)
    t_weights = np.rint(3.0 * np.linalg.eigvalsh(-1j * representation[0, 5:, 5:])).astype(int)

    matter_holonomy = expm(2.0 * np.pi * representation[0])
    gauge_holonomy = expm(2.0 * np.pi * adjoint[0])

    beta = float(thermal["critical_inverse_temperature"])
    spectrum = np.array(thermal["coexistence_ordered_spectrum"], dtype=float)
    gap = float(spectrum[0] - spectrum[1])
    q_vacuum = gap * (np.outer(director, director) - identity / 3.0)
    t_vacuum = np.einsum("ai,aj,ak->ijk", axes, axes, axes)
    q_coefficients = np.einsum("aij,ij->a", q_basis, q_vacuum)
    t_coefficients = np.einsum("aijk,ijk->a", t_basis, t_vacuum)
    v_t_squared = float(np.sum(t_vacuum**2))
    alignment_scale = (8.0 / 9.0) ** 2
    ordered_free_energy = q_module["free_energy"](identity / 3.0 + q_vacuum, beta)

    # Разложение фонового T на веса 0 и +/-3.
    eigenvalues, eigenvectors = np.linalg.eigh(-1j * representation[0, 5:, 5:])
    weight_zero_projector = eigenvectors[:, np.abs(eigenvalues) < 1.0e-10] @ eigenvectors[:, np.abs(eigenvalues) < 1.0e-10].conj().T
    t_zero = np.real_if_close(weight_zero_projector @ t_coefficients).real
    t_three = t_coefficients - t_zero

    def unpack(value: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        q_value = np.einsum("a,aij->ij", value[:5], q_basis)
        t_value = np.einsum("a,aijk->ijk", value[5:], t_basis)
        return q_value, t_value

    def potential(value: np.ndarray) -> float:
        q_value, t_value = unpack(value)
        density = identity / 3.0 + q_value
        q_potential = q_module["free_energy"](density, beta) - ordered_free_energy
        moment = np.einsum("ikl,jkl->ij", t_value, t_value)
        curvature_t = moment - v_t_squared * identity / 3.0
        projective_readout = identity / 3.0 + q_value / gap
        contraction = np.einsum("ijk,jk->i", t_value, projective_readout)
        curvature_qt = np.outer(contraction, contraction) - alignment_scale * projective_readout
        return float(q_potential + np.sum(curvature_t**2) / 3.0 + np.sum(curvature_qt**2) / 3.0)

    off_sector_residuals = []
    orbit_map_residuals = []
    sample_profiles = [(0.0, 1.0851729254), (0.35, 1.06), (0.8, 1.01), (1.0, 1.0)]
    for a_value, b_value in sample_profiles:
        point = np.concatenate([q_coefficients, b_value * t_zero + a_value * t_three])
        hessian = coupled["finite_hessian"](potential, point, step=4.0e-5)
        off_sector_residuals.append(float(np.linalg.norm(matter_holonomy.T @ hessian @ matter_holonomy - hessian)))
        orbit_map = np.column_stack([matrix @ point for matrix in representation])
        orbit_map_residuals.append(float(np.linalg.norm(matter_holonomy @ orbit_map - orbit_map @ gauge_holonomy)))

    sector_dimensions = {}
    harmonic_examples = {}
    for character in (-1, 0, 1):
        matter_sector_weights = [int(weight) for weight in matter_weights if residue(int(weight)) == character]
        gauge_sector_weights = [int(weight) for weight in gauge_weights if residue(int(weight)) == character]
        assert len(gauge_sector_weights) == 1
        gauge_weight = gauge_sector_weights[0]
        sector_dimensions[str(character)] = {
            "matter": len(matter_sector_weights),
            "radial_connection": 1,
            "angular_connection": 1,
            "total_complex_radial_fields": len(matter_sector_weights) + 2,
            "matter_weights": matter_sector_weights,
            "gauge_weight": gauge_weight,
        }
        harmonic_examples[str(character)] = {
            "common_corotating_exponent": f"j-{gauge_weight}/3",
            "laboratory_harmonics_at_j_0": {
                str(weight): int((weight - gauge_weight) // 3)
                for weight in matter_sector_weights
            },
            "connection_laboratory_harmonic_at_j_0": 0,
        }

    result = {
        "gate": "version6_bosonic_defect_full_tensor_polar_hessian_gate",
        "global_bundle_domain": {
            "vortex_holonomy": "exp(2*pi*J0/3) in residual Z3",
            "corotating_boundary_condition": "xi(theta+2*pi)=rho(g_Z3)^(-1) xi(theta)",
            "common_exponent_rule": "mu=j-s_g/3; laboratory harmonic n_s=j+(s-s_g)/3",
            "integer_label": "j in Z",
            "residual_characters": [-1, 0, 1],
        },
        "representation_weights": {
            "Q_spin_two": q_weights.tolist(),
            "T_spin_three": t_weights.tolist(),
            "family_connection_adjoint": gauge_weights.tolist(),
            "matter_residue_multiplicities": dict(sorted(Counter(residue(int(x)) for x in matter_weights).items())),
        },
        "twisted_sector_dimensions": sector_dimensions,
        "harmonic_examples": harmonic_examples,
        "covariance_checks": {
            "sample_count": len(sample_profiles),
            "maximum_potential_hessian_Z3_residual": max(off_sector_residuals),
            "maximum_gauge_orbit_map_Z3_residual": max(orbit_map_residuals),
            "potential_hessian_preserves_residual_character": max(off_sector_residuals) < 2.0e-5,
            "connection_to_matter_map_preserves_residual_character": max(orbit_map_residuals) < 1.0e-10,
        },
        "previous_radial_scan_boundary": {
            "common_integer_corotating_harmonic_is_globally_valid_for_all_components": False,
            "globally_periodic_character_zero_complex_fields": sector_dimensions["0"]["total_complex_radial_fields"],
            "full_complex_radial_fields": 18,
            "omitted_twisted_complex_fields": 12,
            "previous_thirteen_real_component_scan_remains_local_robustness_test": True,
            "previous_scan_is_full_global_section_spectrum": False,
        },
        "translation_location": {
            "residual_character": 0,
            "integer_labels": [-1, 1],
            "expected_real_zero_mode_count": 2,
        },
        "verdict": {
            "full_tensor_polar_operator_domain_derived": True,
            "ordinary_single_integer_fourier_decomposition_rejected": True,
            "three_Z3_twisted_sector_decomposition_required": True,
            "full_tensor_spectrum_computed": False,
            "full_vortex_stability_closed": False,
            "matter_birth_closed": False,
            "next_gate": "version6_bosonic_defect_full_tensor_twisted_sector_spectrum_gate",
        },
    }

    assert q_weights.tolist() == [-2, -1, 0, 1, 2]
    assert t_weights.tolist() == [-3, -2, -1, 0, 1, 2, 3]
    assert gauge_weights.tolist() == [-1, 0, 1]
    assert all(row["total_complex_radial_fields"] == 6 for row in sector_dimensions.values())
    assert result["previous_radial_scan_boundary"]["omitted_twisted_complex_fields"] == 12
    assert result["covariance_checks"]["potential_hessian_preserves_residual_character"]
    assert result["covariance_checks"]["connection_to_matter_map_preserves_residual_character"]
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()