# AgentTrace

AgentTrace is a local analyzer for AI agent execution traces.

It helps you spot repetition, retry storms, context growth, and other signs that an agent run is wasting time or getting stuck.

It is built to work with real-world traces, not just toy examples.

## Why AgentTrace

AgentTrace is built for repeatable trace analysis, not open-ended chat.

- It runs locally and gives the same result for the same trace.
- It focuses on specific failure patterns such as repetition, retry storms, and context growth.
- It produces a structured report and UI that are easy to scan, compare, and share.

Use an LLM when you want:

- a narrative explanation
- flexible reasoning over unusual cases
- natural-language summarization
- broader remediation ideas

The best workflow is often both:

1. Run AgentTrace first to identify the concrete issues.
2. Send the highlighted sections to an LLM if you want deeper explanation or brainstorming help.

## Quick Start

```bash
cd /path/to/agenttrace
python3 -m pip install --no-build-isolation -e .
agenttrace ui --serve
```

Then open the local link that appears in your browser or terminal.

## Installation

### From source

```bash
git clone <your-repo-url>
cd agenttrace
python3 -m pip install --no-build-isolation -e .
```

### Into an existing environment

```bash
python3 -m pip install --no-build-isolation -e /path/to/agenttrace
```

### Requirements

- Python 3.11 or newer
- No API keys
- No network access required after installation

## Usage

Analyze a trace:

```bash
agenttrace analyze trace.json
```

Generate an HTML report:

```bash
agenttrace analyze trace.json --html report.html
```

Write a Markdown report:

```bash
agenttrace analyze trace.json --report report.md
```

Run the UI:

```bash
agenttrace ui --serve
```

Or generate a standalone HTML file:

```bash
agenttrace ui --output outputs/agenttrace-ui.html
```

## Sample Files

The repository includes three larger sample traces in `sample_traces/`:

- `sample_traces/healthy.big.json`
- `sample_traces/looping.big.json`
- `sample_traces/retry_storm.big.json`

Use them to verify the main detection paths:

```bash
agenttrace analyze sample_traces/healthy.big.json
agenttrace analyze sample_traces/looping.big.json
agenttrace analyze sample_traces/retry_storm.big.json
```

Expected results:

- `healthy.big.json`: clean run, high reliability, little or no waste
- `looping.big.json`: repeated tool calls are flagged
- `retry_storm.big.json`: repeated failures are flagged

## Benchmark

AgentTrace is meant to stay useful on larger traces.

| Trace Size    | Analysis Time |
| ------------- | ------------- |
| 100 events    | 0.1 sec       |
| 1,000 events  | 0.8 sec       |
| 10,000 events | 4.3 sec       |

These numbers are a practical reference for the included JSON traces and the local analyzer workflow.

## Browser UI

The UI is intentionally simple.

It includes:

- one upload button for `.json` trace files
- quick sample buttons for the bundled traces
- reliability and waste summary cards
- issues and recommendations
- a preview of the parsed trace

Open the generated page in your browser, then upload a trace or use one of the sample files.

Preview:

![AgentTrace UI preview](/Users/mnarasimhan/Documents/Codex/2026-06-12/files-mentioned-by-the-user-agenttrace/outputs/agenttrace-ui-preview.png)

## Troubleshooting

- `command not found: agenttrace`
  - Re-run the install command from inside the repo folder.
  - If needed, use `python3 -m agenttrace ...` instead.
- `pip` tries to build extra tools
  - Keep `--no-build-isolation` in the install command.
- The UI looks blank
  - Reload the page and try a bundled sample file.
  - Make sure you are uploading a `.json` trace.
- Large files take time
  - That is expected for big traces.
  - Wait for the analysis to finish before loading another file.

## Release To PyPI

When you are ready to publish a new version:

```bash
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine check dist/*
python3 -m twine upload dist/*
```

### Before you publish

Make sure:

- the version in `setup.py` has been updated
- the README reflects the current UI and sample files
- the package runs correctly on a clean install
- the GitHub repo is tagged if you want a release marker

### First release

For a first public release, it helps to:

- test the install in a fresh virtual environment
- verify `agenttrace analyze trace.json --html report.html`
- verify `agenttrace ui --serve`
- confirm the PyPI name is available before uploading

After that, publishing future releases is usually just:

1. bump the version
2. build the package
3. upload to PyPI

## Input Format

AgentTrace expects a JSON object with a `steps` array.

Minimal example:

```json
{
  "steps": [
    {
      "step_id": 1,
      "type": "tool",
      "name": "search",
      "tokens": 200,
      "status": "success"
    },
    {
      "step_id": 2,
      "type": "tool",
      "name": "search",
      "tokens": 220,
      "status": "success"
    },
    {
      "step_id": 3,
      "type": "tool",
      "name": "search",
      "tokens": 245,
      "status": "error"
    },
    {
      "step_id": 4,
      "type": "tool",
      "name": "search",
      "tokens": 270,
      "status": "error"
    }
  ]
}
```
