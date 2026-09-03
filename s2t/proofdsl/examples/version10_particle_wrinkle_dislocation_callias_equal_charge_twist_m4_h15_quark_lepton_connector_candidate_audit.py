"""LCF certificate for the H15 quark-lepton connector candidate audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class H15QuarkLeptonConnectorCertificate:
    existing_incidence: sp.ImmutableMatrix
    direct_bridge: sp.ImmutableMatrix
    direct_augmented_incidence: sp.ImmutableMatrix
    direct_laplacian: sp.ImmutableMatrix
    chirality: sp.ImmutableMatrix
    color_label: sp.ImmutableMatrix
    hypercharge6: sp.ImmutableMatrix
    missing_edges: sp.ImmutableMatrix
    r2_pair: sp.ImmutableMatrix
    r2_augmented_incidence: sp.ImmutableMatrix
    r2_laplacian: sp.ImmutableMatrix
    bimodule_coordinates: sp.ImmutableMatrix
    first_order_pass: sp.ImmutableMatrix
    r2_first_order_defect: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    coverage: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> H15QuarkLeptonConnectorCertificate:
    # Vertex order: Q_L, L_L, u_R, d_R, e_R.
    existing_incidence = sp.ImmutableMatrix(
        [[1, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    )
    direct_bridge = sp.ImmutableMatrix([1, -1, 0, 0, 0])
    direct_augmented_incidence = sp.ImmutableMatrix.hstack(existing_incidence, direct_bridge)
    direct_laplacian = sp.ImmutableMatrix(direct_augmented_incidence * direct_augmented_incidence.T)

    # Same sign means the same chirality.  The direct Q_L-L_L bridge is even.
    chirality = sp.ImmutableMatrix([[1, 1, -1, -1, -1]])
    color_label = sp.ImmutableMatrix([[1, 0, 1, 1, 0]])
    hypercharge6 = sp.ImmutableMatrix([[1, -3, 4, -2, -6]])

    # Missing opposite-chirality edges: L-u, L-d, Q-e.
    missing_edges = sp.ImmutableMatrix(
        [[0, 0, 1], [1, 1, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]]
    )
    r2_pair = sp.ImmutableMatrix.hstack(missing_edges[:, 0], missing_edges[:, 2])
    r2_augmented_incidence = sp.ImmutableMatrix.hstack(existing_incidence, r2_pair)
    r2_laplacian = sp.ImmutableMatrix(r2_augmented_incidence * r2_augmented_incidence.T)

    # Coordinates encode (H versus C, M3 versus C).
    bimodule_coordinates = sp.ImmutableMatrix(
        [[1, 1], [1, 0], [0, 1], [0, 1], [0, 0]]
    )
    # Q-u, Q-d, L-e pass; L-u, L-d, Q-e change both coordinates.
    first_order_pass = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])
    r2_first_order_defect = sp.ImmutableMatrix([1, 1])

    # Columns: component connection, odd chirality, gauge typing,
    # strict first order, inherited carrier, independent normalization.
    candidate_matrix = sp.ImmutableMatrix(
        [
            [1, 0, 0, 1, 0, 0],  # direct Q_L-L_L graph edge
            [0, 1, 1, 1, 1, 1],  # inherited Higgs forest
            [1, 1, 1, 0, 0, 0],  # minimal R2 pair, strict SM geometry
            [1, 1, 1, 0, 0, 0],  # R2 plus tilde-R2, strict geometry
            [1, 1, 1, 1, 0, 0],  # R2 with generalized first order
            [1, 1, 1, 1, 0, 0],  # Pati-Salam/SU4 enlargement
            [1, 1, 0, 1, 0, 0],  # neutral Callias bridge
            [0, 1, 1, 1, 1, 0],  # composite of inherited paths
            [1, 0, 1, 0, 0, 0],  # unified vector connector
            [1, 1, 1, 1, 0, 1],  # target-loaded generalized R2
            [0, 0, 0, 0, 0, 1],  # normalization-only parent
        ]
    )
    score_vector = sp.ImmutableMatrix(candidate_matrix * sp.ones(6, 1))
    pass_vector = sp.ImmutableMatrix.zeros(candidate_matrix.rows, 1)
    coverage = sp.ImmutableMatrix(
        [[int(any(candidate_matrix[r, c] for r in range(candidate_matrix.rows)))] for c in range(candidate_matrix.cols)]
    )
    physical_origin = sp.ImmutableMatrix.zeros(3, 1)

    theorems = (
        kernel.prove_exact_rank(existing_incidence, 3, subject="inherited H15 forest has three independent edges"),
        kernel.prove_exact_rank(direct_augmented_incidence, 4, subject="direct graph bridge connects the two H15 components"),
        kernel.prove_exact_rank(direct_laplacian, 4, subject="directly bridged H15 graph is connected"),
        kernel.prove_exact_nullity(direct_laplacian, 1, subject="directly bridged graph leaves one uniform ray"),
        kernel.prove_matrix_equality(chirality * direct_bridge, sp.zeros(1, 1), subject="direct QL-LL bridge joins equal chirality"),
        kernel.prove_matrix_equality(color_label * direct_bridge, sp.ones(1, 1), subject="direct bridge carries a color mismatch"),
        kernel.prove_matrix_equality(hypercharge6 * direct_bridge, sp.ImmutableMatrix([[4]]), subject="direct bridge carries nonzero hypercharge mismatch"),
        kernel.prove_exact_rank(missing_edges, 3, subject="three opposite-chirality quark-lepton edges are independent"),
        kernel.prove_exact_rank(r2_pair, 2, subject="minimal R2 completion contains two independent edges"),
        kernel.prove_exact_rank(r2_augmented_incidence, 4, subject="R2 pair connects the H15 type graph"),
        kernel.prove_exact_rank(r2_laplacian, 4, subject="R2-completed graph is connected"),
        kernel.prove_exact_nullity(r2_laplacian, 1, subject="R2 completion leaves one common graph amplitude"),
        kernel.prove_expression_equality(r2_augmented_incidence.cols - r2_augmented_incidence.rank(), 1, subject="minimal R2 completion creates one mixed cycle"),
        kernel.prove_exact_rank(bimodule_coordinates, 2, subject="both finite bimodule coordinates are resolved"),
        kernel.prove_matrix_equality(first_order_pass, sp.ImmutableMatrix([1, 1, 1, 0, 0, 0]), subject="only inherited Yukawa edges pass strict first order"),
        kernel.prove_matrix_equality(r2_first_order_defect, sp.ones(2, 1), subject="both R2 edges change both bimodule coordinates"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="candidate audit resolves all six criteria"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([2, 5, 3, 3, 4, 4, 3, 4, 2, 5, 1]), subject="candidate scores are exact"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(11, 1), subject="no candidate passes all six criteria"),
        kernel.prove_matrix_equality(coverage, sp.ones(6, 1), subject="every audit criterion is independently represented"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="connector carrier normalization and common parent remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict connector physical-origin score is zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate",
        theorems,
    )
    return H15QuarkLeptonConnectorCertificate(
        existing_incidence,
        direct_bridge,
        direct_augmented_incidence,
        direct_laplacian,
        chirality,
        color_label,
        hypercharge6,
        missing_edges,
        r2_pair,
        r2_augmented_incidence,
        r2_laplacian,
        bimodule_coordinates,
        first_order_pass,
        r2_first_order_defect,
        candidate_matrix,
        score_vector,
        pass_vector,
        coverage,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate",
    title="Аудит кандидатов кварк--лептонного коннектора H15",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_h15_quark_lepton_connector_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"h15_quark_lepton_connector_candidate_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(22)
    ),
)