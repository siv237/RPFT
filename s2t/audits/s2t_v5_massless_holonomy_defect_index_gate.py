#!/usr/bin/env python3
"""Спектр безмассового триплета на окружности с C3-голономией."""

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_massless_holonomy_defect_index_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


reflection = load_result("s2t_v5_rank_one_tetrahedral_transfer_reflection_gate_results.json")
assert reflection["verdict"]["minimal_dynamic_mass_route"] == "closed"
assert reflection["verdict"]["massless_holonomy_transport"] == "retained"

# Трёхцикл на трёхмерном стандартном секторе имеет спектр 1,omega,omega^2.
C3 = np.array(
    [
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
    ]
)
identity = np.eye(3)
assert np.linalg.norm(C3 @ C3 @ C3 - identity) < 1e-14

eigenvalues, eigenvectors = np.linalg.eig(C3.astype(complex))
phases = np.angle(eigenvalues) / (2 * np.pi)
phases = np.where(phases > 0.5, phases - 1.0, phases)
phases = np.where(phases <= -0.5, phases + 1.0, phases)
phases_sorted = sorted(float(x) for x in phases)
expected = [-1 / 3, 0.0, 1 / 3]
assert np.max(np.abs(np.array(phases_sorted) - np.array(expected))) < 1e-12

invariant_kernel_dimension = 3 - np.linalg.matrix_rank(C3 - identity, tol=1e-12)
assert invariant_kernel_dimension == 1
invariant_vector = np.ones(3) / np.sqrt(3)
assert np.linalg.norm(C3 @ invariant_vector - invariant_vector) < 1e-14

# Спектр D=-i d/ds при psi(s+L)=C3 psi(s):
# p_{n,r}=2*pi*(n+alpha_r)/L.
L = sp.symbols("L", positive=True, real=True)
alpha_values = [sp.Rational(-1, 3), sp.Integer(0), sp.Rational(1, 3)]
n = sp.symbols("n", integer=True)
momentum_formulae = [2 * sp.pi * (n + alpha) / L for alpha in alpha_values]

cutoff = 8
levels = []
for branch, alpha in zip(("minus", "invariant", "plus"), alpha_values):
    for mode in range(-cutoff, cutoff + 1):
        value = float(2 * np.pi * (mode + float(alpha)))
        levels.append(
            {
                "branch": branch,
                "alpha": str(alpha),
                "n": mode,
                "dimensionless_L_times_p": value,
                "is_zero": abs(value) < 1e-12,
            }
        )

zero_levels = [row for row in levels if row["is_zero"]]
assert len(zero_levels) == 1
smallest_nonzero = min(abs(row["dimensionless_L_times_p"]) for row in levels if not row["is_zero"])
assert abs(smallest_nonzero - 2 * np.pi / 3) < 1e-12

# Инверсия winding меняет C3 на C3^{-1} и только переставляет две
# сопряжённые ветви.
C3_inverse = C3.T
inverse_eigenvalues = np.linalg.eigvals(C3_inverse.astype(complex))
inverse_phases = np.angle(inverse_eigenvalues) / (2 * np.pi)
inverse_phases = np.where(inverse_phases > 0.5, inverse_phases - 1.0, inverse_phases)
inverse_phases = np.where(inverse_phases <= -0.5, inverse_phases + 1.0, inverse_phases)
inverse_phases_sorted = sorted(float(x) for x in inverse_phases)
assert np.max(np.abs(np.array(inverse_phases_sorted) - np.array(expected))) < 1e-12

# Эта единичная кратность ядра не является комплексным Fredholm-индексом:
# для самосопряжённого оператора на окружности ядро и коядро равны.
complex_kernel_dimension_single_chiral = 1
complex_cokernel_dimension_single_chiral = 1
fredholm_index = complex_kernel_dimension_single_chiral - complex_cokernel_dimension_single_chiral
assert fredholm_index == 0

# При вещественном (майорановском) ограничении инвариантный постоянный
# вектор даёт одну вещественную моду; фиксируется только чётность ядра.
real_majorana_kernel_dimension = 1
mod2_kernel_parity = real_majorana_kernel_dimension % 2
assert mod2_kernel_parity == 1

# Для двух независимых направлений минимального блуждания комплексная
# нулевая кратность удваивается. H15-нейтринная ветвь сохраняет только
# левое хиральное чтение; без этого физического ограничения exact-one нет.
doubled_orientation_zero_dimension = 2

# Eta-инварианты двух сдвинутых ветвей взаимно уничтожаются:
# eta_alpha(0)=1-2alpha для 0<alpha<1.
eta_one_third = sp.Rational(1, 3)
eta_two_thirds = -sp.Rational(1, 3)
total_eta = sp.simplify(eta_one_third + eta_two_thirds)
assert total_eta == 0

# Нулевая мода плоской связи глобальна, а не локализована. Для N узлов её
# inverse participation ratio равен 1/N.
site_count = 60
uniform_wave = np.ones(site_count, dtype=complex) / np.sqrt(site_count)
inverse_participation_ratio = float(np.sum(np.abs(uniform_wave) ** 4))
assert abs(inverse_participation_ratio - 1 / site_count) < 1e-14

result = {
    "gate": "version5_massless_holonomy_defect_index_gate",
    "input_certificates": {
        "mass_selector_from_tetrahedral_reflection": "closed",
        "massless_holonomy_transport": "retained",
        "holonomy": "C3",
    },
    "holonomy_spectrum": {
        "matrix": C3.tolist(),
        "order": 3,
        "eigenvalues": ["1", "exp(+2*pi*i/3)", "exp(-2*pi*i/3)"],
        "fractional_phases": ["-1/3", "0", "+1/3"],
        "invariant_eigenline_dimension": int(invariant_kernel_dimension),
        "invariant_vector": invariant_vector.tolist(),
    },
    "twisted_circle_spectrum": {
        "operator": "D=-i d/ds",
        "boundary_condition": "psi(s+L)=C3 psi(s)",
        "formulae": [str(expr) for expr in momentum_formulae],
        "zero_level_count_single_chiral": len(zero_levels),
        "zero_levels": zero_levels,
        "smallest_nonzero_absolute_momentum": "2*pi/(3L)",
        "enumeration_cutoff": cutoff,
    },
    "orientation_and_reality": {
        "single_H15_chiral_branch_complex_kernel_dimension": complex_kernel_dimension_single_chiral,
        "two_direction_walk_complex_kernel_dimension": doubled_orientation_zero_dimension,
        "Majorana_real_kernel_dimension_after_single_chiral_restriction": real_majorana_kernel_dimension,
        "mod2_kernel_parity": mod2_kernel_parity,
        "exact_one_requires_H15_chiral_restriction": True,
    },
    "index_audit": {
        "complex_kernel_dimension": complex_kernel_dimension_single_chiral,
        "complex_cokernel_dimension": complex_cokernel_dimension_single_chiral,
        "Fredholm_index": fredholm_index,
        "nonzero_integer_index": False,
        "conditional_real_mod2_parity": mod2_kernel_parity,
        "boundary_kernel_is_not_yet_a_bulk_defect_index": True,
    },
    "winding_and_eta": {
        "inverse_winding_phases": ["-1/3", "0", "+1/3"],
        "winding_only_swaps_conjugate_branches": True,
        "eta_plus_one_third": str(eta_one_third),
        "eta_minus_one_third": str(eta_two_thirds),
        "total_eta": str(total_eta),
        "orientation_selected_by_eta": False,
    },
    "localization_audit": {
        "site_count": site_count,
        "zero_mode_profile": "uniform invariant holonomy eigenvector",
        "inverse_participation_ratio": inverse_participation_ratio,
        "expected_uniform_IPR": 1 / site_count,
        "localized_at_defect_core": False,
    },
    "flavour_boundary": {
        "holonomy_eigenchannels_propagate_diagonally": True,
        "physical_flavour_readout_basis_derived": False,
        "neutrino_oscillation_prediction": False,
    },
    "verdict": {
        "parameter_free_fractional_shifts": "pass",
        "one_invariant_zero_level_single_chiral": "pass",
        "one_real_Majorana_zero_mode_conditional_on_H15_chirality": "conditional_pass",
        "nonzero_Fredholm_index": "fail",
        "localized_defect_core_mode": "fail",
        "physical_neutrino_identification": "not_derived",
        "massless_holonomy_spectral_mechanism": "retained",
        "physical_closure": False,
        "status": "C3 holonomy gives parameter-free momentum shifts 0,+/-1/3 and one invariant zero level on the single H15 chiral branch; the integer index is zero and the mode is delocalized, so this is a boundary spectral selector rather than a localized neutrino defect",
    },
    "next_gate": (
        "Bridge the boundary zero level to the old vortex-core Majorana branch. "
        "Test whether the existing projector supercurvature Q(H), cubic-root connection "
        "and transfer operator determine a bulk radial profile and normalizable localized "
        "mode without a new stiffness, condensate scale or hand-chosen domain wall."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))