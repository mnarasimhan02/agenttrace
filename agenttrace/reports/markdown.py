from __future__ import annotations

from agenttrace.models.trace import AnalysisResult


def render_markdown_report(result: AnalysisResult) -> str:
    lines = [
        "# AgentTrace Report",
        "",
        "## Summary",
        f"- Reliability Score: {result.reliability_score}",
        f"- Total Tokens: {result.total_tokens}",
        f"- Estimated Waste: {result.wasted_tokens}",
        "",
        "## Issues Found",
    ]
    if not result.issues:
        lines.append("- None")
    else:
        for issue in result.issues:
            lines.append(f"- {issue.title} ({issue.severity}): {issue.details}")
    lines += ["", "## Recommendations"]
    recommendations = [issue.recommendation for issue in result.issues if issue.recommendation]
    if recommendations:
        lines.extend(f"- {recommendation}" for recommendation in recommendations)
    else:
        lines.append("- No issues detected.")
    return "\n".join(lines) + "\n"
