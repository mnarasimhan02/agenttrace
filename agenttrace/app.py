from __future__ import annotations

import argparse
import json
from pathlib import Path

from agenttrace.analyzer import analyze_trace
from agenttrace.models.trace import Trace, TraceParseError
from agenttrace.reports.html import render_html_report
from agenttrace.reports.markdown import render_markdown_report


def load_trace(path: Path) -> Trace:
    try:
        payload = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc.msg}") from exc
    except OSError as exc:
        raise ValueError(f"Unable to read {path}: {exc.strerror}") from exc
    try:
        return Trace.from_dict(payload)
    except TraceParseError as exc:
        raise ValueError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agenttrace", description="Analyze agent execution traces offline.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a trace file.")
    analyze_parser.add_argument("trace", type=Path)
    analyze_parser.add_argument("--report", type=Path, help="Write a markdown report.")
    analyze_parser.add_argument("--html", type=Path, help="Write an HTML report.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "analyze":
        parser.error("Unknown command")

    result = analyze_trace(load_trace(args.trace))
    print(f"Reliability Score: {result.reliability_score}")
    print(f"Estimated Waste: {result.wasted_tokens}")
    for issue in result.issues:
        print(f"{issue.title} [{issue.severity}] {issue.details}")

    if args.report:
        args.report.write_text(render_markdown_report(result))
    if args.html:
        args.html.write_text(render_html_report(result))
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
