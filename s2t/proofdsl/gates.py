"""Reusable gate specification, verification and certificate template."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Callable, Iterable

import sympy as sp

from .kernel import Theorem, kernel


TheoremFactory = Callable[[], Theorem]


@dataclass(frozen=True, slots=True)
class Obligation:
    name: str
    prove: TheoremFactory

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("an obligation must have a name")


@dataclass(frozen=True, slots=True)
class GateSpec:
    identifier: str
    title: str
    source_paths: tuple[str, ...]
    obligations: tuple[Obligation, ...]

    def __init__(
        self,
        identifier: str,
        title: str,
        source_paths: Iterable[str],
        obligations: Iterable[Obligation],
    ) -> None:
        paths = tuple(source_paths)
        checks = tuple(obligations)
        if not identifier or not title or not paths or not checks:
            raise ValueError("gate identifier, title, sources and obligations are required")
        names = [item.name for item in checks]
        if len(names) != len(set(names)):
            raise ValueError("obligation names must be unique within a gate")
        object.__setattr__(self, "identifier", identifier)
        object.__setattr__(self, "title", title)
        object.__setattr__(self, "source_paths", paths)
        object.__setattr__(self, "obligations", checks)


def _json_value(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    if isinstance(value, sp.Basic):
        return str(value)
    return str(value)


def theorem_record(theorem: Theorem) -> dict[str, object]:
    return {
        "kind": theorem.proposition.kind,
        "subject": theorem.proposition.subject,
        "data": _json_value(dict(theorem.proposition.data)),
        "rule": theorem.rule,
        "premise_count": len(theorem.premises),
        "certificate": _json_value(dict(theorem.certificate)),
    }


@dataclass(frozen=True, slots=True)
class VerifiedGate:
    spec: GateSpec
    obligations: tuple[tuple[str, Theorem], ...]
    theorem: Theorem

    def to_dict(self) -> dict[str, object]:
        return {
            "identifier": self.spec.identifier,
            "title": self.spec.title,
            "status": "lcf-checked",
            "source_paths": list(self.spec.source_paths),
            "obligations": [
                {"name": name, "theorem": theorem_record(theorem)}
                for name, theorem in self.obligations
            ],
            "gate_theorem": theorem_record(self.theorem),
        }

    def canonical_json(self) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode()).hexdigest()


def verify_gate(spec: GateSpec) -> VerifiedGate:
    checked = []
    for obligation in spec.obligations:
        theorem = obligation.prove()
        if not isinstance(theorem, Theorem):
            raise TypeError(f"obligation {obligation.name} did not return a Theorem")
        checked.append((obligation.name, theorem))
    gate_theorem = kernel.prove_gate(
        spec.identifier, [theorem for _, theorem in checked]
    )
    return VerifiedGate(spec, tuple(checked), gate_theorem)