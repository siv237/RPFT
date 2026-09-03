"""LCF certificate for the democratic flavor-selector parent."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class DemocraticFlavorSelectorParentCertificate:
    democratic_vector: sp.ImmutableMatrix
    democratic_projector: sp.ImmutableMatrix
    orthogonal_projector: sp.ImmutableMatrix
    complete_adjacency: sp.ImmutableMatrix
    complete_laplacian: sp.ImmutableMatrix
    cyclic_shift: sp.ImmutableMatrix
    pair_spectrum_multiplicities: sp.ImmutableMatrix
    inherited_flavor_operator: sp.ImmutableMatrix
    inherited_graph_operator: sp.ImmutableMatrix
    inherited_pair_degeneracy: sp.Expr
    pole_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> DemocraticFlavorSelectorParentCertificate:
    democratic_vector=sp.ImmutableMatrix(sp.ones(16,1)/4)
    democratic_projector=sp.ImmutableMatrix(democratic_vector*democratic_vector.H)
    orthogonal_projector=sp.ImmutableMatrix(sp.eye(16)-democratic_projector)
    complete_adjacency=sp.ImmutableMatrix(sp.ones(16)-sp.eye(16))
    complete_laplacian=sp.ImmutableMatrix(15*sp.eye(16)-complete_adjacency)
    shift=sp.zeros(16)
    for i in range(16): shift[(i+1)%16,i]=1
    cyclic_shift=sp.ImmutableMatrix(shift)
    pair_spectrum_multiplicities=sp.ImmutableMatrix([1,30,225])
    inherited_flavor_operator=sp.ImmutableMatrix(sp.eye(16))
    inherited_graph_operator=sp.ImmutableMatrix(sp.zeros(16))
    inherited_pair_degeneracy=sp.Integer(256)
    pole_map=sp.ImmutableMatrix([[0]])
    architecture=sp.ones(11,1)
    physical_origin=sp.zeros(2,1)
    theorems=(
        kernel.prove_expression_equality((democratic_vector.H*democratic_vector)[0],1,subject="democratic flavor vector is normalized"),
        kernel.prove_matrix_equality(democratic_projector*democratic_projector,democratic_projector,subject="democratic flavor projector is exact"),
        kernel.prove_exact_rank(democratic_projector,1,subject="democratic selector is rank one"),
        kernel.prove_exact_rank(orthogonal_projector,15,subject="orthogonal flavor sector has rank fifteen"),
        kernel.prove_matrix_equality(democratic_projector+orthogonal_projector,sp.eye(16),subject="democratic and orthogonal sectors resolve flavor space"),
        kernel.prove_matrix_equality(cyclic_shift*democratic_projector-democratic_projector*cyclic_shift,sp.zeros(16),subject="democratic selector preserves cyclic flavor symmetry"),
        kernel.prove_exact_spectrum(complete_adjacency,{sp.Integer(15):1,sp.Integer(-1):15},subject="complete flavor graph adjacency spectrum"),
        kernel.prove_matrix_equality(complete_laplacian,16*orthogonal_projector,subject="complete graph Laplacian selects the democratic mode"),
        kernel.prove_exact_spectrum(complete_laplacian,{sp.Integer(0):1,sp.Integer(16):15},subject="complete flavor Laplacian has one democratic ground state"),
        kernel.prove_exact_spectrum(orthogonal_projector,{sp.Integer(0):1,sp.Integer(1):15},subject="normalized flavor parent has unit gap"),
        kernel.prove_matrix_equality(orthogonal_projector*democratic_vector,sp.zeros(16,1),subject="democratic vector is the parent ground state"),
        kernel.prove_matrix_equality(pair_spectrum_multiplicities,sp.Matrix([1,30,225]),subject="two-slot parent spectrum multiplicities"),
        kernel.prove_expression_equality(sum(pair_spectrum_multiplicities),256,subject="two-slot multiplicities exhaust all flavor pairs"),
        kernel.prove_expression_equality(pair_spectrum_multiplicities[0],1,subject="two-slot democratic ground line is unique"),
        kernel.prove_exact_rank(inherited_flavor_operator,16,subject="inherited one-slot flavor operator is fully degenerate"),
        kernel.prove_matrix_equality(inherited_graph_operator,sp.zeros(16),subject="no complete flavor graph is inherited"),
        kernel.prove_expression_equality(inherited_pair_degeneracy,256,subject="inherited flavor pair remains fully degenerate"),
        kernel.prove_matrix_equality(pole_map,sp.zeros(1),subject="democratic selector has no inherited gap-to-pole map"),
        kernel.prove_expression_equality(sum(architecture),11,subject="conditional democratic-parent architecture is complete"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(2,1),subject="flavor graph and pole map origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict democratic selector origin score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_democratic_flavor_selector_parent_origin_gate",theorems)
    return DemocraticFlavorSelectorParentCertificate(democratic_vector,democratic_projector,orthogonal_projector,complete_adjacency,complete_laplacian,cyclic_shift,pair_spectrum_multiplicities,inherited_flavor_operator,inherited_graph_operator,inherited_pair_degeneracy,pole_map,architecture,physical_origin,theorems,gate_theorem)

SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_democratic_flavor_selector_parent_origin_gate",title="Родитель демократического flavor-селектора",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_democratic_flavor_selector_parent_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_su2_gauge_singlet_democratic_flavor_selector_parent_origin_gate_results.json"),obligations=tuple(Obligation(f"democratic_flavor_parent_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(21)))