# Fix My Process Agent

An employee describes a process problem once. An n8n agent researches it, checks it against internal rules and tools, and returns a compliant fix (Report A) plus a use-case card for the CPO / AI enablement team (Report B). Demo company: Kleinanzeigen, with fictional internal data.

## Architecture

**In one line:** Trigger → Collect data (3 free APIs) → Check it (RAG / trusted docs) → Compliance → Report with sources → Log and reply

```mermaid
flowchart TD
    subgraph MAIN["n8n main workflow"]
        U["1. Employee describes the problem<br/>Gradio form or chat<br/>(backup: n8n form / chat)"] --> V["Validate input<br/>Airtable row + reference code FMP-xxxx"]
        V --> API["2. Call 3 APIs<br/>Tavily · GNews · OpenAlex"]
        V --> RAG["3. Search internal PDFs (RAG)<br/>Pinecone + Cohere rerank"]
        API --> C["4. Compliance check<br/>green / amber / red"]
        RAG --> C
        C --> R["5. LLM writes Report A + Report B<br/>with sources and confidence"]
        R --> Q{"6. Quality gate<br/>score at least 85% and sources?"}
        Q -- "yes" --> L["7. Log in Airtable and reply"]
        Q -- "no" --> LC["Add 'low confidence' banner"]
        LC --> L
        L --> UI["Report A on screen<br/>+ feedback box"]
    end

    C -- "amber / red" --> REV["Review branch, user does not wait<br/>Slack #ai-governance-review"]
    REV --> DEC["AI Governance Board decision<br/>updates Airtable, visible in Check status"]
    UI -- "feedback" --> FB["Airtable: same row"]

    subgraph UP["n8n document upload"]
        PDF["Upload PDF"] --> EX["Extract text and chunk"] --> EMB["Cohere embeddings"] --> PC["Pinecone namespace"]
    end
    PC -.-> RAG

    subgraph ERR["n8n error workflow"]
        E["Any step fails"] --> EL["Airtable Errors row + Slack alert"]
    end
```

| Part | What it does |
|---|---|
| **Main workflow** | Steps 1 to 7: research, RAG, compliance, two reports, quality gate, log and reply |
| **Review branch** | Sends amber / red cases to the AI Governance Board; the user gets the report at once with an "under review" banner |
| **Document upload** | Adds or replaces one of the 4 internal PDFs in Pinecone |
| **Error workflow** | Logs failures in Airtable and alerts the owner in Slack |

## Tool list
_To be completed._

## Setup
_To be completed._

## How to run
_To be completed._

## Stack decision
See [`stack_decision.md`](stack_decision.md).

## Future GTM sprints
See [`gtm_future_sprints.md`](gtm_future_sprints.md).
