"""Copy this template when migrating another exact project gate."""

from __future__ import annotations

from s2t.proofdsl.gates import GateSpec, Obligation
from s2t.proofdsl.kernel import kernel


def prove_primary_identity():
    # Replace the exact expressions below. Float values are intentionally banned.
    return kernel.prove_expression_equality(
        1 + 1,
        2,
        subject="replace_with_project_statement",
    )


SPEC = GateSpec(
    identifier="replace_namespace_topic",
    title="Краткое название формального гейта",
    source_paths=("path/to/source.tex", "path/to/result.json"),
    obligations=(Obligation("primary_identity", prove_primary_identity),),
)