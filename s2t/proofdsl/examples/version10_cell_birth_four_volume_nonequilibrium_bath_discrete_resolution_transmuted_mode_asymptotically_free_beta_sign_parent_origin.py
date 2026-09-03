"""LCF certificate for the parent origin of an asymptotically-free beta sign."""

from dataclasses import dataclass
from functools import lru_cache
import sympy as sp

from ..gates import GateSpec, Obligation
from ..kernel import Theorem, kernel


@dataclass(frozen=True, slots=True)
class AsymptoticallyFreeBetaSignParentOriginCertificate:
    required_beta: sp.Expr
    inherited_beta: sp.Expr
    su2_beta: sp.Expr
    su3_beta: sp.Expr
    anomalous_su3_weyl_beta: sp.Expr
    beta_constraint_map: sp.ImmutableMatrix
    beta_constraint_kernel: sp.ImmutableMatrix
    beta_parent_hessian: sp.ImmutableMatrix
    candidate_matrix: sp.ImmutableMatrix
    score_vector: sp.ImmutableMatrix
    pass_vector: sp.ImmutableMatrix
    conditional_exact_carriers: sp.ImmutableMatrix
    physical_origin: sp.ImmutableMatrix
    theorems: tuple[Theorem, ...]
    gate_theorem: Theorem


@lru_cache(maxsize=1)
def build_certificate() -> AsymptoticallyFreeBetaSignParentOriginCertificate:
    required_beta = sp.Integer(-2)
    inherited_beta = sp.Integer(2)

    # Convention: beta_g = b g^3/(16 pi^2), with n_D Dirac and n_s complex
    # fundamental multiplets: b=-11 C_A/3+2 n_D/3+n_s/6.
    c_a, n_d, n_s = sp.symbols("C_A n_D n_s", real=True)
    beta = -sp.Rational(11, 3) * c_a + sp.Rational(2, 3) * n_d + sp.Rational(1, 6) * n_s
    su2_beta = sp.simplify(beta.subs({c_a: 2, n_d: 8, n_s: 0}))
    su3_beta = sp.simplify(beta.subs({c_a: 3, n_d: 13, n_s: 2}))
    anomalous_su3_weyl_beta = sp.simplify(-11 + sp.Rational(27, 3))

    # The multiplied condition 6b=-12 is -22 C_A+4 n_D+n_s=-12.
    beta_constraint_map = sp.ImmutableMatrix([[-22, 4, 1]])
    beta_constraint_kernel = sp.ImmutableMatrix([
        [sp.Rational(2, 11), sp.Rational(1, 22)],
        [1, 0],
        [0, 1],
    ])
    residual = -22 * c_a + 4 * n_d + n_s + 12
    beta_parent_hessian = sp.ImmutableMatrix(sp.hessian(residual**2 / 2, (c_a, n_d, n_s)))

    # Columns: typed gauge beta, internal carrier, negative sign, exact -2,
    # anomaly-free field content, independently parent-selected.
    candidate_matrix = sp.ImmutableMatrix([
        [1, 1, 0, 0, 1, 1],  # inherited relative U(1)
        [1, 0, 1, 0, 1, 1],  # pure SU(2)
        [1, 0, 1, 0, 1, 1],  # pure SU(3)
        [1, 0, 1, 1, 1, 0],  # SU(2)+8 Dirac fundamentals
        [1, 0, 1, 1, 0, 0],  # SU(3)+27 chiral Weyl fundamentals
        [1, 0, 1, 1, 1, 0],  # SU(3)+13 Dirac+2 complex scalars
        [0, 1, 0, 0, 0, 0],  # reinterpretation of the K43/BV number 27
        [0, 1, 0, 0, 1, 1],  # bath/ghost coefficient of the wrong type
        [1, 1, 1, 1, 1, 0],  # formal b=-2 insertion
    ])
    score_vector = sp.ImmutableMatrix([sum(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    pass_vector = sp.ImmutableMatrix([sp.prod(candidate_matrix.row(i)) for i in range(candidate_matrix.rows)])
    conditional_exact_carriers = sp.ImmutableMatrix([1, 1])
    physical_origin = sp.zeros(4, 1)

    theorems = (
        kernel.prove_expression_equality(required_beta, -2, subject="required asymptotically-free beta coefficient"),
        kernel.prove_expression_equality(inherited_beta, 2, subject="inherited relative-U1 beta coefficient"),
        kernel.prove_expression_equality(required_beta + inherited_beta, 0, subject="required beta sign reverses the inherited coefficient"),
        kernel.prove_expression_equality(su2_beta, required_beta, subject="SU2 with eight Dirac fundamentals conditionally gives beta minus two"),
        kernel.prove_expression_equality(su3_beta, required_beta, subject="SU3 with thirteen Dirac fundamentals and two scalars conditionally gives beta minus two"),
        kernel.prove_expression_equality(anomalous_su3_weyl_beta, required_beta, subject="twenty-seven chiral SU3 Weyl fundamentals give the coefficient but not anomaly cancellation"),
        kernel.prove_exact_rank(beta_constraint_map, 1, subject="one beta equation constrains three field-content variables"),
        kernel.prove_exact_nullity(beta_constraint_map, 2, subject="the beta equation leaves two field-content directions free"),
        kernel.prove_matrix_equality(beta_constraint_map * beta_constraint_kernel, sp.zeros(1, 2), subject="two exact field-content deformations preserve beta minus two"),
        kernel.prove_exact_rank(beta_parent_hessian, 1, subject="the beta mismatch parent is only semidefinite"),
        kernel.prove_exact_nullity(beta_parent_hessian, 2, subject="the beta parent does not select a unique carrier"),
        kernel.prove_matrix_equality(beta_parent_hessian * beta_constraint_kernel, sp.zeros(3, 2), subject="the parent has the same two flat field-content directions"),
        kernel.prove_expression_equality(candidate_matrix.shape[0], 9, subject="nine beta-sign candidates are audited"),
        kernel.prove_expression_equality(candidate_matrix.shape[1], 6, subject="six beta-origin criteria are applied"),
        kernel.prove_exact_rank(candidate_matrix, 6, subject="beta-sign audit has full criterion rank"),
        kernel.prove_matrix_equality(score_vector, sp.ImmutableMatrix([4, 4, 4, 4, 3, 4, 1, 3, 5]), subject="beta-sign candidate score ledger"),
        kernel.prove_expression_equality(max(score_vector), 5, subject="best beta-sign candidate remains incomplete"),
        kernel.prove_matrix_equality(pass_vector, sp.zeros(9, 1), subject="no beta-sign candidate passes all origin criteria"),
        kernel.prove_expression_equality(sum(pass_vector), 0, subject="strict beta-sign pass count is zero"),
        kernel.prove_matrix_equality(conditional_exact_carriers, sp.ones(2, 1), subject="two anomaly-free nonabelian field contents conditionally realize the exact coefficient"),
        kernel.prove_expression_equality(sum(conditional_exact_carriers), 2, subject="two explicit exact conditional carriers are exhibited"),
        kernel.prove_matrix_equality(physical_origin, sp.zeros(4, 1), subject="gauge algebra matter representation multiplicity and common parent origins remain open"),
        kernel.prove_expression_equality(sum(physical_origin), 0, subject="strict asymptotically-free carrier origin score remains zero"),
    )
    gate_theorem = kernel.prove_gate(
        "version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate",
        theorems,
    )
    return AsymptoticallyFreeBetaSignParentOriginCertificate(
        required_beta, inherited_beta, su2_beta, su3_beta, anomalous_su3_weyl_beta,
        beta_constraint_map, beta_constraint_kernel, beta_parent_hessian,
        candidate_matrix, score_vector, pass_vector, conditional_exact_carriers,
        physical_origin, theorems, gate_theorem,
    )


SPEC = GateSpec(
    identifier="version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate",
    title="Родитель отрицательного beta-знака асимптотически-свободной моды",
    source_paths=(
        "s2t/gates/version10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate.tex",
        "s2t/results/s2t_v10_cell_birth_four_volume_nonequilibrium_bath_discrete_resolution_transmuted_mode_asymptotically_free_beta_sign_parent_origin_gate_results.json",
    ),
    obligations=tuple(
        Obligation(f"asymptotically_free_beta_sign_parent_{i:02d}", lambda i=i: build_certificate().theorems[i])
        for i in range(23)
    ),
)