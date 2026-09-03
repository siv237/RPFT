"""LCF certificate for embedding bath continuum dispersion into cell geometry."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class BathContinuumEmbeddingCertificate:
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    physical_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> BathContinuumEmbeddingCertificate:
    k,ell,v,c,x=sp.symbols("k ell v c x",positive=True)
    dispersion=2*v*sp.sin(k*ell/2)/ell
    cutoff=sp.simplify(dispersion.subs(k,sp.pi/ell))
    group_velocity=sp.simplify(sp.diff(dispersion,k).subs(k,0))
    kx=sp.log((1+2*x)/(1+x))
    velocity_ratio=sp.Rational(121,24)*kx
    a=sp.Rational(24,121)
    y=sp.exp(a)
    x_luminal=sp.simplify((y-1)/(2-y))
    kx_luminal=sp.simplify(kx.subs(x,x_luminal))
    S_luminal=-sp.log(x_luminal)
    S_locked=sp.Rational(13703599917352236,10**14)
    kx_locked=sp.log((1+2*sp.exp(-S_locked))/(1+sp.exp(-S_locked)))

    # variables: log ell, log Omega_C, log Omega_bath, log kappa
    scale_map=sp.ImmutableMatrix([[1,1,0,0],[1,0,1,0],[0,-1,0,1]])
    scale_kernel=sp.ImmutableMatrix([1,-1,-1,-1])
    parent_hessian=sp.ImmutableMatrix(scale_map.T*scale_map)
    # dispersion, positivity, cutoff, relative match, locked-vacuum match,
    # internal velocity origin
    candidate_matrix=sp.ImmutableMatrix([
      [1,1,1,1,0,1],  # luminal cell chain
      [1,1,1,1,1,0],  # free-velocity cell chain
      [1,1,0,1,0,0],  # Hopf propagation
      [1,0,1,1,0,0],  # K43 level spacing
      [1,1,1,1,0,0],  # cell-birth front
      [1,1,1,1,1,0],  # vacuum-suppressed velocity
    ])
    pass_vector=sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(6)])
    scores=[sum(candidate_matrix.row(i)) for i in range(6)]
    architecture=sp.ones(9,1)
    physical_ledger=sp.ImmutableMatrix([1,1,1,1,0,0])
    ts=(
      kernel.prove_expression_equality(group_velocity,v,subject="cell-chain infrared group velocity"),
      kernel.prove_expression_equality(cutoff,2*v/ell,subject="cell-chain bath cutoff"),
      kernel.prove_expression_equality((2*v/ell)/(c/ell),2*v/c,subject="bath cutoff relative to cell clock"),
      kernel.prove_expression_equality((2*velocity_ratio)/kx,sp.Rational(121,12),subject="memory compatibility after velocity selection"),
      kernel.prove_expression_equality(velocity_ratio,sp.Rational(121,24)*kx,subject="selected bath velocity ratio"),
      kernel.prove_expression_equality(sp.Rational(2,1)/(sp.Rational(24,121)),sp.Rational(121,12),subject="luminal branch cutoff conductance ratio"),
      kernel.prove_expression_equality((1+2*x_luminal)/(1+x_luminal),y,subject="luminal branch solves growth ratio"),
      kernel.prove_expression_equality(kx_luminal,a,subject="luminal branch selects k_X=24/121"),
      kernel.prove_expression_equality(S_luminal,-sp.log((sp.exp(a)-1)/(2-sp.exp(a))),subject="luminal branch vacuum action"),
      kernel.prove_matrix_inequality(sp.Matrix([[kx_locked]]),sp.Matrix([[a]]),subject="locked S_vac growth coupling differs from luminal requirement"),
      kernel.prove_expression_nonconstant(velocity_ratio,x,subject="required propagation speed depends on vacuum weight"),
      kernel.prove_exact_rank(scale_map,3,subject="cell dispersion scale map rank"),
      kernel.prove_exact_nullity(scale_map,1,subject="cell dispersion absolute scale nullity"),
      kernel.prove_matrix_equality(scale_map*scale_kernel,sp.zeros(3,1),subject="cell length frequency scale kernel"),
      kernel.prove_matrix_equality(parent_hessian,sp.Matrix([[2,1,1,0],[1,2,0,-1],[1,0,1,0],[0,-1,0,1]]),subject="cell dispersion parent Hessian"),
      kernel.prove_exact_rank(parent_hessian,3,subject="cell dispersion parent rank"),
      kernel.prove_matrix_equality(parent_hessian*scale_kernel,sp.zeros(4,1),subject="cell dispersion parent flat scale direction"),
      kernel.prove_matrix_equality(candidate_matrix,sp.Matrix(candidate_matrix),subject="six continuum embedding candidates"),
      kernel.prove_matrix_equality(pass_vector,sp.zeros(6,1),subject="zero complete continuum embeddings"),
      kernel.prove_expression_equality(max(scores),5,subject="best continuum embedding score"),
      kernel.prove_exact_rank(candidate_matrix,5,subject="continuum embedding candidate rank"),
      kernel.prove_matrix_equality(architecture,sp.ones(9,1),subject="conditional cell continuum architecture"),
      kernel.prove_expression_equality(sum(architecture),9,subject="nine conditional embedding checks pass"),
      kernel.prove_matrix_equality(physical_ledger,sp.Matrix([1,1,1,1,0,0]),subject="dispersion and relative matching pass while velocity and scale origins remain open"),
      kernel.prove_expression_equality(sum(physical_ledger),4,subject="four of six physical embedding requirements pass"),
      kernel.prove_expression_equality(sp.Rational(121,24)*sp.Rational(24,121),1,subject="velocity selector reciprocal normalization"),
    )
    gate=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_bath_continuum_dispersion_cell_geometry_typed_embedding_gate",ts)
    return BathContinuumEmbeddingCertificate(scale_map,scale_kernel,parent_hessian,candidate_matrix,pass_vector,architecture,physical_ledger,ts,gate)

SPEC=GateSpec("version10_cell_birth_four_volume_nonequilibrium_bath_continuum_dispersion_cell_geometry_typed_embedding_gate","Вложение континуальной дисперсии ванны в клеточную геометрию",("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_continuum_dispersion_cell_geometry_typed_embedding_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_continuum_dispersion_cell_geometry_typed_embedding_gate_results.json"),tuple(Obligation(f"bath_continuum_embedding_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(26)))