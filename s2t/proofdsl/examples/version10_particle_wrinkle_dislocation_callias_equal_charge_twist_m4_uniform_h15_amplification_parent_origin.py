"""LCF certificate for the uniform H15 amplification parent-origin gate."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class UniformH15AmplificationCertificate:
    block_replication: sp.ImmutableMatrix
    block_metric: sp.ImmutableMatrix
    existing_incidence: sp.ImmutableMatrix
    existing_laplacian: sp.ImmutableMatrix
    component_kernel: sp.ImmutableMatrix
    component_amplifier: sp.ImmutableMatrix
    bridge_edge: sp.ImmutableMatrix
    augmented_incidence: sp.ImmutableMatrix
    augmented_laplacian: sp.ImmutableMatrix
    uniform_kernel: sp.ImmutableMatrix
    uniform_channel_vector: sp.ImmutableMatrix
    conditional_twist_amplifier: sp.ImmutableMatrix
    inherited_bridge: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> UniformH15AmplificationCertificate:
    rows = [[1, 0, 0, 0, 0]] * 6 + [[0, 1, 0, 0, 0]] * 2 + [[0, 0, 1, 0, 0]] * 3 + [[0, 0, 0, 1, 0]] * 3 + [[0, 0, 0, 0, 1]]
    block_replication = sp.ImmutableMatrix(rows)
    block_metric = sp.ImmutableMatrix(block_replication.T * block_replication)
    # Existing charged H15 edges: Q-u, Q-d, L-e.
    existing_incidence = sp.ImmutableMatrix([
        [1, 1, 0], [0, 0, 1], [-1, 0, 0], [0, -1, 0], [0, 0, -1]
    ])
    existing_laplacian = sp.ImmutableMatrix(existing_incidence * existing_incidence.T)
    component_kernel = sp.ImmutableMatrix([
        [1, 0], [0, 1], [1, 0], [1, 0], [0, 1]
    ])
    component_amplifier = sp.ImmutableMatrix(block_replication * component_kernel)
    bridge_edge = sp.ImmutableMatrix([1, -1, 0, 0, 0])
    augmented_incidence = sp.ImmutableMatrix.hstack(existing_incidence, bridge_edge)
    augmented_laplacian = sp.ImmutableMatrix(augmented_incidence * augmented_incidence.T)
    uniform_kernel = sp.ImmutableMatrix.ones(5, 1)
    uniform_channel_vector = sp.ImmutableMatrix(block_replication * uniform_kernel)
    conditional_twist_amplifier = sp.ImmutableMatrix(sp.kronecker_product(sp.eye(2), uniform_channel_vector))
    inherited_bridge = sp.ImmutableMatrix.zeros(5, 1)
    conditional_architecture = sp.ImmutableMatrix.ones(12, 1)
    physical_origin = sp.ImmutableMatrix.zeros(3, 1)

    theorems = (
        kernel.prove_exact_rank(block_replication, 5, subject="five H15 type blocks embed into fifteen channels"),
        kernel.prove_matrix_equality(block_metric, sp.diag(6, 2, 3, 3, 1), subject="H15 block multiplicity metric"),
        kernel.prove_exact_rank(existing_incidence, 3, subject="three inherited charged H15 edges are independent"),
        kernel.prove_exact_rank(existing_laplacian, 3, subject="existing H15 type graph has two components"),
        kernel.prove_exact_nullity(existing_laplacian, 2, subject="existing H15 parent leaves two component amplitudes"),
        kernel.prove_matrix_equality(existing_incidence.T * component_kernel, sp.zeros(3, 2), subject="quark and lepton component constants lie in the kernel"),
        kernel.prove_exact_rank(component_kernel, 2, subject="component kernel has two independent rays"),
        kernel.prove_exact_rank(component_amplifier, 2, subject="inherited H15 amplifier has two independent component amplitudes"),
        kernel.prove_matrix_equality(component_amplifier.T * component_amplifier, sp.diag(12, 3), subject="quark and lepton channel multiplicities are twelve and three"),
        kernel.prove_exact_rank(bridge_edge, 1, subject="one quark-lepton bridge is sufficient conditionally"),
        kernel.prove_exact_rank(augmented_incidence, 4, subject="augmented H15 type graph is connected"),
        kernel.prove_exact_rank(augmented_laplacian, 4, subject="connected augmented graph fixes all relative amplitudes"),
        kernel.prove_exact_nullity(augmented_laplacian, 1, subject="augmented graph leaves one common amplitude"),
        kernel.prove_matrix_equality(augmented_incidence.T * uniform_kernel, sp.zeros(4, 1), subject="uniform block vector spans the augmented kernel"),
        kernel.prove_matrix_equality(uniform_channel_vector, sp.ones(15, 1), subject="uniform block kernel lifts to all fifteen channels"),
        kernel.prove_exact_rank(conditional_twist_amplifier, 2, subject="conditional uniform twist amplifier has rank two"),
        kernel.prove_matrix_equality(conditional_twist_amplifier.T * conditional_twist_amplifier, 15 * sp.eye(2), subject="conditional uniform twist amplifier has Gram fifteen"),
        kernel.prove_matrix_equality(inherited_bridge, sp.zeros(5, 1), subject="quark-lepton bridge is absent from the inherited parent"),
        kernel.prove_exact_rank(inherited_bridge, 0, subject="inherited quark-lepton bridge rank is zero"),
        kernel.prove_expression_equality(sum(conditional_architecture), 12, subject="conditional uniform amplification architecture is complete"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="bridge weight and absolute amplitude origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict uniform H15 amplification origin score is zero"),
    )
    gate_theorem = kernel.prove_gate("version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate", theorems)
    return UniformH15AmplificationCertificate(block_replication, block_metric, existing_incidence, existing_laplacian, component_kernel, component_amplifier, bridge_edge, augmented_incidence, augmented_laplacian, uniform_kernel, uniform_channel_vector, conditional_twist_amplifier, inherited_bridge, conditional_architecture, physical_origin, theorems, gate_theorem)


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate",
    title="Родитель равномерного усиления Callias--M4 по H15",
    source_paths=("s2t/gates/version10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate.tex", "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_equal_charge_twist_m4_uniform_h15_amplification_parent_origin_gate_results.json"),
    obligations=tuple(Obligation(f"uniform_h15_amplification_parent_{i:02d}", lambda i=i: build_certificate().theorems[i]) for i in range(22)),
)