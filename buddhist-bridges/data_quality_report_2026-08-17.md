# Data Quality & Coverage Report — 2026-08-17 (P5 round)

**Project:** India–Korea Buddhist Mediators (Buddhist Bridges V3)
**Builds:** `build_dataset.py` 0 errors / 0 warnings · `build_classification.py` 0 errors / 0 warnings

## 1. Dataset inventory (post-build)

| Table | Count | | Table | Count |
|---|---|---|---|---|
| PEOPLE | 76 (P-0001..P-0077) | | EVENTS | 19 (EV-0001..EV-0019) |
| PLACES | 39 | | PERSON_EVENT | 13 |
| TRAVELS | 41 | | EVENT_PARTICIPANTS | 10 |
| TEXTS | 30 | | SOURCES | 187 |
| INSTITUTIONS | 31 | | PERSON_PERSON (RELS) | 22 |
| PERSON_PLACE | 35 | | PERSON_TEXT | 32 |

**People attribute distribution:** period — ANCIENT=20, CONTEMPORARY=34, EARLY_MODERN=3, MEDIEVAL=6, MODERN=13 · relationship_type — DIRECT=45, INDIRECT=16, MEDIATED=10, UNCERTAIN=5 · direction — INDIA_TO_KOREA=44, KOREA_TO_INDIA=17, BIDIRECTIONAL=9, UNCERTAIN=6 · confidence — HIGH=38, MEDIUM=33, LOW=3, SPECULATIVE=2 · status — VERIFIED=64, PARTIAL=8, UNRESOLVED=2, LEGENDARY=2 · physically_traveled — YES=38, NO=30, UNCERTAIN=8.

**Classification (V3):** relevance — PRIMARY=171, SECONDARY=17, MEDIATOR=19, CONTEXTUAL=46, NONE=85 · scope — KEEP=171, ADAPT=36, CONTEXT=46, EXCLUDE=85, **REVIEW=0** · carry rows (KEEP+ADAPT) = 207, PEOPLE carried = 43 · movement — visited=45, worked=33, studied=29, legendary=3, planned=3.

## 2. This round (P5) — what changed

1. **REVIEW closure — both records closed (REVIEW: 2 → 0).**
   - **P-0068 Sŏ Chŏng-ju → SECONDARY/ADAPT/B5/(ENCOUNTER)**: India link now documented — Indian Gujarati poet Sitanshu Yashaschandra visited Dongguk University and met Sŏ (동대신문, reposted 2010-08-11; visit year unstated, ~1970s). Literary exchange (compassion theme, mutual translation proposal, '자비회' society). No evidence Sŏ himself visited India.
   - **P-0070 Kim Chi-ha → NONE/EXCLUDE/B5/(INDIRECT)**: documented negative via Hani 2026-07-03 (임진택 interview): thought is Donghak-rooted (시천주/향아설위, 증산도 개벽사상, Buddhism, Christianity); no Gandhi/India influence. Status field kept UNRESOLVED because the popular Gandhi/ahimsa association is unverified rather than refuted.
2. **New records:** P-0076 Sitanshu Yashaschandra (SECONDARY/ADAPT/B5/(ENCOUNTER)); P-0077 Ch'ukwŏn Chijŏn (축원 지천, 竺源 智泉, 1324–1395, 정지국사 — SECONDARY/ADAPT/B2/(INDIRECT)); R-0021 (Sŏ–Yashaschandra MET_IN_PERSON); R-0022 (Jikong–Ch'ukwŏn TEACHER_STUDENT). Jikong circle now complete: Naong / Muhak / Baegun / Ch'ukwŏn.
3. **Sources:** 185 → 187 (`donggukmedia_seo_yashaschandra`, `hani_kimchiha_2026`).
4. **Fuchs year resolved:** German translation of *Wang ocheonchukguk jeon* = **1938** (W. Fuchs, *Huei-ch'ao's Pilgerreise durch Nordwest-Indien und Zentral-Asien um 726*, Sitzungsberichte der Preußischen Akademie der Wissenschaften, Phil.-hist. Klasse XXX, 1938; pub. 1939 per KCI 이재원 2016). encykorea E0039126's "1928" is an error, contradicted by the primary bibliographic record and the peer-reviewed KCI article. TX-0001 notes updated.

## 3. Documented negatives (preserved, not speculative)

- **Kelaniya–Bongeunsa sisterhood** (agreed Dec 1981 per Dong-A 1982): no evidence of realisation in English/Korean searches; only find = BBSI 2018-06-24 Korean-Sri Lankan cultural exchange (residents' event, not the twinning).
- **Nav Nalanda Mahavihara pre-Pŏpchŏng Koreans**: no Korean students documented in Nalanda literature; corroborated by Hwang Su-yŏng's 1963 note of absent Korean students.
- **"16 Goryeo monks in Yuan-era India/Tibet"**: unverified (P4).
- **Piparhawa exhibition ↔ Korea**: no Korean participation documented (P1).
- **GBS 2023 / 2nd GBS 2026 / ICYBS 2025 Korean participation**: unconfirmed (P1).

## 4. Coverage by band (V3 rows)

| Band | Rows | Notes |
|---|---|---|
| B1 (<900) | 79 | Ancient core: Hyecho, Gyeomik, Marananta, Heo Hwang-ok; WOJ display event (EV-0019) |
| B2 (900–1392) | 21 | Jikong circle complete (4 disciples), Hoeamsa relic legacy (EV-0017/18) |
| B3 (1392–1900) | 11 | Thinnest band — Joseon-era India contact remains a structural gap |
| B4 (1900–1945) | 53 | Colonial-era: Kim Iryŏp/Paek Yong-sŏng candidates still open (not records) |
| B5 (1945–1990) | 54 | Post-war: Pŏpchŏng, Hwang Su-yŏng, 1982 delegation, Sŏ Chŏng-ju encounter |
| B6 (1990–2026) | 120 | Contemporary: pilgrimages, institutions, relic returns, exhibitions |

## 5. Remaining open items (see collect_next.md §4–§5)

- **Candidates (not records):** Paek Yong-sŏng, Kim Iryŏp, Pang Han-am — one targeted research round each.
- **B5 gaps:** 1950s–60s Korean monks in India before Pŏpchŏng; 1960s–70s organised pilgrimages; post-1973 embassy-sponsored Buddhist events beyond EV-0014.
- **P-0069 Hwang Tong-gyu:** UNRESOLVED (no India link found in searched sources).
- **Pending source append:** buddhistdoor.net 2022-05-19 "New Korean Buddhist Temple to Open in Bodh Gaya" (Bunhwangsa India dedication) — not yet added to the registry.

## 6. Quality observations

- All validation vocabularies pass; 0 errors / 0 warnings across both builders for three consecutive rounds.
- Evidence discipline held: every new record this round is source-backed (institutional news or peer-reviewed scholarship); every negative is documented with its search scope.
- Confidence mix is healthy (HIGH=38, MEDIUM=33); only 2 SPECULATIVE and 2 LEGENDARY rows, both flagged as such.
- The only known factual discrepancy in the dataset (Fuchs year) is now resolved and annotated in TX-0001.