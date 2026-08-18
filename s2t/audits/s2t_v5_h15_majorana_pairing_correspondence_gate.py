#!/usr/bin/env python3
"""Классификация C3-эквивариантного майорановского тензора на H15."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_h15_majorana_pairing_correspondence_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


freeze = load_result("s2t_v5_defect_transport_status_freeze_gate_results.json")
h15 = load_result("s2t_v5_h15_neutrino_degree_split_gate_results.json")
boundary = load_result("s2t_v5_massless_holonomy_defect_index_gate_results.json")
quiver = load_result("s2t_v4_family_defect_quiver_moment_map_gate_results.json")

assert freeze["architecture_fork"]["selected_next_by_minimal_change_rule"] == "branch_A_preserve_H15"
assert not h15["verdict"]["H15_contains_Dirac_neutrino_edge"]
assert boundary["twisted_circle_spectrum"]["zero_level_count_single_chiral"] == 1
assert quiver["checks"]["real_a4_triplet_commutant_dimension"] == 1

# Трёхцикл действует на трёх семейных каналах циклической перестановкой.
C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
I3 = sp.eye(3)
assert C3**3 == I3

# Общая комплексная симметричная майорановская матрица имеет шесть
# коэффициентов. Условие C3^T M C3=M сокращает пространство до двух.
m00, m11, m22, m01, m02, m12 = sp.symbols("m00 m11 m22 m01 m02 m12")
M = sp.Matrix(
    [
        [m00, m01, m02],
        [m01, m11, m12],
        [m02, m12, m22],
    ]
)
equations = list(C3.T * M * C3 - M)
coefficient_matrix, _ = sp.linear_eq_to_matrix(
    equations, [m00, m11, m22, m01, m02, m12]
)
nullspace = coefficient_matrix.nullspace()
assert len(nullspace) == 2

A = C3 + C3.T
assert C3.T * I3 * C3 == I3
assert C3.T * A * C3 == A
assert A.T == A

# Спектральный проектор на инвариантную нулевую линию является полиномом
# от голономии и не требует выбора базиса.
P0 = sp.simplify((I3 + C3 + C3**2) / 3)
Q = sp.simplify(I3 - P0)
ones_projector = sp.ones(3) / 3
assert P0 == ones_projector
assert P0**2 == P0
assert Q**2 == Q
assert P0 * Q == sp.zeros(3)
assert P0.rank() == 1
assert Q.rank() == 2

x, y = sp.symbols("x y", real=True)
M_c3 = sp.simplify(x * P0 + y * Q)
assert C3.T * M_c3 * C3 == M_c3
assert M_c3.eigenvals() == {x: 1, y: 2}

# Сжатие на единственную нулевую ветвь оставляет только x P0.
compressed = sp.simplify(P0 * M_c3 * P0)
assert compressed == x * P0

# Нормированный след задаёт длину, но не отношение x/y до сжатия.
tau3_norm = sp.simplify(sp.trace(M_c3.T * M_c3) / 3)
assert tau3_norm == x**2 / 3 + 2 * y**2 / 3

observed_corner_weight = sp.Rational(3, 7)
zero_line_family_weight = sp.simplify(observed_corner_weight * sp.trace(P0) / 3)
transverse_family_weight = sp.simplify(observed_corner_weight * sp.trace(Q) / 3)
assert zero_line_family_weight == sp.Rational(1, 7)
assert transverse_family_weight == sp.Rational(2, 7)

# Ранги показывают цену дополнительных условий нулевого ядра.
rank_cases = {
    "x_nonzero_y_nonzero": int(M_c3.subs({x: 2, y: 3}).rank()),
    "x_zero_y_nonzero": int(M_c3.subs({x: 0, y: 3}).rank()),
    "x_nonzero_y_zero": int(M_c3.subs({x: 2, y: 0}).rank()),
    "x_zero_y_zero": int(M_c3.subs({x: 0, y: 0}).rank()),
}
assert rank_cases == {
    "x_nonzero_y_nonzero": 3,
    "x_zero_y_nonzero": 2,
    "x_nonzero_y_zero": 1,
    "x_zero_y_zero": 0,
}

result = {
    "gate": "version5_h15_majorana_pairing_correspondence_gate",
    "input_certificates": {
        "architecture": "H15/M35 retained",
        "right_handed_neutrino_present": False,
        "degree_five_neutrino_sector_required": True,
        "C3_boundary_zero_level_count": 1,
    },
    "weinberg_operator_type": {
        "schematic_operator": "(c_ij/Lambda) (L_i^c tilde(H)^*) (tilde(H)^dagger L_j)",
        "weak_invariant_contraction_count": 1,
        "family_coefficient_type": "complex symmetric 3x3 matrix",
        "unconstrained_complex_dimension": 6,
        "lepton_number_violation": 2,
        "absolute_scale_requires": "1/Lambda or an equivalent parent spectral moment",
    },
    "C3_family_classification": {
        "holonomy_matrix": [list(map(int, C3.row(i))) for i in range(3)],
        "invariance_equation": "C3^T M C3=M with M^T=M",
        "invariant_symmetric_dimension": len(nullspace),
        "basis": ["P0", "Q=I-P0"],
        "general_tensor": "M=x P0+y Q",
        "eigenvalues": ["x on the invariant line", "y with multiplicity two on the transverse plane"],
        "normalized_trace_norm": str(tau3_norm),
        "relative_parameter_before_compression": True,
        "full_A4_invariant_commutant_dimension": 1,
        "full_A4_consequence": "only the identity survives, giving a family-degenerate tensor",
    },
    "zero_branch_spectral_compression": {
        "projector_formula": "P0=(I+C3+C3^2)/3=(1/3) all-ones matrix",
        "projector_rank": int(P0.rank()),
        "projector_is_basis_free_polynomial_in_holonomy": True,
        "compressed_tensor": "P0 M P0=x P0",
        "compressed_family_direction_dimension": 1,
        "M35_zero_line_trace_weight": "1/7",
        "M35_transverse_trace_weight": "2/7",
        "family_direction_fixed_without_hand_chosen_vector": True,
        "overall_amplitude_fixed": False,
    },
    "rank_ledger": rank_cases,
    "fermionic_spectral_action_literature_route": {
        "reference": "Sakellariadou-Sitarz, arXiv:1903.09149",
        "positive": "A left-neutrino-only 15-state almost-commutative geometry can generate a Higgs-quadratic Majorana/Weinberg-type term from a next-order nonscalar fermionic spectral action.",
        "unresolved": [
            "the nonscalar cutoff endomorphism/function is additional data and is not classified by the current parent",
            "the relevant cutoff moment and absolute scale are not fixed by C3 or the M35 trace",
            "the construction supplies an effective mass term, not a radial defect saddle or localization length",
        ],
    },
    "verdict": {
        "H15_gauge_invariant_higher_degree_route": "pass_as_an_admissible_operator_type",
        "C3_unrestricted_family_uniqueness": "fail_dimension_two",
        "canonical_zero_branch_family_direction": "pass_dimension_one_after_spectral_compression",
        "absolute_majorana_scale": "not_derived",
        "nonscalar_fermionic_spectral_measure": "promising_but_not_fixed",
        "radial_localization": "not_derived",
        "physical_closure": False,
        "status": "The H15 route is not empty: the unique C3 zero branch has a canonical polynomial projector P0, and compression fixes the family direction of a higher-degree Majorana correspondence to P0. C3 alone leaves two coefficients, while the overall Weinberg scale, nonscalar fermionic spectral moment and defect profile remain open.",
    },
    "next_gate": "version5_h15_fermionic_spectral_weinberg_measure_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))