# Project 3: Four Example Ideas (Student Board)

---

## Screen 1 — Same shape, four industries

```
Trigger  →  Collect data (≥3 free APIs)  →  Check it (RAG / trusted docs)  →  Report with sources
```

**The key question:** where does the data come from?

---

## Screen 2 — Example 1: Competitor report (Market research)

**User:** marketing manager at a sportswear brand
**Types:** a competitor's name ("Puma")
**Gets:** 1-page report: who they are, how they're doing, what's new, what it means for us

| Data | Where from | Cost |
|---|---|---|
| Company info | Web search API (e.g. Tavily) | Free tier |
| Latest news | News API (e.g. NewsAPI, GNews) | Free tier |
| Numbers | Finance API (e.g. Alpha Vantage) | Free tier |
| RAG | Competitor's **annual report PDF** + a short **"our company" doc you write** | Free |

```
1. Type "Puma"
2. Call 3 APIs → web info, news, numbers
3. Search the PDFs (RAG) → trusted facts
4. LLM writes the report, with sources
5. Send it (Slack, email, file)
```

---

## Screen 3 — Example 2: Interview prep report (HR and careers)

**User:** a job seeker with an interview next week
**Types:** company name + job ad link + GitHub username
**Gets:** 1-page prep: about the company, recent news, what they want, how my CV and projects match, which projects to talk about, my gaps, 5 likely questions

| Data | Where from | Cost |
|---|---|---|
| Company info & culture | Web search API (e.g. Tavily) | Free tier |
| Recent news | News API (e.g. NewsAPI, GNews) | Free tier |
| Job requirements | The **job ad page** (fetched from the link) | Free |
| My projects | **GitHub API**: repo names, descriptions, languages, READMEs | Free |
| RAG | **Your own CV** + a short **interview tips guide you write** | Free |

**What's expected** (job ad + research) ⟷ **What I have** (CV + GitHub)

```
1. Type company + job link + GitHub username
2. Call 4 sources → company info, news, job ad, my GitHub projects
3. Search CV + tips (RAG)
4. Compare: "job asks for APIs → talk about your weather-dashboard project"
            "job asks for Docker → no project yet, prepare an honest answer"
5. LLM writes the prep report, with sources → email or file
```

---

## Screen 4 — Example 3: Car part failure report (Automotive)

**User:** development engineer at a car manufacturer
**Trigger:** email with a test report + photos (rusty exhaust, cracked headlight)
**Gets:** 1 report per issue: what it is, seen before?, likely causes, design fix

| Data | Where from | Cost |
|---|---|---|
| Recalls | **NHTSA Recalls API** (US vehicle safety agency) | Free, no key |
| Driver complaints | **NHTSA Complaints API** | Free, no key |
| Technical research | **OpenAlex** (research papers) or web search | Free key |
| RAG | **10 fake documents you write**: past failure reports, design rules, material specs | Free |

```
1. Email arrives → read report + photos
2. Call 3 sources → recalls, complaints, papers
3. Search internal docs (RAG) → "seen this before?"
4. LLM writes failure report, with sources
5. Save to Drive + message engineers in Slack
```

---

## Screen 5 — Example 4: School book order report (Small business)

**User:** owner of a small school-book distributor (30 schools, 5 publishers)
**Trigger:** a school sends an order on Telegram / WhatsApp (text or photo of a handwritten list)
**Gets:** a priced order summary for the school + **every Monday**, a purchase report for the owner

| Data | Where from | Cost |
|---|---|---|
| The order | **Telegram / WhatsApp API** (text or photo) | Free |
| Books, publishers, prices | **Catalogue in Google Sheets** | Free |
| All orders so far | **Orders sheet** (Google Sheets) | Free |
| Grounding | **Exact lookup** in the catalogue (better than semantic search for exact titles and prices) | Free |

```
1. School sends a message (text or photo)
2. LLM reads it → school, class, book, quantity
3. Look up each book in the catalogue → price, publisher
4. Reply with a priced summary + save to the orders sheet
5. Every Monday → purchase report to Gmail / Slack
   (what to buy per publisher, schools not ordered yet, books not found)
```

> **Make it stronger:** every Monday, also research each publisher (web + news): new titles, price changes, delivery problems.

---

## Screen 6 — Find your own use case

**Look for a process that repeats:** every day, every Monday, done by hand.
**Automate it** → send a **report** to a tool people already use: Slack, Gmail, Notion, Google Sheets.

**Where to find ideas:**
- Your past job: what did you do every week that was boring and repetitive?
- A friend or family member's business: what do they still do by hand?
- Something you need yourself (like interview prep)

**About data:**
- Best: **≥3 external APIs** + research outside
- Also accepted: a real repeated business process **with no external API**, using the business's own data + a real report
- If you can, add **one research step**. It makes your project stronger.

| Your checklist | Your answer |
|---|---|
| Who is the user? | |
| Which process repeats? How often? | |
| What triggers the agent? | |
| Where does the data come from? | |
| What report, sent where? | |

---

## Screen 7 — What a GTM sprint looks like

GTM = **go-to-market**: how you take your MVP to **real users** after this week.
You plan **2–3 sprints**. They're **next steps**, not things you already built.

**NOT GTM (just a feature list):**
Sprint 1: add a dashboard · Sprint 2: add WhatsApp · Sprint 3: add more APIs
→ Who uses it? How do you reach them? How do you know it worked?

**A REAL GTM sprint: Sprint 1 for the school book order agent**

| | |
|---|---|
| **Goal** | Prove it saves time for one real distributor |
| **Audience** | 1 book distributor + 5 of their schools |
| **Channel** | Free 4-week pilot, introduced through the owner's network |
| **Deliverable** | Working bot + Monday report in Gmail + a short feedback form |
| **Success metric** | Order typing time per day: 2 h → under 20 min · 4 of 5 schools keep using it |

**Every sprint answers 5 things:** Goal · Audience · Channel · Deliverable · Metric
**Sprint 2 and 3 ideas:** reach 3 more distributors through publisher sales reps · offer a paid monthly plan
