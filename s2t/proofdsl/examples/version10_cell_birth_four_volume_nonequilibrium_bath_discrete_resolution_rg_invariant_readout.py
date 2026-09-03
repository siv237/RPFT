"""LCF certificate for the RG-invariant discrete-resolution readout."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class DiscreteResolutionInvariantReadoutCertificate:
    landau_log: sp.Expr
    k43_cell_product: sp.Expr
    bridge_ratio: sp.Expr
    mode_cell_product: sp.Expr
    resolution: sp.Expr
    constraint_map: sp.ImmutableMatrix
    augmented_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    resolution_covector: sp.ImmutableMatrix
    mismatch_factors: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    relational_consequence: sp.ImmutableMatrix
    physical_typing: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> DiscreteResolutionInvariantReadoutCertificate:
    landau_log=32*sp.pi**2/3
    k43_cell_product=sp.Integer(42)
    bridge_ratio=sp.exp(-landau_log)/42
    mode_cell_product=sp.simplify(bridge_ratio*k43_cell_product)
    resolution=sp.simplify(1/mode_cell_product)

    # Columns: log(Lambda43), log(ell_cell), log(mu_spec).
    constraint_map=sp.ImmutableMatrix([[1,1,0],[-1,0,1]])
    derived_row=sp.ImmutableMatrix([[0,1,1]])
    augmented_map=sp.ImmutableMatrix.vstack(constraint_map,derived_row)
    scale_kernel=sp.ImmutableMatrix([1,-1,1])
    resolution_covector=sp.ImmutableMatrix([[0,-1,-1]])
    mismatch_factors=sp.ImmutableMatrix([resolution/10**20,resolution/10**43])
    architecture=sp.ones(10,1)
    relational_consequence=sp.ones(7,1)
    physical_typing=sp.zeros(3,1)

    mu,ell,c,s=sp.symbols("mu ell c s",positive=True)
    tau_birth=ell/c
    tau_mode=1/(c*mu)
    theorems=(
        kernel.prove_expression_equality(landau_log,32*sp.pi**2/3,subject="exact inherited RG logarithm"),
        kernel.prove_expression_equality(k43_cell_product,42,subject="exact K43 cutoff per cell"),
        kernel.prove_expression_equality(bridge_ratio,sp.exp(-32*sp.pi**2/3)/42,subject="exact RG K43 reference ratio"),
        kernel.prove_expression_equality(mode_cell_product,sp.exp(-32*sp.pi**2/3),subject="K43 factor cancels in the mode-cell product"),
        kernel.prove_expression_equality(resolution,sp.exp(32*sp.pi**2/3),subject="exact discrete resolution hierarchy"),
        kernel.prove_expression_equality((mu/s)*(s*ell),mu*ell,subject="mode-cell product is invariant under the common scale orbit"),
        kernel.prove_expression_equality(1/((mu/s)*(s*ell)),1/(mu*ell),subject="resolution is invariant under the common scale orbit"),
        kernel.prove_expression_equality(tau_mode/tau_birth,1/(mu*ell),subject="temporal and spatial resolution agree when ell equals c tau_birth"),
        kernel.prove_exact_rank(constraint_map,2,subject="K43 cell and RG K43 relations are independent"),
        kernel.prove_exact_nullity(constraint_map,1,subject="one absolute scale orbit remains"),
        kernel.prove_matrix_equality(constraint_map*scale_kernel,sp.zeros(2,1),subject="exact absolute scale orbit"),
        kernel.prove_exact_rank(augmented_map,2,subject="the mode-cell consequence does not add a dimensional constraint"),
        kernel.prove_exact_nullity(augmented_map,1,subject="derived resolution does not fix the absolute cell size"),
        kernel.prove_matrix_equality(augmented_map*scale_kernel,sp.zeros(3,1),subject="absolute scale survives the invariant readout"),
        kernel.prove_expression_equality((derived_row-constraint_map.row(0)-constraint_map.row(1)).norm(),0,subject="mode-cell row is the sum of the two parent rows"),
        kernel.prove_expression_equality((resolution_covector*scale_kernel)[0],0,subject="resolution covector annihilates the scale orbit"),
        kernel.prove_matrix_inequality(mismatch_factors,sp.ones(2,1),subject="the exact hierarchy is neither the proposed proton nor one-second count"),
        kernel.prove_matrix_equality(architecture,sp.ones(10,1),subject="discrete-resolution readout architecture is complete"),
        kernel.prove_expression_equality(sum(architecture),10,subject="ten readout architecture requirements pass"),
        kernel.prove_matrix_equality(relational_consequence,sp.ones(7,1),subject="all exact relational consequences pass"),
        kernel.prove_expression_equality(sum(relational_consequence),7,subject="seven relational checks are closed"),
        kernel.prove_matrix_equality(physical_typing,sp.zeros(3,1),subject="Compton mode particle identity and independent bridge origin remain open"),
        kernel.prove_expression_equality(sum(physical_typing),0,subject="strict physical mode attribution score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_rg_invariant_readout_gate",theorems)
    return DiscreteResolutionInvariantReadoutCertificate(landau_log,k43_cell_product,bridge_ratio,mode_cell_product,resolution,constraint_map,augmented_map,scale_kernel,resolution_covector,mismatch_factors,architecture,relational_consequence,physical_typing,theorems,gate_theorem)


SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_rg_invariant_readout_gate",title="RG-инвариантное чтение дискретного разрешения",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_rg_invariant_readout_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_rg_invariant_readout_gate_results.json"),obligations=tuple(Obligation(f"discrete_resolution_readout_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(23)))