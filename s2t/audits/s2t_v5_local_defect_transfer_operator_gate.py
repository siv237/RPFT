#!/usr/bin/env python3
"""Минимальный аудит локального переноса на родителе Мориты Тома V."""

import json
from pathlib import Path

import numpy as np
import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v5_local_defect_transfer_operator_gate_results.json"


def load_result(name):
    return json.loads((ROOT / "s2t/results" / name).read_text(encoding="utf-8"))


morita = load_result("s2t_v5_morita_linking_parent_gate_results.json")
assert morita["morita_carrier"]["equivalence_bimodule"] == "E=M20x15(C)"
assert morita["linking_algebra"]["family_corner_weight"] == 4 / 7
assert morita["linking_algebra"]["observed_corner_weight"] == 3 / 7

# Проверяем на малом полном прямоугольном бимодуле общий факт Шура:
# эндоморфизм, коммутирующий со всеми левыми M_p и правыми M_q действиями,
# скалярен. Полный случай 20x15 имеет ту же матрично-единичную проверку.
p, q = 3, 2
dim_e = p * q


def matrix_units(n):
    units = []
    for i in range(n):
        for j in range(n):
            e = np.zeros((n, n), dtype=float)
            e[i, j] = 1.0
            units.append(e)
    return units


generators = []
for a in matrix_units(p):
    generators.append(np.kron(np.eye(q), a))
for b in matrix_units(q):
    generators.append(np.kron(b.T, np.eye(p)))

identity_end = np.eye(dim_e)
constraints = []
for g in generators:
    # vec(Tg-gT)=0 в столбцовом соглашении.
    constraints.append(np.kron(g.T, identity_end) - np.kron(identity_end, g))
constraint_matrix = np.vstack(constraints)
singular_values = np.linalg.svd(constraint_matrix, compute_uv=False)
tol = 1e-10
commutant_rank = int(np.count_nonzero(singular_values > tol))
commutant_nullity = dim_e**2 - commutant_rank
assert commutant_nullity == 1

# На двух направлениях самый общий ближайший однородный перенос после
# требований унитарности, чётности и обращения времени имеет стандартную
# дираковскую форму. Внутренний бимодульный множитель тождественен.
m, n, z, lam = sp.symbols("m n z lambda", real=True, nonzero=True)
I = sp.I
walk = sp.Matrix([[n * z, -I * m], [-I * m, n / z]])
walk_dagger_on_unit_circle = sp.Matrix([[n / z, I * m], [I * m, n * z]])
unitarity_product = sp.simplify(walk * walk_dagger_on_unit_circle)
unitarity_defect = sp.simplify(unitarity_product - sp.eye(2))
assert unitarity_product == (m**2 + n**2) * sp.eye(2)

parity = sp.Matrix([[0, 1], [1, 0]])
parity_defect = sp.simplify(parity * walk * parity - walk.subs(z, 1 / z))
assert parity_defect == sp.zeros(2)

characteristic = sp.factor((walk - lam * sp.eye(2)).det())
characteristic_unitary = sp.factor(characteristic.subs(n**2 + m**2, 1))
trace_walk = sp.simplify(sp.trace(walk))

# Непрерывный предел: m=a M, k=a p, n=sqrt(1-a^2 M^2).
a, mass, momentum = sp.symbols("a M p", positive=True, real=True)
cosine_dispersion = sp.sqrt(1 - a**2 * mass**2) * sp.cos(a * momentum)
continuum_series = sp.series(cosine_dispersion, a, 0, 4)
target_series = sp.series(sp.cos(a * sp.sqrt(mass**2 + momentum**2)), a, 0, 4)
continuum_defect = sp.simplify(
    sp.expand(cosine_dispersion.series(a, 0, 4).removeO())
    - sp.expand(sp.cos(a * sp.sqrt(mass**2 + momentum**2)).series(a, 0, 4).removeO())
)
assert continuum_defect == 0

# Унитарность оставляет один непрерывный модуль m. Угловые веса следа
# сохраняются для любого m и потому не задают его. Две перестановочно
# естественные подстановки показывают неоднозначность чтения весов как
# вероятностей смешивания.
corner_weights = {"family": sp.Rational(4, 7), "observed": sp.Rational(3, 7)}
candidate_masses = {
    "m2_equals_observed_weight": sp.sqrt(corner_weights["observed"]),
    "m2_equals_family_weight": sp.sqrt(corner_weights["family"]),
}
candidate_gaps = {
    name: sp.asin(value) for name, value in candidate_masses.items()
}

# Для трёх заряженных рёбер независимые монеты возвращают ровно три
# массовых модуля, то есть две относительные свободы после общего масштаба.
sector_count = 3
relative_sector_parameters = sector_count - 1

sample_unitarity_defects = {}
for sample_m in (0.0, 0.2, 0.5, 0.9, 1.0):
    sample_n = float(np.sqrt(max(0.0, 1.0 - sample_m**2)))
    sample_k = 0.37
    sample_walk = np.array(
        [
            [sample_n * np.exp(1j * sample_k), -1j * sample_m],
            [-1j * sample_m, sample_n * np.exp(-1j * sample_k)],
        ],
        dtype=complex,
    )
    defect = np.linalg.norm(sample_walk @ sample_walk.conj().T - np.eye(2))
    sample_unitarity_defects[str(sample_m)] = float(defect)
assert max(sample_unitarity_defects.values()) < 1e-12

result = {
    "gate": "version5_local_defect_transfer_operator_gate",
    "input_certificates": {
        "Morita_transition_carrier": "E=M20x15(C)",
        "carrier_dimension": 300,
        "family_corner_weight": "4/7",
        "observed_corner_weight": "3/7",
    },
    "bimodule_intertwiner_classification": {
        "theorem": "End_{M_p-M_q}(M_pq(C))=C for full matrix corners",
        "proxy_dimensions": {"p": p, "q": q, "dim_E": dim_e},
        "constraint_matrix_shape": list(constraint_matrix.shape),
        "constraint_rank": commutant_rank,
        "commutant_dimension": commutant_nullity,
        "consequence_for_M20x15": "local transport is scalar on the Morita carrier before the orientation doublet is added",
    },
    "minimal_two_direction_walk": {
        "formula": "W(k)=[[n exp(ik),-i m],[-i m,n exp(-ik)]] tensor I_E",
        "unitarity_condition": "n^2+m^2=1",
        "symbolic_unitarity_product": str(unitarity_product),
        "symbolic_unitarity_defect_before_constraint": str(unitarity_defect),
        "parity_relation": "sigma_x W(k) sigma_x=W(-k)",
        "parity_defect": [[str(x) for x in row] for row in parity_defect.tolist()],
        "characteristic_polynomial": str(characteristic),
        "trace": str(trace_walk),
        "dispersion": "cos(omega)=n cos(k)",
        "sample_unitarity_defects": sample_unitarity_defects,
    },
    "continuum_limit": {
        "scaling": "m=a M, k=a p, n=sqrt(1-a^2 M^2)",
        "walk_cosine_series": str(continuum_series),
        "Dirac_cosine_series": str(target_series),
        "difference_through_order_a3": str(continuum_defect),
        "emergent_dispersion": "E^2=p^2+M^2",
        "common_light_cone": True,
    },
    "free_parameter_audit": {
        "continuous_transfer_moduli_after_unitarity": 1,
        "parameter": "m in [-1,1]",
        "m_zero": "two uncoupled massless chiral shifts",
        "absolute_m_one": "spatial propagation coefficient n vanishes",
        "nonzero_propagating_mass": "requires 0<|m|<1 and is not fixed by current axioms",
        "normalized_trace_preserved_for_every_m": True,
    },
    "corner_weight_candidate_audit": {
        "weights": {name: str(value) for name, value in corner_weights.items()},
        "candidate_identifications": {
            name: {"m": str(value), "gap_omega0": str(candidate_gaps[name])}
            for name, value in candidate_masses.items()
        },
        "unitarity_or_trace_selects_between_candidates": False,
        "extra_principle_required": "a reflection, purification or stochastic rule relating diagonal trace weights to off-diagonal transfer amplitudes",
    },
    "charged_sector_extension": {
        "sector_count": sector_count,
        "independent_mass_parameters_if_edges_are_split": sector_count,
        "relative_parameters_after_common_scale": relative_sector_parameters,
        "matches_previous_H15_relative_freedom": True,
        "common_scalar_transport": "gives one universal gap and no u,d,e hierarchy",
        "block_projectors_needed_for_hierarchy": True,
        "block_projectors_reintroduce_Yukawa_input": True,
    },
    "defect_stage": {
        "homogeneous_transfer_classification_passed": True,
        "topological_defect_inserted": False,
        "reason_for_early_stop": "the homogeneous massive walk already contains an underived continuous modulus",
        "zero_mode_or_flavour_oscillation_claimed": False,
    },
    "verdict": {
        "local_unitary_transfer_exists": "pass",
        "Dirac_continuum_limit_exists": "pass",
        "Morita_covariance_removes_internal_matrix_freedom": "pass",
        "unique_nonzero_mass_from_current_geometry": "fail",
        "corner_trace_weights_fix_transfer_mass": "fail",
        "charged_mass_hierarchy_without_sector_inputs": "fail",
        "minimal_transfer_language_validated": True,
        "minimal_transfer_dynamics_physically_closed": False,
        "physical_closure": False,
        "status": "the Morita carrier supports a canonical massless chiral transport class, but every nonzero propagating mass requires one external mixing modulus; splitting u,d,e restores the two forbidden relative Yukawa freedoms",
    },
    "next_gate": (
        "Do not insert a defect or fit flavour oscillations yet. Test one and only one "
        "project-native candidate for fixing the mixing modulus: whether the existing "
        "rank-one/tetrahedral holonomy canonically defines a reflection or partial "
        "isometry on the orientation doublet. Close the dynamic route if that map is "
        "not functorial and unique."
    ),
}

OUTPUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))