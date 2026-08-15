import contextlib
import importlib
import io
import json
import math
from pathlib import Path

import numpy as np


with contextlib.redirect_stdout(io.StringIO()):
    projection = importlib.import_module("s2t_c6_l21_n3_explicit_projection_audit")


LAMBDA_1 = 4.0
LAMBDA_3 = 16.0
SPECTRAL_GAP = LAMBDA_3 - LAMBDA_1
EPSILON = 1e-4


def normalized_killing_vectors():
    _, killing_matrices = projection.antisym_basis_4()
    norm = math.sqrt(projection.killing_norm_sq)
    return [
        projection.vector_scale(projection.vector_lin(matrix), 1.0 / norm)
        for matrix in killing_matrices
    ]


def weighted_inner(left, right, weight):
    pointwise = {}
    for axis in range(projection.DIM):
        pointwise = projection.add_poly(
            pointwise,
            projection.mul_poly(left[axis], right[axis]),
        )
    weighted = projection.mul_poly(weight, pointwise)
    return sum(
        coefficient * projection.integral_monomial_l21(monomial)
        for monomial, coefficient in weighted.items()
    )


n1_vectors = normalized_killing_vectors()
n3_vectors = [
    projection.coeff_to_vector(projection.orthonormal_basis[:, index])
    for index in range(projection.orthonormal_basis.shape[1])
]
all_vectors = n1_vectors + n3_vectors

strain = np.diag([1.0, -1.0, 0.0, 0.0])
weight = projection.quad_form_poly(strain)
hilbert = np.array(
    [
        [weighted_inner(left, right, weight) for right in all_vectors]
        for left in all_vectors
    ],
    dtype=float,
)
hilbert = (hilbert + hilbert.T) / 2.0
hilbert_31 = hilbert[6:, :6]

forward_31 = projection.projection_coefficients.T
gap_identity_residual = forward_31 + SPECTRAL_GAP * hilbert_31
reverse_13_transpose = forward_31 - SPECTRAL_GAP * hilbert_31

dimension = hilbert.shape[0]
operator_0 = np.diag([LAMBDA_1] * 6 + [LAMBDA_3] * 30)
operator_1 = np.zeros((dimension, dimension), dtype=float)
operator_1[6:, :6] = forward_31
operator_1[:6, 6:] = reverse_13_transpose.T


def symmetric_sqrt(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh((matrix + matrix.T) / 2.0)
    if np.min(eigenvalues) <= 0:
        raise ValueError("Gram matrix is not positive")
    return eigenvectors @ np.diag(np.sqrt(eigenvalues)) @ eigenvectors.T


def selfadjoint_representation(epsilon):
    gram = np.eye(dimension) + epsilon * hilbert
    operator = operator_0 + epsilon * operator_1
    square_root = symmetric_sqrt(gram)
    inverse_square_root = np.linalg.inv(square_root)
    return square_root @ operator @ inverse_square_root


representation_plus = selfadjoint_representation(EPSILON)
representation_minus = selfadjoint_representation(-EPSILON)
representation_0 = operator_0

representation_1 = (representation_plus - representation_minus) / (2.0 * EPSILON)
representation_2 = (
    representation_plus + representation_minus - 2.0 * representation_0
) / (EPSILON**2)

inverse_0 = np.linalg.inv(operator_0)
raw_trace_square = float(
    np.trace(inverse_0 @ operator_1 @ inverse_0 @ operator_1)
)
selfadjoint_trace_square = float(
    np.trace(inverse_0 @ representation_1 @ inverse_0 @ representation_1)
)
similarity_second_trace = float(np.trace(inverse_0 @ representation_2))

raw_logdet_hessian = -raw_trace_square
selfadjoint_logdet_hessian = similarity_second_trace - selfadjoint_trace_square


def logdet(matrix):
    sign, value = np.linalg.slogdet(matrix)
    if sign <= 0:
        raise ValueError("Operator determinant changed sign")
    return value


operator_plus = operator_0 + EPSILON * operator_1
operator_minus = operator_0 - EPSILON * operator_1
raw_finite_difference = (
    logdet(operator_plus) + logdet(operator_minus) - 2.0 * logdet(operator_0)
) / (EPSILON**2)
selfadjoint_finite_difference = (
    logdet(representation_plus)
    + logdet(representation_minus)
    - 2.0 * logdet(representation_0)
) / (EPSILON**2)

similarity_logdet_plus_error = abs(logdet(representation_plus) - logdet(operator_plus))
similarity_logdet_minus_error = abs(logdet(representation_minus) - logdet(operator_minus))

raw_forward_norm_squared = float(np.trace(forward_31.T @ forward_31))
selfadjoint_cross = representation_1[6:, :6]
selfadjoint_cross_norm_squared = float(
    np.trace(selfadjoint_cross.T @ selfadjoint_cross)
)

results = {
    "status": "Hilbert_similarity_second_order_cancels_representation_change_in_logdet",
    "setup": {
        "witness": "A=diag(1,-1,0,0)",
        "dimension": dimension,
        "operator_0": "diag(4 on n1, 16 on n3)",
        "Gram_path": "G(eps)=I+eps H for the isolated representation test",
        "operator_path": "L(eps)=L0+eps L1 with L2=0",
        "selfadjoint_representation": "A(eps)=G(eps)^(1/2)L(eps)G(eps)^(-1/2)",
        "epsilon": EPSILON,
    },
    "first_order_checks": {
        "gap_identity_residual_max_abs": float(
            np.max(np.abs(gap_identity_residual))
        ),
        "raw_forward_norm_squared": raw_forward_norm_squared,
        "selfadjoint_cross_norm_squared": selfadjoint_cross_norm_squared,
    },
    "trace_terms": {
        "raw_trace_square": raw_trace_square,
        "selfadjoint_trace_square": selfadjoint_trace_square,
        "similarity_second_trace": similarity_second_trace,
        "raw_logdet_hessian": raw_logdet_hessian,
        "selfadjoint_logdet_hessian": selfadjoint_logdet_hessian,
        "hessian_difference": selfadjoint_logdet_hessian - raw_logdet_hessian,
    },
    "finite_difference_checks": {
        "raw_logdet_hessian": raw_finite_difference,
        "selfadjoint_logdet_hessian": selfadjoint_finite_difference,
        "finite_difference_hessian_difference": selfadjoint_finite_difference
        - raw_finite_difference,
        "logdet_similarity_plus_error": similarity_logdet_plus_error,
        "logdet_similarity_minus_error": similarity_logdet_minus_error,
    },
    "interpretation": {
        "first_order_80_to_180": "representation-dependent cross-block norm, not a determinant change by itself",
        "second_order_compensation": "the similarity A2 term restores equality of the logdet Hessian",
        "Hilbert_rescue_status": "neutral_for_the_determinant_by_similarity_invariance",
        "remaining_physical_question": "the genuine L_AB operator and same-scheme determinant contribution",
    },
    "decision": {
        "theory_effect": "restores_neutral_outlook_after_apparent_first_order_worsening",
        "C6_status": "still_open",
        "next_required_object": "compute genuine mixed second operator L_AB in a fixed quotient identification and combine it with the basis-invariant raw trace-square",
    },
    "verdict": (
        "The apparent increase of the cross-shell norm from 80 to 180 is exactly a representation effect. "
        "Because G^(1/2)L G^(-1/2) is similar to L, its determinant and log-determinant Hessian are unchanged. "
        "The explicit second-order calculation shows that the additional self-adjoint trace-square is compensated by the second derivative of the similarity representation. "
        "Hilbert/basis transport therefore neither rescues nor worsens C6 at determinant level. "
        "The decisive remaining quantity is the genuine mixed second operator L_AB together with same-scheme Maxwell--ghost bookkeeping."
    ),
}

Path("s2t_c6_hilbert_similarity_invariance_results.json").write_text(
    json.dumps(results, indent=2, ensure_ascii=False) + "\n"
)

print(
    json.dumps(
        {
            "status": results["status"],
            "raw_forward_norm_squared": raw_forward_norm_squared,
            "selfadjoint_cross_norm_squared": selfadjoint_cross_norm_squared,
            "raw_trace_square": raw_trace_square,
            "selfadjoint_trace_square": selfadjoint_trace_square,
            "similarity_second_trace": similarity_second_trace,
            "raw_hessian": raw_logdet_hessian,
            "selfadjoint_hessian": selfadjoint_logdet_hessian,
            "hessian_difference": selfadjoint_logdet_hessian
            - raw_logdet_hessian,
            "finite_difference_difference": selfadjoint_finite_difference
            - raw_finite_difference,
        },
        indent=2,
        ensure_ascii=False,
    )
)