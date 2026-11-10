# Cost per Run

*Fix My Process · 10 Nov 2026 · prices checked 10 Nov 2026 (USD unless stated) · tokens measured in n8n executions · settings read from the v5 workflow export (`n8n_workflows/`)*

## 1. Summary

- **Expected cost: $0.021 per run** at list prices, **$21 per 1,000 runs**. 
- **Demo today: $0.006 per run.** On the free tiers, only the OpenAI calls are paid. **$6 per 1,000 runs**. 
- **The LLM is only 28% of the cost.** Tavily (38%) and Cohere (29%) are the main drivers, so a bigger model would barely move the total, while caching or a Tavily volume plan would.
- **First free limit:** the Cohere trial allows about 330 runs a month (3 calls per run).
- **Range:** $0.055 in the worst case.

## 2. What one run calls

Check status, feedback and the Error Handler use only Airtable and Slack, so they have no per-call cost.

| Node | Calls per run | Billed by | Setting that drives the cost |
|---|---|---|---|
| OpenAI Model (agent), gpt-4o-mini | 3: tool calls, final answer, Research Output auto-fix | Tokens | Chat Memory window 10 messages |
| OpenAI Model (reports), gpt-4o-mini | 1 (2 if the Reports auto-fix runs) | Tokens | Report A 300 to 450 words |
| OpenAI Model (judge), gpt-4o-mini | 1 | Tokens | Raw tool results capped at 30,000 characters |
| OpenAI Embeddings (search), text-embedding-3-small | 4 (one per Pinecone search) | Tokens | 1536 dimensions |
| Pinecone searches | 4 | Read units | topK 8 per namespace |
| Cohere Reranker | 2 (only Search Approved Tools and Search Policy use it) | Searches | Chunks max 1,200 characters, so 1 search unit per call |
| Cohere Rerank Score | 1 | Searches | rerank-v3.5, top_n 3 |
| Tavily Web Search | 1 | Credits | Only `query` is sent, so the default basic depth applies (1 credit) |
| OpenAlex Research | 1 | Calls | `search` parameter (keyword search), `per-page` 5 |
| GNews Search | 1 | Monthly plan | `max` 5 |

**Chat:** every chat message is a full run (all 7 tools), plus up to 10 earlier messages from Chat Memory. A follow-up message therefore costs at least one run.

## 3. Prices used

| Service | Price | Free tier |
|---|---|---|
| gpt-4o-mini | $0.15 per 1M input tokens, $0.60 per 1M output tokens | None |
| text-embedding-3-small | $0.02 per 1M tokens | None |
| Cohere Rerank 3.5 | $2.00 per 1,000 searches (one search = 1 query + up to 100 documents of up to 500 tokens) | Trial: 1,000 calls a month, non-production |
| Tavily | $0.008 per credit pay-as-you-go; monthly plans $0.0075 to $0.005 per credit | 1,000 credits a month |
| OpenAlex | Keyword search $1 per 1,000 calls; list / filter $0.10 per 1,000 | $1 a day with a free API key |
| Pinecone | Standard: $16 to $18 per 1M read units, $50 a month minimum | Starter: up to 1M read units a month |
| GNews | Essential €49.99 a month (1,000 requests a day) | 100 requests a day, non-commercial or testing only |
| Airtable | Team $20 per seat a month (annual), $24 monthly; 50,000 records per base | 1,000 records per base |
| Render | Starter $7 a month, always on | Free instance sleeps after 15 minutes, about 1 minute to wake |

## 4. Measured tokens (Ticket Lens case)

| Call | Input tokens | Output tokens | Cost |
|---|---|---|---|
| Agent run 1: 7 tool calls | 2,123 | 177 | $0.00042 |
| Agent run 2: final answer | 14,072 | 637 | $0.00249 |
| Agent run 3: Research Output auto-fix | 1,605 | 634 | $0.00062 |
| Write Reports A + B (1 call, no auto-fix) | 2,012 | 690 | $0.00072 |
| Groundedness Check | 10,127 | 139 | $0.00160 |
| **Total** | **29,939** | **2,277** | **$0.00586** |

Each tool ran once. The judge is 27% of the LLM cost because it reads the raw tool results.


## 5. Free-tier limits and fixed monthly costs

| Service | Free limit | Breaks at about |
|---|---|---|
| Cohere | 1,000 calls a month, non-production | **330 runs a month (first limit)** |
| Tavily | 1,000 credits a month | 1,000 runs a month |
| Airtable | 1,000 records per base (Submissions and Errors share the base) | 1,000 submissions in total |
| OpenAlex | $1 a day | 1,000 runs a day |
| GNews | 100 requests a day, non-commercial | 100 runs a day, or any company use |
| Pinecone | 1M read units a month | Far above pilot volume |
| Render | Sleeps after 15 minutes | Any user-facing use |

**Fixed costs for a pilot** (always on, company use): Render Starter $7 + 1 Airtable Team seat $20 = **$27 a month**, plus GNews Essential €49.99 a month, because the free plan is for non-commercial use only. Pinecone stays on Starter. Cohere and Tavily have no fixed fee on pay-as-you-go.

| Runs a month | Variable (expected) | Fixed | Total |
|---|---|---|---|
| 300 | $6 | $27 + €49.99 | $33 + €49.99 |
| 1,000 | $21 | $27 + €49.99 | $48 + €49.99 |
| 3,000 | $63 | $27 + €49.99 | $90 + €49.99 |

## 6. Cost levers

| # | Lever | Saving per run | Note |
|---|---|---|---|
| 1 | Cache API results for repeated questions (backlog) | Up to $0.015 on a cache hit | Saves the tool costs and the free-tier quota |
| 2 | Tavily monthly plan instead of pay-as-you-go | $0.003 (−14%) | Only at volume |
| 3 | Judge evidence cap 30,000 → 15,000 characters | $0.0006 (−3%) | Recalibrate the confidence score after the change |
| 4 | Fix the Research Output first parse | $0.0006 (−3%) | Known gap: the auto-fix call returns the same content |
| 5 | Remove Cohere Rerank Score | $0.002 (−10%) | **Not recommended:** rerank is the only confidence input that tracks correctness (r = 0.39) |
| 6 | Bigger model (for example GPT-5.4 mini) | Increases cost | The LLM is 28% of the cost; dismissed for cost and latency |


## Sources

- [OpenAI API pricing](https://developers.openai.com/api/docs/pricing), [text-embedding-3-small](https://developers.openai.com/api/docs/models/text-embedding-3-small)
- [Cohere API pricing overview (Rerank 3.5)](https://pecollective-com.pages.dev/tools/cohere-pricing/), [Cohere search unit rules](https://apicostcalc.com/cohere-vs-voyage-vs-jina-rerank-cost-calculator.html)
- [Tavily API credits](https://docs.tavily.com/guides/api-credits), [Tavily Search API reference](https://docs.tavily.com/api-reference/endpoint/search)
- [OpenAlex API pricing](https://developers.openalex.org/api-reference/authentication)
- [GNews plans](https://gnews.io)
- [Pinecone cost guide](https://docs.pinecone.io/guides/manage-cost/understanding-cost), [Pinecone plan rates](https://www.withorb.com/pricing-atlas/pinecone)
- [Airtable plans](https://www.capterra.com/p/146652/Airtable/pricing/)
- [Render pricing](https://render.com/pricing), [Render free instances](https://render.com/articles/how-much-does-cloud-application-hosting-cost-for-small-businesses)
