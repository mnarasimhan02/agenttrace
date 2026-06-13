from pathlib import Path
import json
import tempfile

from agenttrace.analyzer import analyze_trace
from agenttrace.app import load_trace
from agenttrace.models.trace import Trace, TraceParseError


def load_sample(name: str) -> Trace:
    path = Path("sample_traces") / name
    return Trace.from_dict(json.loads(path.read_text()))


def test_healthy_trace_has_no_issues():
    result = analyze_trace(load_sample("healthy.json"))
    assert result.issues == []
    assert result.reliability_score == 100


def test_looping_trace_detects_repetition():
    result = analyze_trace(load_sample("looping.json"))
    assert any(issue.kind == "tool_repetition" for issue in result.issues)
    assert result.reliability_score < 100


def test_retry_storm_detects_failures():
    result = analyze_trace(load_sample("retry_storm.json"))
    assert any(issue.kind == "retry_storm" for issue in result.issues)


def test_context_growth_detection():
    trace = Trace.from_dict(
        {
            "steps": [
                {"step_id": 1, "tokens": 1000, "status": "success"},
                {"step_id": 2, "tokens": 2400, "status": "success"},
                {"step_id": 3, "tokens": 5000, "status": "success"},
            ]
        }
    )
    result = analyze_trace(trace)
    assert any(issue.kind == "context_growth" for issue in result.issues)


def test_missing_steps_defaults_to_empty_trace():
    trace = Trace.from_dict({})
    assert trace.steps == []


def test_invalid_steps_type_raises_clear_error():
    try:
        Trace.from_dict({"steps": "oops"})
    except TraceParseError as exc:
        assert "steps" in str(exc)
    else:
        raise AssertionError("expected TraceParseError")


def test_invalid_step_object_raises_clear_error():
    try:
        Trace.from_dict({"steps": ["oops"]})
    except TraceParseError as exc:
        assert "Step 1" in str(exc)
    else:
        raise AssertionError("expected TraceParseError")


def test_load_trace_accepts_json_array():
    with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=True) as handle:
        json.dump(
            [
                {"step_id": 1, "type": "tool", "name": "search", "tokens": 10, "status": "success"},
                {"step_id": 2, "type": "tool", "name": "answer", "tokens": 20, "status": "success"},
            ],
            handle,
        )
        handle.flush()
        trace = load_trace(Path(handle.name))
    assert len(trace.steps) == 2


def test_load_trace_accepts_jsonl_log_file():
    with tempfile.NamedTemporaryFile("w+", suffix=".log", delete=True) as handle:
        handle.write('{"step_id": 1, "type": "tool", "name": "search", "tokens": 10, "status": "success"}\n')
        handle.write('{"step_id": 2, "type": "tool", "name": "search", "tokens": 10, "status": "success"}\n')
        handle.flush()
        trace = load_trace(Path(handle.name))
    assert len(trace.steps) == 2


def test_load_trace_accepts_noisy_log_lines():
    with tempfile.NamedTemporaryFile("w+", suffix=".log", delete=True) as handle:
        handle.write('2026-06-12T10:00:00Z INFO step={"step_id": 1, "type": "tool", "name": "search", "tokens": 10, "status": "success"}\n')
        handle.write('2026-06-12T10:00:01Z INFO step={"step_id": 2, "type": "tool", "name": "search", "tokens": 10, "status": "success"}\n')
        handle.flush()
        trace = load_trace(Path(handle.name))
    assert len(trace.steps) == 2


def test_load_trace_accepts_large_jsonl_trace():
    with tempfile.NamedTemporaryFile("w+", suffix=".jsonl", delete=True) as handle:
        for i in range(10_000):
            json.dump(
                {
                    "step_id": i + 1,
                    "type": "tool",
                    "name": "search" if i % 2 == 0 else "answer",
                    "tokens": 1,
                    "status": "success",
                },
                handle,
            )
            handle.write("\n")
        handle.flush()
        trace = load_trace(Path(handle.name))
    assert len(trace.steps) == 10_000
