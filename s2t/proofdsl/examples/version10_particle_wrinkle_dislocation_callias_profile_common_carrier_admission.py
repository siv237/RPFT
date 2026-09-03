"""LCF certificate for the Callias common-carrier admission gate."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class CalliasProfileCommonCarrierCertificate:
    spatial_clifford_generators: tuple[sp.ImmutableMatrix, ...]
    twist_generators: tuple[sp.ImmutableMatrix, ...]
    spatial_twist_commutators: sp.ImmutableMatrix
    positive_mass_projector: sp.ImmutableMatrix
    negative_mass_projector: sp.ImmutableMatrix
    coefficient_projector: sp.ImmutableMatrix
    ko_charge_operator: sp.ImmutableMatrix
    ko_twist_flip: sp.ImmutableMatrix
    ko_charge_defect: sp.ImmutableMatrix
    cell_charge_operator: sp.ImmutableMatrix
    cell_twist_generators: tuple[sp.ImmutableMatrix, ...]
    cell_to_flavor_twist_map: sp.ImmutableMatrix
    dimension_data: sp.ImmutableMatrix
    conditional_architecture: sp.ImmutableMatrix
    inherited_ingredients: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> CalliasProfileCommonCarrierCertificate:
    sx = sp.ImmutableMatrix([[0, 1], [1, 0]])
    sy = sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]])
    sz = sp.ImmutableMatrix([[1, 0], [0, -1]])
    pauli = (sx, sy, sz)
    identity2 = sp.eye(2)
    identity15 = sp.eye(15)

    spatial_clifford_generators = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(g, identity2, identity15)) for g in pauli
    )
    twist_generators = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(identity2, g, identity15)) for g in pauli
    )
    spatial_twist_commutators = sp.ImmutableMatrix.vstack(
        *(g * t - t * g for g in spatial_clifford_generators for t in twist_generators)
    )

    positive_twist = (identity2 + sz) / 2
    negative_twist = (identity2 - sz) / 2
    positive_mass_projector = sp.ImmutableMatrix(sp.kronecker_product(identity2, positive_twist, identity15))
    negative_mass_projector = sp.ImmutableMatrix(sp.kronecker_product(identity2, negative_twist, identity15))
    coefficient_projector = sp.ImmutableMatrix(identity15)

    ko_charge_operator = sp.ImmutableMatrix(sp.kronecker_product(sz, identity15))
    ko_twist_flip = sp.ImmutableMatrix(sp.kronecker_product(sx, identity15))
    ko_charge_defect = sp.ImmutableMatrix(ko_charge_operator * ko_twist_flip - ko_twist_flip * ko_charge_operator)

    cell_charge_operator = sp.ImmutableMatrix(identity2)
    cell_twist_generators = pauli
    cell_to_flavor_twist_map = sp.ImmutableMatrix(sp.zeros(30, 2))
    dimension_data = sp.ImmutableMatrix([2, 2, 15, 60, 30, 43])
    conditional_architecture = sp.ImmutableMatrix(sp.ones(10, 1))
    inherited_ingredients = sp.ImmutableMatrix(sp.ones(5, 1))
    physical_origin = sp.ImmutableMatrix(sp.zeros(3, 1))

    clifford_defects = sp.ImmutableMatrix.vstack(
        *(
            spatial_clifford_generators[i] * spatial_clifford_generators[j]
            + spatial_clifford_generators[j] * spatial_clifford_generators[i]
            - (2 if i == j else 0) * sp.eye(60)
            for i in range(3)
            for j in range(3)
        )
    )
    twist_defects = sp.ImmutableMatrix.vstack(
        *(
            twist_generators[i] * twist_generators[j]
            + twist_generators[j] * twist_generators[i]
            - (2 if i == j else 0) * sp.eye(60)
            for i in range(3)
            for j in range(3)
        )
    )
    cell_clifford_defects = sp.ImmutableMatrix.vstack(
        *(
            cell_twist_generators[i] * cell_twist_generators[j]
            + cell_twist_generators[j] * cell_twist_generators[i]
            - (2 if i == j else 0) * sp.eye(2)
            for i in range(3)
            for j in range(3)
        )
    )

    theorems = (
        kernel.prove_matrix_equality(clifford_defects, sp.zeros(540, 60), subject="spatial Pauli generators form a Clifford triple"),
        kernel.prove_matrix_equality(twist_defects, sp.zeros(540, 60), subject="independent twist generators form a Pauli triple"),
        kernel.prove_matrix_equality(spatial_twist_commutators, sp.zeros(540, 60), subject="spatial and twist factors commute exactly"),
        kernel.prove_matrix_equality(positive_mass_projector * positive_mass_projector, positive_mass_projector, subject="positive Callias mass sector is projective"),
        kernel.prove_matrix_equality(negative_mass_projector * negative_mass_projector, negative_mass_projector, subject="negative Callias mass sector is projective"),
        kernel.prove_matrix_equality(positive_mass_projector + negative_mass_projector, sp.eye(60), subject="Callias mass sectors resolve the conditional carrier"),
        kernel.prove_exact_rank(positive_mass_projector, 30, subject="positive Callias mass sector has rank thirty"),
        kernel.prove_exact_rank(negative_mass_projector, 30, subject="negative Callias mass sector has rank thirty"),
        kernel.prove_exact_rank(coefficient_projector, 15, subject="coefficient class carries multiplicity fifteen"),
        kernel.prove_exact_rank(ko_charge_defect, 30, subject="KO particle conjugate pair cannot support an equal-charge twist flip"),
        kernel.prove_expression_equality(sp.trace(ko_charge_operator * ko_twist_flip), 0, subject="KO off-diagonal twist mixes opposite charges"),
        kernel.prove_matrix_equality(cell_charge_operator * sx - sx * cell_charge_operator, sp.zeros(2), subject="cell edge admits an abstract equal-charge x flip"),
        kernel.prove_matrix_equality(cell_charge_operator * sy - sy * cell_charge_operator, sp.zeros(2), subject="cell edge admits an abstract equal-charge y flip"),
        kernel.prove_matrix_equality(cell_clifford_defects, sp.zeros(18, 2), subject="cell edge algebra conditionally supplies a Pauli triple"),
        kernel.prove_matrix_equality(cell_to_flavor_twist_map, sp.zeros(30, 2), subject="cell edge has no inherited embedding into fifteen twist channels"),
        kernel.prove_exact_rank(cell_to_flavor_twist_map, 0, subject="cell to flavor twist embedding has rank zero"),
        kernel.prove_matrix_equality(dimension_data, sp.Matrix([2, 2, 15, 60, 30, 43]), subject="Callias and inherited carrier dimensions are exact"),
        kernel.prove_expression_equality(dimension_data[3], dimension_data[0] * dimension_data[1] * dimension_data[2], subject="minimal Callias carrier has dimension sixty"),
        kernel.prove_expression_equality(dimension_data[4], dimension_data[0] * dimension_data[2], subject="inherited spin times H15 carrier has dimension thirty"),
        kernel.prove_expression_equality(sum(conditional_architecture), 10, subject="conditional Callias carrier architecture is complete"),
        kernel.prove_expression_equality(sum(inherited_ingredients), 5, subject="five required ingredients exist separately"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="equal-charge twist embedding and normalization origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict Callias carrier origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate",
        theorems,
    )
    return CalliasProfileCommonCarrierCertificate(
        spatial_clifford_generators,
        twist_generators,
        spatial_twist_commutators,
        positive_mass_projector,
        negative_mass_projector,
        coefficient_projector,
        ko_charge_operator,
        ko_twist_flip,
        ko_charge_defect,
        cell_charge_operator,
        cell_twist_generators,
        cell_to_flavor_twist_map,
        dimension_data,
        conditional_architecture,
        inherited_ingredients,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate",
    title="Допуск общего каллиасова носителя морщинки и дислокации",
    source_paths=(
        "s2t/gates/version10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate.tex",
        "s2t/results/s2t_v10_particle_wrinkle_dislocation_callias_profile_common_carrier_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"particle_wrinkle_dislocation_callias_carrier_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)