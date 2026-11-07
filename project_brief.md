# Project 3 Brief: Two Decisions

**Project:** Kleinanzeigen "Fix My Process" Agent  
**Author:** Ayhan Demir  
**Type:** Autonomous Company Research & Report Generation Agent

---

## 1. Industry / Use Case

**Online classifieds marketplace (Kleinanzeigen): internal AI enablement and process improvement during the company's move to a standalone business.**

An employee describes a daily process problem once. The agent researches how others solve it (3 free APIs), checks the internal knowledge base (AI policy, approved tools, works council agreement, past projects), classifies compliance as green / amber / red, and writes two reports with sources and a confidence level:

| Report | Reader | What it gives |
|---|---|---|
| **A: Fix for me** | Operations employee / OEE team | A practical fix with an internal tool first, then an approved external tool, step by step, the same day |
| **B: Use-case card** | CPO / AI enablement team | Evidence, size of the problem, compliance status, effort vs impact and user feedback, to prioritise the AI roadmap |

All internal data is synthetic. No real company or employee data is used.

---

## 2. Primary Stack

☑ **n8n** &nbsp;&nbsp; ☐ LangGraph

### Why this stack fits this industry and problem

"Fix My Process" is an operations workflow, not an open-ended reasoning problem: intake from a form or chat, research, a compliance check, two reports for two different readers, human review for edge cases, logging and error handling.  
The flow is mostly linear with a few branches (for upload, review steps), and n8n covers every step with a ready node:  
- Triggers, IF and Switch, Slack send and wait for the AI Governance Board review,  
- Airtable logging and a separate error workflow.  
- Integrating business systems such as Slack and Airtable is exactly the "ops thinking" this use case needs, because the value only appears when the output reaches people and is tracked.  
- No MVP step needs reasoning that loops back and remembers state, so LangGraph is not needed now. It stays a possible light helper for a later sprint (a research loop behind an n8n HTTP Request node), while all primary orchestration and agent logic live in n8n.
