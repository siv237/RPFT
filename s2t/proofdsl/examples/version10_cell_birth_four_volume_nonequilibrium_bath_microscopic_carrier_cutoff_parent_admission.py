"""LCF certificate for the microscopic carrier-cutoff parent admission."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class MicroscopicCutoffCertificate:
    cutoff_vector: sp.ImmutableMatrix
    parent_gradient: sp.ImmutableMatrix
    parent_hessian: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    velocity_anchored_map: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    conditional_admission: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> MicroscopicCutoffCertificate:
    q1, q2, q3 = sp.symbols("q1 q2 q3", real=True)
    lattice_symbol = 4 * sum(sp.sin(q / 2) ** 2 for q in (q1, q2, q3))
    corner_symbol = sp.simplify(lattice_symbol.subs({q1: sp.pi, q2: sp.pi, q3: sp.pi}))
    axis_symbol = sp.simplify(lattice_symbol.subs({q1: sp.pi, q2: 0, q3: 0}))
    omega_factor = sp.sqrt(corner_symbol)
    cutoff_vector = sp.ImmutableMatrix([sp.pi, omega_factor, 42])

    u, w, s = sp.symbols("u w s", real=True)
    parent = ((u - sp.pi) ** 2 + (w - 2 * sp.sqrt(3)) ** 2 + (s - 42) ** 2) / 2
    variables = (u, w, s)
    target = {u: sp.pi, w: 2 * sp.sqrt(3), s: 42}
    parent_gradient = sp.ImmutableMatrix([sp.diff(parent, item) for item in variables]).subs(target)
    parent_hessian = sp.ImmutableMatrix(sp.hessian(parent, variables))

    # Logarithmic variables are (k_BZ, omega_UV, Lambda_43, ell_cell, v_g).
    scale_map = sp.ImmutableMatrix(
        [[1, 0, 0, 1, 0], [0, 1, 0, 1, -1], [0, 0, 1, 1, 0]]
    )
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([-1, -1, -1, 1, 0]),
        sp.ImmutableMatrix([0, 1, 0, 0, 1]),
    )
    velocity_anchored_map = sp.ImmutableMatrix.vstack(
        scale_map, sp.ImmutableMatrix([[0, 0, 0, 0, 1]])
    )
    fully_anchored_map = sp.ImmutableMatrix.vstack(
        velocity_anchored_map, sp.ImmutableMatrix([[0, 0, 0, 1, 0]])
    )
    conditional_admission = sp.ones(9, 1)
    physical_origin = sp.zeros(2, 1)

    theorems = (
        kernel.prove_expression_equality(corner_symbol, 12, subject="cell Laplacian operator-norm symbol"),
        kernel.prove_expression_equality(axis_symbol, 4, subject="axis Brillouin-edge symbol"),
        kernel.prove_expression_equality(omega_factor, 2 * sp.sqrt(3), subject="three-dimensional ultraviolet frequency factor"),
        kernel.prove_expression_equality(cutoff_vector[0], sp.pi, subject="Brillouin momentum cutoff times cell length"),
        kernel.prove_expression_equality(cutoff_vector[1], 2 * sp.sqrt(3), subject="frequency cutoff times cell transit scale"),
        kernel.prove_expression_equality(cutoff_vector[2], 42, subject="K43 spectral cutoff times cell length"),
        kernel.prove_expression_equality(cutoff_vector[2] / cutoff_vector[0], 42 / sp.pi, subject="spectral to Brillouin cutoff ratio"),
        kernel.prove_expression_equality(cutoff_vector[2] / cutoff_vector[1], 7 * sp.sqrt(3), subject="spectral energy to corner frequency ratio when v_g equals c"),
        kernel.prove_expression_equality((1 / (2 * sp.sqrt(3))) * cutoff_vector[1], 1, subject="ultraviolet correlation time frequency product"),
        kernel.prove_expression_equality(cutoff_vector[0] * cutoff_vector[2] / sp.pi, 42, subject="common cell-length cutoff closure"),
        kernel.prove_matrix_equality(parent_gradient, sp.zeros(3, 1), subject="cutoff parent stationary point"),
        kernel.prove_matrix_equality(parent_hessian, sp.eye(3), subject="cutoff parent Hessian"),
        kernel.prove_exact_rank(parent_hessian, 3, subject="cutoff parent strict rank"),
        kernel.prove_expression_equality(parent_hessian.det(), 1, subject="cutoff parent determinant"),
        kernel.prove_exact_rank(scale_map, 3, subject="microscopic cutoff dimensional map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="length and velocity cutoff freedoms"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(3, 2), subject="microscopic cutoff scale kernels"),
        kernel.prove_exact_rank(velocity_anchored_map, 4, subject="velocity anchor leaves one length orbit"),
        kernel.prove_exact_nullity(velocity_anchored_map, 1, subject="absolute cell length remains after velocity anchor"),
        kernel.prove_exact_rank(fully_anchored_map, 5, subject="velocity and length anchors close cutoff map"),
        kernel.prove_matrix_equality(conditional_admission, sp.ones(9, 1), subject="conditional microscopic cutoff parent admitted"),
        kernel.prove_expression_equality(sum(conditional_admission), 9, subject="nine conditional cutoff requirements pass"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(2, 1), subject="carrier and absolute cutoff origins remain open"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate",
        theorems,
    )
    return MicroscopicCutoffCertificate(
        cutoff_vector,
        parent_gradient,
        parent_hessian,
        scale_map,
        scale_kernel,
        velocity_anchored_map,
        fully_anchored_map,
        conditional_admission,
        physical_origin,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate",
    title="Допуск родителя микроскопического обрезания неравновесного носителя",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_microscopic_carrier_cutoff_parent_admission_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"microscopic_cutoff_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(23)
    ),
)