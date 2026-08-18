#!/usr/bin/env python3
"""Аудит голономного проектора и кратности нелинейного дефекта."""

import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_holonomy_projector_defect_multiplicity_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


self_defect = load_result("s2t_v5_self_generated_transition_defect_gate_results.json")
affine = load_result("s2t_v5_affine_ko6_reference_corner_gate_results.json")
h15 = load_result("s2t_v5_h15_majorana_pairing_correspondence_gate_results.json")
connection = load_result("s2t_v5_physical_corner_connection_classification_gate_results.json")
holonomy = load_result("s2t_v5_massless_holonomy_defect_index_gate_results.json")

assert self_defect["Morita_multiplicity_obstruction"]["zero_mode_multiplicity"] == 300
assert affine["canonical_reference_corner"]["physical_particle_count"] == 45
assert h15["zero_branch_spectral_compression"]["projector_rank"] == 1
assert connection["rank_one_family_corner"]["family_rank_one_selection_removes_observed_block_ambiguity"] is False
assert holonomy["holonomy_spectrum"]["invariant_eigenline_dimension"] == 1

# Полный бимодульный коммутант скалярен. Идемпотентный скаляр равен 0 или 1.
lam = sp.symbols("lambda")
scalar_projector_solutions = sp.solve(sp.Eq(lam**2, lam), lam)
assert scalar_projector_solutions == [0, 1]

# Голономный проектор на семейной тройке.
C3 = sp.Matrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
P0 = sp.simplify((sp.eye(3) + C3 + C3**2) / 3)
assert P0.rank() == 1
assert P0**2 == P0

I15 = sp.eye(15)
family_compression = sp.kronecker_product(P0, I15)
assert family_compression.rank() == 15

observed_block_sizes = [6, 2, 3, 3, 1]
combined_block_ranks = [P0.rank() * size for size in observed_block_sizes]
assert combined_block_ranks == [6, 2, 3, 3, 1]

# На слабом дублете коммутант полного M2 скалярен.
a, b, c, d = sp.symbols("a b c d")
T = sp.Matrix([[a, b], [c, d]])
E01 = sp.Matrix([[0, 1], [0, 0]])
E10 = sp.Matrix([[0, 0], [1, 0]])
equations = list(T * E01 - E01 * T) + list(T * E10 - E10 * T)
coefficient_matrix, _ = sp.linear_eq_to_matrix(equations, [a, b, c, d])
weak_commutant_dimension = len(coefficient_matrix.nullspace())
assert weak_commutant_dimension == 1

# Хиггс-зависимый ранг-один проектор и его SU(2)-ковариантность.
I = sp.I
H = sp.Matrix([1 + I, 2 - I])
sigma2 = sp.Matrix([[0, -I], [I, 0]])
H_tilde = sp.simplify(I * sigma2 * sp.conjugate(H))
norm = sp.simplify((sp.conjugate(H).T * H)[0])
Pnu = sp.simplify(H_tilde * sp.conjugate(H_tilde).T / norm)
assert sp.simplify(Pnu**2 - Pnu) == sp.zeros(2)
assert Pnu.rank() == 1

U = sp.Matrix([[0, 1], [-1, 0]])
assert sp.simplify(U * sp.conjugate(U).T - sp.eye(2)) == sp.zeros(2)
H_transformed = U * H
H_tilde_transformed = sp.simplify(I * sigma2 * sp.conjugate(H_transformed))
norm_transformed = sp.simplify((sp.conjugate(H_transformed).T * H_transformed)[0])
Pnu_transformed = sp.simplify(
    H_tilde_transformed * sp.conjugate(H_tilde_transformed).T / norm_transformed
)
covariance_residual = sp.simplify(Pnu_transformed - U * Pnu * sp.conjugate(U).T)
assert covariance_residual == sp.zeros(2)

combined_neutrino_projector = sp.kronecker_product(P0, Pnu)
assert combined_neutrino_projector.rank() == 1

rank_chain = [45, family_compression.rank(), 2, combined_neutrino_projector.rank()]
assert rank_chain == [45, 15, 2, 1]

result = {
    "gate": "version5_holonomy_projector_defect_multiplicity_gate",
    "full_bimodule_projector_no_go": {
        "carrier": "E=M20x15(C)",
        "bimodule_endomorphism_algebra": "C I_E",
        "scalar_idempotent_solutions": [int(value) for value in scalar_projector_solutions],
        "nontrivial_full_bimodule_linear_projector": False,
        "consequence": "every nontrivial compression is a physical-corner readout after restricting the coordinate action, not an endomorphism of the full factor bimodule",
    },
    "canonical_rank_ledger": {
        "full_parent_carrier": 300,
        "affine_physical_light_partial_sector": 45,
        "family_holonomy_projector_formula": "P0=(I+C3+C3^2)/3",
        "family_holonomy_projector_rank": P0.rank(),
        "P0_tensor_I15_rank": family_compression.rank(),
        "KO6_J_completed_family_compressed_rank": 30,
        "observed_block_names": ["Q_L", "L_L", "u_R", "d_R", "e_R"],
        "observed_block_sizes": observed_block_sizes,
        "combined_P0_block_ranks": combined_block_ranks,
        "only_fixed_rank_one_observed_block": "e_R",
        "fixed_rank_one_block_is_neutrino": False,
    },
    "weak_doublet_obstruction": {
        "space": "L_L=C^2",
        "coordinate_action": "M2(C)",
        "commutant_dimension": weak_commutant_dimension,
        "commutant": "C I2",
        "fixed_gauge_invariant_projector_ranks": [0, 2],
        "fixed_neutrino_rank_one_projector": False,
    },
    "Higgs_dressed_projector": {
        "formula": "P_nu(H)=tilde(H) tilde(H)^dagger/(H^dagger H)",
        "rank": Pnu.rank(),
        "idempotence_residual": [[str(value) for value in row] for row in (Pnu**2 - Pnu).tolist()],
        "SU2_covariance_residual": [[str(value) for value in row] for row in covariance_residual.tolist()],
        "defined_at_H_equal_zero": False,
        "constant_commutant_projector": False,
        "requires_broken_phase_or_nonzero_Higgs_section": True,
    },
    "conditional_neutrino_rank_chain": {
        "chain": "45 -> 15 by P0 -> 2 by L_L -> 1 by P_nu(H)",
        "ranks": rank_chain,
        "combined_projector": "P0 tensor P_nu(H)",
        "combined_complex_rank": combined_neutrino_projector.rank(),
        "family_direction_from_holonomy": True,
        "weak_direction_from_Higgs": True,
        "from_holonomy_alone": False,
        "matches_higher_degree_Weinberg_route": True,
    },
    "nonlinear_defect_embedding_boundary": {
        "old_scalar_defect": "q(x) I_E",
        "candidate_operator_valued_defect": "q(x) P0 tensor P_nu(H(x))",
        "requires_joint_q_and_H_dynamics": True,
        "regularity_at_Higgs_zeros_open": True,
        "common_kinetic_normalization_open": True,
        "overall_Weinberg_or_defect_amplitude_fixed": False,
        "already_a_term_of_scalar_kink_action": False,
    },
    "verdict": {
        "holonomy_projector_alone_removes_multiplicity_300_to_one": "fail",
        "holonomy_projector_reduces_family_three_to_one": "pass",
        "fixed_gauge_invariant_neutrino_projector": "fail",
        "Higgs_dressed_neutrino_projector": "conditional_pass",
        "conditional_single_complex_neutrino_line": "pass_after_physical_light_H15_and_nonzero_Higgs_compressions",
        "single_line_from_current_universal_scalar_defect": "fail",
        "absolute_mass_or_nonlinear_parent_derived": "fail",
        "physical_closure": False,
        "status": "P0 canonically removes only family multiplicity. A single neutrino line appears only after two further physical reductions: the L_L block and a Higgs-dressed covariant rank-one projector. This is precisely a higher-degree Weinberg-type route, not a projector of the full M20-M15 bimodule and not a consequence of holonomy alone.",
    },
    "next_gate": "version5_defect_transport_part_conclusion_gate",
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))