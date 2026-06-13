from __future__ import annotations

from agenttrace.models.trace import Issue, Step


def detect_tool_repetition(steps: list[Step]) -> list[Issue]:
    issues: list[Issue] = []
    if not steps:
        return issues

    current_name: str | None = None
    current_count = 0

    def flush(name: str | None, count: int) -> None:
        if not name or count < 3:
            return
        severity = "Critical" if count >= 5 else "Warning"
        issues.append(
            Issue(
                kind="tool_repetition",
                title="Tool Repetition Detected",
                severity=severity,
                details={"tool": name, "occurrences": count},
                recommendation="Add result caching or planner confidence thresholds.",
            )
        )

    for step in steps:
        if step.type != "tool" or not step.name:
            flush(current_name, current_count)
            current_name = None
            current_count = 0
            continue
        if step.name == current_name:
            current_count += 1
        else:
            flush(current_name, current_count)
            current_name = step.name
            current_count = 1
    flush(current_name, current_count)
    return issues
