# Controlled Vocabularies — Buddhist Bridges Dataset V3.0 (FINAL)

**Version:** 3.0 · **Date:** 2026-08-17 · **Status:** FROZEN
**Supersedes:** `schema/controlled_vocabularies.md` v0.1 (2026-08-16) for the Buddhist-scope dataset.
These are the ONLY allowed values for the corresponding fields in `buddhist-bridges/v3.0_frozen/*.csv`.

## 1. relationship_type (people.csv, person_person.csv)

| Value | Definition |
|---|---|
| `DIRECT` | Physical encounter/travel: travelled between India and Korea, or met an Indian/Korean in person in a third country |
| `INDIRECT` | Influence or connection without physical travel (wrote about the other country, was read there, shaped perceptions) |
| `MEDIATED` | Influence through an intermediary: another person, a language, a text, a translation, an institution |
| `UNCERTAIN` | Evidence insufficient to classify; record uncertainty explicitly in notes |

## 2. exchange_types (people.csv, classification_v3.csv)

`RELIGIOUS` · `LITERARY` · `INTELLECTUAL` · `POLITICAL` · `ARTISTIC` · `LINGUISTIC` · `CULTURAL` · `DIPLOMATIC` · `ECONOMIC` · `MILITARY` · `ACADEMIC` · `MUSICAL` · `CINEMATIC` · `HUMANITARIAN` · `JOURNALISM` · `OTHER`
(multi-value, semicolon-separated. v3.0 usage: RELIGIOUS=35, INTELLECTUAL=21, ACADEMIC=9, CULTURAL=7, LITERARY=6, POLITICAL=3, LINGUISTIC=3, JOURNALISM=1 among carried rows)

## 3. period (people.csv)

| Value | Range (approx.) |
|---|---|
| `ANCIENT` | before 900 CE (Three Kingdoms / Silla / Gaya / early Goryeo) |
| `MEDIEVAL` | 900–1392 (Goryeo) |
| `EARLY_MODERN` | 1392–1900 (Joseon) |
| `MODERN` | 1900–1945 (colonial era) |
| `CONTEMPORARY` | 1945–2026 |

v3.0 note: P-0037 Ham Sok-hon and P-0073 Hwang Su-yŏng moved MODERN → CONTEMPORARY (both active post-1945; band B5).

## 4. direction_of_influence (people.csv)

`INDIA_TO_KOREA` · `KOREA_TO_INDIA` · `BIDIRECTIONAL` · `UNCERTAIN`

## 5. confidence

| Value | Definition |
|---|---|
| `HIGH` | Multiple independent authoritative sources; primary evidence |
| `MEDIUM` | One authoritative source or consistent secondary sources |
| `LOW` | Single secondary/popular source; details uncertain |
| `SPECULATIVE` | Scholarly hypothesis or legend; explicitly flagged |

## 6. status (people.csv, events.csv)

People: `VERIFIED` · `PARTIAL` · `UNRESOLVED` · `LEGENDARY`
Events: `VERIFIED` · `PARTIAL` · `UNCONFIRMED`

## 7. source_type (sources.csv)

`PRIMARY` (contemporary document, inscription, letter, travelogue) · `SECONDARY` (scholarly monograph/article) · `TERTIARY` (encyclopedia, reference work) · `ARCHIVAL` (archive holding) · `DATABASE` (structured database: Wikidata, OpenAlex, DBpedia) · `NEWS` (newspaper/periodical) · `WEBSITE` (institutional website) · `OTHER`

## 8. reliability (sources.csv)

`INSTITUTIONAL` · `SCHOLARLY` · `POPULAR` · `UNKNOWN`

## 9. place_type (places.csv)

`CITY` · `SITE` · `MONASTERY` · `TEMPLE` · `UNIVERSITY` · `REGION` · `COUNTRY` · `MOUNTAIN` · `OTHER`

v3.0 change: `SITE` added (2026-08-17). The 7 sacred sites re-typed MONASTERY → SITE: PL-0010 Bodh Gaya, PL-0032 Sarnath, PL-0033 Kushinagar, PL-0034 Lumbini, PL-0035 Vaishali, PL-0036 Shravasti, PL-0037 Rajgir.

## 10. link_type (person_place.csv)

`RESIDENCE` · `VISITED` · `STUDIED` · `WORKED` · `BORN` · `DIED` · `OTHER`

## 11. link_type (person_text.csv)

`AUTHOR` · `TRANSLATOR` · `SUBJECT` · `READ` · `INFLUENCED_BY`

## 12. relationship_kind (person_person.csv)

`TEACHER_STUDENT` · `MET_IN_PERSON` · `CORRESPONDED` · `TRANSLATED` · `OTHER`

## 13. event_type (events.csv)

`PILGRIMAGE` · `CONFERENCE` · `EXHIBITION` · `RELIC_TRANSFER` · `MOU_AGREEMENT` · `TEMPLE_DEDICATION` · `TEMPLE_FOUNDATION` · `OTHER`

v3.0 usage (19 events): PILGRIMAGE=7, CONFERENCE=3, EXHIBITION=3, RELIC_TRANSFER=2, MOU_AGREEMENT=2, TEMPLE_DEDICATION=1, TEMPLE_FOUNDATION=1.

## 14. role (person_event.csv)

`ORGANIZER` · `PARTICIPANT` · `SPEAKER` · `OTHER`

## 15. buddhist_relevance (classification_v3.csv)

| Value | Definition | Scope mapping |
|---|---|---|
| `PRIMARY` | Buddhism is the core of the connection | KEEP |
| `SECONDARY` | Buddhism is a significant but not sole element | KEEP / ADAPT |
| `MEDIATOR` | Person/entity enabled Buddhist exchange without being Buddhist themselves | ADAPT |
| `CONTEXTUAL` | Background context for the network | CONTEXT |
| `NONE` | No Buddhist relevance | EXCLUDE |

## 16. scope (classification_v3.csv)

`KEEP` · `ADAPT` · `EXCLUDE` · `CONTEXT`

## 17. period_band (classification_v3.csv)

| Band | Range (as stored in classification_v3.csv) |
|---|---|
| `B1 Ancient/early-medieval (<900)` | before 900 CE (Three Kingdoms / Silla / Gaya) |
| `B2 Silla/Goryeo (900-1392)` | 900–1392 (Goryeo) |
| `B3 Joseon (1392-1900)` | 1392–1900 (Joseon) |
| `B4 Modern/colonial (1900-1945)` | 1900–1945 (colonial era) |
| `B5 1945-1990` | 1945–1990 (post-liberation) |
| `B6 1990-2026` | 1990–2026 (contemporary) |

## 18. connection_type (classification_v3.csv)

`PHYSICAL_MOVEMENT` · `TEXTUAL_TRANSMISSION` · `INSTITUTIONAL` · `INDIRECT_INFLUENCE` · `PERSON_ENCOUNTER` · `LEGENDARY` · `-` (multi-value, semicolon-separated)

## 19. movement_status (classification_v3.csv)

`visited` · `worked` · `studied` · `planned` · `-` (no physical movement; includes legendary figures whose movement is not historical fact)