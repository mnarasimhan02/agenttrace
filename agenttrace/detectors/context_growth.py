from __future__ import annotations

from agenttrace.models.trace import Issue, Step


def detect_context_growth(steps: list[Step]) -> tuple[list[Issue], float | None, float | None]:
    token_counts = [step.tokens for step in steps]
    if len(token_counts) < 2:
        return [], None, None

    initial = token_counts[0]
    final = token_counts[-1]
    if initial <= 0:
        growth_percent = None
    else:
        growth_percent = ((final - initial) / initial) * 100.0

    deltas: list[float] = []
    for earlier, later in zip(token_counts, token_counts[1:]):
        if earlier > 0:
            deltas.append(((later - earlier) / earlier) * 100.0)
    average_growth_rate = sum(deltas) / len(deltas) if deltas else None

    issues: list[Issue] = []
    if growth_percent is not None and growth_percent > 100:
        severity = "Critical" if growth_percent > 300 else "Warning"
        peak_tokens = max(token_counts)
        issues.append(
            Issue(
                kind="context_growth",
                title="Context Explosion Detected",
                severity=severity,
                details={
                    "initial_tokens": initial,
                    "final_tokens": final,
                    "peak_tokens": peak_tokens,
                    "growth_percent": round(growth_percent, 2),
                    "average_growth_rate": round(average_growth_rate, 2) if average_growth_rate is not None else None,
                },
                recommendation="Add context summarization or memory compression.",
            )
        )
    return issues, growth_percent, average_growth_rate
