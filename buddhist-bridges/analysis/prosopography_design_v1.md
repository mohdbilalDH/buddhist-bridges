# Prosopography Design v1 — Structured Biographical Analysis

**Phase:** 2 — Analysis Design · **Date:** 2026-08-17 · **Baseline:** frozen V3.0
**Answers:** Q0.1, Q1.2, Q2.2 (see `analysis_blueprint_v1.md` §3)

---

## 1. Principle

Prosopography here means **systematic comparison of the 43 carried people across structured dimensions** — not biography-writing. The output is a register, matrices, and a typology that the timeline and network consume.

## 2. Population

43 carried people: B1=18 (Silla/Gaya), B2=6 (Goryeo), B4=6 (colonial), B5=5 (1945–1990), B6=8 (1990–2026). Nationality: ~35 Korean (Silla/Goryeo/colonial/ROK), ~6 Indian, 1 UNCERTAIN, 1 other. Confidence: HIGH=19, MEDIUM=24. Status: VERIFIED=39, PARTIAL=4.

## 3. Comparison dimensions (variable → operationalization)

| Dimension | Frozen field(s) | Normalization needed |
|---|---|---|
| **Role** | `profession_role` (free text, ~40 distinct values) | Role taxonomy: `pilgrim-monk`, `scholar-monk`, `translator`, `master/patriarch`, `modern intellectual`, `poet/writer`, `academic`, `activist`, `institutional leader`, `bhikkhuni`, `non-Buddhist figure` (mapping table, auditable) |
| **Period** | `period` + `period_band` | none (already controlled) |
| **Tradition** | `religious_affiliation` (free text, ~30 values) | Tradition taxonomy: `Seon/Chan`, `Esoteric (Milgyo)`, `Yogacara`, `Vinaya`, `Hwaeom`, `Lay/Modern Buddhist`, `Non-Buddhist`, `Unknown` |
| **Movement** | `movement_status` (classification) | none: visited=12, studied=7, worked=4, planned=2, `-`=18 |
| **Mediation** | `buddhist_relevance` (classification) | none: PRIMARY=158 rows / MEDIATOR=19 / SECONDARY=17 (person-level counts derived) |
| **Texts** | PTX links (14 carried) | count + role (AUTHOR/TRANSLATOR/SUBJECT/READ) per person |
| **Institutions** | `institution_org` (free text) | mapped to I-#### (blueprint §7 item 5) |
| **Influence** | `direction_of_influence` + `exchange_types` | none: INDIA_TO_KOREA=27, KOREA_TO_INDIA=11, BIDIRECTIONAL=4, UNCERTAIN=1 |

## 4. Methods

1. **Structured register (V2, primary output).** One card per person: all dimensions above + evidence summary + source keys + classification rationale. This is the analytical backbone — the timeline and network read from it.
2. **Role × period matrix.** Rows = role taxonomy, columns = B1–B6. Reveals the shift from pilgrim-monk (B1) to institutional leader/academic (B6) — the quantitative face of Q2.2.
3. **Tradition × period matrix.** Shows the Esoteric/Yogacara dominance of B1–B2 vs Seon/Jogye and lay/modern in B5–B6.
4. **k-modes clustering (exploratory).** On categorical dimensions (role, tradition, movement, mediation, direction) to propose a typology — e.g., "pilgrim-monk", "scholar-translator", "institutional mediator", "modern intellectual", "non-Buddhist enabler". **Exploratory only**: n=43, results are hypotheses, not findings.
5. **Life-course sequence analysis.** For the 19 people with full lifespans: birth → ordination/study → travel → work → death sequences; compare B1 monks (travel early, die in Korea/China) vs B6 actors (study in India, return to institutional careers).
6. **Cohort comparison.** B1 (18) vs B6 (8): movement, direction, exchange types, institution attachment. Every comparison carries per-cohort source counts.

## 5. Missing-data handling (mandatory)

| Missingness | Count | Handling |
|---|---|---|
| No birth year | 24/43 | floruit span (APPROX) derived from band + dated activities; rendered as fuzzy, never as a point |
| No death year | 24/43 | same |
| Movement `-` | 18/43 | a real category (no physical movement — indirect/mediated connection), not missing data |
| Direction UNCERTAIN | 1/43 | shown as such |
| No institution mapping | ~7 | "no institution recorded" category |

Every breakdown includes an explicit `Unknown` category. A **missingness matrix** (dimension × person) is part of the register so users see what the analysis rests on.

## 6. Outputs

1. `prosopography_register_v1.csv` + rendered cards — 43 people × all dimensions.
2. `role_x_period_matrix` · `tradition_x_period_matrix` · `movement_x_direction` tables.
3. Typology table (from k-modes, labeled exploratory).
4. Cohort profiles (B1 vs B6, with source counts).
5. Missingness matrix.

## 7. Statistical caution

- n=43: **descriptive statistics only**. No significance tests, no inferential claims.
- Any apparent pattern (e.g., "B1 monks all travelled") must be checked against source density: B1's 18 people rest on a small primary core; B6's 8 people on news sources.
- The typology is a hypothesis generator for the next research phase, not a result.

## 8. How the five data limitations appear

| Limitation | Rendering |
|---|---|
| B3 zero carried | Cohort row "B3: 0 (see gap note)" — the register states the absence explicitly. |
| B1 small primary core | B1 cohort profiles carry their source counts; SPECULATIVE/legendary people (P-0007/0008) are excluded from the "documented" subset and analyzed separately. |
| B6 source-rich | B6 profiles carry NEWS-heavy source mix; single-source people (P-0055, P-0063) hatched/badged. |
| Single-source HIGH | Badged in the register; a "corroborated" filter isolates the defensible core. |
| Uneven density | Per-cohort source counts in every table; missingness matrix visible. |

## 9. Data prep required (blueprint §7, items 2, 4, 5, 8)

Floruit ranges for 24 people · role taxonomy · tradition taxonomy · institution mapping · density tables. All derived; frozen data untouched.