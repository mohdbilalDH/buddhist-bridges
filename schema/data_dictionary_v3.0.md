# Data Dictionary — Buddhist Bridges: Mapping India–Korea Networks of People, Places, Texts, and Ideas

**Version:** 3.0 (FINAL) · **Date:** 2026-08-17 · **Status:** FROZEN — matches `buddhist-bridges/v3.0_frozen/*.csv`
**Supersedes:** `schema/data_dictionary.md` v0.1 (pilot, 2026-08-16) for the Buddhist-scope dataset. The V2 parent dataset (India–Korea Mediators, 275 records) keeps its own dictionary.

## Conventions

- **Stable IDs**: opaque, stable, never reused. `P-####` people · `PL-####` places · `T-####` travels · `TX-####` texts · `I-####` institutions · `R-####` person–person relationships · `L-####` person–place / person–text links · `EV-####` events · `EP-####` event participants · `S-####` sources.
- **Dates**: ISO 8601 (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`); `_precision` fields record granularity. `NULL` = unknown; never invent dates.
- **Uncertainty**: every record carries `confidence` (see controlled vocabularies). Uncertainty is explicit, never forced into a binary.
- **Encoding**: UTF-8. Korean names in Hangul and Hanja where attested; Revised Romanization (RR) for modern names, McCune–Reischauer (MR) for pre-1945 names, alternatives in `name_variants`.
- **Empty cells**: `NULL` (not blank, not "N/A") unless a controlled vocabulary value applies.
- **Source discipline**: every record must cite `source_ids`; "no evidence found" is recorded as a documented negative, never rewritten as "did not happen".

---

## 1. people.csv (76 rows) — one row per person

| Field | Type | Description | Allowed values / notes |
|---|---|---|---|
| person_id | TEXT | Stable unique ID | `P-0001` … |
| full_name | TEXT | Primary attested name (romanised) | e.g. `Hyecho` |
| name_variants | TEXT | Semicolon-separated alternate romanisations | e.g. `Hye-ch'o; Hyech'o; Hui Chao` |
| korean_name_hangul | TEXT | Hangul form if Korean | e.g. `혜초` |
| korean_name_hanja | TEXT | Hanja form if Korean | e.g. `慧超` |
| indian_local_name_variants | TEXT | Sanskrit/Pali/Hindi/other local forms | e.g. `Māraṇanta` |
| birth_year | INTEGER | Year of birth | `NULL` if unknown |
| birth_date_precision | TEXT | Precision of birth date | `YEAR; MONTH; DAY; CENTURY; APPROX; UNKNOWN` |
| death_year | INTEGER | Year of death | `NULL` if living/unknown |
| death_date_precision | TEXT | Precision of death date | as above |
| nationality_region | TEXT | Nationality or regional identity | controlled: see vocabularies |
| period | TEXT | Historical period bucket | `ANCIENT; MEDIEVAL; EARLY_MODERN; MODERN; CONTEMPORARY` (v3.0: MODERN = 1900–1945, CONTEMPORARY = 1945–2026) |
| profession_role | TEXT | Primary role(s) | free text, e.g. `monk; pilgrim` |
| religious_affiliation | TEXT | Buddhist school/order if applicable | e.g. `Seon (Jogye)` |
| institution_org | TEXT | Associated institution(s) | free text |
| india_connection | TEXT | Documented India connection | free text; `No documented travel to India…` for indirect-only records |
| korea_connection | TEXT | Documented Korea connection | free text |
| relationship_type | TEXT | Connection class | `DIRECT; INDIRECT; MEDIATED; UNCERTAIN` |
| physically_traveled | TEXT | Travel flag | `YES; NO; UNCERTAIN` |
| travel_summary | TEXT | Summary of travel evidence | free text |
| direction_of_influence | TEXT | Influence direction | `INDIA_TO_KOREA; KOREA_TO_INDIA; BIDIRECTIONAL; UNCERTAIN` |
| exchange_types | TEXT | Multi-value, semicolon-separated | `RELIGIOUS; LITERARY; INTELLECTUAL; POLITICAL; ARTISTIC; LINGUISTIC; CULTURAL; DIPLOMATIC; ECONOMIC; MILITARY; ACADEMIC; MUSICAL; CINEMATIC; HUMANITARIAN; JOURNALISM; OTHER` |
| evidence_of_influence | TEXT | What the influence consisted of | free text |
| historical_significance | TEXT | Why the record matters | free text |
| confidence | TEXT | Evidence strength | `HIGH; MEDIUM; LOW; SPECULATIVE` |
| notes | TEXT | Caveats, debates, documented negatives | free text |
| data_entry_date | TEXT | Entry date | ISO date |
| status | TEXT | Record status | `VERIFIED; PARTIAL; UNRESOLVED; LEGENDARY` |
| source_ids | TEXT | Semicolon-separated source keys | must exist in sources.csv |

## 2. places.csv (39 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| place_id | TEXT | Stable ID | `PL-0001` … |
| place_name | TEXT | Primary name | |
| name_variants | TEXT | Alternate names | |
| modern_country | TEXT | Modern country | |
| historical_region | TEXT | Historical region | |
| lat / lon | REAL | Coordinates | `NULL` if unknown |
| place_type | TEXT | Type | `CITY; SITE; MONASTERY; TEMPLE; UNIVERSITY; REGION; COUNTRY; MOUNTAIN; OTHER` (v3.0: `SITE` added for the 7 sacred sites) |
| notes | TEXT | Caveats | |

## 3. travels.csv (41 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| travel_id | TEXT | Stable ID | `T-0001` … |
| person_id | TEXT | Traveller | FK → people |
| origin_place_id / destination_place_id | TEXT | Endpoints | FK → places |
| intermediate_place_ids | TEXT | Waypoints, semicolon-separated | |
| travel_start_year / travel_end_year | INTEGER | Years | `NULL` if unknown |
| travel_dates_precision | TEXT | Precision | `YEAR; MONTH; DAY; APPROX; UNKNOWN` |
| purpose | TEXT | Purpose | e.g. `pilgrimage; study; diplomatic` |
| route_description | TEXT | Route | |
| evidence | TEXT | Evidence summary | |
| confidence | TEXT | | `HIGH; MEDIUM; LOW; SPECULATIVE` |
| notes | TEXT | | |

## 4. texts.csv (30 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| text_id | TEXT | Stable ID | `TX-0001` … |
| title / title_variants | TEXT | Title(s) | |
| author_person_id | TEXT | Author | FK → people |
| language | TEXT | Original language | |
| date | TEXT | Date of composition | ISO or free text |
| text_type | TEXT | Genre | e.g. `travelogue; poem; translation; biography` |
| india_relevance / korea_relevance | TEXT | Relevance to each side | |
| translation_info | TEXT | Translation history | e.g. Fuchs 1938 German translation |
| confidence | TEXT | | |
| notes | TEXT | | |

## 5. institutions.csv (31 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| institution_id | TEXT | Stable ID | `I-0001` … |
| name / name_variants | TEXT | Name(s) | |
| location_place_id | TEXT | Location | FK → places |
| founded_year | INTEGER | Founding year | `NULL` if unknown |
| institution_type | TEXT | Type | e.g. `university; monastery; order; society; museum` |
| india_relevance / korea_relevance | TEXT | Relevance | |
| notes | TEXT | | |

## 6. person_person.csv (22 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| relationship_id | TEXT | Stable ID | `R-0001` … |
| person_a_id / person_b_id | TEXT | Endpoints | FK → people |
| relationship_kind | TEXT | Nature | e.g. `TEACHER_STUDENT; MET_IN_PERSON; CORRESPONDED; TRANSLATED` |
| relationship_type | TEXT | Connection class | `DIRECT; INDIRECT; MEDIATED; UNCERTAIN` |
| evidence | TEXT | Evidence summary | |
| confidence | TEXT | | |
| notes | TEXT | | |

## 7. person_place.csv (35 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| link_id | TEXT | Stable ID | `L-0001` … |
| person_id / place_id | TEXT | Endpoints | FK |
| link_type | TEXT | Nature | e.g. `RESIDENCE; VISITED; STUDIED; WORKED; BORN; DIED` |
| year | TEXT | Year(s) | |
| confidence | TEXT | | |
| notes | TEXT | | |

## 8. person_text.csv (32 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| link_id | TEXT | Stable ID | `L-0101` … |
| person_id / text_id | TEXT | Endpoints | FK |
| link_type | TEXT | Nature | `AUTHOR; TRANSLATOR; SUBJECT; READ; INFLUENCED_BY` |
| confidence | TEXT | | |
| notes | TEXT | Evidence for the link (v3.0: all TRANSLATOR links carry evidence notes) | |

## 9. events.csv (19 rows) — contemporary developments

| Field | Type | Description | Notes |
|---|---|---|---|
| event_id | TEXT | Stable ID | `EV-0001` … |
| title | TEXT | Event name | |
| event_type | TEXT | Controlled | `PILGRIMAGE; CONFERENCE; EXHIBITION; RELIC_TRANSFER; MOU_AGREEMENT; TEMPLE_DEDICATION; TEMPLE_FOUNDATION; OTHER` |
| start_date / end_date | TEXT | ISO dates | `YYYY-MM-DD` or `YYYY-MM` |
| location_place_id | TEXT | Venue | FK → places |
| organizer_institution_ids | TEXT | Organizers | FK → institutions |
| description | TEXT | What happened | |
| significance | TEXT | Why it matters | |
| evidence | TEXT | Evidence summary | |
| confidence | TEXT | | |
| status | TEXT | | `VERIFIED; PARTIAL; UNCONFIRMED` |
| source_ids | TEXT | Sources | FK → sources |

## 10. person_event.csv (13 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| person_id | TEXT | Person | FK → people |
| event_id | TEXT | Event | FK → events |
| role | TEXT | Role | e.g. `ORGANIZER; PARTICIPANT; SPEAKER` |
| evidence / confidence / notes | TEXT | | |

## 11. event_participants.csv (10 rows) — event-level actors, NOT people records

| Field | Type | Description | Notes |
|---|---|---|---|
| participant_id | TEXT | Stable ID | `EP-0001` … |
| name | TEXT | Name | |
| hangul | TEXT | Hangul form | |
| role_hint | TEXT | Role | |
| notes | TEXT | | |

## 12. sources.csv (187 rows)

| Field | Type | Description | Notes |
|---|---|---|---|
| source_id | TEXT | Stable ID | `S-0001` … |
| source_key | TEXT | Slug used in `source_ids` fields | e.g. `sy_garak` |
| citation | TEXT | Full citation | |
| source_type | TEXT | Controlled | `PRIMARY; SECONDARY; TERTIARY; ARCHIVAL; DATABASE; NEWS; WEBSITE; OTHER` |
| url | TEXT | URL | `NULL` for print-only |
| archive_database | TEXT | Archive/database holding | |
| accessed_date | TEXT | Access date | |
| reliability | TEXT | | `INSTITUTIONAL; SCHOLARLY; POPULAR; UNKNOWN` |
| notes | TEXT | | |

## 13. classification_v3.csv (325 rows) — per-record classification

| Field | Type | Description | Notes |
|---|---|---|---|
| table | TEXT | Source table | `PEOPLE; PLACES; TRAVELS; TEXTS; INSTITUTIONS; RELS; PPL; PTX; EVENTS; PERSON_EVENT; EVENT_PARTICIPANTS` |
| record_id | TEXT | Record ID | |
| label | TEXT | Display label | |
| buddhist_relevance | TEXT | Graded relevance | `PRIMARY; SECONDARY; MEDIATOR; CONTEXTUAL; NONE` |
| scope | TEXT | Dataset membership | `KEEP; ADAPT; EXCLUDE; CONTEXT` |
| period_band | TEXT | Historical band | `B1 Ancient/early-medieval (<900); B2 Silla/Goryeo (900-1392); B3 Joseon (1392-1900); B4 Modern/colonial (1900-1945); B5 1945-1990; B6 1990-2026` |
| connection_type | TEXT | Multi-value | `PHYSICAL_MOVEMENT; TEXTUAL_TRANSMISSION; INSTITUTIONAL; INDIRECT_INFLUENCE; PERSON_ENCOUNTER; LEGENDARY` |
| movement_status | TEXT | Physical movement | `visited; worked; studied; planned; legendary; -` |
| exchange_types | TEXT | Multi-value | as people.csv |
| rationale | TEXT | Why classified this way | |

## Relationship rules (enforced by audit_v3.py)

- `relationship_type` DIRECT requires physical travel or in-person meeting; INDIRECT = influence without travel; MEDIATED = via intermediary.
- `physically_traveled=YES` requires a T-#### travel record; movement status in classification must be consistent with travel records.
- `buddhist_relevance` mapping: PRIMARY → KEEP; SECONDARY → KEEP/ADAPT; MEDIATOR → ADAPT; CONTEXTUAL → CONTEXT; NONE → EXCLUDE.
- REVIEW scope must be empty in a frozen release (v3.0: 0 REVIEW rows).