"""Fix My Process: Gradio UI only.
Rule from agents.md: no business logic here. Every answer comes from the n8n webhooks
/form, /chat, /status and /feedback; this file only builds requests and shows responses."""
import os
import uuid

import gradio as gr
import requests
from dotenv import load_dotenv

import ui_style as ui

load_dotenv()
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "").rstrip("/")  # e.g. https://your-n8n/webhook
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")
SECRET_HEADER = "X-Webhook-Secret"  # must match the Header Auth credential name in n8n
LOGO_URL = os.getenv("LOGO_URL", "https://static.kleinanzeigen.de/static/img/common/logo/logo-kleinanzeigen-horizontal.svg")
TIMEOUT_SECONDS = 180

DEPARTMENTS = ["Customer Service", "Operations", "Trust and Safety", "Sales Ops",
               "BI and Finance", "IT", "Internal Comms", "Other"]
FREQUENCIES = ["Daily", "Weekly", "Monthly", "Rarely"]
# Tools from the Approved Tools List (KA-AI-TOOLS-002) plus the everyday tools it mentions.
# Users can also type their own tool and press Enter.
TOOLS = ["KAi Assist", "Ticket Lens", "FlowMate", "Knowledge Finder", "Insight Desk",
         "Microsoft 365 Copilot", "DeepL Pro", "Miro AI", "Atlassian Intelligence",
         "GitHub Copilot Business", "Grammarly Business", "Zapier",
         "CS platform", "Excel / Google Sheets", "Outlook / Teams", "Slack", "Jira", "Confluence"]
EXAMPLES = [
    ["Customer Service", "Reading long customer ticket threads takes about 10 minutes per ticket before I can reply.", ["CS platform"], "Daily"],
    ["Operations", "Every Friday I write the same weekly status email by copying numbers from three spreadsheets.", ["Excel / Google Sheets", "Outlook / Teams"], "Weekly"],
    ["BI and Finance", "Ops leads ask me for ad-hoc KPI charts several times a week and I build each one by hand.", ["Excel / Google Sheets"], "Weekly"],
    ["Customer Service", "We want an AI score that ranks agents by productivity based on their ticket handling.", ["CS platform"], "Monthly"],
]

# Messages when a required field is empty (Form and Chat)
MSG_DEPARTMENT = "Please choose your department. If none fits, select Other."
MSG_PROBLEM = "Please describe your problem: what is slow, manual or unclear, and why it matters."


# Browser-only: scroll to the big loader after the click (returns the inputs unchanged)
SCROLL_TO_LOADER = """(...args) => { setTimeout(() => document.getElementById('fmp-big')
  ?.scrollIntoView({behavior: 'smooth', block: 'start'}), 400); return args; }"""


# ---------- n8n connection ----------
def call_n8n(path, payload):
    """POST to an n8n webhook. Returns (data, error_message)."""
    if not N8N_WEBHOOK_URL:
        return None, "N8N_WEBHOOK_URL is not set in .env."
    try:
        r = requests.post(f"{N8N_WEBHOOK_URL}/{path}", json=payload,
                          headers={SECRET_HEADER: WEBHOOK_SECRET}, timeout=(10, TIMEOUT_SECONDS))
    except requests.exceptions.Timeout:
        return None, "n8n took longer than 3 minutes. Try Check status later."
    except requests.exceptions.ConnectionError:
        return None, "Can't reach n8n. Check N8N_WEBHOOK_URL and that n8n is running."
    if r.status_code in (401, 403):
        return None, "n8n rejected the request: WEBHOOK_SECRET does not match the Header Auth credential."
    if r.status_code == 404:
        return None, "Webhook not found: activate the workflow (production URL) or click Execute workflow (test URL)."
    if r.status_code >= 400:
        return None, f"n8n returned an error ({r.status_code}). Open Executions in n8n to see which node failed."
    try:
        return r.json(), None
    except ValueError:
        return None, "n8n answered, but not with JSON. Check the Respond to Webhook node."


def hide():
    return gr.update(visible=False)


def show(value):
    return gr.update(value=value, visible=True)


# ---------- Form tab ----------
def submit_form(department, problem, current_tools, frequency):
    """Shows both loaders, waits for n8n, then shows the report and the feedback box."""
    if not department:
        gr.Warning(MSG_DEPARTMENT)
        yield hide(), hide(), hide(), hide(), hide(), None, gr.update(interactive=True)
        return
    if not (problem or "").strip():
        gr.Warning(MSG_PROBLEM)
        yield hide(), hide(), hide(), hide(), hide(), None, gr.update(interactive=True)
        return
    run = uuid.uuid4().hex[:8]  # new id restarts the animations
    yield (show(ui.big_loader(run)), show(ui.thin_loader(run)), hide(), hide(), hide(), None,
           gr.update(interactive=False))
    data, error = call_n8n("form", {"department": department, "problem": problem.strip(),
                                    "current_tools": ", ".join(current_tools or []) or "Not given",
                                    "frequency": frequency, "session_id": f"form-{run}"})
    if error:
        yield hide(), hide(), show(ui.error_card(error)), hide(), hide(), None, gr.update(interactive=True)
        return
    yield (hide(), hide(), show(ui.result_card(data)), show(data.get("report_a", "")),
           gr.update(visible=True), data.get("reference_code"), gr.update(interactive=True))


def clear_form():
    return None, "", [], "Weekly", hide(), hide(), hide(), hide(), hide(), None


# ---------- Chat tab ----------
def send_chat(message, history, department, session_id):
    """Sends one chat message to n8n; the reply is the report for that message."""
    history = history or []
    if not department:
        gr.Warning(MSG_DEPARTMENT)
        yield history, message, gr.skip(), gr.skip(), gr.skip()  # keep the typed text
        return
    if not (message or "").strip():
        gr.Warning(MSG_PROBLEM)
        yield history, "", hide(), hide(), None
        return
    history = history + [{"role": "user", "content": message.strip()}]
    yield history, "", show(ui.thin_loader(uuid.uuid4().hex[:8])), hide(), None
    data, error = call_n8n("chat", {"message": message.strip(), "department": department,
                                    "session_id": session_id, "channel": "gradio_chat"})
    reply = f"⚠️ {error}" if error else (data.get("report_a") or data.get("output") or "No report returned.")
    history = history + [{"role": "assistant", "content": reply}]
    yield history, "", hide(), gr.update(visible=not error), (None if error else data.get("reference_code"))


def new_chat():
    return [], "", hide(), hide(), None, uuid.uuid4().hex


# ---------- Check status tab ----------
def check_status(reference):
    ref = (reference or "").strip().upper()
    if not ref:
        gr.Warning("Enter your reference code, for example FMP-1234.")
        return hide(), hide()
    data, error = call_n8n("status", {"reference_code": ref})
    if error:
        return show(ui.error_card(error)), hide()
    if not data.get("found"):
        return show(ui.status_card(data)), hide()
    return show(ui.status_card(data)), show(data.get("report_a", ""))


# ---------- Feedback (same for Form and Chat) ----------
def send_feedback(reference, will_use, reason):
    if not reference:
        return "No report yet: submit a problem first."
    if not will_use:
        return "Please choose Yes or No."
    data, error = call_n8n("feedback", {"reference_code": reference, "will_use": will_use,
                                        "feedback_reason": (reason or "").strip()})
    if error:
        return error
    return "Thanks! Your feedback was saved." if data.get("saved") else "Feedback not saved: reference not found."


def reset_feedback():
    """Fresh feedback box for every new report: Yes selected, empty reason, no message."""
    return "Yes", "", ""


def feedback_box():
    """Builds the feedback box shown under a report. Returns its components."""
    with gr.Column(visible=False, elem_classes=["fmp-panel", "fmp-feedback"]) as group:
        gr.HTML('<div class="fmp-fb-title">💬 Was this useful?</div>')
        will_use = gr.Radio(["Yes", "No"], value="Yes", label="Will you use the suggested internal tool?")
        reason = gr.Textbox(label="Why?", placeholder="For example: saves me time, not enabled for my team, missing feature",
                            lines=2)
        send = gr.Button("Send feedback", variant="secondary")
        result = gr.Markdown()
    return group, will_use, reason, send, result


# ---------- Layout ----------
with gr.Blocks(title="Fix My Process · Kleinanzeigen") as demo:
    gr.HTML(ui.header_html(LOGO_URL))

    with gr.Tabs():
        # Form tab
        with gr.Tab("📝 Form"):
            with gr.Row(equal_height=True):
                with gr.Column(scale=5, min_width=320, elem_classes="fmp-form-col"):
                    department = gr.Dropdown(DEPARTMENTS, label="Department", value=None)
                    problem = gr.Textbox(label="What is slow, manual or unclear?", lines=5, elem_classes="fmp-grow",
                                         placeholder="Describe the process, not the people. Do not include names.")
                    with gr.Row():
                        current_tools = gr.Dropdown(TOOLS, value=[], multiselect=True, allow_custom_value=True,
                                                    label="Tools you use today (optional)",
                                                    info="Pick from the list or type your own and press Enter",
                                                    min_width=220)
                        frequency = gr.Dropdown(FREQUENCIES, label="How often?", value="Weekly", min_width=140)
                    with gr.Row():
                        submit = gr.Button("Find my fix 🚀", variant="primary", scale=3)
                        clear = gr.Button("Clear", scale=1)
                with gr.Column(scale=4, min_width=280):
                    gr.HTML(ui.HOW_IT_WORKS)
                    gr.HTML(ui.GUIDE_FORM, elem_classes="fmp-guide-wrap")
            with gr.Accordion("💡 Try an example", open=False):
                gr.Examples(EXAMPLES, inputs=[department, problem, current_tools, frequency], label=None)

            big = gr.HTML(visible=False, elem_id="fmp-big")
            with gr.Column(elem_classes="fmp-panel"):
                thin = gr.HTML(visible=False)
                card = gr.HTML(visible=False)
                report = gr.Markdown(visible=False, elem_classes="fmp-report")
                fb_group, fb_use, fb_reason, fb_send, fb_result = feedback_box()
            form_ref = gr.State(None)

            submit.click(submit_form, [department, problem, current_tools, frequency],
                         [big, thin, card, report, fb_group, form_ref, submit],
                         show_progress="hidden", js=SCROLL_TO_LOADER)
            submit.click(reset_feedback, None, [fb_use, fb_reason, fb_result], show_progress="hidden")
            clear.click(clear_form, None, [department, problem, current_tools, frequency,
                                           big, thin, card, report, fb_group, form_ref], show_progress="hidden")
            fb_send.click(send_feedback, [form_ref, fb_use, fb_reason], fb_result)

        # Chat tab
        with gr.Tab("💬 Chat"):
            gr.HTML(ui.GUIDE_CHAT)
            with gr.Row(elem_classes="fmp-align-end"):
                chat_dept = gr.Dropdown(DEPARTMENTS, label="Department", value=None, scale=3, min_width=200)
                reset = gr.Button("New conversation", size="sm", scale=1, min_width=140)
            chatbot = gr.Chatbot(height=460, show_label=False, elem_classes="fmp-report",
                                 placeholder="👋 Describe one process problem: what is slow or manual, which tools you use and how often.")
            chat_loader = gr.HTML(visible=False)
            with gr.Row():
                msg = gr.Textbox(show_label=False, placeholder="Describe the process, not the people…", scale=5, min_width=200)
                send = gr.Button("Send", variant="primary", scale=1, min_width=90)
            c_group, c_use, c_reason, c_send, c_result = feedback_box()
            chat_ref = gr.State(None)
            session_id = gr.State(lambda: uuid.uuid4().hex)  # chat memory key in n8n, never stored in Airtable

            for trigger in (send.click, msg.submit):
                trigger(send_chat, [msg, chatbot, chat_dept, session_id],
                        [chatbot, msg, chat_loader, c_group, chat_ref], show_progress="hidden")
            for trigger in (send.click, msg.submit):
                trigger(reset_feedback, None, [c_use, c_reason, c_result], show_progress="hidden")
            reset.click(new_chat, None, [chatbot, msg, chat_loader, c_group, chat_ref, session_id], show_progress="hidden")
            c_send.click(send_feedback, [chat_ref, c_use, c_reason], c_result)

        # Check status tab
        with gr.Tab("🔎 Check status"):
            gr.HTML(ui.GUIDE_STATUS)
            with gr.Row(elem_classes="fmp-align-end"):
                ref_in = gr.Textbox(label="Reference code", placeholder="FMP-1234", scale=4, min_width=200)
                check = gr.Button("Check status", variant="primary", scale=1, min_width=120)
            status_card = gr.HTML(visible=False)
            status_report = gr.Markdown(visible=False, elem_classes="fmp-report")
            check.click(check_status, ref_in, [status_card, status_report])
            ref_in.submit(check_status, ref_in, [status_card, status_report])

    gr.HTML('<div class="fmp-hint" style="text-align:center">Fix My Process · concept demo with fictional internal data · '
            'Your report is AI-generated: check the sources before you act.</div>')


# Several people can wait for n8n at the same time (I/O only, no heavy work here)
demo.queue(default_concurrency_limit=20)

if __name__ == "__main__":
    # Render needs 0.0.0.0 and its PORT; Gradio 6 takes theme, css and js in launch()
    demo.launch(server_name="0.0.0.0", server_port=int(os.getenv("PORT", 7860)),
                theme=ui.THEME,
                css=ui.CSS, js=ui.FORCE_LIGHT_JS)
