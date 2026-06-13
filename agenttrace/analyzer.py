from __future__ import annotations

from agenttrace.detectors import detect_context_growth, detect_retry_storm, detect_tool_repetition
from agenttrace.models.trace import AnalysisResult, Issue, Trace


def estimate_waste(issues: list[Issue]) -> int:
    wasted = 0
    for issue in issues:
        if issue.kind == "tool_repetition":
            occurrences = int(issue.details.get("occurrences", 0))
            wasted += max(0, occurrences - 1) * 100
        elif issue.kind == "retry_storm":
            failed_attempts = int(issue.details.get("failed_attempts", 0))
            wasted += failed_attempts * 150
        elif issue.kind == "context_growth":
            wasted += int(issue.details.get("final_tokens", 0)) - int(issue.details.get("initial_tokens", 0))
    return max(wasted, 0)


def reliability_score(issues: list[Issue]) -> int:
    score = 100
    for issue in issues:
        if issue.severity == "Warning":
            score -= 12
        elif issue.severity == "Critical":
            score -= 24
    return max(0, score)


def analyze_trace(trace: Trace) -> AnalysisResult:
    repetition_issues = detect_tool_repetition(trace.steps)
    retry_issues = detect_retry_storm(trace.steps)
    context_issues, growth_percent, avg_growth_rate = detect_context_growth(trace.steps)
    issues = [*repetition_issues, *retry_issues, *context_issues]
    total_tokens = sum(step.tokens for step in trace.steps)
    wasted_tokens = estimate_waste(issues)
    return AnalysisResult(
        reliability_score=reliability_score(issues),
        total_tokens=total_tokens,
        wasted_tokens=wasted_tokens,
        context_growth_percent=growth_percent,
        average_growth_rate=avg_growth_rate,
        issues=issues,
    )
