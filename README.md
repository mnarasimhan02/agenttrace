# AgentTrace

AgentTrace is an offline analyzer for AI agent execution traces.

It helps you spot common failure patterns in agent runs, including:

- repeated tool calls
- retry storms
- context growth
- estimated token waste
- overall reliability risk

The tool runs locally, requires no LLM calls, and is designed for agent traces captured from frameworks such as OpenAI Agents SDK, LangGraph, CrewAI, AutoGen, or custom workflows.

It can handle long traces, and JSONL or log-style input is usually the best fit for very large runs.

## Why use it

When an agent gets stuck, the symptoms are usually visible in the trace:

- the same tool gets called again and again
- failures keep repeating without recovery
- context keeps growing until the run becomes expensive or unstable
- tokens are burned without progress

AgentTrace turns those symptoms into a readable report with a reliability score and suggested fixes.

## Installation

### Option 1: Install from source

```bash
git clone <your-repo-url>
cd agenttrace
pip install -e .
```

### Option 2: Install into an existing environment

```bash
pip install -e /path/to/agenttrace
```

### Requirements

- Python 3.11 or newer
- No API keys
- No network access required after installation

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

To open the browser UI:

```bash
agenttrace ui --serve
```

Or generate a standalone HTML file:

```bash
agenttrace ui --output agenttrace-ui.html
```

## Included Sample Files

The repository includes sample traces in `sample_traces/` so you can try the tool immediately.

The examples are intentionally sized to feel more like real traces, not just toy fixtures.

### `sample_traces/healthy.json`

A simple trace with normal progression and no major issues.

Use it to see the baseline output:

```bash
agenttrace analyze sample_traces/healthy.json
```

Expected result:

- reliability score stays high
- no issues are reported
- estimated waste is near zero

You can also run the JSONL version:

```bash
agenttrace analyze sample_traces/healthy.jsonl
```

### `sample_traces/looping.json`

A trace that repeats the same tool many times.

Use it to verify tool repetition detection:

```bash
agenttrace analyze sample_traces/looping.json
```

Expected result:

- tool repetition is flagged
- the reliability score drops
- waste is estimated from repeated calls

You can also run the JSONL version:

```bash
agenttrace analyze sample_traces/looping.jsonl
```

### `sample_traces/retry_storm.json`

A trace with repeated failures and retries.

Use it to verify retry storm detection:

```bash
agenttrace analyze sample_traces/retry_storm.json
```

Expected result:

- retry storm is flagged
- severity increases with repeated failures
- waste is estimated from failed attempts

You can also run the JSONL version:

```bash
agenttrace analyze sample_traces/retry_storm.jsonl
```

### Larger samples

If you want to try longer files right away, use these bigger examples:

- `sample_traces/healthy.big.jsonl`
- `sample_traces/looping.big.jsonl`

They are still easy to read, but they better reflect the kind of input AgentTrace is meant to handle in practice.

The browser UI also includes quick-load buttons for these bundled samples.

## Browser UI

The interactive UI lets you upload a trace directly in the browser and review the analysis in place.

It includes:

- file upload and drag-and-drop
- quick sample buttons
- reliability and waste summary cards
- issues and recommendations panels
- a preview of the parsed trace

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
agenttrace ui --output agenttrace-ui.html
```

## Input Format

AgentTrace automatically detects the input format.

Recommended format:

- JSON object with a `steps` array

It can also read:

- a JSON array of step objects
- JSONL-style log files with one JSON step per line
- log files with extra text around embedded JSON objects
- large traces with thousands of steps

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

### Log files

If your agent writes trace entries to a `.log`, `.txt`, or `.jsonl` file, AgentTrace can still read it as long as each line is valid JSON.

Example JSONL trace:

```text
{"step_id": 1, "type": "tool", "name": "search", "tokens": 200, "status": "success"}
{"step_id": 2, "type": "tool", "name": "summarize", "tokens": 120, "status": "success"}
{"step_id": 3, "type": "tool", "name": "answer", "tokens": 80, "status": "success"}
```

If the log line contains extra text around the JSON object, AgentTrace will try to extract the JSON portion first.

For very large traces, JSONL is the safest format because AgentTrace can process it line by line without needing to reshape the whole file first.

## Sample Log Files

The repository also includes JSONL-formatted log examples:

- `sample_traces/healthy.jsonl`
- `sample_traces/looping.jsonl`
- `sample_traces/retry_storm.jsonl`

Try them like this:

```bash
agenttrace analyze sample_traces/healthy.jsonl
agenttrace analyze sample_traces/looping.jsonl
agenttrace analyze sample_traces/retry_storm.jsonl
```

## Large Traces

For long production runs, prefer `.jsonl` or `.log` files with one JSON object per line.

That format is the most convenient for:

- huge traces
- live logs
- partial exports
- traces that are written incrementally

Plain JSON files are still supported, but JSONL is generally the most robust option when traces get large.

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
agenttrace analyze sample_traces/healthy.json
```

Analyze a looping trace and write a Markdown report:

```bash
agenttrace analyze sample_traces/looping.json --report report.md
```

Analyze a retry storm trace and write HTML output:

```bash
agenttrace analyze sample_traces/retry_storm.json --html report.html
```

## Project Structure

```text
agenttrace/
├── app.py
├── analyzer.py
├── detectors/
├── models/
├── reports/
sample_traces/
tests/
README.md
pyproject.toml
```

## Development

Run the code formatter or tests from your local environment as needed.

If you want to verify the package manually, these commands are a good starting point:

```bash
python -m agenttrace analyze sample_traces/healthy.json
python -m agenttrace analyze sample_traces/looping.json --report report.md
python -m agenttrace analyze sample_traces/retry_storm.json --html report.html
```

## Roadmap

Planned future enhancements include:

- support for additional trace formats
- agent comparison mode
- execution graph visualization
- optional LLM-powered explanations
- interactive dashboards

## License

Add your preferred open-source license before publishing the repository.
