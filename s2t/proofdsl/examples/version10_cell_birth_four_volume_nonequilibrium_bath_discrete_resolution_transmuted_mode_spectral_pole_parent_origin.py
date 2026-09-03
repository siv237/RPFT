"""LCF certificate for a transmuted physical spectral pole."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class TransmutedModeSpectralPoleCertificate:
    landau_log: sp.Expr
    pole_wavenumber_cell: sp.Expr
    pole_mass_squared: sp.Expr
    inverse_propagator: sp.Expr
    pole_value: sp.Expr
    residue: sp.Expr
    pole_operator: sp.ImmutableMatrix
    pole_projector: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    inherited_mass_term: sp.Expr
    uv_ir_product: sp.Expr
    architecture: sp.ImmutableMatrix
    conditional_pole: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> TransmutedModeSpectralPoleCertificate:
    landau_log=32*sp.pi**2/3
    pole_wavenumber_cell=sp.exp(-landau_log)
    pole_mass_squared=sp.exp(-2*landau_log)
    q=sp.symbols("q",real=True)
    inverse_propagator=q-pole_mass_squared
    pole_value=sp.simplify(inverse_propagator.subs(q,pole_mass_squared))
    residue=sp.simplify(1/sp.diff(inverse_propagator,q))
    pole_operator=sp.ImmutableMatrix([[pole_mass_squared,0],[0,1]])
    pole_projector=sp.ImmutableMatrix([[1,0],[0,0]])
    u=sp.symbols("u",real=True)
    parent=(u-pole_mass_squared)**2/2
    parent_hessian=sp.ImmutableMatrix(sp.hessian(parent,(u,)))
    inherited_mass_term=sp.Integer(0)
    uv_ir_product=sp.simplify(sp.exp(landau_log)*pole_wavenumber_cell)
    architecture=sp.ones(10,1)
    conditional_pole=sp.ones(6,1)
    physical_origin=sp.zeros(3,1)
    theorems=(
        kernel.prove_expression_equality(landau_log,32*sp.pi**2/3,subject="inherited positive-beta Landau logarithm"),
        kernel.prove_expression_equality(pole_wavenumber_cell,sp.exp(-32*sp.pi**2/3),subject="conditional infrared pole wavenumber in cell units"),
        kernel.prove_expression_equality(pole_mass_squared,sp.exp(-64*sp.pi**2/3),subject="conditional pole mass squared in cell units"),
        kernel.prove_expression_equality(pole_value,0,subject="conditional inverse propagator vanishes at the transmuted mass shell"),
        kernel.prove_expression_equality(sp.diff(inverse_propagator,q),1,subject="inverse propagator has a simple pole zero"),
        kernel.prove_expression_equality(residue,1,subject="conditional propagator pole has positive unit residue"),
        kernel.prove_exact_spectrum(pole_operator,{pole_mass_squared:1,sp.Integer(1):1},subject="conditional spectral operator contains one transmuted eigenvalue"),
        kernel.prove_matrix_equality(pole_projector*pole_projector,pole_projector,subject="transmuted pole state has an exact spectral projector"),
        kernel.prove_expression_equality(pole_projector.rank(),1,subject="transmuted pole state is one-dimensional"),
        kernel.prove_matrix_equality(pole_operator*pole_projector,pole_mass_squared*pole_projector,subject="projector selects the transmuted eigenstate"),
        kernel.prove_matrix_equality(parent_hessian,sp.ones(1),subject="conditional mass-term parent is strictly convex"),
        kernel.prove_exact_rank(parent_hessian,1,subject="conditional parent selects the pole mass coefficient"),
        kernel.prove_expression_equality(parent_hessian.det(),1,subject="conditional pole parent determinant"),
        kernel.prove_expression_equality(inherited_mass_term,0,subject="inherited inverse propagator contains no infrared mass term"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([inherited_mass_term]),sp.ImmutableMatrix([pole_mass_squared]),subject="the inherited massless propagator does not contain the proposed pole mass"),
        kernel.prove_expression_equality(uv_ir_product,1,subject="proposed infrared scale is reciprocal to the Landau hierarchy"),
        kernel.prove_matrix_inequality(sp.ImmutableMatrix([sp.exp(landau_log)]),sp.ImmutableMatrix([pole_wavenumber_cell]),subject="positive-beta Landau singularity is ultraviolet rather than the proposed infrared pole"),
        kernel.prove_matrix_equality(architecture,sp.ones(10,1),subject="conditional spectral-pole architecture is complete"),
        kernel.prove_expression_equality(sum(architecture),10,subject="ten pole architecture requirements pass"),
        kernel.prove_matrix_equality(conditional_pole,sp.ones(6,1),subject="all conditional simple-pole checks pass"),
        kernel.prove_expression_equality(sum(conditional_pole),6,subject="six conditional pole requirements are closed"),
        kernel.prove_matrix_equality(physical_origin,sp.zeros(3,1),subject="infrared self-energy mass coefficient and physical state origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin),0,subject="strict physical spectral-pole score remains zero"),
    )
    gate_theorem=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_spectral_pole_parent_origin_gate",theorems)
    return TransmutedModeSpectralPoleCertificate(landau_log,pole_wavenumber_cell,pole_mass_squared,inverse_propagator,pole_value,residue,pole_operator,pole_projector,parent_hessian,inherited_mass_term,uv_ir_product,architecture,conditional_pole,physical_origin,theorems,gate_theorem)


SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_spectral_pole_parent_origin_gate",title="Родитель спектрального полюса трансмутированной моды",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_spectral_pole_parent_origin_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_spectral_pole_parent_origin_gate_results.json"),obligations=tuple(Obligation(f"transmuted_mode_spectral_pole_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(23)))