from __future__ import annotations

import argparse
import json
import re
import threading
import webbrowser
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from agenttrace.analyzer import analyze_trace
from agenttrace.models.trace import Trace, TraceParseError
from agenttrace.reports.html import render_html_report
from agenttrace.reports.markdown import render_markdown_report
from agenttrace.reports.ui import render_ui_html


def load_trace(path: Path) -> Trace:
    try:
        with path.open("r", encoding="utf-8") as handle:
            first_non_whitespace = _peek_first_non_whitespace(handle)
            handle.seek(0)
            if first_non_whitespace == "[":
                payload = json.load(handle)
                return Trace.from_steps(payload)
            if first_non_whitespace == "{":
                try:
                    payload = json.load(handle)
                    return Trace.from_dict(payload)
                except json.JSONDecodeError:
                    handle.seek(0)
                    payload = _parse_log_stream(handle, path)
            else:
                payload = _parse_log_stream(handle, path)
    except OSError as exc:
        raise ValueError(f"Unable to read {path}: {exc.strerror}") from exc

    try:
        return Trace.from_dict(payload)
    except TraceParseError as exc:
        raise ValueError(str(exc)) from exc


def _peek_first_non_whitespace(handle) -> str | None:
    while True:
        chunk = handle.read(4096)
        if not chunk:
            return None
        for char in chunk:
            if not char.isspace():
                return char


def _parse_log_stream(handle, path: Path) -> dict[str, object]:
    steps: list[object] = []
    json_candidate_pattern = re.compile(r"\{.*\}")
    saw_content = False
    for line_number, line in enumerate(handle, start=1):
        line = line.strip()
        if not line:
            continue
        saw_content = True
        try:
            steps.append(json.loads(line))
        except json.JSONDecodeError as exc:
            candidate = json_candidate_pattern.search(line)
            if candidate:
                try:
                    steps.append(json.loads(candidate.group(0)))
                    continue
                except json.JSONDecodeError:
                    pass
            raise ValueError(
                f"Unable to parse {path} as JSON or JSONL; line {line_number} is not valid JSON: {exc.msg}"
            ) from exc
    if not steps:
        if saw_content:
            raise ValueError(f"Unable to parse trace file {path}: no usable JSON records found.")
        raise ValueError(f"Trace file is empty: {path}")
    return {"steps": steps}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agenttrace", description="Analyze agent execution traces offline.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a trace file.")
    analyze_parser.add_argument("trace", type=Path)
    analyze_parser.add_argument("--report", type=Path, help="Write a markdown report.")
    analyze_parser.add_argument("--html", type=Path, help="Write an HTML report.")
    ui_parser = subparsers.add_parser("ui", help="Write a standalone interactive HTML UI.")
    ui_parser.add_argument("--output", type=Path, default=Path("agenttrace-ui.html"), help="HTML output file.")
    ui_parser.add_argument("--serve", action="store_true", help="Serve the UI on a local web server.")
    ui_parser.add_argument("--host", default="127.0.0.1", help="Host to bind when serving the UI.")
    ui_parser.add_argument("--port", type=int, default=8765, help="Port to bind when serving the UI.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "analyze":
        if args.command == "ui":
            if args.serve:
                _serve_ui(args.host, args.port)
            else:
                args.output.write_text(render_ui_html())
                print(f"Wrote interactive UI to {args.output}")
            return 0
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


def _serve_ui(host: str, port: int) -> None:
    html = render_ui_html().encode("utf-8")

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            if self.path not in {"/", "/index.html"}:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html)))
            self.end_headers()
            self.wfile.write(html)

        def log_message(self, format, *args):  # noqa: A003
            return

    server = ThreadingHTTPServer((host, port), Handler)
    url = f"http://{host}:{port}"
    print(f"Serving AgentTrace UI at {url}")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping AgentTrace UI server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
