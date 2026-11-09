# Future GTM Sprints

**Project:** Kleinanzeigen "Fix My Process" Agent  
**Status:** Updated after the build, 9 Nov 2026. Calibration results to be added.

The MVP proves the core loop: one submission, researched and compliance-checked, two reports with a confidence score, logged with feedback. These sprints move it toward internal go-to-market: from a working tool to an adopted one that shapes the AI roadmap. Order follows the sponsor first: the CPO / AI enablement team funds the next step, so their value comes first.

---

## What the MVP does today

- **Entry points:** Gradio form and chat (UI), with n8n form and chat as backup; Check status and feedback by reference code (FMP-xxxx).
- **Research:** one n8n Research Agent calls Tavily (web practice), GNews (news) and OpenAlex (research), and searches 4 internal PDFs in Pinecone (policy, approved tools, works council agreement, past projects), with Cohere reranking.
- **Compliance:** green / amber / red with policy rule IDs; **red** cases go to the AI Governance Board in Slack after the user already has the report. Red stays blocked; the Board chooses **Add to pipeline** (worth a compliant solution) or **Dismiss for now**.
- **Reports:** Report A for the employee (internal tool first, steps, is it allowed) and Report B for the CPO / AI enablement team (use-case card with executive summary).
- **Quality gate:** Cohere relevance score + LLM groundedness judge + code checks (known tools, document IDs, URLs found in the search results, valid rule IDs). Confidence High (75+), Medium (40-74) or Low (below 40), shown as a banner.
- **Logging:** every submission, review decision, feedback ("will you use the internal tool?" + reason) and error in Airtable; errors also alert in Slack.
- **Calibration:** [x of 15 test cases High; compliance level correct in x of 15]

---

## Overview

| Sprint | Goal | Audience | Channel / motion | Deliverable | Success metric |
|---|---|---|---|---|---|
| **1. Close the loop** | Turn logged submissions and feedback into roadmap decisions | CPO / AI enablement team, internal tool owners | Scheduled n8n digest posted to Slack, reviewed in the monthly AI roadmap meeting | Monthly portfolio digest and internal-tool gap report | % of "won't use internal tool" reasons categorised; number of "no internal solution" cases turned into roadmap items |
| **2. Meet them where they work** | Grow submissions and adoption by moving intake into daily tools | Operations employees, pilot with 1 or 2 ops teams | Slack entry point, introduced in team meetings by the OEE team | Slack Trigger entry point + PII redaction step | Submissions per week; internal tool adoption rate; feedback rate |
| **3. Smarter and trusted** | Raise report quality and earn works council trust for wider rollout | Works council, Legal, CPO | Joint review with the works council; research loop only if calibration shows the need | Amber handling agreement, compliance pipeline report, ops health digest, research loop (conditional) | % of cases auto-cleared vs reviewed; review turnaround; % of reports with High confidence |

---

## Sprint 1: Close the loop

- **Goal:** Give the CPO / AI enablement team a regular, evidence-based view of where employees struggle and why internal tools are not used.
- **Audience:** CPO / AI enablement team; owners of internal tools such as Ticket Lens, FlowMate and Knowledge Finder.
- **Channel / motion:** A scheduled n8n workflow reads the Airtable submissions, an LLM groups them into themes, and the digest is posted to Slack before the monthly AI roadmap meeting.
- **Data used (already logged by the MVP):** `will_use`, `feedback_reason`, `no_internal_solution`, `internal_tool`, `use_case_title`, `effort`, `impact`, `confidence_label`, department.
- **Deliverable:**
  - **Portfolio digest:** top friction themes per department, use-case ranking by impact and effort, list of "no internal solution" cases.
  - **Internal-tool gap report:** reasons people do not use each internal tool, with suggested fixes for the tool owner.
  - **Knowledge gap signal:** low-confidence rate per department and topic, showing where internal documents are missing or outdated.
  - **Red cases in the pipeline:** red cases the AI Governance Board marked "Add to pipeline" (`review_status` = Added to pipeline), each with a suggested compliant path to amber or green, for example team-level KPIs without personal data instead of an individual productivity score.
  - Privacy: department level only, groups of 5 or more (KA-BV-AI-2026 section 6).
- **Success metric:** % of "won't use internal tool" reasons categorised; number of "no internal solution" cases turned into roadmap items; tool owners act on at least one finding per month.
- **Milestone:** First monthly roadmap input built from real submissions.

## Sprint 2: Meet them where they work

- **Goal:** Make submitting a problem as easy as sending a Slack message, so more employees use it and adoption data grows.
- **Audience:** Operations employees, starting with 1 or 2 pilot teams chosen with the OEE team.
- **Channel / motion:** Slack Trigger as a new entry point to the same main workflow; the OEE team introduces it in team meetings; champions from the KAi Assist rollout help spread it.
- **Deliverable:**
  - Slack entry point that reuses the main workflow (no change to the core).
  - **PII redaction** before any LLM call, closing the main known gap of the MVP.
  - Reply in the Slack thread with the reference code and feedback buttons.
- **Success metric:** Submissions per week; internal tool adoption rate in pilot teams; feedback rate on reports, compared with the Gradio feedback rate from the MVP.
- **Milestone:** 4-week pilot live in Slack.

## Sprint 3: Smarter and trusted

- **Goal:** Improve answer quality on hard cases and give the works council and Legal a clear view of how cases are handled, as a condition for company-wide rollout.
- **Audience:** Works council, Legal, CPO.
- **Channel / motion:** Joint review sessions with the works council representative on the AI Governance Board; quarterly compliance report.
- **Deliverable:**
  - **Amber handling agreement:** the Internal AI Policy (section 5.2) sends amber cases to Board review, while the MVP sends only red. Agree the rule with the Board and the works council, then align policy and workflow.
  - **Board review form with a note:** replace the Add to pipeline / Dismiss for now buttons with a short form (decision + reason), so `review_note` carries the real reason.
  - **Compliance pipeline report:** cases in review, turnaround time, auto-cleared vs escalated.
  - **Ops health digest** in Slack and an Airtable view: errors, failed APIs, low-confidence rate.
  - **Research loop (conditional):** a LangGraph service behind an n8n HTTP Request node that re-queries when evidence is weak and finds an approved alternative when a tool is not approved. Built only if calibration and live data show many Low-confidence cases.
- **Success metric:** % of cases auto-cleared vs reviewed; review turnaround time; % of reports with High confidence.
- **Milestone:** Works council sign-off on the transparency and review process.

---

## Feature and improvement backlog (not GTM sprints)

| Item | Type | Why |
|---|---|---|
| Compliance through Annex A yes / no fields, with code deciding the level | Improvement | More stable and auditable than a free LLM judgement |
| Send Low-confidence reports to the AI Governance Board | Option | Decide after calibration, based on how often Low happens |
| Retrieval tuning: reranker top 4-5 instead of 3 | Improvement | More policy text reaches the agent |
| Retries on the 3 research API tools | Fix | Free-tier limits and short outages |
| Cost trims: shorter Tavily results, smaller judge evidence limit, no reranker on past projects, optional removal of the rerank score | Improvement | Lower cost per run where quality stays the same |
| Async response: return the reference code at once and let Check status show the report | Fix (only if timing tests fail) | Webhook or Render timeouts on long runs |
| Access control for the app and the admin upload form | Feature | Nothing is password protected in the MVP |
| Cache API results for repeated questions | Improvement | Saves free-tier quota and time |
| Expand the calibration set beyond 15 cases and re-tune the bands | Improvement | Better confidence scores |
| German and English reports | Feature | Kleinanzeigen works in both languages |
| Keep Render awake or move off the free plan for demos | Improvement | Free plan sleeps (about 1 minute to wake) |
