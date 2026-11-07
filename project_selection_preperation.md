# Project 3: Research (Prework)

**Project:** Kleinanzeigen "Fix My Process" Agent  

**Type:** Autonomous Company Research & Report Generation Agent  

**Primary stack:** n8n (self-hosted), Gradio on Render as UI only  

**Author:** Ayhan Demir · Ironhack AI Consulting & Integration Bootcamp · November 2026


---

## 1. Industry Selection

**Company:** Kleinanzeigen (Germany's largest classifieds marketplace: C2C second-hand, B2C, real estate)  

**Users:** Kleinanzeigen employees: operations teams, the Operational Effectiveness and Enablement (OEE) team, and the CPO's AI-Tech and enablement teams  

**Data:** public web data (3 APIs) plus synthetic internal documents (AI policy, approved tools list, works council agreement, past projects). No real company or employee data.

### What industry problem are we solving?

Kleinanzeigen is moving to become a standalone company. Adevinta, owned by Permira and Blackstone since 2024, is breaking up its portfolio. During a change like this, which includes AI adoption, three things happen at once:

1. **Employees feel friction every day**: repeated manual tasks, slow processes, unclear tools and weak AI support. They have no simple way to turn a frustration into a solution.
2. **AI enablement teams need real use cases with evidence.** Instead they get vague ideas or top-down guesses about what operations needs, without knowing what is critical to quality for real users. The result is low AI adoption.
3. **Every AI or process idea must pass German rules**: the internal AI policy, the approved tools list, the works council (Betriebsrat) agreement, GDPR and the EU AI Act. Nobody checks this early, so good ideas stall late.

Today the steps from "this is annoying" → research → compliance check → proposal are done by hand, slowly, or not at all.

### Who is the report for, and what does "useful" mean?

| Reader | What they need | What "useful" means |
|---|---|---|
| **Operations employee / team lead + OEE team** | Help to fix the problem now, made easy | Practical steps using **approved** tools only, the same day. Internal tools first, approved external tools second, with a research summary, confidence level and sources |
| **CPO / AI enablement team** | A list of qualified use cases | Evidence, size of the problem, compliance status, effort vs impact and user feedback, so they can prioritise and build the roadmap |

**One submission, two reports.** The employee describes the problem once. Operations gets help right away, and leadership gets a scoped, compliant use case. Bottom-up demand feeds a top-down AI portfolio.

### Why I chose this project

- **Same facts, different readers.** Web research and internal documents are shared; only the prompt and report format change.
- **Small extra scope.** One pipeline, one extra LLM step and one extra output (roughly 15 to 20% more work).
- **The employee is the user.** People get help; they are not monitored. This avoids the works council and GDPR problems of option D.
- **It fits the AI consulting role.** It connects the CPO / AI enablement team and the OEE team in one flow: employee experience, AI enablement and process improvement.

---

## 2. Stack Decision: n8n vs LangGraph

### Decision

**n8n (self-hosted) is the primary stack for the MVP. LangGraph is secondary and not in the MVP.**

| Role | Choice | Why |
|---|---|---|
| **Primary** | **n8n, self-hosted** | All business logic lives here. The workflow is ops-heavy and mostly linear with a few branches |
| **Secondary** | **LangGraph, not in MVP** | Added later only as a small Python service behind an n8n HTTP Request node, and only if the reasoning needs state across steps |
| **UI** | **Gradio on Render** | UI only. Calls n8n webhooks and shows the answer. Rule: `app.py` has no business logic (no LLM calls, no API calls except the n8n webhooks, no scoring) |

### Why n8n is primary

"Fix My Process" is an ops workflow: intake from several entry points, two readers, human review routed to department channels, logging, error handling and status lookup. The flow is mostly linear with a few branches, and n8n covers each step with a ready node (triggers, IF and Switch, Slack send and wait, Airtable, an error workflow). This is the "ops thinking" the course asks for. LangGraph is secondary for now because no MVP step needs reasoning that loops back and remembers state; it comes in later only as a small Python service behind an HTTP Request node. Using both stacks as equal requirements in the MVP would be over-engineering, which the course names as a red flag.

### When LangGraph comes in

| Situation | n8n handles it? | Needs LangGraph? |
|---|---|---|
| Intake → validation → research → reports → response | ✅ Yes | No |
| Route by green / amber / red | ✅ Yes (Switch) | No |
| Send edge cases to a human in the department channel | ✅ Yes (review branch, Slack send and wait) | No |
| Retry a failed API call | ✅ Yes (Retry On Fail) | No |
| Look up status by reference code | ✅ Yes (Airtable search) | No |
| Compliance sends the flow back to research: "tool not approved, find an approved alternative, re-check" | Not cleanly | ⚠️ Yes (GTM sprint) |
| Multi-pass research loop that remembers which sources and queries it tried | Not cleanly | ⚠️ Yes (GTM sprint) |

If LangGraph is added, n8n still owns intake, logging, review, errors and the response. LangGraph only does the looping reasoning step.

### MVP architecture

**In one line:** Trigger → Collect data (3 free APIs) → Check it (RAG / trusted docs) → Compliance → Report with sources → Log and reply

```
1. Employee describes the problem   →  Gradio form or chat (n8n form / chat as backup)
2. Call 3 APIs                      →  web practice (Tavily), news (GNews), research numbers (OpenAlex)
3. Search the internal PDFs (RAG)   →  policy, approved tools, works council, past projects
4. Compliance check                 →  green / amber / red
5. LLM writes two reports           →  A: employee / OEE · B: CPO / AI enablement, with sources and confidence
6. Quality gate                     →  below about 85%: "low confidence" banner
7. Log and reply                    →  Airtable row + reference code, report on screen, feedback box
```

**The user never waits for a human.** Edge cases get the report at once with an "under review" banner; the final version appears in Check status after review.

| n8n workflow | Starts when | What it does |
|---|---|---|
| **Main workflow** (one canvas) | An employee submits a problem | Steps 1 to 7 above. Check status and feedback read and update the same Airtable row |
| ↳ Review branch | An edge case is found | Sends it to the department's Slack channel, waits for the decision, updates Airtable |
| ↳ Document upload | The CPO / AI enablement team uploads a PDF | Extract text → chunk → embed (Cohere) → Pinecone |
| **Error workflow** (separate) | Any step fails | Logs the error in Airtable and alerts the owner in Slack |

### Stack and tools

| Tool | Role |
|---|---|
| **n8n (self-hosted)** | All business logic, all workflows |
| **Gradio on Render** | UI: Form, Chat, Check status. n8n URL  |
| **OpenAI gpt-4o-mini** | Search queries, compliance class, Reports A and B, groundedness check |
| **Tavily · GNews · OpenAlex** | External research |
| **Pinecone** | Vector store for internal PDFs, one namespace per type: policy, approved tools, works council, past projects |
| **Cohere** | Embeddings and rerank (relevance score for the quality gate) |
| **Airtable** | Submissions table and Errors table |
| **Slack** | Human review in department channels, error alerts |
| **Not in MVP** | LangGraph, Gmail, Google Drive, Telegram, Notion |

---

## 3. API Research

### Selected APIs

Each API has one job in the workflow. One call per API per submission, so free tiers cover the MVP and demo comfortably.

| API | Category | Job in the workflow | Docs | Authentication | Free tier and limits (Nov 2026) |
|---|---|---|---|---|---|
| **Tavily** | Web search | How others solve the problem (competitors, industry practice). Built for LLMs: returns clean content, not just links | [docs.tavily.com](https://docs.tavily.com/documentation/api-reference/endpoint/search) | API key | 1,000 credits/month, no credit card; basic search = 1 credit |
| **GNews** | News | Latest AI tools and trends for the problem area | [docs.gnews.io](https://docs.gnews.io/) | API key as query parameter (`apikey`) | 100 requests/day, up to 10 articles each, max 1 request/second, 12 h delay. Free plan for non-commercial / development use |
| **OpenAlex** | Research / evidence | Research numbers that size the problem and back the fix (Report B) | [developers.openalex.org](https://developers.openalex.org/api-reference/authentication) | Free API key (`api_key` parameter), **required since Feb 2026** | $1/day of free usage with a key ($0.10/day without); single-record lookups unlimited |

### Rate limits and error handling

Free tiers mean limits, so every API node has **Retry On Fail**, and failures (for example a 429 "limit reached") are logged in the Airtable Errors table with a Slack alert. Keys live in n8n credentials only, never in Gradio. Other integrations (OpenAI, Cohere, Pinecone, Slack, Airtable) are also key-based APIs and are covered.

---

## 4. Use Case Exploration

### Research tasks the agent performs

| # | Task | Reader | Scope |
|---|---|---|---|
| 1 | **How do others solve this?** Common AI solutions at competitors and in the industry (Tavily, GNews) | Employee + CPO | MVP |
| 2 | **Evidence and size:** research numbers behind the problem and the fix (OpenAlex) | CPO | MVP |
| 3 | **Internal match:** which internal tool or approved method fixes it (RAG over internal PDFs), shown first | Employee | MVP |
| 4 | **External option:** an approved external tool, or one flagged "not on the approved list" | Employee | MVP |
| 5 | **Compliance status:** AI policy, works council, GDPR, EU AI Act → green / amber / red, with "under review by [department]" when escalated | Both | MVP |
| 6 | **Confidence and sources** on every recommendation; below the threshold the report says it is not sure | Both | MVP |
| 7 | **"No internal solution exists" flag** stored in Airtable | CPO | MVP (field only) |
| 8 | **Research loop:** re-query when evidence is weak | Both | GTM sprint |

### Report types

| Report | Reader | Content | Scope |
|---|---|---|---|
| **A: Fix for me** | Employee / OEE | Internal solution first, approved external alternative, steps, compliance status, confidence, sources, reference code, feedback box ("will use / won't use + why") | MVP |
| **B: Use-case card** | CPO / AI enablement | Question, department, internal and external answers, evidence, size, compliance, effort vs impact, feedback | MVP (one Airtable row per submission) |
| C: Portfolio digest (weekly / monthly) | CPO | Top friction themes, use-case ranking, "no internal solution" list → roadmap input | GTM sprint |
| D: Adoption and internal-tool gap | CPO + internal tool owners | Why people reject internal tools, adoption per department (groups of 5+ only) | GTM sprint |
| E: Compliance pipeline | Works council / Legal | Cases in review, turnaround, auto-cleared vs escalated | GTM sprint |
| F: Ops health | Owner | Errors, failed APIs, low-confidence rate | GTM sprint |

### Similar tools and services

| Type | Examples | What they do | What is missing |
|---|---|---|---|
| **Public AI tool directories** | There's An AI For That | Very large public catalog (over 50,000 listed tools in 2026) | Public and generic: no knowledge of internal approved tools, policy or works council rules, so it cannot pass a confidentiality check. Hard to navigate |
| **Enterprise AI governance intake** | ServiceNow AI Control Tower, OneTrust AI Governance, Credo AI, LogicGate | Use-case intake, approval workflows and inventories for governance teams | Built for governance teams, not employees. The submitter gets a process, not a solution; reviews can take weeks or quarters |
| **Fix My Process** | This project | Instant, compliant fix for the employee **and** a pre-scoped use case for governance | Combines both halves in one flow |

**Positioning:** directories give choice without compliance; governance platforms give compliance without help; Fix My Process gives both at the moment of friction.

### Future GTM sprints

| Sprint | Audience | Channel | Milestone | Success metric |
|---|---|---|---|---|
| **1. Close the loop** | CPO / AI enablement + internal tool owners | Scheduled n8n digest to Slack (Reports C and D), LLM reviews all logged feedback | First monthly roadmap input built from real submissions | % of "won't use internal tool" reasons categorised; "no internal solution" cases turned into roadmap items |
| **2. Meet them where they work** | Ops employees (pilot with 1 or 2 ops teams) | Slack Trigger entry point + PII redaction | 4-week pilot live in Slack | Submissions per week; internal tool adoption rate; feedback rate |
| **3. Smarter and trusted** | Works council, Legal, CPO | Research loop (LangGraph entry point), Report E, Notion ops digest (Report F) | Works council sign-off on the transparency and review process | % auto-cleared vs reviewed; review turnaround; % of reports above the confidence threshold |

### Feature and improvement backlog

Smaller items: features, fixes and improvements, not GTM sprints.

| Item | Type | Why |
|---|---|---|
| Save the execution ID on the Airtable row so the error workflow can find the reference code | Fix | Error Trigger may not receive the reference code |
| Async response: return the reference code at once and let Check status show the report | Fix (only if the timing test fails) | Webhook or Render timeouts on long runs |
| Access control for the app and the admin upload form | Feature | Nothing is password protected in the MVP |
| Cache API results for repeated questions | Improvement | Saves free-tier quota and time |
| Expand the calibration set beyond 15 cases and re-tune the threshold | Improvement | Better confidence scores |
| German and English reports | Feature | Kleinanzeigen works in both languages |
| Keep Render awake or move off the free plan for demos | Improvement | Free plan sleeps (about 1 minute to wake) |

---

## Known Gaps and Open Questions

| Type | Item | Plan |
|---|---|---|
| **Accepted tradeoff** | Free text may contain names; no PII redaction in the MVP | UI notice "Describe the process, not the people. Don't include names." LLM rule: reports never repeat personal names. Redaction in GTM sprint 2 |
| **Accepted tradeoff** | A Report B from a small department could point to one person | Department level only, never team; CPO summaries only for groups of 5+ |
| **Accepted tradeoff** | No password protection, including the admin upload form | Access control in the backlog |
| **To test** | 3 APIs, RAG and several LLM calls before the answer; timeouts possible | Time 3 test cases end to end through Gradio and the fallback form; force one error and check what the Error Trigger receives |
| **Open question** | Where does self-hosted n8n run so Render can reach its webhooks? | Decide before the build; Gradio needs a public `N8N_WEBHOOK_URL` |

---

## Sources

- [Tavily: credits and pricing](https://docs.tavily.com/documentation/api-credits)
- [GNews: pricing and plans](https://gnews.io)
- [OpenAlex: authentication and pricing](https://developers.openalex.org/api-reference/authentication) · [API key announcement, Jan 2026](https://groups.google.com/g/openalex-users/c/rI1GIAySpVQ)
- [ServiceNow: AI Control Tower, AI use case intake](https://www.servicenow.com/community/servicenow-ai-platform-forum/ai-without-chaos-a-deep-dive-into-ai-control-tower/m-p/3455272)
- [OneTrust: AI governance](https://www.onetrust.com/govern-ai-risk/)
- [Credo AI: GAIA governance agent](https://www.credo.ai/blog/governance-at-the-speed-of-ai-introducing-gaia-credo-ais-governance-agent-public-preview)
- [ToolDirectory.ai: AI tool directory counts, Sept 2026](https://tooldirectory.ai/blog/how-many-ai-tools-are-there-2026)
