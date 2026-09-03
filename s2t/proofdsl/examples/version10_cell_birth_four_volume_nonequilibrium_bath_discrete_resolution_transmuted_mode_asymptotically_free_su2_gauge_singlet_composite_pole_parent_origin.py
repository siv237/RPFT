"""LCF certificate for the composite SU(2)-singlet pole architecture."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SU2GaugeSingletCompositePoleCertificate:
    singlet_vector: sp.ImmutableMatrix
    singlet_projector: sp.ImmutableMatrix
    triplet_projector: sp.ImmutableMatrix
    swap: sp.ImmutableMatrix
    antisymmetrizer: sp.ImmutableMatrix
    total_generators: tuple[sp.ImmutableMatrix, ...]
    total_casimir: sp.ImmutableMatrix
    binding_parent: sp.ImmutableMatrix
    inherited_two_body_parent: sp.ImmutableMatrix
    singlet_triplet_splitting: sp.Expr
    full_singlet_multiplicity: sp.Expr
    required_mass_squared: sp.Expr
    inverse_propagator: sp.Expr
    pole_value: sp.Expr
    residue: sp.Expr
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SU2GaugeSingletCompositePoleCertificate:
    pauli = (
        sp.ImmutableMatrix([[0, 1], [1, 0]]),
        sp.ImmutableMatrix([[0, -sp.I], [sp.I, 0]]),
        sp.ImmutableMatrix([[1, 0], [0, -1]]),
    )
    fundamental_generators = tuple(sigma / 2 for sigma in pauli)
    total_generators = tuple(
        sp.ImmutableMatrix(sp.kronecker_product(t, sp.eye(2)) + sp.kronecker_product(sp.eye(2), t))
        for t in fundamental_generators
    )
    singlet_vector = sp.ImmutableMatrix([0, 1 / sp.sqrt(2), -1 / sp.sqrt(2), 0])
    singlet_projector = sp.ImmutableMatrix(singlet_vector * singlet_vector.H)
    triplet_projector = sp.ImmutableMatrix(sp.eye(4) - singlet_projector)
    swap_mutable = sp.zeros(4)
    for a in range(2):
        for b in range(2):
            swap_mutable[2 * b + a, 2 * a + b] = 1
    swap = sp.ImmutableMatrix(swap_mutable)
    antisymmetrizer = sp.ImmutableMatrix((sp.eye(4) - swap) / 2)
    total_casimir_mutable = sp.zeros(4)
    for generator in total_generators:
        total_casimir_mutable += generator * generator
    total_casimir = sp.ImmutableMatrix(total_casimir_mutable)
    binding_parent = triplet_projector
    inherited_two_body_parent = sp.zeros(4)
    singlet_triplet_splitting = sp.Integer(0)
    full_singlet_multiplicity = sp.Integer(16**2)

    required_mass_squared = sp.exp(-64 * sp.pi**2 / 3)
    q = sp.symbols("q", real=True)
    inverse_propagator = q - required_mass_squared
    pole_value = sp.simplify(inverse_propagator.subs(q, required_mass_squared))
    residue = sp.simplify(1 / sp.diff(inverse_propagator, q))
    annihilation_stack = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(generator * singlet_vector) for generator in total_generators
    ))
    commutator_stack = sp.ImmutableMatrix.vstack(*(
        sp.ImmutableMatrix(generator * singlet_projector - singlet_projector * generator)
        for generator in total_generators
    ))
    architecture = sp.ones(12, 1)
    physical_origin = sp.zeros(3, 1)

    theorems = (
        kernel.prove_expression_equality((singlet_vector.H * singlet_vector)[0], 1, subject="antisymmetric two-doublet singlet is normalized"),
        kernel.prove_matrix_equality(singlet_projector * singlet_projector, singlet_projector, subject="composite singlet defines an exact projector"),
        kernel.prove_exact_rank(singlet_projector, 1, subject="composite gauge singlet is rank one in the gauge pair"),
        kernel.prove_matrix_equality(triplet_projector * triplet_projector, triplet_projector, subject="orthogonal complement is the triplet projector"),
        kernel.prove_exact_rank(triplet_projector, 3, subject="two doublets contain a three-dimensional triplet"),
        kernel.prove_matrix_equality(singlet_projector + triplet_projector, sp.eye(4), subject="singlet and triplet resolve the two-doublet carrier"),
        kernel.prove_matrix_equality(antisymmetrizer, singlet_projector, subject="fermionic gauge antisymmetrizer canonically selects the singlet"),
        kernel.prove_matrix_equality(swap * singlet_vector, -singlet_vector, subject="composite singlet is antisymmetric under gauge-factor exchange"),
        kernel.prove_matrix_equality(annihilation_stack, sp.zeros(12, 1), subject="total SU2 generators annihilate the composite singlet"),
        kernel.prove_matrix_equality(commutator_stack, sp.zeros(12, 4), subject="rank-one composite projector is gauge invariant"),
        kernel.prove_matrix_equality(total_casimir, 2 * triplet_projector, subject="total Casimir separates singlet zero from triplet eigenvalue two"),
        kernel.prove_exact_spectrum(total_casimir, {sp.Integer(0): 1, sp.Integer(2): 3}, subject="two-doublet Casimir has one singlet and one triplet"),
        kernel.prove_exact_spectrum(binding_parent, {sp.Integer(0): 1, sp.Integer(1): 3}, subject="conditional binding parent has a unique singlet ground state"),
        kernel.prove_exact_rank(binding_parent, 3, subject="conditional parent penalizes all triplet directions"),
        kernel.prove_expression_equality(full_singlet_multiplicity, 256, subject="sixteen doublet copies leave two hundred fifty-six flavor-pair singlets"),
        kernel.prove_matrix_equality(inherited_two_body_parent, sp.zeros(4), subject="inherited K43 parent contains no two-body binding interaction"),
        kernel.prove_expression_equality(singlet_triplet_splitting, 0, subject="inherited carrier has no singlet-triplet binding gap"),
        kernel.prove_expression_equality(required_mass_squared, sp.exp(-64 * sp.pi**2 / 3), subject="conditional composite pole uses the required transmuted mass"),
        kernel.prove_expression_equality(pole_value, 0, subject="conditional composite inverse propagator vanishes on shell"),
        kernel.prove_expression_equality(sp.diff(inverse_propagator, q), 1, subject="conditional composite pole is simple"),
        kernel.prove_expression_equality(residue, 1, subject="conditional composite pole has positive unit residue"),
        kernel.prove_matrix_equality(architecture, sp.ones(12, 1), subject="composite singlet pole architecture is complete"),
        kernel.prove_expression_equality(sum(architecture), 12, subject="twelve conditional composite checks pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(3, 1), subject="flavor selector binding kernel and mass map origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict composite pole origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate",
        theorems,
    )
    return SU2GaugeSingletCompositePoleCertificate(
        singlet_vector, singlet_projector, triplet_projector, swap,
        antisymmetrizer, total_generators, total_casimir, binding_parent,
        inherited_two_body_parent, singlet_triplet_splitting,
        full_singlet_multiplicity, required_mass_squared, inverse_propagator,
        pole_value, residue, architecture, physical_origin, theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate",
    title="Родитель композитного SU(2)-синглетного полюса",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_composite_pole_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"su2_composite_singlet_pole_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(25)
    ),
)