# Confidence Calibration and Prompt Improvement

*Fix My Process · 10 Nov 2026 · 8 runs: 2 fixed inputs × 4 prompt versions, plus a 15-case study (19 runs)*

## 1. Setup

- **Inputs** (department "Other", no tools given):
  - **Good case:** weekly team update written from an aggregated KPI table. Expected: **green**, KAi Assist.
  - **Bad case:** CVs scored in a free online AI tool, with automatic rejections. Expected: **red**, core rules R1, R4, R7, no internal tool.
- **Versions:** v1 = original prompts. v2 to v4 = iterations on the Research Agent and Write Reports A + B prompts.
- **Rubric:** 6 checks per run, scored 1 / 0.5 / 0. Manual review against `KA-AI-POL-001` and `KA-AI-TOOLS-002`.
  - C1: the level is correct.
  - C2: no rule is cited that does not apply.
  - C3: the core rules are present.
  - C4: the internal tool is allowed for the data class.
  - C5: the external alternative is valid and the same in Report A, Report B and Airtable.
  - C6: the rest of the report is consistent (tool owner, no self-references).

## 2. Results

| Ver | Code | Level | Rules | Internal | External | Conf. | Score /6 | Main defect |
|---|---|---|---|---|---|---|---|---|
| v1 | FMP-3095 | ❌ Amber | A1, A5, R1, R3 | KAi Assist | Article title | 83 High | 1 | Wrong level; R rules in an amber case |
| v1 | FMP-3097 | ✅ Red | R1, R3, R4, R6 | ❌ KAi Assist (CVs are D4, tool max D3) | Unsourced company claim | 56 Med | 2 | Unsafe alternative |
| v2 | FMP-3100 | ✅ Green | G1, G2, G3, G5 | KAi Assist | M365 Copilot | 83 High | 5.5 | Wrong tool owner |
| v2 | FMP-3104 | ✅ Red | R1, R2, R3, R4, R7 | None | ❌ M365 Copilot (CVs into a D3 tool) | 76 High | 3 | Unsafe alternative scored High |
| v3 | FMP-3106 | ✅ Green | G1, G2, G5 | KAi Assist | M365 Copilot | 83 High | 5.0 | A5 source in a green case |
| v3 | FMP-3108 | ✅ Red | R1, R3, R4, R7 | None | None in field, generic tool in text | 77 High | 4 | Text fills an empty field |
| v4 | FMP-3110 | ✅ Green | G1, G2, G3, G5 | KAi Assist | Copilot in field, "none fits" in text | 90 High | 5.5 | Field and text disagree; wrong tool owner |
| v4 | FMP-3112 | ✅ Red | R1, R2, R3, R4, R7 | None | None | 62 Med | 4.5 | Points to an internal policy not a tool |


## 3. What the confidence score measures

`confidence = 100 × (0.3 × rerank + 0.7 × groundedness) − 20 per invented item − 10 per missing item`

The formula was recomputed for all 8 runs and matches. No penalty fired in any run.

| Finding | Evidence |
|---|---|
| It measures **source support**, not **decision correctness** | The wrong v1 green report and the correct v2 and v3 green reports all score 83. Correlation with the rubric: r = 0.38 |
| A wrong report can score High | FMP-3104 (Copilot for CVs) scores 76 High; the best red report (FMP-3112) scores 62 Medium |
| Rerank is biased against red cases | Green rerank is 0.67 in all runs; red is 0.11 to 0.24. Red reaches High only if groundedness is ≥ 0.98 |
| Poor repeatability | The same red input scores 56 / 76 / 77 / 62 (range 21 points, crossing the High line twice); green scores 83 / 83 / 83 / 90 |
| Groundedness decides the band | Red groundedness of 0.75 to 1.00 moves the score by up to 17.5 points; rerank moves it by at most 4 |

**Conclusion:** the score is useful as a "check the sources" signal. It is not a measure of compliance correctness. The 75 / 40 bands stay as judgement settings (see section 4).

## 4. 15-case study (9 Nov 2026)

### Setup

- **Cases:** 15 labelled cases (5 green, 5 amber, 5 red) written from the 4 knowledge-base PDFs, covering all 8 departments, each with 2 tools selected (`calibration/calibration_cases.csv`). R04 (R6) and R05 (R7) were skipped, so 13 cases ran.
- **Runs:** 1 per case, 3 for G01, A01 and R03 to check repeatability: 19 runs (FMP-3124 to FMP-3171), prompt v4.
- **Rubric:** 4 checks per run, scored 1 / 0, from the Airtable fields against the expected labels: level; core rule (expected rule cited, no rule from another level); internal tool; external tool.

### Results

| Check | Correct | Main errors |
|---|---|---|
| Level | 16 / 19 (84%) | R01 (personal ChatGPT with D3 financial notes) rated green; G02 (Ticket Lens on tickets, approved for D4) rated amber A3; 1 of 3 G01 runs rated amber A1 after choosing Zapier |
| Core rule | 14 / 19 (74%) | The 3 level misses; G5 cited in 2 amber cases (A02, A03); A6 missing for the public chatbot (A03) |
| Internal tool | 18 / 19 (95%) | G04: Miro AI, an external tool, in the internal field |
| External tool | 12 / 19 (63%) | Zapier (pilot, not approved) 3 times; Microsoft 365 Copilot for customer data 3 times |
| **Total** | **60 / 76 (79%)** | By level: green 71%, amber 79%, red 90% |

Other findings:

- **Report A hid the external tool:** all 19 reports said "No approved external tool fits this case"; in 9 of them the field named a tool.
- **Red reports had no safe alternative:** in 4 of 4 red runs the "Fix it" section pointed to itself ("Use the internal option above").
- **A5 over-cited:** cited in 8 runs, expected in 1 (A04).
- **R2 / R3 no longer cited for candidates:** R03 cited only R4 in 3 of 3 runs.
- **Repeatability:** G01 changed level once and named 2 different external tools in 3 runs; A01 named 2 different external tools; R03 gave the same answer 3 times.
- **Penalty:** fired once, correctly (G04, unknown internal tool, −20).
- **Duration:** 16 of 19 runs took 45 s or less; FMP-3124 took 234 s, over the app's 180 s timeout.

### What the confidence score measures (19 runs)

| Finding | Evidence |
|---|---|
| Still **source support**, not **decision correctness** | Correlation with the rubric: r = 0.35 (8-run set: 0.38) |
| Rerank carries the only signal | Rerank r = 0.39; groundedness r = 0.01, although groundedness has 70% of the weight. The wrong green R01 got groundedness 1.0 |
| High is not safe | 5 runs scored High, 2 of them wrong (G02 at 80, wrong level; A03 at 91, wrong rule) |
| Same answer, different score | R03 gave identical answers 3 times and scored 84 / 85 / 71 |

19 runs is a small sample: these are signals, not proof.

### Fixes after the study

| # | Fix | Where | Target | Status |
|---|---|---|---|---|
| 1 | Fixed lists for the tool fields: `internal_tool` = the 5 internal tools or None, `external_tool` = the 6 approved tools or None; external is None for customer data (D4) | Research Output parser schema, Research Agent prompt | Zapier 3 times, Miro AI in the internal field, Copilot for customer data 3 times | Applied |
| 2 | Report A uses `internal_tool` and `external_tool` as written; red cases without an internal tool get a fixed "no safe alternative" sentence; Report A never advises the flagged step | Write Reports A + B prompt | 9 of 19 reports where text and fields disagreed; 4 of 4 red reports | Applied |

### After the fixes

5 spot-check runs after fixes 1 and 2, reviewed by hand: all improved. They were not rescored on the rubric, so the 79% above is the before-fix baseline. An after-fix number needs a rescore of the 13 cases.

**Conclusion:** prompt fixes keep improving the reports; the confidence score still does not track correctness. The 75 / 40 bands stay. Next: deterministic Quality Gate checks for level / rule consistency and external tool data class, then rescore and set the bands from the results.
