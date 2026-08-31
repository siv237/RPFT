#!/usr/bin/env python3
"""Exact parent-action origin audit for the two extra-edge central gaps."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate_results.json"

def main() -> None:
    previous=json.loads((ROOT/"s2t/results/s2t_v8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_minimal_central_hamiltonian_data_gate_results.json").read_text())
    gate="version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_central_hamiltonian_parent_action_origin_gate"
    assert previous["next_gate"]==gate
    PY=sp.diag(*([1]*4+[0]*12)); Pu=sp.diag(*([0]*4+[1]*6+[0]*6)); Pd=sp.diag(*([0]*10+[1]*6)); I=sp.eye(16)
    A=Pu-Pd; B=Pu+Pd-3*PY
    assert sp.trace(A)==sp.trace(B)==sp.trace(A*B)==0
    assert sp.trace(A*A)==12 and sp.trace(B*B)==48
    a,b=sp.symbols('a b', real=True); h=a*A+b*B
    assert sp.expand(sp.trace(h*h))==12*a**2+48*b**2
    assert sp.expand(sp.trace(h**3))==36*a**2*b-96*b**3
    gaps=sp.Matrix([a+4*b,-a+4*b])
    assert sp.solve([sp.Symbol('Du')-(a+4*b),sp.Symbol('Dd')-(-a+4*b)],(a,b))=={a:sp.Symbol('Du')/2-sp.Symbol('Dd')/2,b:sp.Symbol('Du')/8+sp.Symbol('Dd')/8}
    gauge=sp.Matrix([[sp.Rational(91,36),-sp.Rational(3,4),sp.Rational(4,3)],[sp.Rational(7,36),-sp.Rational(3,4),sp.Rational(4,3)]])
    assert gauge.rank()==2 and len(gauge.nullspace())==1
    c1,c2,c3=sp.symbols('c1 c2 c3', real=True)
    gg=gauge*sp.Matrix([c1,c2,c3]); assert sp.simplify(gg[0]-gg[1]-sp.Rational(7,3)*c1)==0
    eps=sp.symbols('epsilon', real=True); n=sp.symbols('n', integer=True, positive=True)
    # Exact first variations of polynomial moments at a scalar background.
    assert sp.trace(A)==0 and sp.trace(B)==0
    H2=sp.expand(sp.trace((eps*I+h)**2));
    assert sp.diff(H2,a).subs({a:0,b:0})==0 and sp.diff(H2,b).subs({a:0,b:0})==0
    assert sp.hessian(H2,(a,b))==sp.diag(24,96)
    jA,jB=sp.symbols('j_A j_B', real=True)
    V=sp.trace(h*h)/2-jA*a-jB*b
    sol=sp.solve([sp.diff(V,a),sp.diff(V,b)],(a,b)); assert sol=={a:jA/12,b:jB/48}
    coherence_scalar=sp.Integer(3)*I
    assert sp.trace(coherence_scalar*A)==sp.trace(coherence_scalar*B)==0
    objs=[PY,Pu,Pd,A,B,h,gaps,gauge,gg,H2,V,coherence_scalar]
    assert not any(o.atoms(sp.Float) for o in objs)
    result={
      "date":"2026-08-31","gate":gate,
      "traceless_central_basis":{"A":"P_u-P_d","B":"P_u+P_d-3P_Y","gram_matrix":[[12,0],[0,48]],"gap_map":["Delta_u=a+4b","Delta_d=-a+4b"],"basis_dimension":2},
      "spectral_moment_test":{"Tr_h2":"12 a^2+48 b^2","Tr_h3":"36 a^2 b-96 b^3","scalar_background_linear_response":[0,0],"quadratic_hessian":[[24,0],[0,96]],"selects_nonzero_gap":False},
      "gauge_casimir_test":{"gap_coefficient_matrix":[["91/36","-3/4","4/3"],["7/36","-3/4","4/3"]],"rank":2,"nullity":1,"gap_difference":"Delta_u-Delta_d=(7/3)c1","equal_gaps_require":"c1=0","casimir_hamiltonian_in_parent":False},
      "other_sources":{"grading_sector_vector":"scalar; zero after quotient","coherence_radius":3,"coherence_scalar_gap_response":[0,0],"old_parent_depends_on_new_center":False},
      "minimal_source_preview":{"potential":"(1/2)Tr(h^2)-j_A a-j_B b","stationary_point":["j_A/12","j_B/48"],"generic_source_components":2},
      "ledgers":{"conditional_shape_satisfied":5,"conditional_shape_tested":5,"parent_origin_satisfied":0,"parent_origin_tested":7},
      "verdict":{"two_gap_shape_available":True,"ordinary_moments_generate_stiffness":True,"ordinary_moments_generate_nonzero_source":False,"gauge_casimirs_span_gap_plane_conditionally":True,"gauge_casimir_coefficients_inherited":False,"coherence_scalar_generates_gaps":False,"two_gap_values_derived":False},
      "next_gate":"version8_baryon_c0_singlet_triplet_central_gap_isotypic_channel_extra_edge_mass_two_source_parent_architecture_gate","floating_point_values":0}
    text=json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n"; OUTPUT.write_text(text); print(OUTPUT); print(hashlib.sha256(text.encode()).hexdigest())
if __name__=='__main__': main()