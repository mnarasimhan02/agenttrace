from __future__ import annotations

from agenttrace.models.trace import Issue, Step


def detect_retry_storm(steps: list[Step]) -> list[Issue]:
    issues: list[Issue] = []
    failure_count = 0
    failure_spans: list[int] = []

    for step in steps:
        is_failure = (step.status or "").lower() in {"error", "failed", "failure"}
        if is_failure:
            failure_count += 1
            continue
        if failure_count >= 3:
            failure_spans.append(failure_count)
        failure_count = 0

    if failure_count >= 3:
        failure_spans.append(failure_count)

    for span in failure_spans:
        severity = "Critical" if span >= 5 else "Warning"
        issues.append(
            Issue(
                kind="retry_storm",
                title="Retry Storm Detected",
                severity=severity,
                details={
                    "failed_attempts": span,
                    "span_type": "consecutive_failures",
                },
                recommendation="Implement retry limits and fallback logic.",
            )
        )

    return issues
