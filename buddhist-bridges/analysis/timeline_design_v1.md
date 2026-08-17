# Timeline Design v1 — Interactive India–Korea Buddhist Timeline

**Phase:** 2 — Analysis Design · **Date:** 2026-08-17 · **Baseline:** frozen V3.0
**Answers:** Q0.1–Q0.4, Q1.1, Q2.1 (see `analysis_blueprint_v1.md` §3)

---

## 1. Design principles

1. **The timeline is an analytical instrument, not a decorative chronology.** Every element encodes a variable from the classification; every visual choice answers a question.
2. **No implied continuity.** Records at different dates do not imply exchange in between. Empty space is data. There are no connecting lines between same-type markers across gaps.
3. **Evidence status is always visible.** Confidence, status, scope, and single-source-ness are encoded in the marks themselves, not only in tooltips.
4. **Gaps are findings.** B3 (Joseon, 0 carried records) and the 1370→1981 event gap are rendered as annotated empty space.
5. **Intensity is never shown without source density.** The source-density ribbon is a mandatory companion layer.

## 2. Axis and structure — verdicts on the investigated options

| Option | Verdict | Rationale |
|---|---|---|
| **Continuous chronological axis** | **YES — primary axis.** Linear years CE, ~300 CE → 2027. | Time is continuous; a continuous axis is the honest representation and makes gaps visible. |
| **Bands by historical period** | **YES — as background shading overlay, NOT as separate panels.** | Separate panels would imply discontinuity between bands and hide the B3 gap. Shading keeps the axis continuous while supporting band filtering. |
| **Lanes by entity type** | **YES — 6 data lanes + 2 auxiliary lanes** (see §3). | Lanes separate incommensurable entities (a lifespan is not a point event). |
| **Geographic movement overlays** | **ADVANCED ONLY** — a mini-map synced to the time cursor. | In the MVP it would double the complexity; the GIS layer covers static geography. |
| **Event density** | **YES — as a density strip** (carried records per decade), always paired with the source-density ribbon. | Density answers Q1.1; unpaired it would mislead (B6 would look "more important"). |
| **Person lifespans** | **YES — lifeline spans.** | 19/43 carried people have full lifespans; the rest get floruit spans (precision APPROX, fuzzy rendering). |
| **Text transmission dates** | **YES — composition marker + translation markers** (from PTX TRANSLATOR links, e.g., Fuchs 1938, Ch'oe Nam-sŏn 1943). | Answers Q0.3; transmission chains are the advanced version's centerpiece. |
| **Historical gap indicators** | **YES — mandatory.** Band shading + explicit annotations + the density ribbon's zero-bins. | Directly implements the bias strategy for B3 and the 1370–1981 event gap. |

**Rejected (critical review):** 3D timelines; animated auto-play (implies continuity); proportional symbols sized by "importance" (no defensible importance measure); auto-clustering of events (hides gaps); smooth route interpolation (no evidence); "heat pulse" effects.

## 3. Lanes

| Lane | Content | Mark type |
|---|---|---|
| 1. PEOPLE | Lifelines (birth→death or floruit span) + activity markers (dated events in the person's life) | horizontal spans + ticks |
| 2. TRAVELS | Journey markers at start year; arrow glyph encodes direction (Korea→India / India→Korea / via third country); undated travels = fuzzy span anchored to floruit with `?` | point markers / fuzzy spans |
| 3. TEXTS | Composition marker + translation markers (PTX links) | point markers, chained in advanced version |
| 4. INSTITUTIONS | Founding marker + activity span (band-based, APPROX) | point + span |
| 5. EVENTS | Point markers (19 events, 1370–2027) | point markers |
| 6. RELS/ENCOUNTERS | Person-to-person encounters (MET_IN_PERSON, TEACHER_STUDENT) at their date | paired markers with connector (only within a dated encounter — never across gaps) |
| 7. CONTEXT (auxiliary) | CONTEXT/EXCLUDE records (e.g., the 11 B3 rows: Yi Su-gwang, Yi Kyu-gyŏng, Ch'oe Han-gi + texts) — dimmed, toggleable | dimmed markers |
| 8. NEGATIVES (auxiliary) | Documented negatives at their date/place (e.g., Kelaniya–Bongeunsa 1981, Nav Nalanda pre-1971, Kim Chi-ha–Gandhi) | X markers |

## 4. Evidence-status encoding (applies to every mark)

| Evidence state | Encoding |
|---|---|
| HIGH / VERIFIED | solid fill, full opacity |
| MEDIUM / PARTIAL | dashed outline |
| LOW / SPECULATIVE | dotted, reduced opacity |
| LEGENDARY (P-0007/0008, Tagore composite) | distinct glyph (◈) + "legend" label, never in the same visual weight as documented marks |
| Single-source HIGH (5 people, 8 events) | hatched overlay + badge; tooltip names the single source |
| Undated / APPROX | fuzzy span (soft-edged rectangle) with `?` |
| Documented negative | X marker in lane 8 |
| EXCLUDE/CONTEXT | dimmed (40% opacity), toggleable |

## 5. Filters (all combinable)

- **Band** B1–B6 (multi-select; B3 selectable and shows the annotation + context lane)
- **Entity type** people / travels / texts / institutions / events / rels
- **Direction** INDIA_TO_KOREA / KOREA_TO_INDIA / BIDIRECTIONAL / UNCERTAIN (from `direction_of_influence`)
- **Tradition/school** normalized taxonomy (Seon/Chan, Esoteric, Yogacara, Vinaya, Hwaeom, Lay/Modern, Non-Buddhist, Unknown)
- **Connection type** PHYSICAL_MOVEMENT / TEXTUAL_TRANSMISSION / INSTITUTIONAL / INDIRECT_INFLUENCE / PERSON_ENCOUNTER / LEGENDARY
- **Confidence/status** HIGH/MEDIUM/LOW/SPECULATIVE × VERIFIED/PARTIAL/UNRESOLVED/LEGENDARY
- **Scope** carried (default) / +context / +excluded
- **Corroboration** "≥2 sources" toggle (isolates the defensible core)

## 6. Interaction

- Hover: tooltip with label, dates, evidence summary, source keys, classification rationale.
- Click: record card (all fields + links to related records).
- Search: name/ID lookup.
- Filter chips with active-state counts.
- Zoom: decade ↔ century ↔ full-range.
- Export: SVG/PNG (current view), CSV (filtered records).

## 7. Minimum Viable Version (MVP)

**Form:** single self-contained HTML page (no build step), data embedded from the frozen CSVs + derived tables.

**Contents:**
1. Continuous axis 300 CE → 2027 with B1–B6 band shading and labels.
2. Lanes 1–6 (PEOPLE lifelines, TRAVELS, TEXTS, INSTITUTIONS, EVENTS, RELS) + lane 8 (NEGATIVES).
3. Full evidence-status encoding (§4) — including single-source hatching and fuzzy spans.
4. Gap annotations: "B3 Joseon — no carried records (see context lane)" and "1370–1981: no documented events".
5. Source-density ribbon (carried records per decade) + event-density strip.
6. Filters: band, entity type, direction, confidence, scope, corroboration toggle.
7. Tooltips with evidence + source keys; click-through record cards.
8. Legend explaining every encoding.

**Scale check:** ~250 marks max (43 lifelines + 26 travels + 13 texts + 19 institutions + 19 events + 10 rels + negatives) — comfortably within a single-page renderer.

**Acceptance criteria:** (a) a user can tell at a glance which marks are documented vs legendary vs negative; (b) the B3 gap and the 1370–1981 gap are visible without clicking anything; (c) no mark implies continuity across a gap; (d) every mark's tooltip cites its sources.

## 8. Advanced version (adds to MVP)

1. **Geographic mini-map** synced to the time cursor: route polylines for the 8 routed travels (T-0001 Hyecho, T-0003, T-0005–0007, T-0010, T-0013 Jikong, T-0042 Hwang Su-yŏng) + event locations.
2. **Text-transmission chains**: original → translations → editions (e.g., WOJ: 723 composition → Fuchs 1938 → Ch'oe Nam-sŏn 1943 → 지안/정수일 editions; Tagore: 1929 note → Chu Yo-han 4-line rendering).
3. **Temporal network mini-view**: network snapshot at the cursor position (nodes active at that time), answering "who was connected when".
4. **Density histogram toggle** (records per decade, by entity type).
5. **Saved filter states** (URL-encoded), keyboard navigation, compare mode (two filtered views side by side).
6. **Export CSV** of the filtered view for downstream analysis.

**Explicitly NOT in the advanced version:** auto-play animation, 3D, "flow" effects, inferred routes, importance-scaled symbols.

## 9. How the five data limitations appear (no misleading)

| Limitation | Rendering |
|---|---|
| B3 zero carried | Band shading + annotation + dimmed context lane with the 11 excluded rows; the gap reads as a historical finding, and the excluded records are visible as evidence of the decision. |
| B1 small primary core | Solid rendering only for HIGH/MEDIUM; SPECULATIVE dotted; per-band source counts in the legend; density ribbon shows B1's sparse source base. |
| B6 source-rich | Density ribbon + "news-era" annotation; single-source hatching on the 8 events; corroboration toggle. |
| Single-source HIGH | Hatched + badged; tooltip names the source; excluded from the "≥2 sources" view. |
| Uneven density | The ribbon is a companion layer, not decoration; intensity readings require checking it. |

## 10. Data prep required (from blueprint §7, items 2, 3, 4, 6, 7, 8)

Floruit ranges for 24 people · dates for 14 travels (APPROX) · tradition taxonomy · translation dates for 6 PTX links · event end dates · density tables. All derived, none modify the frozen data.