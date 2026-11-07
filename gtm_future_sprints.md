# Future GTM Sprints

**Project:** Kleinanzeigen "Fix My Process" Agent  
**Status:** Draft, written before the build. To be updated at the end of the project with real MVP results.

The MVP proves the core loop: one submission, researched and compliance-checked, two reports, logged with feedback. These sprints move it toward internal go-to-market: from a working tool to an adopted one that shapes the AI roadmap. Order follows the sponsor first: the CPO / AI enablement team funds the next step, so their value comes first.

---

## Overview

| Sprint | Goal | Audience | Channel / motion | Deliverable | Success metric |
|---|---|---|---|---|---|
| **1. Close the loop** | Turn logged submissions and feedback into roadmap decisions | CPO / AI enablement team, internal tool owners | Scheduled n8n digest posted to Slack, reviewed in the monthly AI roadmap meeting | Monthly portfolio digest and internal-tool gap report | % of "won't use internal tool" reasons categorised; number of "no internal solution" cases turned into roadmap items |
| **2. Meet them where they work** | Grow submissions and adoption by moving intake into daily tools | Operations employees, pilot with 1 or 2 ops teams | Slack entry point, introduced in team meetings by the OEE team | Slack Trigger entry point + PII redaction step | Submissions per week; internal tool adoption rate; feedback rate |
| **3. Smarter and trusted** | Raise report quality and earn works council trust for wider rollout | Works council, Legal, CPO | Research loop with LangGraph, compliance pipeline report, joint review with the works council | Research loop service, compliance pipeline report, ops health digest | % of cases auto-cleared vs reviewed; review turnaround; % of reports above the confidence threshold |

---

## Sprint 1: Close the loop

- **Goal:** Give the CPO / AI enablement team a regular, evidence-based view of where employees struggle and why internal tools are not used.
- **Audience:** CPO / AI enablement team; owners of internal tools such as Ticket Lens, FlowMate and Knowledge Finder.
- **Channel / motion:** A scheduled n8n workflow reads all Airtable submissions and feedback, an LLM groups them into themes, and the digest is posted to Slack before the monthly AI roadmap meeting.
- **Deliverable:**
  - **Portfolio digest:** top friction themes per department, use-case ranking by impact and effort, list of "no internal solution" cases.
  - **Internal-tool gap report:** reasons people do not use each internal tool, with suggested fixes for the tool owner.
  - Privacy: department level only, groups of 5 or more (KA-BV-AI-2026 section 6.2).
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
- **Success metric:** Submissions per week; internal tool adoption rate in pilot teams; feedback rate on reports.
- **Milestone:** 4-week pilot live in Slack.

## Sprint 3: Smarter and trusted

- **Goal:** Improve answer quality on hard cases and give the works council and Legal a clear view of how cases are handled, as a condition for company-wide rollout.
- **Audience:** Works council, Legal, CPO.
- **Channel / motion:** Joint review sessions with the works council representative on the AI Governance Board; quarterly compliance report.
- **Deliverable:**
  - **Research loop** (LangGraph service behind an n8n HTTP Request node): re-query when evidence is weak; find an approved alternative when a tool is not approved.
  - **Compliance pipeline report:** cases in review, turnaround time, auto-cleared vs escalated.
  - **Ops health digest** (for example in Notion): errors, failed APIs, low-confidence rate.
- **Success metric:** % of cases auto-cleared vs reviewed; review turnaround time; % of reports above the confidence threshold.
- **Milestone:** Works council sign-off on the transparency and review process.

---

## Feature and improvement backlog (not GTM sprints)

| Item | Type | Why |
|---|---|---|
| Save the execution ID on the Airtable row so the error workflow can find the reference code | Fix | Error Trigger may not receive the reference code |
| Async response: return the reference code at once and let Check status show the report | Fix (only if timing tests fail) | Webhook or Render timeouts on long runs |
| Access control for the app and the admin upload form | Feature | Nothing is password protected in the MVP |
| Cache API results for repeated questions | Improvement | Saves free-tier quota and time |
| Expand the calibration set beyond 15 cases and re-tune the threshold | Improvement | Better confidence scores |
| German and English reports | Feature | Kleinanzeigen works in both languages |
| Keep Render awake or move off the free plan for demos | Improvement | Free plan sleeps (about 1 minute to wake) |
