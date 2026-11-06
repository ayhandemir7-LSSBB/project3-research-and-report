# Project 3: Project Selection

**Project:** Kleinanzeigen "Fix My Process" Agent
**Type:** Autonomous Company Research & Report Generation Agent
**Company:** Kleinanzeigen (Germany's largest classifieds marketplace: C2C second-hand, B2C, real estate)
**Users:** Kleinanzeigen employees: operations teams, the operational excellence (OEE) team, and the CPO / AI enablement teams

---

## 1. Problem Definition

**What industry problem are we solving?**

Kleinanzeigen is moving to become a standalone company. The context: Adevinta, owned by Permira and Blackstone since 2024, is breaking up its portfolio. It has sold Spain, exited willhaben and is planning a mobile.de IPO. During a change like this, three things happen at once:

1. **Employees feel friction every day**, such as repeated manual tasks, slow processes and unclear tools, but they have no simple way to turn a frustration into a solution.
2. **AI enablement teams need real use cases** with evidence. Instead, they get vague ideas or top-down guesses about what operations needs.
3. **Every AI or process idea must pass German rules**: the internal AI policy, the approved tools list, the works council (Betriebsrat) agreement, GDPR and the EU AI Act. Nobody checks this early, so good ideas stall late.

Today, the steps from "this is annoying" → research → compliance check → proposal are done by hand, slowly, or not at all.

**Who is the report for?**

| Reader | What they need | What "useful" means |
|---|---|---|
| **Operations employee / team lead + OEE team** | Help to fix the problem now | Practical steps using **approved** tools only, ready the same day |
| **CPO / AI enablement team** | A list of qualified use cases | Evidence, size of the problem, compliance status and effort vs impact, so they can prioritise |

**One submission, two reports.** The employee describes the problem once. Operations gets help right away, and leadership gets a scoped, compliant use case. Bottom-up demand automatically feeds a top-down AI portfolio.

---

## 2. How We Chose This Project

### Options considered

| # | Idea | User | Verdict |
|---|---|---|---|
| A | **Team AI & Friction Report**: researched AI/process fixes with a compliance check | CPO / AI enablement | Strong, but top-down only |
| B | **"What's changing for me" briefing**: weekly transition news per department | All employees | Good for culture, weak research value |
| C | **AI Use-Case Scout**: employee types their role and tasks, gets AI help | Operations employees | Strong bottom-up, but no portfolio view |
| D | **Retention Risk Radar**: pulse data vs job market | Managers / People team | Reports *about* employees, so high works council and GDPR risk |
| **A + C** | **"Fix My Process"**: one input, shared research, two reports | Ops + OEE **and** CPO / AI enablement | ✅ **Selected** |

### Why A + C combined

- **Same facts, different readers.** The web research and the internal documents (policy, tools, works council, past projects) are the same for both. Only the LLM prompt and the report format change.
- **Small extra scope.** It's one pipeline with one extra LLM step and one extra send step (roughly 15–20% more work).
- **The employee is the user.** People get help; they are not monitored. This avoids the works council and GDPR problems of option D.
- **It fits the transformation role.** It connects the CPO / AI enablement team and the OEE team in one flow and covers employee experience, AI enablement and process improvement.
- **It follows the course template exactly:** type → 3 APIs → RAG → report with sources → send.

---

## 3. How It Works

```
1. Employee types:  team + pain point
                    e.g. "Customer Support C2C: hours every day on 'is this buyer a scammer?' tickets"

2. Call 3 APIs ──────────────────────────────────────────┐
   • Web search (Tavily)  → how others solve it          │
   • News (GNews/NewsAPI) → latest tools & trends        │  shared
   • OpenAlex             → research numbers & evidence  │
                                                         │
3. Search internal PDFs (RAG) ───────────────────────────┘
   • AI policy + approved tools
   • Works council agreement summary
   • Past improvement projects (lessons learned)
   • Transformation goals

4. Compare "what's possible" (external) ⟷ "what's allowed & what we tried" (internal)
   then branch into two prompts:
   ├─ Report C → Ops employee + OEE team     "How to fix this now"
   └─ Report A → CPO / AI enablement team    "Use-case brief"

5. Send
   • Report C → Slack DM to the employee (+ OEE channel)
   • Report A → AI enablement Slack channel + row in a use-case backlog sheet
   • Both saved to Google Drive
```

### Example of the compare step

| What others do (external) | What our docs say (internal) | Result |
|---|---|---|
| Vinted uses AI to pre-sort fraud tickets | AI policy allows ticket classification with an approved tool | ✅ Quick win |
| Some companies track agent speed with AI | Counts as performance monitoring → works council approval needed | ⚠️ Needs works council |
| A chatbot answers buyers directly | A 2024 pilot failed (see lessons-learned log) | ❌ Avoid, or redesign first |

---

## 4. Data Sources

| Data | Where from | Cost |
|---|---|---|
| How other companies solve the problem | **Tavily** web search API | Free tier |
| Latest AI tools, trends and news | **GNews / NewsAPI** | Free tier |
| Research numbers (time saved, error rates, adoption) | **OpenAlex** API | Free |
| Trusted internal facts (RAG) | **4–5 synthetic PDFs written by us** (see below) | Free |
| Backlog of use cases | **Google Sheets** | Free |
| Delivery | **Slack** + **Google Drive** | Free |

### Internal documents for RAG (synthetic, written for this project)

1. **AI Usage Policy**: what is allowed, what is forbidden, data classes
2. **Approved Tools List**: tools, owners, the data each is cleared for
3. **Works Council Agreement Summary**: what needs co-determination (e.g. anything that monitors performance or behaviour)
4. **Lessons Learned Log**: past improvement and AI pilots, what worked and what failed
5. **Transformation Goals**: standalone-company priorities and employee experience targets

All internal data is **synthetic**. No real employee or company-confidential data is used.

---

## 5. The Two Reports

| | **Report C: Ops / OEE** | **Report A: CPO / AI Enablement** |
|---|---|---|
| Reader | Employee, team lead, OEE coach | Product and AI enablement leads |
| Question | "What can I do about this tomorrow?" | "Should we invest in this?" |
| Tone | Practical, step by step | Business case |
| Contents | Quick wins with approved tools only · how to start · who can help · what to avoid | Problem size · evidence and numbers · how others solved it · compliance status ✅/⚠️/❌ · effort vs impact · priority suggestion |
| Length | ½ page | 1 page |
| Sources | Yes, every claim linked | Yes, every claim linked |

**Quality rule:** the two reports must read clearly differently. If they are the same text with different headings, the split adds no value.

---

## 6. Course Checklist

| Question | Answer |
|---|---|
| Who is the user? | Kleinanzeigen operations employees / team leads (input + Report C) and the CPO / AI enablement team (Report A) |
| Which process repeats? How often? | Employees raise process pain points every week; today nobody researches them, checks compliance or turns them into use cases in a structured way |
| What triggers the agent? | The employee types the problem (form, Slack command or chat) |
| Where does the data come from? | Tavily + GNews + OpenAlex, plus RAG on 4–5 internal PDFs |
| What report, sent where? | Report C → Slack DM / OEE channel; Report A → AI enablement channel + backlog sheet; both saved to Drive |

---

## 7. Scope

### In scope (MVP this week)
- One input form
- 3 external APIs
- 4–5 synthetic internal PDFs for RAG
- 2 LLM prompts (Report A and Report C)
- 2 delivery channels (Slack + Sheets/Drive)
- Testing with 3–4 sample problems:
  - Scam-check tickets in C2C Customer Support
  - Manual listing reviews in Real Estate
  - B2B dealer onboarding paperwork
  - Repeated questions to internal IT

### Out of scope (moved to the GTM sprints)
- Monday summary of all submissions for OEE
- Dashboard
- Employee voting on use cases
- Automatic routing to different teams
- Feedback loop and report rating

---

## 8. Stack Choice (to decide)

| | n8n | LangGraph |
|---|---|---|
| Strength | Fast to build, visual, easy to demo to non-technical leaders | Real multi-step agent that can decide which research to run |
| Branch into 2 reports | Simple (one merge node → two LLM nodes) | Simple (two writer nodes) |
| Fit for this project | Best for a fast, clear demo | Best to show agent reasoning |

**Decision:** _TBD_

---

## 9. Ethics and Risks

- **Synthetic data only.** No real employee, customer or confidential Kleinanzeigen data.
- **Employees are helped, not monitored.** The agent never scores or tracks people.
- **Works council awareness is built in.** Any idea that touches performance or behaviour monitoring is flagged ⚠️.
- **Sources on every claim**, so readers can check the research.
- **Public framing.** The standalone context is described only from public news (the Adevinta breakup and the mobile.de IPO plans).

---

## 10. Next Steps

1. Write the 4–5 synthetic internal PDFs
2. Choose the stack (n8n or LangGraph) and write down why
3. Write the two report templates and prompts
4. Build the pipeline and test with 4 sample problems
5. Plan 2–3 GTM sprints (goal · audience · channel · deliverable · metric)

---

## Sources

- [Reuters via Investing.com: Permira plans 2026 mobile.de IPO](https://ph.investing.com/news/stock-market-news/permira-plans-2026-ipo-for-mobilede-with-potential-10bn-valuation-reuters-93CH-1627402)
- [Vend Marketplaces: Adevinta Spain divestment completed](https://www.inderes.fi/en/releases/vend-marketplaces-asa-divestment-of-adevinta-spain-completed-expected-capital-distribution-of-eur-282-million)
- [Adevinta explores breakup / Spain sale (May 2025)](https://whbl.com/2025/05/16/adevinta-explores-sale-of-its-spanish-business-as-owners-pursue-break-up-sources-say/)
- [Who owns Kleinanzeigen](https://www.uamr.de/wem-gehoert-ebay-kleinanzeigen/)
- [Kleinanzeigen without eBay: what changes](https://onlinemarketing.de/unternehmensnews/kleinanzeigen-ohne-ebay-was-sich-aendert)
- [Glassdoor: Kleinanzeigen employee reviews](https://www.glassdoor.co.in/Reviews/Kleinanzeigen-Reviews-E9306098.htm)
