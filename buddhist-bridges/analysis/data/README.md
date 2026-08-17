# Data-Preparation Layer — Provenance & README

**Phase:** 2, Step 1 (blueprint §7) · **Date:** 2026-08-17 · **Status:** COMPLETE, validated
**Input:** frozen V3.0 (`buddhist-bridges/v3.0_frozen/`, read-only — SHA-256 verified unchanged)
**Build:** `buddhist-bridges/analysis/build_derived_tables.py` (re-runnable)
**Validation:** `buddhist-bridges/analysis/validate_derived_tables.py` — **0 errors / 0 warnings**

## 1. Provenance method (applies to every table)

1. **Read-only input.** All tables are derived from the frozen CSVs; the frozen files are never written. Validation V8 re-checks SHA-256 hashes against the VERSION.md manifest after every build.
2. **Every row carries** `basis` (what in the frozen data the value rests on), `provenance` (this document + build script), `precision` (APPROX / YEAR / UNDOCUMENTED), and `confidence` (HIGH/MEDIUM/LOW).
3. **No invented dates or coordinates.** Where the frozen data contains no dated activity, the derived value is `UNDOCUMENTED` (empty range) — never an estimate. Region centroids are explicitly labeled `REGION_CENTROID` approximations with uncertainty radii, for cartographic anchoring only.
4. **Historical event dates vs evidence dates are kept distinct.** Translation dates come from the text records (the translation's own date), not from the date a source was accessed. The source-mix table counts *sources cited by records*, never record dates.
5. **Multi-affiliation preserved.** The tradition taxonomy allows up to three categories per person where the raw affiliation justifies it (e.g., P-0003 Hwaeom + Mahayana; P-0062 Jogye Seon + Theravada-oriented).
6. **B3 is treated as "no carried records under current criteria," not proof of no Buddhist activity.** No derived table fills the Joseon gap; the 11 excluded B3 rows remain EXCLUDE in the classification and are only referenced, never promoted.

## 2. Tables (10 files in `buddhist-bridges/analysis/data/`)

| File | Rows | Content | Key derivation rule |
|---|---|---|---|
| `region_centroids.csv` | 9 | Centroids for the 9 non-point places (kingdoms/regions) | Historical-capital/region centroids from standard geographic knowledge; `REGION_CENTROID`, precision APPROX, uncertainty radius 100–600 km |
| `person_floruits.csv` | 20 | Floruit/activity windows for carried people without birth years | Documented activity only (reigns, journeys, degrees, publications); precision APPROX |
| `travel_date_ranges.csv` | 14 | APPROX date ranges for undated travels | Anchored to person floruit; 4 rows `UNDOCUMENTED` (no dated activity in frozen data); scope column included (4 of 14 are EXCLUDE) |
| `tradition_taxonomy.csv` | 43 | Normalized tradition categories for all carried people | 11 controlled categories; multi-affiliation (up to 3) where justified; raw affiliation preserved |
| `institution_mapping.csv` | 43 | `institution_org` → I-#### mapping | MAPPED (13) / PARTIAL (3) / UNMAPPED (20) / NO_INSTITUTION (7); mapped IDs verified against institutions.csv |
| `translation_dates.csv` | 6 | Dates for the 6 PTX TRANSLATOR links | From texts.csv date field (the translation record); L-0113 discrepancy flagged (see §4) |
| `event_end_dates.csv` | 19 | Verification table | **Finding: all 19 events already carry end dates in the frozen data — blueprint §7 item 7 required no derivation** |
| `density_by_decade.csv` | 54 | Carried records per decade by entity type | Explicit dates only (birth_year, travel_start_year, text date, founded_year, event start_date); undated never imputed |
| `undated_counts.csv` | 8 | Carried records without explicit dates, by entity type | Companion to density table |
| `source_mix_by_band.csv` | 27 | Source types cited by carried records per band | **Only PEOPLE and EVENTS carry `source_ids` in the frozen schema** (see §4); resolved via source_id → source_type |

## 3. Row-count reconciliation

- Floruits: 20 people (blueprint estimated 24 — the estimate used the all-people birth-year count; among the **43 carried** people the true count is 20).
- Travel ranges: 14 undated travels (frozen CSV), of which 10 are carried (KEEP) and 4 EXCLUDE (T-0029, T-0030, T-0032, T-0041 — non-Buddhist academic travels; kept in the table for completeness).
- Density: dated carried records only; undated counts listed separately (PEOPLE=20, TRAVELS=10, INSTITUTIONS=4, PLACES=32, RELS=10, PPL=18, PTX=14, PERSON_EVENT=13 — the link tables carry no dates by design).

## 4. Unresolved derivations & flagged discrepancies

1. **T-0030 (Pankaj Mohan), T-0034 (Hyoseok), T-0041 (Kaushal Kumar): `UNDOCUMENTED`** — the frozen records contain no dated activity; ranges cannot be derived without new research (which is out of scope). They will render as fuzzy "undated" markers in the timeline.
2. **L-0113 date discrepancy:** the link's evidence note says Kim Ŏk's Gitanjali translation is 1921, but TX-0013 date=1923 and P-0032 notes document March 1923 (Choi Dong-ho) vs April 1923 (Jeong Ji-yong Literary Museum). Derived date = **1923** (follows the text record); the discrepancy is recorded in the table and should be adjudicated in the next research phase.
3. **P-0054 Jung Seung-suk floruit (1980–1991) crosses the B6 boundary (1990–2026).** This is expected: floruit = documented activity window (degrees), band = India-exchange activity. Validation V2 uses overlap semantics, not containment.
4. **Source-mix coverage:** TRAVELS/TEXTS/INSTITUTIONS/RELS/PPL/PTX have no `source_ids` field in the frozen schema, so the source-mix table covers PEOPLE + EVENTS only. A full per-band source mix would require a schema extension (V3.1+), not a derivation.
5. **P-0062 Buddhavara floruit = 2026 only** (documented activity window). His long-term Bodh Gaya residence is documented but undated; the floruit does not claim a residence start year.

## 5. Places where the blueprint could not be executed safely from frozen data

| Blueprint §7 item | Status | Reason |
|---|---|---|
| 1. Region centroids | DONE (9) | All derivable from standard geographic knowledge; labeled APPROX |
| 2. Floruits (24) | DONE (20) | True count among carried people is 20, not 24 |
| 3. Travel ranges (14) | DONE (10 + 4 UNDOCUMENTED) | 3 travels have no dated activity anywhere in the frozen data |
| 4. Tradition taxonomy | DONE (43) | Multi-affiliation applied where justified |
| 5. Institution mapping | DONE (43) | 20 UNMAPPED (institutions not in institutions.csv — kept as free-text nodes for the network layer) |
| 6. Translation dates | DONE (6) | All from text records; L-0113 discrepancy flagged |
| 7. Event end dates | **NO-OP** | All 19 events already carry end dates in the frozen data |
| 8. Density + source mix | DONE | Source mix limited to PEOPLE/EVENTS (schema limitation) |

## 6. Validation summary (validate_derived_tables.py)

V1 existence/row counts · V2 floruit↔band overlap · V3 travel↔floruit containment · V4 taxonomy coverage + controlled categories · V5 mapping coverage + ID existence · V6 translation dates vs texts.csv · V7 event end dates · V8 frozen SHA-256 unchanged (13 files) · V9 no invented dates (UNDOCUMENTED rows carry no dates) · V10 centroid geometry/precision · V11 density uses explicit dates only.

**Result: 0 errors, 0 warnings.**

## 7. Usage notes for downstream layers

- Timeline: use `person_floruits` + `travel_date_ranges` for fuzzy spans; `translation_dates` for transmission markers; `density_by_decade` + `undated_counts` for the density ribbon; `tradition_taxonomy` for the tradition filter.
- GIS: use `region_centroids` for the 9 non-point places (hatched regions, never precise points).
- Network: use `institution_mapping` (MAPPED/PARTIAL rows) for INSTITUTIONAL edges; UNMAPPED values remain free-text nodes.
- Prosopography: use `tradition_taxonomy` + `institution_mapping` + `person_floruits` as the normalized dimensions.