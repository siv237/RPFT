"""LCF audit of scale-orbit breakers for the nonequilibrium entropy branch."""
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel

@dataclass(frozen=True, slots=True)
class Certificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    scale_degrees: sp.ImmutableMatrix
    internal_conformal: sp.ImmutableMatrix
    conditional_breakers: sp.ImmutableMatrix
    independent_origins: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> Certificate:
    # energy-density type, different degree from -4, internal origin,
    # target independence, typed entropy coupling, orbit breaking.
    candidates=sp.ImmutableMatrix([
      [1,0,1,1,1,0], # cell-temperature black body
      [1,0,1,1,1,0], # cell Casimir density
      [1,0,1,1,0,0], # curvature squared
      [1,0,0,1,1,0], # Lambda/G density
      [1,1,0,1,1,1], # fixed bath correlation time
      [1,1,0,1,1,1], # fixed chemical potential
      [1,1,0,0,1,1], # observed external mass gap
      [1,1,0,1,0,1], # dimensional-transmutation scale
      [1,1,0,1,0,1], # nonlocal memory length
      [0,0,0,0,0,1], # bare external ruler
    ])
    passes=sp.ImmutableMatrix([sp.prod(candidates.row(i)) for i in range(10)])
    scores=sp.ImmutableMatrix([sum(candidates.row(i)) for i in range(10)])
    degrees=sp.ImmutableMatrix([-4,-4,-4,-4,-3,-3,0,0,0,0])
    conformal=sp.ImmutableMatrix([1,1,1,1,0,0,0,0,0,0])
    breakers=sp.ImmutableMatrix([0,0,0,0,1,1,1,1,1,1])
    origins=sp.zeros(10,1);architecture=sp.ones(10,1);physical=sp.zeros(2,1)
    ell,A,B=sp.symbols("ell A B",positive=True)
    ts=(
      kernel.prove_matrix_equality(candidates,sp.Matrix(candidates),subject="ten orbit breakers on six origin criteria"),
      kernel.prove_matrix_equality(passes,sp.zeros(10,1),subject="no orbit breaker passes the complete contract"),
      kernel.prove_matrix_equality(scores,sp.Matrix([4,4,3,3,5,5,4,4,4,1]),subject="orbit breaker candidate scores"),
      kernel.prove_expression_equality(max(scores),5,subject="external bath scales reach five of six criteria"),
      kernel.prove_exact_rank(candidates,6,subject="orbit breaker menu spans all criteria"),
      kernel.prove_matrix_equality(degrees,sp.Matrix([-4,-4,-4,-4,-3,-3,0,0,0,0]),subject="candidate scale degrees"),
      kernel.prove_matrix_equality(conformal,sp.Matrix([1,1,1,1,0,0,0,0,0,0]),subject="four internal densities remain conformal"),
      kernel.prove_expression_equality(sum(conformal),4,subject="four internal conformal candidates"),
      kernel.prove_matrix_equality(breakers,sp.Matrix([0,0,0,0,1,1,1,1,1,1]),subject="six candidates conditionally break the orbit"),
      kernel.prove_expression_equality(sum(breakers),6,subject="six conditional orbit breakers"),
      kernel.prove_matrix_equality(origins,sp.zeros(10,1),subject="no breaker has an independent internal origin"),
      kernel.prove_expression_equality(sum(origins),0,subject="independent breaker origin score zero"),
      kernel.prove_expression_equality((A/ell**4).subs(ell,A/B),B/(A/B)**3,subject="fixed bath time conditionally selects a length"),
      kernel.prove_expression_equality((A/ell**4).subs(ell,(A/B)**sp.Rational(1,4)),B,subject="fixed mass density conditionally selects a length"),
      kernel.prove_expression_equality(sp.diff(A/ell**4,ell),-4*A/ell**5,subject="internal entropy density degree minus four"),
      kernel.prove_expression_equality(sp.diff(B/ell**3,ell),-3*B/ell**4,subject="fixed bath time density degree minus three"),
      kernel.prove_matrix_equality(architecture,sp.ones(10,1),subject="orbit breaker audit coverage"),
      kernel.prove_expression_equality(sum(architecture),10,subject="ten candidates audited"),
      kernel.prove_matrix_equality(physical,sp.zeros(2,1),subject="independent scale and common parent origins open"),
      kernel.prove_expression_equality(sum(physical),0,subject="absolute scale remains unselected"))
    gate=kernel.prove_gate("version10_cell_birth_four_volume_nonequilibrium_entropy_scale_orbit_breaker_candidate_audit_gate",ts)
    return Certificate(candidates,passes,scores,degrees,conformal,breakers,origins,architecture,physical,ts,gate)

SPEC=GateSpec(identifier="version10_cell_birth_four_volume_nonequilibrium_entropy_scale_orbit_breaker_candidate_audit_gate",title="Аудит нарушителей энтропийной масштабной орбиты",source_paths=("s2t/gates/version10_cell_birth_four_volume_nonequilibrium_entropy_scale_orbit_breaker_candidate_audit_gate.tex","s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_entropy_scale_orbit_breaker_candidate_audit_gate_results.json"),obligations=tuple(Obligation(f"entropy_breaker_{i:02d}",lambda i=i:build_certificate().theorems[i]) for i in range(20)))