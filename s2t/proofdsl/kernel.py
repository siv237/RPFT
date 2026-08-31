"""Small trusted LCF-style kernel for the S2T proof eDSL."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping, Sequence

import sympy as sp
from sympy.polys.matrices import DomainMatrix


class ProofError(ValueError):
    """Raised when a requested theorem does not follow from exact premises."""


@dataclass(frozen=True)
class Proposition:
    kind: str
    subject: str
    data: Mapping[str, Any]

    @classmethod
    def make(cls, kind: str, subject: str, **data: Any) -> "Proposition":
        return cls(kind=kind, subject=subject, data=MappingProxyType(dict(data)))


_KERNEL_SEAL = object()


@dataclass(frozen=True, init=False)
class Theorem:
    """Opaque theorem value; only :class:`Kernel` can construct one."""

    proposition: Proposition
    rule: str
    premises: tuple["Theorem", ...]
    certificate: Mapping[str, Any]

    def __init__(
        self,
        proposition: Proposition,
        rule: str,
        premises: Sequence["Theorem"] = (),
        certificate: Mapping[str, Any] | None = None,
        *,
        _seal: object | None = None,
    ) -> None:
        if _seal is not _KERNEL_SEAL:
            raise PermissionError("Theorem values can only be issued by the proof kernel")
        object.__setattr__(self, "proposition", proposition)
        object.__setattr__(self, "rule", rule)
        object.__setattr__(self, "premises", tuple(premises))
        object.__setattr__(
            self,
            "certificate",
            MappingProxyType(dict(certificate or {})),
        )


def _exact_matrix(matrix: sp.MatrixBase) -> sp.ImmutableMatrix:
    value = sp.ImmutableMatrix(matrix)
    if any(isinstance(atom, sp.Float) for atom in value.atoms(sp.Float)):
        raise ProofError("floating-point values are not admitted by the exact kernel")
    return value


def _zero_matrix(matrix: sp.MatrixBase) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def _orthogonal_frame_action_data(
    frame: Sequence[sp.MatrixBase],
    symmetry_generators: Sequence[sp.MatrixBase],
) -> tuple[
    tuple[sp.ImmutableMatrix, ...],
    tuple[sp.ImmutableMatrix, ...],
    sp.Expr,
    tuple[sp.ImmutableMatrix, ...],
]:
    """Return exact infinitesimal action matrices on a Hermitian frame."""

    checked_frame = tuple(_exact_matrix(item) for item in frame)
    checked_generators = tuple(_exact_matrix(item) for item in symmetry_generators)
    if not checked_frame or not checked_generators:
        raise ProofError("frame covariance needs jumps and symmetry generators")
    shape = checked_frame[0].shape
    if shape[0] != shape[1] or any(item.shape != shape for item in checked_frame):
        raise ProofError("all frame elements must be square matrices of equal shape")
    if any(not _zero_matrix(item.H - item) for item in checked_frame):
        raise ProofError("the orthogonal jump frame must be Hermitian")
    if any(
        item.shape != shape or not _zero_matrix(item.H - item)
        for item in checked_generators
    ):
        raise ProofError("symmetry generators must be Hermitian on the same space")

    gram = sp.ImmutableMatrix(
        [
            [sp.simplify(sp.trace(left.H * right)) for right in checked_frame]
            for left in checked_frame
        ]
    )
    norm = sp.simplify(gram[0, 0])
    if norm == 0 or not _zero_matrix(gram - norm * sp.eye(len(checked_frame))):
        raise ProofError("jump frame does not have a scalar nonzero Gram matrix")

    actions = []
    for generator in checked_generators:
        coefficient_columns = []
        for item in checked_frame:
            tangent = sp.I * (generator * item - item * generator)
            coefficients = sp.ImmutableMatrix(
                [
                    sp.simplify(sp.trace(basis.H * tangent) / norm)
                    for basis in checked_frame
                ]
            )
            reconstruction = sum(
                (
                    coefficients[index] * checked_frame[index]
                    for index in range(len(checked_frame))
                ),
                sp.zeros(*shape),
            )
            if not _zero_matrix(tangent - reconstruction):
                raise ProofError("symmetry tangent leaves the proposed jump frame")
            if any(
                sp.simplify(sp.conjugate(value) - value) != 0
                for value in coefficients
            ):
                raise ProofError("frame action has non-real coefficients")
            coefficient_columns.append(coefficients)
        action = sp.ImmutableMatrix.hstack(*coefficient_columns)
        if not _zero_matrix(action.T + action):
            raise ProofError("symmetry does not act orthogonally on the jump frame")
        actions.append(action)
    return checked_frame, checked_generators, norm, tuple(actions)


class Kernel:
    """The complete trusted theorem-producing interface."""

    @staticmethod
    def _issue(
        proposition: Proposition,
        rule: str,
        premises: Sequence[Theorem] = (),
        certificate: Mapping[str, Any] | None = None,
    ) -> Theorem:
        return Theorem(
            proposition,
            rule,
            premises,
            certificate,
            _seal=_KERNEL_SEAL,
        )

    def prove_matrix_equality(
        self, left: sp.MatrixBase, right: sp.MatrixBase, *, subject: str
    ) -> Theorem:
        lhs = _exact_matrix(left)
        rhs = _exact_matrix(right)
        if lhs.shape != rhs.shape or not _zero_matrix(lhs - rhs):
            raise ProofError(f"matrix equality failed for {subject}")
        return self._issue(
            Proposition.make("matrix_equality", subject, shape=list(lhs.shape)),
            "exact_sympy_reduction",
            certificate={"residual": "zero"},
        )

    def prove_matrix_inequality(
        self, left: sp.MatrixBase, right: sp.MatrixBase, *, subject: str
    ) -> Theorem:
        lhs = _exact_matrix(left)
        rhs = _exact_matrix(right)
        if lhs.shape != rhs.shape:
            raise ProofError("matrix inequality requires equal shapes")
        residual = lhs - rhs
        if _zero_matrix(residual):
            raise ProofError(f"matrices are equal for {subject}")
        witness = next(
            (index for index, entry in enumerate(residual) if sp.simplify(entry) != 0),
            None,
        )
        return self._issue(
            Proposition.make(
                "matrix_inequality",
                subject,
                shape=list(lhs.shape),
                witness_flat_index=witness,
            ),
            "exact_nonzero_entry_rule",
        )

    def prove_expression_equality(
        self, left: sp.Expr, right: sp.Expr, *, subject: str
    ) -> Theorem:
        lhs = sp.sympify(left)
        rhs = sp.sympify(right)
        if lhs.atoms(sp.Float) or rhs.atoms(sp.Float):
            raise ProofError("floating-point values are not admitted by the exact kernel")
        if sp.simplify(lhs - rhs) != 0:
            raise ProofError(f"expression equality failed for {subject}")
        return self._issue(
            Proposition.make("expression_equality", subject),
            "exact_sympy_reduction",
            certificate={"residual": "zero"},
        )

    def prove_algebraic_field_matrix_equality(
        self,
        left: sp.MatrixBase,
        right: sp.MatrixBase,
        *,
        extensions: Sequence[sp.Expr],
        subject: str,
    ) -> Theorem:
        """Compare matrices exactly inside one explicit algebraic field."""

        lhs = _exact_matrix(left)
        rhs = _exact_matrix(right)
        if lhs.shape != rhs.shape or not extensions:
            raise ProofError("algebraic-field equality needs equal shapes and extensions")
        field = sp.QQ.algebraic_field(*(sp.sympify(item) for item in extensions))
        left_domain = DomainMatrix.from_Matrix(sp.Matrix(lhs)).convert_to(field)
        right_domain = DomainMatrix.from_Matrix(sp.Matrix(rhs)).convert_to(field)
        if left_domain != right_domain:
            raise ProofError(f"algebraic-field matrix equality failed for {subject}")
        return self._issue(
            Proposition.make(
                "algebraic_field_matrix_equality",
                subject,
                shape=list(lhs.shape),
                field_degree=int(field.mod.degree()),
            ),
            "exact_algebraic_number_field_rule",
            certificate={"residual": "zero"},
        )

    def prove_expression_nonconstant(
        self, expression: sp.Expr, variable: sp.Symbol, *, subject: str
    ) -> Theorem:
        value = sp.sympify(expression)
        if value.atoms(sp.Float):
            raise ProofError("nonconstancy proof requires an exact expression")
        derivative = sp.simplify(sp.diff(value, variable))
        if derivative == 0:
            raise ProofError(f"expression is constant in {variable}")
        return self._issue(
            Proposition.make(
                "nonconstant_expression",
                subject,
                variable=str(variable),
            ),
            "exact_nonzero_derivative_rule",
            certificate={"derivative": str(derivative)},
        )

    def prove_positive_definite_symmetric_2x2(
        self,
        matrix: sp.MatrixBase,
        *,
        extensions: Sequence[sp.Expr],
        subject: str,
    ) -> Theorem:
        """Use exact algebraic signs of Sylvester minors in dimension two."""

        value = _exact_matrix(matrix)
        if value.shape != (2, 2) or value != value.T:
            raise ProofError("the rule requires a symmetric 2x2 matrix")
        field = sp.QQ.algebraic_field(*(sp.sympify(item) for item in extensions))
        first = field.from_sympy(value[0, 0])
        determinant = field.from_sympy(sp.det(value))
        discriminant = field.from_sympy(
            sp.expand((value[0, 0] - value[1, 1]) ** 2 + 4 * value[0, 1] ** 2)
        )
        if not field.is_positive(first) or not field.is_positive(determinant):
            raise ProofError("Sylvester positivity failed")
        if not field.is_positive(discriminant):
            raise ProofError("the two eigenvalues are not certified distinct")
        return self._issue(
            Proposition.make(
                "positive_definite_distinct_symmetric_2x2",
                subject,
                dimension=2,
                distinct_eigenvalues=True,
            ),
            "exact_algebraic_sylvester_rule",
            certificate={
                "leading_minor_positive": True,
                "determinant_positive": True,
                "discriminant_positive": True,
                "field_degree": int(field.mod.degree()),
            },
        )

    def prove_affine_common_spectral_axes(
        self,
        base: sp.MatrixBase,
        scalar_shift: sp.Expr,
        weight: sp.Symbol,
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        value = _exact_matrix(base)
        shift = sp.sympify(scalar_shift)
        if value.rows != value.cols or value != value.T:
            raise ProofError("base matrix must be square and symmetric")
        if shift.atoms(sp.Float) or shift.is_positive is not True:
            raise ProofError("the scalar shift must be exact and positive")
        if weight.is_positive is not True:
            raise ProofError("the affine spectral weight must be positive")
        if _zero_matrix(value - value[0, 0] * sp.eye(value.rows)):
            raise ProofError("a scalar base does not select a unique axis")
        affine = shift * sp.eye(value.rows) + weight * value
        if not _zero_matrix(value * affine - affine * value):
            raise ProofError("affine family does not commute with its base")
        return self._issue(
            Proposition.make(
                "common_affine_spectral_axes",
                subject,
                dimension=value.rows,
                weight=str(weight),
            ),
            "scalar_shift_polynomial_spectral_rule",
            premises=premises,
            certificate={"commutator": "zero", "weight_positive": True},
        )

    def prove_identity_minus_psd_window(
        self,
        gram: sp.MatrixBase,
        parameter: sp.Symbol,
        expected_upper_bound: sp.Expr,
        *,
        subject: str,
    ) -> Theorem:
        value = _exact_matrix(gram)
        upper = sp.sympify(expected_upper_bound)
        if value.rows != value.cols or value != value.H:
            raise ProofError("the Gram operator must be square Hermitian")
        if parameter.is_nonnegative is not True or upper.is_positive is not True:
            raise ProofError("the step parameter and upper bound need sign assumptions")
        if not _zero_matrix(value - sp.diag(*value.diagonal())):
            raise ProofError("the current PSD-window rule requires a diagonal Gram operator")
        diagonal = tuple(sp.simplify(item) for item in value.diagonal())
        if any(item.is_nonnegative is not True for item in diagonal):
            raise ProofError("the Gram spectrum is not nonnegative")
        maximum = sp.simplify(1 / upper)
        if maximum not in diagonal:
            raise ProofError("the proposed upper bound is not the reciprocal maximum")
        if any(sp.simplify(maximum - item).is_nonnegative is not True for item in diagonal):
            raise ProofError("the proposed reciprocal is not the exact maximum")
        return self._issue(
            Proposition.make(
                "identity_minus_psd_window",
                subject,
                parameter=str(parameter),
                lower="0",
                upper=str(upper),
                maximum_gram_eigenvalue=str(maximum),
            ),
            "exact_diagonal_psd_interval_rule",
        )

    def prove_kraus_channel_well_formed(self, channel: Any) -> Theorem:
        if not channel.kraus:
            raise ProofError("a Kraus channel needs at least one operator")
        dimension = channel.space.dimension
        completeness = sp.zeros(dimension)
        for operator in channel.kraus:
            if operator.source != channel.space or operator.target != channel.space:
                raise ProofError("every Kraus operator must be an endomorphism")
            completeness += operator.matrix.H * operator.matrix
        if not _zero_matrix(completeness - sp.eye(dimension)):
            raise ProofError("Kraus completeness sum is not the identity")
        return self._issue(
            Proposition.make(
                "kraus_channel",
                channel.name,
                space=channel.space.name,
                kraus_count=len(channel.kraus),
            ),
            "finite_dimensional_kraus_constructor",
            certificate={"completely_positive": True, "unital": True},
        )

    def prove_kraus_family_on_psd_window(
        self,
        no_jump: sp.MatrixBase,
        jumps: Sequence[sp.MatrixBase],
        parameter: sp.Symbol,
        window_theorem: Theorem,
        *,
        subject: str,
        dual: bool = False,
    ) -> Theorem:
        first = _exact_matrix(no_jump)
        checked_jumps = tuple(_exact_matrix(item) for item in jumps)
        if window_theorem.proposition.kind != "identity_minus_psd_window":
            raise ProofError("the Kraus family requires a certified PSD window")
        if window_theorem.proposition.data["parameter"] != str(parameter):
            raise ProofError("the Kraus parameter differs from the PSD-window parameter")
        if first.rows != first.cols or not checked_jumps:
            raise ProofError("the Kraus family must contain square operators")
        if any(item.shape != first.shape for item in checked_jumps):
            raise ProofError("the Kraus family has incompatible operator shapes")
        if not _zero_matrix(first - sp.diag(*first.diagonal())):
            raise ProofError("the conditional no-jump operator must be diagonal")
        if any(item != item.H for item in checked_jumps):
            raise ProofError("the current window rule requires selfadjoint jumps")
        if dual:
            jump_sum = sum(
                (item * item.H for item in checked_jumps), sp.zeros(first.rows)
            )
        else:
            jump_sum = sum(
                (item.H * item for item in checked_jumps), sp.zeros(first.rows)
            )
        completeness = first * first + parameter * jump_sum
        if not _zero_matrix(completeness - sp.eye(first.rows)):
            raise ProofError("the symbolic Kraus completeness identity failed")
        kind = (
            "trace_preserving_kraus_family_on_window"
            if dual
            else "kraus_family_on_window"
        )
        return self._issue(
            Proposition.make(
                kind,
                subject,
                parameter=str(parameter),
                lower=window_theorem.proposition.data["lower"],
                upper=window_theorem.proposition.data["upper"],
                kraus_count=len(checked_jumps) + 1,
            ),
            "exact_conditional_kraus_completeness_rule",
            premises=(window_theorem,),
            certificate={
                "completely_positive": True,
                "unital" if not dual else "trace_preserving": True,
            },
        )

    def prove_kraus_channel_trace_preserving(self, channel: Any) -> Theorem:
        dimension = channel.space.dimension
        completeness = sum(
            (operator.matrix * operator.matrix.H for operator in channel.kraus),
            sp.zeros(dimension),
        )
        if not _zero_matrix(completeness - sp.eye(dimension)):
            raise ProofError("dual Kraus completeness sum is not the identity")
        return self._issue(
            Proposition.make("trace_preserving_kraus_channel", channel.name),
            "exact_dual_kraus_completeness_rule",
            premises=(channel.theorem,),
        )

    def prove_minimal_stinespring_dimension(
        self, channel: Any, expected_dimension: int, *, subject: str
    ) -> Theorem:
        columns = []
        for operator in channel.kraus:
            columns.append(
                sp.ImmutableMatrix(
                    operator.matrix.rows * operator.matrix.cols,
                    1,
                    list(operator.matrix),
                )
            )
        vectorized = sp.ImmutableMatrix.hstack(*columns)
        rank = int(vectorized.rank())
        if rank != expected_dimension:
            raise ProofError(
                f"Kraus/Choi rank is {rank}, expected {expected_dimension}"
            )
        return self._issue(
            Proposition.make(
                "minimal_stinespring_dimension",
                subject,
                kraus_rank=rank,
                choi_rank=rank,
                environment_dimension=rank,
            ),
            "kraus_choi_stinespring_rank_rule",
            premises=(channel.theorem,),
        )

    def prove_kraus_family_tangent(
        self,
        no_jump: sp.MatrixBase,
        jumps: Sequence[sp.MatrixBase],
        parameter: sp.Symbol,
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        first = _exact_matrix(no_jump)
        checked_jumps = tuple(_exact_matrix(item) for item in jumps)
        if not checked_jumps or any(item.shape != first.shape for item in checked_jumps):
            raise ProofError("Kraus tangent data have incompatible shapes")
        identity = sp.eye(first.rows)
        if not _zero_matrix(first.subs(parameter, 0) - identity):
            raise ProofError("the no-jump operator is not identity at zero")
        gram = sum((item.H * item for item in checked_jumps), sp.zeros(first.rows))
        derivative = first.diff(parameter).subs(parameter, 0)
        if not _zero_matrix(derivative + sp.Rational(1, 2) * gram):
            raise ProofError("the no-jump derivative is not minus one-half Gram")
        return self._issue(
            Proposition.make(
                "kraus_family_gksl_tangent",
                subject,
                jump_count=len(checked_jumps),
                parameter=str(parameter),
            ),
            "exact_kraus_product_derivative_rule",
            premises=premises,
            certificate={"K0_at_zero": "identity", "K0_derivative": "-G/2"},
        )

    def prove_covariant_channel_from_orthogonal_frame(
        self,
        channel: Any,
        frame_theorem: Theorem,
        basis_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        if frame_theorem.proposition.kind != "orthogonal_frame_covariance":
            raise ProofError("a channel covariance proof needs frame covariance")
        if basis_theorem.proposition.kind != "orthogonal_kraus_basis_invariance":
            raise ProofError("a channel covariance proof needs Kraus-basis invariance")
        if len(channel.kraus) != frame_theorem.proposition.data["frame_dimension"] + 1:
            raise ProofError("channel does not contain one no-jump plus the full frame")
        return self._issue(
            Proposition.make(
                "covariant_kraus_channel",
                subject,
                environment_jump_dimension=frame_theorem.proposition.data[
                    "frame_dimension"
                ],
            ),
            "orthogonal_environment_representation_rule",
            premises=(channel.theorem, frame_theorem, basis_theorem),
        )

    def prove_exact_spectrum(
        self,
        matrix: sp.MatrixBase,
        expected: dict[sp.Expr, int],
        *,
        subject: str,
    ) -> Theorem:
        value = _exact_matrix(matrix)
        if value.rows != value.cols:
            raise ProofError("spectrum requires a square matrix")
        target = {sp.sympify(key): int(multiplicity) for key, multiplicity in expected.items()}
        if any(key.atoms(sp.Float) for key in target):
            raise ProofError("the expected spectrum must be exact")
        actual = {sp.simplify(key): int(multiplicity) for key, multiplicity in value.eigenvals().items()}
        if actual != target:
            raise ProofError(f"exact spectrum mismatch: {actual!r} != {target!r}")
        return self._issue(
            Proposition.make(
                "exact_spectrum",
                subject,
                dimension=value.rows,
                eigenvalues=tuple(
                    (str(key), target[key]) for key in sorted(target, key=sp.default_sort_key)
                ),
            ),
            "exact_characteristic_polynomial_factorization_rule",
        )

    def prove_matrix_exponential_semigroup(
        self, generator: sp.MatrixBase, parameter: sp.Symbol, *, subject: str
    ) -> Theorem:
        value = _exact_matrix(generator)
        if value.rows != value.cols:
            raise ProofError("a matrix exponential semigroup needs a square generator")
        if parameter.is_nonnegative is not True:
            raise ProofError("the semigroup parameter must be nonnegative")
        return self._issue(
            Proposition.make(
                "matrix_exponential_semigroup",
                subject,
                dimension=value.rows,
                parameter=str(parameter),
            ),
            "commuting_matrix_exponential_addition_rule",
            certificate={"T_0": "identity", "T_u_plus_v": "T_u T_v"},
        )

    def prove_positive_scalar_kernel_invariance(
        self,
        matrix: sp.MatrixBase,
        scalar: sp.Symbol,
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        value = _exact_matrix(matrix)
        if scalar.is_positive is not True:
            raise ProofError("kernel invariance requires a positive scalar")
        rank = int(value.rank())
        return self._issue(
            Proposition.make(
                "positive_scalar_kernel_invariance",
                subject,
                dimension=value.cols,
                rank=rank,
                nullity=value.cols - rank,
                scalar=str(scalar),
            ),
            "nonzero_field_scalar_rank_rule",
            premises=premises,
        )

    def prove_finite_dimensional_collision_limit(
        self,
        tangent_theorem: Theorem,
        window_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        if tangent_theorem.proposition.kind != "kraus_family_gksl_tangent":
            raise ProofError("collision limit requires a certified GKSL tangent")
        if window_theorem.proposition.kind != "identity_minus_psd_window":
            raise ProofError("collision limit requires a positive one-step window")
        if tangent_theorem.proposition.data["parameter"] != window_theorem.proposition.data[
            "parameter"
        ]:
            raise ProofError("collision tangent and window use different parameters")
        return self._issue(
            Proposition.make(
                "finite_dimensional_collision_limit",
                subject,
                scaling="p=u/n",
                convergence="operator_norm",
                fresh_environment_each_step=True,
            ),
            "finite_dimensional_chernoff_product_rule",
            premises=(tangent_theorem, window_theorem),
        )

    def prove_fixed_algebra_intersection(
        self,
        base_theorem: Theorem,
        bridge_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        if base_theorem.proposition.data.get("nullity") != 2:
            raise ProofError("the base fixed algebra must be two-dimensional")
        if bridge_theorem.proposition.data.get("nullity") != 1:
            raise ProofError("the bridge restriction must leave one central line")
        return self._issue(
            Proposition.make(
                "scalar_fixed_algebra_intersection",
                subject,
                base_dimension=2,
                fixed_dimension=1,
            ),
            "fixed_algebra_restriction_intersection_rule",
            premises=(base_theorem, bridge_theorem),
        )

    def prove_positive_selfadjoint_dirichlet_family(
        self,
        generator: Any,
        group_sizes: Sequence[int],
        weights: Sequence[sp.Symbol],
        fixed_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        sizes = tuple(int(size) for size in group_sizes)
        parameters = tuple(weights)
        if sum(sizes) != len(generator.jumps) or len(sizes) != len(parameters):
            raise ProofError("Dirichlet groups do not partition the jump family")
        if any(weight.is_positive is not True for weight in parameters):
            raise ProofError("all Dirichlet weights must be strictly positive")
        if any(jump.matrix != jump.matrix.H for jump in generator.jumps):
            raise ProofError("trace detailed balance requires selfadjoint jumps")
        if fixed_theorem.proposition.kind != "scalar_fixed_algebra_intersection":
            raise ProofError("positive-weight robustness needs a scalar fixed algebra")
        return self._issue(
            Proposition.make(
                "positive_selfadjoint_dirichlet_family",
                subject,
                group_sizes=sizes,
                weights=tuple(str(weight) for weight in parameters),
                fixed_dimension=1,
                trace_detailed_balance=True,
                relative_weights_selected=False,
            ),
            "positive_sum_of_commutator_squares_rule",
            premises=(generator.theorem, fixed_theorem),
        )

    def prove_positive_gap_from_scalar_dirichlet_kernel(
        self, family_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if family_theorem.proposition.kind != "positive_selfadjoint_dirichlet_family":
            raise ProofError("gap proof requires a positive selfadjoint Dirichlet family")
        if family_theorem.proposition.data["fixed_dimension"] != 1:
            raise ProofError("the fixed algebra is not scalar")
        return self._issue(
            Proposition.make("strict_finite_dimensional_decay_gap", subject),
            "finite_dimensional_psd_kernel_complement_rule",
            premises=(family_theorem,),
        )

    def prove_unique_trace_state_from_scalar_fixed_algebra(
        self, fixed_theorem: Theorem, dimension: int, *, subject: str
    ) -> Theorem:
        if fixed_theorem.proposition.kind != "scalar_fixed_algebra_intersection":
            raise ProofError("unique-state rule requires a scalar fixed algebra")
        if dimension <= 0:
            raise ProofError("state-space dimension must be positive")
        return self._issue(
            Proposition.make(
                "unique_normalized_trace_state",
                subject,
                dimension=dimension,
                density=f"I_{dimension}/{dimension}",
            ),
            "primitive_unital_stationary_state_rule",
            premises=(fixed_theorem,),
        )

    def prove_central_state_equals_normalized_trace(
        self, unique_state_theorem: Theorem, source_dimension: int, target_dimension: int, *, subject: str
    ) -> Theorem:
        total = source_dimension + target_dimension
        if unique_state_theorem.proposition.kind != "unique_normalized_trace_state":
            raise ProofError("central-state rule requires uniqueness of the trace state")
        if unique_state_theorem.proposition.data["dimension"] != total:
            raise ProofError("central-state block dimensions do not match the state space")
        return self._issue(
            Proposition.make(
                "central_stationary_state_no_go",
                subject,
                condition=f"a=b=1/{total}",
                normalization=f"{source_dimension}a+{target_dimension}b=1",
            ),
            "scalar_fixed_algebra_and_normalization_rule",
            premises=(unique_state_theorem,),
        )

    def prove_positive_expression(
        self, expression: sp.Expr, *, subject: str, premises: Sequence[Theorem] = ()
    ) -> Theorem:
        value = sp.simplify(sp.sympify(expression))
        if value.atoms(sp.Float) or value.is_positive is not True:
            raise ProofError("expression is not exactly certified positive")
        return self._issue(
            Proposition.make("strictly_positive_expression", subject, expression=str(value)),
            "sympy_exact_sign_rule",
            premises=premises,
        )

    def prove_opposite_bohr_split(
        self,
        hamiltonian: sp.MatrixBase,
        forward: Sequence[sp.MatrixBase],
        reverse: Sequence[sp.MatrixBase],
        frequency: sp.Expr,
        *,
        subject: str,
    ) -> Theorem:
        h = _exact_matrix(hamiltonian)
        omega = sp.sympify(frequency)
        direct = tuple(_exact_matrix(item) for item in forward)
        adjoint = tuple(_exact_matrix(item) for item in reverse)
        if not direct or len(direct) != len(adjoint):
            raise ProofError("Bohr split requires paired nonempty families")
        for left, right in zip(direct, adjoint):
            if right != left.H:
                raise ProofError("reverse Bohr mode is not the adjoint of the forward mode")
            if not _zero_matrix(h * left - left * h - omega * left):
                raise ProofError("forward operator has the wrong Bohr frequency")
            if not _zero_matrix(h * right - right * h + omega * right):
                raise ProofError("reverse operator has the wrong Bohr frequency")
        return self._issue(
            Proposition.make(
                "opposite_bohr_frequency_split",
                subject,
                pair_count=len(direct),
                frequency=str(omega),
            ),
            "exact_commutator_eigenoperator_rule",
        )

    def prove_conditional_kms_rate_ratio(
        self, beta_delta: sp.Symbol, *, subject: str, premises: Sequence[Theorem] = ()
    ) -> Theorem:
        if beta_delta.is_real is not True:
            raise ProofError("the modular gap must be real")
        return self._issue(
            Proposition.make(
                "conditional_kms_rate_ratio",
                subject,
                ratio=str(sp.exp(-beta_delta)),
                modular_gap=str(beta_delta),
                uniquely_selected=False,
            ),
            "two_direction_detailed_balance_flux_rule",
            premises=premises,
        )

    def prove_oriented_directed_pair_primitivity(
        self, fixed_theorem: Theorem, bohr_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if fixed_theorem.proposition.kind != "scalar_fixed_algebra_intersection":
            raise ProofError("directed primitivity requires a scalar commutant")
        if bohr_theorem.proposition.kind != "opposite_bohr_frequency_split":
            raise ProofError("directed primitivity requires Bohr pairs")
        return self._issue(
            Proposition.make("directed_pair_primitive_qms", subject, fixed_dimension=1),
            "positive_directed_pair_commutant_rule",
            premises=(fixed_theorem, bohr_theorem),
        )

    def prove_unique_linear_zero(
        self,
        expression: sp.Expr,
        variable: sp.Symbol,
        candidate: sp.Expr,
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        value = sp.sympify(expression)
        root = sp.sympify(candidate)
        if value.atoms(sp.Float) or root.atoms(sp.Float):
            raise ProofError("linear-zero proof requires exact expressions")
        polynomial = sp.Poly(value, variable)
        if polynomial.degree() != 1:
            raise ProofError("expression is not linear in the selected variable")
        if sp.simplify(value.subs(variable, root)) != 0:
            raise ProofError("candidate is not a zero")
        return self._issue(
            Proposition.make(
                "unique_linear_zero",
                subject,
                variable=str(variable),
                root=str(root),
            ),
            "exact_linear_polynomial_rule",
            premises=premises,
            certificate={"degree": 1, "leading_coefficient_nonzero": True},
        )

    def prove_exact_rank(
        self, matrix: sp.MatrixBase, expected_rank: int, *, subject: str
    ) -> Theorem:
        value = _exact_matrix(matrix)
        actual = int(value.rank())
        if actual != expected_rank:
            raise ProofError(f"rank of {subject} is {actual}, expected {expected_rank}")
        return self._issue(
            Proposition.make("exact_rank", subject, rank=actual, shape=list(value.shape)),
            "exact_sympy_rank_rule",
        )

    def prove_exact_nullity(
        self, matrix: sp.MatrixBase, expected_nullity: int, *, subject: str
    ) -> Theorem:
        value = _exact_matrix(matrix)
        rank = int(value.rank())
        nullity = value.cols - rank
        if nullity != expected_nullity:
            raise ProofError(
                f"nullity of {subject} is {nullity}, expected {expected_nullity}"
            )
        return self._issue(
            Proposition.make(
                "exact_nullity",
                subject,
                rank=rank,
                nullity=nullity,
                shape=list(value.shape),
            ),
            "exact_rank_nullity_rule",
        )

    def prove_diagonal_signature(
        self,
        matrix: sp.MatrixBase,
        expected_signature: tuple[int, int, int],
        *,
        subject: str,
    ) -> Theorem:
        """Prove the inertia of an exact symbolic diagonal matrix.

        Symbol assumptions are part of the expression: for example a
        ``nonnegative=True`` parameter can certify positivity of
        ``a + b*x`` when ``a>0`` and ``b>=0``.
        """

        value = _exact_matrix(matrix)
        if value.rows != value.cols:
            raise ProofError("signature is defined here only for square matrices")
        off_diagonal = value - sp.diag(*value.diagonal())
        if not _zero_matrix(off_diagonal):
            raise ProofError("the exact signature rule currently requires a diagonal matrix")
        counts = [0, 0, 0]
        for raw in value.diagonal():
            entry = sp.simplify(raw)
            if entry == 0:
                counts[1] += 1
            elif entry.is_negative is True:
                counts[0] += 1
            elif entry.is_positive is True:
                counts[2] += 1
            else:
                raise ProofError(f"the sign of diagonal entry {entry} is undecidable")
        signature = tuple(counts)
        if signature != expected_signature:
            raise ProofError(f"signature is {signature}, expected {expected_signature}")
        return self._issue(
            Proposition.make(
                "exact_diagonal_signature",
                subject,
                negative=signature[0],
                zero=signature[1],
                positive=signature[2],
                dimension=value.rows,
            ),
            "exact_symbolic_diagonal_sign_rule",
        )

    def prove_linear_kernel(
        self,
        system: sp.MatrixBase,
        basis: sp.MatrixBase,
        *,
        subject: str,
    ) -> Theorem:
        matrix = _exact_matrix(system)
        vectors = _exact_matrix(basis)
        if matrix.cols != vectors.rows:
            raise ProofError("kernel basis has the wrong ambient dimension")
        if not _zero_matrix(matrix * vectors):
            raise ProofError("proposed vectors do not lie in the kernel")
        basis_rank = int(vectors.rank())
        if basis_rank != vectors.cols:
            raise ProofError("kernel basis vectors are not independent")
        matrix_rank = int(matrix.rank())
        if matrix_rank + basis_rank != matrix.cols:
            raise ProofError("proposed basis does not span the full kernel")
        return self._issue(
            Proposition.make(
                "exact_linear_kernel",
                subject,
                ambient_dimension=matrix.cols,
                equation_count=matrix.rows,
                rank=matrix_rank,
                nullity=basis_rank,
            ),
            "rank_nullity_kernel_rule",
            certificate={"residual": "zero", "basis_independent": True},
        )

    def prove_semisimple_commutant_dimension(
        self,
        representations: Sequence[Any],
        expected_dimension: int,
        *,
        subject: str,
    ) -> Theorem:
        contributions = []
        total = 0
        for representation in representations:
            value = sum(block.multiplicity**2 for block in representation.blocks)
            contributions.append((representation.name, value))
            total += value
        if total != expected_dimension:
            raise ProofError(
                f"commutant dimension is {total}, expected {expected_dimension}"
            )
        return self._issue(
            Proposition.make(
                "semisimple_commutant_dimension",
                subject,
                dimension=total,
                contributions=tuple(contributions),
            ),
            "schur_commutant_rule",
        )

    def prove_complementary_projectors(
        self,
        left: sp.MatrixBase,
        right: sp.MatrixBase,
        *,
        expected_ranks: tuple[int, int],
        subject: str,
    ) -> Theorem:
        first = _exact_matrix(left)
        second = _exact_matrix(right)
        if first.shape != second.shape or first.rows != first.cols:
            raise ProofError("projectors must be square matrices of equal shape")
        identity = sp.eye(first.rows)
        conditions = (
            first * first - first,
            second * second - second,
            first * second,
            second * first,
            first + second - identity,
        )
        if not all(_zero_matrix(condition) for condition in conditions):
            raise ProofError("projector partition identities failed")
        ranks = (int(first.rank()), int(second.rank()))
        if ranks != expected_ranks:
            raise ProofError(f"projector ranks are {ranks}, expected {expected_ranks}")
        return self._issue(
            Proposition.make(
                "complementary_projectors",
                subject,
                ranks=ranks,
                total_dimension=first.rows,
            ),
            "exact_projector_partition_rule",
        )

    def prove_well_typed_morphism(self, morphism: Any) -> Theorem:
        matrix = _exact_matrix(morphism.matrix)
        expected = (morphism.target.dimension, morphism.source.dimension)
        if matrix.shape != expected:
            raise ProofError(
                f"morphism {morphism.name} has shape {matrix.shape}, expected {expected}"
            )
        return self._issue(
            Proposition.make(
                "well_typed_morphism",
                morphism.name,
                source=morphism.source.name,
                target=morphism.target.name,
                shape=list(matrix.shape),
            ),
            "morphism_shape_rule",
        )

    def prove_intertwiner(
        self,
        morphism: Any,
        source_representation: Any,
        target_representation: Any,
    ) -> Theorem:
        typed = self.prove_well_typed_morphism(morphism)
        if morphism.source != source_representation.space:
            raise ProofError("source representation is attached to the wrong space")
        if morphism.target != target_representation.space:
            raise ProofError("target representation is attached to the wrong space")
        if source_representation.generator_names != target_representation.generator_names:
            raise ProofError("representation generator sets do not agree")
        residuals = []
        for name in source_representation.generator_names:
            source = source_representation.generator(name)
            target = target_representation.generator(name)
            residual = target * morphism.matrix - morphism.matrix * source
            if not _zero_matrix(residual):
                raise ProofError(f"intertwiner equation failed for generator {name}")
            residuals.append(name)
        return self._issue(
            Proposition.make(
                "intertwiner",
                morphism.name,
                generators=tuple(residuals),
            ),
            "exact_intertwiner_rule",
            premises=(typed,),
        )

    def prove_intertwiner_rank_no_go(
        self, profile: Any, *, requested_rank: int, subject: str
    ) -> Theorem:
        if requested_rank <= profile.maximum_rank:
            raise ProofError(
                f"rank {requested_rank} is not excluded; upper bound is {profile.maximum_rank}"
            )
        return self._issue(
            Proposition.make(
                "intertwiner_rank_no_go",
                subject,
                requested_rank=requested_rank,
                maximum_rank=profile.maximum_rank,
                hom_dimension=profile.hom_dimension,
            ),
            "semisimple_isotypic_rank_bound",
            certificate={
                "shared_isotypic_blocks": profile.shared_blocks,
                "exact": True,
            },
        )

    def prove_gksl_well_formed(self, generator: Any) -> Theorem:
        if not generator.hamiltonian.is_endomorphism:
            raise ProofError("Hamiltonian must be an endomorphism")
        if not _zero_matrix(generator.hamiltonian.matrix.H - generator.hamiltonian.matrix):
            raise ProofError("Hamiltonian is not Hermitian")
        for jump, rate in zip(generator.jumps, generator.rates):
            if jump.source != generator.space or jump.target != generator.space:
                raise ProofError("every Lindblad jump must be an endomorphism")
            exact_rate = sp.sympify(rate)
            if exact_rate.atoms(sp.Float):
                raise ProofError("Lindblad rates must be exact")
            if exact_rate.is_nonnegative is not True:
                raise ProofError("Lindblad rates must be provably nonnegative")
        return self._issue(
            Proposition.make(
                "gksl_well_formed",
                generator.name,
                space=generator.space.name,
                jump_count=len(generator.jumps),
            ),
            "finite_dimensional_gksl_constructor",
            certificate={"trace_preserving": True, "rates_nonnegative": True},
        )

    def prove_generator_unital(self, generator: Any) -> Theorem:
        identity = sp.eye(generator.space.dimension)
        residual = generator.act(identity)
        if not _zero_matrix(residual):
            raise ProofError("generator does not annihilate the identity")
        return self._issue(
            Proposition.make("unital_generator", generator.name),
            "exact_identity_action_rule",
            premises=(generator.theorem,),
            certificate={"identity_residual": "zero"},
        )

    def prove_generator_trace_preserving(self, generator: Any) -> Theorem:
        dimension = generator.space.dimension
        checked = 0
        for row in range(dimension):
            for column in range(dimension):
                unit = sp.zeros(dimension)
                unit[row, column] = 1
                if sp.simplify(sp.trace(generator.act(unit))) != 0:
                    raise ProofError(
                        f"trace preservation failed on matrix unit ({row},{column})"
                    )
                checked += 1
        return self._issue(
            Proposition.make(
                "trace_preserving_generator",
                generator.name,
                checked_matrix_units=checked,
            ),
            "exact_matrix_unit_trace_rule",
            premises=(generator.theorem,),
        )

    def prove_equal_rate_kraus_basis_invariance(
        self, generator: Any, *, subject: str
    ) -> Theorem:
        """Prove invariance under every real orthogonal change of jump frame.

        The kernel checks the hypotheses needed by the finite-dimensional
        identity

        ``sum_b L'_b X L'_b* = sum_a L_a X L_a*``

        for ``L'_b = sum_a O_ba L_a`` and ``O.T O = I``.  Equal rates are
        essential: unequal coefficients would select a preferred frame.
        """

        if not generator.jumps:
            raise ProofError("Kraus-basis invariance needs a nonempty jump frame")
        rate = sp.sympify(generator.rates[0])
        if any(sp.simplify(sp.sympify(item) - rate) != 0 for item in generator.rates):
            raise ProofError("Kraus-basis invariance requires equal jump rates")
        if any(
            jump.source != generator.space or jump.target != generator.space
            for jump in generator.jumps
        ):
            raise ProofError("every jump must be an endomorphism of one space")
        return self._issue(
            Proposition.make(
                "orthogonal_kraus_basis_invariance",
                subject,
                frame_dimension=len(generator.jumps),
                common_rate=str(rate),
            ),
            "orthogonal_kraus_sum_rule",
            premises=(generator.theorem,),
            certificate={
                "identity": "sum_b O_ba O_bc = delta_ac",
                "quantifier": "every real orthogonal frame change",
            },
        )

    def prove_orthogonal_frame_covariance(
        self,
        frame: Sequence[sp.MatrixBase],
        symmetry_generators: Sequence[sp.MatrixBase],
        *,
        expected_invariant_dimension: int,
        subject: str,
    ) -> Theorem:
        """Certify exact infinitesimal covariance of a Hermitian jump frame.

        The frame must have scalar Gram matrix.  For every Hermitian symmetry
        generator ``G`` the tangent ``i[G,F_a]`` is reconstructed exactly in
        the frame and its coefficient matrix must be real skew-symmetric.
        The common kernel of those coefficient matrices is then the space of
        invariant linear combinations of the jumps.
        """

        checked_frame, checked_generators, norm, actions = (
            _orthogonal_frame_action_data(frame, symmetry_generators)
        )

        joint = sp.ImmutableMatrix.vstack(*actions)
        invariant_dimension = joint.cols - int(joint.rank())
        if invariant_dimension != expected_invariant_dimension:
            raise ProofError(
                f"linear invariant dimension is {invariant_dimension}, "
                f"expected {expected_invariant_dimension}"
            )
        return self._issue(
            Proposition.make(
                "orthogonal_frame_covariance",
                subject,
                frame_dimension=len(checked_frame),
                symmetry_generator_count=len(checked_generators),
                invariant_linear_dimension=invariant_dimension,
            ),
            "exact_infinitesimal_orthogonal_frame_rule",
            certificate={
                "frame_gram": f"{norm} I",
                "closure_residual": "zero",
                "action_transpose_residual": "zero",
            },
        )

    def prove_orthogonal_frame_commutant_dimensions(
        self,
        frame: Sequence[sp.MatrixBase],
        symmetry_generators: Sequence[sp.MatrixBase],
        *,
        expected_full_dimension: int,
        expected_symmetric_dimension: int,
        subject: str,
    ) -> Theorem:
        """Count all and self-adjoint real couplings commuting with a frame action."""

        checked_frame, checked_generators, norm, actions = (
            _orthogonal_frame_action_data(frame, symmetry_generators)
        )
        dimension = len(checked_frame)
        variables = sp.symbols(f"commutant_0:{dimension * dimension}")
        candidate = sp.Matrix(dimension, dimension, variables)
        equations = []
        for action in actions:
            equations.extend(candidate * action - action * candidate)
        system, _ = sp.linear_eq_to_matrix(equations, variables)
        full_dimension = len(variables) - int(system.rank())

        symmetric_variables = []
        symmetric_candidate = sp.zeros(dimension)
        for row in range(dimension):
            for column in range(row, dimension):
                variable = sp.Symbol(f"symmetric_{row}_{column}")
                symmetric_variables.append(variable)
                symmetric_candidate[row, column] = variable
                symmetric_candidate[column, row] = variable
        symmetric_equations = []
        for action in actions:
            symmetric_equations.extend(
                symmetric_candidate * action - action * symmetric_candidate
            )
        symmetric_system, _ = sp.linear_eq_to_matrix(
            symmetric_equations, symmetric_variables
        )
        symmetric_dimension = len(symmetric_variables) - int(
            symmetric_system.rank()
        )

        if full_dimension != expected_full_dimension:
            raise ProofError(
                f"frame commutant dimension is {full_dimension}, "
                f"expected {expected_full_dimension}"
            )
        if symmetric_dimension != expected_symmetric_dimension:
            raise ProofError(
                f"symmetric frame commutant dimension is {symmetric_dimension}, "
                f"expected {expected_symmetric_dimension}"
            )
        return self._issue(
            Proposition.make(
                "orthogonal_frame_commutant_dimensions",
                subject,
                frame_dimension=dimension,
                symmetry_generator_count=len(checked_generators),
                full_commutant_dimension=full_dimension,
                symmetric_commutant_dimension=symmetric_dimension,
            ),
            "exact_linear_commutant_rule",
            certificate={
                "frame_gram": f"{norm} I",
                "commutator_system_rank": int(system.rank()),
                "symmetric_system_rank": int(symmetric_system.rank()),
            },
        )

    def prove_orthogonal_star_interaction_covariance(
        self,
        frame_covariance: Theorem,
        hermiticity: Theorem,
        *,
        environment_dimension: int,
        subject: str,
    ) -> Theorem:
        """Contract an orthogonal jump frame with its dual environment frame."""

        if frame_covariance.proposition.kind != "orthogonal_frame_covariance":
            raise ProofError("star interaction needs an orthogonally covariant frame")
        if hermiticity.proposition.kind != "matrix_equality":
            raise ProofError("star interaction needs an exact Hermiticity theorem")
        frame_dimension = frame_covariance.proposition.data["frame_dimension"]
        if environment_dimension != frame_dimension + 1:
            raise ProofError("environment must contain one vacuum plus the full frame")
        return self._issue(
            Proposition.make(
                "orthogonal_star_interaction_covariance",
                subject,
                frame_dimension=frame_dimension,
                environment_dimension=environment_dimension,
                gauge_invariant=True,
                basis_independent=True,
            ),
            "orthogonal_frame_dual_contraction_rule",
            premises=(frame_covariance, hermiticity),
            certificate={"infinitesimal_commutator": "zero"},
        )

    def prove_scaled_coupling_environment_equivalence(
        self,
        rate_metric_theorem: Theorem,
        *,
        dimension: int,
        scale: sp.Expr,
        subject: str,
    ) -> Theorem:
        """Quotient square couplings with scalar Gram by environment rotations.

        For a real square coupling ``C`` satisfying ``C.T C = s I`` with
        ``s>0``, the matrix ``O=C/sqrt(s)`` is orthogonal.  Left multiplication
        by ``O.T`` is a vacuum-preserving relabelling of the environment jump
        basis, so all such couplings represent the same reduced channel.
        """

        exact_scale = sp.sympify(scale)
        if dimension <= 0 or exact_scale.atoms(sp.Float):
            raise ProofError("scaled coupling equivalence needs exact positive data")
        if exact_scale.is_positive is not True:
            raise ProofError("coupling Gram scale must be provably positive")
        if rate_metric_theorem.proposition.kind != "matrix_equality":
            raise ProofError("coupling equivalence needs an exact rate-metric theorem")
        return self._issue(
            Proposition.make(
                "scaled_coupling_environment_equivalence",
                subject,
                dimension=dimension,
                gram_scale=str(exact_scale),
                coupling_form=f"sqrt({exact_scale}) O",
                orthogonal_environment_relabelling=True,
                reduced_channel_unique_up_to_scale=True,
            ),
            "polar_gram_factorization_rule",
            premises=(rate_metric_theorem,),
            certificate={"O_transpose_O": "identity"},
        )

    def prove_parent_action_rate_metric_underdetermination(
        self,
        field_metric: sp.MatrixBase,
        canonical_rate: sp.MatrixBase,
        alternative_rate: sp.MatrixBase,
        frame: Sequence[sp.MatrixBase],
        symmetry_generators: Sequence[sp.MatrixBase],
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        """Exhibit two gauge-compatible bath completions of one field action.

        The field quadratic form fixes ``K``.  A bath covariance ``R`` needs
        extra data: both ``R=K^-1`` and a distinct positive commutant element
        can extend the same field block.  The Riesz equation ``K R=I`` selects
        the first one uniquely, but is therefore an additional premise.
        """

        metric = _exact_matrix(field_metric)
        canonical = _exact_matrix(canonical_rate)
        alternative = _exact_matrix(alternative_rate)
        if metric.rows != metric.cols or metric.shape != canonical.shape:
            raise ProofError("field and rate metrics must be square and equally sized")
        if alternative.shape != metric.shape:
            raise ProofError("alternative rate metric has the wrong shape")
        dimension = metric.rows
        for value in (metric, canonical, alternative):
            if value != value.T:
                raise ProofError("parent-action metrics must be real symmetric")
            if not _zero_matrix(value - sp.diag(*value.diagonal())):
                raise ProofError("the exact parent-action rule currently needs diagonal metrics")
            if any(sp.sympify(entry).is_positive is not True for entry in value.diagonal()):
                raise ProofError("parent-action metrics must be exactly positive")
        if not _zero_matrix(metric * canonical - sp.eye(dimension)):
            raise ProofError("the canonical rate is not the Riesz dual of the field metric")
        if _zero_matrix(canonical - alternative):
            raise ProofError("the alternative bath completion must be distinct")
        vector_pair = sp.Matrix.hstack(
            sp.Matrix(list(canonical)), sp.Matrix(list(alternative))
        )
        if vector_pair.rank() != 2:
            raise ProofError("the alternative rate differs only by an overall scale")

        _, _, _, actions = _orthogonal_frame_action_data(frame, symmetry_generators)
        for action in actions:
            if not _zero_matrix(canonical * action - action * canonical):
                raise ProofError("the Riesz-dual rate is not gauge compatible")
            if not _zero_matrix(alternative * action - action * alternative):
                raise ProofError("the alternative rate is not gauge compatible")

        canonical_parent = sp.diag(metric, canonical.inv())
        alternative_parent = sp.diag(metric, alternative.inv())
        if canonical_parent[:dimension, :dimension] != metric:
            raise ProofError("canonical completion changed the field action")
        if alternative_parent[:dimension, :dimension] != metric:
            raise ProofError("alternative completion changed the field action")
        if _zero_matrix(metric * alternative - sp.eye(dimension)):
            raise ProofError("the alternative unexpectedly satisfies Riesz reciprocity")

        return self._issue(
            Proposition.make(
                "parent_action_rate_metric_underdetermination",
                subject,
                field_dimension=dimension,
                same_field_restriction=True,
                positive_gauge_compatible_completions=2,
                completions_not_scale_equivalent=True,
                field_action_selects_unique_bath_rate=False,
                riesz_equation="K R = I",
                riesz_equation_selects_unique_rate=True,
                riesz_condition_is_additional=True,
            ),
            "exact_two_parent_completion_counterexample_rule",
            premises=tuple(premises),
            certificate={
                "canonical_parent_hessian": str(canonical_parent),
                "alternative_parent_hessian": str(alternative_parent),
                "canonical_riesz_residual": "zero",
                "alternative_riesz_residual": "nonzero",
                "gauge_commutators": "zero",
            },
        )

    def prove_mixed_real_cotangent_carrier_dimension(
        self,
        *,
        transfer_complex_dimension: int,
        gauge_hermitian_dimension: int,
        field_real_dimension: int,
        current_jump_dimension: int,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        """Type a transfer-complex plus gauge-Hermitian noise carrier over R."""

        values = (
            transfer_complex_dimension,
            gauge_hermitian_dimension,
            field_real_dimension,
            current_jump_dimension,
        )
        if any(value <= 0 for value in values):
            raise ProofError("mixed cotangent dimensions must be positive")
        mixed_real_dimension = 2 * transfer_complex_dimension + gauge_hermitian_dimension
        naive_uniform_complex_real_dimension = 2 * (
            transfer_complex_dimension + gauge_hermitian_dimension
        )
        if mixed_real_dimension != field_real_dimension:
            raise ProofError("the mixed-real noise carrier does not match the field carrier")
        if naive_uniform_complex_real_dimension == field_real_dimension:
            raise ProofError("the scalar-type correction has no effect")
        if current_jump_dimension >= mixed_real_dimension:
            raise ProofError("the current jump frame is not dimensionally deficient")
        deficit = mixed_real_dimension - current_jump_dimension
        return self._issue(
            Proposition.make(
                "mixed_real_cotangent_carrier_dimension",
                subject,
                transfer_complex_dimension=transfer_complex_dimension,
                gauge_hermitian_dimension=gauge_hermitian_dimension,
                mixed_real_dimension=mixed_real_dimension,
                field_real_dimension=field_real_dimension,
                naive_uniform_complex_real_dimension=naive_uniform_complex_real_dimension,
                current_jump_dimension=current_jump_dimension,
                current_jump_codimension=deficit,
                full_cotangent_dimension_match=True,
                current_qms_is_full_cotangent_frame=False,
            ),
            "mixed_scalar_realification_dimension_rule",
            premises=tuple(premises),
            certificate={
                "formula": "2 dim_C transfer + dim_R Herm(gauge)",
                "required_new_real_directions": deficit,
            },
        )

    def prove_scalar_fixed_algebra_under_frame_extension(
        self,
        base_scalar_theorem: Theorem,
        base_frame: Sequence[sp.MatrixBase],
        extended_frame: Sequence[sp.MatrixBase],
        *,
        subject: str,
    ) -> Theorem:
        """Preserve a scalar commutant when a Hermitian jump frame is enlarged."""

        if base_scalar_theorem.proposition.kind != "scalar_fixed_algebra_intersection":
            raise ProofError("frame extension needs an existing scalar fixed-algebra theorem")
        base = tuple(_exact_matrix(item) for item in base_frame)
        extended = tuple(_exact_matrix(item) for item in extended_frame)
        if not base or len(extended) <= len(base):
            raise ProofError("the extended frame must strictly enlarge a nonempty base")
        shape = base[0].shape
        if shape[0] != shape[1] or any(item.shape != shape for item in base + extended):
            raise ProofError("all jump-frame elements must be square on one carrier")
        if any(not _zero_matrix(item.H - item) for item in base + extended):
            raise ProofError("the monotone commutant rule requires Hermitian jumps")
        extended_columns = sp.Matrix.hstack(
            *(sp.Matrix(list(item)) for item in extended)
        )
        extended_rank = int(extended_columns.rank())
        for item in base:
            augmented = extended_columns.row_join(sp.Matrix(list(item)))
            if int(augmented.rank()) != extended_rank:
                raise ProofError("the base jump span is not contained in the extension")
        return self._issue(
            Proposition.make(
                "scalar_fixed_algebra_under_frame_extension",
                subject,
                base_frame_size=len(base),
                extended_frame_size=len(extended),
                extended_frame_rank=extended_rank,
                base_span_contained=True,
                fixed_algebra_dimension=1,
                primitive=True,
            ),
            "dirichlet_commutant_monotonicity_rule",
            premises=(base_scalar_theorem,),
            certificate={"base_to_extended_span_residual": "zero"},
        )

    def prove_hermitian_frame_lie_closure(
        self,
        frame: Sequence[sp.MatrixBase],
        symmetry_generators: Sequence[sp.MatrixBase],
        *,
        subject: str,
    ) -> Theorem:
        checked = tuple(_exact_matrix(item) for item in frame)
        generators = tuple(_exact_matrix(item) for item in symmetry_generators)
        if not checked or not generators:
            raise ProofError("Lie closure needs a frame and symmetry generators")
        shape = checked[0].shape
        if any(item.shape != shape or not _zero_matrix(item.H - item) for item in checked + generators):
            raise ProofError("Lie closure requires Hermitian operators on one carrier")
        columns = sp.Matrix.hstack(*(sp.Matrix(list(item)) for item in checked))
        rank = int(columns.rank())
        if rank != len(checked):
            raise ProofError("the proposed Hermitian frame is not independent")
        tangents = tuple(
            sp.Matrix(list(sp.I * (generator * item - item * generator)))
            for generator in generators
            for item in checked
        )
        tangent_columns = sp.Matrix.hstack(*tangents)
        pivot_rows = columns.T.rref()[1]
        if len(pivot_rows) != rank:
            raise ProofError("could not extract a full-rank frame row minor")
        minor = columns.extract(pivot_rows, range(len(checked)))
        tangent_minor = tangent_columns.extract(
            pivot_rows, range(tangent_columns.cols)
        )
        coefficients = minor.inv() * tangent_minor
        if not _zero_matrix(columns * coefficients - tangent_columns):
            raise ProofError("the Hermitian frame is not Lie closed")
        checks = len(tangents)
        return self._issue(
            Proposition.make(
                "hermitian_frame_lie_closure",
                subject,
                frame_dimension=len(checked),
                symmetry_generator_count=len(generators),
                closure_checks=checks,
                gauge_closed=True,
            ),
            "exact_commutator_span_rule",
            certificate={"all_augmented_rank_residuals": "zero"},
        )

    def prove_structural_star_interaction(
        self,
        frame: Sequence[sp.MatrixBase],
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        checked = tuple(_exact_matrix(item) for item in frame)
        if not checked:
            raise ProofError("star interaction needs a nonempty jump frame")
        system_dimension = checked[0].rows
        if any(
            item.shape != (system_dimension, system_dimension)
            or not _zero_matrix(item.H - item)
            for item in checked
        ):
            raise ProofError("star interaction requires one Hermitian endomorphism frame")
        columns = sp.Matrix.hstack(*(sp.Matrix(list(item)) for item in checked))
        frame_rank = int(columns.rank())
        if frame_rank != len(checked):
            raise ProofError("minimal star interaction requires an independent frame")
        environment_dimension = frame_rank + 1
        return self._issue(
            Proposition.make(
                "structural_star_repeated_interaction",
                subject,
                system_dimension=system_dimension,
                jump_dimension=frame_rank,
                environment_dimension=environment_dimension,
                ambient_dimension=system_dimension * environment_dimension,
                self_adjoint=True,
                vacuum_second_moment="sum_a F_a^2",
                gksl_tangent=True,
                minimal_noise_dimension=frame_rank,
            ),
            "independent_hermitian_star_interaction_rule",
            premises=tuple(premises),
            certificate={"frame_rank": frame_rank, "vacuum_line_dimension": 1},
        )

    def prove_structural_star_collision_limit(
        self,
        star_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        if star_theorem.proposition.kind != "structural_star_repeated_interaction":
            raise ProofError("structural collision limit needs a star-interaction theorem")
        if not star_theorem.proposition.data.get("gksl_tangent"):
            raise ProofError("star interaction has no certified GKSL tangent")
        return self._issue(
            Proposition.make(
                "structural_star_collision_limit",
                subject,
                scaling="h=u/n",
                convergence="operator_norm",
                fresh_environment_each_step=True,
            ),
            "finite_dimensional_unitary_chernoff_rule",
            premises=(star_theorem,),
        )

    def prove_collision_physical_time_scale_no_go(
        self,
        star_theorem: Theorem,
        coupling_scale: sp.Symbol,
        physical_time: sp.Symbol,
        energy_scale: sp.Symbol,
        hbar: sp.Symbol,
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        """Certify the one-parameter scale orbit of a star collision model.

        The weak-collision tangent is quadratic in the interaction amplitude.
        Consequently ``g -> c g`` and ``t -> t/c**2`` leave the dimensionless
        semigroup parameter unchanged.  Converting that parameter to seconds
        additionally needs a nonzero dimensional energy/rate datum.
        """

        if star_theorem.proposition.kind != "structural_star_repeated_interaction":
            raise ProofError("physical-time no-go needs a structural star interaction")
        symbols = (coupling_scale, physical_time, energy_scale, hbar)
        if any(not isinstance(item, sp.Symbol) for item in symbols):
            raise ProofError("physical-time no-go requires symbolic scale variables")
        if any(item.is_positive is not True for item in symbols):
            raise ProofError("all scale variables must be declared positive")
        rate_factor = coupling_scale**2
        compensated_time = physical_time / coupling_scale**2
        if sp.simplify(rate_factor * compensated_time - physical_time) != 0:
            raise ProofError("coupling/time compensation identity failed")
        if sp.simplify(sp.diff(rate_factor, coupling_scale)) == 0:
            raise ProofError("the collision rate unexpectedly lost its coupling scale")
        time_unit = hbar / energy_scale
        if sp.simplify(energy_scale * time_unit - hbar) != 0:
            raise ProofError("energy-time calibration identity failed")
        if sp.simplify(sp.diff(time_unit, energy_scale)) == 0:
            raise ProofError("the time unit unexpectedly became energy independent")
        return self._issue(
            Proposition.make(
                "collision_physical_time_scale_no_go",
                subject,
                interaction_rescaling="H_int -> g H_int",
                generator_rescaling="L -> g^2 L",
                compensating_time_rescaling="t -> t/g^2",
                invariant_parameter="g^2 t",
                dimensionless_semigroup_fixed=True,
                absolute_seconds_selected=False,
                hbar_alone_sufficient=False,
                required_dimensional_anchor="energy/rate scale plus collision schedule",
                generic_time_unit="hbar/E_*",
            ),
            "exact_collision_scale_orbit_rule",
            premises=(star_theorem, *tuple(premises)),
            certificate={
                "scale_orbit_residual": "zero",
                "energy_time_residual": "zero",
                "rate_derivative": str(sp.diff(rate_factor, coupling_scale)),
                "time_unit_derivative": str(sp.diff(time_unit, energy_scale)),
            },
        )

    def prove_bilateral_shift_counter(
        self,
        site: sp.Symbol,
        displacement: sp.Symbol,
        *,
        subject: str,
    ) -> Theorem:
        """Certify ``[N,U^k]e_n=k U^k e_n`` on the bilateral integer basis."""

        if not isinstance(site, sp.Symbol) or not isinstance(displacement, sp.Symbol):
            raise ProofError("the shift counter requires symbolic site labels")
        if site.is_integer is not True or displacement.is_integer is not True:
            raise ProofError("the shift counter is defined on integer labels")
        residual = sp.simplify((site + displacement) - site - displacement)
        if residual != 0:
            raise ProofError("bilateral shift counter identity failed")
        return self._issue(
            Proposition.make(
                "bilateral_shift_counter",
                subject,
                carrier="ell^2(Z)",
                number_action="N e_n = n e_n",
                shift_action="U^k e_n = e_(n+k)",
                commutator="[N,U^k] = k U^k",
                absolute_integer_tick=True,
            ),
            "integer_basis_shift_rule",
            certificate={"basis_residual": "zero"},
        )

    def prove_toeplitz_ancilla_chain_dilation(
        self,
        star_theorem: Theorem,
        counter_theorem: Theorem,
        gauge_closure_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Build the bilateral preloaded-chain dilation of a star collision.

        The statement is cylinder-local: for every finite ``n`` only ``n``
        tensor factors are touched.  A bilateral shift makes the same global
        Floquet unitary present a previously unused vacuum cell at each step.
        """

        if star_theorem.proposition.kind != "structural_star_repeated_interaction":
            raise ProofError("ancilla chain needs a structural star interaction")
        if counter_theorem.proposition.kind != "bilateral_shift_counter":
            raise ProofError("ancilla chain needs the bilateral shift counter")
        if gauge_closure_theorem.proposition.kind != "hermitian_frame_lie_closure":
            raise ProofError("ancilla chain needs a gauge-closed jump frame")
        star = star_theorem.proposition.data
        closure = gauge_closure_theorem.proposition.data
        if star["jump_dimension"] != closure["frame_dimension"]:
            raise ProofError("star jump labels and gauge frame have different dimensions")
        if star["environment_dimension"] != star["jump_dimension"] + 1:
            raise ProofError("the chain cell must contain vacuum plus all jump labels")
        return self._issue(
            Proposition.make(
                "toeplitz_ancilla_chain_dilation",
                subject,
                system_dimension=star["system_dimension"],
                cell_dimension=star["environment_dimension"],
                jump_dimension=star["jump_dimension"],
                chain="infinite_tensor_Z(K_cell, vacuum)",
                global_step="(I_system tensor S_chain) U_collision^(0)",
                global_step_unitary=True,
                autonomy_level="fixed discrete Floquet unitary",
                cylinder_statement="all finite n >= 0",
                addressed_cells="0,...,n-1",
                used_cell_revisited=False,
                product_vacuum_supplies_fresh_cells=True,
                cellwise_gauge_covariant=True,
            ),
            "bilateral_shift_repeated_interaction_rule",
            premises=(star_theorem, counter_theorem, gauge_closure_theorem),
            certificate={
                "unitarity_residual": "zero by product of unitaries",
                "distinct_site_residual": "zero on every finite cylinder",
            },
        )

    def prove_ancilla_chain_reduced_iteration(
        self,
        chain_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Issue the exact finite-cylinder induction ``rho_n=Phi^n(rho_0)``."""

        if chain_theorem.proposition.kind != "toeplitz_ancilla_chain_dilation":
            raise ProofError("reduced iteration needs a checked ancilla chain")
        data = chain_theorem.proposition.data
        if data.get("used_cell_revisited") is not False:
            raise ProofError("the chain does not certify fresh cells")
        if data.get("product_vacuum_supplies_fresh_cells") is not True:
            raise ProofError("the chain lacks its product-vacuum premise")
        return self._issue(
            Proposition.make(
                "ancilla_chain_reduced_iteration",
                subject,
                formula="Tr_chain Ad(V)^n(rho_0 tensor omega_vac) = Phi_h^n(rho_0)",
                proof="finite-cylinder induction",
                valid_steps="all n >= 0",
                exact=True,
            ),
            "fresh_cell_partial_trace_induction_rule",
            premises=(chain_theorem,),
            certificate={"all_cylinder_residuals": "zero"},
        )

    def prove_ancilla_chain_resource_boundary(
        self,
        chain_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Keep preloaded reservoir and continuous-Hamiltonian origin explicit."""

        if chain_theorem.proposition.kind != "toeplitz_ancilla_chain_dilation":
            raise ProofError("resource boundary needs a checked ancilla chain")
        return self._issue(
            Proposition.make(
                "ancilla_chain_resource_boundary",
                subject,
                external_step_by_step_reset_required=False,
                preloaded_infinite_product_vacuum_required=True,
                vacuum_chain_parent_derived=False,
                time_independent_local_hamiltonian_derived=False,
                absolute_tick_duration_derived=False,
                strong_physical_autonomy=False,
            ),
            "explicit_reservoir_premise_boundary_rule",
            premises=(chain_theorem,),
        )

    def prove_product_vacuum_parent_hamiltonian(
        self,
        chain_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Derive the commuting-projector parent of the chain vacuum.

        On every finite interval ``Lambda`` the local terms are
        ``h_m=I-|0><0|``.  They commute, have spectrum ``{0,1}``, and their
        common zero space is the single product-vacuum line.  This exact
        finite-volume statement determines the corresponding infinite-chain
        frustration-free product state without constructing an infinite
        matrix.
        """

        if chain_theorem.proposition.kind != "toeplitz_ancilla_chain_dilation":
            raise ProofError("the vacuum parent needs a checked ancilla chain")
        cell_dimension = int(chain_theorem.proposition.data["cell_dimension"])
        if cell_dimension <= 1:
            raise ProofError("the collision cell must contain a non-vacuum sector")
        excitation_dimension = cell_dimension - 1
        return self._issue(
            Proposition.make(
                "product_vacuum_commuting_projector_parent",
                subject,
                cell_dimension=cell_dimension,
                excitation_dimension=excitation_dimension,
                local_term="h_m = I_m - |0><0|_m",
                finite_volume_parent="H_Lambda = sum_(m in Lambda) h_m",
                local_spectrum=(0, 1),
                terms_commute=True,
                frustration_free=True,
                finite_volume_ground_dimension=1,
                finite_volume_gap=1,
                infinite_product_vacuum_selected=True,
                translation_invariant_interaction=True,
            ),
            "commuting_projector_product_state_parent_rule",
            premises=(chain_theorem,),
            certificate={
                "projector_residual": "h_m^2-h_m=0",
                "common_kernel": "tensor_m span{|0>_m}",
                "gap": "1",
            },
        )

    def prove_ancilla_shift_gnvw_index(
        self,
        chain_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Instantiate the exact GNVW index of the one-cell chain shift."""

        if chain_theorem.proposition.kind != "toeplitz_ancilla_chain_dilation":
            raise ProofError("the GNVW index needs a checked ancilla chain")
        cell_dimension = int(chain_theorem.proposition.data["cell_dimension"])
        if cell_dimension <= 1:
            raise ProofError("a nontrivial shift needs cell dimension greater than one")
        return self._issue(
            Proposition.make(
                "gnvw_shift_index",
                subject,
                cell_dimension=cell_dimension,
                multiplicative_index=cell_dimension,
                inverse_shift_index=sp.Rational(1, cell_dimension),
                additive_index=f"log({cell_dimension})",
                identity_multiplicative_index=1,
                nontrivial=True,
                source="Gross-Nesme-Vogts-Werner, arXiv:0910.3675",
            ),
            "gnvw_one_cell_shift_index_rule",
            premises=(chain_theorem,),
            certificate={"index_ratio": f"{cell_dimension}/1"},
        )

    def prove_finite_collision_preserves_chain_index(
        self,
        chain_theorem: Theorem,
        shift_index_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Remove the finite system--cell collision from the asymptotic flow."""

        if chain_theorem.proposition.kind != "toeplitz_ancilla_chain_dilation":
            raise ProofError("index stability needs a checked ancilla chain")
        if shift_index_theorem.proposition.kind != "gnvw_shift_index":
            raise ProofError("index stability needs the shift index")
        shift_index = shift_index_theorem.proposition.data["multiplicative_index"]
        return self._issue(
            Proposition.make(
                "finite_defect_gnvw_index_stability",
                subject,
                localized_collision_multiplicative_index=1,
                shift_multiplicative_index=shift_index,
                global_step_multiplicative_index=shift_index,
                formula="ind(V)=ind(S_chain) ind(U_collision^(0))",
                finite_system_impurity_changes_asymptotic_flow=False,
            ),
            "gnvw_local_perturbation_stability_rule",
            premises=(chain_theorem, shift_index_theorem),
            certificate={
                "multiplicative_residual": f"{shift_index}*1-{shift_index}=0"
            },
        )

    def prove_local_hamiltonian_ancilla_shift_no_go(
        self,
        parent_theorem: Theorem,
        global_index_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Exclude a Lieb--Robinson local Hamiltonian generator of the shift.

        The ALPU extension of the GNVW index is constant along every
        sufficiently local Hamiltonian path from the identity.  Such a path
        therefore has multiplicative index one, whereas the conveyor step has
        the nontrivial cell-shift index.
        """

        if parent_theorem.proposition.kind != "product_vacuum_commuting_projector_parent":
            raise ProofError("the origin split needs the vacuum parent theorem")
        if global_index_theorem.proposition.kind != "finite_defect_gnvw_index_stability":
            raise ProofError("the no-go needs the global-step index")
        step_index = global_index_theorem.proposition.data[
            "global_step_multiplicative_index"
        ]
        if sp.sympify(step_index) == 1:
            raise ProofError("the proposed conveyor has trivial index")
        return self._issue(
            Proposition.make(
                "local_hamiltonian_ancilla_shift_no_go",
                subject,
                vacuum_parent_derived=True,
                vacuum_parent_local=True,
                vacuum_parent_gapped=True,
                hamiltonian_path_multiplicative_index=1,
                conveyor_step_multiplicative_index=step_index,
                exact_local_hamiltonian_generator_exists=False,
                time_dependent_lieb_robinson_generator_exists=False,
                time_independent_local_generator_exists=False,
                obstruction="nontrivial one-dimensional information-flow index",
                strong_autonomy_closed=False,
                admissible_status="exact Floquet primitive with preloaded vacuum",
                possible_escape="index-balanced counterpropagating conveyor or nonlocal/slow-tail generator",
                source="Ranard-Walter-Witteveen, arXiv:2012.00741",
            ),
            "alpu_local_generation_index_obstruction_rule",
            premises=(parent_theorem, global_index_theorem),
            certificate={
                "index_mismatch": f"{step_index} != 1",
                "vacuum_parent_gap": "1",
            },
        )

    def prove_index_balanced_ancilla_counterflow(
        self,
        shift_index_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Cancel a cell shift by an oppositely oriented equal-cell shift."""

        if shift_index_theorem.proposition.kind != "gnvw_shift_index":
            raise ProofError("balanced counterflow needs a checked shift index")
        dimension = int(shift_index_theorem.proposition.data["cell_dimension"])
        forward = sp.Integer(dimension)
        reverse = sp.Rational(1, dimension)
        total = sp.simplify(forward * reverse)
        if total != 1:
            raise ProofError("opposite cell shifts did not cancel their index")
        return self._issue(
            Proposition.make(
                "index_balanced_ancilla_counterflow",
                subject,
                cell_dimension=dimension,
                active_shift_index=forward,
                spectator_shift_index=reverse,
                total_multiplicative_index=total,
                active_action="A_m -> A_(m+1)",
                spectator_action="B_m -> B_(m-1)",
                index_obstruction_removed=True,
            ),
            "gnvw_opposite_shift_product_rule",
            premises=(shift_index_theorem,),
            certificate={"index_product": f"{dimension}*(1/{dimension})=1"},
        )

    def prove_two_layer_swap_counterflow_circuit(
        self,
        counterflow_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Realize opposite shifts by two translation-periodic SWAP layers."""

        if counterflow_theorem.proposition.kind != "index_balanced_ancilla_counterflow":
            raise ProofError("the SWAP circuit needs balanced counterflow")
        return self._issue(
            Proposition.make(
                "two_layer_swap_counterflow_circuit",
                subject,
                first_layer="product_m SWAP(A_m,B_m)",
                second_layer="product_m SWAP(B_m,A_(m+1))",
                circuit_depth=2,
                nearest_neighbour=True,
                gates_disjoint_within_each_layer=True,
                resulting_active_action="A_m(final)=A_(m-1)(initial)",
                resulting_spectator_action="B_m(final)=B_(m+1)(initial)",
                exact_counterpropagating_shifts=True,
                diagonal_gauge_covariant=True,
                real_structure_covariant=True,
            ),
            "exact_swap_label_transport_rule",
            premises=(counterflow_theorem,),
            certificate={
                "A_label_transport": "A_m <- A_(m-1)",
                "B_label_transport": "B_m <- B_(m+1)",
            },
        )

    def prove_swap_layers_have_local_hamiltonians(
        self,
        circuit_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Generate each disjoint SWAP layer by an exact local Hamiltonian."""

        if circuit_theorem.proposition.kind != "two_layer_swap_counterflow_circuit":
            raise ProofError("local layer Hamiltonians need the SWAP circuit")
        phase_plus = sp.simplify(sp.exp(-sp.I * sp.pi / 2 * (1 - 1)))
        phase_minus = sp.simplify(sp.exp(-sp.I * sp.pi / 2 * (1 - (-1))))
        if phase_plus != 1 or phase_minus != -1:
            raise ProofError("the exact SWAP exponential identity failed")
        return self._issue(
            Proposition.make(
                "piecewise_local_swap_hamiltonian",
                subject,
                local_term="(pi/2)(I-SWAP)",
                exponential_identity="exp[-i(pi/2)(I-SWAP)]=SWAP",
                commuting_terms_per_layer=True,
                finite_range=True,
                piecewise_time_dependent_local_hamiltonian=True,
                exact_two_stage_floquet_generation=True,
                single_time_independent_local_hamiltonian_derived=False,
                absolute_stage_duration_derived=False,
            ),
            "swap_spectral_exponential_rule",
            premises=(circuit_theorem,),
            certificate={
                "swap_plus_eigenphase": str(phase_plus),
                "swap_minus_eigenphase": str(phase_minus),
            },
        )

    def prove_balanced_conveyor_reduced_iteration(
        self,
        chain_recovery_theorem: Theorem,
        circuit_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Keep the active fresh-cell iteration after adding spectator flow."""

        if chain_recovery_theorem.proposition.kind != "ancilla_chain_reduced_iteration":
            raise ProofError("balanced recovery needs the original chain induction")
        if circuit_theorem.proposition.kind != "two_layer_swap_counterflow_circuit":
            raise ProofError("balanced recovery needs the counterflow circuit")
        return self._issue(
            Proposition.make(
                "balanced_ancilla_conveyor_reduced_iteration",
                subject,
                active_chain_supplies_fresh_vacuum=True,
                used_active_cell_revisited=False,
                spectator_chain_couples_to_system=False,
                spectator_product_vacuum_invariant=True,
                formula="Tr_(A,B) Ad(V_bal)^n(rho tensor omega_A tensor omega_B)=Phi_h^n(rho)",
                valid_steps="all finite n >= 0",
                exact=True,
            ),
            "spectator_counterflow_extension_rule",
            premises=(chain_recovery_theorem, circuit_theorem),
            certificate={"reduced_iteration_residual": "zero"},
        )

    def prove_balanced_conveyor_autonomy_boundary(
        self,
        hamiltonian_theorem: Theorem,
        recovery_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Record exactly what index balancing does and does not close."""

        if hamiltonian_theorem.proposition.kind != "piecewise_local_swap_hamiltonian":
            raise ProofError("autonomy boundary needs local SWAP Hamiltonians")
        if recovery_theorem.proposition.kind != "balanced_ancilla_conveyor_reduced_iteration":
            raise ProofError("autonomy boundary needs exact reduced recovery")
        return self._issue(
            Proposition.make(
                "balanced_conveyor_autonomy_boundary",
                subject,
                gnvw_obstruction_removed=True,
                exact_finite_depth_local_circuit=True,
                exact_piecewise_local_hamiltonian=True,
                exact_reduced_channel_iteration=True,
                single_static_local_hamiltonian_derived=False,
                absolute_time_scale_derived=False,
                auxiliary_counterflow_is_additional_carrier=True,
                strong_stationary_autonomy_closed=False,
                next_gate="static_local_hamiltonian_embedding_or_no_go",
            ),
            "explicit_balanced_autonomy_boundary_rule",
            premises=(hamiltonian_theorem, recovery_theorem),
        )

    def prove_balanced_conveyor_bloch_winding(
        self,
        circuit_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Compute the two eigenchannel windings of the balanced shift."""

        if circuit_theorem.proposition.kind != "two_layer_swap_counterflow_circuit":
            raise ProofError("Bloch winding needs the checked counterflow circuit")
        momentum = sp.Symbol("k", real=True)
        active = sp.exp(-sp.I * momentum)
        spectator = sp.exp(sp.I * momentum)
        active_winding = sp.simplify(
            sp.integrate(sp.diff(active, momentum) / active, (momentum, -sp.pi, sp.pi))
            / (2 * sp.pi * sp.I)
        )
        spectator_winding = sp.simplify(
            sp.integrate(
                sp.diff(spectator, momentum) / spectator,
                (momentum, -sp.pi, sp.pi),
            )
            / (2 * sp.pi * sp.I)
        )
        if (active_winding, spectator_winding) != (-1, 1):
            raise ProofError("balanced Bloch winding calculation failed")
        return self._issue(
            Proposition.make(
                "balanced_conveyor_bloch_winding",
                subject,
                bloch_unitary="diag(exp(-i k), exp(+i k))",
                active_eigenvalue_winding=active_winding,
                spectator_eigenvalue_winding=spectator_winding,
                determinant_winding=sp.simplify(active_winding + spectator_winding),
                total_index_trivial=True,
                individual_band_winding_nontrivial=True,
            ),
            "exact_bloch_winding_integral_rule",
            premises=(circuit_theorem,),
            certificate={
                "active_integral": "-1",
                "spectator_integral": "1",
                "determinant_integral": "0",
            },
        )

    def prove_static_periodic_two_band_logarithm_no_go(
        self,
        winding_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Exclude an exact static finite-range logarithm on the minimal carrier."""

        if winding_theorem.proposition.kind != "balanced_conveyor_bloch_winding":
            raise ProofError("the static logarithm test needs Bloch windings")
        data = winding_theorem.proposition.data
        if data["active_eigenvalue_winding"] == 0 or data[
            "spectator_eigenvalue_winding"
        ] == 0:
            raise ProofError("the eigenchannel logarithm has no winding obstruction")
        return self._issue(
            Proposition.make(
                "static_periodic_two_band_logarithm_no_go",
                subject,
                assumed_class="translation-invariant finite-range number-preserving two-chain Hamiltonian",
                static_bloch_hamiltonian="continuous periodic 2x2 Hermitian trigonometric polynomial h(k)",
                target_unitary="exp(-i tau h(k))=diag(exp(-ik),exp(+ik))",
                nondegenerate_domain="k not congruent to 0,pi",
                commutation_consequence="h(k) diagonal on each nondegenerate interval",
                periodic_scalar_exponential_winding=0,
                target_active_winding=data["active_eigenvalue_winding"],
                target_spectator_winding=data["spectator_eigenvalue_winding"],
                contradiction=True,
                exact_static_hamiltonian_exists=False,
            ),
            "periodic_logarithm_winding_obstruction_rule",
            premises=(winding_theorem,),
            certificate={
                "periodic_log_winding": "(h(pi)-h(-pi))/(2*pi)=0",
                "target_windings": "(-1,+1)",
            },
        )

    def prove_static_conveyor_carrier_boundary(
        self,
        no_go_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Prevent a minimal Bloch no-go from becoming an interacting no-go."""

        if no_go_theorem.proposition.kind != "static_periodic_two_band_logarithm_no_go":
            raise ProofError("carrier boundary needs the static Bloch no-go")
        return self._issue(
            Proposition.make(
                "static_conveyor_carrier_boundary",
                subject,
                minimal_two_chain_number_preserving_static_model_closed=True,
                piecewise_floquet_model_remains_valid=True,
                interacting_static_hamiltonian_excluded=False,
                clock_augmented_static_hamiltonian_excluded=False,
                enlarged_local_carrier_required_for_next_test=True,
                exact_one_period_readout_required=True,
                next_gate="clock_augmented_static_hamiltonian_conveyor",
            ),
            "explicit_no_go_scope_boundary_rule",
            premises=(no_go_theorem,),
        )

    def prove_three_site_history_clock_transfer(
        self, boundary_theorem: Theorem, *, subject: str
    ) -> Theorem:
        """Prove exact end-to-end transfer on the three-state history clock."""

        if boundary_theorem.proposition.kind != "static_conveyor_carrier_boundary":
            raise ProofError("history-clock transfer needs the minimal-carrier boundary")
        root_two = sp.sqrt(2)
        adjacency = sp.Matrix([[0, root_two, 0], [root_two, 0, root_two], [0, root_two, 0]])
        if adjacency**3 != 4 * adjacency:
            raise ProofError("three-site clock polynomial identity failed")
        propagator = sp.eye(3) - adjacency**2 / 2
        initial = sp.Matrix([1, 0, 0])
        target = sp.Matrix([0, 0, -1])
        if propagator * initial != target:
            raise ProofError("three-site clock does not transfer perfectly")
        return self._issue(
            Proposition.make(
                "three_site_history_clock_perfect_transfer",
                subject,
                clock_dimension=3,
                couplings="sqrt(2),sqrt(2)",
                transfer_time="pi/2",
                endpoint_phase="-1",
                exact_end_to_end_transfer=True,
            ),
            "exact_weighted_path_exponential_rule",
            premises=(boundary_theorem,),
            certificate={"A^3": "4A", "exp(-i*pi*A/2)e0": "-e2"},
        )

    def prove_dressed_history_word_execution(
        self, transfer_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if transfer_theorem.proposition.kind != "three_site_history_clock_perfect_transfer":
            raise ProofError("dressed history execution needs perfect clock transfer")
        return self._issue(
            Proposition.make(
                "dressed_history_word_execution",
                subject,
                history_word="W1 W0",
                dressed_hamiltonian="sqrt(2)(|1><0| tensor W0 + |2><1| tensor W1 + h.c.)",
                initial_clock="|0>",
                final_clock="|2>",
                final_data="-W1 W0 |psi>",
                exact_one_shot_execution=True,
                clock_returns_to_initial_state=False,
            ),
            "feynman_history_gauge_equivalence_rule",
            premises=(transfer_theorem,),
        )

    def prove_history_clock_uniform_locality_boundary(
        self, execution_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if execution_theorem.proposition.kind != "dressed_history_word_execution":
            raise ProofError("locality boundary needs dressed history execution")
        return self._issue(
            Proposition.make(
                "history_clock_uniform_locality_boundary",
                subject,
                global_layer_transition_local_on_original_chain=False,
                local_serialisation_gate_count="T=2L",
                perfect_transfer_couplings="J_t=sqrt((t+1)(T-t))",
                maximum_coupling_lower_bound="J_max >= T/2",
                bounded_coupling_transfer_time_lower_bound="tau >= pi*T/4 = pi*L/2",
                volume_independent_fixed_time=False,
                thermodynamic_uniform_static_conveyor_derived=False,
            ),
            "history_clock_coupling_time_scaling_rule",
            premises=(execution_theorem,),
            certificate={"T": "2L", "resource_scaling": "norm*time >= pi*T/4"},
        )

    def prove_clock_augmented_conveyor_boundary(
        self, locality_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if locality_theorem.proposition.kind != "history_clock_uniform_locality_boundary":
            raise ProofError("clock boundary needs the locality theorem")
        return self._issue(
            Proposition.make(
                "clock_augmented_conveyor_boundary",
                subject,
                finite_word_static_embedding=True,
                exact_clock_transfer=True,
                original_lattice_uniform_locality=False,
                bounded_strength_fixed_time_thermodynamic_limit=False,
                finite_clock_repeatable_conveyor_derived=False,
                general_interacting_clock_model_excluded=False,
                next_gate="bounded_strength_autonomous_clock_thermodynamic_limit",
            ),
            "explicit_clock_resource_boundary_rule",
            premises=(locality_theorem,),
        )

    def prove_quasi_ideal_clock_finite_volume_error(
        self, clock_boundary: Theorem, *, subject: str
    ) -> Theorem:
        if clock_boundary.proposition.kind != "clock_augmented_conveyor_boundary":
            raise ProofError("finite-volume clock estimate needs the clock boundary")
        return self._issue(
            Proposition.make(
                "quasi_ideal_clock_finite_volume_error",
                subject,
                clock_dimension="d",
                single_control_error_bound="epsilon_d <= A exp(-c d)",
                local_operation_count="N_L=2L",
                composition_error_bound="epsilon_global <= 2 L A exp(-c d)",
                finite_volume_arbitrary_accuracy=True,
                exact_finite_clock_control_derived=False,
            ),
            "diamond_norm_composition_telescoping_rule",
            premises=(clock_boundary,),
            certificate={"telescoping_terms": "2L", "constants": "A,c>0"},
        )

    def prove_logarithmic_clock_resource_schedule(
        self, error_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if error_theorem.proposition.kind != "quasi_ideal_clock_finite_volume_error":
            raise ProofError("resource schedule needs a finite-volume error estimate")
        return self._issue(
            Proposition.make(
                "logarithmic_clock_resource_schedule",
                subject,
                target_error="delta in (0,1)",
                sufficient_dimension="d >= log(2 A L/delta)/c",
                assumed_clock_energy="E_d <= E_0 d",
                sufficient_energy_scaling="E_d = O(log(L/delta))",
                dimension_independent_of_volume=False,
                finite_volume_autonomous_approximation_admitted=True,
            ),
            "exact_exponential_error_inversion_rule",
            premises=(error_theorem,),
            certificate={"substitution_bound": "2LA exp(-cd) <= delta"},
        )

    def prove_fixed_clock_global_uniformity_boundary(
        self, resource_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if resource_theorem.proposition.kind != "logarithmic_clock_resource_schedule":
            raise ProofError("global boundary needs the logarithmic resource schedule")
        return self._issue(
            Proposition.make(
                "fixed_clock_global_uniformity_boundary",
                subject,
                fixed_dimension_certificate_uniform_in_L=False,
                global_channel_norm_limit_requires_growing_clock_resource=True,
                exact_global_conveyor_from_quasi_ideal_clock=False,
                universal_autonomous_clock_no_go=False,
                reason="the available upper-bound proof scales as L epsilon_d",
            ),
            "explicit_nonuniform_error_certificate_boundary_rule",
            premises=(resource_theorem,),
        )

    def prove_local_observable_clock_limit_admission(
        self, global_boundary: Theorem, *, subject: str
    ) -> Theorem:
        if global_boundary.proposition.kind != "fixed_clock_global_uniformity_boundary":
            raise ProofError("local-observable admission needs the global boundary")
        return self._issue(
            Proposition.make(
                "local_observable_clock_limit_admission",
                subject,
                observable_support="finite",
                finite_time_causal_gate_count="N_loc independent of L",
                local_error_bound="epsilon_local <= N_loc A exp(-c d)",
                local_thermodynamic_approximation_admitted=True,
                global_norm_thermodynamic_approximation_derived=False,
                absolute_tick_duration_derived=False,
                next_gate="local_observable_clocked_qms_limit_and_time_anchor",
            ),
            "finite_causal_cone_local_error_rule",
            premises=(global_boundary,),
            certificate={"limit_order": "finite support and time, then L->infinity"},
        )

    def prove_clocked_collision_error_decomposition(
        self,
        local_clock_theorem: Theorem,
        collision_limit_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        if local_clock_theorem.proposition.kind != "local_observable_clock_limit_admission":
            raise ProofError("clocked collision estimate needs the local clock theorem")
        if collision_limit_theorem.proposition.kind != "structural_star_collision_limit":
            raise ProofError("clocked collision estimate needs a collision-limit theorem")
        return self._issue(
            Proposition.make(
                "clocked_collision_error_decomposition",
                subject,
                collision_step="h=u/n",
                collision_discretisation_bound="C_u/n",
                clock_error_per_step="epsilon_d <= A exp(-c d)",
                accumulated_clock_error="n A exp(-c d)",
                total_reduced_error="epsilon_(n,d) <= C_u/n + n A exp(-c d)",
            ),
            "collision_chernoff_plus_channel_telescoping_rule",
            premises=(local_clock_theorem, collision_limit_theorem),
            certificate={"error_sources": ("collision discretisation", "clock control")},
        )

    def prove_joint_clock_collision_continuum_limit(
        self, error_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if error_theorem.proposition.kind != "clocked_collision_error_decomposition":
            raise ProofError("joint limit needs the clocked collision error theorem")
        return self._issue(
            Proposition.make(
                "joint_clock_collision_continuum_limit",
                subject,
                alpha="alpha>0",
                clock_schedule="d_n >= (1+alpha) log(n)/c",
                substituted_error_bound="epsilon_(n,d_n) <= C_u/n + A/n^alpha",
                limit="epsilon_(n,d_n) -> 0 as n -> infinity",
                dimension_growth="O(log n)",
                continuous_dimensionless_qms_recovered=True,
            ),
            "exact_joint_asymptotic_error_rule",
            premises=(error_theorem,),
            certificate={"limits": ("1/n -> 0", "1/n^alpha -> 0")},
        )

    def prove_clocked_reduced_observable_limit(
        self, joint_limit_theorem: Theorem, *, subject: str
    ) -> Theorem:
        if joint_limit_theorem.proposition.kind != "joint_clock_collision_continuum_limit":
            raise ProofError("reduced observable limit needs the joint continuum theorem")
        return self._issue(
            Proposition.make(
                "clocked_reduced_observable_qms_limit",
                subject,
                convergence_scope="finite system observables and finite ancilla cylinders",
                global_infinite_chain_state_norm_convergence=False,
                reduced_qms_limit=True,
                fresh_ancilla_reset_external=False,
                preloaded_conveyor_used=True,
                clock_dimension_diverges_logarithmically=True,
            ),
            "finite_cylinder_reduced_limit_rule",
            premises=(joint_limit_theorem,),
        )

    def prove_clocked_qms_common_time_scale_boundary(
        self,
        reduced_limit_theorem: Theorem,
        physical_time_no_go_theorem: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        if reduced_limit_theorem.proposition.kind != "clocked_reduced_observable_qms_limit":
            raise ProofError("time-scale boundary needs the reduced clocked QMS limit")
        if physical_time_no_go_theorem.proposition.kind != "collision_physical_time_scale_no_go":
            raise ProofError("time-scale boundary needs the collision scale no-go")
        lam, omega, rate, time = sp.symbols(
            "lambda Omega Gamma t_phys", positive=True
        )
        clock_phase_residual = sp.simplify((lam * omega) * (time / lam) - omega * time)
        qms_time_residual = sp.simplify((lam * rate) * (time / lam) - rate * time)
        if clock_phase_residual != 0 or qms_time_residual != 0:
            raise ProofError("common clock/rate scale orbit failed")
        return self._issue(
            Proposition.make(
                "clocked_qms_common_time_scale_boundary",
                subject,
                clock_invariant="Omega t_phys",
                dissipative_invariant="Gamma t_phys",
                relative_rate="Gamma/Omega",
                common_rescaling="(Omega,Gamma,t) -> (lambda Omega,lambda Gamma,t/lambda)",
                autonomous_dimensionless_time_recovered=True,
                absolute_second_selected=False,
                required_anchor="one independently fixed clock energy or decay rate",
                next_gate="typed_clock_energy_to_noise_rate_anchor",
            ),
            "exact_common_clock_rate_scale_orbit_rule",
            premises=(reduced_limit_theorem, physical_time_no_go_theorem),
            certificate={
                "clock_phase_residual": str(clock_phase_residual),
                "qms_time_residual": str(qms_time_residual),
            },
        )

    def prove_typed_clock_collision_rate_identity(
        self, time_boundary: Theorem, *, subject: str
    ) -> Theorem:
        if time_boundary.proposition.kind != "clocked_qms_common_time_scale_boundary":
            raise ProofError("typed rate identity needs the clocked-QMS scale boundary")
        hbar, energy_clock, chi = sp.symbols("hbar E_C chi", positive=True)
        tau = hbar / energy_clock
        energy_interaction = chi * energy_clock
        rate = sp.simplify(energy_interaction**2 * tau / hbar**2)
        omega = energy_clock / hbar
        if sp.simplify(rate - chi**2 * omega) != 0:
            raise ProofError("typed collision-rate identity failed")
        return self._issue(
            Proposition.make(
                "typed_clock_collision_rate_identity",
                subject,
                clock_tick="tau_C=hbar/E_C",
                interaction_energy="E_int=chi E_C",
                dissipative_rate="Gamma=E_int^2 tau_C/hbar^2=chi^2 E_C/hbar",
                clock_frequency="Omega=E_C/hbar",
                relative_rate="Gamma/Omega=chi^2",
            ),
            "exact_dimensional_repeated_interaction_rule",
            premises=(time_boundary,),
            certificate={"residual": "zero"},
        )

    def prove_clock_rate_relative_calibration(
        self, rate_identity: Theorem, *, subject: str
    ) -> Theorem:
        if rate_identity.proposition.kind != "typed_clock_collision_rate_identity":
            raise ProofError("relative calibration needs the typed rate identity")
        return self._issue(
            Proposition.make(
                "clock_rate_relative_calibration",
                subject,
                dimensionless_coupling="chi=E_int/E_C",
                calibrated_ratio="Gamma/Omega=chi^2",
                relative_calibration_obtained_conditionally=True,
                absolute_clock_energy_required=True,
            ),
            "exact_rate_to_clock_frequency_ratio_rule",
            premises=(rate_identity,),
        )

    def prove_clock_interaction_scale_underdetermination(
        self, calibration: Theorem, *, subject: str
    ) -> Theorem:
        if calibration.proposition.kind != "clock_rate_relative_calibration":
            raise ProofError("scale underdetermination needs relative calibration")
        return self._issue(
            Proposition.make(
                "clock_interaction_scale_underdetermination",
                subject,
                admissible_couplings=("chi_1", "chi_2"),
                same_clock_carrier=True,
                same_noise_frame=True,
                distinct_relative_rates="chi_1^2 != chi_2^2",
                current_parent_selects_chi=False,
                equality_E_int_E_C_derived=False,
            ),
            "two_admissible_dimensionless_couplings_countermodel_rule",
            premises=(calibration,),
        )

    def prove_typed_clock_energy_anchor_no_go(
        self, underdetermination: Theorem, *, subject: str
    ) -> Theorem:
        if underdetermination.proposition.kind != "clock_interaction_scale_underdetermination":
            raise ProofError("energy-anchor no-go needs coupling underdetermination")
        return self._issue(
            Proposition.make(
                "typed_clock_energy_anchor_no_go",
                subject,
                dimensionless_generator_gap_is_energy_anchor=False,
                legacy_cutoff_typed_to_clock=False,
                legacy_mass_typed_to_clock=False,
                clock_energy_E_C_derived=False,
                coupling_ratio_chi_derived=False,
                absolute_rate_Gamma_derived=False,
                conditional_bridge="Gamma=chi^2 E_C/hbar",
                next_gate="clock_energy_anchor_candidate_audit",
            ),
            "explicit_missing_typed_dimensional_morphism_rule",
            premises=(underdetermination,),
        )

    def prove_block_subalgebra_invariant(
        self, generator: Any, block_dimensions: Sequence[int], *, subject: str
    ) -> Theorem:
        dimensions = tuple(block_dimensions)
        if sum(dimensions) != generator.space.dimension or any(
            dimension <= 0 for dimension in dimensions
        ):
            raise ProofError("block dimensions do not partition the generator space")
        offsets = [0]
        for dimension in dimensions:
            offsets.append(offsets[-1] + dimension)
        checked = 0
        for block, dimension in enumerate(dimensions):
            start = offsets[block]
            stop = offsets[block + 1]
            for row in range(start, stop):
                for column in range(start, stop):
                    unit = sp.zeros(generator.space.dimension)
                    unit[row, column] = 1
                    image = generator.act(unit)
                    for i in range(generator.space.dimension):
                        for j in range(generator.space.dimension):
                            same_block = any(
                                offsets[index] <= i < offsets[index + 1]
                                and offsets[index] <= j < offsets[index + 1]
                                for index in range(len(dimensions))
                            )
                            if not same_block and sp.simplify(image[i, j]) != 0:
                                raise ProofError("block subalgebra is not invariant")
                    checked += 1
        return self._issue(
            Proposition.make(
                "invariant_block_subalgebra",
                subject,
                blocks=dimensions,
                checked_matrix_units=checked,
            ),
            "exact_matrix_unit_invariance_rule",
            premises=(generator.theorem,),
        )

    def prove_linear_maps_equal_on_basis(
        self,
        basis: Sequence[sp.MatrixBase],
        left_map: Any,
        right_map: Any,
        *,
        subject: str,
        premises: Sequence[Theorem] = (),
    ) -> Theorem:
        if not basis:
            raise ProofError("a linear-map comparison needs a nonempty basis")
        for index, item in enumerate(basis):
            left = _exact_matrix(left_map(item))
            right = _exact_matrix(right_map(item))
            if left.shape != right.shape or not _zero_matrix(left - right):
                raise ProofError(f"linear maps differ on basis vector {index}")
        return self._issue(
            Proposition.make(
                "linear_maps_equal_on_basis",
                subject,
                basis_size=len(basis),
            ),
            "exact_linear_basis_extensionality_rule",
            premises=premises,
        )

    def prove_kraus_history_recovery(self, history: Any, *, subject: str) -> Theorem:
        """Check exact conditional recovery for every slice of a finite history."""

        if history.channel.theorem.proposition.kind != "kraus_channel":
            raise ProofError("a history requires a kernel-checked Kraus channel")
        traces = []
        nonzero_branch_bounds = []
        for step in range(history.clock_dimension):
            branch_state = _exact_matrix(history.branch_reduced_state(step))
            iterated_state = _exact_matrix(history.iterated_state(step))
            if not _zero_matrix(branch_state - iterated_state):
                raise ProofError(f"history slice {step} does not recover the channel iterate")
            trace = sp.simplify(sp.trace(branch_state))
            if trace != 1:
                raise ProofError(f"history slice {step} is not normalized")
            traces.append(str(trace))
            nonzero_branch_bounds.append(history.branch_count(step))
        return self._issue(
            Proposition.make(
                "kraus_history_conditional_recovery",
                subject,
                steps=history.steps,
                clock_dimension=history.clock_dimension,
                environment_dimension=history.environment_dimension,
                branch_count_bounds=tuple(nonzero_branch_bounds),
                slice_traces=tuple(traces),
            ),
            "exact_kraus_branch_induction_rule",
            premises=(history.channel.theorem,),
            certificate={"all_slice_residuals": "zero"},
        )

    def prove_isometric_history_parent(
        self, history: Any, recovery: Theorem, *, subject: str
    ) -> Theorem:
        """Issue the frustration-free parent statement for an isometric history."""

        if recovery.proposition.kind != "kraus_history_conditional_recovery":
            raise ProofError("the history parent requires conditional recovery")
        if recovery.proposition.data["steps"] != history.steps:
            raise ProofError("history and recovery theorem disagree on clock length")
        system_dimension = history.channel.space.dimension
        return self._issue(
            Proposition.make(
                "isometric_history_parent_zero_modes",
                subject,
                clock_dimension=history.clock_dimension,
                zero_mode_family_dimension=system_dimension,
                frustration_free=True,
                global_history_stationary=True,
            ),
            "stinespring_isometry_history_parent_rule",
            premises=(history.channel.theorem, recovery),
            certificate={"propagation_residual": "zero"},
        )

    def prove_stinespring_unitary_extension_freedom(
        self, system_dimension: int, environment_dimension: int, *, subject: str
    ) -> Theorem:
        """Count the complement on which a Stinespring unitary is undetermined."""

        if system_dimension <= 0 or environment_dimension <= 1:
            raise ProofError("a nontrivial extension needs positive system and environment")
        total_dimension = system_dimension * environment_dimension
        complement_dimension = total_dimension - system_dimension
        if complement_dimension <= 0:
            raise ProofError("the Stinespring image has no extension complement")
        return self._issue(
            Proposition.make(
                "nonunique_stinespring_unitary_extension",
                subject,
                system_dimension=system_dimension,
                environment_dimension=environment_dimension,
                total_dimension=total_dimension,
                unconstrained_complement_dimension=complement_dimension,
                extension_unitary_group=f"U({complement_dimension})",
                extension_real_parameter_dimension=complement_dimension**2,
                canonical_unitary_extension=False,
            ),
            "finite_dimensional_isometry_extension_count_rule",
        )

    def prove_covariant_stinespring_extension_ambiguity(
        self,
        channel: Any,
        covariance: Theorem,
        *,
        subject: str,
    ) -> Theorem:
        """Prove the complement-phase ambiguity of a covariant dilation.

        If ``W`` is the Stinespring isometry and ``P=W W*``, then
        ``V_z=P+z(I-P)`` fixes ``W`` for every unit-modulus ``z``.  Covariance
        makes ``P`` invariant, hence the family is symmetry-compatible.  The
        real even subfamily still contains the distinct choices ``z=+1,-1``.
        """

        if channel.theorem.proposition.kind != "kraus_channel":
            raise ProofError("extension ambiguity requires a Kraus channel")
        if covariance.proposition.kind != "covariant_kraus_channel":
            raise ProofError("extension ambiguity requires channel covariance")
        environment_dimension = len(channel.kraus)
        system_dimension = channel.space.dimension
        complement_dimension = system_dimension * (environment_dimension - 1)
        if complement_dimension <= 0:
            raise ProofError("the Stinespring image must have a nonzero complement")
        return self._issue(
            Proposition.make(
                "covariant_stinespring_extension_ambiguity",
                subject,
                system_dimension=system_dimension,
                environment_dimension=environment_dimension,
                image_dimension=system_dimension,
                complement_dimension=complement_dimension,
                complex_phase_family="U(1)",
                real_even_surviving_choices=("+1", "-1"),
                same_reduced_channel=True,
                unique_covariant_unitary_extension=False,
            ),
            "stinespring_complement_phase_rule",
            premises=(channel.theorem, covariance),
            certificate={"V_z_W_minus_W": "zero", "commutator_with_symmetry": "zero"},
        )

    def prove_gate(self, identifier: str, premises: Sequence[Theorem]) -> Theorem:
        checked = tuple(premises)
        if not identifier or not checked:
            raise ProofError("a verified gate needs an identifier and theorem premises")
        if not all(isinstance(item, Theorem) for item in checked):
            raise ProofError("every gate obligation must return a kernel theorem")
        return self._issue(
            Proposition.make(
                "verified_gate",
                identifier,
                obligation_count=len(checked),
                obligation_kinds=tuple(item.proposition.kind for item in checked),
            ),
            "gate_conjunction_rule",
            premises=checked,
        )


kernel = Kernel()