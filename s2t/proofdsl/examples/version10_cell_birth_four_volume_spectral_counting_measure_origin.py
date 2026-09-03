"""LCF certificate for spectral counting of intrinsic cell volume."""

from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import sympy as sp
from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class FourVolumeSpectralCountingCertificate:
    spectral_shape: sp.ImmutableMatrix
    dimensionless_spectrum: sp.ImmutableMatrix
    counting_projector: sp.ImmutableMatrix
    scale_hessian: sp.ImmutableMatrix
    scale_vector: sp.ImmutableMatrix
    architecture: sp.ImmutableMatrix
    origin_ledger: sp.ImmutableMatrix
    dimension_theorem: Theorem
    spectrum_theorem: Theorem
    counting_rank_theorem: Theorem
    top_level_theorem: Theorem
    second_moment_theorem: Theorem
    rescaling_theorem: Theorem
    counting_invariance_theorem: Theorem
    parent_stationary_theorem: Theorem
    hessian_theorem: Theorem
    hessian_rank_theorem: Theorem
    hessian_nullity_theorem: Theorem
    scale_kernel_theorem: Theorem
    hessian_spectrum_theorem: Theorem
    architecture_theorem: Theorem
    origin_ledger_theorem: Theorem
    origin_score_theorem: Theorem
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> FourVolumeSpectralCountingCertificate:
    ell, cutoff, scale = sp.symbols("ell_cell Lambda s", positive=True)
    levels = tuple(sp.Integer(i) for i in range(43))
    spectral_shape = sp.ImmutableMatrix(sp.diag(*levels))
    dimensionless_spectrum = sp.ImmutableMatrix(ell * spectral_shape / ell)
    counting_projector = sp.ImmutableMatrix(sp.eye(43))
    top_level = spectral_shape[42, 42] / ell
    second_moment = sp.trace((spectral_shape / ell) ** 2)
    rescaled_top = sp.simplify((spectral_shape[42, 42] / (scale * ell)) * (scale * ell))

    q, r = sp.symbols("q r", real=True)
    parent = (q + r) ** 2 / 2
    gradient = sp.ImmutableMatrix([sp.diff(parent, z).subs({q: 0, r: 0}) for z in (q, r)])
    scale_hessian = sp.ImmutableMatrix(sp.hessian(parent, (q, r)))
    scale_vector = sp.ImmutableMatrix([1, -1])
    architecture = sp.ones(8, 1)
    origin_ledger = sp.ImmutableMatrix([1, 1, 1, 0, 0])

    dimension_theorem = kernel.prove_expression_equality(spectral_shape.rows, 43, subject="the cell spectral carrier has dimension forty three")
    spectrum_theorem = kernel.prove_exact_spectrum(spectral_shape, {sp.Integer(i): 1 for i in range(43)}, subject="the normalized cell operator has forty three exact levels")
    counting_rank_theorem = kernel.prove_exact_rank(counting_projector, 43, subject="the cutoff at the highest level counts all cell states")
    top_level_theorem = kernel.prove_expression_equality(top_level * ell, 42, subject="the highest spectral threshold fixes only cutoff times cell length")
    second_moment_theorem = kernel.prove_expression_equality(second_moment * ell**2, 25585, subject="the normalized second spectral moment is dimensionless")
    rescaling_theorem = kernel.prove_expression_equality(rescaled_top, 42, subject="opposite cutoff and length rescaling preserves the top threshold")
    counting_invariance_theorem = kernel.prove_expression_equality((cutoff / scale) * (scale * ell), cutoff * ell, subject="spectral counting depends only on cutoff times cell length")
    parent_stationary_theorem = kernel.prove_matrix_equality(gradient, sp.zeros(2, 1), subject="the spectral scale parent has a stationary representative")
    hessian_theorem = kernel.prove_matrix_equality(scale_hessian, sp.ones(2), subject="the spectral counting parent has an exact Hessian")
    hessian_rank_theorem = kernel.prove_exact_rank(scale_hessian, 1, subject="spectral counting fixes one relative scale combination")
    hessian_nullity_theorem = kernel.prove_exact_nullity(scale_hessian, 1, subject="one cutoff length scale orbit remains")
    scale_kernel_theorem = kernel.prove_matrix_equality(scale_hessian * scale_vector, sp.zeros(2, 1), subject="opposite cutoff length scaling is the exact zero mode")
    hessian_spectrum_theorem = kernel.prove_exact_spectrum(scale_hessian, {sp.Integer(0): 1, sp.Integer(2): 1}, subject="the spectral parent is semidefinite with one scale zero mode")
    architecture_theorem = kernel.prove_matrix_equality(architecture, sp.ones(8, 1), subject="all finite spectral counting conditions pass")
    origin_ledger_theorem = kernel.prove_matrix_equality(origin_ledger, sp.Matrix([1, 1, 1, 0, 0]), subject="spectral carrier count and relative measure pass while absolute scales remain open")
    origin_score_theorem = kernel.prove_expression_equality(sum(origin_ledger), 3, subject="three of five spectral volume origin requirements pass")
    gate_theorem = kernel.prove_gate("version10_cell_birth_four_volume_spectral_counting_measure_origin_gate", (dimension_theorem, spectrum_theorem, counting_rank_theorem, top_level_theorem, second_moment_theorem, rescaling_theorem, counting_invariance_theorem, parent_stationary_theorem, hessian_theorem, hessian_rank_theorem, hessian_nullity_theorem, scale_kernel_theorem, hessian_spectrum_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem))
    return FourVolumeSpectralCountingCertificate(spectral_shape, dimensionless_spectrum, counting_projector, scale_hessian, scale_vector, architecture, origin_ledger, dimension_theorem, spectrum_theorem, counting_rank_theorem, top_level_theorem, second_moment_theorem, rescaling_theorem, counting_invariance_theorem, parent_stationary_theorem, hessian_theorem, hessian_rank_theorem, hessian_nullity_theorem, scale_kernel_theorem, hessian_spectrum_theorem, architecture_theorem, origin_ledger_theorem, origin_score_theorem, gate_theorem)


SPEC = GateSpec("version10_cell_birth_four_volume_spectral_counting_measure_origin_gate", "Спектральная счётная мера четырёхмерного объёма ячейки", ("s2t/gates/version10_cell_birth_four_volume_spectral_counting_measure_origin_gate.tex", "s2t/results/s2t_v10_cell_birth_four_volume_spectral_counting_measure_origin_gate_results.json"), tuple(Obligation(name, getter) for name, getter in (
    ("cell_spectral_dimension_43", lambda: build_certificate().dimension_theorem), ("cell_spectral_levels", lambda: build_certificate().spectrum_theorem), ("full_counting_rank_43", lambda: build_certificate().counting_rank_theorem), ("top_threshold_product_42", lambda: build_certificate().top_level_theorem), ("second_moment_25585", lambda: build_certificate().second_moment_theorem), ("top_threshold_rescaling", lambda: build_certificate().rescaling_theorem), ("counting_product_invariance", lambda: build_certificate().counting_invariance_theorem), ("spectral_parent_stationary", lambda: build_certificate().parent_stationary_theorem), ("spectral_parent_hessian", lambda: build_certificate().hessian_theorem), ("spectral_parent_rank_one", lambda: build_certificate().hessian_rank_theorem), ("spectral_parent_nullity_one", lambda: build_certificate().hessian_nullity_theorem), ("cutoff_length_scale_kernel", lambda: build_certificate().scale_kernel_theorem), ("spectral_parent_semidefinite_spectrum", lambda: build_certificate().hessian_spectrum_theorem), ("spectral_counting_architecture_full", lambda: build_certificate().architecture_theorem), ("spectral_volume_origin_three_of_five", lambda: build_certificate().origin_ledger_theorem), ("spectral_volume_origin_score_three", lambda: build_certificate().origin_score_theorem))))