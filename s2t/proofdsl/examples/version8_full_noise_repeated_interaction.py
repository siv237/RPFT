"""Structural exact certificate for the full 42-jump repeated interaction."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from ..kernel import Theorem, kernel
from .version8_full_noise_trace_frame import full_noise_frame
from .version8_gauge_twirl_kraus import _endpoint_gauge_generators
from .version8_full_noise_gksl import build_certificate as gksl_certificate
from .version8_microscopic_interaction_hamiltonian import build_certificate as cross_micro_certificate

@dataclass(frozen=True, slots=True)
class FullNoiseRepeatedInteractionCertificate:
    system_dimension:int; jump_dimension:int; environment_dimension:int; ambient_dimension:int
    closure_theorem:Theorem; star_theorem:Theorem; minimality_theorem:Theorem
    collision_limit_theorem:Theorem; fixed_algebra_theorem:Theorem; scale_no_go_theorem:Theorem
    full_gate_theorem:Theorem

@lru_cache(maxsize=1)
def build_certificate()->FullNoiseRepeatedInteractionCertificate:
    frame=full_noise_frame(); gksl=gksl_certificate(); micro=cross_micro_certificate()
    closure=kernel.prove_hermitian_frame_lie_closure(frame,_endpoint_gauge_generators(),subject="gauge closure of the full 42-jump Hermitian frame")
    star=kernel.prove_structural_star_interaction(frame,subject="full-noise vacuum-to-jump star Hamiltonian",premises=(closure,gksl.gksl_theorem))
    minimality=kernel.prove_expression_equality(star.proposition.data["environment_dimension"],43,subject="minimal full-noise collision environment")
    collision=kernel.prove_structural_star_collision_limit(star,subject="full 42-jump unitary collision limit")
    gate=kernel.prove_gate("full_noise_repeated_interaction",(closure,star,minimality,collision,gksl.scalar_fixed_theorem,micro.scale_no_go_theorem))
    return FullNoiseRepeatedInteractionCertificate(21,42,43,903,closure,star,minimality,collision,gksl.scalar_fixed_theorem,micro.scale_no_go_theorem,gate)

if __name__=="__main__":
    c=build_certificate(); print(c.star_theorem.proposition)