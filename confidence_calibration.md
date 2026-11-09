# Confidence Calibration and Prompt Improvement

*Fix My Process · 9 Nov 2026 · 8 runs: 2 fixed inputs × 4 prompt versions*

## 1. Setup

- **Inputs** (department "Other", no tools given):
  - **Good case:** weekly team update written from an aggregated KPI table. Expected: **green**, KAi Assist.
  - **Bad case:** CVs scored in a free online AI tool, with automatic rejections. Expected: **red**, core rules R1, R4, R7, no internal tool.
- **Versions:** v1 = original prompts. v2 to v4 = iterations on the Research Agent and Write Reports A + B prompts:
  - a tool may only get data within its data class;
  - external alternatives only from the approved list;
  - cite only rules that apply, and the level follows the highest rule;
  - fixed text when no external tool fits.
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
| v3 | FMP-3106 | ✅ Green | G1, G2, G5 | KAi Assist | M365 Copilot | 83 High | 5.5 | A5 source in a green case |
| v3 | FMP-3108 | ✅ Red | R1, R3, R4, R7 | None | None in field, generic tool in text | 77 High | 4.5 | Text fills an empty field |
| v4 | FMP-3110 | ✅ Green | G1, G2, G3, G5 | KAi Assist | Copilot in field, "none fits" in text | 90 High | 5 | Field and text disagree; wrong tool owner |
| v4 | FMP-3112 | ✅ Red | R1, R2, R3, R4, R7 | None | None | 62 Med | 4 | Points to an internal option that does not exist |

**Improvement:** the score rose from 3 / 12 (25%) in v1 to 9 / 12 (75%) in v4. From v2 onwards:
- the level is correct in every run;
- CVs are no longer sent to KAi Assist;
- R1, R4 and R7 are always cited for the red case.

The differences between v2, v3 and v4 are within run-to-run noise (one run per input).

**Still open in v4:**
- R2 and R3 (employee rules) are cited for job candidates.
- Report A text does not always match the fields.
- The tool owner is written by the LLM and is sometimes wrong.

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

## 4. Backlog

**Deterministic Quality Gate checks** (code only, no new nodes, weights unchanged):

| # | Check | Effect | Would have caught |
|---|---|---|---|
| 1 | Rules match the level (red = R only, amber = A only, green = G only) | −20 per mismatch | FMP-3095 |
| 2 | R2 / R3 only when the problem is about employees (keyword list) | −20 per rule | FMP-3097, 3104, 3108, 3112 |
| 3 | D4 terms (CV, candidate, customer message, user ID) with a tool limited to D3 or lower | −20 | FMP-3097, 3104 |
| 4 | External tool must be one of the 6 approved or None; Quality Gate writes that Report A sentence | Fix | FMP-3095, 3110 |
| 5 | Tool owner from a lookup table, not from the LLM | Fix | FMP-3100, 3110 |

Applied to the same 8 runs:
- wrong reports would fall to 16 to 57;
- correct green reports would stay at 83 to 90;
- correlation with the rubric would rise from 0.41 to 0.73.

Checks 2 and 3 are keyword heuristics and can misfire on unusual wording.

**Full calibration:**
1. Build a labelled set of 15 to 20 cases (expected level, rules, tools).
2. Run each case 3 times.
3. Measure accuracy per band (target: High ≥ 90% correct) and repeatability (target: same band in 3 of 3 runs).
4. Then tune rerank scope, weights and the 75 / 40 thresholds from the data.
