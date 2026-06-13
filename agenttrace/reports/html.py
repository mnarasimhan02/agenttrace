from __future__ import annotations

from html import escape

from agenttrace.models.trace import AnalysisResult


def render_html_report(result: AnalysisResult) -> str:
    issues = "".join(
        f"<li>{escape(issue.title)} ({escape(issue.severity)}): {escape(str(issue.details))}</li>"
        for issue in result.issues
    ) or "<li>None</li>"
    recommendations = "".join(
        f"<li>{escape(issue.recommendation)}</li>"
        for issue in result.issues
        if issue.recommendation
    ) or "<li>No issues detected.</li>"
    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>AgentTrace Report</title></head>
<body>
  <h1>AgentTrace Report</h1>
  <p><strong>Reliability Score:</strong> {result.reliability_score}</p>
  <p><strong>Total Tokens:</strong> {result.total_tokens}</p>
  <p><strong>Estimated Waste:</strong> {result.wasted_tokens}</p>
  <h2>Issues Found</h2>
  <ul>{issues}</ul>
  <h2>Recommendations</h2>
  <ul>{recommendations}</ul>
</body>
</html>
"""
