"""Look only: colours, CSS and the HTML for loaders and result cards.
No business logic here. app.py imports these helpers."""
import html

# ---------- Brand colours (Kleinanzeigen-inspired) ----------
BRAND_DARK = "#1D4B00"    # Kleinanzeigen dark green
BRAND_LIME = "#B5E31F"    # bright green accent, change here if you have the official value
BRAND_SOFT = "#F3F9E6"    # very light green background
INK = "#1F2A1A"           # text colour
MUTED = "#5F6B57"         # secondary text

# ---------- Loader steps: emoji, title, subtitle, colour, seconds (total about 30 s) ----------
PHASES = [
    ("Research", [
        ("🌐", "Tavily", "How others solve it", "#0EA5E9", 2.5),
        ("📰", "GNews", "Latest AI news", "#F97316", 2.5),
        ("🎓", "OpenAlex", "Research papers", "#8B5CF6", 2.5),
    ]),
    ("Internal documents", [
        ("📘", "AI Policy", "Rules G, A, R", "#1D4B00", 2.0),
        ("🧰", "Approved Tools", "Internal tools first", "#4D7C0F", 2.0),
        ("🤝", "Works Council", "Agreement on AI", "#0F766E", 2.0),
        ("🗂️", "Past Projects", "P-01 to P-09", "#65A30D", 2.0),
    ]),
    ("Writing", [
        ("✍️", "Report creation", "Writing your personal fix", "#F59E0B", 5.0),
    ]),
    ("Quality", [
        ("🎯", "Rerank", "Is the evidence relevant?", "#EC4899", 2.0),
        ("🔎", "Groundedness", "Is every claim backed?", "#6366F1", 3.0),
        ("✅", "Quality check", "Tools, sources, rules", "#16A34A", 2.0),
        ("📦", "Finalising", "Logging and preparing your report", "#1D4B00", 2.5),
    ]),
]


def _timed_steps():
    """Adds start and end seconds to every step, in order."""
    steps, t = [], 0.0
    for phase, items in PHASES:
        for emoji, title, sub, colour, secs in items:
            steps.append(dict(phase=phase, emoji=emoji, title=title, sub=sub, c=colour, s=t, e=t + secs))
            t += secs
    steps[-1]["last"] = True  # the last step keeps animating until the report arrives
    return steps, t


def _vars(step):
    return f"--c:{step['c']};--s:{step['s']:.1f}s;--e:{step['e']:.1f}s"


def _captions(steps):
    """Stacked captions: each one is visible only while its step is active."""
    caps = "".join(
        f'<span class="fmp-cap{" fmp-last" if s.get("last") else ""}" style="{_vars(s)}">'
        f'{s["emoji"]} {html.escape(s["title"])}: {html.escape(s["sub"])}…</span>' for s in steps)
    return f'<div class="fmp-caps">{caps}</div>'


def big_loader(run_id):
    """Large step-by-step loader shown on top of the results while n8n works."""
    steps, total = _timed_steps()
    cols = []
    for phase, _ in PHASES:
        cards = "".join(
            f'<div class="fmp-step{" fmp-last" if s.get("last") else ""}" style="{_vars(s)}">'
            f'<span class="fmp-ico">{s["emoji"]}</span>'
            f'<span class="fmp-txt"><b>{html.escape(s["title"])}</b><small>{html.escape(s["sub"])}</small></span>'
            f'<span class="fmp-state"><i class="fmp-spin"></i><i class="fmp-check">✓</i></span></div>'
            for s in steps if s["phase"] == phase)
        cols.append(f'<div class="fmp-phase"><div class="fmp-phase-title">{html.escape(phase)}</div>{cards}</div>')
    return (
        f'<div class="fmp-big" data-run="{run_id}" role="status" aria-live="polite">'
        f'<div class="fmp-big-head"><div class="fmp-orb"></div><div>'
        f'<div class="fmp-big-title">Fix My Process is working on your request</div>'
        f'{_captions(steps)}</div></div>'
        f'<div class="fmp-bar"><i style="--t:{total:.0f}s"></i></div>'
        f'<div class="fmp-grid">{"".join(cols)}</div>'
        f'<div class="fmp-big-foot">Usually about 30 seconds. Please keep this tab open.</div></div>')


def thin_loader(run_id):
    """Slim linear loader for narrow boxes (report box, chat)."""
    steps, total = _timed_steps()
    dots = "".join(
        f'<span class="fmp-dot{" fmp-last" if s.get("last") else ""}" style="{_vars(s)}" '
        f'title="{html.escape(s["title"])}">{s["emoji"]}</span>' for s in steps)
    return (
        f'<div class="fmp-thin" data-run="{run_id}" role="status" aria-live="polite">'
        f'<div class="fmp-rail"><div class="fmp-track"><i style="--t:{total:.0f}s"></i></div>'
        f'<div class="fmp-dots">{dots}</div></div>{_captions(steps)}</div>')


def header_html(logo_url):
    """Top bar: logo (falls back to text if the image can't load), title, demo tag."""
    logo = (f'<img class="fmp-logo" src="{html.escape(logo_url)}" alt="Kleinanzeigen" '
            f'onerror="this.style.display=\'none\';this.nextElementSibling.style.display=\'inline-flex\'">'
            f'<span class="fmp-logo-text" style="display:none">kleinanzeigen</span>') if logo_url else \
           '<span class="fmp-logo-text">kleinanzeigen</span>'
    return (
        '<div class="fmp-header"><div class="fmp-brand">'
        f'<span class="fmp-logo-wrap">{logo}</span>'
        '<div><div class="fmp-title">Fix My Process</div>'
        '<div class="fmp-sub">Describe a process problem once. Get a compliant fix, internal tools first.</div></div></div>'
        '<span class="fmp-tag">internal tool · concept demo</span></div>')


HOW_IT_WORKS = (
    '<div class="fmp-how"><div class="fmp-how-title">How it works</div>'
    '<div class="fmp-how-row"><span>🌐</span><div><b>Research</b><small>Web, news and research papers</small></div></div>'
    '<div class="fmp-how-row"><span>📚</span><div><b>Internal check</b><small>AI policy, approved tools, works council, past projects</small></div></div>'
    '<div class="fmp-how-row"><span>🚦</span><div><b>Is it allowed?</b><small>Green, amber or red with policy rule IDs</small></div></div>'
    '<div class="fmp-how-row"><span>📝</span><div><b>Your fix</b><small>Steps, sources and a confidence score</small></div></div>'
    '<div class="fmp-note">🔒 Describe the process, not the people. Do not include names.</div></div>')

def _guide(title, steps, tip=""):
    """Small 'how to use' box: title, numbered steps, optional tip."""
    items = "".join(f"<li>{s}</li>" for s in steps)
    tip_html = f'<div class="fmp-guide-tip">{tip}</div>' if tip else ""
    return f'<div class="fmp-guide"><div class="fmp-guide-title">{title}</div><ol>{items}</ol>{tip_html}</div>'


GUIDE_FORM = _guide("👉 What to do", [
    "Choose your <b>department</b> (required).",
    "Describe <b>what is slow, manual or unclear</b> and why it matters (required).",
    "Optional: add the tools you use today and how often.",
    "Click <b>Find my fix</b> and wait about 30 seconds.",
    "Read your report and <b>send feedback</b> at the end.",
], "💾 Save your reference code (FMP-…) to check the status later.")

GUIDE_CHAT = _guide("👉 How to use the chat", [
    "Choose your <b>department</b> (required). If none fits, choose Other.",
    "Describe one process problem: what is slow or manual, which tools you use and how often.",
    "<b>Keep chatting</b>: ask follow-up questions to get a more detailed, tailored report.",
    "Send feedback under the answer. Use <b>New conversation</b> for a different problem.",
])

GUIDE_STATUS = _guide("👉 Why and how to check status", [
    "<b>Why:</b> red cases go to the AI Governance Board. Here you see the Board decision and can open your report again.",
    "<b>How:</b> copy the reference code from your report, for example FMP-1234.",
    "Paste it below and click <b>Check status</b>.",
])

_LEVEL = {"green": ("🟢", "GREEN", "#16A34A"), "amber": ("🟠", "AMBER", "#D97706"), "red": ("🔴", "RED", "#DC2626")}
_CONF = {"High": "#1D4B00", "Medium": "#2F5BCB", "Low": "#B42318"}


def _chip(text, colour, solid=False):
    style = (f"background:{colour};color:#fff;border-color:{colour}" if solid
             else f"color:{colour};border-color:{colour}")
    return f'<span class="fmp-chip" style="{style}">{text}</span>'


def result_card(data):
    """Summary chips above the report: reference, compliance, confidence, review."""
    ref = html.escape(str(data.get("reference_code", "")))
    icon, name, colour = _LEVEL.get(str(data.get("compliance_level", "")).lower(), ("⚪", "UNKNOWN", "#6B7280"))
    label = str(data.get("confidence_label", ""))
    conf = data.get("confidence", "")
    chips = [_chip(f"🧾 {ref}", BRAND_DARK), _chip(f"{icon} Compliance {name}", colour, solid=True),
             _chip(f"📊 Confidence {html.escape(label)} ({conf}%)" if label else f"📊 Confidence {conf}%",
                   _CONF.get(label, "#6B7280"))]
    if data.get("under_review"):
        chips.append(_chip("🛡️ Sent to the AI Governance Board", "#7C3AED"))
    return (f'<div class="fmp-result"><div class="fmp-chips">{"".join(chips)}</div>'
            f'<div class="fmp-hint">Save your reference <b>{ref}</b> to check the status later.</div></div>')


def status_card(data):
    """Card for the Check status tab."""
    if not data.get("found"):
        return '<div class="fmp-result fmp-empty">🔍 No submission found for this reference. Check the code, for example FMP-1234.</div>'
    review = html.escape(str(data.get("review_status") or "Not needed"))
    note = html.escape(str(data.get("review_note") or ""))
    rows = [("Status", data.get("status")), ("Board review", review), ("Board note", note)]
    table = "".join(f"<div><span>{k}</span><b>{html.escape(str(v or '-'))}</b></div>" for k, v in rows)
    return result_card({**data, "under_review": False}).replace(
        '<div class="fmp-hint">', f'<div class="fmp-status">{table}</div><div class="fmp-hint">', 1)


def error_card(message):
    return f'<div class="fmp-result fmp-error">⚠️ {html.escape(message)}</div>'


# Opens the app in light mode, so brand colours look the same everywhere
FORCE_LIGHT_JS = """
() => {
  const url = new URL(window.location);
  if (url.searchParams.get('__theme') !== 'light') {
    url.searchParams.set('__theme', 'light');
    window.location.href = url.href;
  }
}
"""

CSS = f"""
:root {{ --brand:{BRAND_DARK}; --lime:{BRAND_LIME}; --soft:{BRAND_SOFT}; --ink:{INK}; --muted:{MUTED}; }}
.gradio-container {{ max-width: 1180px !important; margin: 0 auto !important; }}
footer {{ display: none !important; }}

/* Header */
.fmp-header {{ display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap:wrap;
  background:linear-gradient(120deg, var(--brand) 0%, #2C6A06 70%, #3F8A0C 100%); color:#fff;
  border-radius:18px; padding:18px 22px; box-shadow:0 8px 24px rgba(29,75,0,.18); }}
.fmp-brand {{ display:flex; align-items:center; gap:14px; }}
.fmp-logo-wrap {{ background:#fff; border-radius:12px; padding:8px 12px; display:inline-flex; align-items:center; }}
.fmp-logo {{ height:26px; display:block; }}
.fmp-logo-text {{ font-weight:800; color:var(--brand); letter-spacing:-.5px; font-size:18px; align-items:center; }}
.fmp-title {{ font-size:24px; font-weight:800; letter-spacing:-.3px; color:#fff !important; }}
.fmp-sub {{ opacity:.92; font-size:14px; margin-top:2px; color:#fff !important; }}
.fmp-tag {{ background:var(--lime); color:var(--brand); font-weight:700; font-size:12px; padding:6px 12px; border-radius:999px; }}

/* Cards and panels */
.fmp-panel {{ border:1px solid #E3EBD6 !important; border-radius:16px !important; background:#fff !important; }}
.fmp-how {{ background:var(--soft); border-radius:16px; padding:16px; color:var(--ink); }}
.fmp-how-title {{ font-weight:800; color:var(--brand); margin-bottom:10px; }}
.fmp-how-row {{ display:flex; gap:12px; align-items:flex-start; margin:10px 0; }}
.fmp-how-row span {{ font-size:22px; line-height:1; }}
.fmp-how-row small {{ display:block; color:var(--muted); }}
.fmp-note {{ margin-top:12px; background:#fff; border:1px dashed #9DBB6B; border-radius:12px; padding:10px; font-size:13px; }}
.fmp-guide {{ background:#fff; border:1px solid #E3EBD6; border-radius:14px; padding:12px 14px; color:var(--ink); font-size:13px; }}
.fmp-guide-title {{ font-weight:800; color:var(--brand); font-size:14px; margin-bottom:6px; }}
.fmp-guide ol {{ margin:0 !important; padding-left:20px !important; }}
.fmp-guide li {{ margin:3px 0 !important; }}
.fmp-guide-tip {{ margin-top:8px; color:var(--muted); }}
button.primary, .fmp-primary {{ background:var(--brand) !important; color:#fff !important; border:none !important; }}
button.primary:hover {{ filter:brightness(1.15); }}

/* Alignment: form column fills the height of the right column; field and button on one line */
.fmp-form-col {{ display:flex !important; flex-direction:column !important; }}
.fmp-form-col > * {{ flex-grow:0 !important; }}
.fmp-form-col > .form {{ flex-grow:1 !important; }}
.fmp-form-col > .form > .block:not(.fmp-grow) {{ flex-grow:0 !important; }}
.fmp-form-col > .form > .block {{ margin-top:0 !important; margin-bottom:0 !important; }}
.fmp-grow {{ flex:1 1 auto !important; display:flex !important; flex-direction:column !important; }}
.fmp-grow label {{ flex:1 1 auto; display:flex !important; flex-direction:column; }}
.fmp-grow .input-container {{ flex:1 1 auto; display:flex; align-items:stretch !important; }}
.fmp-grow textarea {{ flex:1 1 auto; height:auto !important; min-height:120px; }}
.fmp-guide-wrap .html-container {{ padding-bottom:0 !important; }}
.fmp-align-end {{ align-items:flex-end !important; }}
.fmp-align-end > button {{ margin-bottom:10px !important; min-height:40px; }}

/* Feedback box */
.fmp-feedback {{ padding:14px !important; background:var(--soft) !important; }}
.fmp-feedback .fmp-fb-title {{ font-weight:800; color:var(--brand); }}

/* Report text */
.fmp-report {{ color:var(--ink); }}
.fmp-report h1 {{ font-size:22px !important; color:var(--brand); }}
.fmp-report h2 {{ font-size:17px !important; color:var(--brand); border-bottom:2px solid var(--soft); padding-bottom:4px; margin-top:18px !important; }}
.fmp-report blockquote {{ border-left:5px solid var(--lime) !important; background:var(--soft) !important;
  border-radius:10px; padding:10px 14px !important; margin:8px 0 !important; color:var(--ink); }}

/* Result chips */
.fmp-result {{ padding:4px 2px; }}
.fmp-chips {{ display:flex; flex-wrap:wrap; gap:8px; }}
.fmp-chip {{ border:2px solid; border-radius:999px; padding:5px 12px; font-weight:700; font-size:13px; background:#fff; }}
.fmp-hint {{ color:var(--muted); font-size:13px; margin-top:8px; }}
.fmp-status {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(170px,1fr)); gap:8px; margin-top:12px; }}
.fmp-status div {{ background:var(--soft); border-radius:10px; padding:8px 10px; display:flex; flex-direction:column; }}
.fmp-status span {{ font-size:12px; color:var(--muted); }}
.fmp-error {{ background:#FEF3F2; border:1px solid #FDA29B; color:#B42318; border-radius:12px; padding:12px; }}
.fmp-empty {{ background:#F9FAFB; border-radius:12px; padding:12px; color:var(--muted); }}

/* ---------- Big loader ---------- */
.fmp-big {{ background:#fff; border:1px solid #E3EBD6; border-radius:20px; padding:20px;
  box-shadow:0 12px 32px rgba(29,75,0,.10); color:var(--ink); }}
.fmp-big-head {{ display:flex; gap:14px; align-items:center; }}
.fmp-big-title {{ font-weight:800; font-size:18px; color:var(--brand); }}
.fmp-orb {{ width:44px; height:44px; flex:0 0 44px; border-radius:50%;
  background:conic-gradient(var(--lime), var(--brand), #0EA5E9, #F59E0B, var(--lime));
  animation:fmp-rot 1.6s linear infinite; -webkit-mask:radial-gradient(circle 14px, transparent 98%, #000);
  mask:radial-gradient(circle 14px, transparent 98%, #000); }}
.fmp-caps {{ position:relative; height:22px; margin-top:4px; color:var(--muted); font-size:14px; }}
.fmp-cap {{ position:absolute; left:0; top:0; opacity:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:100%;
  animation:fmp-show .25s ease var(--s) forwards, fmp-hide .25s ease var(--e) forwards; }}
.fmp-cap.fmp-last {{ animation:fmp-show .25s ease var(--s) forwards; }}
.fmp-bar {{ height:8px; background:#EEF3E6; border-radius:999px; margin:16px 0; overflow:hidden; }}
.fmp-bar i, .fmp-track i {{ display:block; height:100%; width:0; border-radius:999px;
  background-image:linear-gradient(90deg, {BRAND_DARK}, {BRAND_LIME}, {BRAND_DARK}); background-size:200% 100%;
  animation:fmp-fill var(--t) linear forwards, fmp-shine 1.8s linear infinite; }}
.fmp-grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:14px; }}
.fmp-phase-title {{ font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-weight:700; margin-bottom:8px; }}
.fmp-step {{ display:flex; align-items:center; gap:10px; padding:10px; margin-bottom:8px; border-radius:14px;
  border:1.5px solid #E5E7EB; background:#fff; opacity:.4; filter:grayscale(.7);
  animation:fmp-on .35s ease var(--s) forwards, fmp-off .35s ease var(--e) forwards; }}
.fmp-step.fmp-last {{ animation:fmp-on .35s ease var(--s) forwards, fmp-pulse 1.6s ease-in-out var(--s) infinite; }}
.fmp-ico {{ width:36px; height:36px; flex:0 0 36px; border-radius:11px; display:grid; place-items:center; font-size:19px;
  background:color-mix(in srgb, var(--c) 14%, #fff); }}
.fmp-txt {{ display:flex; flex-direction:column; min-width:0; flex:1; }}
.fmp-txt b {{ font-size:14px; color:var(--ink); }}
.fmp-txt small {{ font-size:12px; color:var(--muted); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.fmp-state {{ position:relative; width:20px; height:20px; flex:0 0 20px; }}
.fmp-spin {{ position:absolute; inset:0; border-radius:50%; border:2.5px solid color-mix(in srgb, var(--c) 25%, #fff);
  border-top-color:var(--c); opacity:0;
  animation:fmp-show 0s linear var(--s) forwards, fmp-hide 0s linear var(--e) forwards, fmp-rot .8s linear infinite; }}
.fmp-last .fmp-spin {{ animation:fmp-show 0s linear var(--s) forwards, fmp-rot .8s linear infinite; }}
.fmp-check {{ position:absolute; inset:0; border-radius:50%; background:var(--c); color:#fff; font-style:normal;
  font-size:12px; font-weight:800; display:grid; place-items:center; opacity:0; transform:scale(.4);
  animation:fmp-pop .3s ease var(--e) forwards; }}
.fmp-last .fmp-check {{ display:none; }}
.fmp-big-foot {{ font-size:12px; color:var(--muted); margin-top:4px; text-align:right; }}

/* ---------- Thin loader ---------- */
.fmp-thin {{ background:var(--soft); border-radius:14px; padding:12px 14px 8px; color:var(--ink); }}
.fmp-rail {{ position:relative; padding:6px 4px; }}
.fmp-track {{ position:absolute; left:16px; right:16px; top:50%; height:4px; transform:translateY(-50%);
  background:#DCE7C8; border-radius:999px; overflow:hidden; }}
.fmp-dots {{ position:relative; display:flex; justify-content:space-between; }}
.fmp-dot {{ width:28px; height:28px; border-radius:50%; display:grid; place-items:center; font-size:14px;
  background:#fff; border:2px solid #DCE7C8; filter:grayscale(1); opacity:.55;
  animation:fmp-don .3s ease var(--s) forwards, fmp-doff .3s ease var(--e) forwards; }}
.fmp-dot.fmp-last {{ animation:fmp-don .3s ease var(--s) forwards, fmp-pulse 1.6s ease-in-out var(--s) infinite; }}
.fmp-thin .fmp-caps {{ font-size:13px; margin-top:6px; }}

/* ---------- Keyframes ---------- */
@keyframes fmp-on {{ to {{ opacity:1; filter:none; border-color:var(--c);
  background:color-mix(in srgb, var(--c) 9%, #fff); box-shadow:0 0 0 4px color-mix(in srgb, var(--c) 16%, transparent); }} }}
@keyframes fmp-off {{ to {{ opacity:1; filter:none; border-color:color-mix(in srgb, var(--c) 40%, #fff); background:#fff; box-shadow:none; }} }}
@keyframes fmp-don {{ to {{ opacity:1; filter:none; transform:scale(1.25); border-color:var(--c); background:#fff;
  box-shadow:0 0 0 4px color-mix(in srgb, var(--c) 22%, transparent); }} }}
@keyframes fmp-doff {{ to {{ opacity:1; filter:none; transform:scale(1); border-color:var(--c);
  background:color-mix(in srgb, var(--c) 18%, #fff); box-shadow:none; }} }}
@keyframes fmp-pulse {{ 0%,100% {{ box-shadow:0 0 0 3px color-mix(in srgb, var(--c) 18%, transparent); }}
  50% {{ box-shadow:0 0 0 9px color-mix(in srgb, var(--c) 6%, transparent); }} }}
@keyframes fmp-show {{ to {{ opacity:1; }} }}
@keyframes fmp-hide {{ to {{ opacity:0; }} }}
@keyframes fmp-pop {{ to {{ opacity:1; transform:scale(1); }} }}
@keyframes fmp-rot {{ to {{ transform:rotate(360deg); }} }}
@keyframes fmp-fill {{ from {{ width:2%; }} to {{ width:100%; }} }}
@keyframes fmp-shine {{ to {{ background-position:-200% 0; }} }}

/* ---------- Tablet and mobile ---------- */
@media (max-width: 900px) {{
  .fmp-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
}}
@media (max-width: 640px) {{
  .fmp-header {{ padding:14px; border-radius:14px; gap:10px; }}
  .fmp-brand {{ flex-direction:column; align-items:flex-start; gap:8px; }}
  .fmp-logo-wrap {{ padding:6px 10px; }}
  .fmp-tag {{ font-size:11px; padding:4px 10px; }}
  .fmp-title {{ font-size:20px; }}
  .fmp-sub {{ font-size:13px; }}
  .fmp-logo {{ height:20px; }}
  .fmp-big {{ padding:14px; border-radius:16px; }}
  .fmp-big-title {{ font-size:15px; }}
  .fmp-grid {{ grid-template-columns:1fr; gap:6px; }}
  .fmp-phase-title {{ margin:6px 0 4px; }}
  .fmp-step {{ padding:7px 9px; margin-bottom:5px; }}
  .fmp-ico {{ width:30px; height:30px; flex-basis:30px; font-size:16px; }}
  .fmp-dot {{ width:19px; height:19px; font-size:9.5px; border-width:1.5px; }}
  .fmp-dots {{ gap:2px; }}
  .fmp-thin {{ padding:10px 8px 6px; }}
  .fmp-caps {{ font-size:12.5px; }}
  .fmp-align-end {{ flex-wrap:nowrap !important; }}
  .fmp-align-end > * {{ min-width:0 !important; }}
  .fmp-align-end > button {{ flex:0 0 auto !important; width:auto !important; padding:0 14px !important; }}
}}
@media (prefers-reduced-motion: reduce) {{
  .fmp-orb {{ animation:none; }}
}}
"""


# ---------- Gradio theme in brand colours ----------
import gradio as gr  # noqa: E402

_BRAND_HUE = gr.themes.Color(
    c50="#F3F9E6", c100="#E4F2C7", c200="#CBE69A", c300="#B5E31F", c400="#8CC21A", c500="#5E9A0E",
    c600="#3F7A07", c700="#2C6A06", c800="#1D4B00", c900="#163A00", c950="#0E2600", name="kleinanzeigen")

THEME = gr.themes.Soft(
    primary_hue=_BRAND_HUE, secondary_hue=_BRAND_HUE, neutral_hue="gray", radius_size="lg",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "-apple-system", "Segoe UI", "Roboto", "Arial", "sans-serif"],
).set(
    block_label_text_color=BRAND_DARK, block_label_background_fill=BRAND_SOFT,
    block_title_text_color=BRAND_DARK, button_primary_background_fill=BRAND_DARK,
    button_primary_background_fill_hover="#2C6A06", button_primary_text_color="#FFFFFF",
    checkbox_background_color_selected=BRAND_DARK, slider_color=BRAND_DARK,
)
