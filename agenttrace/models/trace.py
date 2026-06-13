from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


class TraceParseError(ValueError):
    """Raised when a trace file cannot be normalized into AgentTrace models."""


@dataclass(slots=True)
class Step:
    step_id: int | None = None
    type: str = "tool"
    name: str | None = None
    tokens: int = 0
    status: str | None = None


@dataclass(slots=True)
class Trace:
    steps: list[Step] = field(default_factory=list)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Trace":
        if not isinstance(payload, dict):
            raise TraceParseError("Trace file must contain a JSON object.")

        raw_steps = payload.get("steps", [])
        if raw_steps is None:
            raw_steps = []
        if not isinstance(raw_steps, list):
            raise TraceParseError("The 'steps' field must be a JSON array.")

        steps = []
        for index, raw_step in enumerate(raw_steps, start=1):
            if not isinstance(raw_step, dict):
                raise TraceParseError(f"Step {index} must be a JSON object.")
            step_id = raw_step.get("step_id")
            if step_id is not None and not isinstance(step_id, int):
                raise TraceParseError(f"Step {index} has an invalid 'step_id' value.")

            raw_tokens = raw_step.get("tokens", 0)
            try:
                tokens = int(raw_tokens or 0)
            except (TypeError, ValueError) as exc:
                raise TraceParseError(f"Step {index} has an invalid 'tokens' value.") from exc
            tokens = max(tokens, 0)

            step_type = raw_step.get("type", "tool")
            if step_type is None:
                step_type = "tool"
            if not isinstance(step_type, str):
                raise TraceParseError(f"Step {index} has an invalid 'type' value.")

            name = raw_step.get("name")
            if name is not None and not isinstance(name, str):
                raise TraceParseError(f"Step {index} has an invalid 'name' value.")

            status = raw_step.get("status")
            if status is not None and not isinstance(status, str):
                raise TraceParseError(f"Step {index} has an invalid 'status' value.")

            steps.append(
                Step(
                    step_id=step_id,
                    type=step_type,
                    name=name,
                    tokens=tokens,
                    status=status,
                )
            )
        return cls(steps=steps)


@dataclass(slots=True)
class Issue:
    kind: str
    title: str
    severity: Literal["Info", "Warning", "Critical"]
    details: dict[str, Any] = field(default_factory=dict)
    recommendation: str | None = None


@dataclass(slots=True)
class AnalysisResult:
    reliability_score: int
    total_tokens: int
    wasted_tokens: int
    context_growth_percent: float | None = None
    average_growth_rate: float | None = None
    issues: list[Issue] = field(default_factory=list)
