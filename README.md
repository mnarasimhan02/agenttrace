# AgentTrace

AgentTrace is a local analyzer for AI agent execution traces.

It helps builders understand what an agent is doing when a run gets slow, repetitive, or expensive.

## Why It Exists

AI agents are easy to launch and hard to debug.

The trace often shows the problem clearly:

- the same tool gets called again and again
- retries keep failing
- context grows faster than the task does
- tokens are spent without forward progress

AgentTrace turns those patterns into a simple report and browser view, without needing an LLM in the loop.

## What It Finds

- repeated tool calls
- retry storms
- context growth
- estimated token waste
- reliability risk

## Why Not Just Use an LLM?

AgentTrace is built for repeatable trace analysis, not open-ended chat.

- It runs locally and gives the same result for the same trace.
- It focuses on specific failure patterns.
- It produces a structured report and UI that are easy to scan, compare, and share.

An LLM is still useful when you want:

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

## Install

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

## Use It

Analyze a trace:

```bash
agenttrace analyze trace.json
```

Generate an HTML report:

```bash
agenttrace analyze trace.json --html report.html
```

Generate a Markdown report:

```bash
agenttrace analyze trace.json --report report.md
```

Run the browser UI:

```bash
agenttrace ui --serve
```

Or write a standalone HTML file:

```bash
agenttrace ui --output outputs/agenttrace-ui.html
```

## Sample Files

The repo includes larger sample traces in `sample_traces/`:

- `sample_traces/healthy.big.json`
- `sample_traces/looping.big.json`
- `sample_traces/retry_storm.big.json`

Use them to test the main analysis paths:

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

These numbers are a practical reference for local trace analysis.

## Browser UI

The UI is intentionally simple.

It includes:

- one upload button for `.json` trace files
- quick sample buttons for the bundled traces
- reliability and waste summary cards
- issues and recommendations
- a preview of the parsed trace

Preview:

![AgentTrace UI preview](/Users/mnarasimhan/Documents/Codex/2026-06-12/files-mentioned-by-the-user-agenttrace/outputs/agenttrace-ui-preview.png)

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
