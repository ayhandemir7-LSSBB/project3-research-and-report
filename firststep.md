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

## 2. How I Chose This Project

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
