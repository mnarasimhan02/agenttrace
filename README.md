# AgentTrace

AgentTrace is an offline analyzer for AI agent execution traces.

It reads a trace file, looks for failure patterns, and shows where an agent may be wasting time or repeating itself.

## Start Here

If you just want to try it quickly:

```bash
cd /path/to/agenttrace
python3 -m pip install --no-build-isolation -e .
agenttrace ui --serve
```

Then open the local link that appears in your browser or terminal.

It helps you spot common failure patterns in agent runs, including:

- repeated tool calls
- retry storms
- context growth
- estimated token waste
- overall reliability risk

The tool runs locally, requires no LLM calls, and is designed for agent traces captured from frameworks such as OpenAI Agents SDK, LangGraph, CrewAI, AutoGen, or custom workflows.

It can handle long traces, and plain JSON files are the simplest way to use it.

## Why use it

When an agent gets stuck, the symptoms are usually visible in the trace:

- the same tool gets called again and again
- failures keep repeating without recovery
- context keeps growing until the run becomes expensive or unstable
- tokens are burned without progress

AgentTrace turns those symptoms into a readable report with a reliability score and suggested fixes.

## Installation

### Install from source

```bash
git clone <your-repo-url>
cd agenttrace
python3 -m pip install --no-build-isolation -e .
```

### Install into an existing environment

```bash
python3 -m pip install --no-build-isolation -e /path/to/agenttrace
```

### Requirements

- Python 3.11 or newer
- No API keys
- No network access required after installation
- If `pip install -e .` tries to fetch build tools, add `--no-build-isolation`

## Quick Start

Run the analyzer on a trace file:

```bash
agenttrace analyze trace.json
```

Generate a Markdown report:

```bash
agenttrace analyze trace.json --report report.md
```

Generate an HTML report:

```bash
agenttrace analyze trace.json --html report.html
```

Generate both at once:

```bash
agenttrace analyze trace.json --report report.md --html report.html
```

You can also run it as a module:

```bash
python -m agenttrace analyze trace.json
```

If you want to test without installing first, this works too:

```bash
PYTHONPATH=. python3 -m agenttrace analyze sample_traces/healthy.big.json
```

To open the browser UI:

```bash
agenttrace ui --serve
```

Or generate a standalone HTML file:

```bash
agenttrace ui --output outputs/agenttrace-ui.html
```

## Included Sample Files

The repository includes sample traces in `sample_traces/` so you can try the tool immediately.

The examples are intentionally sized to feel more like real traces, not just toy fixtures.

### `sample_traces/healthy.big.json`

Use the larger JSON sample instead:

```bash
agenttrace analyze sample_traces/healthy.big.json
```

Expected result:

- reliability score stays high
- no issues are reported
- estimated waste is near zero
- the UI should show a clean run with no major warnings

### `sample_traces/looping.big.json`

Use it to verify tool repetition detection:

```bash
agenttrace analyze sample_traces/looping.big.json
```

Expected result:

- tool repetition is flagged
- the reliability score drops
- waste is estimated from repeated calls
- the UI should show repeated-tool warnings

### `sample_traces/retry_storm.big.json`

Use it to verify retry storm detection:

```bash
agenttrace analyze sample_traces/retry_storm.big.json
```

Expected result:

- retry storm is flagged
- severity increases with repeated failures
- waste is estimated from failed attempts
- the UI should show retry-related warnings

### Larger samples

If you want to try longer files right away, use these bigger examples:

- `sample_traces/healthy.big.json`
- `sample_traces/looping.big.json`
- `sample_traces/retry_storm.big.json`

These are much larger files, closer to the kind of trace data AgentTrace is meant to handle in practice.

The browser UI includes quick-load buttons for these bundled samples.

## Browser UI

The interactive UI is intentionally simple and uses a single page layout.

It includes:

- one upload button for `.json` trace files
- three quick sample buttons for the bundled traces
- a summary of reliability and waste
- detected issues and recommendations
- a preview of the parsed trace data

When you run the UI locally, open the generated page in your browser and upload a sample or your own trace file.

### Local server mode

Run this when you want the UI to open on `localhost`:

```bash
agenttrace ui --serve
```

By default the server uses:

- host: `127.0.0.1`
- port: `8765`

You can override them:

```bash
agenttrace ui --serve --host 0.0.0.0 --port 9000
```

### Static HTML mode

If you just want a file you can keep or share locally:

```bash
agenttrace ui --output outputs/agenttrace-ui.html
```

## Input Format

AgentTrace expects a JSON object with a `steps` array.

Recommended format:

- JSON object with a `steps` array

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
    }
  ]
}
```

### Supported fields

- `step_id`: optional numeric step identifier
- `type`: step type, such as `tool`
- `name`: tool or step name
- `tokens`: token count for the step
- `status`: execution result such as `success` or `error`

### Missing fields

Missing fields are handled gracefully:

- `steps` defaults to an empty list
- missing `name` values do not crash the analyzer
- missing `tokens` values default to `0`
- missing `status` values are treated as non-failures

## Output

The CLI prints a compact summary to the terminal and can optionally write reports to disk.

Terminal output includes:

- reliability score
- estimated waste
- detected issues

### Markdown report

The Markdown report includes:

- summary
- reliability score
- issues found
- token analysis
- recommendations

### HTML report

The HTML report is meant for quick sharing or browser viewing and includes:

- reliability score
- issue summary
- token statistics
- recommendations

## Detection Rules

### Tool repetition

- Warning: 3 or more consecutive calls to the same tool
- Critical: 5 or more consecutive calls to the same tool

### Retry storms

- Warning: 3 or more consecutive failures
- Critical: 5 or more consecutive failures

### Context growth

- Warning: growth above 100%
- Critical: growth above 300%

## Example Commands

Analyze a healthy trace:

```bash
agenttrace analyze sample_traces/healthy.big.json
```

Analyze a looping trace and write a Markdown report:

```bash
agenttrace analyze sample_traces/looping.big.json --report report.md
```

Analyze a retry storm trace and write HTML output:

```bash
agenttrace analyze sample_traces/retry_storm.big.json --html report.html
```

## Project Structure

```text
agenttrace/
├── app.py
├── analyzer.py
├── __main__.py
├── __init__.py
sample_traces/
tests/
outputs/
README.md
setup.py
pytest.ini
```

## Development

Run the code formatter or tests from your local environment as needed.

If you want to verify the package manually, these commands are a good starting point:

```bash
python -m agenttrace analyze sample_traces/healthy.big.json
python -m agenttrace analyze sample_traces/looping.big.json --report report.md
python -m agenttrace analyze sample_traces/retry_storm.big.json --html report.html
```

## Troubleshooting

If something does not work, these are the most common fixes:

- `command not found: agenttrace`
  - Re-run the install command from inside the repo folder.
  - If needed, use `python3 -m agenttrace ...` instead of `agenttrace ...`.
- `pip` tries to build extra tools
  - Use `--no-build-isolation` exactly as shown in the install commands.
- The UI opens but looks empty
  - Reload the page and try one of the bundled sample files.
  - Make sure you are uploading a `.json` trace file.
- The file is large and slow to load
  - That is expected for big traces.
  - Wait for the analysis to finish before opening another file.

## Roadmap

Planned future enhancements include:

- support for additional trace formats
- agent comparison mode
- execution graph visualization
- optional LLM-powered explanations
- interactive dashboards

## License

Add your preferred open-source license before publishing the repository.
