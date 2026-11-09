# Stack Decision: n8n vs LangGraph

**Project:** Kleinanzeigen "Fix My Process" Agent  
**Status:** Final, updated after the build, 10 Nov 2026.

---

## 1. Decision

**n8n (self-hosted) is the primary stack. LangGraph is not in the MVP.**

| Role | Choice | Responsibility |
|---|---|---|
| **Primary orchestration** | **n8n, self-hosted (2.13.2)** | All business logic: intake, research, RAG, compliance, two reports, quality gate, review, logging, errors |
| **Secondary (later)** | **LangGraph** | Only if a reasoning step needs to loop back and remember state. Would run as a small Python service behind an n8n HTTP Request node |
| **UI** | **Gradio on Render** | Form, Chat and Check status tabs. Calls n8n webhooks and shows the answer. No business logic |

### Final stack

| Layer | Tool | Use |
|---|---|---|
| LLM | OpenAI gpt-4o-mini | Research Agent (temperature 0.2), Reports A + B (0.4), groundedness judge (0) |
| Embeddings | OpenAI text-embedding-3-small (1536) | Internal PDFs and queries |
| Vector store | Pinecone (`fix-my-process-kb`, one namespace per document) | Policy, approved tools, works council, past projects |
| Rerank | Cohere rerank-v3.5 | Reranks Pinecone results and gives the relevance part of the confidence score |
| Research APIs | Tavily · GNews · OpenAlex | Web practice · news · research papers |
| Logging | Airtable | Submissions table and Errors table |
| Review and alerts | Slack | #ai-governance-review (notice for every case, Board decision for red), #fix-my-process-alerts (errors) |
| Use-case pages | Notion | One Report B page per case for the CPO / AI enablement team |

---

## 2. Why n8n fits this industry and problem

"Fix My Process" is an operations workflow, not an open-ended reasoning problem: intake from a form or chat, research, a compliance check, two reports for two readers, human review for edge cases, logging and error handling.  
The flow is mostly linear with a few branches, and n8n covers every step with a ready node: Webhook, IF, Slack send and wait for the AI Governance Board, Airtable for logging, Notion for use-case pages, and a separate error workflow.  
  
The value of the project only appears when the output reaches people and is tracked, so connecting business systems matters more than complex agent reasoning. n8n also makes the logic visible on one canvas, which helps non-technical stakeholders such as the OEE team and the works council understand what the agent does. To see where LLM gets involved and which data LLM is using, n8n is the best choice.

---

## 3. Why LangGraph is secondary for now

No MVP step needs reasoning that loops back and remembers state across steps.  
One research pass, one compliance classification and two report steps are fixed, predictable steps that n8n handles directly. LangGraph stays a clear upgrade path for a later sprint.

| Situation | n8n handles it? | Needs LangGraph? |
|---|---|---|
| Trigger → research → RAG → reports → response | ✅ Yes | No |
| Route red cases to review | ✅ Yes (IF node) | No |
| Send red cases to the AI Governance Board | ✅ Yes (Slack send and wait) | No |
| Retry a failed API call | ✅ Yes (Retry On Fail on regular nodes; an agent prompt rule for tool nodes, which have no retry setting) | No |
| Look up a report by reference code | ✅ Yes (Airtable search) | No |
| Compliance sends the flow back to research ("tool not approved, find an approved alternative, re-check") | Not cleanly | ⚠️ Yes (GTM sprint 3) |
| Multi-pass research loop that remembers which sources and queries it tried | Not cleanly | ⚠️ Yes (GTM sprint 3) |

**If LangGraph is added:** n8n still owns intake, logging, review, errors and the response. LangGraph only runs the looping reasoning step and returns JSON to n8n.

The calibration (`confidence_calibration.md`) showed that the weakest step is rule selection, not looping. The next fix for that is deterministic checks in the n8n Quality Gate, not LangGraph.

---

## 4. MVP flow in n8n (as built)

**In one line:** Trigger → Collect data (3 free APIs) → Check it (RAG / trusted docs) → Compliance → Report with sources → Log and reply

```
1. Employee describes the problem   →  Gradio form or chat (n8n form / chat as backup)
2. Call 3 APIs                      →  web practice (Tavily), news (GNews), research papers (OpenAlex)
3. Search the internal PDFs (RAG)   →  policy, approved tools, works council, past projects
4. Compliance check                 →  green / amber / red with policy rule IDs
5. LLM writes two reports           →  A: employee · B: CPO / AI enablement, with sources
6. Quality gate                     →  confidence = 0.3 × rerank + 0.7 × groundedness, minus penalties
                                       High ≥ 75 · Medium 40-74 · Low < 40; banner below High
7. Log and reply                    →  Airtable row + reference code, report on screen, feedback box
8. Hand-off                         →  Report B page in Notion + notice in #ai-governance-review
```

| n8n workflow | Starts when | What it does |
|---|---|---|
| **Main workflow** (one canvas) | An employee submits a problem | Steps 1 to 8. Check status and feedback use the same Airtable row |
| ↳ Review branch | A case is red | AI Governance Board decides in Slack (Add to pipeline / Dismiss for now); the user never waits |
| ↳ Document upload | The AI enablement team uploads a PDF | Extract → chunk → OpenAI embeddings → Pinecone namespace |
| **Error workflow** (separate) | A main-chain node fails | Airtable Errors row + Slack alert (`error_handling_proofing.md`) |

---

## 5. Red flags this decision avoids

| Red flag | How it is avoided |
|---|---|
| Over-engineering | One primary stack; LangGraph only when a looping step is proven necessary |
| Under-engineering | RAG over four internal PDFs, because the answer depends on internal rules and tools |
| Ignoring errors | Retries on every node that supports them, error workflow, Airtable Errors table, 13 forced failures tested |
| Poor context management | Separate namespaces per document type, rerank, quality gate; the LLM writes the search queries |
| No quality control | Groundedness judge, code checks on tools, document IDs, URLs and rule IDs; calibration documented |
| Missing ops thinking | Triggers, human review, logging and status lookup are part of the MVP, not an afterthought |