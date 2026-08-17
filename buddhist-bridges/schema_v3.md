# Buddhist Bridges — Dataset V3 Schema (FINAL v3.0)

**Project:** Buddhist Bridges: Mapping India–Korea Networks of People, Places, Texts, and Ideas
**Status:** FINAL — v3.0 (2026-08-17). Frozen with the dataset; see `buddhist-bridges/v3.0_frozen/VERSION.md`.
**Supersedes:** v0.2 proposal (2026-08-17); `schema/data_dictionary.md` and `schema/controlled_vocabularies.md` for the Buddhist-scope dataset. Final dictionary and vocabularies: `schema/data_dictionary_v3.0.md`, `schema/controlled_vocabularies_v3.0.md`. The V2 dataset (India–Korea Mediators, 275 records) remains intact as the parent dataset; V3 is a Buddhist-scope subset + extension (see `classification_v3.csv`).

**v3.0 freeze changes (2026-08-17):** `SITE` added to PLACE_TYPES (7 sacred sites re-typed MONASTERY → SITE); 6 PTX TRANSLATOR links gained evidence notes; P-0037/P-0073 period MODERN → CONTEMPORARY; audit_v3.py passes 0 errors / 0 warnings; REVIEW scope = 0.

**What changed in v0.2** (per the user's methodological pass):
1. Binary KEEP/EXCLUDE replaced by the **graded `buddhist_relevance` scale** (PRIMARY / SECONDARY / MEDIATOR / CONTEXTUAL / NONE) — people are no longer excluded simply because Buddhism was not their primary identity.
2. **Multiple connection types** per record (previously one forced type).
3. **Movement statuses** (`planned / visited / worked / studied / legendary`) replace the binary travel flag.
4. **EVENTS table** formalised as the home for contemporary developments (pilgrimages, conferences, MOUs, openings) — contemporary actors live at event level, not forced into the historical person model.
5. Research round results folded in: Bunhwangsa India timeline (groundbreaking 2020-03-28, dedication 2022-05), Yeoraesunwon (founded ~2000–01, abbot Wonman, Dharma School), GBS 2023 / 2nd GBS 2026 / ICYBS 2025 (Korean participation unconfirmed), Delhi University as the main Indian host of Korean Buddhist-students.

---

## 1. Purpose and scope

V3 captures every **Buddhist-relevant** India–Korea connection across a continuous historical framework — from the earliest recorded contacts (4th c. CE) through **2026**. It is not limited to ancient/medieval monks: it also records modern Buddhist intellectuals, contemporary monastic institutions, organised pilgrimages, conferences, exhibitions, relic and MOU events, and the organisations behind them.

Scope rules:
- **Buddhist-only.** A record is in scope only when the documented India–Korea connection is Buddhist: monks/pilgrims/teachers/disciples, translators of Buddhist texts, Buddhist scholarship, monasteries/temples, pilgrimage routes, Buddhist institutions, or contemporary Buddhist exchanges/events.
- **Graded relevance, not binary.** Whether a person "is Buddhist" is not the question; the question is their *documented role in the Buddhist exchange*. A non-Buddhist who was a documented channel (Tagore, Gandhi, Vinoba Bhave) is a **MEDIATOR** and stays in V3. A person with no Buddhist channel at all (diplomacy, military, economy, literature without Buddhist content) is **NONE** and stays in V2 only.
- **No inferred links.** A person's Buddhism alone is not enough; an Indian connection alone is not enough. Both sides of the relation must be documented by an authoritative source.
- **CONTEXTUAL records** (legends, literary circles, partly-relevant surveys) are carried as labelled reference-only rows (scope CONTEXT), never asserted as fact.
- The **connection-type ladder** (section 4) is recorded per connection; legendary material is retained only as labelled context.

## 2. Period bands (continuous historical framework)

| Band | Range | Content emphasis |
|------|-------|------------------|
| B1 | Ancient / early-medieval (<900) | Silla–Tang–India monks; Marananta, Gyeomik, Yijing cohort, Hyecho, Woncheuk, Wŏnhyo; Nalanda/Bodh Gaya |
| B2 | Silla/Goryeo (900–1392) | Iryŏn; Dhyānabhadra, Naong, Hoeamsa; Goryeo Seon formation |
| B3 | Joseon (1392–1900) | (near-empty in Buddhist scope — see gap analysis; re-audited v0.2) |
| B4 | Modern/colonial (1900–1945) | Yi Nŭng-hwa, Ch'oe Nam-sŏn, Han Yong-un; Buddhist historiography; Tagore as MEDIATOR channel (Lamp of the East, 1929) |
| B5 | 1945–1990 | Pŏpchŏng (1971), Vinoba Bhave, Gandhi as MEDIATOR; post-war re-engagement |
| B6 | 1990–2026 | Delhi University monks (Wookwan, Gakseong, Hyoseok, U Myeong-ju), Buddhavara/Bunhwangsa India (2020–22), Yeoraesunwon, Lokesh Chandra, 2014–2026 pilgrimages, Bexpo 2026, GBS 2026, Jungto program, DU–BGICBS MOU 2026 |

Every record carries exactly one band (the band of its principal activity/exchange). Links inherit the band of their endpoint person unless an explicit band is set.

## 3. Entity model (8 tables)

V3 reuses the V2 table shapes (Python modules + `build_dataset.py` as source of truth; stable prefixed IDs) and adds one new entity table.

| Table | ID prefix | Notes |
|-------|-----------|-------|
| PEOPLE | `P-` | Buddhist actors: monks, bhikkhunis, pilgrims, teachers, translators, scholars, lay leaders, mediator channel figures |
| PLACES | `PL-` | Sacred sites, monasteries, universities, kingdoms, route nodes, modern venues |
| JOURNEYS (renamed TRAVELS) | `T-` | Pilgrimages and all documented physical movement |
| TEXTS | `TX-` | Sutras, commentaries, histories, essays, translations, official records |
| INSTITUTIONS | `I-` | Monasteries, orders, universities, centres, lay societies, orgs |
| EVENTS *(new)* | `EV-` | Dated contemporary developments: pilgrimages, conferences, exhibitions, relic transfers, MOUs, temple foundations/openings |
| RELATIONSHIPS (RELS) | `R-` | teacher–student, encounter, translation, influence, documentation |
| PERSON–PLACE / PERSON–TEXT links | `L-` | Existing PPL/PTX link tables (kept as-is, reclassified) |

**EVENTS table fields** (new; confirmed home for contemporary developments — contemporary actors such as Jung Won-ju and Abhijit Halder are recorded as `participant_person_ids`, not forced into PEOPLE):

| Field | Notes |
|-------|-------|
| `event_id` | `EV-####` |
| `title` | free text |
| `event_type` | vocabulary below |
| `start_date` / `end_date` | precision-tagged dates |
| `event_location_place_id` | PL-#### reference (e.g., PL-0010 Bodh Gaya, PL-0027 New Delhi) |
| `organizer_institution_ids` | I-#### references (e.g., Jogye Order, IBC, Bunhwangsa India, Jungto) |
| `participant_person_ids` | P-#### references (role-tagged: leader/organizer/participant) |
| `description` / `significance` | free text |
| `evidence` / `confidence` / `status` | provenance discipline (section 8) |
| `source_ids` | SOURCES registry keys |

Suggested `event_type` vocabulary: `PILGRIMAGE`, `CONFERENCE`, `EXHIBITION`, `RELIC_TRANSFER`, `MOU_AGREEMENT`, `TEMPLE_FOUNDATION`, `TEMPLE_DEDICATION`, `DONATION`, `FESTIVAL`, `LECTURE_SERIES`, `OTHER`.

**Confirmed seed events for EVENTS** (from proposal_v3.md + v0.2 research round; full details in `proposal_v3.md`):

| ID | Event | Date | Where |
|----|-------|------|-------|
| E1 | Sangwol 1167-km / 43-day pilgrimage (108+ monastics) | 2023 | Bodh Gaya → Sarnath (PIB-documented) |
| E2 | Bexpo 2026 Buddhist lounge: IBC–Jogye lay exchange | 2026-04-04 | New Delhi |
| E3 | 2nd Global Buddhist Summit | 2026-01-24/25 | New Delhi — **no Korean confirmed** |
| E4 | Jungto annual India program | annual (35th early 2026; 36th 2027-01-14~30) | Bodh Gaya region |
| E5 | Delhi University – BGICBS MOU | 2026-04-23 | Delhi |
| E6 | Jogye delegation Sarnath → Bodh Gaya | 2022-05 | Sarnath/Bodh Gaya |
| E7 | Jogye pilgrimage: 8 Indian sites + Nepal incl. Yeoraesunwon | 2014 | India/Nepal |
| E8 | Bunhwangsa India groundbreaking | 2020-03-28 | Bodh Gaya |
| E9 | Bunhwangsa India dedication (대웅보전 준공식; 150-person Jogye delegation led by 총무원장 Wonhaeng) | 2022-05 | Bodh Gaya |
| E10 | GBS 2023 | 2023 (Nov) | New Delhi — Korea presence unconfirmed |
| E11 | ICYBS 2025 (3rd Int'l Conf. of Young Buddhist Scholars, IBC/Ministry of Culture) | 2025-08 | New Delhi — Korea unconfirmed |

## 4. Connection-type ladder (multi-valued)

Each record carries one or more `connection_type` values — the **documented channels** of the exchange, strongest to weakest (by weight of evidence, not value). Multiple values are joined in the CSV with `"; "` (e.g., Dhyānabhadra: `PHYSICAL_MOVEMENT; INSTITUTIONAL; PERSON_ENCOUNTER`).

1. **PHYSICAL_MOVEMENT** — documented travel of a person between India and Korea (e.g., Hyecho's pilgrimage; Gakseong's 1992–98 Delhi study; Pŏpchŏng's 1971 trip).
2. **PERSON_ENCOUNTER** — documented person-to-person meeting without (necessarily) residence (e.g., Naong–Jikong meetings; Pŏpchŏng–Vinoba Bhave 1971).
3. **INSTITUTIONAL** — institutional/organisational channel: temples, universities, orders, MOUs (e.g., Nalanda as destination institution; Hoeamsa; Bunhwangsa India; DU–BGICBS MOU 2026).
4. **TEXTUAL_TRANSMISSION** — texts, translations, commentaries, or teachings as the channel (e.g., Wŏnhyo's Haedong-so; Lokesh Chandra's *Morning Calm*).
5. **INDIRECT_INFLUENCE** — documented influence with no direct channel (e.g., Tagore's lyricism on Han Yong-un; Gandhi's words opening *Muso-yu*).
6. **LEGENDARY** — traditional/legendary narrative, always flagged and never asserted (e.g., Heo Hwang-ok; Suro).

The V2 `rel` field (DIRECT/INDIRECT/MEDIATED/UNCERTAIN) is retained for backward compatibility; the ladder is the primary analytical axis in V3.

## 5. Graded relevance scale and movement statuses (new in v0.2)

### 5.1 `buddhist_relevance` (graded decision mechanism)

| Grade | Meaning | Scope (derived) |
|-------|---------|-----------------|
| **PRIMARY** | Buddhist identity: monks/nuns/ordained practitioners, Buddhist institutions, sacred sites, core Buddhist texts | KEEP |
| **SECONDARY** | Significant Buddhist activity, primary identity elsewhere (scholars of Buddhism, Buddhist-themed writers, partly-Buddhist institutions/texts) | ADAPT |
| **MEDIATOR** | Not Buddhist themselves, but a documented channel in the India–Korea Buddhist exchange (Tagore, Gandhi, Vinoba, hosts) | ADAPT |
| **CONTEXTUAL** | Relevant background/context, no direct Buddhist channel (legends, literary circles, partly-relevant surveys) | CONTEXT (reference-only) |
| **NONE** | No Buddhist relevance (V2-only records) | EXCLUDE |

Mapping is validated by the generator (`build_classification.py`); REVIEW is an explicit override for records pending research.

### 5.2 Movement statuses

`movement_status` describes the person's movement relative to the India–Korea exchange (replaces the V2 binary `travel` YES/NO/UNCERTAIN, kept for backward compatibility):

| Status | Meaning | Examples |
|--------|---------|----------|
| `planned` | intended but not (documented as) realised | Tagore's Seoul visit 1929 (never made) |
| `visited` | travelled, no long-term residence | Hyecho; Pŏpchŏng 1971; Ko Un 1990s/2019 |
| `worked` | travelled and resided/worked | Marananta in Baekje; Dhyānabhadra in Goryeo; Buddhavara at Bodh Gaya |
| `studied` | travelled for study/ordination | Gyeomik (Sangana); Gakseong (DU 1992–98); Hyoseok (Pune/Delhi) |
| `legendary` | movement attested only in legend | Heo Hwang-ok; Suro |
| `-` | not applicable (no India–Korea movement) | Woncheuk; Wŏnhyo; Han Yong-un |

## 6. New fields (user-specified) — mapping to tables

| Field | Table(s) | Type / vocabulary (proposal) |
|-------|----------|------------------------------|
| `buddhist_relevance` | all tables | PRIMARY / SECONDARY / MEDIATOR / CONTEXTUAL / NONE |
| `movement_status` | PEOPLE, JOURNEYS, PPL | planned / visited / worked / studied / legendary / - |
| `buddhist_tradition` | PEOPLE | Theravada / Mahayana / Vajrayana-Esoteric / Seon-Chan / Vinaya / Yogacara / Huayan-Hwaeom / Pure Land / mixed |
| `school_lineage` | PEOPLE | free text (e.g., Amoghavajra line; Jogye Order; Songgwangsa lineage; BGICBS) |
| `monastery_temple` | PEOPLE, INSTITUTIONS | ID reference to PLACE or INSTITUTION (e.g., Ximing, Hoeamsa, Bunhwangsa India, Bongnyeongsa) |
| `teacher` / `disciple` | PEOPLE, RELS | person ID reference(s); kept in sync with R-#### records (kind TEACHER_STUDENT) |
| `pilgrimage` | PEOPLE, JOURNEYS | YES/NO + link to T-####; purpose vocabulary reuses V2 (`PILGRIMAGE`) |
| `text` / `translation` | TEXTS, PTX | existing TX-#### / L-#### structure |
| `transmission_route` | JOURNEYS, TEXTS | route string (e.g., `SEA_BLUE_WATER`; `OVERLAND_SILK_ROAD`; `VIA_CHINA`; `VIA_TIBET`; `MODERN_AIR`) |
| `doctrinal_knowledge_exchange` | RELS, PEOPLE | YES/NO + free text; the specific doctrine/knowledge exchanged |
| `institutional_exchange` | RELS, INSTITUTIONS, EVENTS | YES/NO + free text |
| `contemporary_event` | EVENTS | event ID reference |
| `event_date` / `event_location` | EVENTS | date (precision-tagged) / PL-#### reference |

Proposed `transmission_route` vocabulary: `VIA_CHINA`, `VIA_TIBET`, `SEA_INDIA_BAEKJE`, `SEA_BAEKJE_INDIA`, `OVERLAND_SILK_ROAD`, `VIA_JAPAN`, `MODERN_AIR`, `UNKNOWN`.

## 7. Controlled vocabularies (reused from V2, unchanged)

`relationship_type` {DIRECT, INDIRECT, MEDIATED, UNCERTAIN} · `exchange_types` {RELIGIOUS, LITERARY, INTELLECTUAL, POLITICAL, ARTISTIC, LINGUISTIC, CULTURAL, DIPLOMATIC, ECONOMIC, MILITARY, ACADEMIC, MUSICAL, CINEMATIC, HUMANITARIAN, JOURNALISM, OTHER} · `direction` {INDIA_TO_KOREA, KOREA_TO_INDIA, BIDIRECTIONAL, UNCERTAIN} · `confidence` {HIGH, MEDIUM, LOW, SPECULATIVE} · `status` {VERIFIED, PARTIAL, UNRESOLVED, LEGENDARY} · `physically_traveled` {YES, NO, UNCERTAIN} · periods (V2) retained for compat.

## 8. Classification & migration rules (v0.2 numbers)

Per `classification_v3.csv` (generated from `buddhist-bridges/classification_v3.py`; 275 records, 0 errors/0 warnings):

| Scope | Meaning | Rows | People |
|-------|---------|------|--------|
| KEEP | PRIMARY — carry as-is | 117 | 29 |
| ADAPT | SECONDARY/MEDIATOR — carry with reframing | 27 | 7 |
| CONTEXT | CONTEXTUAL — reference-only rows | 46 | 10 |
| EXCLUDE | NONE — V2 only | 83 | 22 |
| REVIEW | pending research | 2 | 2 (P-0068 Sŏ Chŏng-ju, P-0070 Kim Chi-ha) |

Relevance totals: PRIMARY=117, SECONDARY=11, MEDIATOR=18, CONTEXTUAL=46, NONE=83. Movement totals (non-"-"): visited=42, studied=29, worked=33, legendary=3, planned=1.

Key grading decisions vs v0.1:
- Tagore P-0030: EXCLUDE → **MEDIATOR/ADAPT** (Lamp of the East channel; planned Seoul 1929)
- Han Yong-un P-0034: ADAPT → **PRIMARY/KEEP** (he is a monk; the graded scale recognises his Buddhist identity)
- Gandhi P-0038: EXCLUDE → **MEDIATOR/ADAPT** (Muso-yu channel via Pŏpchŏng)
- Vinoba Bhave P-0071: KEEP → **MEDIATOR/ADAPT** (documented counterpart, not Buddhist himself)
- Tagore circle (P-0031..P-0033, P-0035, P-0036), Ham Sŏk-hŏn P-0037, Vyjayanti P-0059, P-0061, Heo Hwang-ok/Suro: EXCLUDE → **CONTEXT** (reference-only)
- Diplomats/military/economists/Korean-studies scholars/translators: unchanged **NONE/EXCLUDE**

Rules: relationships and links inherit their people's relevance where content matches; a link is excluded when its *content* is non-Buddhist even if the person is in scope (e.g., Ch'oe Nam-sŏn's 1916 Tokyo travel T-0016 is ADAPT only as part of his Buddhist-history channel while his *Chosŏn Pulgyo* TX-0016 is KEEP). EXCLUDE records are never deleted from V2.

## 9. Provenance discipline

Unchanged from V2: every record cites `source_ids` from the `SOURCES` registry (`data_sources.py`); new contemporary sources are appended as new keys. Any record asserted for 2024–2026 must be traceable to an official/primary or named institutional source; unconfirmed claims (e.g., Korean delegation at GBS 2023/2026 or ICYBS 2025, a distinct "2026 Jogye pilgrimage", Paek Yong-sŏng's or Kim Iryŏp's India links) are recorded as REVIEW/UNRESOLVED until sourced. Pending source keys from the v0.2 research round are listed in `collect_next.md`.
