# Buddhist Bridges — V3 Dataset Proposal

**Date:** 2026-08-17 · **Author:** OpenWork (per project brief) · **Status:** for user review/approval
**Companion docs:** `schema_v3.md` (schema) · `classification_audit.md` (what the V2 data becomes) · `gap_analysis.md` (where to expand) · `classification_v3.csv` (machine-readable classification)

---

## 1. What this proposal does

1. Establishes the **V3 Buddhist-only schema** (new EVENTS entity, 13 new fields, connection-type ladder, 6 period bands) — see `schema_v3.md`.
2. Classifies **all 275 V2 records** — see `classification_v3.csv` (34 people in scope; 138 in-scope rows).
3. Reports the **2024–2026 research findings** and proposes the first batch of new V3 records.
4. Queues **12 new source keys** for `data_sources.py`.
5. Sets the **roadmap** to GIS / network / timeline / interactive DH website (no visualization work yet).

## 2. Contemporary research findings (2024–2026)

### 2.1 Confirmed events (sources verified 2026-08-17)

| # | Event | Date(s) | Actors | Sources |
|---|-------|---------|--------|---------|
| E1 | **Sangwol/Jogye walking pilgrimage** — 108 Buddhists from ROK, 1,100+ km on foot, Sarnath → Shravasti via Bodh Gaya, Vulture Peak, Rajgir, Nalanda, Vaishali, Kushinagar, Lumbini, Kapilavastu (per route reports: **1,167 km / 43 days**) | began Feb 2023 | Jogye Order; Sangwol Society (상월결사); ~200-strong delegation | PIB PRID=1896682 (2023-02-06); Korea Bizwire (2023-02-10); India Narrative (2023-03-22); The Federal |
| E2 | **Bexpo 2026** (Seoul International Buddhism Expo) — IBC DG Abhijit Halder presented a Buddha statue to Jung Won-ju, president of the Lay Buddhist Association of the Jogye Order (chair, Daewoo E&C); cultural/spiritual cooperation agreed | 2026-04-04 | IBC; Lay Buddhist Association of the Jogye Order | Korea Herald (2026-04-09, Sanjay Kumar); Our Buddhism World (2026-04-10) |
| E3 | **2nd Global Buddhist Summit 2026** — Bharat Mandapam, New Delhi; IBC + Ministry of Culture; theme "Collective Wisdom, United Voice and Mutual Coexistence"; ~200 delegates. **Korean participation not yet confirmed** | 2026-01-24/25 | IBC; Government of India | Buddhist Door Tea House (2026-01-18); IBC official PDF |
| E4 | **Jungto (정토회) India pilgrimage program** — annual; 35th pilgrimage in early 2026 (implied); 36th: 14–30 Jan 2027 (16박17일, 500 participants, registration from 2026-05-25) | annual, Jan | Jungto Society; Pomnyun Sunim (founder) | jungto.org/india |
| E5 | **Delhi University ↔ Bodh Gaya International College of Buddhist Studies MOU** (academic exchange) | 2026-04-23 | DU; BGICBS (Chancellor: Ven. Buddhavara) | BTN (already `btn_buddhavara` key) |
| E6 | **Jogye delegation pilgrimage** — Sarnath → Bodh Gaya (Mahabodhi) | May 2022 | Jogye Order | Beopbo (2022-05-20) |
| E7 | **Jogye pilgrimage to the 8 great sites + Nepal** — 13박14일, incl. visit to **Yeoraesunwon** (여래선원, Korean-run temple at Bodh Gaya) | 2014-02-19 → 03-04 | Jogye Order | jogyesa.kr |

### 2.2 Unconfirmed (record only when sourced)

- **A distinct "2026 Jogye Order pilgrimage"** as an individual event (user brief asserts 2023 and 2026; 2023 is fully confirmed, the 2026-specific record is not yet pinned — the Jungto 35th (early 2026) may be what is meant). **One more targeted search round needed** (불교신문/법보신문/조계종 archives, Korean-language).
- **Korean delegation at the 2nd GBS 2026** (E3) — no Korean participation found in the sources reviewed.
- **Piparhawa Buddha relics exhibition ↔ Korea** — PM Modi inaugurated the Grand International Exhibition of the Holy Piparhawa Remains (Rai Pithora Cultural Complex, Delhi, 2026-01-03); no Korea link found in the report.

## 3. Proposed new records (V3 phase 1)

### 3.1 EVENTS (new table, `EV-####`) — the 7 confirmed events above (E1–E7)
Each carries: event_type, dates, location (PL-####), organizer institution IDs, participant person IDs, evidence, confidence. E3 is recorded with `status=UNRESOLVED` for Korean participation until confirmed.

### 3.2 INSTITUTIONS (new, `I-####`)
- **IBC (International Buddhist Confederation)** — organizer of GBS 2026, Bexpo 2026 engagement.
- **Jogye Order (대한불교조계종)** — host of the 2023 pilgrimage; central modern actor (suggest a Jogye root record; sub-orgs reference it).
- **Sangwol Society (상월결사)** — organizer of the 2023 walking pilgrimage.
- **Jungto Society (정토회)** — annual India pilgrimage program (E4).
- **Yeoraesunwon (여래선원), Bodh Gaya** — Korean-run temple; active by 2014 (E7), complements Bunhwangsa India (I-0015).
- *(Optional, at event level only: Lay Buddhist Association of the Jogye Order.)*

### 3.3 PLACES (new, `PL-####`)
Pilgrimage-route nodes for the 2023 route and standard pilgrimage set: **Sarnath**, **Kushinagar**, **Lumbini**, **Rajgir/Vulture Peak**, **Vaishali**, **Shravasti**, **Kapilavastu** (lat/lon to be filled at record time). Also **Bharat Mandapam, New Delhi** (E3 venue — may fold into PL-0027 as a venue note instead).

### 3.4 PEOPLE (candidates — REVIEW before adding)
- **Pomnyun Sunim (법륜)** — founder of Jungto; major India pilgrimage program; Buddhist social activist. REVIEW: sources needed for a PEOPLE record (or record only as founder of I-Jungto).
- **Jung Won-ju** — president, Lay Buddhist Association of the Jogye Order; Bexpo 2026 principal. Likely event-level participant only.
- **Abhijit Halder** — IBC Director General; Bexpo 2026 principal. Likely event-level participant only.
- **Paek Yong-sŏng, Kim Iryŏp, Pang Han-am** — B4 research pipeline (see `gap_analysis.md` §2 B4).

### 3.5 TEXTS (new, `TX-####`)
- PIB press release (E1) as a primary archival record; Korea Herald Bexpo report (E2); Buddhist Door/IBC GBS documents (E3); Jungto program page (E4) — primarily as SOURCES; a TEXT record only if the document itself is an object of transmission (e.g., the PIB record of the pilgrimage).

## 4. Schema changes (summary)

- New **EVENTS** entity (`EV-####`); fields per `schema_v3.md` §3.
- 13 new fields (user-specified) mapped to PEOPLE/JOURNEYS/RELS/EVENTS — `buddhist_tradition`, `school_lineage`, `monastery_temple`, `teacher`, `disciple`, `pilgrimage`, `text`, `translation`, `transmission_route`, `doctrinal_knowledge_exchange`, `institutional_exchange`, `contemporary_event`, `event_date`, `event_location` (`schema_v3.md` §5).
- Connection-type ladder + 6 period bands carried on every record (`schema_v3.md` §4, §2).
- No deletions: EXCLUDE records stay in V2; V3 is a subset+extension view with its own build outputs.

## 5. Roadmap

| Phase | Work | Gate |
|-------|------|------|
| **V3-1** (this proposal, pending approval) | EVENTS table + new fields in schema; 12 SOURCES keys; regenerate classification CSV | `build_classification.py` 0 errors; `build_dataset.py` 0 errors |
| **V3-2** | Add confirmed records: 7 EVENTS, 5–6 INSTITUTIONS, 7 PLACES, REVIEW people pipeline (1 targeted research round for the 2026 Jogye item + B4 candidates) | `build_dataset.py` 0 errors; every new record cited |
| **V3-3** | Analysis: GIS (Folium/Leaflet map of journeys + pilgrimage routes), network analysis (NetworkX: B1 monastic cluster vs B6 institutional cluster), timeline (TimelineJS, U-curve narrative) | reviewed outputs in `buddhist-bridges/` |
| **V3-4** | Interactive DH website (static single-page: map + network + timeline + record browser) | local preview URL |

**Not started and not part of this proposal:** any visualization work (V3-3/4) or V2 deletions.

## 6. Source registry additions (append to `data_sources.py`)

12 keys, appended at the end of the registry (style: `key: ("citation", "TYPE", "url", "archive", "reliability")`):

1. `pib_sangwol2023` — PIB press release PRID=1896682 (2023-02-06): 108 Korean Buddhists walking pilgrimage hosted by Jogye Order — PRIMARY/ARCHIVAL, AUTHORITATIVE — https://pib.gov.in/PressReleasePage.aspx?PRID=1896682
2. `koreabizwire_sangwol2023` — Korea Bizwire (2023-02-10) — NEWS, POPULAR — http://koreabizwire.com/buddhist-monks-set-off-on-pilgrimage-to-india-and-nepal/240292
3. `indianarrative_sangwol2023` — India Narrative (2023-03-22): Sangwol Society 200-strong, Yogi Adityanath outreach — NEWS, POPULAR — https://www.indianarrative.com/culture/yogi-adityanath-reaches-out-to-korean-monks-in-bid-to-revive-buddhist-ties-with-asia/
4. `thefederal_sangwol2023` — The Federal: 1,167 km / 43-day walking pilgrimage — NEWS, POPULAR — https://thefederal.com/news/south-korean-buddhists-walking-in-india-for-1167-km-on-43-day-pilgrimage
5. `koreaherald_bexpo2026` — Korea Herald (2026-04-09, Sanjay Kumar): IBC–Jogye lay meeting at Bexpo 2026 — NEWS, POPULAR — https://www.koreaherald.com/article/10713686
6. `ourbuddhismworld_bexpo2026` — Our Buddhism World (2026-04-10) — NEWS, POPULAR — https://www.ourbuddhismworld.com/archives/11412
7. `buddhistdoor_gbs2026` — Buddhist Door Tea House (2026-01-18): 2nd GBS 2026, Bharat Mandapam, 24–25 Jan — NEWS, INSTITUTIONAL — https://teahouse.buddhistdoor.net/2nd-global-buddhist-summit-2026-to-bring-together-buddhist-leaders-in-new-delhi
8. `ibcworld_gbs2026` — IBC official PDF: 2nd GBS 2026 — PRIMARY, AUTHORITATIVE — https://www.ibcworld.org/docs/event_files/2nd%20GBS%202026.pdf
9. `jungto_india` — Jungto official India pilgrimage program page (36th: 14–30 Jan 2027; registration from 2026-05-25) — WEBSITE, INSTITUTIONAL — https://www.jungto.org/india/
10. `jogyesa_2014_pilgrimage` — Jogye Order official news (2014): 8 great sites + Nepal pilgrimage incl. Yeoraesunwon — WEBSITE, INSTITUTIONAL — https://www.jogyesa.kr/board/news/board_view.php?num=3148
11. `beopbo_2022_jogye` — Beopbo (2022-05-20): Jogye delegation at Mahabodhi/Sarnath — NEWS, INSTITUTIONAL — https://www.beopbo.com/news/articleView.html?idxno=309535
12. `southasiatime_piparhawa2026` — South Asia Time (2026-01-03): PM Modi inaugurates Piparhawa relics exhibition, Delhi — NEWS, POPULAR — https://www.southasiatime.com/2026/01/03/pm-modi-inaugurates-exhibition-of-lord-buddhas-relics/

*Supplementary (URL to pin at next access):* buddhism.or.kr board post on the Sangwol 43-day walking pilgrimage ending at Mahabodhi (2023).

## 7. Open questions for approval

1. **Borderline classifications** — OK to exclude the Tagore literary cluster, Gandhi, Heo Hwang-ok/Suro (kept in V2 only)? OK to ADAPT-keep Han Yong-un, Vinoba Bhave, Ko Un, Yi Nŭng-hwa, Ch'oe Nam-sŏn? OK to keep Hyŏnyu (Sri Lanka) under "South Asian Buddhist world"?
2. **EVENTS table** — confirm new `EV-####` entity and the 7 event records (E1–E7).
3. **People vs event-level actors** — record Jung Won-ju, Abhijit Halder, Pomnyun Sunim as PEOPLE, or keep them at event/institution level?
4. **Source keys** — approve appending the 12 keys in §6 (harmless to the build; used by V3-2 records).
5. **Research round** — approve one more targeted search (2026 Jogye pilgrimage; GBS 2026 Korean delegation; B4 candidates Paek Yong-sŏng/Kim Iryŏp/Pang Han-am) before or during V3-2.
6. **V2 untouched** — confirm no V2 deletions/edits during V3 work (recommended: keep V2 frozen, V3 as additive).
