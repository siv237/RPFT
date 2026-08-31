#!/usr/bin/env python3
"""Test the existing colored arrow multiplets as a gauge-covariant Kraus bridge."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eigvalsh


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "s2t/results/s2t_v8_gauge_twirl_cross_sector_kraus_bridge_gate_results.json"
TOL = 1.0e-9

sys.path.insert(0, str(Path(__file__).resolve().parent))
from s2t_v7_derived_relative_involution_curvature_norm_gate import physical_blocks


def block_generator(incidence: np.ndarray) -> np.ndarray:
    target_dimension, source_dimension = incidence.shape
    source_gram = incidence.conj().T @ incidence
    target_gram = incidence @ incidence.conj().T
    source_diagonal = (
        -0.5 * np.kron(np.eye(source_dimension), source_gram)
        -0.5 * np.kron(source_gram.T, np.eye(source_dimension))
    )
    target_diagonal = (
        -0.5 * np.kron(np.eye(target_dimension), target_gram)
        -0.5 * np.kron(target_gram.T, np.eye(target_dimension))
    )
    return np.block(
        [
            [source_diagonal, np.kron(incidence.T, incidence.conj().T)],
            [np.kron(incidence.conj(), incidence), target_diagonal],
        ]
    )


def pair_vector(source: np.ndarray, target: np.ndarray) -> np.ndarray:
    return np.concatenate(
        [source.reshape(-1, order="F"), target.reshape(-1, order="F")]
    )


def block_diagonal(blocks):
    dimension = sum(block.shape[0] for block in blocks)
    result = np.zeros((dimension, dimension), dtype=complex)
    offset = 0
    for block in blocks:
        size = block.shape[0]
        result[offset : offset + size, offset : offset + size] = block
        offset += size
    return result


def random_special_unitary(dimension: int, rng: np.random.Generator) -> np.ndarray:
    seed = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(
        size=(dimension, dimension)
    )
    unitary, _ = np.linalg.qr(seed)
    determinant = np.linalg.det(unitary)
    return unitary / determinant ** (1.0 / dimension)


def gauge_frames(rng: np.random.Generator):
    color = random_special_unitary(3, rng)
    weak = random_special_unitary(2, rng)
    angle = float(rng.uniform(-np.pi, np.pi))

    def phase(charge):
        return np.exp(1j * charge * angle)

    source = block_diagonal(
        [
            phase(1.0 / 6.0) * np.kron(color, weak),
            phase(-1.0 / 2.0) * weak,
            phase(-1.0) * np.eye(1),
            phase(-1.0 / 2.0) * weak,
        ]
    )
    target = block_diagonal(
        [
            phase(2.0 / 3.0) * color,
            phase(-1.0 / 3.0) * color,
            phase(-1.0) * np.eye(1),
            phase(-1.0) * np.eye(1),
            phase(-1.0 / 2.0) * weak,
        ]
    )
    return source, target


reference, all_variations, heavy_labels, _ = physical_blocks()
heavy_variations = all_variations[7:]
assert len(heavy_variations) == len(heavy_labels) == 20

groups = {
    "QLYR": [index for index, label in enumerate(heavy_labels) if label.startswith("QLYR")],
    "XLdR": [index for index, label in enumerate(heavy_labels) if label.startswith("XLdR")],
    "LLXR": [index for index, label in enumerate(heavy_labels) if label.startswith("LLXR")],
    "YLeR": [index for index, label in enumerate(heavy_labels) if label.startswith("YLeR")],
}
assert {name: len(indices) for name, indices in groups.items()} == {
    "QLYR": 6,
    "XLdR": 6,
    "LLXR": 4,
    "YLeR": 4,
}


def normalized_group_generator(indices):
    result = np.zeros((221, 221), dtype=complex)
    for index in indices:
        variation = heavy_variations[index]
        variation = variation / np.linalg.norm(variation, ord="fro")
        result += block_generator(variation)
    return result


group_generators = {
    name: normalized_group_generator(indices) for name, indices in groups.items()
}
cross_generator = group_generators["QLYR"] + group_generators["XLdR"]
internal_lepton_generator = group_generators["LLXR"] + group_generators["YLeR"]

source_dimension = 11
target_dimension = 10
quark_source = np.diag([1.0] * 6 + [0.0] * 5)
quark_target = np.diag([1.0] * 6 + [0.0] * 4)
lepton_source = np.eye(source_dimension) - quark_source
lepton_target = np.eye(target_dimension) - quark_target
identity_vector = pair_vector(np.eye(source_dimension), np.eye(target_dimension))
quark_vector = pair_vector(quark_source, quark_target)
lepton_vector = pair_vector(lepton_source, lepton_target)

central_basis = np.column_stack(
    [quark_vector / np.sqrt(12.0), lepton_vector / np.sqrt(9.0)]
)


def central_restriction(generator):
    return central_basis.conj().T @ (-generator) @ central_basis


central_tests = {}
for name, generator in {
    "QLYR": group_generators["QLYR"],
    "XLdR": group_generators["XLdR"],
    "both_cross_multiplets": cross_generator,
    "internal_lepton_only": internal_lepton_generator,
}.items():
    restriction = central_restriction(generator)
    values = eigvalsh(restriction)
    central_tests[name] = {
        "matrix": [[float(value.real) for value in row] for row in restriction],
        "eigenvalues": [float(value) for value in values],
        "kernel_dimension_inside_C2": int(np.sum(np.abs(values) < TOL)),
    }

assert central_tests["QLYR"]["kernel_dimension_inside_C2"] == 1
assert central_tests["XLdR"]["kernel_dimension_inside_C2"] == 1
assert central_tests["both_cross_multiplets"]["kernel_dimension_inside_C2"] == 1
assert central_tests["internal_lepton_only"]["kernel_dimension_inside_C2"] == 2

cross_unital_residual = float(np.linalg.norm(cross_generator @ identity_vector))
cross_self_adjoint_residual = float(
    np.linalg.norm(cross_generator - cross_generator.conj().T)
)
quark_not_fixed_norm = float(np.linalg.norm(cross_generator @ quark_vector))
lepton_not_fixed_norm = float(np.linalg.norm(cross_generator @ lepton_vector))
assert cross_unital_residual < 1.0e-12
assert cross_self_adjoint_residual < 1.0e-12
assert quark_not_fixed_norm > 1.0e-3
assert lepton_not_fixed_norm > 1.0e-3

# The complete color, weak and U(1) multiplets make the quadratic generator
# gauge covariant although no individual cross arrow is gauge invariant.
rng = np.random.default_rng(20260828)
covariance_residuals = []
for _ in range(12):
    source_frame, target_frame = gauge_frames(rng)
    representation = np.block(
        [
            [
                np.kron(source_frame.conj(), source_frame),
                np.zeros((source_dimension**2, target_dimension**2)),
            ],
            [
                np.zeros((target_dimension**2, source_dimension**2)),
                np.kron(target_frame.conj(), target_frame),
            ],
        ]
    )
    residual = float(
        np.linalg.norm(representation @ cross_generator - cross_generator @ representation)
    )
    covariance_residuals.append(residual)
assert max(covariance_residuals) < 1.0e-10

# The SU(3) center kills every linear cross arrow, so the surviving object is
# genuinely quadratic and carries no colored one-point expectation.
omega = np.exp(2j * np.pi / 3.0)
color_center_source = block_diagonal(
    [omega * np.eye(6), np.eye(2), np.eye(1), np.eye(2)]
)
color_center_target = block_diagonal(
    [omega * np.eye(3), omega * np.eye(3), np.eye(1), np.eye(1), np.eye(2)]
)
sample_index = groups["QLYR"][0]
sample_arrow = heavy_variations[sample_index]
center_orbit_average = sum(
    (
        np.linalg.matrix_power(color_center_target, power)
        @ sample_arrow
        @ np.linalg.matrix_power(color_center_source.conj().T, power)
        for power in range(3)
    ),
    np.zeros_like(sample_arrow),
) / 3.0
linear_center_average_norm = float(np.linalg.norm(center_orbit_average, ord="fro"))
assert linear_center_average_norm < 1.0e-12

# Qualitative primitivity is independent of all positive rates because the
# kernel of a positive sum of Dirichlet forms is the intersection of kernels.
weight_scan = []
for _ in range(64):
    qlyr_weight, xldr_weight = 10.0 ** rng.uniform(-6.0, 6.0, size=2)
    generator = (
        qlyr_weight * group_generators["QLYR"]
        + xldr_weight * group_generators["XLdR"]
    )
    values = eigvalsh(central_restriction(generator))
    kernel_dimension = int(np.sum(np.abs(values) < max(TOL, 1.0e-12 * values[-1])))
    assert kernel_dimension == 1
    weight_scan.append(
        {
            "QLYR_weight": float(qlyr_weight),
            "XLdR_weight": float(xldr_weight),
            "central_kernel_dimension": kernel_dimension,
            "central_decay_eigenvalue": float(values[-1]),
        }
    )

previous_result = json.loads(
    (ROOT / "s2t/results/s2t_v8_markov_fixed_algebra_selector_gate_results.json").read_text(
        encoding="utf-8"
    )
)
assert previous_result["final_fixed_algebra"]["dimension"] == 2
assert previous_result["final_fixed_algebra"]["quark_projector_rank"] == 12
assert previous_result["final_fixed_algebra"]["lepton_vectorlike_projector_rank"] == 9

result = {
    "date": "2026-08-28",
    "gate": "version8_gauge_twirl_cross_sector_kraus_bridge_gate",
    "inherited_fixed_algebra": "C P_quark direct_sum C P_lepton_vectorlike",
    "existing_arrow_multiplets": {
        "cross_sector": {
            "QLYR_real_directions": len(groups["QLYR"]),
            "XLdR_real_directions": len(groups["XLdR"]),
            "total_real_dimension": len(groups["QLYR"]) + len(groups["XLdR"]),
        },
        "internal_lepton_controls": {
            "LLXR_real_directions": len(groups["LLXR"]),
            "YLeR_real_directions": len(groups["YLeR"]),
        },
    },
    "basis_independent_kraus_sum": {
        "formula": "L_cross = sum_e -1/2 ad(D_e)^2 over an HS-orthonormal real cross-arrow basis",
        "unital_residual": cross_unital_residual,
        "self_adjoint_residual": cross_self_adjoint_residual,
        "quark_projector_action_norm": quark_not_fixed_norm,
        "lepton_projector_action_norm": lepton_not_fixed_norm,
        "central_tests": central_tests,
    },
    "gauge_covariance": {
        "random_SU3_SU2_U1_tests": len(covariance_residuals),
        "maximum_superoperator_commutator_norm": max(covariance_residuals),
        "linear_cross_arrow_SU3_center_average_norm": linear_center_average_norm,
        "linear_gauge_singlet_present": False,
        "quadratic_kraus_sum_gauge_invariant": True,
        "colored_one_point_condensate_required": False,
    },
    "rate_robustness": {
        "positive_weight_samples": len(weight_scan),
        "weight_range": "1e-6 through 1e6 independently",
        "central_kernel_dimension_always_one": True,
        "samples": weight_scan,
    },
    "verdict": {
        "existing_cross_arrow_space_is_nonzero": True,
        "direct_linear_gauge_singlet_bridge_exists": False,
        "gauge_twirl_quadratic_kraus_bridge_exists": True,
        "C2_superselection_survives": False,
        "primitive_center_obtained": True,
        "unique_quantitative_rate_derived": False,
        "common_parent_action_hessian_checked": False,
        "status": "positive_gauge_covariant_kraus_bridge_rate_and_parent_open",
        "reason": (
            "the complete colored arrow multiplets have no invariant linear vector, but their "
            "basis-independent quadratic Dirichlet sum is gauge covariant and reduces the "
            "previous C^2 fixed algebra to the scalar identity without a colored condensate"
        ),
    },
    "next_gate": {
        "name": "version8_kraus_bridge_parent_action_hessian_gate",
        "question": (
            "can the gauge-twirled bridge be placed in one parent curvature functional while "
            "preserving the Tome VII 7+20 launch and stable vacuum without choosing its rate?"
        ),
    },
}

payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
OUTPUT.write_text(payload, encoding="utf-8")
print(OUTPUT)
print(hashlib.sha256(payload.encode("utf-8")).hexdigest())