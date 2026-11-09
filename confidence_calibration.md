# Confidence Calibration and Prompt Improvement

*Fix My Process · 10 Nov 2026 · 8 runs: 2 fixed inputs × 4 prompt versions*

## 1. Setup

- **Inputs** (department "Other", no tools given):
  - **Good case:** weekly team update written from an aggregated KPI table. Expected: **green**, KAi Assist.
  - **Bad case:** CVs scored in a free online AI tool, with automatic rejections. Expected: **red**, core rules R1, R4, R7, no internal tool.
- **Versions:** v1 = original prompts. v2 to v4 = iterations on the Research Agent and Write Reports A + B prompts:
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
| It measures **source support**, not **decision correctness** | The wrong v1 green report and the correct v2 and v3 green reports all score 83. Correlation with the rubric: r = 0.41 |
| A wrong report can score High | FMP-3104 (Copilot for CVs) scores 76 High; the best red report (FMP-3112) scores 62 Medium |
| Rerank is biased against red cases | Green rerank is 0.67 in all runs; red is 0.11 to 0.24. Red reaches High only if groundedness is ≥ 0.98 |
| Poor repeatability | The same red input scores 56 / 76 / 77 / 62 (range 21 points, crossing the High line twice); green scores 83 / 83 / 83 / 90 |
| Groundedness decides the band | Red groundedness of 0.75 to 1.00 moves the score by up to 17.5 points; rerank moves it by at most 4 |

**Conclusion:** the score is useful as a "check the sources" signal. It is not a measure of compliance correctness. The 75 / 40 bands stay as judgement settings until a calibration is done.