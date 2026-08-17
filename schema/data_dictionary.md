# Data Dictionary — Mediators Across Civilizations: Mapping Individual India–Korea Encounters

Version: 0.1 (pilot schema) · Date: 2026-08-16 · Status: PILOT — to be evaluated after first 30–50 records

## Conventions

- **Stable IDs**: All IDs are opaque, stable, and never reused. Format: `P-####` (people), `PL-####` (places), `T-####` (travels), `TX-####` (texts/works), `I-####` (institutions), `R-####` (person–person relationships), `L-####` (person–place / person–text links), `S-####` (sources).
- **Dates**: ISO 8601 (`YYYY`, `YYYY-MM`, `YYYY-MM-DD`). Where only a year or century is known, use that precision and set the corresponding `_precision` field. `NULL` = unknown; never invent dates.
- **Uncertainty**: Every record carries a `confidence` field (see controlled vocabularies). Uncertainty is recorded explicitly, never forced into a binary.
- **Encoding**: UTF-8. Korean names given in Hangul and Hanja where attested; romanisation follows Revised Romanization (RR) for modern names and McCune–Reischauer (MR) for pre-1945 names, with the alternative noted in `name_variants`.
- **Empty cells**: `NULL` (not blank, not "N/A") unless a controlled vocabulary value applies.

---

## 1. people.csv (MASTER TABLE — one row per person)

| Field | Type | Description | Allowed values / notes |
|---|---|---|---|
| person_id | TEXT | Stable unique ID | `P-0001` … |
| full_name | TEXT | Primary attested name (romanised) | e.g. `Hyecho` |
| name_variants | TEXT | Semicolon-separated alternate romanisations/spellings | e.g. `Hye-ch'o; Hyech'o; Hui Chao` |
| korean_name_hangul | TEXT | Hangul form if Korean | e.g. `혜초` |
| korean_name_hanja | TEXT | Hanja form if Korean | e.g. `慧超` |
| indian_local_name_variants | TEXT | Sanskrit/Pali/Hindi/other local forms | e.g. `Māraṇanta` |
| birth_year | INTEGER | Year of birth | `NULL` if unknown |
| birth_date_precision | TEXT | Precision of birth date | `YEAR; MONTH; DAY; CENTURY; APPROX; UNKNOWN` |
| death_year | INTEGER | Year of death | `NULL` if living/unknown |
| death_date_precision | TEXT | Precision of death date | as above |
| nationality_region | TEXT | Nationality or regional identity | controlled: see vocabularies |
| period | TEXT | Historical period bucket | controlled: `ANCIENT; MEDIEVAL; EARLY_MODERN; MODERN; CONTEMPORARY` |
| profession_role | TEXT | Primary role(s), semicolon-separated | e.g. `Buddhist monk; pilgrim; author` |
| religious_affiliation | TEXT | Religion where historically relevant | `BUDDHISM; HINDUISM; ISLAM; CHRISTIANITY; NONE; UNKNOWN; OTHER` |
| institution_org | TEXT | Key institution(s), semicolon-separated | use institution names as in institutions.csv |
| india_connection | TEXT | Free-text summary of the India-side connection | documentary, not inferred |
| korea_connection | TEXT | Free-text summary of the Korea-side connection | documentary, not inferred |
| relationship_type | TEXT | Core typology | `DIRECT; INDIRECT; MEDIATED; UNCERTAIN` (see vocabularies) |
| physically_traveled | TEXT | Did they physically travel between India & Korea (or via intermediates)? | `YES; NO; UNCERTAIN` |
| travel_summary | TEXT | Where/when they travelled | short summary; details in travels.csv |
| direction_of_influence | TEXT | Net direction | `INDIA_TO_KOREA; KOREA_TO_INDIA; BIDIRECTIONAL; UNCERTAIN` |
| exchange_types | TEXT | Semicolon-separated types | controlled: `RELIGIOUS; LITERARY; INTELLECTUAL; POLITICAL; ARTISTIC; LINGUISTIC; CULTURAL; DIPLOMATIC; ECONOMIC; MILITARY; ACADEMIC; MUSICAL; CINEMATIC` |
| evidence_of_influence | TEXT | Concrete documentary evidence | texts, letters, records, translations, citations |
| historical_significance | TEXT | Why this person matters for India–Korea exchange | 1–3 sentences |
| confidence | TEXT | Overall confidence in the record | `HIGH; MEDIUM; LOW; SPECULATIVE` |
| notes | TEXT | Caveats, open questions, legendary status | explicit uncertainty |
| data_entry_date | DATE | Date of entry | ISO 8601 |
| status | TEXT | Record status | `VERIFIED; PARTIAL; UNRESOLVED; LEGENDARY` |

## 2. places.csv

| Field | Type | Description |
|---|---|---|
| place_id | TEXT | `PL-####` |
| place_name | TEXT | Primary name |
| name_variants | TEXT | alt names (historical, local, romanised) |
| modern_country | TEXT | current country |
| historical_region | TEXT | e.g. `Silla; Baekje; Gaya; Tang China; British India` |
| lat / lon | REAL | coordinates if known (for future GIS) |
| place_type | TEXT | `CITY; REGION; KINGDOM; MONASTERY; PORT; MOUNTAIN; COUNTRY; OTHER` |
| notes | TEXT | |

## 3. travels.csv (movements)

| Field | Type | Description |
|---|---|---|
| travel_id | TEXT | `T-####` |
| person_id | TEXT | FK → people.person_id |
| origin_place_id | TEXT | FK → places |
| destination_place_id | TEXT | FK → places |
| intermediate_place_ids | TEXT | semicolon-separated FKs |
| travel_start_year / travel_end_year | INTEGER | |
| travel_dates_precision | TEXT | `YEAR; APPROX; UNKNOWN` |
| purpose | TEXT | `PILGRIMAGE; DIPLOMATIC; STUDY; TRADE; EXILE; MISSIONARY; WAR; OTHER; UNKNOWN` |
| route_description | TEXT | narrative of route |
| evidence | TEXT | documentary basis |
| confidence | TEXT | |
| notes | TEXT | |

## 4. texts.csv (works)

| Field | Type | Description |
|---|---|---|
| text_id | TEXT | `TX-####` |
| title | TEXT | primary title |
| title_variants | TEXT | original-language title, translations |
| author_person_id | TEXT | FK → people (may be NULL for anonymous) |
| language | TEXT | e.g. `Classical Chinese; Sanskrit; Korean; English; Bengali` |
| date | TEXT | date or century of composition |
| text_type | TEXT | `TRAVELOGUE; COMMENTARY; POEM; LETTER; TREATISE; BIOGRAPHY; TRANSLATION; NEWSPAPER_ARTICLE; SUTRA; OTHER` |
| india_relevance | TEXT | why it matters for India side |
| korea_relevance | TEXT | why it matters for Korea side |
| translation_info | TEXT | known translations |
| confidence | TEXT | |
| notes | TEXT | |

## 5. institutions.csv

| Field | Type | Description |
|---|---|---|
| institution_id | TEXT | `I-####` |
| name | TEXT | |
| name_variants | TEXT | |
| location_place_id | TEXT | FK → places |
| founded_year | INTEGER | |
| institution_type | TEXT | `MONASTERY; UNIVERSITY; GOVERNMENT; EMBASSY; COMPANY; NGO; MEDIA; OTHER` |
| india_relevance / korea_relevance | TEXT | |
| notes | TEXT | |

## 6. person_person.csv (relationships)

| Field | Type | Description |
|---|---|---|
| relationship_id | TEXT | `R-####` |
| person_a_id / person_b_id | TEXT | FKs → people |
| relationship_kind | TEXT | `TEACHER_STUDENT; CONTEMPORARY; CORRESPONDENT; TRANSLATOR_OF; SUBJECT_OF; COLLEAGUE; FAMILY; MET_IN_PERSON; INFLUENCED; DOCUMENTED; OTHER` |
| relationship_type | TEXT | `DIRECT; INDIRECT; MEDIATED; UNCERTAIN` (interaction type) |
| evidence | TEXT | documentary basis |
| confidence | TEXT | |
| notes | TEXT | |

## 7. person_place.csv

| Field | Type | Description |
|---|---|---|
| link_id | TEXT | `L-####` |
| person_id | TEXT | FK |
| place_id | TEXT | FK |
| link_type | TEXT | `BIRTH; RESIDENCE; VISITED; STUDIED; WORKED; LEGENDARY_ORIGIN; DIED; OTHER` |
| year | TEXT | |
| confidence | TEXT | |
| notes | TEXT | |

## 8. person_text.csv

| Field | Type | Description |
|---|---|---|
| link_id | TEXT | `L-####` |
| person_id | TEXT | FK |
| text_id | TEXT | FK |
| link_type | TEXT | `AUTHOR; TRANSLATOR; SUBJECT; MENTIONED_IN; COMMENTATOR; OTHER` |
| confidence | TEXT | |
| notes | TEXT | |

## 9. sources.csv (provenance log)

| Field | Type | Description |
|---|---|---|
| source_id | TEXT | `S-####` |
| citation | TEXT | full citation (author, title, publisher, year) |
| source_type | TEXT | controlled: `PRIMARY; SECONDARY; TERTIARY; ARCHIVAL; DATABASE; NEWS; WEBSITE; WIKIDATA; OTHER` |
| url | TEXT | |
| archive_database | TEXT | e.g. `Encyclopedia of Korean Culture; National Institute of Korean History; Wikidata; OpenAlex; Internet Archive` |
| accessed_date | DATE | |
| reliability | TEXT | `AUTHORITATIVE; ACADEMIC; INSTITUTIONAL; POPULAR; UNVERIFIED` |
| notes | TEXT | |

---

## Relationship typology (core rule)

- **DIRECT** = physical encounter/travel between the person and the other country (or an in-person meeting between an Indian and a Korean).
- **INDIRECT** = influence/connection without physical travel (e.g., Tagore writing about Korea without visiting).
- **MEDIATED** = influence through another person, language, text, or intermediary (e.g., a Korean reader encountering Indian thought via a Chinese translation).
- **UNCERTAIN** = evidence insufficient to classify (e.g., legendary figures like Heo Hwang-ok).

**Golden rule**: no relationship is recorded as influential without documentary evidence. Association with both countries ≠ influence.