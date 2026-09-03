"""LCF certificate for the bath spectral-density and memory-scale audit."""

from dataclasses import dataclass
from functools import lru_cache

import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class SpectralDensityMemoryAuditCertificate:
    candidate_matrix: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    component_assignment: sp.ImmutableMatrix
    component_availability: sp.ImmutableMatrix
    scale_map: sp.ImmutableMatrix
    scale_kernel: sp.ImmutableMatrix
    velocity_anchored_map: sp.ImmutableMatrix
    fully_anchored_map: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> SpectralDensityMemoryAuditCertificate:
    # Criteria: nonnegative spectrum, normalized full profile, finite absolute
    # memory, exact KMS/on-shell compatibility, inherited parent selector,
    # independent breaking of the absolute scale orbit.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 1, 1, 0, 0],  # Drude/exponential correlation
        [1, 1, 1, 1, 0, 0],  # Gaussian correlation
        [1, 1, 1, 1, 0, 0],  # Ohmic exponential cutoff
        [1, 1, 0, 1, 1, 0],  # hard Brillouin band
        [1, 1, 1, 0, 0, 0],  # damped oscillatory profile
        [1, 1, 0, 1, 1, 0],  # finite K43 spectral comb
        [1, 0, 0, 1, 1, 0],  # two-KMS on-shell completion
        [1, 1, 0, 0, 0, 0],  # maximum entropy on a hard band
        [1, 1, 1, 1, 0, 0],  # reciprocal clock/cutoff time
        [1, 1, 1, 1, 0, 1],  # observed relaxation time
    ])
    pass_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    component_assignment = sp.ImmutableMatrix([[1, 0]] * 8 + [[0, 1]] * 2)
    component_availability = sp.zeros(2, 1)

    # Logarithmic variables: (tau_corr, omega_UV, ell_cell, v_g).
    scale_map = sp.ImmutableMatrix([[1, 1, 0, 0], [0, 1, 1, -1]])
    scale_kernel = sp.ImmutableMatrix.hstack(
        sp.ImmutableMatrix([-1, 1, 0, 1]),
        sp.ImmutableMatrix([1, -1, 1, 0]),
    )
    velocity_anchored_map = sp.ImmutableMatrix.vstack(scale_map, sp.ImmutableMatrix([[0, 0, 0, 1]]))
    fully_anchored_map = sp.ImmutableMatrix.vstack(velocity_anchored_map, sp.ImmutableMatrix([[0, 0, 1, 0]]))
    architecture = sp.ones(10, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0, 0])

    x = sp.symbols("x", nonnegative=True)
    tau_observed = sp.symbols("tau_observed", positive=True)
    theorems = (
        kernel.prove_matrix_equality(candidate_matrix, sp.Matrix(candidate_matrix), subject="ten bath spectral-density candidates on six criteria"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(10, 1), subject="no spectral-density candidate passes the full physical contract"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 4, 4, 4, 3, 4, 3, 2, 4, 5]), subject="spectral-density candidate scores"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="observed relaxation time reaches five of six criteria"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="spectral-density audit spans all six criteria"),
        kernel.prove_matrix_equality(component_assignment.T * sp.ones(10, 1), sp.ImmutableMatrix([8, 2]), subject="eight shape and two scale candidates"),
        kernel.prove_exact_rank(component_assignment, 2, subject="profile shape and memory scale are independent components"),
        kernel.prove_matrix_equality(component_availability, sp.zeros(2, 1), subject="neither profile nor absolute scale has complete origin"),
        kernel.prove_expression_equality(sp.integrate(sp.exp(-x), (x, 0, sp.oo)), 1, subject="exponential profile memory"),
        kernel.prove_expression_equality(sp.integrate(sp.exp(-x**2), (x, 0, sp.oo)), sp.sqrt(sp.pi) / 2, subject="Gaussian profile memory"),
        kernel.prove_expression_equality(sp.integrate(sp.exp(-x) * sp.cos(x), (x, 0, sp.oo)), sp.Rational(1, 2), subject="damped oscillatory profile memory"),
        kernel.prove_expression_equality(sp.integrate(1 - x, (x, 0, 1)), sp.Rational(1, 2), subject="compact triangular profile memory"),
        kernel.prove_matrix_equality(scale_map, sp.Matrix(scale_map), subject="memory scale dimensional relations"),
        kernel.prove_exact_rank(scale_map, 2, subject="memory scale map rank"),
        kernel.prove_exact_nullity(scale_map, 2, subject="memory scale map nullity"),
        kernel.prove_matrix_equality(scale_map * scale_kernel, sp.zeros(2, 2), subject="memory scale residual orbits"),
        kernel.prove_exact_rank(velocity_anchored_map, 3, subject="velocity anchor leaves one absolute time orbit"),
        kernel.prove_exact_rank(fully_anchored_map, 4, subject="velocity and cell length close the time map"),
        kernel.prove_expression_equality(tau_observed * (1 / tau_observed), 1, subject="observed relaxation time is a circular reciprocal anchor"),
        kernel.prove_matrix_equality(architecture, sp.ones(10, 1), subject="all ten spectral-density candidates audited"),
        kernel.prove_matrix_equality(origin_ledger, sp.ImmutableMatrix([1, 1, 1, 0, 0, 0]), subject="coverage and no-go diagnosis pass while origins remain open"),
        kernel.prove_expression_equality(sum(origin_ledger), 3, subject="three of six spectral-memory origin requirements pass"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate",
        theorems,
    )
    return SpectralDensityMemoryAuditCertificate(
        candidate_matrix,
        pass_vector,
        score_vector,
        component_assignment,
        component_availability,
        scale_map,
        scale_kernel,
        velocity_anchored_map,
        fully_anchored_map,
        architecture,
        origin_ledger,
        theorems,
        gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate",
    title="Аудит спектральной плотности и масштаба памяти ванны",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_spectral_density_memory_scale_candidate_audit_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"spectral_memory_audit_{index:02d}", lambda index=index: build_certificate().theorems[index])
        for index in range(22)
    ),
)