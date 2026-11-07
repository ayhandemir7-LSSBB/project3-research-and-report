# agents.md: Fix My Process Agent
 
## Purpose
A tool that turns an employee's process problem into a researched, compliance-checked fix. Demo company: Kleinanzeigen (fictional internal data). The employee describes the problem once; an n8n workflow researches it with 3 APIs, checks 4 internal PDFs (AI policy, approved tools, works council agreement, past projects) with RAG, classifies compliance as green / amber / red, and returns two reports with sources: A for the employee (fix with internal tool first), B for the CPO / AI enablement team (use-case card). Edge cases go to the AI Governance Board in Slack; the user never waits. Everything is logged in Airtable.
 
## Stack & run
- **n8n (self-hosted):** primary stack. All logic, all LLM prompts, all scoring and compliance
- **Python 3.12 + Gradio 6** (`app.py`): UI only, deployed on Render (`0.0.0.0` + `PORT`, theme and css in `launch()`)
- Services: OpenAI gpt-4o-mini · Cohere (embeddings, rerank) · Pinecone · Tavily · GNews · OpenAlex · Airtable · Slack
- Install: `pip install -r requirements.txt` · Run: `python app.py`
- Env vars in `.env` (copy `.env.example`): `N8N_WEBHOOK_URL`, `WEBHOOK_SECRET`. All API keys live in n8n credentials only. Never commit `.env`.
## Repo map
- `app.py`: Gradio UI with Form, Chat and Check status tabs plus a feedback box; calls the n8n webhooks only
- `n8n/`: exported workflows, credentials stripped (main workflow with review branch and document upload; error workflow)
- `samples/`: sample reports (.md), at least 2 on different problems
- `README.md`: setup, architecture diagram, tool list, how to run
- `stack_decision.md`: n8n vs LangGraph and why
- `gtm_future_sprints.md`: 2 to 3 sprints with goal, audience, channel, deliverable, metric
## Conventions
- `app.py` stays thin: build the request, call the webhook, show the response. Short functions with `#` comments
- Webhook paths: `/form`, `/chat`, `/status`, `/feedback`; every request sends the `WEBHOOK_SECRET` header
- Department is the only identity field; the chat session ID lives in Gradio State only
- Prompts are edited in n8n, not in Python or text files
- Every report cites sources (internal doc ID and section, or URL); compliance cites policy rule IDs (G1-G5, A1-A7, R1-R7)
- Quality threshold (about 85%) is one config value in n8n, calibrated on test cases
- Clear errors in the UI when n8n is unreachable or returns an error
- Commit messages say what changed, e.g. "add status tab"
## Definition of Done (agent changes)
- The card's check passes and is shown (PASS / FAIL)
- Touches only the active card
- Existing behaviour still works
- No secrets committed
## Never do
- Commit `.env`, API keys or credential IDs
- Put business logic, LLM calls or API keys in `app.py`
- Store names, login IDs or emails anywhere
- Expand into the Won't list (LangGraph, Slack entry point, research loop, PII redaction, Notion) without agreement
- Invent facts, figures, prices or tool features
- Work directly on `main`, or run `git commit` / `git push` (print the commands instead)
- Use em dashes in docs
## How we use agents
- One card at a time; paste the card ID and name into the prompt
- Point the agent at this file first: "Read agents.md, then do card 2.1"
- Work in `workbench_<card>.ipynb` (git-ignored): check branch, back up, PASS/FAIL checks, undo cell
- Review the agent's changes before committing