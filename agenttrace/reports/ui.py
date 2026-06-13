from __future__ import annotations

import json
from pathlib import Path


SAMPLE_FILES = {
    "Healthy": "sample_traces/healthy.big.jsonl",
    "Looping": "sample_traces/looping.big.jsonl",
    "Retry Storm": "sample_traces/retry_storm.jsonl",
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
    samples = _load_sample_texts()
    sample_json = json.dumps(samples)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AgentTrace</title>
  <style>
    :root {{
      --bg: #060816;
      --panel: rgba(13, 19, 40, .88);
      --panel-strong: rgba(19, 28, 56, .96);
      --text: #eff3ff;
      --muted: #9aa7ca;
      --accent: #8b5cf6;
      --accent-2: #22d3ee;
      --ok: #34d399;
      --warn: #fbbf24;
      --critical: #fb7185;
      --border: rgba(255,255,255,.1);
      --shadow: 0 28px 80px rgba(0,0,0,.38);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--text);
      background:
        radial-gradient(circle at top left, rgba(139, 92, 246, .24), transparent 28%),
        radial-gradient(circle at top right, rgba(34, 211, 238, .20), transparent 24%),
        linear-gradient(180deg, #0b1022, #060816 48%, #060816);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    .shell {{ max-width: 1220px; margin: 0 auto; padding: 28px 18px 56px; }}
    .hero {{
      position: relative;
      overflow: hidden;
      padding: 28px;
      border: 1px solid var(--border);
      border-radius: 28px;
      background: linear-gradient(180deg, rgba(255,255,255,.07), rgba(255,255,255,.03));
      box-shadow: var(--shadow);
      margin-bottom: 18px;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      inset: auto -20% -50% auto;
      width: 360px;
      height: 360px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(139,92,246,.35), transparent 68%);
      pointer-events: none;
    }}
    .eyebrow {{
      display: inline-flex;
      gap: 8px;
      align-items: center;
      padding: 7px 12px;
      border-radius: 999px;
      background: rgba(255,255,255,.06);
      border: 1px solid var(--border);
      color: var(--muted);
      font-size: .88rem;
      letter-spacing: .02em;
    }}
    h1 {{
      margin: 16px 0 10px;
      font-size: clamp(2.2rem, 7vw, 4.6rem);
      line-height: .95;
      letter-spacing: -.05em;
    }}
    .lede {{
      margin: 0;
      max-width: 78ch;
      color: var(--muted);
      line-height: 1.62;
      font-size: 1.02rem;
    }}
    .actions {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }}
    .button, .ghost {{
      appearance: none;
      border: 0;
      border-radius: 999px;
      padding: 11px 16px;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      transition: transform .15s ease, box-shadow .15s ease, background .15s ease;
    }}
    .button {{
      background: linear-gradient(135deg, var(--accent), var(--accent-2));
      color: #07111f;
      box-shadow: 0 12px 30px rgba(34, 211, 238, .18);
    }}
    .ghost {{
      background: rgba(255,255,255,.05);
      color: var(--text);
      border: 1px solid var(--border);
    }}
    .button:hover, .ghost:hover {{ transform: translateY(-1px); }}
    .layout {{
      display: grid;
      gap: 16px;
      grid-template-columns: repeat(12, 1fr);
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 22px;
      padding: 18px;
      box-shadow: 0 16px 46px rgba(0,0,0,.22);
      backdrop-filter: blur(12px);
    }}
    .upload {{ grid-column: span 12; }}
    .metrics {{ grid-column: span 12; display: grid; gap: 12px; grid-template-columns: repeat(4, minmax(0,1fr)); }}
    .issues {{ grid-column: span 7; }}
    .recs {{ grid-column: span 5; }}
    .preview {{ grid-column: span 12; }}
    .samples {{ grid-column: span 12; }}
    .drop {{
      display: grid;
      gap: 14px;
      place-items: center;
      min-height: 220px;
      text-align: center;
      border-radius: 18px;
      border: 1px dashed rgba(139, 92, 246, .45);
      background: linear-gradient(180deg, rgba(255,255,255,.05), rgba(255,255,255,.03));
    }}
    .drop.drag {{
      border-color: var(--accent-2);
      background: rgba(34, 211, 238, .08);
    }}
    .muted {{ color: var(--muted); }}
    .metric {{
      padding: 16px;
      border-radius: 18px;
      background: var(--panel-strong);
      border: 1px solid var(--border);
    }}
    .metric .label {{ color: var(--muted); font-size: .9rem; }}
    .metric .value {{ font-size: 1.8rem; font-weight: 800; margin-top: 8px; }}
    .metric.good .value {{ color: var(--ok); }}
    .metric.warn .value {{ color: var(--warn); }}
    .metric.bad .value {{ color: var(--critical); }}
    .sample-grid {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .sample-grid button {{
      border: 1px solid var(--border);
      background: rgba(255,255,255,.06);
      color: var(--text);
      border-radius: 999px;
      padding: 10px 14px;
      cursor: pointer;
    }}
    .sample-grid button:hover {{
      background: rgba(255,255,255,.1);
    }}
    input[type=file] {{ display: none; }}
    ul {{ margin: 0; padding-left: 18px; }}
    li {{ margin: 10px 0; }}
    pre {{
      white-space: pre-wrap;
      word-break: break-word;
      overflow-wrap: anywhere;
      margin: 0;
      padding: 16px;
      border-radius: 16px;
      border: 1px solid var(--border);
      background: rgba(0,0,0,.25);
    }}
    .sev-warning {{ color: var(--warn); }}
    .sev-critical {{ color: var(--critical); }}
    .sev-ok {{ color: var(--ok); }}
    @media (max-width: 960px) {{
      .issues, .recs {{ grid-column: span 12; }}
      .metrics {{ grid-template-columns: repeat(2, minmax(0,1fr)); }}
    }}
    @media (max-width: 640px) {{
      .shell {{ padding-inline: 12px; }}
      .hero, .card {{ border-radius: 18px; }}
      .metrics {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="shell">
    <section class="hero">
      <div class="eyebrow">Offline analysis · no LLM calls · local file upload</div>
      <h1>AgentTrace</h1>
      <p class="lede">Upload a trace and see the analysis immediately. The UI reads plain JSON, JSONL, and noisy log files, then shows reliability, waste, issues, and recommendations in one place.</p>
      <div class="actions">
        <label class="button" for="file">Choose a trace</label>
        <a class="ghost" href="#" id="clearLink">Clear results</a>
      </div>
    </section>

    <section class="layout">
      <section class="card upload">
        <div id="drop" class="drop">
          <div>
            <strong>Drop a file here</strong>
            <div class="muted">or pick a `.json`, `.jsonl`, `.log`, or `.txt` trace</div>
            <input id="file" type="file" accept=".json,.jsonl,.log,.txt">
            <div class="muted" id="fileName" style="margin-top: 10px;"></div>
            <div id="status" class="muted" style="margin-top: 8px;"></div>
          </div>
        </div>
      </section>

      <section class="card samples">
        <h2 style="margin-top: 0;">Quick samples</h2>
        <p class="muted">Load one of the bundled examples instantly.</p>
        <div class="sample-grid" id="sampleGrid"></div>
      </section>

      <section class="card metrics">
        <div class="metric good"><div class="label">Reliability</div><div class="value" id="reliability">-</div></div>
        <div class="metric"><div class="label">Total Tokens</div><div class="value" id="totalTokens">-</div></div>
        <div class="metric warn"><div class="label">Estimated Waste</div><div class="value" id="waste">-</div></div>
        <div class="metric"><div class="label">Issues</div><div class="value" id="issueCount">-</div></div>
      </section>

      <section class="card issues">
        <h2 style="margin-top: 0;">Issues found</h2>
        <div id="issues" class="muted">No file loaded yet.</div>
      </section>

      <section class="card recs">
        <h2 style="margin-top: 0;">Recommendations</h2>
        <div id="recommendations" class="muted">No file loaded yet.</div>
      </section>

      <section class="card preview">
        <h2 style="margin-top: 0;">Trace preview</h2>
        <pre id="preview" class="muted">Upload a trace or choose a sample to see the parsed content here.</pre>
      </section>
    </section>
  </main>

  <script>
    const SAMPLE_DATA = {sample_json};
    const fileInput = document.getElementById('file');
    const drop = document.getElementById('drop');
    const statusEl = document.getElementById('status');
    const fileNameEl = document.getElementById('fileName');
    const previewEl = document.getElementById('preview');
    const sampleGrid = document.getElementById('sampleGrid');
    const clearLink = document.getElementById('clearLink');

    function isWhitespace(ch) {{ return /\\s/.test(ch); }}

    function peekFirstNonWhitespace(text) {{
      for (const ch of text) {{
        if (!isWhitespace(ch)) return ch;
      }}
      return null;
    }}

    function parseTraceText(text) {{
      const stripped = text.trim();
      if (!stripped) throw new Error('Trace file is empty.');

      const first = peekFirstNonWhitespace(text);
      if (first === '[') return JSON.parse(text);
      if (first === '{{') {{
        try {{
          return JSON.parse(text);
        }} catch (err) {{
          return parseLogStream(text);
        }}
      }}
      return parseLogStream(text);
    }}

    function parseLogStream(text) {{
      const steps = [];
      const lines = text.split(/\\r?\\n/);
      for (const line of lines) {{
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
      let currentName = null;
      let currentCount = 0;
      function flush() {{
        if (!currentName || currentCount < 3) return;
        issues.push({{
          kind: 'tool_repetition',
          title: 'Tool Repetition Detected',
          severity: currentCount >= 5 ? 'Critical' : 'Warning',
          details: {{ tool: currentName, occurrences: currentCount }},
          recommendation: 'Add result caching or planner confidence thresholds.',
        }});
      }}
      for (const step of steps) {{
        if (step.type !== 'tool' || !step.name) {{
          flush();
          currentName = null;
          currentCount = 0;
          continue;
        }}
        if (step.name === currentName) {{
          currentCount += 1;
        }} else {{
          flush();
          currentName = step.name;
          currentCount = 1;
        }}
      }}
      flush();
      return issues;
    }}

    function detectRetryStorm(steps) {{
      const issues = [];
      let count = 0;
      const spans = [];
      for (const step of steps) {{
        const isFailure = ['error', 'failed', 'failure'].includes(String(step.status || '').toLowerCase());
        if (isFailure) {{
          count += 1;
          continue;
        }}
        if (count >= 3) spans.push(count);
        count = 0;
      }}
      if (count >= 3) spans.push(count);
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
      if (tokenCounts.length < 2) return {{ issues: [], growth: null, avg: null }};
      const initial = tokenCounts[0];
      const final = tokenCounts[tokenCounts.length - 1];
      const growth = initial > 0 ? ((final - initial) / initial) * 100 : null;
      const deltas = [];
      for (let i = 0; i < tokenCounts.length - 1; i++) {{
        const earlier = tokenCounts[i];
        const later = tokenCounts[i + 1];
        if (earlier > 0) deltas.push(((later - earlier) / earlier) * 100);
      }}
      const avg = deltas.length ? deltas.reduce((a, b) => a + b, 0) / deltas.length : null;
      const issues = [];
      if (growth !== null && growth > 100) {{
        issues.push({{
          kind: 'context_growth',
          title: 'Context Explosion Detected',
          severity: growth > 300 ? 'Critical' : 'Warning',
          details: {{
            initial_tokens: initial,
            final_tokens: final,
            peak_tokens: Math.max(...tokenCounts),
            growth_percent: Number(growth.toFixed(2)),
            average_growth_rate: avg === null ? null : Number(avg.toFixed(2)),
          }},
          recommendation: 'Add context summarization or memory compression.',
        }});
      }}
      return {{ issues, growth, avg }};
    }}

    function scoreFromIssues(issues) {{
      let score = 100;
      for (const issue of issues) {{
        if (issue.severity === 'Warning') score -= 12;
        if (issue.severity === 'Critical') score -= 24;
      }}
      return Math.max(0, score);
    }}

    function estimateWaste(issues) {{
      let wasted = 0;
      for (const issue of issues) {{
        if (issue.kind === 'tool_repetition') {{
          wasted += Math.max(0, Number(issue.details.occurrences || 0) - 1) * 100;
        }} else if (issue.kind === 'retry_storm') {{
          wasted += Number(issue.details.failed_attempts || 0) * 150;
        }} else if (issue.kind === 'context_growth') {{
          wasted += Math.max(0, Number(issue.details.final_tokens || 0) - Number(issue.details.initial_tokens || 0));
        }}
      }}
      return Math.max(0, wasted);
    }}

    function escapeHtml(text) {{
      return String(text)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
    }}

    function renderIssues(issues) {{
      if (!issues.length) return '<div class="sev-ok">No major issues detected.</div>';
      return '<ul>' + issues.map(issue =>
        `<li><strong>${{issue.title}}</strong> <span class="sev-${{issue.severity.toLowerCase()}}">(${{issue.severity}})</span><br><span class="muted">${{escapeHtml(JSON.stringify(issue.details))}}</span></li>`
      ).join('') + '</ul>';
    }}

    function renderRecommendations(issues) {{
      const recs = issues.map(issue => issue.recommendation).filter(Boolean);
      if (!recs.length) return '<div class="sev-ok">No recommendations needed.</div>';
      return '<ul>' + recs.map(rec => `<li>${{escapeHtml(rec)}}</li>`).join('') + '</ul>';
    }}

    function updateStats(steps, issues) {{
      const totalTokens = steps.reduce((sum, step) => sum + step.tokens, 0);
      const score = scoreFromIssues(issues);
      const waste = estimateWaste(issues);
      document.getElementById('reliability').textContent = score;
      document.getElementById('reliability').parentElement.className = `metric ${{score >= 90 ? 'good' : score >= 75 ? 'warn' : 'bad'}}`;
      document.getElementById('totalTokens').textContent = totalTokens.toLocaleString();
      document.getElementById('waste').textContent = waste.toLocaleString();
      document.getElementById('issueCount').textContent = issues.length.toLocaleString();
      document.getElementById('issues').innerHTML = renderIssues(issues);
      document.getElementById('recommendations').innerHTML = renderRecommendations(issues);
      previewEl.textContent = JSON.stringify({{ total_steps: steps.length, sample_preview: steps.slice(0, 20) }}, null, 2);
      statusEl.textContent = `Analyzed ${{steps.length.toLocaleString()}} steps.`;
    }}

    async function analyzeText(text, name = 'trace') {{
      fileNameEl.textContent = `Loaded: ${{name}}`;
      statusEl.textContent = 'Reading file...';
      const payload = normalizeTrace(parseTraceText(text));
      const steps = (payload.steps || []).map(toStep);
      const issues = [
        ...detectToolRepetition(steps),
        ...detectRetryStorm(steps),
        ...detectContextGrowth(steps).issues,
      ];
      updateStats(steps, issues);
    }}

    async function handleFile(file) {{
      try {{
        await analyzeText(await file.text(), file.name);
      }} catch (err) {{
        statusEl.textContent = err.message || String(err);
        fileNameEl.textContent = `Loaded: ${{file.name}}`;
      }}
    }}

    fileInput.addEventListener('change', event => {{
      const file = event.target.files && event.target.files[0];
      if (file) {{
        handleFile(file).catch(err => {{
          statusEl.textContent = err.message || String(err);
        }});
      }}
    }});

    drop.addEventListener('dragover', event => {{
      event.preventDefault();
      drop.classList.add('drag');
    }});
    drop.addEventListener('dragleave', () => drop.classList.remove('drag'));
    drop.addEventListener('drop', event => {{
      event.preventDefault();
      drop.classList.remove('drag');
      const file = event.dataTransfer.files && event.dataTransfer.files[0];
      if (file) {{
        handleFile(file).catch(err => {{
          statusEl.textContent = err.message || String(err);
        }});
      }}
    }});

    clearLink.addEventListener('click', event => {{
      event.preventDefault();
      fileInput.value = '';
      fileNameEl.textContent = '';
      statusEl.textContent = 'Ready for a new trace.';
      document.getElementById('reliability').textContent = '-';
      document.getElementById('totalTokens').textContent = '-';
      document.getElementById('waste').textContent = '-';
      document.getElementById('issueCount').textContent = '-';
      document.getElementById('issues').innerHTML = '<div class="muted">No file loaded yet.</div>';
      document.getElementById('recommendations').innerHTML = '<div class="muted">No file loaded yet.</div>';
      previewEl.textContent = 'Upload a trace or choose a sample to see the parsed content here.';
    }});

    for (const [label, text] of Object.entries(SAMPLE_DATA)) {{
      const btn = document.createElement('button');
      btn.textContent = label;
      btn.addEventListener('click', () => analyzeText(text, `${{label}} sample`).catch(err => {{
        statusEl.textContent = err.message || String(err);
      }}));
      sampleGrid.appendChild(btn);
    }}
  </script>
</body>
</html>
"""
