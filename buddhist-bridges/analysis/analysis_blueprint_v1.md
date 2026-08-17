# Analysis Blueprint v1 — Buddhist Bridges Phase 2 (ANALYSIS DESIGN)

**Project:** Buddhist Bridges: Mapping India–Korea Networks of People, Places, Texts, and Ideas
**Phase:** 2 — Analysis Design (design only; no analyses run, no data modified)
**Date:** 2026-08-17 · **Baseline:** frozen V3.0 (`buddhist-bridges/v3.0_frozen/`) + finalized documentation
**Companion docs:** `timeline_design_v1.md` · `gis_design_v1.md` · `network_design_v1.md` · `prosopography_design_v1.md`

---

## 1. Guiding principle

**DATA → HISTORICAL QUESTION → ANALYSIS → VISUALIZATION**, never DATA → PRETTY VISUALIZATION.

Every visualization must answer a named question from §3, must encode evidence status explicitly, and must not imply more than the data supports. A feature is included only if it serves a question; "technically possible" is not a reason.

## 2. Baseline inventory (frozen V3.0, read-only)

| Table | Rows | Carried (KEEP+ADAPT) |
|---|---|---|
| people | 76 | 43 |
| places | 39 | 32 |
| travels | 41 | 26 |
| texts | 30 | 13 |
| institutions | 31 | 19 |
| person_person (RELS) | 22 | 10 |
| person_place (PPL) | 35 | 18 |
| person_text (PTX) | 32 | 14 |
| events | 19 | 19 |
| person_event | 13 | 13 |
| event_participants | 10 | 10 |
| sources | 187 | — |
| classification | 325 | 207 (KEEP=171, ADAPT=36; CONTEXT=46, EXCLUDE=85, REVIEW=0) |

**Carried rows by band:** B1=68 · B2=21 · **B3=0** · B4=19 · B5=17 · B6=82.
**Carried people (43):** B1=18, B2=6, B4=6, B5=5, B6=8; movement: `-`=18, visited=12, studied=7, worked=4, planned=2; direction: INDIA_TO_KOREA=27, KOREA_TO_INDIA=11, BIDIRECTIONAL=4, UNCERTAIN=1; confidence: HIGH=19, MEDIUM=24; status: VERIFIED=39, PARTIAL=4.
**Carried connection types (single-type counts):** PHYSICAL_MOVEMENT=51, INSTITUTIONAL=40, TEXTUAL_TRANSMISSION=34, INDIRECT_INFLUENCE=11, PERSON_ENCOUNTER=8 (+ multi-type rows).
**Events (19):** PILGRIMAGE=7, EXHIBITION=3, CONFERENCE=3, MOU_AGREEMENT=2, RELIC_TRANSFER=2, TEMPLE_FOUNDATION=1, TEMPLE_DEDICATION=1; dates 1370 → 2027-01-14; VERIFIED=18, UNRESOLVED=1.
**Data quality facts that constrain every layer:** 30/39 places have coordinates; 41/41 travels have endpoints but only 8 have intermediate routes and 14 lack start years; 19/43 carried people have full lifespans; 5 people and 8 events rest on single HIGH sources; B3 has zero carried records; B6 is news-source-rich, B1 rests on a small primary core.

## 3. Research-question hierarchy

Three tiers. Tier 0 must be answered before Tier 1, Tier 1 before Tier 2. Every analysis output maps to at least one question.

### Tier 0 — Descriptive (what is documented?)
- **Q0.1 Inventory.** What is the complete documented inventory of India–Korea Buddhist connections (4th c. CE–2026) by type, period, and direction?
- **Q0.2 Movement.** Who travelled, when, by what route, and with what confidence? (41 travels; 8 routed; 14 undated)
- **Q0.3 Transmission.** Which texts carried Buddhist knowledge between India and Korea, when, and through whom? (30 texts; 14 carried PTX links)
- **Q0.4 Institutions.** Which institutions anchor the network, when were they active, and in what role? (31 institutions; 19 carried)

### Tier 1 — Comparative / structural (how does the network differ across time and role?)
- **Q1.1 Period structure.** How do density, node mix, connection types, and direction differ across B1/B2/B4/B5/B6?
- **Q1.2 Mediation.** What distinguishes the 19 MEDIATOR records from PRIMARY (158) and SECONDARY (17)? Who are the structural intermediaries?
- **Q1.3 The B3 question.** Is the Joseon gap genuine? What does the absence of carried records mean historically (closed Neo-Confucian state vs collection failure)? — answered from the 11 excluded B3 rows + documented negatives, not from silence.
- **Q1.4 Connection-type distribution.** How do PHYSICAL_MOVEMENT / TEXTUAL_TRANSMISSION / INSTITUTIONAL / INDIRECT_INFLUENCE / PERSON_ENCOUNTER distribute across bands, and what does the shift person-mediated → institution-mediated look like?
- **Q1.5 Direction.** What explains the INDIA_TO_KOREA (27) vs KOREA_TO_INDIA (11) asymmetry, and is it real or source-driven?

### Tier 2 — Interpretive (what does it mean?)
- **Q2.1 Continuity test.** Is there a continuous "Buddhist bridge," or discrete episodes? (Explicitly test: the data shows B1 cluster → B2 cluster → 500-year gap → B4/B5 revival → B6 institutionalization. The timeline must render this honestly.)
- **Q2.2 Mechanism shift.** What explains the shift from person-mediated exchange (monks, pilgrims) to institution-mediated exchange (orders, universities, MOUs, relic returns)?
- **Q2.3 Relics and pilgrimage.** What role do relic transfers (EV-0017/0018) and organized pilgrimage (7 events) play in sustaining the link across the modern period?
- **Q2.4 Source-bias correction.** What is the corrected picture once source density (B6 news-rich, B1 primary-poor) is controlled for?

## 4. Variable → method mapping

| Variable | Operationalization (frozen field) | Method | Layer |
|---|---|---|---|
| Period | `period_band` (classification) | Banded filtering, cohort counts, density strips | all |
| Connection type | `connection_type` (classification) | Edge typing; lane assignment; distribution tables | timeline, network |
| Direction | `direction_of_influence` (people) | Directed edges; arrow encoding; direction counts | timeline, network |
| Movement | `movement_status` (classification) | GIS polylines; lifeline markers; movement typology | GIS, timeline, prosopography |
| Confidence | `confidence` (records) | Line style (solid/dashed/dotted); badge; tooltip | all |
| Status | `status` (people/events) | Glyph + label (VERIFIED/PARTIAL/UNRESOLVED/LEGENDARY) | all |
| Evidence strength | `source_ids` count (derived) | Single-source badge/hatching; corroboration subsets | all |
| Source density | records-per-decade (derived from dates) | Source-density ribbon; per-band source counts | timeline, network |
| Exchange type | `exchange_types` (classification) | Edge color; prosopography clustering | network, prosopography |
| Tradition/school | `religious_affiliation` (people, free text) | Normalized taxonomy (see §7) → color coding | timeline, prosopography |
| Institution | `institution_org` (people, free text) | Mapped to I-#### → institution nodes | network, prosopography |
| Lifespan | `birth_year`/`death_year` | Lifeline spans; life-course sequences | timeline, prosopography |
| Text transmission | `texts.date` + PTX link dates | Composition + translation markers; transmission chains | timeline |
| Route | `origin/destination/intermediate_place_ids` | Polylines only where intermediates exist; schematic otherwise | GIS |
| Event date | `events.start_date` | Point markers; density strip | timeline, GIS |
| Scope | `scope` (classification) | Analysis set (KEEP/ADAPT) vs context lane (CONTEXT/EXCLUDE) | timeline |
| Documented negatives | docs (unresolved_cases.md, collect_next.md) | X-markers in dedicated lane/layer | timeline, GIS |

## 5. Recommended visualizations (consolidated)

| # | Visualization | Answers | Layer | Priority |
|---|---|---|---|---|
| V1 | Interactive timeline (MVP): continuous axis, band shading, entity lanes, evidence styling, gap annotations, source-density ribbon | Q0.1–Q0.4, Q1.1, Q2.1 | timeline | 1 |
| V2 | Prosopographical register: 43 person cards + role×period matrix + typology table | Q0.1, Q1.2 | prosopography | 2 |
| V3 | Static per-band network graphs (B1/B2/B4/B5/B6) with typed, directed edges | Q1.1, Q1.2, Q1.4, Q1.5 | network | 3 |
| V4 | Static per-band GIS maps: places, routed journeys, schematic corridors, event markers, negatives | Q0.2, Q1.1 | GIS | 4 |
| V5 | Timeline advanced: geographic mini-map synced to cursor, text-transmission chains, temporal network snapshot | Q0.3, Q2.1, Q2.2 | timeline | 5 |
| V6 | Density + source-mix charts: records per decade vs source types per band | Q1.1, Q2.4 | all | 6 |
| V7 | Direction and connection-type distribution charts (stacked bars per band) | Q1.4, Q1.5 | all | 7 |
| V8 | Mediator analysis: MEDIATOR vs PRIMARY/SECONDARY comparison table + network role stats | Q1.2 | network, prosopography | 8 |

## 6. Bias and uncertainty strategy

The five known limitations are **features of the visualization, not footnotes**. Each must appear in every layer where it could mislead:

| Limitation | How it appears (never hidden) |
|---|---|
| **B3 = 0 carried records** | Timeline: band shading + explicit annotation "no carried records (Joseon)" + a dimmed CONTEXT lane showing the 11 excluded B3 rows (Yi Su-gwang, Yi Kyu-gyŏng, Ch'oe Han-gi + texts/links) so the gap is visible as a *decision*, not an artifact. Network: B3 snapshot rendered as an empty state with the same annotation. GIS: no B3 layer; the map legend states why. Prosopography: B3 cohort row = "0 (see gap note)". |
| **B1 smaller primary core** | Only HIGH/MEDIUM records render solid; SPECULATIVE/legendary get distinct styling. Every B1 chart carries its source count (13 PRIMARY + 15 ARCHIVAL sources serve the whole ancient layer). Never compare B1 vs B6 intensity without the density ribbon visible. |
| **B6 source-rich** | Source-density ribbon is mandatory on the timeline; B6 charts carry "news-era" annotation; single-source badges on the 8 events and 5 people; B6 intensity treated as source-driven until corroborated. |
| **5 people + 8 events single-source HIGH** | Hatched/badged in every layer; tooltip names the single source; a "corroborated (≥2 sources)" filter isolates the defensible core. |
| **Uneven historical source density** | The density ribbon (carried records per decade) is a *companion layer*, not decoration: any intensity reading must be checked against it. Charts show per-band source-type mix (NEWS vs PRIMARY vs ARCHIVAL). |

**Global rules:** (1) no connecting lines between same-type markers across gaps — empty space is data; (2) "no evidence found" is rendered as a documented-negative marker or as absence with annotation, never as a positive; (3) legendary content (Suro/Heo Hwang-ok, Tagore composite poem) is visually distinct and labeled; (4) uncertain dates render as fuzzy spans with `?`, never as points; (5) every tooltip lists evidence summary + source keys.

## 7. Exact additional data requirements

**None require new collection.** All are curation/derivation tasks over the frozen data, written as derived tables in `analysis/` (the frozen CSVs are never modified):

1. **Region geometries/centroids** for the 9 non-point places (PL-0001 Silla, PL-0002 Baekje, PL-0004 Goguryeo, PL-0005 Goryeo, PL-0006 Joseon, PL-0008 Gandhara, PL-0012 Central India/Sangana, PL-0019 Serindia, PL-0031 India unspecified) — standard gazetteer values, marked `REGION_CENTROID` (uncertainty class).
2. **Floruit/activity ranges** for the 24 carried people without birth years — derived from period band + dated activities in notes; precision `APPROX`.
3. **Dates for the 14 undated travels** (T-0005..T-0009, T-0012, T-0029..T-0035, T-0039, T-0041) — derived from person floruit; precision `APPROX`, rendered as fuzzy spans.
4. **Normalized tradition taxonomy** — map ~30 free-text `religious_affiliation` values to ~8 categories: `Seon/Chan`, `Esoteric (Milgyo)`, `Yogacara`, `Vinaya`, `Hwaeom`, `Lay/Modern Buddhist`, `Non-Buddhist`, `Unknown`. (Mapping table, auditable.)
5. **institution_org → I-#### mapping** — map free-text `institution_org` values to institution IDs for network edges (e.g., "Dongguk University (professor)" → I-0010). Unmappable values stay as text nodes.
6. **Translation dates** for the 6 PTX TRANSLATOR links — extract from the evidence notes added in the freeze round.
7. **Event end dates** where month-precision only (EV-0001, EV-0006, EV-0009, EV-0015, EV-0018).
8. **Derived density tables** — carried records per decade; source-type mix per band (computed from existing dates and source_ids; no new data).

## 8. Recommended order of implementation

1. **Data-prep layer** (§7 items 1–8) — derived tables in `analysis/`, each with a provenance note. No frozen-file changes.
2. **Prosopography** (V2) — pure tabular analysis of 43 people; produces the register that timeline and network consume; cheapest and highest leverage.
3. **Timeline MVP** (V1) — the flagship output; consumes classification + prosopography.
4. **Network static per-band** (V3) — consumes institution mapping.
5. **GIS static per-band** (V4) — consumes region centroids; most prep, most uncertainty, so last of the static layers.
6. **Timeline advanced** (V5) — density ribbon, transmission chains, temporal network mini-view, geo mini-map.
7. **Synthesis** — Tier 1/2 answers (V6–V8 + written findings), each with the bias strategy applied.

## 9. Non-goals (explicit)

- No modification of the frozen V3.0 data (all derived tables live in `analysis/`).
- No website development.
- No large-scale new data collection (only §7 curation).
- No inferential statistics (n=43 people; descriptive only).
- No community detection as evidence (network too small; exploratory only).
- No animated auto-play or "flow" effects that imply continuous exchange.
- No "importance" claims from centrality without source-density control.