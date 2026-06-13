from __future__ import annotations

import json
from pathlib import Path


SAMPLE_FILES = {
    "Healthy": "sample_traces/healthy.big.jsonl",
    "Looping": "sample_traces/looping.big.jsonl",
    "Retry Storm": "sample_traces/retry_storm.big.jsonl",
}


def _load_sample_texts() -> dict[str, str]:
    root = Path(__file__).resolve().parents[2]
    samples: dict[str, str] = {}
    for label, relpath in SAMPLE_FILES.items():
        path = root / relpath
        if path.exists():
            samples[label] = path.read_text(encoding="utf-8")
    return samples


def render_ui_html() -> str:
    sample_json = json.dumps(_load_sample_texts())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AgentTrace</title>
  <style>
    :root {{
      --bg: #07111f;
      --panel: #0f1a30;
      --panel-soft: #15213c;
      --text: #eef2ff;
      --muted: #9aa7c6;
      --accent: #60a5fa;
      --good: #34d399;
      --warn: #fbbf24;
      --critical: #fb7185;
      --border: rgba(255,255,255,.10);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: linear-gradient(180deg, #0b1530, var(--bg));
      color: var(--text);
    }}
    .wrap {{ max-width: 1080px; margin: 0 auto; padding: 28px 18px 56px; }}
    .hero {{
      padding: 28px;
      border: 1px solid var(--border);
      border-radius: 24px;
      background: linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
      margin-bottom: 16px;
    }}
    h1 {{ margin: 0 0 10px; font-size: clamp(2rem, 5vw, 3.4rem); letter-spacing: -.04em; }}
    .lede {{ margin: 0; color: var(--muted); max-width: 70ch; line-height: 1.6; }}
    .card {{
      background: rgba(15, 26, 48, .94);
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 18px;
      margin-top: 16px;
      box-shadow: 0 14px 40px rgba(0,0,0,.20);
    }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }}
    .button {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 0;
      border-radius: 999px;
      padding: 11px 16px;
      font-weight: 700;
      cursor: pointer;
      background: linear-gradient(135deg, var(--accent), #22d3ee);
      color: #03101f;
    }}
    .sample {{
      border: 1px solid var(--border);
      background: rgba(255,255,255,.06);
      color: var(--text);
      border-radius: 999px;
      padding: 10px 14px;
      cursor: pointer;
    }}
    .sample:hover {{ background: rgba(255,255,255,.1); }}
    .muted {{ color: var(--muted); }}
    input[type=file] {{ display: none; }}
    .grid {{
      display: grid;
      gap: 12px;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      margin-top: 16px;
    }}
    .metric {{
      padding: 16px;
      border-radius: 16px;
      background: var(--panel-soft);
      border: 1px solid var(--border);
    }}
    .metric .label {{ color: var(--muted); font-size: .9rem; }}
    .metric .value {{ font-size: 1.8rem; font-weight: 800; margin-top: 8px; }}
    .metric.good .value {{ color: var(--good); }}
    .metric.warn .value {{ color: var(--warn); }}
    .metric.bad .value {{ color: var(--critical); }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin: 8px 0; }}
    pre {{
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      margin: 0;
      padding: 14px;
      border-radius: 14px;
      background: rgba(0,0,0,.22);
      border: 1px solid var(--border);
    }}
    .two-col {{
      display: grid;
      gap: 16px;
      grid-template-columns: 7fr 5fr;
    }}
    .section-title {{ margin-top: 0; }}
    @media (max-width: 900px) {{
      .grid, .two-col {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="hero">
      <h1>AgentTrace</h1>
      <p class="lede">Upload a trace or use one of the bundled examples. The page reads JSON, JSONL, and log-style files, then shows a compact analysis right away.</p>
    </section>

    <section class="card">
      <h2 class="section-title">Open a trace</h2>
      <div class="controls">
        <label class="button" for="file">Choose File</label>
        <input id="file" type="file" accept=".json,.jsonl,.log,.txt">
        <span class="muted">or pick a sample:</span>
        <button class="sample" data-sample="Healthy">Healthy</button>
        <button class="sample" data-sample="Looping">Looping</button>
        <button class="sample" data-sample="Retry Storm">Retry Storm</button>
      </div>
      <p id="fileName" class="muted" style="margin: 12px 0 0;"></p>
      <p id="status" class="muted"></p>
    </section>

    <section class="grid">
      <div class="metric good"><div class="label">Reliability</div><div class="value" id="reliability">-</div></div>
      <div class="metric"><div class="label">Total Tokens</div><div class="value" id="totalTokens">-</div></div>
      <div class="metric warn"><div class="label">Estimated Waste</div><div class="value" id="waste">-</div></div>
      <div class="metric"><div class="label">Issues</div><div class="value" id="issueCount">-</div></div>
    </section>

    <section class="two-col">
      <div class="card">
        <h2 class="section-title">Issues</h2>
        <div id="issues" class="muted">No trace loaded yet.</div>
      </div>
      <div class="card">
        <h2 class="section-title">Recommendations</h2>
        <div id="recommendations" class="muted">No trace loaded yet.</div>
      </div>
    </section>

    <section class="card">
      <h2 class="section-title">Preview</h2>
      <pre id="preview" class="muted">Choose a sample or upload a trace to see a preview here.</pre>
    </section>
  </main>

  <script>
    const SAMPLE_DATA = {sample_json};
    const fileInput = document.getElementById('file');
    const fileNameEl = document.getElementById('fileName');
    const statusEl = document.getElementById('status');
    const previewEl = document.getElementById('preview');

    function parseTraceText(text) {{
      const stripped = text.trim();
      if (!stripped) throw new Error('Trace file is empty.');
      if (stripped.startsWith('[')) return JSON.parse(text);
      if (stripped.startsWith('{{')) {{
        try {{
          return JSON.parse(text);
        }} catch (err) {{
          return parseJsonLines(text);
        }}
      }}
      return parseJsonLines(text);
    }}

    function parseJsonLines(text) {{
      const steps = [];
      for (const line of text.split(/\\r?\\n/)) {{
        const trimmed = line.trim();
        if (!trimmed) continue;
        try {{
          steps.push(JSON.parse(trimmed));
          continue;
        }} catch (err) {{
          const match = trimmed.match(/\\{{.*\\}}/);
          if (match) {{
            steps.push(JSON.parse(match[0]));
            continue;
          }}
          throw new Error('Unable to parse a log line as JSON.');
        }}
      }}
      if (!steps.length) throw new Error('No usable JSON records found.');
      return {{ steps }};
    }}

    function normalizeTrace(payload) {{
      if (Array.isArray(payload)) return {{ steps: payload }};
      return payload && typeof payload === 'object' ? payload : {{ steps: [] }};
    }}

    function toStep(step, index) {{
      return {{
        step_id: Number.isInteger(step.step_id) ? step.step_id : index + 1,
        type: typeof step.type === 'string' ? step.type : 'tool',
        name: typeof step.name === 'string' ? step.name : null,
        tokens: Math.max(Number(step.tokens || 0) || 0, 0),
        status: typeof step.status === 'string' ? step.status : null,
      }};
    }}

    function detectToolRepetition(steps) {{
      const issues = [];
      let current = null;
      let count = 0;
      function flush() {{
        if (!current || count < 3) return;
        issues.push({{
          kind: 'tool_repetition',
          title: 'Tool Repetition Detected',
          severity: count >= 5 ? 'Critical' : 'Warning',
          details: {{ tool: current, occurrences: count }},
          recommendation: 'Add result caching or planner confidence thresholds.',
        }});
      }}
      for (const step of steps) {{
        if (step.type !== 'tool' || !step.name) {{
          flush();
          current = null;
          count = 0;
          continue;
        }}
        if (step.name === current) count += 1; else {{
          flush();
          current = step.name;
          count = 1;
        }}
      }}
      flush();
      return issues;
    }}

    function detectRetryStorm(steps) {{
      const issues = [];
      let failures = 0;
      const spans = [];
      for (const step of steps) {{
        const isFailure = ['error', 'failed', 'failure'].includes(String(step.status || '').toLowerCase());
        if (isFailure) {{
          failures += 1;
          continue;
        }}
        if (failures >= 3) spans.push(failures);
        failures = 0;
      }}
      if (failures >= 3) spans.push(failures);
      for (const span of spans) {{
        issues.push({{
          kind: 'retry_storm',
          title: 'Retry Storm Detected',
          severity: span >= 5 ? 'Critical' : 'Warning',
          details: {{ failed_attempts: span, span_type: 'consecutive_failures' }},
          recommendation: 'Implement retry limits and fallback logic.',
        }});
      }}
      return issues;
    }}

    function detectContextGrowth(steps) {{
      const tokenCounts = steps.map(step => step.tokens);
      if (tokenCounts.length < 2) return [];
      const initial = tokenCounts[0];
      const final = tokenCounts[tokenCounts.length - 1];
      const growth = initial > 0 ? ((final - initial) / initial) * 100 : null;
      if (growth === null || growth <= 100) return [];
      const avg = tokenCounts.slice(1).reduce((sum, val, idx) => {{
        const prev = tokenCounts[idx];
        return prev > 0 ? sum + ((val - prev) / prev) * 100 : sum;
      }}, 0) / Math.max(1, tokenCounts.length - 1);
      return [{{
        kind: 'context_growth',
        title: 'Context Explosion Detected',
        severity: growth > 300 ? 'Critical' : 'Warning',
        details: {{
          initial_tokens: initial,
          final_tokens: final,
          peak_tokens: Math.max(...tokenCounts),
          growth_percent: Number(growth.toFixed(2)),
          average_growth_rate: Number(avg.toFixed(2)),
        }},
        recommendation: 'Add context summarization or memory compression.',
      }}];
    }}

    function score(issues) {{
      let value = 100;
      for (const issue of issues) {{
        value -= issue.severity === 'Critical' ? 24 : 12;
      }}
      return Math.max(0, value);
    }}

    function waste(issues) {{
      let total = 0;
      for (const issue of issues) {{
        if (issue.kind === 'tool_repetition') total += Math.max(0, Number(issue.details.occurrences || 0) - 1) * 100;
        if (issue.kind === 'retry_storm') total += Number(issue.details.failed_attempts || 0) * 150;
        if (issue.kind === 'context_growth') total += Math.max(0, Number(issue.details.final_tokens || 0) - Number(issue.details.initial_tokens || 0));
      }}
      return Math.max(0, total);
    }}

    function renderIssues(issues) {{
      if (!issues.length) return '<div class="muted">No major issues detected.</div>';
      return '<ul>' + issues.map(issue => `<li><strong>${{issue.title}}</strong> <span>(${{issue.severity}})</span><br><span class="muted">${{JSON.stringify(issue.details)}}</span></li>`).join('') + '</ul>';
    }}

    function renderRecommendations(issues) {{
      const recs = issues.map(issue => issue.recommendation).filter(Boolean);
      if (!recs.length) return '<div class="muted">No recommendations needed.</div>';
      return '<ul>' + recs.map(rec => `<li>${{rec}}</li>`).join('') + '</ul>';
    }}

    function updateUI(steps, issues, name) {{
      const totalTokens = steps.reduce((sum, step) => sum + step.tokens, 0);
      document.getElementById('reliability').textContent = score(issues);
      document.getElementById('totalTokens').textContent = totalTokens.toLocaleString();
      document.getElementById('waste').textContent = waste(issues).toLocaleString();
      document.getElementById('issueCount').textContent = issues.length.toLocaleString();
      document.getElementById('issues').innerHTML = renderIssues(issues);
      document.getElementById('recommendations').innerHTML = renderRecommendations(issues);
      previewEl.textContent = JSON.stringify({{ total_steps: steps.length, preview: steps.slice(0, 20) }}, null, 2);
      fileNameEl.textContent = name ? `Loaded: ${{name}}` : '';
      statusEl.textContent = `Analyzed ${{steps.length.toLocaleString()}} steps.`;
    }}

    async function analyzeText(text, name) {{
      const payload = normalizeTrace(parseTraceText(text));
      const steps = (payload.steps || []).map(toStep);
      const issues = [...detectToolRepetition(steps), ...detectRetryStorm(steps), ...detectContextGrowth(steps)];
      updateUI(steps, issues, name);
    }}

    fileInput.addEventListener('change', async event => {{
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      try {{
        await analyzeText(await file.text(), file.name);
      }} catch (err) {{
        fileNameEl.textContent = `Loaded: ${{file.name}}`;
        statusEl.textContent = err.message || String(err);
      }}
    }});

    for (const button of document.querySelectorAll('.sample')) {{
      button.addEventListener('click', () => {{
        const name = button.getAttribute('data-sample');
        const text = SAMPLE_DATA[name];
        if (!text) {{
          statusEl.textContent = 'Sample not found.';
          return;
        }}
        analyzeText(text, `${{name}} sample`).catch(err => {{
          statusEl.textContent = err.message || String(err);
        }});
      }});
    }}
  </script>
</body>
</html>
"""
