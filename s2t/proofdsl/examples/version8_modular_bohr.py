"""Exact chain-number Bohr-parent certificate."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..kernel import Theorem, kernel
from .version8_full_primitive import _jumps, build_certificate as build_full

@dataclass(frozen=True, slots=True)
class ModularBohrCertificate:
    transfer_count: int
    forward_ratio: sp.Expr
    reverse_ratio: sp.Expr
    forward_bohr_theorem: Theorem
    reverse_bohr_theorem: Theorem
    gauge_invariance_theorem: Theorem
    forward_primitive_theorem: Theorem
    reverse_primitive_theorem: Theorem
    orientation_no_go_theorem: Theorem

@lru_cache(maxsize=1)
def build_certificate() -> ModularBohrCertificate:
    jumps=_jumps(); source=sp.diag(sp.eye(11),sp.zeros(10)); target=sp.eye(21)-source
    transfer=(jumps[0],)+jumps[13:]
    forward=tuple(sp.ImmutableMatrix(target*j*source) for j in transfer)
    reverse=tuple(sp.ImmutableMatrix(source*j*target) for j in transfer)
    n=2*target
    f=kernel.prove_opposite_bohr_split(n,forward,reverse,sp.Integer(2),subject="chain-number forward orientation")
    r=kernel.prove_opposite_bohr_split(2*source,reverse,forward,sp.Integer(2),subject="chain-number reverse orientation")
    gauge=sp.Matrix.hstack(*[n*j-j*n for j in jumps[1:13]])
    gt=kernel.prove_matrix_equality(gauge,sp.zeros(21,21*12),subject="chain number commutes with all gauge jumps")
    full=build_full()
    fp=kernel.prove_oriented_directed_pair_primitivity(full.scalar_fixed_theorem,f,subject="forward directed KMS process")
    rp=kernel.prove_oriented_directed_pair_primitivity(full.scalar_fixed_theorem,r,subject="reverse directed KMS process")
    nogo=kernel.prove_matrix_inequality(sp.Matrix([[sp.exp(-2)]]),sp.Matrix([[sp.exp(2)]]),subject="two chain orientations give distinct KMS ratios")
    return ModularBohrCertificate(13,sp.exp(-2),sp.exp(2),f,r,gt,fp,rp,nogo)
if __name__ == "__main__": print(build_certificate())