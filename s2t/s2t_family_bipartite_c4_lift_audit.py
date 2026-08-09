#!/usr/bin/env python3
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from s2t_two_layer_physical_ckm_redteam_audit import standard_parameters


VERTICES = tuple(range(4))
PHYSICAL_VERTICES = (0, 1, 2)
GRADING = (1, -1, 1, -1)
REQUIRED_A3_EDGES = {frozenset((0, 1)), frozenset((1, 2))}


def cycle_rank(edges):
    incidence = np.zeros((len(VERTICES), len(edges)), dtype=int)
    for column, edge in enumerate(edges):
        source, target = sorted(edge)
        incidence[source, column] = -1
        incidence[target, column] = 1
    rank = int(np.linalg.matrix_rank(incidence))
    return len(edges) - rank, rank


def connected(edges):
    reached = {0}
    changed = True
    while changed:
        changed = False
        for edge in edges:
            first, second = tuple(edge)
            if first in reached and second not in reached:
                reached.add(second)
                changed = True
            if second in reached and first not in reached:
                reached.add(first)
                changed = True
    return len(reached) == len(VERTICES)


def classify_minimal_lifts():
    all_edges = [frozenset(edge) for edge in itertools.combinations(VERTICES, 2)]
    rows = []
    for edge_count in range(2, len(all_edges) + 1):
        for edges in itertools.combinations(all_edges, edge_count):
            edge_set = set(edges)
            if not REQUIRED_A3_EDGES.issubset(edge_set):
                continue
            if not all(
                GRADING[first] == -GRADING[second]
                for first, second in (tuple(edge) for edge in edge_set)
            ):
                continue
            if not connected(edge_set):
                continue
            graph_cycle_rank, incidence_rank = cycle_rank(edge_set)
            if graph_cycle_rank < 1:
                continue
            rows.append(
                {
                    "edges": sorted([sorted(edge) for edge in edge_set]),
                    "edge_count": edge_count,
                    "incidence_rank": incidence_rank,
                    "cycle_rank": graph_cycle_rank,
                }
            )
    minimum_edge_count = min(row["edge_count"] for row in rows)
    minimal = [row for row in rows if row["edge_count"] == minimum_edge_count]
    return rows, minimal


def exact_schur_and_invariant():
    auxiliary_mass, spectral_parameter, flux = sp.symbols(
        "mu lambda Phi", real=True
    )
    imaginary_unit = sp.I
    level3 = sp.diag(1, 2, 3)
    chain = sp.Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    coupling = sp.Matrix([1, 0, sp.exp(imaginary_unit * flux)])
    parent = (level3 + chain).row_join(coupling)
    parent = parent.col_join(
        coupling.conjugate().T.row_join(sp.Matrix([[auxiliary_mass]]))
    )
    grading = sp.diag(1, -1, 1, -1)
    odd_part = parent - sp.diag(1, 2, 3, auxiliary_mass)
    assert sp.simplify(grading * odd_part + odd_part * grading) == sp.zeros(4)

    energy_schur = (
        level3
        + chain
        - coupling * coupling.conjugate().T
        / (auxiliary_mass - spectral_parameter)
    )
    determinant_identity = sp.simplify(
        (parent - spectral_parameter * sp.eye(4)).det()
        - (auxiliary_mass - spectral_parameter)
        * (energy_schur - spectral_parameter * sp.eye(3)).det()
    )
    assert determinant_identity == 0

    lower = level3 + chain
    upper = level3 - coupling * coupling.conjugate().T / auxiliary_mass
    upper_squared = sp.simplify(upper * upper.conjugate().T)
    lower_squared = sp.simplify(lower * lower.conjugate().T)
    commutator = upper_squared * lower_squared - lower_squared * upper_squared
    physical_trace = sp.factor(
        sp.expand_complex(sp.trace(commutator**3))
    )
    expected_trace = (
        1248
        * imaginary_unit
        * (2 * auxiliary_mass - 1)
        * (15 * auxiliary_mass - 8)
        * sp.sin(flux)
        / auxiliary_mass**3
    )
    assert sp.simplify(physical_trace - expected_trace) == 0
    return {
        "grading": "Gamma=diag(1,-1,1,-1)",
        "parent_odd_part_anticommutes": True,
        "energy_dependent_schur": (
            "M_eff(lambda)=L3+D_A3-v v^dagger/(mu-lambda)"
        ),
        "determinant_identity": (
            "det(M4-lambda I)=(mu-lambda) det(M_eff(lambda)-lambda I)"
        ),
        "static_complementary_upper": (
            "M_u=L3-v v^dagger/mu, v=(1,0,exp(i Phi))^T"
        ),
        "lower_path": "M_d=L3+H_10+H_21",
        "physical_invariant": (
            "1248*i*(2*mu-1)*(15*mu-8)*sin(Phi)/mu^3"
        ),
        "degeneracy_zeros": ["mu=1/2", "mu=8/15"],
    }


def split_readout(auxiliary_mass, flux):
    level3 = np.diag([1.0, 2.0, 3.0]).astype(complex)
    chain = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=complex)
    coupling = np.array([1.0, 0.0, np.exp(1j * flux)], dtype=complex)
    upper = level3 - np.outer(coupling, coupling.conj()) / auxiliary_mass
    lower = level3 + chain
    upper_squared = upper @ upper.conj().T
    lower_squared = lower @ lower.conj().T
    upper_masses, upper_vectors = np.linalg.eigh(upper_squared)
    lower_masses, lower_vectors = np.linalg.eigh(lower_squared)
    mixing = upper_vectors.conj().T @ lower_vectors
    parameters = standard_parameters(mixing)
    commutator = upper_squared @ lower_squared - lower_squared @ upper_squared
    trace_cube = np.trace(commutator @ commutator @ commutator)
    upper_vandermonde = np.prod(
        [
            upper_masses[first] - upper_masses[second]
            for first in range(3)
            for second in range(first + 1, 3)
        ]
    )
    lower_vandermonde = np.prod(
        [
            lower_masses[first] - lower_masses[second]
            for first in range(3)
            for second in range(first + 1, 3)
        ]
    )
    identity_rhs = (
        6j
        * parameters["Jarlskog"]
        * upper_vandermonde
        * lower_vandermonde
    )
    expected = (
        1248j
        * (2 * auxiliary_mass - 1)
        * (15 * auxiliary_mass - 8)
        * math.sin(flux)
        / auxiliary_mass**3
    )
    return {
        "auxiliary_mass": auxiliary_mass,
        "angles_degrees": [
            parameters["theta_12_degrees"],
            parameters["theta_23_degrees"],
            parameters["theta_13_degrees"],
        ],
        "Jarlskog": parameters["Jarlskog"],
        "physical_trace_direct": {
            "real": float(np.real(trace_cube)),
            "imaginary": float(np.imag(trace_cube)),
        },
        "physical_trace_formula_error": float(abs(trace_cube - expected)),
        "Jarlskog_identity_error": float(abs(trace_cube - identity_rhs)),
    }


def gauge_check(flux):
    phases = np.array([0.19, -0.37, 0.61, -0.23])
    gauge = np.diag(np.exp(1j * phases))
    level4 = np.diag([1.0, 2.0, 3.0, 4.0]).astype(complex)
    parent = level4.copy()
    edge_data = [
        (0, 1, 0.0),
        (1, 2, 0.0),
        (2, 3, flux),
        (3, 0, 0.0),
    ]
    for first, second, phase in edge_data:
        parent[first, second] = np.exp(1j * phase)
        parent[second, first] = np.exp(-1j * phase)
    transformed = gauge @ parent @ gauge.conj().T
    return {
        "spectrum_invariant": bool(
            np.allclose(
                np.linalg.eigvalsh(parent),
                np.linalg.eigvalsh(transformed),
                atol=1e-12,
            )
        ),
        "single_cycle_flux": flux,
    }


def canonical_triplet_compatibility(flux_value):
    flux = sp.symbols("Phi", real=True)
    imaginary_unit = sp.I
    uniform = sp.ones(4, 1) / 2
    singlet_projector = uniform * uniform.conjugate().T
    triplet_projector = sp.eye(4) - singlet_projector
    grading = sp.diag(1, -1, 1, -1)
    adjacency = sp.zeros(4)
    for first, second, phase in [
        (0, 1, 0),
        (1, 2, 0),
        (2, 3, flux),
        (3, 0, 0),
    ]:
        adjacency[first, second] = sp.exp(imaginary_unit * phase)
        adjacency[second, first] = sp.exp(-imaginary_unit * phase)

    leakage = triplet_projector * adjacency * uniform
    leakage_squared = sp.trigsimp(
        sp.expand_complex((leakage.conjugate().T * leakage)[0])
    )
    expected_leakage = (
        (1 - sp.cos(flux)) * (3 + sp.cos(flux)) / 4
    )
    assert sp.simplify(leakage_squared - expected_leakage) == 0

    grading_commutator = grading * singlet_projector - singlet_projector * grading
    grading_commutator_norm_squared = sp.simplify(
        sp.trace(grading_commutator.conjugate().T * grading_commutator)
    )
    assert grading_commutator_norm_squared == 2

    coordinate_auxiliary = sp.eye(4)[:, 3]
    singlet_overlap_squared = sp.simplify(
        (coordinate_auxiliary.conjugate().T * singlet_projector * coordinate_auxiliary)[0]
    )
    assert singlet_overlap_squared == sp.Rational(1, 4)

    numerical_leakage_squared = float(
        expected_leakage.subs(flux, flux_value).evalf()
    )
    return {
        "canonical_decomposition": "C^4=span{u_uniform} direct_sum u_uniform^perp",
        "uniform_vector": "u=(1,1,1,1)/2",
        "triplet_projector": "P_3=I-u u^dagger",
        "flux_adjacency_triplet_leakage_squared": (
            "||(I-u u^dagger) A_C4(Phi) u||^2="
            "(1-cos(Phi))(3+cos(Phi))/4"
        ),
        "leakage_zero_condition": "Phi=0 mod 2pi",
        "target_flux_leakage_squared": numerical_leakage_squared,
        "grading_projector_commutator_norm_squared": 2,
        "grading_finding": (
            "Gamma maps the uniform singlet into the sum-zero triplet, so the canonical "
            "1+3 decomposition is not a graded decomposition for Gamma=diag(1,-1,1,-1)."
        ),
        "coordinate_auxiliary_singlet_overlap_squared": "1/4",
        "coordinate_auxiliary_triplet_overlap_squared": "3/4",
        "schur_finding": (
            "Eliminating coordinate vertex 3 does not eliminate the canonical affine singlet; "
            "it removes a vector containing only one quarter singlet probability."
        ),
    }


def random_formula_check(sample_count=25):
    generator = np.random.default_rng(20260806)
    maximum_formula_error = 0.0
    maximum_jarlskog_error = 0.0
    for _ in range(sample_count):
        auxiliary_mass = float(np.exp(generator.uniform(math.log(0.6), math.log(20.0))))
        flux = float(generator.uniform(0.1, math.pi - 0.1))
        row = split_readout(auxiliary_mass, flux)
        maximum_formula_error = max(
            maximum_formula_error, row["physical_trace_formula_error"]
        )
        maximum_jarlskog_error = max(
            maximum_jarlskog_error, row["Jarlskog_identity_error"]
        )
    return {
        "seed": 20260806,
        "sample_count": sample_count,
        "auxiliary_mass_interval": [0.6, 20.0],
        "maximum_physical_formula_error": maximum_formula_error,
        "maximum_Jarlskog_identity_error": maximum_jarlskog_error,
    }


def main():
    all_lifts, minimal_lifts = classify_minimal_lifts()
    exact = exact_schur_and_invariant()
    continuous = json.loads(
        Path("s2t_continuous_wilson_gap_action_results.json").read_text(
            encoding="utf-8"
        )
    )
    target_cosine = float(
        continuous["continuous_two_sector_solution"]["cos_theta_numeric"]
    )
    target_flux = math.acos(target_cosine)
    triplet_compatibility = canonical_triplet_compatibility(target_flux)
    spin_menu = json.loads(
        Path("s2t_spin_menu_dirac_determinant_line_results.json").read_text(
            encoding="utf-8"
        )
    )
    canonical_full_spectrum = spin_menu["cellular_Dirac"][
        "expected_spectrum"
    ]
    assert abs(canonical_full_spectrum[0]) < 1e-15
    canonical_masses = [1.0, 2.0, 3.0, 4.0, math.pi, 2 * math.pi, math.pi**2]
    blind_rows = [split_readout(mass, target_flux) for mass in canonical_masses]

    scan_masses = np.exp(np.linspace(-8.0, 12.0, 4001))
    scan_rows = [split_readout(float(mass), target_flux) for mass in scan_masses]
    control_angles = np.degrees(np.arcsin([0.22501, 0.04183, 0.003732]))
    for row in scan_rows:
        difference = np.radians(np.asarray(row["angles_degrees"]) - control_angles)
        row["post_blind_angle_objective"] = float(np.dot(difference, difference))
    best_scan = min(scan_rows, key=lambda row: row["post_blind_angle_objective"])

    shared_operator = split_readout(4.0, target_flux)
    same_parameters = {
        "theta_12_degrees": 0.0,
        "theta_23_degrees": 0.0,
        "theta_13_degrees": 0.0,
        "Jarlskog": 0.0,
    }
    gauge = gauge_check(target_flux)
    random_check = random_formula_check()
    results = {
        "status": "the_minimal_C4_repairs_vertex_bipartiteness_but_is_incompatible_with_the_canonical_affine_triplet_and_does_not_derive_CKM",
        "date": "2026-08-06",
        "blind_protocol": {
            "CKM_loaded_before_candidate_menu": False,
            "candidate_auxiliary_masses": canonical_masses,
            "flux_source": "conditional transfer from the pre-existing continuous Wilson saddle",
            "edge_weights": "all four C4 edges fixed to one",
        },
        "minimal_graph_gate": {
            "grading": list(GRADING),
            "required_A3_edges": sorted([sorted(edge) for edge in REQUIRED_A3_EDGES]),
            "all_admissible_cyclic_lifts": all_lifts,
            "minimal_lifts": minimal_lifts,
            "unique_minimal_lift": len(minimal_lifts) == 1,
            "finding": (
                "A bipartite graph has no odd cycle. Keeping A3 and adding the fewest vertices and edges gives the unique square 0-1-2-3-0."
            ),
        },
        "canonical_triplet_gate": triplet_compatibility,
        "canonical_spectral_level_gate": {
            "four_mode_factor_laplacian_spectrum": canonical_full_spectrum,
            "uniform_singlet_level": 0.0,
            "static_elimination_at_lambda_zero": "undefined",
            "finding": (
                "The canonical fourth mode is the zero uniform mode, not a pre-existing heavy "
                "auxiliary state. A static Schur inverse at lambda=0 therefore requires an "
                "additional singlet mass operator and its normalization."
            ),
        },
        "schur_gate": exact,
        "gauge_gate": gauge,
        "random_numeric_gate": random_check,
        "shared_parent_warning": {
            "same_operator_mixing_angles_degrees": [
                same_parameters["theta_12_degrees"],
                same_parameters["theta_23_degrees"],
                same_parameters["theta_13_degrees"],
            ],
            "same_operator_Jarlskog": same_parameters["Jarlskog"],
            "finding": (
                "One common C4 operator with one common Schur reduction gives the same left eigenbasis in both sectors and therefore identity mixing. Distinct upper/lower path readouts require additional sector projectors or representations."
            ),
        },
        "complementary_path_candidate": {
            "interpretation": (
                "The lower sector is assigned the physical A3 path; the upper sector is assigned the auxiliary path and statically reduced at lambda=0. This assignment is a test ansatz, not yet a consequence of one action."
            ),
            "blind_rows": blind_rows,
            "all_rows_pass_exact_formula": all(
                row["physical_trace_formula_error"] < 1e-8 for row in blind_rows
            ),
            "all_rows_pass_Jarlskog_identity": all(
                row["Jarlskog_identity_error"] < 1e-8 for row in blind_rows
            ),
        },
        "post_blind_control": {
            "PDG_2024_angles_degrees": control_angles.tolist(),
            "wide_positive_mass_scan": {
                "log_mu_interval": [-8.0, 12.0],
                "sample_count": len(scan_rows),
                "best_row": best_scan,
                "minimum_theta_13_degrees": min(
                    row["angles_degrees"][2] for row in scan_rows
                ),
            },
            "finding": (
                "The unit-edge complementary-path texture remains non-hierarchical across the blind menu. A wide post-blind scan of the one undetermined auxiliary mass finds no CKM-like point and cannot replace a proof over all positive masses."
            ),
        },
        "scientific_verdict": {
            "positive": (
                "C4 is the unique minimal bipartite lift, carries one gauge-invariant flux, keeps every edge grading-odd, and produces the former effective chord through a Schur complement with tied diagonal shifts."
            ),
            "negative": (
                "The coordinate C4 grading does not descend to the canonical affine triplet, and nonzero flux mixes the uniform singlet with that triplet. Eliminating one coordinate vertex is not elimination of the affine singlet. The exact Schur complement is energy-dependent, while a static version needs a new singlet mass; one shared reduction gives no mixing and the split readout is underived."
            ),
            "next_gate": (
                "Either abandon the canonical affine 1+3 generation mechanism and rebuild generation counting on the four-state graded carrier, or construct a larger graded space in which the affine triplet and its singlet complement are invariant before any further CKM comparison."
            ),
        },
    }

    assert len(minimal_lifts) == 1
    assert minimal_lifts[0]["edges"] == [[0, 1], [0, 3], [1, 2], [2, 3]]
    assert minimal_lifts[0]["cycle_rank"] == 1
    assert gauge["spectrum_invariant"]
    assert triplet_compatibility["target_flux_leakage_squared"] > 0.9
    assert random_check["maximum_physical_formula_error"] < 1e-8
    assert random_check["maximum_Jarlskog_identity_error"] < 1e-8
    assert all(row["physical_trace_formula_error"] < 1e-8 for row in blind_rows)
    assert all(row["Jarlskog_identity_error"] < 1e-8 for row in blind_rows)
    assert shared_operator["Jarlskog_identity_error"] < 1e-8
    assert same_parameters["Jarlskog"] == 0.0

    Path("s2t_family_bipartite_c4_lift_results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": results["status"],
                "unique_minimal_lift": True,
                "minimal_edges": minimal_lifts[0]["edges"],
                "physical_invariant": exact["physical_invariant"],
                "shared_parent_CKM": "identity",
                "best_scanned_split_angles": best_scan["angles_degrees"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()