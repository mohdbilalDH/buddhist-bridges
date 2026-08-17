# Provenance & Evidence Audit — Buddhist Bridges V3.0 (FINAL)

**Date:** 2026-08-17 · **Status:** AUDIT PASSED — 0 errors / 0 warnings
**Tool:** `buddhist-bridges/audit_v3.py` (re-runnable; exits 1 on any error)

## 1. Method

The audit runs eight dimensions over the built CSVs and the classification table:

| Dim | Check | Result |
|---|---|---|
| A | Identity/duplicates: normalized hangul/hanja/name/title maps across PEOPLE, PLACES, TEXTS, INSTITUTIONS, EVENTS | PASS |
| B | Classification consistency: missing classifications, period↔band, movement↔travel, movement↔T records, conns↔relevance, relevance→scope mapping, REVIEW must be 0 | PASS |
| C | Source traceability: unknown source keys, missing URLs, HIGH-confidence records without sources | PASS |
| D | Relationship logic: kind→conns, relationship_type vs kind, EXCLUDE endpoints | PASS |
| E | Travel vs encounter: India↔Korea crossings vs movement, pilgrimage purpose, encounter-only vs travel=YES | PASS |
| F | Events: both India & Korea sides in description, band vs dates, event_type vocabulary, PERSON_EVENT linkage | PASS |
| G | Places/institutions/texts vs bands, place-type heuristics | PASS |
| H | Coverage profile (see `coverage_analysis_v3.0.md`) | PASS |

## 2. Normalization changelog (V3.0 freeze round — no new records)

| Record | Change | Reason |
|---|---|---|
| P-0008 Suro | movement `legendary` → `-` | Legend has no physical movement; LEGENDARY conns retained |
| P-0061 Vyjayanti Raghavan | movement `-` → `studied` | Has L-0029 SNU MA studied link + context band |
| PL-0010/0032–0037 (7 sacred sites) | MONASTERY → SITE | Place-type heuristic: pilgrimage sites are not monasteries |
| 6 PTX links (L-0113/114/115/122/123/125) | evidence notes added | Script artifact had left them empty; all TRANSLATOR links now carry evidence |
| P-0037 Ham Sok-hon | period MODERN → CONTEMPORARY | Active post-1945, band B5 |
| P-0073 Hwang Su-yŏng | period MODERN → CONTEMPORARY | Active post-1945, band B5 |

## 3. Evidence-depth spot check (2026-08-17)

- **Carried records with "no travel" phrasing** (P-0074 Muhak, P-0075 Baegun, P-0077 Ch'ukwŏn): correct — indirect connection via Jikong (Dhyānabhadra); no unsupported travel claims. PASS.
- **SPECULATIVE confidence without LEGENDARY status**: none. PASS.
- **Carried people with zero sources**: none. PASS.
- **Single-source HIGH-confidence records** (documented, accepted — single authoritative institutional source each):
  - People: P-0055 U Myeong-ju (ggbn_umyeongju), P-0056 Lee Jeong-ho (kyobo_leejeongho), P-0058 Neerja Samajdar (jnu_neerja), P-0059 Kaushal Kumar (jnu_kaushal), P-0063 Hyoseok (hyunbul_hyoseok)
  - Events (8): EV-0004, EV-0006, EV-0007, EV-0008, EV-0012, EV-0013, EV-0014, EV-0016 — each seeded from one institutional/news source. **Priority for corroboration in the next research phase.**
- **Documented negatives preserved** (never rewritten as "did not happen"): Kelaniya–Bongeunsa twinning (unrealised), Nav Nalanda pre-Pŏpchŏng Koreans (none documented), Kim Chi-ha–Gandhi (unverified), "16 Goryeo monks in Yuan-era India/Tibet" (unverified), Goryeo Hyeil India journey (not verified), Girija Kanta Mookerjee (excluded), Piparhawa 2026 Korean participation (none documented), GBS 2023/2026 + ICYBS 2025 Korean participation (unconfirmed).

## 4. By-design notes (recorded, not errors)

- 10 events have no PERSON_EVENT rows (organizer-only events) — by design.
- 10 event-level participants (EP-0001..0010) are not PEOPLE records — by design.
- TX-0030 kept as EXCLUDE (duplicate of TX-0016, per classification_audit.md) — preserved to keep the chain of evidence.
- Institution founded-year vs band mismatches (G3): band = India-exchange activity, not founding year — by design.
- 52 R/PPL/PTX rows show band `?` (band `-`): relationship/link rows carry no period band — by design.

## 5. Source registry (187 keys)

| source_type | count |
|---|---|
| NEWS | 51 |
| TERTIARY | 43 |
| SECONDARY | 32 |
| WEBSITE | 27 |
| ARCHIVAL | 15 |
| PRIMARY | 13 |
| DATABASE | 6 |

Every `source_ids` value in the dataset resolves to a key in sources.csv (dimension C).